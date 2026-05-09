#!/usr/bin/env python3
"""
strategy_predictor.py - Predict which strategies will persist in top20

Uses ML to predict which strategies appearing in early _top10_history
will remain in the final _top20 at end of day.

Usage:
    python strategy_predictor.py --predict          # Show current predictions
    python strategy_predictor.py --analyze          # Analyze features
    python strategy_predictor.py --train            # Train model on historical data
    python strategy_predictor.py --evaluate         # Evaluate model performance

[2026-03-24] Strategy persistence prediction using ML
"""

import argparse
import json
import pickle
import statistics
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

# Configuration
SCRIPT_DIR = Path(__file__).resolve().parent
JSON_ROOT = SCRIPT_DIR / "json"
MODEL_PATH = SCRIPT_DIR / "strategy_predictor_model.pkl"
CONFIG_PATH = SCRIPT_DIR / "config.json"
RL_MODEL_PATH = SCRIPT_DIR / "strategy_rl_model.pkl"

# Pick Now Thresholds (configurable)
DEFAULT_PICK_NOW_CONFIG = {
    "min_appearances": 20,
    "min_net_trend": 100,
    "min_snapshots": 60,
    "min_net_at_pick": 600,
    "max_net_at_pick": 799,
    "max_trade_count": 19,
    "exclude_strategy_string": "breakout_Rev_",
    "dead_zone_start_snapshot": 85,
    "dead_zone_end_snapshot": 99
}


def load_pick_now_config() -> Dict[str, Any]:
    """Load pick_now configuration from config.json or use defaults."""
    config = DEFAULT_PICK_NOW_CONFIG.copy()
    try:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                full_config = json.load(f)
            pick_config = full_config.get("pick_now", {})
            for key in DEFAULT_PICK_NOW_CONFIG:
                if key in pick_config and pick_config[key] is not None:
                    config[key] = pick_config[key]
    except Exception:
        pass
    return config


# =============================================================================
# Data Loading
# =============================================================================

def get_latest_date_dir(product_type: str = "forex", run_mode: str = "live") -> Optional[Path]:
    """Find the latest date directory."""
    base_path = JSON_ROOT / run_mode / product_type
    if not base_path.exists():
        return None

    date_dirs = []
    for item in base_path.iterdir():
        if item.is_dir() and len(item.name) == 10 and item.name[4] == '-':
            date_dirs.append(item)

    return sorted(date_dirs, key=lambda x: x.name, reverse=True)[0] if date_dirs else None


def load_json_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load {filepath}: {e}")
        return None


def load_day_data(date_dir: Path) -> Dict[str, Any]:
    """Load all relevant data files for a day."""
    return {
        "date_dir": str(date_dir),
        "date": date_dir.name,
        "top10_history": load_json_file(date_dir / "_top10_history.json"),
        "summary_net": load_json_file(date_dir / "_summary_net.json"),
        "top20": load_json_file(date_dir / "_top20.json"),
    }


# =============================================================================
# Feature Extraction
# =============================================================================

def extract_history_features(history_data: Dict, strategy: str, product: str) -> Dict[str, float]:
    """Extract features from _top10_history.json for a strategy."""
    if not history_data or "history" not in history_data:
        return {}

    key = f"{strategy}|{product}"
    snapshots = history_data["history"]
    total_snapshots = len(snapshots)

    appearances = []
    nets = []

    for i, snapshot in enumerate(snapshots):
        for entry in snapshot.get("top10", []):
            if entry["strategy"] == strategy and entry["product"] == product:
                appearances.append(i)
                nets.append(entry.get("net", 0))
                break

    if not appearances:
        return {}

    # Calculate streak (longest consecutive appearance)
    max_streak = 1
    current_streak = 1
    for i in range(1, len(appearances)):
        if appearances[i] == appearances[i-1] + 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1

    return {
        "appearances": len(appearances),
        "appearance_ratio": len(appearances) / total_snapshots if total_snapshots > 0 else 0,
        "first_appearance_idx": appearances[0],
        "last_appearance_idx": appearances[-1],
        "appearance_streak": max_streak,
        "appearance_recency": total_snapshots - appearances[-1] - 1,
        "net_in_history": nets[-1] if nets else 0,
        "net_change_history": nets[-1] - nets[0] if len(nets) > 1 else 0,
    }


