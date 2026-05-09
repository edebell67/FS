from __future__ import annotations

import datetime
import json
import subprocess
import sys
import time
from pathlib import Path
from urllib import error, request


ROOT = Path(r"C:\Users\edebe\eds\TradeApps\breakout\fs")
GENERATE_SCRIPT = ROOT / "tools" / "social_posting_package" / "generate_posting_package.py"
TEMP_TWEET = ROOT / "temp_tweet_consolidated_leaderboard.txt"
WORKFLOW_STATUS = ROOT / "twitter_consolidated_leaderboard_workflow_status.json"
API_HEALTH_URL = "http://localhost:5000/api/health"
API_POST_URL = "http://localhost:5000/api/social/x_api_post"
API_RESPONSE_ARTIFACT = ROOT / "twitter_consolidated_leaderboard_post_response.json"
PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
PACKAGE_FILENAME = "consolidated_leaderboard_posting_package.json"
WORKFLOW_TRIGGER = "breakout_consolidated_leaderboard_every_4_hours"


def _write_status(status: dict) -> None:
    WORKFLOW_STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")


def _new_status(run_date: str) -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "steps": {
            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
            "generate_content": {"ok": False, "details": "", "artifact": str(TEMP_TWEET)},
            "validate_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / PACKAGE_FILENAME)},
            "submit_post": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
            "record_outcome": {"ok": False, "details": "", "artifact": str(API_RESPONSE_ARTIFACT)},
        },
        "final_status": "failed",
    }


def _mark_step(status: dict, step: str, ok: bool, details: str) -> None:
    status["steps"][step]["ok"] = ok
    status["steps"][step]["details"] = details
    _write_status(status)


def _request_json(url: str, payload: dict | None = None) -> tuple[int, dict]:
    body = None
    headers = {}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(url, data=body, headers=headers, method="POST" if body is not None else "GET")
    try:
        with request.urlopen(req, timeout=30) as response:
            raw = response.read().decode("utf-8", errors="replace")
            return int(response.status), json.loads(raw)
    except error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload_json = json.loads(raw)
        except json.JSONDecodeError:
            payload_json = {"success": False, "error": raw or str(exc)}
        return int(exc.code), payload_json


def _is_duplicate_content_response(status_code: int, response_payload: dict) -> bool:
    error_text = str(response_payload.get("error", "")).lower()
    return status_code in {400, 403} and "duplicate content" in error_text


def _build_duplicate_retry_text(tweet_text: str, retry_time: datetime.datetime | None = None) -> str:
    retry_time = retry_time or datetime.datetime.now()
    lines = tweet_text.splitlines()
    if not lines:
        raise ValueError("Cannot build duplicate retry text from an empty tweet")

    first_line = lines[0].rstrip()
    stamp = retry_time.strftime("%H:%M")
    candidate_first_line = f"{first_line} {stamp}"
    candidate_lines = [candidate_first_line, *lines[1:]]
    candidate_text = "\n".join(candidate_lines).strip()
    if len(candidate_text) > 280:
        raise ValueError(
            f"Duplicate retry text would exceed 280 characters ({len(candidate_text)})"
        )
    return candidate_text


def _verify_api_health() -> tuple[bool, str]:
    try:
        status_code, payload = _request_json(API_HEALTH_URL)
    except Exception as exc:
        return False, f"Health check failed: {exc}"

    if status_code != 200:
        return False, f"Health check returned HTTP {status_code}: {payload}"
    if payload.get("status") != "ok":
        return False, f"Health check returned unexpected payload: {payload}"
    return True, f"API reachable on {API_HEALTH_URL}: {payload}"


def _run_command(command: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        timeout=180000,
    )


def _load_package_json(run_date: str) -> dict:
    package_path = PACKAGE_ROOT / run_date / PACKAGE_FILENAME
    if not package_path.exists():
        raise FileNotFoundError(f"Posting package not found: {package_path}")
    return json.loads(package_path.read_text(encoding="utf-8"))


