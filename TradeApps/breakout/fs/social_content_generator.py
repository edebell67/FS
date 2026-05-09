#!/usr/bin/env python3
"""
social_content_generator.py - Generate Twitter and TikTok content from Strategy Warehouse data

Reads live trading data from the warehouse JSON files and generates:
- Twitter posts (signal alerts, performance recaps, leaderboard updates)
- TikTok scripts (spoken text with visual cues for animated character)

Usage:
    python social_content_generator.py --twitter          # Twitter content only
    python social_content_generator.py --tiktok           # TikTok scripts only
    python social_content_generator.py --all              # Both platforms
    python social_content_generator.py --all --output out.json  # Save to file

[2026-03-23] MVP carve-out from Strategy Warehouse Autonomous Marketing Engine
"""

import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# [2026-03-23 13:20] V20260323_1320 - Added browser-based Twitter posting support
# Part of task: breakout_social_content_browser_twitter_posting
try:
    from twitter_browser import TwitterBrowser
except ModuleNotFoundError:
    TwitterBrowser = None


# Configuration
SCRIPT_DIR = Path(__file__).resolve().parent
JSON_ROOT = SCRIPT_DIR / "json"
CONFIG_PATH = SCRIPT_DIR / "config.json"

# Default hashtags
DEFAULT_HASHTAGS = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading"]


def load_config() -> Dict[str, Any]:
    """Load config.json for product type settings."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def get_latest_date_dir(product_type: str = "forex", run_mode: str = "live") -> Optional[Path]:
    """Find the latest date directory for a product type."""
    base_path = JSON_ROOT / run_mode / product_type
    if not base_path.exists():
        # Try legacy path without product_type
        base_path = JSON_ROOT / run_mode
        if not base_path.exists():
            return None

    date_dirs = []
    for item in base_path.iterdir():
        if item.is_dir() and re.match(r"^\d{4}-\d{2}-\d{2}$", item.name):
            date_dirs.append(item)

    if not date_dirs:
        return None

    return sorted(date_dirs, key=lambda x: x.name, reverse=True)[0]


def load_json_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file safely."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Failed to load {filepath}: {e}")
        return None


def load_warehouse_data(product_type: str = "forex") -> Dict[str, Any]:
    """Load all warehouse data files from the latest date directory."""
    date_dir = get_latest_date_dir(product_type)
    if not date_dir:
        return {"error": f"No data directory found for {product_type}"}

    stats_dir = JSON_ROOT / "live" / product_type / "stats"

    data = {
        "date_dir": str(date_dir),
        "date": date_dir.name,
        "product_type": product_type,
        "summary_net": load_json_file(date_dir / "_summary_net.json"),
        "frequency": load_json_file(date_dir / "_frequency.json"),
        "dna_frequency": load_json_file(date_dir / "_dna_frequency.json"),
        "weekly_stats": load_json_file(stats_dir / "daily_net_return.json"),
    }
    return data


def is_dna_strategy(name: str) -> bool:
    """Check if a strategy or product name is a DNA strategy."""
    return name.upper().startswith("DNA") or name.upper().startswith("DNA_")


def extract_best_signal(summary_net: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Extract the best performing signal from summary_net data (excludes DNA)."""
    if not summary_net or "strategies" not in summary_net:
        return None

    best = None
    best_net = float("-inf")

    strategies = summary_net.get("strategies", {})
    for strategy_name, products in strategies.items():
        # Skip DNA strategies
        if is_dna_strategy(strategy_name):
            continue
        if not isinstance(products, dict):
            continue
        for product_name, points in products.items():
            # Skip DNA products
            if is_dna_strategy(product_name):
                continue
            if not isinstance(points, list) or not points:
                continue
            # Get latest point
            latest = points[-1] if points else {}
            net = latest.get("net", 0)
            if net > best_net:
                best_net = net
                best = {
                    "strategy": strategy_name,
                    "product": product_name,
                    "net": net,
                    "buy_net": latest.get("buy_net", 0),
                    "sell_net": latest.get("sell_net", 0),
                    "buys_count": latest.get("b_c", 0),
                    "sells_count": latest.get("s_c", 0),
                }

    return best