def extract_summary_features(summary_data: Dict, strategy: str, product: str) -> Dict[str, float]:
    """Extract features from _summary_net.json for a strategy."""
    if not summary_data or "strategies" not in summary_data:
        return {}

    strategies = summary_data.get("strategies", {})
    if strategy not in strategies:
        return {}

    products = strategies[strategy]
    if product not in products:
        return {}

    snapshots = products[product]
    if not snapshots:
        return {}

    # Extract time series
    nets = [s.get("net", 0) for s in snapshots]
    buy_nets = [s.get("buy_net", 0) for s in snapshots]
    sell_nets = [s.get("sell_net", 0) for s in snapshots]
    buy_pcts = [s.get("buyPercent", 0) for s in snapshots]
    sell_pcts = [s.get("sellPercent", 0) for s in snapshots]

    # Calculate features
    net_volatility = statistics.stdev(nets) if len(nets) > 1 else 0

    # Net momentum (recent trend)
    recent_n = min(5, len(nets))
    if recent_n > 1:
        recent_nets = nets[-recent_n:]
        net_momentum = (recent_nets[-1] - recent_nets[0]) / recent_n
    else:
        net_momentum = 0

    latest = snapshots[-1]
    buy_count = latest.get("b_c", 0)
    sell_count = latest.get("s_c", 0)
    total_trades = buy_count + sell_count

    return {
        "net": nets[-1],
        "max_net": max(nets),
        "min_net": min(nets),
        "net_trend": nets[-1] - nets[0],
        "net_volatility": net_volatility,
        "net_momentum": net_momentum,
        "buy_net": buy_nets[-1],
        "sell_net": sell_nets[-1],
        "buy_sell_balance": abs(buy_nets[-1] - sell_nets[-1]),
        "buy_win_pct": statistics.mean([p for p in buy_pcts if p > 0]) if any(p > 0 for p in buy_pcts) else 0,
        "sell_win_pct": statistics.mean([p for p in sell_pcts if p > 0]) if any(p > 0 for p in sell_pcts) else 0,
        "total_trades": total_trades,
        "snapshot_count": len(snapshots),
    }


def extract_all_features(data: Dict, strategy: str, product: str) -> Dict[str, float]:
    """Extract all features for a strategy-product pair."""
    history_features = extract_history_features(data.get("top10_history"), strategy, product)
    summary_features = extract_summary_features(data.get("summary_net"), strategy, product)

    # Combine features
    features = {**history_features, **summary_features}

    # Add derived features
    if features:
        appearances = features.get("appearances", 0)
        total_snapshots = len(data.get("top10_history", {}).get("history", [])) or 1

        features["consistency_score"] = appearances / total_snapshots
        features["stability_score"] = 1 / (1 + features.get("net_volatility", 0) / 100)

        max_net = max(abs(features.get("buy_net", 0)), abs(features.get("sell_net", 0)), 1)
        features["balance_score"] = 1 - features.get("buy_sell_balance", 0) / max_net

        features["win_rate_combined"] = (features.get("buy_win_pct", 0) + features.get("sell_win_pct", 0)) / 2
        features["is_trending_up"] = 1 if features.get("net_trend", 0) > 0 else 0

    return features


def get_all_strategies_in_history(history_data: Dict) -> List[Tuple[str, str]]:
    """Get all unique strategy-product pairs from history."""
    if not history_data or "history" not in history_data:
        return []

    strategies = set()
    for snapshot in history_data["history"]:
        for entry in snapshot.get("top10", []):
            strategies.add((entry["strategy"], entry["product"]))

    return list(strategies)


def get_current_top20(top20_data: Dict) -> set:
    """Get current top20 as a set of strategy|product keys."""
    if not top20_data or "top20" not in top20_data:
        return set()

    return {f"{e['strategy']}|{e['product']}" for e in top20_data["top20"]}


# =============================================================================
# Model (Simple Rule-Based + Gradient Boosting)
# =============================================================================

FEATURE_NAMES = [
    "appearances", "appearance_ratio", "first_appearance_idx", "appearance_streak",
    "appearance_recency", "net", "max_net", "net_trend", "net_volatility",
    "net_momentum", "buy_sell_balance", "buy_win_pct", "sell_win_pct",
    "total_trades", "consistency_score", "stability_score", "balance_score",
    "win_rate_combined", "is_trending_up"
]


def features_to_vector(features: Dict[str, float]) -> np.ndarray:
    """Convert features dict to numpy vector."""
    return np.array([features.get(name, 0) for name in FEATURE_NAMES])