def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, str]:
    if not TEMP_TWEET.exists():
        return False, f"{TEMP_TWEET.name} was not created", ""

    tweet_text = TEMP_TWEET.read_text(encoding="utf-8").strip()
    if not tweet_text:
        return False, f"{TEMP_TWEET.name} is empty after generation", ""

    if TEMP_TWEET.stat().st_mtime < generated_started_at - 1:
        return False, f"{TEMP_TWEET.name} was not rewritten by the current generator run", tweet_text

    package = _load_package_json(run_date)
    twitter_post = package.get("twitter_post") or {}
    prepared_post = str(twitter_post.get("text", "")).strip()
    if not prepared_post:
        return False, "Posting package is missing twitter_post.text", tweet_text

    if tweet_text != prepared_post:
        return False, f"{TEMP_TWEET.name} does not match twitter_post.text", tweet_text

    if len(tweet_text) > 280:
        return False, f"Prepared post exceeds 280 characters ({len(tweet_text)})", tweet_text

    details = f"Validated payload ({len(tweet_text)} chars) matches {PACKAGE_ROOT / run_date / PACKAGE_FILENAME}"
    return True, details, tweet_text


def _write_api_response_artifact(
    run_date: str,
    tweet_text: str,
    status_code: int,
    response_payload: dict,
    attempts: list[dict] | None = None,
) -> None:
    artifact = {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "request": {
            "url": API_POST_URL,
            "trigger": WORKFLOW_TRIGGER,
            "text_length": len(tweet_text),
            "text": tweet_text,
        },
        "response": {
            "status_code": status_code,
            "payload": response_payload,
        },
    }
    if attempts:
        artifact["attempts"] = attempts
    API_RESPONSE_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")


def main() -> int:
    run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    status = _new_status(run_date)
    _write_status(status)

    api_ok, api_details = _verify_api_health()
    if not api_ok:
        _mark_step(status, "verify_api", False, api_details)
        return 1
    _mark_step(status, "verify_api", True, api_details)

    generate_started_at = time.time()
    generate_result = _run_command(["python", str(GENERATE_SCRIPT), "--date", run_date])
    if generate_result.returncode != 0:
        _mark_step(
            status,
            "generate_content",
            False,
            f"Generator failed with code {generate_result.returncode}: {generate_result.stdout}\n{generate_result.stderr}",
        )
        return 1
    _mark_step(status, "generate_content", True, generate_result.stdout.strip() or "Generator completed successfully")

    try:
        payload_ok, payload_details, tweet_text = _validate_payload(run_date, generate_started_at)
    except Exception as exc:
        _mark_step(status, "validate_payload", False, f"Payload validation failed: {exc}")
        return 1
    if not payload_ok:
        _mark_step(status, "validate_payload", False, payload_details)
        return 1
    _mark_step(status, "validate_payload", True, payload_details)

    attempts = [
        {
            "attempt": 1,
            "text_length": len(tweet_text),
            "text": tweet_text,
        }
    ]
    try:
        status_code, response_payload = _request_json(
            API_POST_URL,
            {
                "text": tweet_text,
                "trigger": WORKFLOW_TRIGGER,
            },
        )
    except Exception as exc:
        _mark_step(status, "submit_post", False, f"POST {API_POST_URL} failed: {exc}")
        return 1

    if _is_duplicate_content_response(status_code, response_payload):
        try:
            retry_text = _build_duplicate_retry_text(tweet_text)
        except Exception as exc:
            _write_api_response_artifact(run_date, tweet_text, status_code, response_payload, attempts)
            _mark_step(
                status,
                "submit_post",
                False,
                f"Duplicate-content retry could not be prepared: {exc}. Initial response: {response_payload}",
            )
            return 1

        attempts.append(
            {
                "attempt": 2,
                "reason": "duplicate_content_retry",
                "text_length": len(retry_text),
                "text": retry_text,
            }
        )
        try:
            status_code, response_payload = _request_json(
                API_POST_URL,
                {
                    "text": retry_text,
                    "trigger": WORKFLOW_TRIGGER,
                },
            )
            tweet_text = retry_text
        except Exception as exc:
            _write_api_response_artifact(run_date, tweet_text, status_code, response_payload, attempts)
            _mark_step(
                status,
                "submit_post",
                False,
                f"Duplicate-content retry POST {API_POST_URL} failed: {exc}",
            )
            return 1

    _write_api_response_artifact(run_date, tweet_text, status_code, response_payload, attempts)

    if status_code != 200 or not response_payload.get("success"):
        _mark_step(status, "submit_post", False, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
        return 1
    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")

    tweet_id = str(response_payload.get("tweet_id") or "").strip()
    if not tweet_id:
        _mark_step(status, "record_outcome", False, f"No tweet ID returned: {response_payload}")
        return 1

    _mark_step(status, "record_outcome", True, f"Recorded tweet ID {tweet_id} in {API_RESPONSE_ARTIFACT}")
    status["final_status"] = "success"
    _write_status(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