def extract_leaderboard(frequency_data: Dict[str, Any], top_n: int = 3) -> List[Dict[str, Any]]:
    """Extract top N leaders from frequency data (excludes DNA)."""
    if not frequency_data:
        return []

    snapshots = frequency_data.get("snapshots", [])
    if not snapshots:
        return []

    # Get latest snapshot
    latest = snapshots[-1]
    all_leaders = latest.get("leaders", [])

    # Filter out DNA strategies and take top N
    filtered_leaders = []
    for leader in all_leaders:
        product = leader.get("product", "")
        strategy = leader.get("strategy", "")
        if is_dna_strategy(product) or is_dna_strategy(strategy):
            continue
        filtered_leaders.append(leader)
        if len(filtered_leaders) >= top_n:
            break

    return [
        {
            "rank": i + 1,  # Re-rank after filtering
            "product": leader.get("product", "Unknown"),
            "strategy": leader.get("strategy", "Unknown"),
            "net": leader.get("net", 0),
        }
        for i, leader in enumerate(filtered_leaders)
    ]


def shorten_strategy_name(name: str) -> str:
    """Shorten strategy name for Twitter brevity."""
    # breakout_R_Rev_2_tp10.0_sl20.0 -> brk R Rev 2 tp10 sl20
    shortened = name.replace("breakout", "brk")
    shortened = re.sub(r"\.0+", "", shortened)  # Remove .0
    shortened = shortened.replace("_", " ")
    return shortened[:40]  # Max 40 chars


def clean_product_name(name: str) -> str:
    """Clean product name for display (remove _C/_S suffix)."""
    return re.sub(r"_[CS]$", "", name)


def format_net_points(net: float) -> str:
    """Format net points with sign."""
    if net >= 0:
        return f"+{int(net)}"
    return str(int(net))


def determine_bias(buy_net: float, sell_net: float) -> str:
    """Determine directional bias."""
    if buy_net > sell_net:
        return "buy-led"
    elif sell_net > buy_net:
        return "sell-led"
    return "balanced"


def number_to_spoken(num: float) -> str:
    """Convert number to spoken form for TikTok scripts."""
    num_int = int(abs(num))
    # Convert to spoken digits for large numbers
    if num_int >= 100000:
        spoken = "-".join(list(str(num_int)))
    elif num_int >= 1000:
        # e.g., 1255 -> "twelve fifty-five" or "one-two-five-five"
        spoken = "-".join(list(str(num_int)))
    else:
        spoken = str(num_int)

    if num < 0:
        return f"minus {spoken}"
    return spoken


def product_to_spoken(product: str) -> str:
    """Convert product code to spoken form."""
    # DNA_104008_CHF -> DNA one-oh-four-oh-oh-eight
    if product.startswith("DNA_"):
        parts = product.split("_")
        if len(parts) >= 2:
            num = parts[1]
            spoken_num = "-".join(list(num))
            return f"DNA {spoken_num}"

    # GBPEUR_C -> GBP EUR
    product = product.replace("_C", "").replace("_S", "")
    return " ".join([product[i:i+3] for i in range(0, len(product), 3) if product[i:i+3].isalpha()])


def format_date_range(date_range: List[str]) -> str:
    """Format ISO date range into a short Twitter-friendly label."""
    if not date_range or len(date_range) < 2:
        return "this week"

    try:
        start = datetime.fromisoformat(date_range[0]).strftime("%b %d")
        end = datetime.fromisoformat(date_range[1]).strftime("%b %d")
        return f"{start}-{end}"
    except Exception:
        return "this week"


def extract_weekly_top_strategies(weekly_stats: Dict[str, Any], top_n: int = 5) -> List[Dict[str, Any]]:
    """Extract top N weekly strategies from aggregated performance stats."""
    if not weekly_stats:
        return []

    top_strategies = weekly_stats.get("top_strategies", [])
    results: List[Dict[str, Any]] = []
    rank = 1

    for item in top_strategies:
        strategy_label = item.get("strategy", "")
        if "|" in strategy_label:
            product, strategy_name = [part.strip() for part in strategy_label.split("|", 1)]
        else:
            product, strategy_name = "Unknown", strategy_label.strip()

        if is_dna_strategy(product) or is_dna_strategy(strategy_name):
            continue

        results.append(
            {
                "rank": rank,
                "product": product,
                "strategy": strategy_name,
                "total_net": item.get("total_net", 0),
                "total_trades": item.get("total_trades", 0),
            }
        )
        rank += 1

        if len(results) >= top_n:
            break

    return results


