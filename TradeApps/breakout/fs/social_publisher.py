"""
PipHunter Social Media Publisher
Publishes market narratives to Twitter/X with teaser content linking to the website.

Credential lookup order:
1. Process environment
2. workstream/.env
3. access_token/key_X.json
4. config.json (legacy fallback)
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from narrative_generator import NarrativeGenerator

BASE_DIR = Path(__file__).parent
REPO_ROOT = BASE_DIR.resolve().parents[2]
CONFIG_FILE = BASE_DIR / "config.json"
POST_LOG_FILE = BASE_DIR / "social_posts.json"
WORKSTREAM_ENV_FILE = REPO_ROOT / "workstream" / ".env"
KEY_X_FILE = REPO_ROOT / "access_token" / "key_X.json"
WEBSITE_URL = "https://piphunter.io"  # Update when domain is live


def _console_safe_text(text: str) -> str:
    """Return text that can be printed on the active console encoding."""
    encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
    return text.encode(encoding, errors="replace").decode(encoding, errors="replace")


def _load_simple_env_file(path: Path) -> Dict[str, str]:
    """Load a minimal KEY=VALUE .env file without external dependencies."""
    values: Dict[str, str] = {}
    if not path.exists():
        return values

    try:
        for raw_line in path.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                values[key] = value
    except Exception as exc:
        print(f"Error loading env file {path}: {exc}")

    return values


def _load_key_x_file(path: Path) -> Dict[str, str]:
    """Load X credentials from the dedicated key_X.json file."""
    if not path.exists():
        return {}

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Error loading X key file {path}: {exc}")
        return {}

    return {
        "TWITTER_API_KEY": str(raw.get("Consumer Key", "")).strip(),
        "TWITTER_API_SECRET": str(raw.get("Consumer Key Secret", "")).strip(),
        "TWITTER_ACCESS_TOKEN": str(raw.get("Access Token", "")).strip(),
        "TWITTER_ACCESS_SECRET": str(raw.get("Access Token Secret", "")).strip(),
        "TWITTER_BEARER_TOKEN": str(raw.get("bearerToken", "")).strip(),
    }


class SocialPublisher:
    """Publishes trading narratives to social media platforms."""

    # Posting constraints - configurable
    DEFAULT_POST_INTERVAL_MINUTES = 10
    DEFAULT_TRADE_UPDATE_INTERVAL_SECONDS = 0
    MAX_POSTS_PER_DAY = 144  # Maximum posts per day (144 = 24h * 6 per hour)
    POST_CHAR_LIMIT = 280  # Standard Twitter limit
    COMPACT_CHAR_LIMIT = 142  # Compact format for best-strategy tweets
    DEFAULT_RETRY_ATTEMPTS = 3
    DEFAULT_RETRY_BACKOFF_SECONDS = 2

    # Hashtags for branding
    HASHTAGS = ["#PipHunter", "#Trading", "#ForexSignals"]
    COMPACT_HASHTAG = "#PH"  # Short hashtag for compact mode

    def __init__(self):
        self.config = self._load_config()
        self.workstream_env = _load_simple_env_file(WORKSTREAM_ENV_FILE)
        self.key_x_credentials = _load_key_x_file(KEY_X_FILE)
        self.post_log = self._load_post_log()
        self.narrative_gen = NarrativeGenerator(data_source="file")
        self.api_enabled = self._check_api_credentials()
        self.MIN_POST_INTERVAL_MINUTES = self._get_config_int(
            "twitter_post_interval_minutes",
            self._get_config_int("social_post_interval_minutes", self.DEFAULT_POST_INTERVAL_MINUTES),
        )
        self.TRADE_UPDATE_INTERVAL_SECONDS = self._get_config_int(
            "twitter_trade_update_interval_seconds",
            self.DEFAULT_TRADE_UPDATE_INTERVAL_SECONDS,
        )
        self.RETRY_ATTEMPTS = max(
            1,
            self._get_config_int("twitter_retry_attempts", self.DEFAULT_RETRY_ATTEMPTS),
        )
        self.RETRY_BACKOFF_SECONDS = max(
            0,
            self._get_config_int("twitter_retry_backoff_seconds", self.DEFAULT_RETRY_BACKOFF_SECONDS),
        )

    def _load_config(self) -> Dict:
        """Load configuration from config.json."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def _load_post_log(self) -> Dict:
        """Load post history from log file."""
        if POST_LOG_FILE.exists():
            try:
                with open(POST_LOG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading post log: {e}")
        return {"posts": [], "last_post_time": None}

    def _save_post_log(self):
        """Save post history to log file."""
        with open(POST_LOG_FILE, 'w') as f:
            json.dump(self.post_log, f, indent=2, default=str)

    def _get_config_int(self, key: str, default: int) -> int:
        """Read an integer config value with fallback."""
        value = self.config.get(key, default)
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def _get_twitter_credential(self, config_key: str, env_var: str) -> str:
        """Resolve credentials from env, then workstream env, key file, then config."""
        return (
            os.getenv(env_var)
            or self.workstream_env.get(env_var)
            or self.key_x_credentials.get(env_var)
            or self.config.get(config_key, "")
        )

    def _check_api_credentials(self) -> bool:
        """Check if Twitter API credentials are configured."""
        required_pairs = [
            ("twitter_api_key", "TWITTER_API_KEY"),
            ("twitter_api_secret", "TWITTER_API_SECRET"),
            ("twitter_access_token", "TWITTER_ACCESS_TOKEN"),
            ("twitter_access_secret", "TWITTER_ACCESS_SECRET"),
        ]
        return all(self._get_twitter_credential(config_key, env_var) for config_key, env_var in required_pairs)

    def _get_trigger_cooldown_seconds(self, trigger: str) -> int:
        """Return the minimum time between posts for a trigger."""
        if trigger == "trade_update":
            return self.TRADE_UPDATE_INTERVAL_SECONDS
        return self.MIN_POST_INTERVAL_MINUTES * 60

    def can_post(self, trigger: str = "manual") -> tuple[bool, str]:
        """Check if we can post based on rate limits."""
        now = datetime.now()

        # Check minimum interval
        if self.post_log.get("last_post_time"):
            last_post = datetime.fromisoformat(self.post_log["last_post_time"])
            elapsed_seconds = (now - last_post).total_seconds()
            required_gap = self._get_trigger_cooldown_seconds(trigger)
            if elapsed_seconds < required_gap:
                remaining_seconds = required_gap - elapsed_seconds
                if required_gap >= 60:
                    return False, f"Rate limit: wait {remaining_seconds / 60:.0f} more minutes"
                return False, f"Rate limit: wait {remaining_seconds:.0f} more seconds"

        # Check daily limit
        today = now.date().isoformat()
        today_posts = [p for p in self.post_log.get("posts", [])
                       if p.get("date", "")[:10] == today]
        if len(today_posts) >= self.MAX_POSTS_PER_DAY:
            return False, f"Daily limit reached ({self.MAX_POSTS_PER_DAY} posts)"

        return True, "OK"

    def format_teaser_post(self, metrics: Dict) -> str:
        """
        Format a teaser post for Twitter.
        Shows: Overall returns, bias, top performer name
        Hides: Trade details, prices, algo parameters
        """
        bias = metrics.get("bias", "NEUTRAL")
        buy_net = metrics.get("buy_net", 0)
        sell_net = metrics.get("sell_net", 0)
        imbalance = metrics.get("imbalance", 0)
        confidence = metrics.get("confidence", "LOW")
        top_strategy = metrics.get("top_strategy")
        winner = "BUY" if buy_net > sell_net else "SELL"

        emoji = "🟢" if winner == "BUY" else "🔴"

        # Build post
        lines = []
        lines.append(f"{emoji} LIVE BATTLE UPDATE")
        lines.append(f"Bias: {bias} | Confidence: {confidence}")

        if top_strategy:
            lines.append(f"Leader: {top_strategy[:15]}")

        lines.append(f"")
        lines.append(f"See full battle stats:")
        lines.append(WEBSITE_URL)
        lines.append("")
        lines.append(" ".join(self.HASHTAGS[:2]))

        post = "\n".join(lines)

        # Truncate if needed
        if len(post) > self.POST_CHAR_LIMIT:
            post = post[:self.POST_CHAR_LIMIT - 3] + "..."

        return post

    def format_milestone_post(self, milestone_type: str, value: float) -> str:
        """Format a milestone celebration post."""
        if milestone_type == "net_milestone":
            return f"""🎯 MILESTONE REACHED!

Our strategies just hit +{value:.0f} net return today!

See who's winning the battle:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        elif milestone_type == "new_leader":
            return f"""👑 NEW LEADER!

{value} has taken the top spot in today's battle!

Watch the live rankings:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        elif milestone_type == "bias_shift":
            return f"""⚡ BIAS SHIFT DETECTED!

Market sentiment has flipped to {value}!

See the full analysis:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

        return ""

    def format_hourly_summary(self, metrics: Dict) -> str:
        """Format an hourly summary post."""
        hour = datetime.now().strftime("%H:00")
        bias = metrics.get("bias", "NEUTRAL")
        confidence = metrics.get("confidence", "LOW")
        open_trades = metrics.get("open_trades", 0)

        return f"""📊 {hour} HOUR UPDATE

Market Bias: {bias}
Confidence: {confidence}
Active Positions: {open_trades}

Full battle stats:
{WEBSITE_URL}

{' '.join(self.HASHTAGS[:2])}"""

    def _truncate_with_suffix(self, value: str, max_len: int, suffix: str = "..") -> str:
        """Deterministically truncate a string and preserve a visible suffix."""
        if max_len <= 0:
            return ""
        if len(value) <= max_len:
            return value
        if max_len <= len(suffix):
            return suffix[:max_len]
        return value[: max_len - len(suffix)] + suffix

    def format_compact_best_strategy(self, metrics: Dict) -> str:
        """
        Format a compact best-strategy tweet (142 chars max).

        Shows: Best strategy name, net return, direction
        Format: "🏆 {STRATEGY} +{NET} {DIR} | {CONF} conf | piphunter.io #PH"
        """
        top = metrics.get("top_strategy", "")
        net = metrics.get("top_strategy_net", 0)
        bias = metrics.get("bias", "BUY")
        conf = metrics.get("confidence", "MED")[:3].upper()

        # Abbreviate confidence
        conf_map = {"HIG": "HI", "MED": "MED", "LOW": "LO"}
        conf_abbr = conf_map.get(conf, conf[:2])

        # Format net with sign
        net_str = f"+{net:.0f}" if net >= 0 else f"{net:.0f}"

        # Truncate strategy name to fit
        # Base: "🏆  +NET DIR | XX | piphunter.io #PH" ~45 chars
        max_strat_len = self.COMPACT_CHAR_LIMIT - 50
        strat = self._truncate_with_suffix(top, max_strat_len) if top else "---"

        emoji = "🟢" if bias == "BUY" else "🔴"

        post = f"{emoji} {strat} {net_str} {bias} | {conf_abbr} | piphunter.io {self.COMPACT_HASHTAG}"

        # Ensure under limit
        if len(post) > self.COMPACT_CHAR_LIMIT:
            # Further truncate strategy
            over = len(post) - self.COMPACT_CHAR_LIMIT
            strat = self._truncate_with_suffix(strat, max(1, len(strat) - over))
            post = f"{emoji} {strat} {net_str} {bias} | {conf_abbr} | piphunter.io {self.COMPACT_HASHTAG}"

        return post

    def format_compact_trade_update(self, trade: Dict) -> str:
        """
        Format a compact real-time trade update (142 chars max).

        Shows: Strategy, product, direction, result
        Format: "⚡ {STRAT} {PRODUCT} {DIR} {RESULT} | piphunter.io #PH"
        """
        strategy = self._truncate_with_suffix(trade.get("strategy_name", trade.get("strategy", "")), 20)
        product = trade.get("product", trade.get("symbol", ""))[:8]
        direction = trade.get("direction", "BUY")[:1]  # B or S
        result = trade.get("net_return", trade.get("pnl", 0))
        status = trade.get("status", "OPEN")

        # Format result
        result_str = f"+{result:.1f}" if result >= 0 else f"{result:.1f}"

        # Status emoji
        if status in ["CLOSED", "COMPLETE"]:
            status_emoji = "✅" if result >= 0 else "❌"
        else:
            status_emoji = "⚡"

        post = f"{status_emoji} {strategy} {product} {direction} {result_str} | piphunter.io {self.COMPACT_HASHTAG}"

        # Ensure under limit
        if len(post) > self.COMPACT_CHAR_LIMIT:
            over = len(post) - self.COMPACT_CHAR_LIMIT
            strategy = self._truncate_with_suffix(strategy, max(1, len(strategy) - over))
            post = f"{status_emoji} {strategy} {product} {direction} {result_str} | piphunter.io {self.COMPACT_HASHTAG}"

        return post

    def _send_tweet_with_retries(self, post_text: str, in_reply_to_tweet_id: Optional[str] = None) -> Dict:
        """Send a tweet with bounded retries and fixed backoff."""
        last_result: Dict = {"success": False, "error": "Unknown Twitter publishing failure"}
        for attempt in range(1, self.RETRY_ATTEMPTS + 1):
            result = self._send_tweet(post_text, in_reply_to_tweet_id=in_reply_to_tweet_id)
            if result.get("success"):
                if attempt > 1:
                    result["attempts"] = attempt
                return result
            last_result = result
            if attempt < self.RETRY_ATTEMPTS and self.RETRY_BACKOFF_SECONDS > 0:
                time.sleep(self.RETRY_BACKOFF_SECONDS)
        return last_result

    def publish_to_twitter(self, post_text: str, trigger: str = "manual") -> Dict:
        """
        Publish a post to Twitter.

        Args:
            post_text: The text to post
            trigger: What triggered this post (bias_shift, milestone, hourly, manual)

        Returns:
            Result dict with success status and details
        """
        # Check rate limits first
        can_post, reason = self.can_post(trigger=trigger)
        if not can_post:
            return {"success": False, "error": reason}

        # Check if API is configured
        if not self.api_enabled:
            # Dry run mode - just log the post
            print(_console_safe_text(f"[DRY RUN] Would post to Twitter:\n{post_text}\n"))
            result = {
                "success": True,
                "dry_run": True,
                "message": "API not configured - dry run mode"
            }
        else:
            # Actual Twitter API call
            try:
                result = self._send_tweet_with_retries(post_text)
            except Exception as e:
                return {"success": False, "error": str(e)}

        # Log the post
        post_entry = {
            "date": datetime.now().isoformat(),
            "trigger": trigger,
            "text": post_text[:100] + "..." if len(post_text) > 100 else post_text,
            "success": result.get("success", False),
            "dry_run": result.get("dry_run", False)
        }

        self.post_log["posts"].insert(0, post_entry)
        self.post_log["posts"] = self.post_log["posts"][:100]  # Keep last 100
        # Only successful posts should advance the cooldown clock.
        if result.get("success"):
            self.post_log["last_post_time"] = datetime.now().isoformat()
        self._save_post_log()

        return result

    def publish_thread(self, posts: List[str], trigger: str = "manual_thread") -> Dict:
        """
        Publish a reply thread where each post replies to the previous post.

        Args:
            posts: Ordered list of prepared post bodies.
            trigger: Trigger name for rate-limit and audit logging.

        Returns:
            Result dict with thread publish details.
        """
        normalized_posts = [str(post or "").strip() for post in posts]
        if not normalized_posts or not any(normalized_posts):
            return {"success": False, "error": "At least one non-empty post is required"}

        for index, post_text in enumerate(normalized_posts, start=1):
            if not post_text:
                return {"success": False, "error": f"Thread item {index} is empty"}
            if len(post_text) > self.POST_CHAR_LIMIT:
                return {
                    "success": False,
                    "error": f"Thread item {index} exceeds {self.POST_CHAR_LIMIT} character limit",
                    "length": len(post_text),
                    "index": index,
                }

        can_post, reason = self.can_post(trigger=trigger)
        if not can_post:
            return {"success": False, "error": reason}

        results: List[Dict] = []
        previous_tweet_id: Optional[str] = None

        if not self.api_enabled:
            for index, post_text in enumerate(normalized_posts, start=1):
                results.append(
                    {
                        "success": True,
                        "dry_run": True,
                        "message": "API not configured - dry run mode",
                        "tweet_id": f"dry_run_{index}",
                        "text": post_text,
                        "reply_to_tweet_id": previous_tweet_id,
                    }
                )
                previous_tweet_id = f"dry_run_{index}"
        else:
            for post_text in normalized_posts:
                try:
                    result = self._send_tweet_with_retries(post_text, in_reply_to_tweet_id=previous_tweet_id)
                except Exception as exc:
                    return {"success": False, "error": str(exc), "results": results}
                if not result.get("success"):
                    result["results"] = results
                    return result
                results.append(result)
                previous_tweet_id = result.get("tweet_id")

        tweet_ids = [str(result.get("tweet_id")) for result in results if result.get("tweet_id")]
        thread_urls = [f"https://x.com/i/web/status/{tweet_id}" for tweet_id in tweet_ids]

        post_entry = {
            "date": datetime.now().isoformat(),
            "trigger": trigger,
            "text": normalized_posts[0][:100] + "..." if len(normalized_posts[0]) > 100 else normalized_posts[0],
            "success": True,
            "dry_run": all(result.get("dry_run", False) for result in results),
            "thread": True,
            "thread_count": len(normalized_posts),
            "tweet_ids": tweet_ids,
        }
        self.post_log["posts"].insert(0, post_entry)
        self.post_log["posts"] = self.post_log["posts"][:100]
        self.post_log["last_post_time"] = datetime.now().isoformat()
        self._save_post_log()

        return {
            "success": True,
            "message": "Thread posted successfully",
            "tweet_ids": tweet_ids,
            "thread_urls": thread_urls,
            "results": results,
        }

    def _send_tweet(self, text: str, in_reply_to_tweet_id: Optional[str] = None) -> Dict:
        """
        Send a tweet using Twitter API v2.

        Requires tweepy library: pip install tweepy
        """
        try:
            import tweepy
        except ImportError:
            return {
                "success": False,
                "error": "tweepy library not installed. Run: pip install tweepy"
            }

        try:
            client = tweepy.Client(
                consumer_key=self._get_twitter_credential("twitter_api_key", "TWITTER_API_KEY"),
                consumer_secret=self._get_twitter_credential("twitter_api_secret", "TWITTER_API_SECRET"),
                access_token=self._get_twitter_credential("twitter_access_token", "TWITTER_ACCESS_TOKEN"),
                access_token_secret=self._get_twitter_credential("twitter_access_secret", "TWITTER_ACCESS_SECRET")
            )

            create_kwargs = {"text": text}
            if in_reply_to_tweet_id:
                create_kwargs["in_reply_to_tweet_id"] = in_reply_to_tweet_id

            response = client.create_tweet(**create_kwargs)

            return {
                "success": True,
                "tweet_id": response.data["id"],
                "message": "Tweet posted successfully",
                "reply_to_tweet_id": in_reply_to_tweet_id,
            }

        except tweepy.TweepyException as e:
            return {"success": False, "error": str(e)}

    def check_and_post_triggers(self, current_metrics: Dict, previous_metrics: Optional[Dict] = None) -> List[Dict]:
        """
        Check for trigger events and post if conditions are met.

        Triggers:
        1. Bias shift (BUY <-> SELL)
        2. Net milestone (+500, +1000, etc.)
        3. Hourly interval

        Args:
            current_metrics: Current market metrics
            previous_metrics: Previous metrics for comparison

        Returns:
            List of post results
        """
        results = []

        # Check bias shift
        if previous_metrics:
            prev_bias = previous_metrics.get("bias")
            curr_bias = current_metrics.get("bias")
            if prev_bias and curr_bias and prev_bias != curr_bias:
                post_text = self.format_milestone_post("bias_shift", curr_bias)
                if post_text:
                    result = self.publish_to_twitter(post_text, trigger="bias_shift")
                    results.append(result)
                    if result.get("success"):
                        return results  # One post per check

        # Check net milestone (every 500)
        buy_net = current_metrics.get("buy_net", 0)
        sell_net = current_metrics.get("sell_net", 0)
        total_net = max(buy_net, sell_net)  # Use the winning side

        if total_net > 0:
            milestone = (int(total_net) // 500) * 500
            if milestone > 0:
                last_milestone = self.post_log.get("last_net_milestone", 0)
                if milestone > last_milestone:
                    post_text = self.format_milestone_post("net_milestone", milestone)
                    if post_text:
                        result = self.publish_to_twitter(post_text, trigger="milestone")
                        if result.get("success"):
                            self.post_log["last_net_milestone"] = milestone
                            self._save_post_log()
                        results.append(result)
                        if result.get("success"):
                            return results

        return results

    def publish_hourly(self) -> Dict:
        """Publish an hourly summary post."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_hourly_summary(metrics)
        return self.publish_to_twitter(post_text, trigger="hourly")

    def publish_teaser(self) -> Dict:
        """Publish a teaser post with current metrics."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_teaser_post(metrics)
        return self.publish_to_twitter(post_text, trigger="teaser")

    def publish_compact_best_strategy(self) -> Dict:
        """Publish a compact best-strategy summary (142 chars)."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)

        post_text = self.format_compact_best_strategy(metrics)
        return self.publish_to_twitter(post_text, trigger="compact_best")

    def publish_trade_update(self, trade: Dict) -> Dict:
        """
        Publish a real-time trade update (142 chars).

        Args:
            trade: Trade data dict with strategy_name, product, direction, status, net_return

        Returns:
            Result dict with success status
        """
        # Check for duplicate suppression
        trade_id = trade.get("trade_id", trade.get("id", ""))
        if self._is_duplicate_trade_post(trade_id):
            return {"success": False, "error": "Duplicate trade post suppressed"}

        post_text = self.format_compact_trade_update(trade)
        result = self.publish_to_twitter(post_text, trigger="trade_update")

        # Track posted trade IDs for dedup
        if result.get("success"):
            self._mark_trade_posted(trade_id)

        return result

    def publish_direct_text(self, post_text: str, trigger: str = "manual_api") -> Dict:
        """
        Publish arbitrary text directly through the configured X/Twitter API path.

        Args:
            post_text: Fully prepared post body.
            trigger: Trigger name for rate-limit and audit logging.

        Returns:
            Result dict with success status and details.
        """
        text = str(post_text or "").strip()
        if not text:
            return {"success": False, "error": "Post text is required"}
        if len(text) > self.POST_CHAR_LIMIT:
            return {
                "success": False,
                "error": f"Post exceeds {self.POST_CHAR_LIMIT} character limit",
                "length": len(text),
            }
        return self.publish_to_twitter(text, trigger=trigger)

    def publish_direct_thread(self, posts: List[str], trigger: str = "manual_api_thread") -> Dict:
        """
        Publish an arbitrary prepared reply thread through the configured X/Twitter API path.

        Args:
            posts: Ordered list of fully prepared post bodies.
            trigger: Trigger name for rate-limit and audit logging.

        Returns:
            Result dict with success status and details.
        """
        normalized_posts = [str(post or "").strip() for post in posts]
        if not normalized_posts or not any(normalized_posts):
            return {"success": False, "error": "At least one non-empty post is required"}
        return self.publish_thread(normalized_posts, trigger=trigger)

    def _is_duplicate_trade_post(self, trade_id: str) -> bool:
        """Check if this trade has already been posted recently."""
        if not trade_id:
            return False
        posted = self.post_log.get("posted_trade_ids", [])
        return trade_id in posted

    def _mark_trade_posted(self, trade_id: str):
        """Mark a trade as posted for duplicate suppression."""
        if not trade_id:
            return
        if "posted_trade_ids" not in self.post_log:
            self.post_log["posted_trade_ids"] = []
        self.post_log["posted_trade_ids"].append(trade_id)
        # Keep only last 100 trade IDs
        self.post_log["posted_trade_ids"] = self.post_log["posted_trade_ids"][-100:]
        self._save_post_log()

    def publish_best_strategy_trade_updates(self, trades: Optional[List[Dict]] = None) -> List[Dict]:
        """Publish updates for trades that belong to the current best strategy."""
        target_trades = trades if trades is not None else self.get_best_strategy_trades()
        results: List[Dict] = []
        for trade in target_trades:
            results.append(self.publish_trade_update(trade))
        return results

    def get_best_strategy_trades(self) -> List[Dict]:
        """Get recent trades for the current best strategy."""
        data = self.narrative_gen.load_data()
        metrics = self.narrative_gen.extract_metrics(data)
        best_strategy = metrics.get("top_strategy")

        if not best_strategy:
            return []

        # Load trades from grid_live
        grid_data = data.get("grid_live", {})
        trades = grid_data.get("trades", [])

        # Filter for best strategy
        return [t for t in trades if t.get("strategy_name", t.get("strategy", "")) == best_strategy]


# Flask endpoint integration
def add_social_routes(app):
    """Add social publishing API routes to existing Flask app."""

    publisher = SocialPublisher()

    @app.route('/api/social/status', methods=['GET'])
    def get_social_status():
        """Get social publishing status and recent posts."""
        can_post, reason = publisher.can_post()
        return {
            "api_enabled": publisher.api_enabled,
            "can_post": can_post,
            "reason": reason,
            "recent_posts": publisher.post_log.get("posts", [])[:10],
            "last_post_time": publisher.post_log.get("last_post_time")
        }

    @app.route('/api/social/preview', methods=['GET'])
    def preview_post():
        """Preview what would be posted."""
        data = publisher.narrative_gen.load_data()
        metrics = publisher.narrative_gen.extract_metrics(data)

        compact_best = publisher.format_compact_best_strategy(metrics)

        return {
            "teaser": publisher.format_teaser_post(metrics),
            "hourly": publisher.format_hourly_summary(metrics),
            "compact_best": compact_best,
            "compact_best_length": len(compact_best),
            "metrics": metrics
        }

    @app.route('/api/social/publish', methods=['POST'])
    def manual_publish():
        """Manually trigger a post (requires API key)."""
        from flask import request

        post_type = request.json.get("type", "teaser")

        if post_type == "teaser":
            result = publisher.publish_teaser()
        elif post_type == "hourly":
            result = publisher.publish_hourly()
        elif post_type == "compact_best":
            result = publisher.publish_compact_best_strategy()
        else:
            return {"success": False, "error": f"Unknown post type: {post_type}"}, 400

        return result

    @app.route('/api/social/publish_trade', methods=['POST'])
    def publish_trade():
        """Publish a real-time trade update."""
        from flask import request

        trade = request.json.get("trade", {})
        if not trade:
            return {"success": False, "error": "No trade data provided"}, 400

        result = publisher.publish_trade_update(trade)
        return result

    @app.route('/api/social/publish_best_strategy_trades', methods=['POST'])
    def publish_best_strategy_trades():
        """Publish trade updates for the current best strategy."""
        from flask import request

        payload = request.json or {}
        trades = payload.get("trades")
        result = publisher.publish_best_strategy_trade_updates(trades=trades)
        return {"results": result, "count": len(result)}

    @app.route('/api/social/best_strategy_trades', methods=['GET'])
    def get_best_strategy_trades():
        """Get trades for the current best strategy."""
        trades = publisher.get_best_strategy_trades()
        return {"trades": trades, "count": len(trades)}

    @app.route('/api/social/x_api_post', methods=['POST'])
    def publish_x_api_post():
        """Publish arbitrary prepared text through the X API-backed path."""
        from flask import request

        payload = request.json or {}
        post_text = payload.get("text", "")
        trigger = payload.get("trigger", "manual_api")

        result = publisher.publish_direct_text(post_text, trigger=trigger)
        status_code = 200 if result.get("success") else 400
        return result, status_code

    @app.route('/api/social/x_api_thread_post', methods=['POST'])
    def publish_x_api_thread_post():
        """Publish an arbitrary prepared reply thread through the X API-backed path."""
        from flask import request

        payload = request.json or {}
        posts = payload.get("posts", [])
        trigger = payload.get("trigger", "manual_api_thread")

        result = publisher.publish_direct_thread(posts, trigger=trigger)
        status_code = 200 if result.get("success") else 400
        return result, status_code


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PipHunter Social Publisher")
    parser.add_argument("--action", choices=["preview", "publish", "status", "publish_best_strategy_trades"],
                        default="preview", help="Action to perform")
    parser.add_argument("--type", choices=["teaser", "hourly", "compact_best"],
                        default="teaser", help="Post type")

    args = parser.parse_args()

    publisher = SocialPublisher()

    if args.action == "status":
        can_post, reason = publisher.can_post()
        print(f"API Enabled: {publisher.api_enabled}")
        print(f"Can Post: {can_post} ({reason})")
        print(f"Post Interval: {publisher.MIN_POST_INTERVAL_MINUTES} minutes")
        print(f"Trade Update Interval: {publisher.TRADE_UPDATE_INTERVAL_SECONDS} seconds")
        print(f"Recent Posts: {len(publisher.post_log.get('posts', []))}")

    elif args.action == "preview":
        data = publisher.narrative_gen.load_data()
        metrics = publisher.narrative_gen.extract_metrics(data)

        if args.type == "teaser":
            print("=== TEASER POST PREVIEW ===")
            print(publisher.format_teaser_post(metrics))
        elif args.type == "hourly":
            print("=== HOURLY POST PREVIEW ===")
            print(publisher.format_hourly_summary(metrics))
        elif args.type == "compact_best":
            compact = publisher.format_compact_best_strategy(metrics)
            print("=== COMPACT BEST STRATEGY PREVIEW ===")
            print(_console_safe_text(compact))
            print(f"\n[Length: {len(compact)}/{publisher.COMPACT_CHAR_LIMIT} chars]")

    elif args.action == "publish":
        if args.type == "teaser":
            result = publisher.publish_teaser()
        elif args.type == "hourly":
            result = publisher.publish_hourly()
        elif args.type == "compact_best":
            result = publisher.publish_compact_best_strategy()
        print(f"Result: {json.dumps(result, indent=2)}")

    elif args.action == "publish_best_strategy_trades":
        results = publisher.publish_best_strategy_trade_updates()
        print(f"Results: {json.dumps(results, indent=2)}")