def rule_based_predict(features: Dict[str, float]) -> Tuple[float, str]:
    """
    Simple rule-based prediction based on data analysis.
    Returns (probability, reason).
    """
    appearances = features.get("appearances", 0)
    net_trend = features.get("net_trend", 0)
    consistency = features.get("consistency_score", 0)
    volatility = features.get("net_volatility", 0)
    win_rate = features.get("win_rate_combined", 0)

    score = 0
    reasons = []

    # Appearances (most important)
    if appearances >= 20:
        score += 0.35
        reasons.append(f"high consistency ({appearances} appearances)")
    elif appearances >= 10:
        score += 0.20
        reasons.append(f"moderate consistency ({appearances} appearances)")
    elif appearances >= 5:
        score += 0.10
    else:
        score -= 0.10
        reasons.append(f"low consistency ({appearances} appearances)")

    # Net trend
    if net_trend > 200:
        score += 0.25
        reasons.append(f"strong uptrend (+{net_trend:.0f})")
    elif net_trend > 0:
        score += 0.15
        reasons.append(f"positive trend (+{net_trend:.0f})")
    elif net_trend < -100:
        score -= 0.20
        reasons.append(f"downtrend ({net_trend:.0f})")

    # Volatility (lower is better)
    if volatility < 150:
        score += 0.15
        reasons.append("stable performance")
    elif volatility > 300:
        score -= 0.10
        reasons.append("high volatility")

    # Win rate
    if win_rate > 60:
        score += 0.15
        reasons.append(f"high win rate ({win_rate:.0f}%)")
    elif win_rate < 40:
        score -= 0.10
        reasons.append(f"low win rate ({win_rate:.0f}%)")

    # Normalize to 0-1
    probability = max(0, min(1, 0.5 + score))

    return probability, "; ".join(reasons) if reasons else "neutral signals"


# =============================================================================
# Reinforcement Learning Environment
# =============================================================================

class StrategySelectionEnv:
    """
    RL environment for strategy selection.

    State: Feature vector for a strategy
    Action: 0 = skip, 1 = select
    Reward: +1 if selected strategy ends in top20, -1 if not
    """

    def __init__(self, historical_days: List[Dict] = None):
        self.historical_days = historical_days or []
        self.current_day_idx = 0
        self.current_strategy_idx = 0
        self.strategies = []
        self.selected = []
        self.n_features = len(FEATURE_NAMES)

    def reset(self) -> np.ndarray:
        """Start a new episode (new trading day)."""
        if not self.historical_days:
            return np.zeros(self.n_features)

        self.current_day_idx = (self.current_day_idx + 1) % len(self.historical_days)
        day_data = self.historical_days[self.current_day_idx]

        history_data = day_data.get("top10_history")
        self.strategies = get_all_strategies_in_history(history_data)
        self.current_strategy_idx = 0
        self.selected = []
        self.top20_set = get_current_top20(day_data.get("top20"))

        return self._get_observation(day_data)

    def _get_observation(self, day_data: Dict) -> np.ndarray:
        """Get feature vector for current strategy."""
        if self.current_strategy_idx >= len(self.strategies):
            return np.zeros(self.n_features)

        strategy, product = self.strategies[self.current_strategy_idx]
        features = extract_all_features(day_data, strategy, product)
        return features_to_vector(features)

    def step(self, action: int) -> Tuple[np.ndarray, float, bool, Dict]:
        """
        Take action (select or skip strategy).

        Returns: (observation, reward, done, info)
        """
        if not self.historical_days:
            return np.zeros(self.n_features), 0, True, {}

        day_data = self.historical_days[self.current_day_idx]
        strategy, product = self.strategies[self.current_strategy_idx]
        key = f"{strategy}|{product}"

        reward = 0
        if action == 1:  # Select
            self.selected.append(key)
            # Immediate reward: small penalty for selection (encourages selectivity)
            reward = -0.1

        self.current_strategy_idx += 1
        done = self.current_strategy_idx >= len(self.strategies)

        # End of episode reward
        if done:
            correct = sum(1 for k in self.selected if k in self.top20_set)
            wrong = len(self.selected) - correct
            reward += correct * 1.0 - wrong * 1.0

        obs = self._get_observation(day_data) if not done else np.zeros(self.n_features)

        return obs, reward, done, {"selected": self.selected}