# =============================================================================
# Twitter Content Generation
# =============================================================================

def generate_twitter_signal_alert(signal: Dict[str, Any]) -> Dict[str, Any]:
    """Generate Twitter signal alert post."""
    if not signal:
        return None

    strategy = shorten_strategy_name(signal["strategy"])
    product = clean_product_name(signal["product"])
    net = format_net_points(signal["net"])
    bias = determine_bias(signal["buy_net"], signal["sell_net"])
    buys = signal["buys_count"]
    sells = signal["sells_count"]

    # Build hashtags
    product_tag = f"#{product}"
    hashtags = ["#ForexTrading", "#CryptoTrading", "#SmallAccountChallenge", product_tag]

    text = (
        f"Day 1 of the modest account journey. "
        f"Tracking {strategy} on {product}. "
        f"Net {net} pts, {bias} bias. "
        f"{buys} buys vs {sells} sells. "
        f"Strategy Warehouse coming soon. "
        f"{' '.join(hashtags[:4])}"
    )

    # Trim if over 280
    if len(text) > 280:
        text = text[:277] + "..."

    return {
        "type": "signal_alert",
        "text": text,
        "hashtags": hashtags[:4],
        "char_count": len(text),
    }


def generate_twitter_leaderboard(leaders: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate Twitter leaderboard post."""
    if not leaders:
        return None

    leader_strs = []
    for leader in leaders[:3]:
        name = clean_product_name(leader["product"])
        net = format_net_points(leader["net"])
        leader_strs.append(f"{leader['rank']}. {name} ({net})")

    leaderboard_text = " | ".join(leader_strs)
    hashtags = ["#ForexTrading", "#CryptoTrading", "#SmallAccountChallenge", "#Leaderboard"]

    text = (
        f"Modest account leaderboard: {leaderboard_text}. "
        f"Forex and crypto signals I'm tracking. Strategy Warehouse coming soon. "
        f"{' '.join(hashtags)}"
    )

    if len(text) > 280:
        text = text[:277] + "..."

    return {
        "type": "leaderboard_watch",
        "text": text,
        "hashtags": hashtags,
        "char_count": len(text),
    }


def generate_twitter_weekly_top5(leaders: List[Dict[str, Any]], weekly_stats: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Generate a weekly forex top 5 strategy results post."""
    if not leaders:
        return None

    date_label = format_date_range(weekly_stats.get("date_range", []))
    line_items = []

    for leader in leaders[:5]:
        strategy = shorten_strategy_name(leader["strategy"])
        product = clean_product_name(leader["product"])
        net = format_net_points(leader["total_net"])
        line_items.append(f"{leader['rank']}. {product} {strategy} {net}")

    text = (
        f"Forex top 5 strategies for {date_label}:\n"
        f"{chr(10).join(line_items)}\n"
        f"#ForexTrading #AlgoTrading #StrategyWarehouse"
    )

    if len(text) > 280:
        text = (
            f"Forex top 5 strategies for {date_label}: "
            f"{' | '.join(line_items)} "
            f"#ForexTrading #AlgoTrading"
        )

    if len(text) > 280:
        compact_items = []
        for leader in leaders[:5]:
            compact_items.append(
                f"{leader['rank']}.{clean_product_name(leader['product'])} {format_net_points(leader['total_net'])}"
            )
        text = (
            f"Forex top 5 for {date_label}: "
            f"{' | '.join(compact_items)} "
            f"#ForexTrading #AlgoTrading"
        )

    if len(text) > 280:
        text = text[:277] + "..."

    return {
        "type": "weekly_top5_forex",
        "text": text,
        "hashtags": ["#ForexTrading", "#AlgoTrading", "#StrategyWarehouse"],
        "char_count": len(text),
    }


def generate_twitter_performance_recap(
    leaders: List[Dict[str, Any]],
    snapshot_count: int
) -> Dict[str, Any]:
    """Generate Twitter performance recap post."""
    if not leaders:
        return None

    top = leaders[0]
    product = clean_product_name(top["product"])
    net = format_net_points(top["net"])

    hashtags = ["#ForexTrading", "#CryptoTrading", "#SmallAccountChallenge", "#TradingJourney"]

    text = (
        f"Modest account update: {product} leading at {net} pts. "
        f"Verified across {snapshot_count} snapshots. "
        f"Slow and steady. Strategy Warehouse coming soon. "
        f"{' '.join(hashtags)}"
    )

    if len(text) > 280:
        text = text[:277] + "..."

    return {
        "type": "performance_recap",
        "text": text,
        "hashtags": hashtags,
        "char_count": len(text),
    }


def generate_twitter_content(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate all Twitter content from warehouse data."""
    posts = []
    weekly_stats = data.get("weekly_stats")
    product_type = data.get("product_type", "unknown")

    if product_type == "forex" and weekly_stats:
        weekly_leaders = extract_weekly_top_strategies(weekly_stats, top_n=5)
        weekly_post = generate_twitter_weekly_top5(weekly_leaders, weekly_stats)
        if weekly_post:
            posts.append(weekly_post)

    # Signal Alert
    if not posts and data.get("summary_net"):
        signal = extract_best_signal(data["summary_net"])
        if signal:
            post = generate_twitter_signal_alert(signal)
            if post:
                posts.append(post)

    # Leaderboard & Performance Recap (use frequency only, not dna_frequency)
    freq_data = data.get("frequency")
    if not posts and freq_data:
        leaders = extract_leaderboard(freq_data)
        snapshot_count = freq_data.get("snapshot_count", 0)

        if leaders:
            leaderboard = generate_twitter_leaderboard(leaders)
            if leaderboard:
                posts.append(leaderboard)

            recap = generate_twitter_performance_recap(leaders, snapshot_count)
            if recap:
                posts.append(recap)

    return {
        "platform": "twitter",
        "generated_at": datetime.now().isoformat(),
        "data_date": data.get("date", "unknown"),
        "product_type": data.get("product_type", "unknown"),
        "posts": posts,
    }


# =============================================================================
# TikTok Script Generation
# =============================================================================

def generate_tiktok_signal_script(signal: Dict[str, Any]) -> Dict[str, Any]:
    """Generate TikTok script for signal alert."""
    if not signal:
        return None

    strategy = shorten_strategy_name(signal["strategy"])
    product = product_to_spoken(signal["product"])
    net = number_to_spoken(signal["net"])
    buys = signal["buys_count"]
    sells = signal["sells_count"]
    bias = "buy side" if signal["buy_net"] > signal["sell_net"] else "sell side"

    spoken_text = (
        f"Hey traders! Quick momentum check - "
        f"our {strategy.split()[0]} strategy just hit plus {net} points on {product}! "
        f"That's {buys} buys versus {sells} sells. "
        f"The {bias} is leading this one. "
        f"Link in bio to join the warehouse!"
    )

    product_tag = f"#{signal['product'].replace('_', '')}"
    hashtags = ["#StrategyWarehouse", "#TradingSignals", "#AlgoTrading", "#ForexTrading", "#TradingTips", product_tag]

    return {
        "type": "signal_alert",
        "duration_seconds": 20,
        "spoken_text": spoken_text,
        "visual_cues": [
            {"time": 0, "cue": "wave_greeting"},
            {"time": 3, "cue": "show_chart_graphic"},
            {"time": 8, "cue": "show_buy_sell_count"},
            {"time": 14, "cue": "thumbs_up"},
            {"time": 18, "cue": "point_to_link"},
        ],
        "hashtags": hashtags[:6],
        "caption": f"Momentum alert! {format_net_points(signal['net'])} pts on {signal['product']}. Join the warehouse for more signals!",
    }


def generate_tiktok_leaderboard_script(leaders: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate TikTok script for leaderboard update."""
    if not leaders or len(leaders) < 3:
        return None

    leader1 = leaders[0]
    leader2 = leaders[1]
    leader3 = leaders[2]

    spoken_text = (
        f"Leaderboard update! "
        f"{product_to_spoken(leader1['product'])} is crushing it at plus {number_to_spoken(leader1['net'])} points! "
        f"Second place goes to {product_to_spoken(leader2['product'])} with {number_to_spoken(leader2['net'])}. "
        f"And third is {product_to_spoken(leader3['product'])}. "
        f"These strategies are on fire today! Follow for daily updates!"
    )

    hashtags = ["#StrategyWarehouse", "#Leaderboard", "#AlgoTrading", "#TradingStrategy", "#ForexTrading"]

    return {
        "type": "leaderboard_watch",
        "duration_seconds": 25,
        "spoken_text": spoken_text,
        "visual_cues": [
            {"time": 0, "cue": "excited_intro"},
            {"time": 4, "cue": "show_rank_1_card"},
            {"time": 10, "cue": "show_rank_2_card"},
            {"time": 16, "cue": "show_rank_3_card"},
            {"time": 21, "cue": "celebrate"},
            {"time": 24, "cue": "point_to_follow"},
        ],
        "hashtags": hashtags,
        "caption": f"Who's leading the board? Top 3 strategies revealed! {' '.join(hashtags[:3])}",
    }


def generate_tiktok_performance_script(
    leaders: List[Dict[str, Any]],
    snapshot_count: int
) -> Dict[str, Any]:
    """Generate TikTok script for performance recap."""
    if not leaders:
        return None

    top = leaders[0]

    spoken_text = (
        f"Performance recap time! "
        f"{product_to_spoken(top['product'])} is leading with plus {number_to_spoken(top['net'])} points. "
        f"We've run {snapshot_count} snapshots today to verify consistency. "
        f"Discipline over hype - that's how the warehouse operates. "
        f"Subscribe for the full performance breakdown!"
    )

    hashtags = ["#StrategyWarehouse", "#TradingPerformance", "#AlgoTrading", "#Consistency", "#TradingResults"]

    return {
        "type": "performance_recap",
        "duration_seconds": 22,
        "spoken_text": spoken_text,
        "visual_cues": [
            {"time": 0, "cue": "thinking_pose"},
            {"time": 3, "cue": "show_leader_stats"},
            {"time": 10, "cue": "show_snapshot_count"},
            {"time": 15, "cue": "serious_nod"},
            {"time": 19, "cue": "point_to_subscribe"},
        ],
        "hashtags": hashtags,
        "caption": f"Discipline over hype. {format_net_points(top['net'])} pts verified across {snapshot_count} snapshots.",
    }


def generate_tiktok_content(data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate all TikTok scripts from warehouse data."""
    scripts = []

    # Signal Alert Script
    if data.get("summary_net"):
        signal = extract_best_signal(data["summary_net"])
        if signal and signal["net"] > 0:  # Only positive signals
            script = generate_tiktok_signal_script(signal)
            if script:
                scripts.append(script)

    # Leaderboard & Performance Scripts (use frequency only, not dna_frequency)
    freq_data = data.get("frequency")
    if freq_data:
        leaders = extract_leaderboard(freq_data, top_n=5)
        snapshot_count = freq_data.get("snapshot_count", 0)

        if leaders:
            leaderboard_script = generate_tiktok_leaderboard_script(leaders)
            if leaderboard_script:
                scripts.append(leaderboard_script)

            performance_script = generate_tiktok_performance_script(leaders, snapshot_count)
            if performance_script:
                scripts.append(performance_script)

    return {
        "platform": "tiktok",
        "generated_at": datetime.now().isoformat(),
        "data_date": data.get("date", "unknown"),
        "product_type": data.get("product_type", "unknown"),
        "scripts": scripts,
    }


# =============================================================================
# Main CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate Twitter and TikTok content from Strategy Warehouse data"
    )
    parser.add_argument("--twitter", action="store_true", help="Generate Twitter content")
    parser.add_argument("--tiktok", action="store_true", help="Generate TikTok scripts")
    parser.add_argument("--all", action="store_true", help="Generate content for all platforms")
    parser.add_argument("--output", "-o", type=str, help="Output file path (default: stdout)")
    parser.add_argument("--product-type", "-p", type=str, default="forex",
                        help="Product type to load data from (default: forex)")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")
    
    # Browser Posting Flags
    parser.add_argument("--post", action="store_true", help="Post to Twitter via browser automation")
    parser.add_argument("--post-delay", type=int, default=60, help="Delay in seconds between posts (default: 60)")
    parser.add_argument("--dry-run", action="store_true", help="Dry run: show what would be posted without posting")
    parser.add_argument("--login", action="store_true", help="Open browser for manual Twitter login setup")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompt before posting")
    parser.add_argument("--max-posts", type=int, default=10, help="Maximum number of posts per session (default: 10)")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")

    args = parser.parse_args()

    # Default to --all if no platform specified
    if not args.twitter and not args.tiktok and not args.all:
        args.all = True

    # Load warehouse data
    print(f"[INFO] Loading warehouse data for {args.product_type}...", file=__import__('sys').stderr)
    data = load_warehouse_data(args.product_type)

    if "error" in data:
        print(f"[ERROR] {data['error']}", file=__import__('sys').stderr)
        return 1

    print(f"[INFO] Loaded data from {data['date_dir']}", file=__import__('sys').stderr)

    # Generate content
    output = {
        "generated_at": datetime.now().isoformat(),
        "data_source": data["date_dir"],
        "data_date": data["date"],
        "product_type": args.product_type,
    }

    if args.twitter or args.all:
        output["twitter"] = generate_twitter_content(data)
        print(f"[INFO] Generated {len(output['twitter']['posts'])} Twitter posts", file=__import__('sys').stderr)

    if args.tiktok or args.all:
        output["tiktok"] = generate_tiktok_content(data)
        print(f"[INFO] Generated {len(output['tiktok']['scripts'])} TikTok scripts", file=__import__('sys').stderr)

    # Output
    indent = 2 if args.pretty else None
    json_output = json.dumps(output, indent=indent, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json_output)
        print(f"[INFO] Output written to {args.output}", file=__import__('sys').stderr)
    else:
        print(json_output)

    # --- Browser Posting Logic ---
    if args.login:
        if TwitterBrowser is None:
            print("[ERROR] Twitter browser support requires Playwright to be installed.", file=__import__('sys').stderr)
            return 1
        with TwitterBrowser(headless=False) as tb:
            tb.login()
            if not tb.wait_for_login(timeout_seconds=600):
                print("[ERROR] Twitter login was not detected before timeout.", file=__import__('sys').stderr)
                return 1
            print("[INFO] Twitter login session saved.", file=__import__('sys').stderr)
        return 0

    if args.post:
        if TwitterBrowser is None:
            print("[ERROR] Twitter posting requires Playwright to be installed.", file=__import__('sys').stderr)
            return 1
        twitter_posts = output.get("twitter", {}).get("posts", [])
        if not twitter_posts:
            print("[WARN] No Twitter posts generated to post.", file=__import__('sys').stderr)
            return 0

        print(f"[INFO] Preparing to post {len(twitter_posts)} tweets...", file=__import__('sys').stderr)
        
        # Limit posts
        posts_to_send = twitter_posts[:args.max_posts]
        
        with TwitterBrowser(headless=args.headless) as tb:
            # Check login status
            if not tb.is_logged_in():
                print("[ERROR] Not logged in to Twitter. Run with --login first.", file=__import__('sys').stderr)
                return 1
            
            for i, post in enumerate(posts_to_send):
                text = post["text"]
                print(f"\n[POST {i+1}/{len(posts_to_send)}]")
                print(f"Content: {text}")
                
                if args.dry_run:
                    print("[DRY-RUN] Skipping actual post.")
                    continue
                
                if not args.yes:
                    confirm = input("Confirm post? [y/N]: ")
                    if confirm.lower() != 'y':
                        print("[INFO] Skipped.")
                        continue
                
                success = tb.post_tweet(text)
                if success:
                    # Log success with timestamp
                    with open("posted_tweets.log", "a", encoding="utf-8") as log:
                        log.write(f"{datetime.now().isoformat()} | {text}\n")
                    
                    if i < len(posts_to_send) - 1:
                        print(f"[INFO] Waiting {args.post_delay} seconds before next post...")
                        time.sleep(args.post_delay)
                else:
                    print("[ERROR] Post failed. Stopping.")
                    break

    return 0


if __name__ == "__main__":
    exit(main())
