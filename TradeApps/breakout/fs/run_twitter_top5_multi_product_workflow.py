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
WORKFLOW_STATUS = ROOT / "twitter_top5_multi_product_workflow_status.json"
WORKFLOW_ARTIFACT = ROOT / "twitter_top5_multi_product_workflow_result.json"
API_HEALTH_URL = "http://localhost:5000/api/health"
API_POST_URL = "http://localhost:5000/api/social/x_api_thread_post"
PACKAGE_ROOT = ROOT / "json" / "live" / "social_posting_package"
PACKAGE_FILENAME = "top5_weekly_posting_package.json"
# [2026-04-07 13:20] V20260407_1320 - Changed to post ONLY the consolidated view
PACKAGE_PAYLOAD_KEY = "consolidated_twitter_post"
# [2026-04-07 15:50] V20260407_1550 - Updated trigger name to match new 4-hour cadence (was every_6_hours)
WORKFLOW_TRIGGER = "breakout_top5_multi_product_every_4_hours"
SUSPENSION_REASON = (
    "Top-5 multi-product X posting workflow is suspended. "
    "Use run_twitter_consolidated_leaderboard_workflow.py for the only approved recurring X post."
)


def _write_status(status: dict) -> None:
    WORKFLOW_STATUS.write_text(json.dumps(status, indent=2), encoding="utf-8")


def _new_status(run_date: str) -> dict:
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "steps": {
            "verify_api": {"ok": False, "details": "", "artifact": API_HEALTH_URL},
            "generate_content": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / PACKAGE_FILENAME)},
            "prepare_payload": {"ok": False, "details": "", "artifact": str(PACKAGE_ROOT / run_date / PACKAGE_FILENAME)},
            "submit_post": {"ok": False, "details": "", "artifact": str(WORKFLOW_ARTIFACT)},
            "record_outcome": {"ok": False, "details": "", "artifact": str(WORKFLOW_ARTIFACT)},
        },
        "final_status": "failed",
    }


def _mark_step(status: dict, step: str, ok: bool, details: str) -> None:
    status["steps"][step]["ok"] = ok
    status["steps"][step]["details"] = details
    _write_status(status)


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


def _load_package_json(run_date: str) -> dict:
    package_path = PACKAGE_ROOT / run_date / PACKAGE_FILENAME
    if not package_path.exists():
        raise FileNotFoundError(f"Posting package not found: {package_path}")
    return json.loads(package_path.read_text(encoding="utf-8"))


def _validate_payload(run_date: str, generated_started_at: float) -> tuple[bool, str, list[str]]:
    package_path = PACKAGE_ROOT / run_date / PACKAGE_FILENAME
    if not package_path.exists():
        return False, f"Posting package was not created: {package_path}", []

    if package_path.stat().st_mtime < generated_started_at - 1:
        return False, f"Posting package was not refreshed by the current generator run: {package_path}", []

    package = _load_package_json(run_date)
    # [2026-04-07 14:45] V20260407_1445 - Consolidated post is now a list of strings (threaded)
    posts = package.get(PACKAGE_PAYLOAD_KEY)
    if not posts or not isinstance(posts, list):
        return False, f"Posting package is missing {PACKAGE_PAYLOAD_KEY} or is not a list", []

    # Basic length and content check for each post in the thread
    validated_posts = []
    for i, post_text in enumerate(posts, start=1):
        text = str(post_text or "").strip()
        if not text:
            return False, f"Consolidated post part {i} is empty", []
        if len(text) > 280:
            return False, f"Consolidated post part {i} exceeds 280 characters ({len(text)})", []
        validated_posts.append(text)
    
    details = f"Validated {len(validated_posts)} consolidated post parts in {package_path}"
    return True, details, validated_posts


def _write_result_artifact(run_date: str, thread_posts: list[str], status_code: int, response_payload: dict) -> None:
    artifact = {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "request": {
            "url": API_POST_URL,
            "trigger": WORKFLOW_TRIGGER,
            "thread_posts": [
                {
                    "index": index,
                    "length": len(post_text),
                    "text": post_text,
                }
                for index, post_text in enumerate(thread_posts, start=1)
            ],
        },
        "response": {
            "status_code": status_code,
            "payload": response_payload,
        },
    }
    WORKFLOW_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")


def _write_suspension_artifact(run_date: str) -> None:
    artifact = {
        "timestamp": datetime.datetime.now().isoformat(),
        "run_date": run_date,
        "request": {
            "url": API_POST_URL,
            "trigger": WORKFLOW_TRIGGER,
            "thread_posts": [],
        },
        "response": {
            "status_code": 409,
            "payload": {
                "success": False,
                "error": SUSPENSION_REASON,
            },
        },
    }
    WORKFLOW_ARTIFACT.write_text(json.dumps(artifact, indent=2), encoding="utf-8")


def main() -> int:
    run_date = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()
    status = _new_status(run_date)
    _write_status(status)
    _mark_step(status, "submit_post", False, SUSPENSION_REASON)
    status["final_status"] = "suspended"
    _write_suspension_artifact(run_date)
    _write_status(status)
    return 1

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
        payload_ok, payload_details, thread_posts = _validate_payload(run_date, generate_started_at)
    except Exception as exc:
        _mark_step(status, "prepare_payload", False, f"Payload validation failed: {exc}")
        return 1
    if not payload_ok:
        _mark_step(status, "prepare_payload", False, payload_details)
        return 1
    _mark_step(status, "prepare_payload", True, payload_details)

    try:
        status_code, response_payload = _request_json(
            API_POST_URL,
            {
                "posts": thread_posts,
                "trigger": WORKFLOW_TRIGGER,
            },
        )
    except Exception as exc:
        _mark_step(
            status,
            "submit_post",
            False,
            f"POST {API_POST_URL} failed: {exc}",
        )
        return 1

    _write_result_artifact(run_date, thread_posts, status_code, response_payload)

    if status_code != 200 or not response_payload.get("success"):
        _mark_step(status, "submit_post", False, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")
        return 1
    _mark_step(status, "submit_post", True, f"POST {API_POST_URL} returned HTTP {status_code}: {response_payload}")

    tweet_ids = response_payload.get("tweet_ids") or []
    thread_urls = response_payload.get("thread_urls") or []
    if not tweet_ids:
        _mark_step(status, "record_outcome", False, f"No tweet IDs returned: {response_payload}")
        return 1

    _mark_step(
        status,
        "record_outcome",
        True,
        f"Recorded {len(tweet_ids)} tweet IDs and {len(thread_urls)} URLs in {WORKFLOW_ARTIFACT}",
    )
    status["final_status"] = "success"
    _write_status(status)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