class RLAgent:
    """Simple Q-learning agent for strategy selection."""

    def __init__(self, n_features: int, learning_rate: float = 0.1, gamma: float = 0.95):
        self.n_features = n_features
        self.lr = learning_rate
        self.gamma = gamma
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

        # Simple linear Q-function approximation
        self.weights = np.zeros((2, n_features))  # 2 actions x n_features

    def get_q_values(self, state: np.ndarray) -> np.ndarray:
        """Get Q-values for both actions."""
        return self.weights @ state

    def select_action(self, state: np.ndarray, training: bool = True) -> int:
        """Select action using epsilon-greedy policy."""
        if training and np.random.random() < self.epsilon:
            return np.random.randint(2)
        q_values = self.get_q_values(state)
        return int(np.argmax(q_values))

    def update(self, state: np.ndarray, action: int, reward: float,
               next_state: np.ndarray, done: bool):
        """Update Q-function using TD learning."""
        q_values = self.get_q_values(state)
        next_q_values = self.get_q_values(next_state)

        target = reward
        if not done:
            target += self.gamma * np.max(next_q_values)

        # Update weights for the selected action
        error = target - q_values[action]
        self.weights[action] += self.lr * error * state

        # Decay exploration
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def save(self, path: Path):
        """Save agent to disk."""
        with open(path, "wb") as f:
            pickle.dump({"weights": self.weights, "epsilon": self.epsilon}, f)

    def load(self, path: Path) -> bool:
        """Load agent from disk."""
        if not path.exists():
            return False
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
            self.weights = data["weights"]
            self.epsilon = data.get("epsilon", 0.01)
            return True
        except Exception:
            return False


