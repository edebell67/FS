"""
PipHunter Narrative Generator
Generates engaging market battle narratives from live trading data.

Uses skills templates:
- strategy-boxing-battle
- strategy-boxing-battle-pulse
- strategy-battle-punchy-updates
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

# Base path
BASE_DIR = Path(__file__).parent


class NarrativeGenerator:
    """Generates battle-style market narratives from trading data."""

    def __init__(self, data_source: str = "file"):
        """
        Initialize the narrative generator.

        Args:
            data_source: "file" to read from JSON files, "api" to fetch from API
        """
        self.data_source = data_source
        self.api_base = "http://localhost:5000"

    def load_data(self) -> Dict:
        """Load current market data from source."""
        if self.data_source == "file":
            return self._load_from_files()
        else:
            return self._load_from_api()

    def _load_from_files(self) -> Dict:
        """Load data from local JSON files."""
        data = {
            "grid_live": {},
            "bias_history": {},
            "top20": [],
            "timestamp": datetime.now().isoformat()
        }

        # Load grid_live.json
        grid_live_path = BASE_DIR / "grid_live.json"
        if grid_live_path.exists():
            try:
                with open(grid_live_path, 'r') as f:
                    data["grid_live"] = json.load(f)
            except Exception as e:
                print(f"Error loading grid_live.json: {e}")

        # Load bias_history.json
        bias_path = BASE_DIR / "bias_history.json"
        if bias_path.exists():
            try:
                with open(bias_path, 'r') as f:
                    data["bias_history"] = json.load(f)
            except Exception as e:
                print(f"Error loading bias_history.json: {e}")

        return data

    def _load_from_api(self) -> Dict:
        """Load data from API endpoints."""
        import requests

        data = {
            "grid_live": {},
            "bias_history": {},
            "top20": [],
            "timestamp": datetime.now().isoformat()
        }

        try:
            # Fetch grid_live
            resp = requests.get(f"{self.api_base}/api/grid_live", timeout=5)
            if resp.ok:
                data["grid_live"] = resp.json()
        except Exception as e:
            print(f"Error fetching grid_live: {e}")

        try:
            # Fetch bias_history
            resp = requests.get(f"{self.api_base}/api/bias_history", timeout=5)
            if resp.ok:
                data["bias_history"] = resp.json()
        except Exception as e:
            print(f"Error fetching bias_history: {e}")

        try:
            # Fetch top20
            resp = requests.get(f"{self.api_base}/api/top20", timeout=5)
            if resp.ok:
                data["top20"] = resp.json()
        except Exception as e:
            print(f"Error fetching top20: {e}")

        return data

    def extract_metrics(self, data: Dict) -> Dict:
        """Extract key metrics from raw data."""
        metrics = {
            "timestamp": datetime.now(),
            "buy_net": 0.0,
            "sell_net": 0.0,
            "imbalance": 0.0,
            "bias": "NEUTRAL",
            "confidence": "LOW",
            "open_trades": 0,
            "buy_exposure": 0,
            "sell_exposure": 0,
            "top_strategy": None,
            "top_strategy_net": 0.0,
            "top_product": None,
            "weak_product": None,
            "last_30m_buy": 0.0,
            "last_30m_sell": 0.0,
        }

        # Extract from bias_history
        bias_data = data.get("bias_history", {})
        if isinstance(bias_data, dict):
            # Handle array format with history entries
            history = bias_data.get("history", [])
            if isinstance(history, list) and len(history) > 0:
                latest = history[0]  # Most recent entry
                metrics["buy_net"] = float(latest.get("recent_buy_pnl", 0) or 0)
                metrics["sell_net"] = float(latest.get("recent_sell_pnl", 0) or 0)
                metrics["bias"] = latest.get("bias", "BUY" if metrics["buy_net"] > metrics["sell_net"] else "SELL")
            else:
                # Fallback for flat format
                metrics["buy_net"] = float(bias_data.get("buy_net", bias_data.get("recent_buy_pnl", 0)) or 0)
                metrics["sell_net"] = float(bias_data.get("sell_net", bias_data.get("recent_sell_pnl", 0)) or 0)
                metrics["bias"] = bias_data.get("current_bias", bias_data.get("bias", "BUY" if metrics["buy_net"] > metrics["sell_net"] else "SELL"))

        # Calculate imbalance
        metrics["imbalance"] = abs(metrics["buy_net"] - metrics["sell_net"])

        # Determine confidence based on imbalance
        if metrics["imbalance"] > 200:
            metrics["confidence"] = "HIGH"
        elif metrics["imbalance"] > 100:
            metrics["confidence"] = "MEDIUM"
        else:
            metrics["confidence"] = "LOW"

        # Extract from grid_live
        grid_data = data.get("grid_live", {})
        trades = grid_data.get("trades", [])
        if isinstance(trades, list):
            metrics["open_trades"] = len(trades)
            for trade in trades:
                direction = trade.get("direction", "BUY")
                if direction == "BUY":
                    metrics["buy_exposure"] += 1
                else:
                    metrics["sell_exposure"] += 1

        # Extract top strategy from top20
        top20 = data.get("top20", [])
        if isinstance(top20, list) and len(top20) > 0:
            top = top20[0]
            metrics["top_strategy"] = top.get("strategy_name", top.get("name", "Unknown"))
            metrics["top_strategy_net"] = float(top.get("net_return", top.get("pnl", 0)) or 0)

        return metrics

    def generate_social(self, metrics: Dict) -> str:
        """
        Generate ultra-compact narrative for social media (280 chars).

        Format: Battle status + key metric + winner call
        """
        bias = metrics["bias"]
        buy_net = metrics["buy_net"]
        sell_net = metrics["sell_net"]
        imbalance = metrics["imbalance"]
        confidence = metrics["confidence"]

        winner = "BUY" if buy_net > sell_net else "SELL"
        winner_emoji = "🟢" if winner == "BUY" else "🔴"

        # Format values with sign
        buy_str = f"+{buy_net:.0f}" if buy_net >= 0 else f"{buy_net:.0f}"
        sell_str = f"+{sell_net:.0f}" if sell_net >= 0 else f"{sell_net:.0f}"

        # Build compact message
        lines = []
        lines.append(f"{winner_emoji} LIVE BATTLE")
        lines.append(f"BUY {buy_str} vs SELL {sell_str}")
        lines.append(f"Winner: {winner} ({confidence})")

        if metrics["top_strategy"]:
            lines.append(f"Leader: {metrics['top_strategy'][:20]}")

        lines.append("🎯 piphunter.io")

        return " | ".join(lines)[:280]

    def generate_pulse(self, metrics: Dict) -> str:
        """
        Generate compact pulse narrative for app notifications.

        Format: Headline + 5-8 battle beats + winner call
        """
        timestamp = metrics["timestamp"].strftime("%H:%M:%S")
        bias = metrics["bias"]
        buy_net = metrics["buy_net"]
        sell_net = metrics["sell_net"]
        imbalance = metrics["imbalance"]
        confidence = metrics["confidence"]
        winner = "BUY" if buy_net > sell_net else "SELL"

        lines = []

        # Headline
        lines.append(f"**LIVE Battle Pulse | Bias {bias} | {timestamp}**")
        lines.append("")

        # Battle Beats
        # Format values with sign
        buy_str = f"+{buy_net:.1f}" if buy_net >= 0 else f"{buy_net:.1f}"
        sell_str = f"+{sell_net:.1f}" if sell_net >= 0 else f"{sell_net:.1f}"

        lines.append("**Battle Beats**")
        lines.append(f"1. Bell: BUY {buy_str} vs SELL {sell_str}.")

        if winner == "BUY":
            lines.append(f"2. BUY presses. Imbalance {imbalance:.1f}.")
        else:
            lines.append(f"2. SELL surges. Imbalance {imbalance:.1f}.")

        if metrics["top_strategy"]:
            lines.append(f"3. Leader: {metrics['top_strategy']} (+{metrics['top_strategy_net']:.1f})")

        lines.append(f"4. Open pressure: {metrics['open_trades']} trades.")
        lines.append(f"5. Exposure: BUY {metrics['buy_exposure']} | SELL {metrics['sell_exposure']}")
        lines.append(f"6. Likely winner: {winner} ({confidence}).")

        lines.append("")
        lines.append("**Winner Call**")
        lines.append(f"- {winner} favored into next round.")

        return "\n".join(lines)

    def generate_full(self, metrics: Dict) -> str:
        """
        Generate full narrative for website display.

        Format: Fight card + round commentary + scoreboard
        """
        timestamp = metrics["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        bias = metrics["bias"]
        buy_net = metrics["buy_net"]
        sell_net = metrics["sell_net"]
        imbalance = metrics["imbalance"]
        confidence = metrics["confidence"]
        winner = "BUY" if buy_net > sell_net else "SELL"
        loser = "SELL" if winner == "BUY" else "BUY"

        # Action verbs based on imbalance
        if imbalance > 150:
            winner_verb = "dominates"
            loser_verb = "crumbles"
        elif imbalance > 75:
            winner_verb = "presses"
            loser_verb = "stumbles"
        else:
            winner_verb = "holds"
            loser_verb = "contests"

        # Format values with sign
        buy_str = f"+{buy_net:.1f}" if buy_net >= 0 else f"{buy_net:.1f}"
        sell_str = f"+{sell_net:.1f}" if sell_net >= 0 else f"{sell_net:.1f}"
        buy_str2 = f"+{buy_net:.2f}" if buy_net >= 0 else f"{buy_net:.2f}"
        sell_str2 = f"+{sell_net:.2f}" if sell_net >= 0 else f"{sell_net:.2f}"

        lines = []

        # Fight Card
        lines.append("## Fight Card")
        lines.append(f"- **Arena**: Live Market Battle")
        lines.append(f"- **Factions**: BUY vs SELL")
        lines.append(f"- **Current Leader**: {winner}")
        lines.append(f"- **Timestamp**: {timestamp}")
        lines.append("")

        # Round Commentary
        lines.append("## Round Commentary")
        lines.append(f"1. The bell rings. BUY opens at {buy_str}, SELL at {sell_str}.")
        lines.append(f"2. {winner} {winner_verb}. {loser} {loser_verb}.")
        lines.append(f"3. Imbalance widens to {imbalance:.1f}.")

        if metrics["top_strategy"]:
            top_str = f"+{metrics['top_strategy_net']:.1f}" if metrics['top_strategy_net'] >= 0 else f"{metrics['top_strategy_net']:.1f}"
            lines.append(f"4. {metrics['top_strategy']} leads the charge with {top_str}.")

        lines.append(f"5. Open trades: {metrics['open_trades']} positions in play.")
        lines.append(f"6. Exposure split: BUY {metrics['buy_exposure']} | SELL {metrics['sell_exposure']}.")
        lines.append("")

        # Scoreboard
        lines.append("## Scoreboard")
        lines.append(f"- **BUY Net**: {buy_str2}")
        lines.append(f"- **SELL Net**: {sell_str2}")
        lines.append(f"- **Imbalance**: {imbalance:.2f}")
        lines.append(f"- **Likely Winner**: {winner} ({confidence} confidence)")
        lines.append("")

        # Winner Call
        lines.append("## Winner Call")
        if confidence == "HIGH":
            lines.append(f"**{winner} controls the ring.** Strong conviction for continued dominance.")
        elif confidence == "MEDIUM":
            lines.append(f"**{winner} has the edge.** Momentum building but watch for reversals.")
        else:
            lines.append(f"**{winner} leads narrowly.** Battle remains contested. Stay alert.")

        return "\n".join(lines)

    def generate_html_snippet(self, metrics: Dict) -> str:
        """Generate HTML snippet for direct website injection."""
        bias = metrics["bias"]
        buy_net = metrics["buy_net"]
        sell_net = metrics["sell_net"]
        imbalance = metrics["imbalance"]
        confidence = metrics["confidence"]
        winner = "BUY" if buy_net > sell_net else "SELL"

        # Format values with sign
        buy_str = f"+{buy_net:.1f}" if buy_net >= 0 else f"{buy_net:.1f}"
        sell_str = f"+{sell_net:.1f}" if sell_net >= 0 else f"{sell_net:.1f}"

        return f'''<span class="highlight">Battle intensifies.</span> BUY faction holds with
<span class="buy-highlight">{buy_str}</span> net vs SELL's
<span class="sell-highlight">{sell_str}</span>.
Imbalance: {imbalance:.1f}.
Likely winner next round: <span class="highlight">{winner} ({confidence} confidence)</span>.'''

    def generate_all(self) -> Dict:
        """Generate all narrative formats."""
        data = self.load_data()
        metrics = self.extract_metrics(data)

        return {
            "timestamp": metrics["timestamp"].isoformat(),
            "metrics": {
                "buy_net": metrics["buy_net"],
                "sell_net": metrics["sell_net"],
                "imbalance": metrics["imbalance"],
                "bias": metrics["bias"],
                "confidence": metrics["confidence"],
                "open_trades": metrics["open_trades"],
                "top_strategy": metrics["top_strategy"],
            },
            "narratives": {
                "social": self.generate_social(metrics),
                "pulse": self.generate_pulse(metrics),
                "full": self.generate_full(metrics),
                "html": self.generate_html_snippet(metrics),
            }
        }

    def save_narratives(self, output_path: Optional[str] = None) -> str:
        """Generate and save narratives to JSON file."""
        result = self.generate_all()

        if output_path is None:
            output_path = BASE_DIR / "narratives.json"

        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)

        return str(output_path)


# Flask endpoint integration
def add_narrative_routes(app):
    """Add narrative API routes to existing Flask app."""

    generator = NarrativeGenerator(data_source="file")

    @app.route('/api/narratives', methods=['GET'])
    def get_narratives():
        """Get all narrative formats."""
        try:
            result = generator.generate_all()
            return result
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/api/narratives/social', methods=['GET'])
    def get_social_narrative():
        """Get social media narrative only."""
        try:
            data = generator.load_data()
            metrics = generator.extract_metrics(data)
            return {"narrative": generator.generate_social(metrics)}
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/api/narratives/pulse', methods=['GET'])
    def get_pulse_narrative():
        """Get pulse narrative only."""
        try:
            data = generator.load_data()
            metrics = generator.extract_metrics(data)
            return {"narrative": generator.generate_pulse(metrics)}
        except Exception as e:
            return {"error": str(e)}, 500

    @app.route('/api/narratives/html', methods=['GET'])
    def get_html_narrative():
        """Get HTML snippet for website."""
        try:
            data = generator.load_data()
            metrics = generator.extract_metrics(data)
            return {
                "html": generator.generate_html_snippet(metrics),
                "bias": metrics["bias"],
                "timestamp": metrics["timestamp"].isoformat()
            }
        except Exception as e:
            return {"error": str(e)}, 500


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate market battle narratives")
    parser.add_argument("--source", choices=["file", "api"], default="file",
                       help="Data source: file or api")
    parser.add_argument("--format", choices=["all", "social", "pulse", "full", "html"],
                       default="all", help="Output format")
    parser.add_argument("--output", help="Output file path (for 'all' format)")

    args = parser.parse_args()

    generator = NarrativeGenerator(data_source=args.source)

    if args.format == "all":
        result = generator.generate_all()
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"Saved to {args.output}")
        else:
            print(json.dumps(result, indent=2, default=str))
    else:
        data = generator.load_data()
        metrics = generator.extract_metrics(data)

        if args.format == "social":
            print(generator.generate_social(metrics))
        elif args.format == "pulse":
            print(generator.generate_pulse(metrics))
        elif args.format == "full":
            print(generator.generate_full(metrics))
        elif args.format == "html":
            print(generator.generate_html_snippet(metrics))
