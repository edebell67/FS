"""
PipHunter Subscriber API
Handles email subscriptions, preferences, and notifications.

Requires Supabase configuration in config.json:
{
    "supabase_url": "https://your-project.supabase.co",
    "supabase_anon_key": "your-anon-key"
}

Supabase Table Schema:
```sql
CREATE TABLE subscribers (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    verification_token UUID DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    verified_at TIMESTAMPTZ,
    unsubscribed_at TIMESTAMPTZ,
    preferences JSONB DEFAULT '{"daily_summary": true, "bias_shifts": true, "milestones": false}'::jsonb,
    source TEXT DEFAULT 'website'
);

CREATE INDEX idx_subscribers_email ON subscribers(email);
CREATE INDEX idx_subscribers_verified ON subscribers(verified) WHERE verified = TRUE;
```
"""

import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

BASE_DIR = Path(__file__).parent
CONFIG_FILE = BASE_DIR / "config.json"
SUBSCRIBERS_FILE = BASE_DIR / "subscribers.json"  # Fallback if no Supabase
WEBSITE_URL = "https://piphunter.io"


class SubscriberManager:
    """Manages email subscriptions for PipHunter."""

    DEFAULT_PREFERENCES = {
        "daily_summary": True,
        "bias_shifts": True,
        "milestones": False,
        "new_leader": False
    }

    def __init__(self):
        self.config = self._load_config()
        self.supabase_enabled = self._check_supabase()
        self._supabase_client = None

    def _load_config(self) -> Dict:
        """Load configuration from config.json."""
        if CONFIG_FILE.exists():
            try:
                with open(CONFIG_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading config: {e}")
        return {}

    def _check_supabase(self) -> bool:
        """Check if Supabase is configured."""
        return bool(
            self.config.get("supabase_url") and
            self.config.get("supabase_anon_key")
        )

    @property
    def supabase(self):
        """Lazy-load Supabase client."""
        if self._supabase_client is None and self.supabase_enabled:
            try:
                from supabase import create_client
                self._supabase_client = create_client(
                    self.config["supabase_url"],
                    self.config["supabase_anon_key"]
                )
            except ImportError:
                print("Supabase library not installed. Run: pip install supabase")
                self.supabase_enabled = False
            except Exception as e:
                print(f"Supabase connection error: {e}")
                self.supabase_enabled = False
        return self._supabase_client

    def _load_local_subscribers(self) -> Dict:
        """Load subscribers from local JSON file (fallback)."""
        if SUBSCRIBERS_FILE.exists():
            try:
                with open(SUBSCRIBERS_FILE, 'r') as f:
                    return json.load(f)
            except Exception:
                pass
        return {"subscribers": []}

    def _save_local_subscribers(self, data: Dict):
        """Save subscribers to local JSON file."""
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(data, f, indent=2, default=str)

    def validate_email(self, email: str) -> tuple[bool, str]:
        """Validate email format."""
        if not email:
            return False, "Email is required"

        email = email.strip().lower()

        # Basic format check
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, "Invalid email format"

        # Length check
        if len(email) > 254:
            return False, "Email too long"

        return True, email

    def subscribe(self, email: str, source: str = "website") -> Dict:
        """
        Subscribe a new email.

        Args:
            email: Email address to subscribe
            source: Where the subscription came from (website, api, mobile)

        Returns:
            Result dict with success status and message
        """
        # Validate email
        is_valid, result = self.validate_email(email)
        if not is_valid:
            return {"success": False, "error": result}

        email = result  # Normalized email

        if self.supabase_enabled and self.supabase:
            return self._subscribe_supabase(email, source)
        else:
            return self._subscribe_local(email, source)

    def _subscribe_supabase(self, email: str, source: str) -> Dict:
        """Subscribe using Supabase."""
        try:
            # Check if already exists
            existing = self.supabase.table("subscribers").select("*").eq("email", email).execute()

            if existing.data:
                subscriber = existing.data[0]
                if subscriber.get("unsubscribed_at"):
                    # Resubscribe
                    self.supabase.table("subscribers").update({
                        "unsubscribed_at": None,
                        "verified": False,
                        "verification_token": str(uuid.uuid4())
                    }).eq("email", email).execute()
                    return {
                        "success": True,
                        "message": "Welcome back! Check your email to confirm.",
                        "needs_verification": True
                    }
                elif subscriber.get("verified"):
                    return {"success": True, "message": "You're already subscribed!"}
                else:
                    return {
                        "success": True,
                        "message": "Check your email to confirm subscription.",
                        "needs_verification": True
                    }

            # New subscriber
            verification_token = str(uuid.uuid4())
            self.supabase.table("subscribers").insert({
                "email": email,
                "verification_token": verification_token,
                "source": source,
                "preferences": self.DEFAULT_PREFERENCES
            }).execute()

            # TODO: Send verification email
            return {
                "success": True,
                "message": "Thanks for subscribing! Check your email to confirm.",
                "needs_verification": True,
                "verification_token": verification_token  # For testing
            }

        except Exception as e:
            print(f"Supabase subscribe error: {e}")
            return {"success": False, "error": "Database error. Please try again."}

    def _subscribe_local(self, email: str, source: str) -> Dict:
        """Subscribe using local JSON file."""
        data = self._load_local_subscribers()

        # Check if exists
        existing = next(
            (s for s in data["subscribers"] if s["email"] == email),
            None
        )

        if existing:
            if existing.get("unsubscribed_at"):
                existing["unsubscribed_at"] = None
                existing["verified"] = False
                self._save_local_subscribers(data)
                return {
                    "success": True,
                    "message": "Welcome back! You've been resubscribed.",
                    "needs_verification": True
                }
            return {"success": True, "message": "You're already subscribed!"}

        # Add new subscriber
        verification_token = str(uuid.uuid4())
        data["subscribers"].append({
            "id": str(uuid.uuid4()),
            "email": email,
            "verified": False,
            "verification_token": verification_token,
            "created_at": datetime.now().isoformat(),
            "source": source,
            "preferences": self.DEFAULT_PREFERENCES
        })
        self._save_local_subscribers(data)

        return {
            "success": True,
            "message": "Thanks for subscribing!",
            "needs_verification": True,
            "verification_token": verification_token
        }

    def verify(self, token: str) -> Dict:
        """Verify a subscriber using their token."""
        if self.supabase_enabled and self.supabase:
            return self._verify_supabase(token)
        else:
            return self._verify_local(token)

    def _verify_supabase(self, token: str) -> Dict:
        """Verify using Supabase."""
        try:
            result = self.supabase.table("subscribers").update({
                "verified": True,
                "verified_at": datetime.utcnow().isoformat()
            }).eq("verification_token", token).eq("verified", False).execute()

            if result.data:
                return {"success": True, "message": "Email verified! You're all set."}
            return {"success": False, "error": "Invalid or expired token"}

        except Exception as e:
            print(f"Supabase verify error: {e}")
            return {"success": False, "error": "Verification failed"}

    def _verify_local(self, token: str) -> Dict:
        """Verify using local file."""
        data = self._load_local_subscribers()

        for subscriber in data["subscribers"]:
            if subscriber.get("verification_token") == token and not subscriber.get("verified"):
                subscriber["verified"] = True
                subscriber["verified_at"] = datetime.now().isoformat()
                self._save_local_subscribers(data)
                return {"success": True, "message": "Email verified! You're all set."}

        return {"success": False, "error": "Invalid or expired token"}

    def unsubscribe(self, email: str) -> Dict:
        """Unsubscribe an email."""
        is_valid, result = self.validate_email(email)
        if not is_valid:
            return {"success": False, "error": result}

        email = result

        if self.supabase_enabled and self.supabase:
            return self._unsubscribe_supabase(email)
        else:
            return self._unsubscribe_local(email)

    def _unsubscribe_supabase(self, email: str) -> Dict:
        """Unsubscribe using Supabase."""
        try:
            result = self.supabase.table("subscribers").update({
                "unsubscribed_at": datetime.utcnow().isoformat()
            }).eq("email", email).is_("unsubscribed_at", "null").execute()

            if result.data:
                return {"success": True, "message": "You've been unsubscribed."}
            return {"success": False, "error": "Email not found or already unsubscribed"}

        except Exception as e:
            print(f"Supabase unsubscribe error: {e}")
            return {"success": False, "error": "Unsubscribe failed"}

    def _unsubscribe_local(self, email: str) -> Dict:
        """Unsubscribe using local file."""
        data = self._load_local_subscribers()

        for subscriber in data["subscribers"]:
            if subscriber["email"] == email and not subscriber.get("unsubscribed_at"):
                subscriber["unsubscribed_at"] = datetime.now().isoformat()
                self._save_local_subscribers(data)
                return {"success": True, "message": "You've been unsubscribed."}

        return {"success": False, "error": "Email not found or already unsubscribed"}

    def update_preferences(self, email: str, preferences: Dict) -> Dict:
        """Update subscriber preferences."""
        valid_keys = set(self.DEFAULT_PREFERENCES.keys())
        filtered_prefs = {k: v for k, v in preferences.items() if k in valid_keys}

        if self.supabase_enabled and self.supabase:
            try:
                result = self.supabase.table("subscribers").update({
                    "preferences": filtered_prefs
                }).eq("email", email).execute()

                if result.data:
                    return {"success": True, "message": "Preferences updated"}
                return {"success": False, "error": "Subscriber not found"}
            except Exception as e:
                return {"success": False, "error": str(e)}
        else:
            data = self._load_local_subscribers()
            for subscriber in data["subscribers"]:
                if subscriber["email"] == email:
                    subscriber["preferences"] = {
                        **subscriber.get("preferences", self.DEFAULT_PREFERENCES),
                        **filtered_prefs
                    }
                    self._save_local_subscribers(data)
                    return {"success": True, "message": "Preferences updated"}
            return {"success": False, "error": "Subscriber not found"}

    def get_active_subscribers(self, preference_filter: Optional[str] = None) -> List[str]:
        """Get list of active, verified subscribers."""
        if self.supabase_enabled and self.supabase:
            try:
                query = self.supabase.table("subscribers").select("email, preferences").eq("verified", True).is_("unsubscribed_at", "null")
                result = query.execute()
                subscribers = result.data or []
            except Exception:
                return []
        else:
            data = self._load_local_subscribers()
            subscribers = [
                s for s in data["subscribers"]
                if s.get("verified") and not s.get("unsubscribed_at")
            ]

        # Filter by preference if specified
        if preference_filter:
            subscribers = [
                s for s in subscribers
                if s.get("preferences", {}).get(preference_filter, False)
            ]

        return [s["email"] for s in subscribers]

    def get_stats(self) -> Dict:
        """Get subscriber statistics."""
        if self.supabase_enabled and self.supabase:
            try:
                all_subs = self.supabase.table("subscribers").select("*").execute()
                data = all_subs.data or []
            except Exception:
                data = []
        else:
            local_data = self._load_local_subscribers()
            data = local_data.get("subscribers", [])

        total = len(data)
        verified = len([s for s in data if s.get("verified")])
        active = len([s for s in data if s.get("verified") and not s.get("unsubscribed_at")])
        unsubscribed = len([s for s in data if s.get("unsubscribed_at")])

        return {
            "total": total,
            "verified": verified,
            "active": active,
            "unsubscribed": unsubscribed,
            "pending_verification": total - verified - unsubscribed
        }


# Flask endpoint integration
def add_subscriber_routes(app):
    """Add subscriber API routes to existing Flask app."""
    from flask import request

    manager = SubscriberManager()

    @app.route('/api/subscribe', methods=['POST'])
    def subscribe():
        """Subscribe a new email."""
        data = request.json or {}
        email = data.get("email", "")
        source = data.get("source", "website")

        result = manager.subscribe(email, source)
        status = 200 if result.get("success") else 400
        return result, status

    @app.route('/api/subscribe/verify', methods=['GET'])
    def verify_subscription():
        """Verify email subscription."""
        token = request.args.get("token", "")
        if not token:
            return {"success": False, "error": "Token required"}, 400

        result = manager.verify(token)
        status = 200 if result.get("success") else 400
        return result, status

    @app.route('/api/unsubscribe', methods=['POST'])
    def unsubscribe():
        """Unsubscribe an email."""
        data = request.json or {}
        email = data.get("email", "")

        result = manager.unsubscribe(email)
        status = 200 if result.get("success") else 400
        return result, status

    @app.route('/api/subscribe/preferences', methods=['POST'])
    def update_preferences():
        """Update subscriber preferences."""
        data = request.json or {}
        email = data.get("email", "")
        preferences = data.get("preferences", {})

        if not email:
            return {"success": False, "error": "Email required"}, 400

        result = manager.update_preferences(email, preferences)
        status = 200 if result.get("success") else 400
        return result, status

    @app.route('/api/subscribe/stats', methods=['GET'])
    def subscriber_stats():
        """Get subscriber statistics."""
        return manager.get_stats()


# CLI usage
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PipHunter Subscriber Manager")
    parser.add_argument("--action", choices=["subscribe", "verify", "unsubscribe", "stats"],
                        required=True, help="Action to perform")
    parser.add_argument("--email", help="Email address")
    parser.add_argument("--token", help="Verification token")

    args = parser.parse_args()

    manager = SubscriberManager()
    print(f"Supabase enabled: {manager.supabase_enabled}")

    if args.action == "stats":
        stats = manager.get_stats()
        print(f"Subscriber Stats: {json.dumps(stats, indent=2)}")

    elif args.action == "subscribe":
        if not args.email:
            print("Error: --email required")
        else:
            result = manager.subscribe(args.email)
            print(f"Result: {json.dumps(result, indent=2)}")

    elif args.action == "verify":
        if not args.token:
            print("Error: --token required")
        else:
            result = manager.verify(args.token)
            print(f"Result: {json.dumps(result, indent=2)}")

    elif args.action == "unsubscribe":
        if not args.email:
            print("Error: --email required")
        else:
            result = manager.unsubscribe(args.email)
            print(f"Result: {json.dumps(result, indent=2)}")