class StrategyPredictor:
    """ML-based strategy persistence predictor."""

    def __init__(self):
        self.model = None
        self.trained = False

    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model using Gradient Boosting."""
        try:
            from sklearn.ensemble import GradientBoostingClassifier
            from sklearn.preprocessing import StandardScaler

            self.scaler = StandardScaler()
            X_scaled = self.scaler.fit_transform(X)

            self.model = GradientBoostingClassifier(
                n_estimators=100,
                max_depth=4,
                learning_rate=0.1,
                random_state=42
            )
            self.model.fit(X_scaled, y)
            self.trained = True

            return True
        except ImportError:
            print("[WARN] scikit-learn not installed. Using rule-based predictions.")
            return False

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        """Predict probability of persistence."""
        if not self.trained or self.model is None:
            return None

        X_scaled = self.scaler.transform(X)
        return self.model.predict_proba(X_scaled)[:, 1]

    def save(self, path: Path):
        """Save model to disk."""
        with open(path, "wb") as f:
            pickle.dump({"model": self.model, "scaler": self.scaler, "trained": self.trained}, f)

    def load(self, path: Path) -> bool:
        """Load model from disk."""
        if not path.exists():
            return False
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
            self.model = data["model"]
            self.scaler = data["scaler"]
            self.trained = data["trained"]
            return True
        except Exception:
            return False


# =============================================================================
# Main Functions
# =============================================================================

def analyze_features(data: Dict):
    """Analyze and display feature statistics."""
    history_data = data.get("top10_history")
    top20_set = get_current_top20(data.get("top20"))

    strategies = get_all_strategies_in_history(history_data)

    winners = []
    losers = []

    for strategy, product in strategies:
        features = extract_all_features(data, strategy, product)
        if not features:
            continue

        key = f"{strategy}|{product}"
        if key in top20_set:
            winners.append(features)
        else:
            losers.append(features)

    def avg(lst, field):
        vals = [x.get(field, 0) for x in lst]
        return statistics.mean(vals) if vals else 0

    print("\n" + "=" * 70)
    print("FEATURE ANALYSIS: Winners vs Losers")
    print("=" * 70)
    print(f"\nWinners (ended in top20): {len(winners)}")
    print(f"Losers (dropped out): {len(losers)}")
    print(f"\n{'Feature':<25} {'Winners':>12} {'Losers':>12} {'Delta':>12}")
    print("-" * 70)

    for feature in ["appearances", "net", "net_trend", "net_volatility",
                    "buy_win_pct", "sell_win_pct", "consistency_score"]:
        w = avg(winners, feature)
        l = avg(losers, feature)
        d = w - l
        print(f"{feature:<25} {w:>12.1f} {l:>12.1f} {d:>+12.1f}")


def evaluate_pick_now_logic(
    features: Dict[str, float],
    total_snapshots: int,
    config: Optional[Dict[str, Any]] = None,
    strategy_name: str = ""
) -> bool:
    """
    Core logic to determine if a strategy is a 'pick now'.

    Configurable thresholds:
    - min_appearances: Minimum times in top10 (default: 20)
    - min_net_trend: Minimum net trend (default: 100)
    - min_snapshots: Minimum total snapshots (default: 60)
    - Golden Filters (net bounds, trade counts, string exclusions, snapshot limits)
    """
    if config is None:
        config = load_pick_now_config()

    min_appearances = config.get("min_appearances", 20)
    min_net_trend = config.get("min_net_trend", 100)
    min_snapshots = config.get("min_snapshots", 60)
    
    # Golden Filters
    min_net_at_pick = config.get("min_net_at_pick", 600)
    max_net_at_pick = config.get("max_net_at_pick", 799)
    max_trade_count = config.get("max_trade_count", 19)
    exclude_string = config.get("exclude_strategy_string", "breakout_Rev_")
    dead_zone_start = config.get("dead_zone_start_snapshot", 85)
    dead_zone_end = config.get("dead_zone_end_snapshot", 99)

    current_net = features.get("net", 0)
    trade_count = features.get("total_trades", 0)

    # 1. Net is in the sweet spot
    is_good_net = min_net_at_pick <= current_net <= max_net_at_pick
    
    # 2. Strategy is fresh, edge hasn't been exhausted
    is_fresh = trade_count <= max_trade_count
    
    # 3. Exclude the toxic variant
    is_not_toxic = exclude_string not in strategy_name if strategy_name else True
    
    # 4. Take a break ONLY during the dead zone
    is_not_dead_zone = not (dead_zone_start <= total_snapshots <= dead_zone_end)

    return (
        features.get("appearances", 0) >= min_appearances and
        features.get("net_trend", 0) > min_net_trend and
        total_snapshots >= min_snapshots and
        is_good_net and
        is_fresh and
        is_not_toxic and
        is_not_dead_zone
    )


def evaluate_pick_now(data: Dict, strategy: str, product: str) -> bool:
    """Evaluate if a strategy should be picked based on current data."""
    features = extract_all_features(data, strategy, product)
    if not features:
        return False
        
    history_data = data.get("top10_history")
    total_snapshots = len(history_data.get("history", [])) if history_data else 0
    
    return evaluate_pick_now_logic(features, total_snapshots, strategy_name=strategy)


def predict_persistence(
    data: Dict,
    model: Optional[StrategyPredictor] = None,
    pick_config: Optional[Dict[str, Any]] = None
):
    """Predict which strategies will persist in top20."""
    history_data = data.get("top10_history")
    top20_set = get_current_top20(data.get("top20"))

    if pick_config is None:
        pick_config = load_pick_now_config()

    strategies = get_all_strategies_in_history(history_data)

    predictions = []

    for strategy, product in strategies:
        features = extract_all_features(data, strategy, product)
        if not features:
            continue

        key = f"{strategy}|{product}"

        # Rule-based prediction
        prob, reason = rule_based_predict(features)

        # ML prediction if available
        if model and model.trained:
            X = features_to_vector(features).reshape(1, -1)
            ml_prob = model.predict_proba(X)[0]
            # Blend rule-based and ML
            prob = 0.3 * prob + 0.7 * ml_prob

        total_snapshots = len(history_data.get("history", [])) if history_data else 0
        pick_now = evaluate_pick_now_logic(features, total_snapshots, pick_config, strategy_name=strategy)

        predictions.append({
            "strategy": strategy,
            "product": product,
            "key": key,
            "probability": float(prob),
            "reason": reason,
            "appearances": features.get("appearances", 0),
            "net": features.get("net", 0),
            "net_trend": features.get("net_trend", 0),
            "currently_in_top20": key in top20_set,
            "pick_now": pick_now,
        })

    # Sort by probability
    predictions.sort(key=lambda x: x["probability"], reverse=True)

    return predictions


def display_predictions(predictions: List[Dict], top_n: int = 20):
    """Display predictions in a formatted table."""
    print("\n" + "=" * 90)
    print("STRATEGY PERSISTENCE PREDICTIONS")
    print("=" * 90)
    print(f"\n{'Rank':<5} {'Strategy':<35} {'Product':<12} {'Prob':>6} {'Apps':>5} {'Net':>8} {'Trend':>8} {'In T20':>7}")
    print("-" * 90)

    for i, pred in enumerate(predictions[:top_n], 1):
        strategy_short = pred["strategy"][:33] + ".." if len(pred["strategy"]) > 35 else pred["strategy"]
        product_short = pred["product"].replace("_C", "")
        in_top20 = "YES" if pred["currently_in_top20"] else "no"
        pick_flag = " [PICK NOW]" if pred.get("pick_now") else ""

        print(f"{i:<5} {strategy_short:<35} {product_short:<12} {pred['probability']:>5.0%} "
              f"{pred['appearances']:>5} {pred['net']:>+8.0f} {pred['net_trend']:>+8.0f} {in_top20:>7}{pick_flag}")

    print("\n" + "-" * 90)
    print("High probability (>70%): Likely to persist in top20")
    print("Medium probability (40-70%): Uncertain, monitor closely")
    print("Low probability (<40%): Likely to drop out")


def get_top_picks(predictions: List[Dict], min_prob: float = 0.7) -> List[Dict]:
    """Get high-confidence picks for social content."""
    return [p for p in predictions if p["probability"] >= min_prob]


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Predict strategy persistence in top20"
    )
    parser.add_argument("--predict", action="store_true", help="Show predictions for current data")
    parser.add_argument("--analyze", action="store_true", help="Analyze feature statistics")
    parser.add_argument("--top", type=int, default=20, help="Number of predictions to show")
    parser.add_argument("--product-type", "-p", type=str, default="forex", help="Product type")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    # Pick Now threshold configuration
    parser.add_argument("--min-appearances", type=int, default=None,
                        help="Minimum appearances in top10 for pick_now (default: 20)")
    parser.add_argument("--min-net-trend", type=float, default=None,
                        help="Minimum net trend for pick_now (default: 100)")
    parser.add_argument("--min-snapshots", type=int, default=None,
                        help="Minimum total snapshots for pick_now (default: 60)")
    parser.add_argument("--show-config", action="store_true",
                        help="Show current pick_now configuration")

    args = parser.parse_args()

    # Build pick_now config from args
    pick_config = load_pick_now_config()
    if args.min_appearances is not None:
        pick_config["min_appearances"] = args.min_appearances
    if args.min_net_trend is not None:
        pick_config["min_net_trend"] = args.min_net_trend
    if args.min_snapshots is not None:
        pick_config["min_snapshots"] = args.min_snapshots

    if args.show_config:
        print("Pick Now Configuration:")
        print(f"  min_appearances: {pick_config['min_appearances']}")
        print(f"  min_net_trend: {pick_config['min_net_trend']}")
        print(f"  min_snapshots: {pick_config['min_snapshots']}")
        return 0

    # Default to predict if no action specified
    if not args.predict and not args.analyze:
        args.predict = True

    # Load data
    date_dir = get_latest_date_dir(args.product_type)
    if not date_dir:
        print(f"[ERROR] No data directory found for {args.product_type}")
        return 1

    print(f"[INFO] Loading data from {date_dir}", file=__import__('sys').stderr)
    data = load_day_data(date_dir)

    # Load model if exists
    model = StrategyPredictor()
    if MODEL_PATH.exists():
        model.load(MODEL_PATH)
        print("[INFO] Loaded trained model", file=__import__('sys').stderr)

    if args.analyze:
        analyze_features(data)

    if args.predict:
        predictions = predict_persistence(data, model, pick_config)

        if args.json:
            import json as json_module
            print(json_module.dumps(predictions[:args.top], indent=2))
        else:
            display_predictions(predictions, args.top)

            # Summary
            high_conf = len([p for p in predictions if p["probability"] >= 0.7])
            med_conf = len([p for p in predictions if 0.4 <= p["probability"] < 0.7])
            low_conf = len([p for p in predictions if p["probability"] < 0.4])
            pick_now_count = len([p for p in predictions if p.get("pick_now")])

            print(f"\nSummary: {high_conf} high confidence, {med_conf} medium, {low_conf} low")
            print(f"Pick Now: {pick_now_count} strategies meet threshold")
            print(f"Config: appearances>={pick_config['min_appearances']}, "
                  f"net_trend>{pick_config['min_net_trend']}, "
                  f"snapshots>={pick_config['min_snapshots']}")

    return 0


if __name__ == "__main__":
    exit(main())
