import os
import json
import re
import shlex
import subprocess

MAX_CONCURRENT_INPROGRESS_TASKS = 3
import sys
import datetime
import shutil
from dataclasses import dataclass
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from typing import Any
from urllib.parse import parse_qs, urlparse

WORKSTREAM_DIR = r"C:\Users\edebe\eds\workstream"
FOLDERS = [
    "000_epic", "000_epic/codex", "000_epic/gemini", "000_epic/claude", "000_epic/general",
    "050_review", "050_review/codex", "050_review/gemini", "050_review/claude", "050_review/general",
    "100_backlog", "100_backlog/codex", "100_backlog/gemini", "100_backlog/claude", "100_backlog/general",
    "100_backlog/blocker", "100_backlog/blocker/codex", "100_backlog/blocker/gemini", "100_backlog/blocker/claude", "100_backlog/blocker/general",
    "200_inprogress", "200_inprogress/codex", "200_inprogress/gemini", "200_inprogress/claude", "200_inprogress/general",
    "200_inprogress/blocker", "200_inprogress/blocker/codex", "200_inprogress/blocker/gemini", "200_inprogress/blocker/claude", "200_inprogress/blocker/general",
    "300_complete", "300_complete/codex", "300_complete/gemini", "300_complete/claude", "300_complete/general",
    "400_failed", "400_failed/codex", "400_failed/gemini", "400_failed/claude", "400_failed/general",
    "500_dump", "500_dump/codex", "500_dump/gemini", "500_dump/claude", "500_dump/general"
]

# The duration in seconds for the news ticker to complete one full scroll across the screen
TICKER_SCROLL_SPEED_SECONDS = 240
TASK_REVIEW_STATIC_DIR = Path(WORKSTREAM_DIR) / "apps" / "task_review" / "static"
EPIC_DECOMPOSE_CLI_PATH = Path(WORKSTREAM_DIR) / "epic_decompose_cli.py"
EPIC_REVIEW_MODEL_FOLDERS = ("gemini", "claude", "codex")
EPIC_REVIEW_STATE_FOLDERS = ("100_backlog", "200_inprogress", "300_complete", "400_failed")
MODEL_LANES = ("claude", "gemini", "codex")
BLOCKER_STATE_FOLDERS = ("100_backlog", "200_inprogress")
PIPELINE_FOCUS_STATE_FOLDERS = ("000_epic", "050_review", "100_backlog", "200_inprogress", "300_complete", "400_failed")
PIPELINE_FOCUS_ACTIVE_FOLDERS = ("100_backlog", "200_inprogress")
PIPELINE_FOCUS_MODE_SELECTED_ONLY = "selected_only"
PIPELINE_FOCUS_CONFIG_PATH = Path(WORKSTREAM_DIR) / ".process" / "pipeline_focus.json"
PIPELINE_PENDING_DIRNAME = "pending"

EPIC_FAMILY_PATTERNS: list[tuple[str, tuple[str, ...]]] = [
    ("strategy_warehouse_marketing_engine", ("strategy_warehouse_marketing_engine", "strategy_warehouse_autonomous_marketing_engine", "warehouse_marketing_engine")),
    ("trading_strategy_warehouse", ("trading_strategy_warehouse",)),
    ("autonomous_trading_signal_platform", ("autonomous_trading_signal_platform", "trading_signal_miniapp")),
    ("mvp_prd_mobile_quarterly_export", ("mvp_prd_mobile_quarterly_export", "mvp_prd_quarterly_export_10min", "quarterly_export_in_10_minutes")),
    ("sfx_technical_design", ("synthetic_frontier_sfx", "sfx_technical_design", "sfx_derivatives_market_technical_design")),
    ("bizpa", ("bizpa",)),
    ("piphunter", ("piphunter",)),
    ("breakout", ("breakout", "trade_bucket")),
    ("kanban", ("kanban",)),
    ("workstream", ("workstream", "agent_cli")),
    ("skills", ("skills",)),
]

KNOWN_EPIC_FAMILIES = {family for family, _ in EPIC_FAMILY_PATTERNS}


def _resolve_agent_binary(agent: str) -> str:
    """Resolve the specific binary/CLI for a given agent. [2026-03-17 V20260317_1530]"""
    agent_lower = agent.lower()
    
    # Try system PATH first
    found = shutil.which(agent_lower) or shutil.which(f"{agent_lower}.cmd") or shutil.which(f"{agent_lower}.exe")
    if found:
        return found
        
    # Fallback to known npm global path
    npm_path = Path.home() / "AppData" / "Roaming" / "npm" / f"{agent_lower}.cmd"
    if npm_path.exists():
        return str(npm_path)
        
    # Final fallback to codex if everything else fails (legacy behavior)
    return shutil.which("codex") or shutil.which("codex.cmd") or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")


def _extract_markdown_section(content: str, heading: str) -> str:
    match = re.search(rf"##\s*{re.escape(heading)}\s*\n(.*?)(?=\n##\s+|\Z)", content, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _parse_objective_delivery_coverage(evidence_section: str, full_content: str) -> int | None:
    candidates = [evidence_section, full_content]
    for source in candidates:
        if not source:
            continue
        match = re.search(r"Objective-Delivery-Coverage:\s*(\d{1,3})%", source, re.IGNORECASE)
        if match:
            try:
                value = int(match.group(1))
            except ValueError:
                return None
            return max(0, min(100, value))
    return None


def _parse_auto_acceptance(evidence_section: str, full_content: str) -> bool:
    candidates = [evidence_section, full_content]
    for source in candidates:
        if not source:
            continue
        match = re.search(r"Auto-Acceptance:\s*(true|false)", source, re.IGNORECASE)
        if match:
            return match.group(1).strip().lower() == "true"
    return True


def _parse_evidence_items(evidence_section: str) -> list[dict[str, str]]:
    if not evidence_section:
        return []

    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in evidence_section.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped:
            continue
        type_match = re.match(r"-\s*Evidence-Type:\s*(.+)", stripped, re.IGNORECASE)
        if type_match:
            if current:
                items.append(current)
            current = {
                "type": type_match.group(1).strip(),
                "artifact": "",
                "objective_proved": "",
                "status": "",
            }
            continue
        if current is None:
            continue
        artifact_match = re.match(r"-\s*Artifact:\s*(.+)", stripped, re.IGNORECASE)
        if artifact_match:
            current["artifact"] = artifact_match.group(1).strip()
            continue
        objective_match = re.match(r"-\s*Objective-Proved:\s*(.+)", stripped, re.IGNORECASE)
        if objective_match:
            current["objective_proved"] = objective_match.group(1).strip()
            continue
        status_match = re.match(r"-\s*Status:\s*(.+)", stripped, re.IGNORECASE)
        if status_match:
            current["status"] = status_match.group(1).strip()
            continue
    if current:
        items.append(current)
    return items


def _resolve_agent_name(folder: str) -> str:
    parts = [part for part in str(folder or "").replace("\\", "/").split("/") if part]
    for part in reversed(parts):
        lowered = part.lower()
        if lowered in {"codex", "gemini", "claude", "general"}:
            return lowered
    return "general"


def _blocker_dir(column: str, agent: str) -> Path:
    return Path(WORKSTREAM_DIR) / column / "blocker" / agent


def _lane_dir(column: str, agent: str) -> Path:
    return Path(WORKSTREAM_DIR) / column / agent


def _append_retry_history(task_path: str | Path, message: str) -> None:
    path = Path(task_path)
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return

    retry_match = re.search(r"Retry-Count:\s*(\d+)", content, re.IGNORECASE)
    retry_count = int(retry_match.group(1)) if retry_match else 0
    new_retry_count = retry_count + 1
    if retry_match:
        content = re.sub(
            r"Retry-Count:\s*\d+",
            f"Retry-Count: {new_retry_count}",
            content,
            count=1,
            flags=re.IGNORECASE,
        )
    else:
        content += f"\n\n## Retry History\nRetry-Count: {new_retry_count}\n"

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content += f"- {timestamp}: {message}\n"
    path.write_text(content, encoding="utf-8")


def _lane_has_capacity(agent: str) -> bool:
    backlog_dir = _lane_dir("100_backlog", agent)
    inprog_dir = _lane_dir("200_inprogress", agent)
    review_dir = _lane_dir("050_review", agent)
    active_count = 0
    for folder in (backlog_dir, inprog_dir, review_dir):
        if not folder.exists():
            continue
        active_count += sum(
            1 for path in folder.glob("*.md")
            if path.is_file() and not path.name.startswith(".")
        )
    return active_count == 0


def _claim_blocked_task_for_lane(agent: str) -> tuple[bool, str]:
    for column in ("200_inprogress", "100_backlog"):
        for source_agent in ("general", *MODEL_LANES):
            blocker_dir = _blocker_dir(column, source_agent)
            if not blocker_dir.exists():
                continue
            blocked_files = sorted(
                path for path in blocker_dir.glob("*.md")
                if path.is_file() and not path.name.startswith(".")
            )
            if not blocked_files:
                continue
            source_path = blocked_files[0]
            target_dir = _lane_dir(column, agent)
            target_dir.mkdir(parents=True, exist_ok=True)
            target_path = target_dir / source_path.name
            _append_retry_history(
                source_path,
                f"Retry scheduled in same column `{column}` from blocker queue `{source_agent}` to lane `{agent}`.",
            )
            shutil.move(str(source_path), str(target_path))
            return True, f"{source_path.name} -> {column}/{agent}"
    return False, ""


def _auto_accept_task(filepath: str, agent: str) -> None:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r"- `Completion Status`:.*",
        "- `Completion Status`: Auto accepted",
        content,
        count=1,
        flags=re.IGNORECASE,
    )
    if "Auto Accepted: TRUE" not in content:
        content += "\n\n# Auto Acceptance\nAuto Accepted: TRUE\nReason: Objective-Delivery-Coverage=100% and Auto-Acceptance=true\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    target_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
    os.makedirs(target_dir, exist_ok=True)
    os.rename(filepath, os.path.join(target_dir, os.path.basename(filepath)))


def _auto_retry_failed_task(filepath: str, max_retries: int = 2) -> tuple[bool, str]:
    """Analyze failure and retry with same or different agent.

    Returns (success, message) tuple indicating if retry was scheduled.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, f"Failed to read task: {e}"

    # Parse retry count from task content
    retry_match = re.search(r"Retry-Count:\s*(\d+)", content, re.IGNORECASE)
    retry_count = int(retry_match.group(1)) if retry_match else 0

    if retry_count >= max_retries:
        return False, f"Max retries ({max_retries}) reached, leaving in failed"

    # Increment retry count in content
    new_retry_count = retry_count + 1
    if retry_match:
        content = re.sub(
            r"Retry-Count:\s*\d+",
            f"Retry-Count: {new_retry_count}",
            content,
            flags=re.IGNORECASE
        )
    else:
        content += f"\n\n## Retry History\nRetry-Count: {new_retry_count}\n"

    # Add retry timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    content += f"- Retry scheduled at {timestamp}\n"

    # Strategy: rotate to different agent on retry (round-robin)
    current_agent = _resolve_agent_name(filepath)
    agents = ["claude", "gemini", "codex"]
    if current_agent in agents:
        next_idx = (agents.index(current_agent) + 1) % len(agents)
    else:
        # General tasks: use retry count to pick agent (round-robin)
        next_idx = (new_retry_count - 1) % len(agents)
    next_agent = agents[next_idx]

    # Move back to backlog for the next agent
    target_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{next_agent}")
    os.makedirs(target_dir, exist_ok=True)

    # Write updated content and move file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    target_path = os.path.join(target_dir, os.path.basename(filepath))
    shutil.move(filepath, target_path)

    return True, f"Retry {new_retry_count}: moved to {next_agent} backlog"


def _validate_task_completion(filepath: str) -> tuple[bool, list[str]]:
    """Run automated checks before accepting a task.

    Returns (is_valid, list_of_issues) tuple.
    """
    issues = []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return False, [f"Failed to read task: {e}"]

    # 1. Check Objective-Delivery-Coverage
    evidence_section = _extract_markdown_section(content, "Evidence")
    odc = _parse_objective_delivery_coverage(evidence_section, content)
    if odc is None:
        issues.append("No Objective-Delivery-Coverage found")
    elif odc < 100:
        issues.append(f"ODC is {odc}%, need 100%")

    # 2. Check Auto-Acceptance flag
    auto_accept = _parse_auto_acceptance(evidence_section, content)
    if not auto_accept:
        issues.append("Auto-Acceptance is disabled for this task")

    # 3. Check for unchecked items (incomplete checklist)
    unchecked = re.findall(r"- \[ \]", content)
    if unchecked:
        issues.append(f"{len(unchecked)} unchecked checklist items remain")

    # 4. Check evidence items have required fields
    evidence_items = _parse_evidence_items(evidence_section)
    for i, item in enumerate(evidence_items, 1):
        if not item.get("artifact"):
            issues.append(f"Evidence item {i} missing Artifact")
        if not item.get("status"):
            issues.append(f"Evidence item {i} missing Status")
        elif item.get("status", "").lower() not in ("verified", "complete", "passed"):
            issues.append(f"Evidence item {i} status is '{item.get('status')}', not verified")

    # 5. Check for test results section if tests are mentioned
    if re.search(r"test|spec", content, re.IGNORECASE):
        test_section = _extract_markdown_section(content, "Test Results")
        if not test_section:
            test_section = _extract_markdown_section(content, "Tests")
        if not test_section:
            issues.append("Tests mentioned but no Test Results section found")

    return len(issues) == 0, issues


def _process_pending_tasks() -> dict[str, list[str]]:
    """Background processor for agentic task management.

    Processes:
    1. Tasks in 050_review - validates and auto-accepts if criteria met
    2. Tasks in 400_failed - retries with different agent if under max retries

    Returns dict with 'accepted', 'retried', and 'errors' lists.
    """
    results = {
        "accepted": [],
        "retried": [],
        "skipped": [],
        "errors": []
    }
    focus_cfg = _load_pipeline_focus_config()
    focus_family = _canonical_epic_family(focus_cfg.get("epic_family"))
    focus_enabled = bool(focus_cfg.get("enabled") and focus_family)

    # Process tasks in review for auto-acceptance
    review_dir = Path(WORKSTREAM_DIR) / "050_review"
    if review_dir.exists():
        for agent_dir in ["claude", "gemini", "codex", "general"]:
            agent_path = review_dir / agent_dir
            if agent_path.exists():
                for task_file in agent_path.glob("*.md"):
                    try:
                        if focus_enabled and _detect_epic_family_for_file(task_file) != focus_family:
                            results["skipped"].append(f"{task_file.name}: suspended by focus mode ({focus_family})")
                            continue
                        is_valid, issues = _validate_task_completion(str(task_file))
                        if is_valid:
                            agent = _resolve_agent_name(str(task_file))
                            _auto_accept_task(str(task_file), agent)
                            results["accepted"].append(f"{task_file.name} -> 300_complete/{agent}")
                        else:
                            results["skipped"].append(f"{task_file.name}: {'; '.join(issues)}")
                    except Exception as e:
                        results["errors"].append(f"{task_file.name}: {e}")

    # Process failed tasks for retry
    failed_dir = Path(WORKSTREAM_DIR) / "400_failed"
    if failed_dir.exists():
        for agent_dir in ["claude", "gemini", "codex", "general"]:
            agent_path = failed_dir / agent_dir
            if agent_path.exists():
                for task_file in agent_path.glob("*.md"):
                    try:
                        if focus_enabled and _detect_epic_family_for_file(task_file) != focus_family:
                            results["skipped"].append(f"{task_file.name}: suspended by focus mode ({focus_family})")
                            continue
                        success, message = _auto_retry_failed_task(str(task_file))
                        if success:
                            results["retried"].append(f"{task_file.name}: {message}")
                        else:
                            results["skipped"].append(f"{task_file.name}: {message}")
                    except Exception as e:
                        results["errors"].append(f"{task_file.name}: {e}")

    return results


# HTML Template exactly matching beautiful dark mode UI guidelines
HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Workstream Kanban Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-deep: #080a18;
            --bg-accent: #0f1225;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        /* Date range dropdown styling */
        select#dateRangePreset option {
            background: #1e1e2e;
            color: #e2e8f0;
            padding: 8px;
        }
        select#dateRangePreset:focus {
            outline: 2px solid #6366f1;
            outline-offset: 2px;
        }
        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, var(--bg-deep) 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px;
        }
        .header {
            text-align: center; margin-bottom: 40px; padding: 30px;
            background: var(--glass-bg); backdrop-filter: blur(20px);
            border-radius: 24px; border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }
        .header h1 { font-size: 2.5em; font-weight: 800; margin-bottom: 10px; background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .kanban-board {
            display: grid;
            grid-template-columns: minmax(340px, 1.2fr) repeat(6, minmax(280px, 1fr));
            gap: 24px;
            align-items: start;
            overflow-x: auto;
            padding-bottom: 10px;
            scroll-padding-left: 30px;
        }
        .kanban-column {
            background: rgba(15, 18, 37, 0.6);
            border-radius: 20px; border: 1px solid var(--glass-border);
            padding: 20px; min-height: 500px;
            display: flex; flex-direction: column; gap: 16px;
        }
        .kanban-column.epic-column {
            position: sticky;
            left: 0;
            z-index: 3;
            background: linear-gradient(180deg, rgba(20, 26, 56, 0.98), rgba(11, 14, 30, 0.96));
            box-shadow: 18px 0 28px rgba(8, 10, 24, 0.55);
            border-color: rgba(99, 102, 241, 0.35);
        }
        .column-header {
            display: flex; justify-content: space-between; align-items: center;
            padding-bottom: 15px; border-bottom: 1px solid var(--glass-border);
            margin-bottom: 10px; font-weight: 700; font-size: 1.1em;
            color: #cbd5e1;
            text-transform: uppercase; letter-spacing: 1px;
        }
        .task-count {
            background: rgba(255, 255, 255, 0.1); padding: 2px 8px;
            border-radius: 12px; font-size: 0.8em; font-family: monospace;
        }
        .task-card {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 16px; padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            transition: transform 0.2s, box-shadow 0.2s;
            cursor: pointer;
            border-left: 4px solid #6366f1; /* Default project color */
        }
        .task-card.status-transition-flash {
            animation: taskStatusFlash 2000ms ease-out 1 both;
        }
        .task-card.complete-transition-flash {
            animation: taskCompleteFlash 3000ms ease-out 1 both;
        }
        .task-card.failed-perimeter-highlight {
            border-color: rgba(239, 68, 68, 0.9);
            box-shadow: inset 0 0 0 2px rgba(239, 68, 68, 0.95), 0 0 18px rgba(239, 68, 68, 0.35);
        }
        .task-card.failed-perimeter-highlight:hover {
            box-shadow: inset 0 0 0 2px rgba(239, 68, 68, 0.95), 0 0 22px rgba(239, 68, 68, 0.45);
        }
        .task-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            background: rgba(255, 255, 255, 0.06);
        }
        @keyframes taskStatusFlash {
            0% {
                background: rgba(96, 165, 250, 0.28);
                box-shadow: inset 0 0 0 2px rgba(96, 165, 250, 0.95), 0 0 0 rgba(96, 165, 250, 0);
            }
            35% {
                background: rgba(96, 165, 250, 0.18);
                box-shadow: inset 0 0 0 2px rgba(96, 165, 250, 0.7), 0 0 16px rgba(96, 165, 250, 0.35);
            }
            100% {
                background: var(--glass-bg);
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
        }
        @keyframes taskCompleteFlash {
            0% {
                background: rgba(34, 197, 94, 0.32);
                box-shadow: inset 0 0 0 2px rgba(34, 197, 94, 1), 0 0 0 rgba(34, 197, 94, 0);
            }
            35% {
                background: rgba(34, 197, 94, 0.22);
                box-shadow: inset 0 0 0 2px rgba(34, 197, 94, 0.8), 0 0 18px rgba(34, 197, 94, 0.45);
            }
            100% {
                background: var(--glass-bg);
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            }
        }
        .project-badge {
            display: inline-block; padding: 4px 10px; font-size: 0.7em;
            font-weight: 700; text-transform: uppercase; border-radius: 8px;
            margin-bottom: 12px; letter-spacing: 1px;
        }
        .task-title {
            font-size: 1.1em; font-weight: 600; margin-bottom: 8px; line-height: 1.4;
        }
        .task-summary {
            font-size: 0.85em; color: var(--text-dim); margin-bottom: 15px;
            line-height: 1.5;
        }
        .task-footer {
            display: flex; justify-content: space-between; align-items: center;
            font-size: 0.75em; color: var(--text-dim); border-top: 1px solid var(--glass-border);
            padding-top: 10px;
        }
        .task-date { font-family: monospace; opacity: 0.8; }
        
        /* Modal Styles */
        .modal-overlay {
            display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.7); backdrop-filter: blur(8px);
            z-index: 1000; justify-content: center; align-items: center;
        }
        .modal-content {
            background: var(--bg-accent); border: 1px solid var(--glass-border);
            border-radius: 16px; width: 98vw; max-width: 1800px; height: 92vh; max-height: 92vh;
            display: flex; flex-direction: column; overflow: hidden;
            box-shadow: 0 15px 50px rgba(0,0,0,0.5);
            animation: fadeIn 0.2s ease-out forwards;
        }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        .modal-header {
            padding: 20px; border-bottom: 1px solid var(--glass-border);
            display: flex; justify-content: space-between; align-items: center;
            background: rgba(15, 18, 37, 0.8);
        }
        .modal-header h2 { font-size: 1.2em; color: #a855f7; display: flex; align-items: center; gap: 10px; }
        .modal-header h2 i { color: #6366f1; }
        .close-btn {
            background: rgba(255, 255, 255, 0.05); border: 1px solid var(--glass-border); color: var(--text-dim);
            font-size: 1.2em; cursor: pointer; transition: all 0.2s; border-radius: 8px; width: 36px; height: 36px;
            display: flex; align-items: center; justify-content: center;
        }
        .close-btn:hover { background: rgba(244, 63, 94, 0.2); color: var(--rose, #f43f5e); border-color: rgba(244, 63, 94, 0.4); }
        .btn-action {
            background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); color: #818cf8;
            padding: 8px 16px; border-radius: 8px; font-size: 0.9em; font-weight: 600; cursor: pointer; transition: all 0.2s;
            display: flex; align-items: center; gap: 8px;
        }
        .btn-action:hover { background: rgba(99, 102, 241, 0.3); color: #fff; }
        .modal-body {
            padding: 25px; overflow-y: auto; flex-grow: 1;
        }
        .modal-body pre {
            white-space: pre-wrap; word-wrap: break-word; font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.95em; line-height: 1.6; color: #cbd5e1;
        }
        .search-container {
            margin-top: 20px;
            display: flex;
            justify-content: center;
            gap: 10px;
        }
        .search-input {
            padding: 12px 20px;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            background: rgba(0,0,0,0.2);
            color: var(--text-main);
            width: 400px;
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
        }
        .search-input:focus { outline: none; border-color: #a855f7; }
        .search-btn {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            border: none;
            padding: 12px 24px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
        }
        .epic-review-btn {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border: none;
            padding: 12px 24px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .epic-review-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
        }
        .epic-decomposition-btn {
            background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
            border: none;
            padding: 12px 24px;
            border-radius: 20px;
            color: white;
            cursor: pointer;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .epic-decomposition-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }
        .epic-reconciliation-btn {
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border: none;
            color: white;
            padding: 12px 20px;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.95em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .epic-reconciliation-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
        }
        .worker-controls {
            display: flex;
            align-items: center;
            gap: 8px;
            margin-left: 20px;
            padding: 6px 12px;
            background: rgba(15, 18, 37, 0.6);
            border-radius: 12px;
            border: 1px solid var(--glass-border);
        }
        .worker-controls-label {
            font-size: 0.8rem;
            color: var(--text-dim);
            margin-right: 4px;
        }
        .worker-toggle {
            display: flex;
            align-items: center;
            gap: 4px;
            padding: 6px 10px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            font-size: 0.85rem;
            font-weight: 500;
            border: 1px solid transparent;
        }
        .worker-toggle.active {
            background: rgba(16, 185, 129, 0.2);
            color: #10b981;
            border-color: rgba(16, 185, 129, 0.3);
        }
        .worker-toggle.excluded {
            background: rgba(244, 63, 94, 0.2);
            color: #f43f5e;
            border-color: rgba(244, 63, 94, 0.3);
            text-decoration: line-through;
        }
        .worker-toggle:hover {
            transform: scale(1.05);
        }
        .worker-toggle .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #10b981;
        }
        .worker-toggle.excluded .status-dot {
            background: #f43f5e;
        }
        #searchResults {
            display: none;
            background: rgba(15, 18, 37, 0.6);
            border-radius: 20px; border: 1px solid var(--glass-border);
            padding: 20px;
            margin-top: 20px;
        }
        .search-snippet {
            font-family: 'JetBrains Mono', Consolas, monospace;
            font-size: 0.85em; color: #a855f7; background: rgba(0,0,0,0.3);
            padding: 8px; border-radius: 6px; margin-top: 8px;
        }
        @media (max-width: 900px) {
            .modal-content {
                width: 99vw;
                height: 95vh;
                max-height: 95vh;
                border-radius: 10px;
            }
            .modal-header { padding: 14px; }
            .modal-body { padding: 14px; }
        }
        
        /* News Ticker Components */
        .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background: rgba(15, 18, 37, 0.9);
            border-bottom: 1px solid var(--glass-border);
            padding: 8px 0;
            box-sizing: content-box;
            position: relative;
        }
        .ticker {
            display: inline-block;
            white-space: nowrap;
            padding-right: 100%;
            box-sizing: content-box;
            transform: translateX(0);
            animation: ticker ##TICKER_SCROLL_SPEED##s linear infinite;
        }
        .ticker:hover {
            animation-play-state: paused;
        }
        @keyframes ticker {
            0% { transform: translateX(100vw); }
            100% { transform: translateX(-100%); }
        }
        .ticker-item {
            display: inline-block;
            padding: 0 30px;
            font-family: 'Outfit', sans-serif;
            font-size: 0.95em;
            font-weight: 500;
        }
        .ticker-agent { color: #a855f7; font-weight: 800; text-transform: uppercase; }
        .ticker-state { color: #6366f1; font-weight: 600; text-transform: uppercase; margin: 0 5px; }
        .ticker-task { color: var(--text-main); }
        .ticker-separator { color: #f43f5e; margin: 0 15px; font-weight: 800; display: inline-block; }

    </style>
</head>
<body>
    <div class="ticker-wrap">
        <div class="ticker" id="newsTicker">
            <span class="ticker-item"><span class="ticker-agent">SYSTEM</span> <span class="ticker-state">INITIALIZING</span> <span class="ticker-task">Fetching latest kanban pipeline statuses...</span></span>
        </div>
    </div>
    
    <div class="header">
        <h1>🚀 Workstream Kanban</h1>
        <p style="color: var(--text-dim);">Real-time workflow monitoring (Refreshes every 2s) <br> <span id="last-updated" style="font-family: monospace; font-size: 0.9em; color: #a855f7;"></span></p>
        <div class="search-container">
            <div style="display: flex; align-items: center; gap: 8px;">
                <select id="dateRangePreset" onchange="applyDatePreset()" style="padding: 12px 16px; border-radius: 20px; border: 1px solid var(--glass-border); background: #1e1e2e; color: #e2e8f0; font-family: 'Outfit', sans-serif; font-size: 0.95rem; cursor: pointer; min-width: 130px;">
                    <option value="today">Today</option>
                    <option value="yesterday">Yesterday</option>
                    <option value="this_week">This Week</option>
                    <option value="last_week">Last Week</option>
                    <option value="this_month">This Month</option>
                    <option value="last_month">Last Month</option>
                    <option value="last_7">Last 7 Days</option>
                    <option value="last_30">Last 30 Days</option>
                    <option value="all">All Time</option>
                    <option value="custom">Custom Range</option>
                </select>
                <span id="dateRangeDisplay" style="font-size: 0.85rem; color: var(--text-dim); white-space: nowrap;"></span>
                <div id="customDateRange" style="display: none; align-items: center; gap: 6px;">
                    <input type="date" id="startDate" style="padding: 8px 12px; border-radius: 12px; border: 1px solid var(--glass-border); background: rgba(0,0,0,0.2); color: var(--text-main); color-scheme: dark; font-size: 0.9rem;">
                    <span style="color: var(--text-dim);">to</span>
                    <input type="date" id="endDate" style="padding: 8px 12px; border-radius: 12px; border: 1px solid var(--glass-border); background: rgba(0,0,0,0.2); color: var(--text-main); color-scheme: dark; font-size: 0.9rem;">
                    <button onclick="applyCustomDateRange()" style="padding: 8px 14px; border-radius: 12px; background: linear-gradient(135deg, #8b5cf6, #6d28d9); border: none; color: white; cursor: pointer; font-size: 0.85rem;">Apply</button>
                </div>
            </div>
            <input type="hidden" id="kanbanDateFilter">
            <input type="text" id="searchInput" class="search-input" placeholder="Search task contents, titles..." onkeyup="if(event.key === 'Enter') performSearch()">
            <button class="search-btn" onclick="performSearch()"><i class="fas fa-search"></i> Search</button>
            <button class="search-btn" id="clearSearchBtn" style="display:none; background: rgba(244, 63, 94, 0.2); color: #f43f5e;" onclick="clearSearch()"><i class="fas fa-times"></i> Clear</button>
            <button class="epic-review-btn" onclick="openEpicReview()" title="Review & Allocate Epic Tasks"><i class="fas fa-tasks"></i> Epic Review</button>
            <button class="epic-decomposition-btn" onclick="openEpicDecomposition()" title="Decompose Epic into Tasks"><i class="fas fa-project-diagram"></i> Decompose Epic</button>
            <button class="epic-reconciliation-btn" onclick="openEpicReconciliation()" title="View Epic Delivery Reconciliation"><i class="fas fa-clipboard-check"></i> Reconciliation</button>
            <button class="search-btn" style="margin-left:20px; background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="openCreateModal()"><i class="fas fa-plus"></i> Create Entry</button>
            <div class="worker-controls">
                <span class="worker-controls-label">Workers:</span>
                <div class="worker-toggle active" id="worker-codex" onclick="toggleWorker('codex')" title="Click to exclude/include Codex worker">
                    <span class="status-dot"></span>
                    <span>Codex</span>
                </div>
                <div class="worker-toggle active" id="worker-gemini" onclick="toggleWorker('gemini')" title="Click to exclude/include Gemini worker">
                    <span class="status-dot"></span>
                    <span>Gemini</span>
                </div>
                <div class="worker-toggle active" id="worker-claude" onclick="toggleWorker('claude')" title="Click to exclude/include Claude worker">
                    <span class="status-dot"></span>
                    <span>Claude</span>
                </div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; margin-left: 16px; padding: 10px 12px; border-radius: 16px; background: rgba(255,255,255,0.04); border: 1px solid var(--glass-border);">
                <span style="font-size:0.8rem; color: var(--text-dim); font-weight:700; text-transform: uppercase;">Epic Focus</span>
                <select id="focusEpicSelect" style="padding: 8px 10px; border-radius: 10px; border: 1px solid var(--glass-border); background: rgba(0,0,0,0.2); color: var(--text-main); min-width: 220px;">
                    <option value="">Select epic...</option>
                </select>
                <button class="search-btn" onclick="applyPipelineFocus()" style="padding: 8px 14px;"><i class="fas fa-filter"></i> Focus</button>
                <button class="search-btn" onclick="clearPipelineFocus()" style="padding: 8px 14px; background: rgba(148,163,184,0.18); color: #cbd5e1;"><i class="fas fa-rotate-left"></i> Clear</button>
                <span id="pipelineFocusStatus" style="font-size:0.8rem; color: var(--text-dim); white-space: nowrap;">Focus: All</span>
            </div>
        </div>
    </div>

    <div class="kanban-board" id="mainBoard">
        <div class="kanban-column epic-column" id="col-000_epic" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '000_epic')">
            <div class="column-header">
                <div>📋 Epic <span class="task-count" id="count-000_epic">0</span></div>
                <button id="toggleAllEpicBtn" onclick="toggleAllEpic()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-000_epic"></div>
        </div>
        <div class="kanban-column" id="col-050_review" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '050_review')">
            <div class="column-header">
                <div>📝 Review <span class="task-count" id="count-050_review">0</span></div>
            </div>
            <div class="column-content" id="list-050_review"></div>
        </div>
        <div class="kanban-column" id="col-100_backlog" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '100_backlog')">
            <div class="column-header">
                <div>🎯 Backlog <span class="task-count" id="count-100_backlog">0</span></div>
                <button id="toggleAllBacklogBtn" onclick="toggleAllBacklog()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-100_backlog"></div>
        </div>
        <div class="kanban-column" id="col-200_inprogress" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '200_inprogress')">
            <div class="column-header">
                <div>⚡ In Progress <span class="task-count" id="count-200_inprogress">0</span></div>
                <button id="toggleAllInprogressBtn" onclick="toggleAllInprogress()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-200_inprogress"></div>
        </div>
        <div class="kanban-column" id="col-300_complete" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '300_complete')">
            <div class="column-header">
                <div>✅ Complete <span class="task-count" id="count-300_complete">0</span></div>
                <button id="toggleAllBtn" onclick="toggleAllComplete()" style="background:transparent; border:1px solid #6366f1; color:#6366f1; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-300_complete"></div>
        </div>
        <div class="kanban-column" id="col-delivered_epic">
            <div class="column-header">
                <div>📦 Delivered (Epic/Backlog) <span class="task-count" id="count-delivered_epic">0</span></div>
                <button id="toggleAllDeliveredBtn" onclick="toggleAllDelivered()" style="background:transparent; border:1px solid #10b981; color:#10b981; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-delivered_epic"></div>
        </div>
        <div class="kanban-column" id="col-400_failed" ondragover="handleDragOver(event)" ondrop="handleDrop(event, '400_failed')">
            <div class="column-header">
                <div>💥 Failed & Blocked <span class="task-count" id="count-400_failed">0</span></div>
                <button id="toggleAllFailedBtn" onclick="toggleAllFailed()" style="background:transparent; border:1px solid #ef4444; color:#ef4444; border-radius:4px; cursor:pointer; font-size:0.6em; padding:4px 8px; text-transform: uppercase;">Expand All</button>
            </div>
            <div class="column-content" id="list-400_failed"></div>
        </div>
    </div>
    
    <div id="searchResults">
        <h2 style="margin-bottom: 20px;"><i class="fas fa-search"></i> Search Results (<span id="searchCount">0</span>)</h2>
        <div id="searchResultsList"></div>
    </div>

    <!-- Modal Overlay -->
    <div id="contentModal" class="modal-overlay" onclick="closeModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="far fa-file-alt"></i> <span id="modalTitle">Loading Document...</span></h2>
                <div style="display:flex; gap:10px;">
                    <button class="btn-action" id="editBtnModal" onclick="openEditModal()" style="display:none; background: rgba(16, 185, 129, 0.2); color: #10b981; border-color: rgba(16, 185, 129, 0.4);" title="Edit Task">
                        <i class="fas fa-edit"></i> Edit
                    </button>
                    <button class="btn-action" onclick="openAndCloseLocal()" title="Open externally in VSCode/Editor">
                        <i class="fas fa-external-link-alt"></i> Open Externally
                    </button>
                    <button class="btn-action" id="deleteBtnModal" onclick="deleteCurrentFile()" style="display:none; background: rgba(244, 63, 94, 0.2); color: #f43f5e; border-color: rgba(244, 63, 94, 0.4);" title="Delete Task">
                        <i class="fas fa-trash"></i> Delete
                    </button>
                    <button class="btn-action" id="dumpBtnModal" onclick="dumpCurrentFile()" style="display:none; background: rgba(251, 191, 36, 0.2); color: #fbbf24; border-color: rgba(251, 191, 36, 0.4);" title="Dump Task - Move to 500_dump without deleting">
                        <i class="fas fa-archive"></i> Dump
                    </button>
                    <button class="close-btn" onclick="closeModal()"><i class="fas fa-times"></i></button>
                </div>
            </div>
            <div class="modal-body">
                <pre id="modalContentText"></pre>
            </div>
        </div>
    </div>

    <!-- Verify Modal Overlay -->
    <div id="verifyModal" class="modal-overlay" onclick="closeVerifyModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="fas fa-search"></i> <span id="vModalTitle">Verification Required</span></h2>
                <button class="close-btn" onclick="closeVerifyModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body" id="vModalBody">
                <!-- Javascript injects content here -->
            </div>
        </div>
    </div>

    <!-- Feedback Modal Overlay -->
    <div id="feedbackModal" class="modal-overlay" onclick="closeFeedbackModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2><i class="fas fa-comment-dots"></i> <span id="fbModalTitle">User Feedback Required</span></h2>
                <button class="close-btn" onclick="closeFeedbackModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body" id="fbModalBody">
                <!-- Javascript injects content here -->
            </div>
        </div>
    </div>

    <!-- Create Entry Modal Overlay -->
    <div id="createModal" class="modal-overlay" onclick="closeCreateModal(event)">
        <div class="modal-content" onclick="event.stopPropagation()">
            <div class="modal-header">
                <h2 id="createModalTitle"><i class="fas fa-plus"></i> <span>Create New Entry</span></h2>
                <button class="close-btn" onclick="closeCreateModal()"><i class="fas fa-times"></i></button>
            </div>
            <div class="modal-body">
                <div style="display:grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap:15px; margin-bottom:15px;">
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Type</label>
                        <select id="createType" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="task">Atomic Task (To Do)</option>
                            <option value="backlog">Backlog Specification</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Agent Lane</label>
                        <select id="createAgent" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="codex">Codex</option>
                            <option value="gemini">Gemini</option>
                            <option value="claude">Claude</option>
                            <option value="general">General</option>
                            <option value="">📁 ROOT (Hold)</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Priority</label>
                        <select id="createPriority" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="1">P1 (Immediate/High)</option>
                            <option value="2" selected>P2 (Normal)</option>
                            <option value="3">P3 (Low/Backlog)</option>
                        </select>
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Completion Action</label>
                        <select id="createCompletionAction" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                            <option value="Awaiting user verification" selected>Awaiting user verification</option>
                            <option value="Evidence of completion">Evidence of completion</option>
                            <option value="Proceed without permission">Proceed without permission</option>
                            <option value="Proceed with Permission">Proceed with Permission</option>
                            <option value="Provide user feedback">Provide user feedback</option>
                        </select>
                    </div>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 2fr; gap:15px; margin-bottom:15px;">
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Project Token (e.g. general, dbx)</label>
                        <input type="text" id="createProject" placeholder="general" value="general" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                    </div>
                    <div>
                        <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Title</label>
                        <input type="text" id="createTitle" placeholder="e.g. update configuration parser" style="width:100%; padding:10px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; border-radius:8px;">
                    </div>
                </div>
                <div style="margin-bottom:20px;">
                    <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Requirements / Markdown Content</label>
                    <textarea id="createContent" style="width:100%; height:200px; padding:15px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:#e2e8f0; font-family:monospace; border-radius:8px;" placeholder="# Task Summary\n...\n# Implementation Plan\n..."></textarea>
                </div>
                <div style="display:flex; justify-content:flex-end;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="submitCreate()"><i class="fas fa-save"></i> Save File explicitly to lane</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        let isEditMode = false;
        let editOriginalFolder = null;
        let editOriginalFilename = null;

        // ==================== WORKER EXCLUSION CONTROLS ====================
        async function toggleWorker(agent) {
            const toggle = document.getElementById(`worker-${agent}`);
            const isCurrentlyExcluded = toggle.classList.contains('excluded');
            const newExcludedState = !isCurrentlyExcluded;

            try {
                const response = await fetch('/api/workers/toggle', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ agent: agent, excluded: newExcludedState })
                });

                if (response.ok) {
                    const data = await response.json();
                    updateWorkerToggleUI(agent, newExcludedState);
                } else {
                    console.error('Failed to toggle worker:', response.statusText);
                }
            } catch (error) {
                console.error('Error toggling worker:', error);
            }
        }

        function updateWorkerToggleUI(agent, excluded) {
            const toggle = document.getElementById(`worker-${agent}`);
            if (toggle) {
                if (excluded) {
                    toggle.classList.remove('active');
                    toggle.classList.add('excluded');
                    toggle.title = `Click to re-enable ${agent.charAt(0).toUpperCase() + agent.slice(1)} worker`;
                } else {
                    toggle.classList.remove('excluded');
                    toggle.classList.add('active');
                    toggle.title = `Click to exclude ${agent.charAt(0).toUpperCase() + agent.slice(1)} worker`;
                }
            }
        }

        function updatePipelineFocusUI(data) {
            const statusEl = document.getElementById('pipelineFocusStatus');
            const selectEl = document.getElementById('focusEpicSelect');
            if (selectEl) {
                const options = Array.isArray(data.available_epics) ? data.available_epics : [];
                const currentValue = data.enabled && data.epic_family ? data.epic_family : (selectEl.value || '');
                const optionHtml = ['<option value="">Select epic...</option>']
                    .concat(options.map(name => `<option value="${name}">${name}</option>`));
                selectEl.innerHTML = optionHtml.join('');
                if (currentValue && options.includes(currentValue)) {
                    selectEl.value = currentValue;
                } else if (!data.enabled) {
                    selectEl.value = '';
                }
            }
            if (!statusEl) return;
            if (!data.enabled || !data.epic_family) {
                statusEl.textContent = 'Focus: All';
                statusEl.style.color = 'var(--text-dim)';
                return;
            }
            const remaining = data.remaining || {};
            const parked = data.parked || {};
            const activeCount = (remaining['000_epic'] || 0) + (remaining['050_review'] || 0) + (remaining['100_backlog'] || 0) + (remaining['200_inprogress'] || 0) + (remaining['400_failed'] || 0);
            const parkedCount = (parked['100_backlog'] || 0) + (parked['200_inprogress'] || 0);
            statusEl.textContent = `Focus: ${data.epic_family} | active ${activeCount} | parked ${parkedCount}`;
            statusEl.style.color = '#fbbf24';
        }

        async function fetchPipelineFocus() {
            try {
                const response = await fetch('/api/pipeline-focus');
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) updatePipelineFocusUI(data);
                }
            } catch (error) {
                console.error('Error fetching pipeline focus:', error);
            }
        }

        async function applyPipelineFocus() {
            const selectEl = document.getElementById('focusEpicSelect');
            const epicFamily = (selectEl?.value || '').trim();
            if (!epicFamily) {
                alert('Select an epic family to focus.');
                return;
            }
            try {
                const response = await fetch('/api/pipeline-focus', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ enabled: true, epic_family: epicFamily })
                });
                const data = await response.json();
                if (!data.success) {
                    alert(data.error || 'Failed to set pipeline focus.');
                    return;
                }
                updatePipelineFocusUI(data);
                fetchTasks();
            } catch (error) {
                console.error('Error setting pipeline focus:', error);
                alert('Failed to set pipeline focus.');
            }
        }

        async function clearPipelineFocus() {
            try {
                const response = await fetch('/api/pipeline-focus', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ enabled: false, epic_family: '' })
                });
                const data = await response.json();
                if (!data.success) {
                    alert(data.error || 'Failed to clear pipeline focus.');
                    return;
                }
                const selectEl = document.getElementById('focusEpicSelect');
                if (selectEl) selectEl.value = '';
                updatePipelineFocusUI(data);
                fetchTasks();
            } catch (error) {
                console.error('Error clearing pipeline focus:', error);
                alert('Failed to clear pipeline focus.');
            }
        }

        async function fetchWorkerStatus() {
            try {
                const response = await fetch('/api/workers/status');
                if (response.ok) {
                    const data = await response.json();
                    ['codex', 'gemini', 'claude'].forEach(agent => {
                        if (data.workers && data.workers[agent]) {
                            updateWorkerToggleUI(agent, data.workers[agent].excluded);
                        }
                    });
                }
            } catch (error) {
                console.error('Error fetching worker status:', error);
            }
        }

        // Fetch worker status on page load and periodically
        document.addEventListener('DOMContentLoaded', () => {
            fetchWorkerStatus();
            fetchPipelineFocus();
            setInterval(fetchWorkerStatus, 10000); // Refresh every 10 seconds
            setInterval(fetchPipelineFocus, 10000);
        });

        // ==================== DATE RANGE FILTER [V20260315] ====================
        const DATE_RANGE_STORAGE_KEY = 'kanban_date_range_preset';
        let currentDateRange = { start: null, end: null, preset: 'today' };

        function calculateDateRange(preset) {
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            let start = new Date(today);
            let end = new Date(today);

            switch (preset) {
                case 'today':
                    break;
                case 'yesterday':
                    start.setDate(start.getDate() - 1);
                    end.setDate(end.getDate() - 1);
                    break;
                case 'this_week':
                    const dayOfWeek = today.getDay();
                    const daysToMonday = dayOfWeek === 0 ? 6 : dayOfWeek - 1;
                    start.setDate(today.getDate() - daysToMonday);
                    break;
                case 'last_week':
                    const lastWeekDay = today.getDay();
                    const daysToLastMonday = lastWeekDay === 0 ? 13 : lastWeekDay + 6;
                    start.setDate(today.getDate() - daysToLastMonday);
                    end.setDate(start.getDate() + 6);
                    break;
                case 'this_month':
                    start.setDate(1);
                    break;
                case 'last_month':
                    start.setMonth(start.getMonth() - 1);
                    start.setDate(1);
                    end.setMonth(end.getMonth());
                    end.setDate(0);
                    break;
                case 'last_7':
                    start.setDate(today.getDate() - 6);
                    break;
                case 'last_30':
                    start.setDate(today.getDate() - 29);
                    break;
                case 'all':
                    return { start: null, end: null };
                case 'custom':
                    return null;
                default:
                    break;
            }

            return {
                start: start.toISOString().split('T')[0],
                end: end.toISOString().split('T')[0]
            };
        }

        function formatDateForDisplay(dateStr) {
            if (!dateStr) return '';
            const d = new Date(dateStr + 'T00:00:00');
            return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short' });
        }

        function updateDateRangeDisplay() {
            const display = document.getElementById('dateRangeDisplay');
            if (!display) return;

            if (!currentDateRange.start && !currentDateRange.end) {
                display.textContent = 'All dates';
            } else if (currentDateRange.start === currentDateRange.end) {
                display.textContent = formatDateForDisplay(currentDateRange.start);
            } else {
                display.textContent = formatDateForDisplay(currentDateRange.start) + ' - ' + formatDateForDisplay(currentDateRange.end);
            }

            // Update hidden kanbanDateFilter for backward compatibility
            const dateFilter = document.getElementById('kanbanDateFilter');
            if (dateFilter) {
                dateFilter.value = currentDateRange.end || '';
            }
        }

        function applyDatePreset() {
            const preset = document.getElementById('dateRangePreset').value;
            const customRangeDiv = document.getElementById('customDateRange');

            if (preset === 'custom') {
                customRangeDiv.style.display = 'flex';
                document.getElementById('startDate').value = currentDateRange.start || new Date().toISOString().split('T')[0];
                document.getElementById('endDate').value = currentDateRange.end || new Date().toISOString().split('T')[0];
                return;
            }

            customRangeDiv.style.display = 'none';
            const range = calculateDateRange(preset);
            if (range !== null) {
                currentDateRange = { ...range, preset };
                updateDateRangeDisplay();
                saveDateRangePreference();
                fetchTasks();
            }
        }

        function applyCustomDateRange() {
            const startDate = document.getElementById('startDate').value;
            const endDate = document.getElementById('endDate').value;

            if (!startDate || !endDate) {
                alert('Please select both start and end dates');
                return;
            }

            if (startDate > endDate) {
                alert('Start date must be before or equal to end date');
                return;
            }

            currentDateRange = { start: startDate, end: endDate, preset: 'custom' };
            updateDateRangeDisplay();
            saveDateRangePreference();
            fetchTasks();
        }

        function saveDateRangePreference() {
            try {
                localStorage.setItem(DATE_RANGE_STORAGE_KEY, JSON.stringify(currentDateRange));
            } catch (e) {
                console.warn('Could not save date range preference:', e);
            }
        }

        function loadDateRangePreference() {
            try {
                const saved = localStorage.getItem(DATE_RANGE_STORAGE_KEY);
                if (saved) {
                    const parsed = JSON.parse(saved);
                    const today = new Date().toISOString().split('T')[0];
                    // For presets that depend on "today", recalculate
                    if (parsed.preset && parsed.preset !== 'custom' && parsed.preset !== 'all') {
                        const range = calculateDateRange(parsed.preset);
                        if (range) {
                            currentDateRange = { ...range, preset: parsed.preset };
                            return true;
                        }
                    } else if (parsed.preset === 'all') {
                        currentDateRange = { start: null, end: null, preset: 'all' };
                        return true;
                    } else if (parsed.start && parsed.end) {
                        currentDateRange = parsed;
                        return true;
                    }
                }
            } catch (e) {
                console.warn('Could not load date range preference:', e);
            }
            return false;
        }

        function initializeDateRangeFilter() {
            const presetSelect = document.getElementById('dateRangePreset');
            if (!presetSelect) return;

            if (loadDateRangePreference()) {
                presetSelect.value = currentDateRange.preset || 'today';
                if (currentDateRange.preset === 'custom') {
                    document.getElementById('customDateRange').style.display = 'flex';
                    document.getElementById('startDate').value = currentDateRange.start;
                    document.getElementById('endDate').value = currentDateRange.end;
                }
            } else {
                currentDateRange = calculateDateRange('today');
                currentDateRange.preset = 'today';
            }

            updateDateRangeDisplay();
        }
        // ==================== END DATE RANGE FILTER ====================

        function openCreateModal() { 
            isEditMode = false;
            document.getElementById('createModalTitle').innerHTML = '<i class="fas fa-plus"></i> <span>Create New Entry</span>';
            document.getElementById('createTitle').value = '';
            document.getElementById('createContent').value = '';
            document.getElementById('createModal').style.display = 'flex'; 
        }
        function openEpicReview() {
            window.location.href = '/epic-review';
        }
        function openEpicDecomposition() {
            window.location.href = '/epic-decomposition';
        }
        function openEpicReconciliation() {
            window.location.href = '/epic-reconciliation';
        }
        function closeCreateModal(e) {
            if (e && e.target.id === 'createModal') document.getElementById('createModal').style.display = 'none';
            else if (!e) document.getElementById('createModal').style.display = 'none';
        }
        
        async function openEditModal() {
            if (!currentFileContext) return;
            isEditMode = true;
            editOriginalFolder = currentFileContext.folder;
            editOriginalFilename = currentFileContext.filename;
            
            const task = lastTasksData.find(t => t.folder === currentFileContext.folder && t.filename === currentFileContext.filename);
            if (!task) return;
            
            closeModal();
            
            document.getElementById('createTitle').value = task.title;
            document.getElementById('createProject').value = task.project;
            let typeVal = currentFileContext.folder.includes("backlog") ? "backlog" : "task";
            document.getElementById('createType').value = typeVal;
            document.getElementById('createPriority').value = task.priority || "2";
            
            let agentStr = ""; 
            if (currentFileContext.folder.includes("codex")) agentStr = "codex";
            else if (currentFileContext.folder.includes("gemini")) agentStr = "gemini";
            else if (currentFileContext.folder.includes("claude")) agentStr = "claude";
            else if (currentFileContext.folder.includes("general")) agentStr = "general";
            document.getElementById('createAgent').value = agentStr;
            
            let rawContent = document.getElementById('modalContentText').innerText;
            // Best effort cleanup of backend injected lines
            rawContent = rawContent.replace(/Priority:\\s*\\d+\\n+/, '');
            const compMatches = rawContent.match(/\\n+- `Completion Status`:.*$/i);
            if (compMatches) {
                rawContent = rawContent.replace(compMatches[0], '');
            }
            document.getElementById('createContent').value = rawContent.trim();
            
            document.getElementById('createModalTitle').innerHTML = '<i class="fas fa-edit"></i> <span>Edit Entry</span>';
            document.getElementById('createModal').style.display = 'flex';
        }

        async function submitCreate() {
            const payload = {
                type: document.getElementById('createType').value,
                agent: document.getElementById('createAgent').value,
                priority: document.getElementById('createPriority').value,
                completionAction: document.getElementById('createCompletionAction').value,
                project: document.getElementById('createProject').value.toLowerCase().replace(/[^a-z0-9_-]/g, ''),
                title: document.getElementById('createTitle').value.toLowerCase().replace(/[^a-z0-9_-]/g, '_'),
                content: document.getElementById('createContent').value,
                is_edit: isEditMode,
                original_folder: editOriginalFolder,
                original_filename: editOriginalFilename
            };
            if(!payload.project || !payload.title) { alert("Project and Title are required"); return; }
            try {
                const res = await fetch('/api/create-entry', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                if(res.ok) {
                    closeCreateModal();
                    document.getElementById('createTitle').value = '';
                    document.getElementById('createContent').value = '';
                    fetchTasks();
                } else {
                    alert("Failed to create file");
                }
            } catch(err) { console.error(err); }
        }

        let currentVerifyTask = null;

        function closeVerifyModal(e) {
            if (e && e.target.id === 'verifyModal') {
                document.getElementById('verifyModal').style.display = 'none';
            } else if (!e) {
                document.getElementById('verifyModal').style.display = 'none';
            }
        }

        function escapeHtml(unsafe) {
            if (!unsafe) return "";
            return unsafe
                 .replace(/&/g, "&amp;")
                 .replace(/</g, "&lt;")
                 .replace(/>/g, "&gt;")
                 .replace(/"/g, "&quot;")
                 .replace(/'/g, "&#039;");
        }

        function renderTaskReviewModal(task, mode) {
            const isVerifyMode = mode === 'verify';
            const coverageText = task.objective_delivery_coverage == null ? 'Not stated' : `${task.objective_delivery_coverage}%`;
            const coverageSummary = task.objective_delivery_coverage === 100
                ? (task.auto_acceptance === false ? 'Evidence claims full objective delivery, but manual acceptance is required.' : 'Evidence claims full objective delivery.')
                : 'Evidence requires reviewer judgement or is partial.';
            const verifyActions = isVerifyMode ? `
                <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="handleVerifyPass()"><i class="fas fa-check"></i> Pass & Complete</button>
                <button class="search-btn" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);" onclick="openVerifyFail()"><i class="fas fa-times"></i> Fail & Request Fix</button>
            ` : '';
            return `
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#6366f1; margin-bottom:8px;"><i class="fas fa-bullseye"></i> Task Summary</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">${escapeHtml(task.summary)}</div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#10b981; margin-bottom:8px;"><i class="fas fa-code-branch"></i> Changes Made</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.changes_made)}</pre></div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#f59e0b; margin-bottom:8px;"><i class="fas fa-flask"></i> Validation Steps</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.validation)}</pre></div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#38bdf8; margin-bottom:8px;"><i class="fas fa-shield-check"></i> Objective Delivery Coverage</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">
                        <strong>${coverageText}</strong>
                        <span style="color:#94a3b8; margin-left:8px;">${coverageSummary}</span>
                    </div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#a78bfa; margin-bottom:8px;"><i class="fas fa-bolt"></i> Auto Acceptance</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">
                        <strong>${task.auto_acceptance === false ? 'false' : 'true'}</strong>
                    </div>
                </div>
                <div style="display:flex; gap:10px; margin-top:20px; flex-wrap:wrap;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);" onclick="showTaskEvidence()"><i class="fas fa-eye"></i> Show Me</button>
                    ${verifyActions}
                </div>
                <div id="evidenceReviewBox" style="display:none; margin-top:20px;"></div>
                ${isVerifyMode ? `
                <div id="verifyFailBox" style="display:none; margin-top:20px;">
                    <textarea id="verifyFeedbackText" style="width:100%; height:100px; background:rgba(0,0,0,0.3); border:1px solid #ef4444; color:white; padding:10px; border-radius:8px;" placeholder="Describe exactly why validation failed so the agent can fix it..."></textarea>
                    <button class="search-btn" style="background:#ef4444; margin-top:10px;" onclick="handleVerifyFailSubmit()">Submit Failure</button>
                </div>
                ` : ''}
            `;
        }

        function openVerifyModal(e, folder, filename) {
            e.stopPropagation();
            const task = lastTasksData.find(t => t.folder === folder && t.filename === filename);
            if (!task) return;
            currentVerifyTask = task;
            
            document.getElementById('vModalTitle').innerText = `Verify: ${task.title}`;
            document.getElementById('vModalBody').innerHTML = renderTaskReviewModal(task, 'verify');
            document.getElementById('verifyModal').style.display = 'flex';
        }

        function openEvidenceModal(e, folder, filename) {
            e.stopPropagation();
            const task = lastTasksData.find(t => t.folder === folder && t.filename === filename);
            if (!task) return;
            currentVerifyTask = task;
            document.getElementById('vModalTitle').innerText = `Evidence: ${task.title}`;
            document.getElementById('vModalBody').innerHTML = renderTaskReviewModal(task, 'evidence');
            document.getElementById('verifyModal').style.display = 'flex';
            showTaskEvidence();
        }

        function openVerifyFail() {
            document.getElementById('verifyFailBox').style.display = 'block';
        }

        function renderEvidenceItems(task) {
            const evidenceItems = Array.isArray(task.evidence_items) ? task.evidence_items : [];
            if (!evidenceItems.length) {
                return `<div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px; color:#94a3b8;">No standardized evidence was parsed for this task.</div>`;
            }
            return evidenceItems.map((item, index) => {
                const artifact = item.artifact || 'not provided';
                const objective = item.objective_proved || 'not stated';
                const status = item.status || 'unknown';
                const type = item.type || 'unknown';
                const openButton = artifact && artifact.toLowerCase() !== 'not_applicable'
                    ? `<button class="search-btn" style="padding:6px 10px; font-size:0.85em;" onclick="openEvidenceArtifact(${index})"><i class="fas fa-arrow-up-right-from-square"></i> Open</button>`
                    : '';
                return `
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:10px; margin-bottom:10px;">
                        <div style="display:flex; justify-content:space-between; gap:12px; align-items:center; margin-bottom:8px; flex-wrap:wrap;">
                            <div>
                                <strong style="color:#e2e8f0;">${escapeHtml(type)}</strong>
                                <span style="color:#94a3b8; margin-left:8px;">Status: ${escapeHtml(status)}</span>
                            </div>
                            ${openButton}
                        </div>
                        <div style="color:#cbd5e1; margin-bottom:6px;"><strong>Artifact:</strong> ${escapeHtml(artifact)}</div>
                        <div style="color:#94a3b8;"><strong>Objective Proved:</strong> ${escapeHtml(objective)}</div>
                    </div>
                `;
            }).join('');
        }

        function showTaskEvidence() {
            if (!currentVerifyTask) return;
            const box = document.getElementById('evidenceReviewBox');
            if (!box) return;
            box.style.display = box.style.display === 'none' ? 'block' : 'none';
            if (box.style.display === 'block') {
                box.innerHTML = `
                    <div style="margin-bottom: 12px;">
                        <h3 style="color:#8b5cf6; margin-bottom:8px;"><i class="fas fa-folder-open"></i> Evidence Review</h3>
                        ${renderEvidenceItems(currentVerifyTask)}
                    </div>
                `;
            }
        }

        function openEvidenceArtifact(index) {
            if (!currentVerifyTask || !Array.isArray(currentVerifyTask.evidence_items)) return;
            const item = currentVerifyTask.evidence_items[index];
            if (!item) return;
            openArtifact(item.type, item.artifact);
        }

        function openArtifact(type, artifact) {
            const evidenceType = String(type || '').trim().toUpperCase();
            const rawArtifact = String(artifact || '').trim();
            if (!rawArtifact || rawArtifact.toLowerCase() === 'not_applicable') {
                alert('No openable artifact is recorded for this evidence item.');
                return;
            }
            if (rawArtifact.startsWith('http://') || rawArtifact.startsWith('https://')) {
                window.open(rawArtifact, '_blank');
                return;
            }
            if (!rawArtifact.startsWith('/') && !rawArtifact.includes(':\\\\') && !rawArtifact.includes(':/')) {
                if (evidenceType === 'DEMO' || evidenceType === 'URL') {
                    window.open('http://localhost:8080' + (rawArtifact.startsWith('/') ? '' : '/') + rawArtifact, '_blank');
                } else {
                    alert(rawArtifact);
                }
                return;
            }

            const cleanPath = rawArtifact.replace(/\\\\/g, '/');
            const mode = ['DIFF', 'CODE'].includes(evidenceType) ? 'code' : 'default';
            fetch('/api/open-file', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({path: cleanPath, mode})
            }).then(res => {
                if (!res.ok) {
                    alert('Could not open artifact. Path: ' + cleanPath);
                }
            }).catch(() => {
                alert('Artifact: ' + cleanPath);
            });
        }

        async function handleVerifyPass() {
            if(!currentVerifyTask) return;
            try {
                const res = await fetch('/api/verify-task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentVerifyTask.folder, filename: currentVerifyTask.filename, action: 'pass' })
                });
                if(res.ok) { closeVerifyModal(); fetchTasks(); }
            } catch(e) {}
        }

        async function handleVerifyFailSubmit() {
            if(!currentVerifyTask) return;
            const fb = document.getElementById('verifyFeedbackText').value;
            try {
                const res = await fetch('/api/verify-task', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentVerifyTask.folder, filename: currentVerifyTask.filename, action: 'fail', feedback: fb })
                });
                if(res.ok) { closeVerifyModal(); fetchTasks(); }
            } catch(e) {}
        }
        
        let currentFeedbackTask = null;
        function closeFeedbackModal(e) {
            if (e && e.target.id === 'feedbackModal') document.getElementById('feedbackModal').style.display = 'none';
            else if (!e) document.getElementById('feedbackModal').style.display = 'none';
        }

        function openFeedbackModal(e, folder, filename) {
            e.stopPropagation();
            const task = lastTasksData.find(t => t.folder === folder && t.filename === filename);
            if (!task) return;
            currentFeedbackTask = task;
            
            document.getElementById('fbModalTitle').innerText = `Feedback: ${task.title}`;
            let html = `
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#6366f1; margin-bottom:8px;"><i class="fas fa-bullseye"></i> Task Summary</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;">${escapeHtml(task.summary)}</div>
                </div>
                <div style="margin-bottom: 20px;">
                    <h3 style="color:#10b981; margin-bottom:8px;"><i class="fas fa-code-branch"></i> Changes Made</h3>
                    <div style="background:rgba(255,255,255,0.05); padding:12px; border-radius:8px;"><pre style="background:transparent; padding:0; margin:0;">${escapeHtml(task.changes_made)}</pre></div>
                </div>
                
                <div style="margin-top:20px;">
                    <label style="color:#a855f7; font-size:0.85em; font-weight:700; display:block; margin-bottom:5px;">Specific Feedback On Outcomes / Findings:</label>
                    <textarea id="userFeedbackText" style="width:100%; height:120px; background:rgba(0,0,0,0.3); border:1px solid #0ea5e9; color:white; padding:10px; border-radius:8px;" placeholder="Provide explicit feedback or findings to append to this task..."></textarea>
                </div>
                
                <div style="display:flex; gap:10px; margin-top:20px;">
                    <button class="search-btn" style="background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);" onclick="handleFeedbackSubmit()"><i class="fas fa-paper-plane"></i> Submit & Complete Task</button>
                    <button class="search-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);" onclick="handleFeedbackReturn()"><i class="fas fa-undo"></i> Submit & Return to ToDo</button>
                </div>
            `;
            document.getElementById('fbModalBody').innerHTML = html;
            document.getElementById('feedbackModal').style.display = 'flex';
        }

        async function postFeedback(action) {
            if(!currentFeedbackTask) return;
            const fb = document.getElementById('userFeedbackText').value;
            if(!fb) { alert('Please provide specific feedback before submitting.'); return; }
            try {
                const res = await fetch('/api/submit-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ folder: currentFeedbackTask.folder, filename: currentFeedbackTask.filename, action: action, feedback: fb })
                });
                if(res.ok) { closeFeedbackModal(); fetchTasks(); }
            } catch(e) {}
        }
        function handleFeedbackSubmit() { postFeedback('complete'); }
        function handleFeedbackReturn() { postFeedback('todo'); }

        function getProjectColor(project) {
            let hash = 0;
            for (let i = 0; i < project.length; i++) {
                hash = project.charCodeAt(i) + ((hash << 5) - hash);
            }
            const h = Math.abs(hash) % 360;
            // Generate distinct vibrant colors
            return `hsl(${h}, 70%, 65%)`; 
        }

        function getTaskKey(task) {
            return `${task.project || 'general'}::${task.filename}`;
        }

        function getTaskStatusBucket(folder) {
            if (folder.includes("000_epic")) return "000_epic";
            if (folder.includes("review")) return "050_review";
            if (folder.includes("100_backlog") || folder.includes("todo")) return "100_backlog";
            if (folder.includes("200_inprogress") || folder.includes("inprogress")) return "200_inprogress";
            if (folder.includes("300_complete") || folder.includes("complete")) return "300_complete";
            if (folder.includes("400_failed") || folder.includes("failed")) return "400_failed";
            return folder;
        }

        let taskStatusMemory = new Map();
        let taskHighlightState = new Map();

        function syncTaskHighlightState(tasks) {
            const now = Date.now();
            const nextStatusMemory = new Map();
            const currentKeys = new Set();

            tasks.forEach(task => {
                const key = getTaskKey(task);
                const status = getTaskStatusBucket(task.folder);
                const previousStatus = taskStatusMemory.get(key);
                currentKeys.add(key);
                nextStatusMemory.set(key, status);

                if (status === "400_failed") {
                    taskHighlightState.set(key, { kind: "failed" });
                } else {
                    const existing = taskHighlightState.get(key);
                    if (existing && existing.kind === "failed") {
                        taskHighlightState.delete(key);
                    }
                }

                if (previousStatus && previousStatus !== status) {
                    if (status === "400_failed") {
                        taskHighlightState.set(key, { kind: "failed" });
                    } else if (status === "300_complete") {
                        taskHighlightState.set(key, { kind: "complete", startedAt: now, duration: 3000 });
                    } else {
                        taskHighlightState.set(key, { kind: "status", startedAt: now, duration: 2000 });
                    }
                }
            });

            for (const [key, effect] of [...taskHighlightState.entries()]) {
                if (!currentKeys.has(key)) {
                    taskHighlightState.delete(key);
                    continue;
                }
                if (effect.kind !== "failed" && now - effect.startedAt >= effect.duration) {
                    taskHighlightState.delete(key);
                }
            }

            taskStatusMemory = nextStatusMemory;
        }

        function createCardHtml(task) {
            const color = getProjectColor(task.project);
            let timeStr = task.timestamp;
            if(timeStr.length === 15) { // format yyyymmdd_hhmmss
                timeStr = `${timeStr.slice(0,4)}-${timeStr.slice(4,6)}-${timeStr.slice(6,8)} ${timeStr.slice(9,11)}:${timeStr.slice(11,13)}`;
            }
            const cardKey = getTaskKey(task);
            const highlightEffect = taskHighlightState.get(cardKey);
            const cardClasses = ["task-card"];
            const cardStyleParts = [`border-left-color: ${color}`];

            if (highlightEffect) {
                if (highlightEffect.kind === "failed") {
                    cardClasses.push("failed-perimeter-highlight");
                } else if (highlightEffect.kind === "complete" || highlightEffect.kind === "status") {
                    const elapsed = Math.max(0, Date.now() - highlightEffect.startedAt);
                    const cappedElapsed = Math.min(elapsed, highlightEffect.duration);
                    cardClasses.push(highlightEffect.kind === "complete" ? "complete-transition-flash" : "status-transition-flash");
                    cardStyleParts.push(`animation-delay: -${cappedElapsed}ms`);
                }
            }

            let progressHtml = '';
            if (task.progress !== null && task.progress !== undefined) {
                let p = Math.max(0, Math.min(100, task.progress));
                progressHtml = `
                    <div style="margin-top: 12px; margin-bottom: 4px; display: flex; align-items: center; justify-content: space-between; font-size: 0.75em; color: var(--text-dim); font-weight: 600;">
                        <span>PROGRESS</span>
                        <span>${p}%</span>
                    </div>
                    <div style="margin-bottom: 12px; height: 6px; background: rgba(0,0,0,0.3); border-radius: 4px; overflow: hidden; position: relative;">
                        <div style="width: ${p}%; height: 100%; background: linear-gradient(90deg, #6366f1, #a855f7); border-radius: 4px; transition: width 0.3s ease; box-shadow: 0 0 10px rgba(99, 102, 241, 0.4);"></div>
                    </div>
                `;
            }

            let verifyBadge = '';
            const hasEvidence = (Array.isArray(task.evidence_items) && task.evidence_items.length > 0) || !!task.deliverable_url;
            if (task.needs_feedback && task.folder.includes("200_inprogress")) {
                verifyBadge += `<button onclick="openFeedbackModal(event, '${task.folder}', '${task.filename}')" style="background:#0ea5e9; color:#fff; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right; margin-right:5px;">💬 FEEDBACK</button>`;
            }
            if (task.needs_verification && task.folder.includes("200_inprogress")) {
                verifyBadge += `<button onclick="openVerifyModal(event, '${task.folder}', '${task.filename}')" style="background:#f59e0b; color:#111; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right;">🔍 VERIFY</button>`;
            }
            if (hasEvidence) {
                verifyBadge += `<button onclick="openEvidenceModal(event, '${task.folder}', '${task.filename}')" style="background:#8b5cf6; color:#fff; border:none; padding:4px 8px; border-radius:4px; font-weight:800; cursor:pointer; font-size:0.8em; z-index:10; float:right; margin-right:5px;">👁 SHOW ME</button>`;
            }
            
            let priorityBadge = '';
            if (task.priority) {
                if (task.priority === 1) priorityBadge = `<span style="background:rgba(239, 68, 68, 0.2); color:#ef4444; border:1px solid #ef4444; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:800;">⚡ P1</span>`;
                else if (task.priority === 2) priorityBadge = `<span style="background:rgba(99, 102, 241, 0.2); color:#a855f7; border:1px solid #8b5cf6; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:800;">⚙️ P2</span>`;
                else if (task.priority === 3) priorityBadge = `<span style="background:rgba(255, 255, 255, 0.1); color:#94a3b8; border:1px solid #475569; padding:2px 6px; border-radius:4px; font-size:0.7em; margin-right:5px; font-weight:600;">💤 P3</span>`;
            }

            // [2026-03-17 V20260317_1730] Special Delivered View Styling
            if (task.isDeliveredView) {
                const isComplete = task.folder.includes("300_complete");
                const deliveryColor = isComplete ? "#10b981" : "#ef4444";
                cardStyleParts.push(`background: ${deliveryColor}10`);
                cardStyleParts.push(`border: 1px solid ${deliveryColor}40`);
                cardStyleParts.push(`border-left: 4px solid ${deliveryColor}`);
            }

            const isDelivered = !!task.isDeliveredView;
            const dragStart = isDelivered ? "" : `ondragstart="handleDragStart(event, '${task.folder}', '${task.filename}')"`;

            return `
                <div class="${cardClasses.join(' ')}" draggable="${!isDelivered}" ${dragStart} style="${cardStyleParts.join('; ')}" onclick="openFile('${task.folder}', '${task.filename}')">
                    ${verifyBadge}
                    <div class="project-badge" style="background: ${color}20; color: ${color}; border: 1px solid ${color}40;">
                        ${task.project}
                    </div>
                    <div class="task-title">${priorityBadge}${task.title}</div>
                    <div class="task-summary">${task.summary}</div>
                    ${progressHtml}
                    <div class="task-footer">
                        <span><i class="far fa-folder" style="color:#6366f1"></i> ${task.folder.replace('_', ' ')}</span>
                        <span class="task-date"><i class="far fa-clock"></i> ${timeStr}</span>
                    </div>
                </div>
            `;
        }

        let currentFileContext = null;

        function closeModal(e) {
            if (e && e.target.id === 'contentModal') {
                document.getElementById('contentModal').style.display = 'none';
            } else if (!e) {
                document.getElementById('contentModal').style.display = 'none';
            }
        }

        async function openAndCloseLocal() {
            if (!currentFileContext) return;
            try {
                await fetch('/api/open-file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentFileContext)
                });
            } catch(err) {}
        }

        async function openAndCloseLocalReview(folder, filename) {
            try {
                await fetch('/api/open-file', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ folder, filename })
                });
            } catch(err) {}
        }

        async function openFile(folder, filename) {
            currentFileContext = { folder, filename };
            document.getElementById('modalTitle').innerText = filename;
            document.getElementById('modalContentText').innerText = "Loading document contents...";
            document.getElementById('contentModal').style.display = 'flex';
            
            const delBtn = document.getElementById('deleteBtnModal');
            const editBtn = document.getElementById('editBtnModal');
            const dumpBtn = document.getElementById('dumpBtnModal');
            if (folder === '000_epic/general' || folder === '000_epic' || folder.includes('100_backlog') || folder.includes('200_inprogress')) {
                delBtn.style.display = (folder === '000_epic/general' || folder === '000_epic') ? 'flex' : 'none';
                editBtn.style.display = (folder.includes('100_backlog') || folder.includes('200_inprogress') || folder.includes('backlog')) ? 'flex' : 'none';
            } else {
                delBtn.style.display = 'none';
                editBtn.style.display = 'none';
            }
            // Show Dump button for all folders except 300_complete and 500_dump
            dumpBtn.style.display = (folder.includes('300_complete') || folder.includes('500_dump')) ? 'none' : 'flex';
            
            try {
                const res = await fetch(`/api/file-content?folder=${encodeURIComponent(folder)}&filename=${encodeURIComponent(filename)}`);
                const data = await res.json();
                if (data.success) {
                    document.getElementById('modalContentText').innerText = data.content;
                } else {
                    document.getElementById('modalContentText').innerText = "❌ Error: " + data.error;
                }
            } catch (err) {
                console.error("Failed to fetch file content", err);
                document.getElementById('modalContentText').innerText = "❌ Failed to load content completely. See console for details.";
            }
        }

        async function deleteCurrentFile() {
            if (!currentFileContext) return;
            const sf = currentFileContext.folder;
            if (sf !== '000_epic/general' && sf !== '000_epic') {
                alert("Only items in general backlog can be directly deleted.");
                return;
            }
            if (!confirm(`Are you sure you want to permanently delete:\\n\\n${currentFileContext.filename}\\n\\nThis action cannot be undone.`)) {
                return;
            }
            
            try {
                const res = await fetch('/api/delete-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentFileContext)
                });
                const data = await res.json();
                if (data.success) {
                    closeModal();
                    fetchTasks();
                } else {
                    alert("Error deleting:\\n" + data.error);
                }
            } catch(err) {
                console.error("Delete failed", err);
                alert("Network error processing deletion.");
            }
        }

        async function dumpCurrentFile() {
            if (!currentFileContext) return;
            const sf = currentFileContext.folder;
            // Don't allow dumping from 300_complete or 500_dump
            if (sf.includes('300_complete') || sf.includes('500_dump')) {
                alert("Cannot dump tasks from Complete or Dump folders.");
                return;
            }
            if (!confirm(`Move this task to DUMP folder?\\n\\n${currentFileContext.filename}\\n\\nThe task will be archived but not deleted.`)) {
                return;
            }

            try {
                const res = await fetch('/api/dump-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(currentFileContext)
                });
                const data = await res.json();
                if (data.success) {
                    closeModal();
                    fetchTasks();
                } else {
                    alert("Error dumping task:\\n" + data.error);
                }
            } catch(err) {
                console.error("Dump failed", err);
                alert("Network error processing dump.");
            }
        }

        let lastTasksData = [];
        let expandedGroups = {};
        let expandAllForce = false;
        let expandedGroupsEpic = {};
        let expandAllForceEpic = false;
        let expandedGroupsBacklog = {};
        let expandAllForceBacklog = false;
        let expandedGroupsInprogress = {};
        let expandAllForceInprogress = false;
        let expandedGroupsFailed = {};
        let expandAllForceFailed = false;
        let expandedGroupsDelivered = {};
        let expandAllForceDelivered = false;

        // Drag and Drop State        let dragSrcFolder = null;
        let dragFilename = null;

        function handleDragStart(e, folder, filename) {
            dragSrcFolder = folder;
            dragFilename = filename;
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', filename);
            e.stopPropagation();
        }

        function handleDragOver(e) {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
        }

        async function handleDrop(e, targetFolder) {
            e.preventDefault();
            e.stopPropagation();
            if(!dragFilename || !dragSrcFolder) return;
            
            // Allow drop to different column conceptually
            if(dragSrcFolder === targetFolder) return;
            
            try {
                await fetch('/api/move-task', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        source_folder: dragSrcFolder,
                        target_folder: targetFolder,
                        filename: dragFilename
                    })
                });
                fetchTasks(); // Force immediate re-render
            } catch(err) {
                 console.error("Failed to execute move-task", err);
            }
            dragFilename = null;
            dragSrcFolder = null;
        }

        function toggleGroup(proj, e) {
            if(e) e.stopPropagation();
            expandedGroups[proj] = !expandedGroups[proj];
            renderBoard(lastTasksData);
        }

        function toggleGroupEpic(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsEpic[proj] = !expandedGroupsEpic[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllComplete() {
            expandAllForce = !expandAllForce;
            const btn = document.getElementById('toggleAllBtn');
            if(expandAllForce) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroups = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleAllEpic() {
            expandAllForceEpic = !expandAllForceEpic;
            const btn = document.getElementById('toggleAllEpicBtn');
            if(expandAllForceEpic) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsEpic = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupBacklog(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsBacklog[proj] = !expandedGroupsBacklog[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllBacklog() {
            expandAllForceBacklog = !expandAllForceBacklog;
            const btn = document.getElementById('toggleAllBacklogBtn');
            if(expandAllForceBacklog) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsBacklog = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupInprogress(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsInprogress[proj] = !expandedGroupsInprogress[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllInprogress() {
            expandAllForceInprogress = !expandAllForceInprogress;
            const btn = document.getElementById('toggleAllInprogressBtn');
            if(expandAllForceInprogress) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsInprogress = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupFailed(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsFailed[proj] = !expandedGroupsFailed[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllFailed() {
            expandAllForceFailed = !expandAllForceFailed;
            const btn = document.getElementById('toggleAllFailedBtn');
            if(expandAllForceFailed) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsFailed = {};
            }
            renderBoard(lastTasksData);
        }

        function toggleGroupDelivered(proj, e) {
            if(e) e.stopPropagation();
            expandedGroupsDelivered[proj] = !expandedGroupsDelivered[proj];
            renderBoard(lastTasksData);
        }

        function toggleAllDelivered() {
            expandAllForceDelivered = !expandAllForceDelivered;
            const btn = document.getElementById('toggleAllDeliveredBtn');
            if(expandAllForceDelivered) {
                btn.innerText = "Collapse All";
            } else {
                btn.innerText = "Expand All";
                expandedGroupsDelivered = {};
            }
            renderBoard(lastTasksData);
        }

        let currentlyReviewing = null;
        async function checkReviewTasks() {
            const reviews = lastTasksData.filter(t => t.folder.startsWith('050_review'));
            if (reviews.length > 0 && !currentlyReviewing) {
                // Group by agent/backlog core
                const agent = reviews[0].folder.split('/')[1] || 'general';
                // Extract core name
                let coreName = "Unknown Backlog";
                const match = reviews[0].filename.match(/from_(.+)\\.md$/);
                if(match) coreName = match[1];

                currentlyReviewing = { agent, coreName, tasks: reviews };
                
                document.getElementById('modalTitle').innerHTML = `Awaiting Approval: <span>${coreName}</span>`;
                let taskListStr = reviews.map(t => `
                    <div style="background:rgba(255,255,255,0.05); padding:10px; margin-bottom:8px; border-radius:8px; border-left:3px solid #6366f1;">
                        <div style="display:flex; align-items:center; justify-content:space-between; gap:10px;">
                            <div style="word-break:break-word; color:#e2e8f0;">${t.filename}</div>
                            <div style="display:flex; gap:8px; flex-shrink:0;">
                                <button class="search-btn" style="padding:6px 10px; font-size:0.8em;" onclick="openFile('${t.folder}', '${t.filename}')" title="Preview file contents in-app"><i class="fas fa-eye"></i> Preview</button>
                                <button class="search-btn" style="padding:6px 10px; font-size:0.8em; background: rgba(99,102,241,0.2);" onclick="openAndCloseLocalReview('${t.folder}', '${t.filename}')" title="Open file externally"><i class="fas fa-external-link-alt"></i> External</button>
                            </div>
                        </div>
                    </div>
                `).join('');
                document.getElementById('modalContentText').innerHTML = `
                    <div style="margin-bottom:15px; font-size:1.1em; color:#cbd5e1;">The <b>${agent.toUpperCase()}</b> agent has generated the following draft tasks:</div>
                    ${taskListStr}
                    <div style="margin-top:20px; display:flex; gap:10px;">
                        <button class="search-btn" style="background: linear-gradient(135deg, #10b981 0%, #059669 100%);" onclick="handleReviewApprove()"><i class="fas fa-check"></i> Approve & Proceed</button>
                        <button class="search-btn" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);" onclick="handleReviewModify()"><i class="fas fa-edit"></i> Request Changes</button>
                        <button class="search-btn" style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);" onclick="handleReviewReject()"><i class="fas fa-ban"></i> Reject & Suspend</button>
                    </div>
                    <div id="reviewFeedbackBox" style="display:none; margin-top:15px;">
                        <textarea id="reviewFeedbackText" style="width:100%; height:80px; background:rgba(0,0,0,0.3); border:1px solid #6366f1; color:white; padding:10px; border-radius:8px;" placeholder="Describe what changes or additions are needed..."></textarea>
                        <button class="search-btn" style="margin-top:10px; padding:8px 16px; font-size:0.9em;" onclick="submitReviewModify()">Submit Feedback</button>
                    </div>
                `;
                
                document.getElementById('contentModal').style.display = 'flex';
                document.getElementById('deleteBtnModal').style.display = 'none';
            } else if (reviews.length === 0 && currentlyReviewing) {
                currentlyReviewing = null;
                closeModal();
            }
        }

        async function handleReviewApprove() {
            if(!currentlyReviewing) return;
            const res = await fetch('/api/review-approve', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(currentlyReviewing) });
            if(res.ok) fetchTasks();
        }
        function handleReviewModify() {
            document.getElementById('reviewFeedbackBox').style.display = 'block';
        }
        async function submitReviewModify() {
            if(!currentlyReviewing) return;
            const fb = document.getElementById('reviewFeedbackText').value;
            const res = await fetch('/api/review-modify', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({ ...currentlyReviewing, feedback: fb }) });
            if(res.ok) { currentlyReviewing = null; closeModal(); fetchTasks(); }
        }
        async function handleReviewReject() {
            if(!currentlyReviewing) return;
            if(!confirm("Are you sure you want to discard these drafts and suspend the backlog?")) return;
            const res = await fetch('/api/review-reject', { method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(currentlyReviewing) });
            if(res.ok) fetchTasks();
        }

        function renderBoard(tasks) {
            syncTaskHighlightState(tasks);
            const groups = {
                "000_epic": [], "050_review": [], "100_backlog": [], "200_inprogress": [], "300_complete": [], "delivered_epic": [], "400_failed": []
            };

            const agentList = [
                { name: "🤖 Codex", handle: "codex" },
                { name: "✨ Gemini", handle: "gemini" },
                { name: "🧠 Claude", handle: "claude" },
                { name: "📋 General", handle: "general" },
                { name: "📁 Root", handle: "" }
            ];

            ["000_epic", "050_review", "100_backlog", "200_inprogress", "300_complete", "400_failed"].forEach(col => {
                const agents = agentList.map(a => ({
                    kanbanGroup: a.name,
                    dropFolder: a.handle ? `${col}/${a.handle}` : col,
                    timestamp: "99999999_999999",
                    isDummy: true,
                    folder: a.handle ? `${col}/${a.handle}` : col
                }));
                groups[col].push(...agents);
            });

            // [2026-03-17 V20260317_1945] Identify originated epics from leftmost column
            const validEpicFilenames = new Set(tasks.filter(t => t.folder.includes("000_epic")).map(t => t.filename));

            // [2026-03-17 V20260317_2015] Helper to strip timestamp and extension for display
            const _cleanEpicName = (name) => {
                if (!name || name === "Others") return name;
                return name.replace(/^\d{8}_\d{6}_/, "").replace(/\.md$/, "").replace(/_/g, " ").toUpperCase();
            };

            tasks.forEach(t => {
                let col = t.folder;
                if (col.includes("000_epic")) col = "000_epic";
                else if (col.includes("review")) col = "050_review";
                else if (col.includes("100_backlog") || col.includes("todo")) col = "100_backlog";
                else if (col.includes("200_inprogress") || col.includes("inprogress")) col = "200_inprogress";
                else if (col.includes("300_complete") || col.includes("complete")) col = "300_complete";
                else if (col.includes("400_failed") || col.includes("failed")) col = "400_failed";

                if (groups[col]) {
                    if (["000_epic", "050_review", "100_backlog", "200_inprogress", "300_complete", "400_failed"].includes(col)) {
                        if (t.folder.endsWith("codex")) { t.kanbanGroup = "🤖 Codex"; t.dropFolder = `${col}/codex`; }
                        else if (t.folder.endsWith("gemini")) { t.kanbanGroup = "✨ Gemini"; t.dropFolder = `${col}/gemini`; }
                        else if (t.folder.endsWith("claude")) { t.kanbanGroup = "🧠 Claude"; t.dropFolder = `${col}/claude`; }
                        else if (t.folder.endsWith("general")) { t.kanbanGroup = "📋 General"; t.dropFolder = `${col}/general`; }
                        else { t.kanbanGroup = "📁 Root"; t.dropFolder = col; }
                    } else {
                        t.kanbanGroup = t.project;
                        t.dropFolder = col;
                    }
                    groups[col].push(t);
                }

                // [2026-03-17 V20260317_2015] Populate Delivered Column with clean names
                if (!t.folder.includes("000_epic")) {
                    const dt = JSON.parse(JSON.stringify(t));
                    const sourceEpicFile = (t.source_epic || "").endsWith(".md") ? t.source_epic : (t.source_epic ? t.source_epic + ".md" : "");
                    const isKnownEpic = sourceEpicFile && validEpicFilenames.has(sourceEpicFile);
                    dt.kanbanGroup = isKnownEpic ? _cleanEpicName(t.source_epic) : "Others";
                    dt.isDeliveredView = true;
                    groups["delivered_epic"].push(dt);
                }
            });
            for (const folder in groups) {
                // Filter out the dummy tasks when taking real column counts
                const realTasks = groups[folder].filter(t => !t.isDummy);
                const sortedTasks = realTasks.sort((a,b) => b.timestamp.localeCompare(a.timestamp));
                document.getElementById(`count-${folder}`).innerText = realTasks.length;
                
                if (["300_complete", "delivered_epic", "000_epic", "050_review", "100_backlog", "200_inprogress", "400_failed"].includes(folder)) {
                     const groupedByProject = {};
                     groups[folder].forEach(t => {
                         if(!groupedByProject[t.kanbanGroup]) groupedByProject[t.kanbanGroup] = [];
                         groupedByProject[t.kanbanGroup].push(t);
                     });

                     // Ensure the projects themselves are ordered by the newest timestamp in their group
                     const sortedProjects = Object.keys(groupedByProject).sort((a,b) => {
                         const timeA = groupedByProject[a][0] ? groupedByProject[a][0].timestamp : "";
                         const timeB = groupedByProject[b][0] ? groupedByProject[b][0].timestamp : "";
                         return timeB.localeCompare(timeA);
                     });

                     let groupHtml = '';
                     for (const proj of sortedProjects) {
                         const projColor = getProjectColor(proj);

                         // Explicitly sort the tasks inside the group descending by timestamp
                         groupedByProject[proj].sort((a,b) => b.timestamp.localeCompare(a.timestamp));
                         // Filter out the dummy task during loop rendering
                         const realCards = groupedByProject[proj].filter(t => !t.isDummy);
                         const projCount = realCards.length;

                         let isExpanded = false;
                         let toggleFunc = '';

                         if (folder === "300_complete") {
                             isExpanded = expandAllForce ? true : !!expandedGroups[proj];
                             toggleFunc = `toggleGroup('${proj}', event)`;
                         } else if (folder === "delivered_epic") {
                             isExpanded = expandAllForceDelivered ? true : !!expandedGroupsDelivered[proj];
                             toggleFunc = `toggleGroupDelivered('${proj}', event)`;
                         } else if (folder === "000_epic") {                             isExpanded = expandAllForceEpic ? true : !!expandedGroupsEpic[proj];
                             toggleFunc = `toggleGroupEpic('${proj}', event)`;
                         } else if (folder === "050_review") {
                             isExpanded = true;
                             toggleFunc = '';
                         } else if (folder === "100_backlog") {
                             isExpanded = expandAllForceBacklog ? true : !!expandedGroupsBacklog[proj];
                             toggleFunc = `toggleGroupBacklog('${proj}', event)`;
                         } else if (folder === "200_inprogress") {
                             isExpanded = expandAllForceInprogress ? true : !!expandedGroupsInprogress[proj];
                             toggleFunc = `toggleGroupInprogress('${proj}', event)`;
                         } else if (folder === "400_failed") {
                             isExpanded = expandAllForceFailed ? true : !!expandedGroupsFailed[proj];
                             toggleFunc = `toggleGroupFailed('${proj}', event)`;
                         }
                         
                         const icon = isExpanded ? 'fa-minus' : 'fa-plus';

                         const dropTarget = groupedByProject[proj][0].dropFolder || folder;
                         const isDelivered = folder === "delivered_epic";
                         const dragEvents = isDelivered ? "" : `ondragover="handleDragOver(event)" ondrop="handleDrop(event, '${dropTarget}')"`;

                         groupHtml += `
                            <div class="project-group" ${dragEvents} style="margin-bottom: 12px; border: 1px solid var(--glass-border); border-radius: 12px; overflow: hidden; background: var(--bg-accent);">                                <div class="group-header" onclick="${toggleFunc}" style="padding: 12px 16px; background: rgba(255,255,255,0.02); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border-left: 4px solid ${projColor};">
                                    <div style="font-weight: 600; color: #cbd5e1; display:flex; align-items:center;"><i class="fas ${icon}" style="margin-right: 8px; color: ${projColor}; width: 14px;"></i> ${proj} <span style="font-size: 0.8em; opacity: 0.6; margin-left: 8px;">(${projCount})</span></div>
                                </div>
                                <div class="group-content" style="display: ${isExpanded ? 'flex' : 'none'}; flex-direction: column; gap: 12px; padding: 12px; background: rgba(0,0,0,0.2);">
                                    ${realCards.map(createCardHtml).join('')}
                                </div>
                            </div>
                         `;
                     }
                     document.getElementById(`list-${folder}`).innerHTML = groupHtml;
                } else {
                    document.getElementById(`list-${folder}`).innerHTML = sortedTasks.map(createCardHtml).join('');
                }
            }
            updateTicker(tasks);
            document.getElementById('last-updated').innerText = "Last update: " + new Date().toLocaleTimeString();
        }

        function updateTicker(tasks) {
             const tickerDiv = document.getElementById('newsTicker');
             if (!tasks || tasks.length === 0) {
                 tickerDiv.innerHTML = '<span class="ticker-item"><span class="ticker-agent">SYSTEM</span> <span class="ticker-state" style="color:#6366f1; margin:0 5px; font-weight:600;">IDLE</span> <span class="ticker-task">No active tasks found in the pipeline.</span></span>';
                 return;
             }

             // Sort all tasks by latest timestamp first for ticker relevance
             const sortedAll = [...tasks].filter(t => !["000_epic", "050_review", "100_backlog", "200_inprogress", "300_complete", "400_failed"].includes(t.folder)).sort((a,b) => b.timestamp.localeCompare(a.timestamp));
             
             let tickerItems = [];
             for (const t of sortedAll) {
                 let agent = (t.folder.split('/')[1] || "general").toLowerCase();
                 let state = "Unknown";
                 if (t.folder.includes("backlog")) state = "Decomposition";
                 else if (t.folder.includes("review")) state = "Review";
                 else if (t.folder.includes("todo")) state = "To Do";
                 else if (t.folder.includes("inprogress")) state = "In Progress";
                 else if (t.folder.includes("complete")) state = "Complete";
                 else if (t.folder.includes("failed")) state = "Failed/Blocked";
                 
                 let itemStr = `<span class="ticker-item"><span class="ticker-agent" style="color:#a855f7; font-weight:800; text-transform:uppercase;">${agent}</span> - <span class="ticker-state" style="color:#6366f1; font-weight:600; text-transform:uppercase; margin:0 5px;">${state}</span> <span class="ticker-task">${t.title}</span></span>`;
                 tickerItems.push(itemStr);
                 
                 // Limit ticker to latest ~30 tasks across the board so the loop completes reasonably quickly
                 if(tickerItems.length >= 30) break;
             }
             
             if(tickerItems.length > 0) {
                 tickerDiv.innerHTML = tickerItems.join('<span class="ticker-separator" style="color:#f43f5e; margin:0 15px; font-weight:800; display:inline-block;">|</span>');
             }
         }

        let isSearching = false;
        let searchExpandedGroups = {};

        function toggleSearchGroup(dateKey) {
            searchExpandedGroups[dateKey] = !searchExpandedGroups[dateKey];
            const content = document.getElementById(`search-group-content-${dateKey}`);
            const icon = document.getElementById(`search-group-icon-${dateKey}`);
            if (searchExpandedGroups[dateKey]) {
                content.style.display = 'block';
                icon.textContent = '−';
            } else {
                content.style.display = 'none';
                icon.textContent = '+';
            }
        }

        async function performSearch() {
            const q = document.getElementById('searchInput').value.trim();
            if (!q) {
                clearSearch();
                return;
            }

            isSearching = true;
            searchExpandedGroups = {}; // Reset expanded state on new search
            document.getElementById('mainBoard').style.display = 'none';
            document.getElementById('searchResults').style.display = 'block';
            document.getElementById('clearSearchBtn').style.display = 'inline-block';
            document.getElementById('searchResultsList').innerHTML = '<div style="text-align:center; padding:30px;"><i class="fas fa-spinner fa-spin fa-2x"></i><p style="margin-top:10px;">Searching...</p></div>';

            try {
                const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`);
                const data = await res.json();

                if (data.success) {
                    document.getElementById('searchCount').innerText = data.results.length;
                    if (data.results.length === 0) {
                        document.getElementById('searchResultsList').innerHTML = '<div style="text-align:center; padding:30px; color: var(--text-dim);"><i class="fas fa-box-open fa-2x"></i><p style="margin-top:10px;">No matching tasks found.</p></div>';
                    } else {
                        // Group results by date (YYYY-MM-DD)
                        const groupedByDate = {};
                        data.results.forEach(r => {
                            // Extract date part (YYYY-MM-DD) from the date string
                            let dateKey = 'Unknown';
                            if (r.date && r.date !== 'Unknown') {
                                dateKey = r.date.split(' ')[0]; // Get YYYY-MM-DD part
                            }
                            if (!groupedByDate[dateKey]) {
                                groupedByDate[dateKey] = [];
                            }
                            groupedByDate[dateKey].push(r);
                        });

                        // Sort dates descending (most recent first)
                        const sortedDates = Object.keys(groupedByDate).sort((a, b) => {
                            if (a === 'Unknown') return 1;
                            if (b === 'Unknown') return -1;
                            return b.localeCompare(a);
                        });

                        // Sort items within each date group by full datetime descending
                        sortedDates.forEach(dateKey => {
                            groupedByDate[dateKey].sort((a, b) => {
                                const dateA = a.date || '';
                                const dateB = b.date || '';
                                return dateB.localeCompare(dateA);
                            });
                        });

                        let html = '';
                        sortedDates.forEach(dateKey => {
                            const items = groupedByDate[dateKey];
                            const safeKey = dateKey.replace(/[^a-zA-Z0-9]/g, '_');
                            const isExpanded = searchExpandedGroups[safeKey] || false;

                            // Date group header
                            html += `
                                <div style="max-width: 800px; margin: 0 auto 8px auto;">
                                    <div onclick="toggleSearchGroup('${safeKey}')" style="cursor: pointer; padding: 12px 16px; background: rgba(99, 102, 241, 0.15); border: 1px solid rgba(99, 102, 241, 0.3); border-radius: 12px; display: flex; align-items: center; gap: 12px; user-select: none;">
                                        <span id="search-group-icon-${safeKey}" style="font-size: 1.4em; font-weight: 700; color: #a855f7; width: 20px; text-align: center;">${isExpanded ? '−' : '+'}</span>
                                        <span style="font-weight: 600; color: var(--text-main); flex-grow: 1;">${dateKey}</span>
                                        <span style="background: rgba(168, 85, 247, 0.2); color: #a855f7; padding: 4px 10px; border-radius: 8px; font-size: 0.85em; font-weight: 600;">${items.length} item${items.length !== 1 ? 's' : ''}</span>
                                    </div>
                                    <div id="search-group-content-${safeKey}" style="display: ${isExpanded ? 'block' : 'none'}; margin-top: 8px; padding-left: 20px; border-left: 2px solid rgba(99, 102, 241, 0.3);">
                            `;

                            // Items within the group
                            items.forEach(r => {
                                let stateColor = '#6366f1';
                                if (r.state === 'Complete') stateColor = '#22c55e';
                                else if (r.state === 'Todo') stateColor = '#eab308';
                                else if (r.state === 'In Progress') stateColor = '#f59e0b';
                                else if (r.state === 'Failed') stateColor = '#ef4444';
                                else if (r.state === 'Dump') stateColor = '#fbbf24';

                                html += `
                                    <div class="task-card" style="border-left-color: ${stateColor}; margin: 0 0 10px 0;" onclick="openFile('${r.folder}', '${r.filename}')">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <div class="project-badge" style="background: ${stateColor}20; color: ${stateColor}; border: 1px solid ${stateColor}40; margin-bottom: 0;">
                                                ${r.state}
                                            </div>
                                            <div class="task-date"><i class="far fa-clock"></i> ${r.date}</div>
                                        </div>
                                        <div class="task-title" style="margin-top: 12px;">${r.filename}</div>
                                        <div class="search-snippet">${r.snippet.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</div>
                                    </div>
                                `;
                            });

                            html += `
                                    </div>
                                </div>
                            `;
                        });

                        document.getElementById('searchResultsList').innerHTML = html;
                    }
                }
            } catch (err) {
                document.getElementById('searchResultsList').innerHTML = '<p style="color:#f43f5e; text-align:center;">Error searching.</p>';
            }
        }
        
        function clearSearch() {
            document.getElementById('searchInput').value = '';
            isSearching = false;
            document.getElementById('mainBoard').style.display = 'grid';
            document.getElementById('searchResults').style.display = 'none';
            document.getElementById('clearSearchBtn').style.display = 'none';
            fetchTasks();
        }

        async function fetchTasks() {
            if (isSearching) return;
            try {
                // Build URL with date range parameters
                const params = new URLSearchParams();
                if (currentDateRange.start) {
                    params.set('startDate', currentDateRange.start);
                }
                if (currentDateRange.end) {
                    params.set('endDate', currentDateRange.end);
                }
                const queryString = params.toString();
                const url = '/api/tasks' + (queryString ? `?${queryString}` : '');
                const res = await fetch(url);
                lastTasksData = await res.json();
                renderBoard(lastTasksData);
                checkReviewTasks();
            } catch (err) {
                console.error("Failed to fetch tasks", err);
            }
        }

        // Initialize date range filter and start fetching
        initializeDateRangeFilter();
        fetchTasks();
        setInterval(fetchTasks, 2000);
    </script>
</body>
</html>
"""


def _json_bytes(payload: Any) -> bytes:
    return json.dumps(payload).encode("utf-8")


def _slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned or "unclassified"


@dataclass(frozen=True)
class EpicReviewTask:
    path: Path
    filename: str
    title: str
    workstream: str
    workstream_group: str
    task_id: str
    epic: str
    epic_slug: str
    priority: int
    status_folder: str
    agent: str | None
    content: str
    purpose: str
    input_text: str
    output_text: str
    verification_text: str
    dependency_text: str
    rejection_reason: str | None
    timestamp: str


def _render_epic_review_html() -> str:
    index_html = (TASK_REVIEW_STATIC_DIR / "index.html").read_text(encoding="utf-8")
    styles = (TASK_REVIEW_STATIC_DIR / "styles.css").read_text(encoding="utf-8")
    app_js = (TASK_REVIEW_STATIC_DIR / "app.js").read_text(encoding="utf-8")
    index_html = index_html.replace('<link rel="stylesheet" href="/static/styles.css">', f"<style>\n{styles}\n</style>")
    index_html = index_html.replace(
        '<script src="/static/app.js"></script>',
        "<script>\n"
        "document.addEventListener('DOMContentLoaded', () => {\n"
        "    const header = document.querySelector('.hero');\n"
        "    if (header) {\n"
        "        const back = document.createElement('a');\n"
        "        back.href = '/';\n"
        "        back.textContent = '\\u2190 Back to Kanban';\n"
        "        back.style.cssText = 'display:inline-flex;align-items:center;gap:8px;padding:10px 14px;border-radius:14px;text-decoration:none;background:rgba(255,255,255,0.75);border:1px solid rgba(71,52,31,0.16);color:#1f1a14;font:600 0.95rem/1.2 Segoe UI,sans-serif;margin-bottom:16px;';\n"
        "        header.prepend(back);\n"
        "    }\n"
        "});\n"
        f"{app_js}\n"
        "</script>",
    )
    return index_html


def _render_epic_reconciliation_html() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epic Reconciliation</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-deep: #080a18;
            --bg-accent: #0f1225;
            --glass-bg: rgba(255, 255, 255, 0.03);
            --glass-border: rgba(255, 255, 255, 0.08);
            --text-main: #f1f5f9;
            --text-dim: #94a3b8;
            --success: #22c55e;
            --warning: #f59e0b;
            --error: #ef4444;
            --info: #3b82f6;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Outfit', sans-serif;
            background: radial-gradient(circle at 50% 0%, #1e1b4b 0%, var(--bg-deep) 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 30px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            text-align: center; margin-bottom: 30px; padding: 25px;
            background: var(--glass-bg); backdrop-filter: blur(20px);
            border-radius: 20px; border: 1px solid var(--glass-border);
        }
        .header h1 {
            font-size: 2em; font-weight: 700; margin-bottom: 10px;
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .back-link {
            display: inline-block; margin-bottom: 15px; color: var(--text-dim);
            text-decoration: none; font-size: 0.9em;
        }
        .back-link:hover { color: var(--text-main); }
        .epic-selector {
            display: flex; gap: 15px; align-items: center; justify-content: center;
            margin-bottom: 30px; flex-wrap: wrap;
        }
        select, button {
            padding: 12px 20px; border-radius: 12px; font-family: inherit;
            font-size: 1em; border: 1px solid var(--glass-border);
            background: var(--glass-bg); color: var(--text-main);
        }
        select {
            min-width: 300px;
            background: #1e1b4b;
            cursor: pointer;
        }
        select option {
            background: #1e1b4b;
            color: var(--text-main);
            padding: 10px;
        }
        select:focus {
            outline: 2px solid #6366f1;
            outline-offset: 2px;
        }
        button {
            background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
            border: none; cursor: pointer; font-weight: 600;
        }
        button:hover { opacity: 0.9; }
        .summary-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px; margin-bottom: 30px;
        }
        .summary-card {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 16px; padding: 20px; text-align: center;
        }
        .summary-card .count {
            font-size: 2.5em; font-weight: 700; margin-bottom: 5px;
        }
        .summary-card .label { color: var(--text-dim); font-size: 0.9em; }
        .summary-card.complete .count { color: var(--success); }
        .summary-card.in-progress .count { color: var(--info); }
        .summary-card.failed .count { color: var(--error); }
        .summary-card.backlog .count { color: var(--warning); }
        .progress-bar {
            height: 20px; background: rgba(255,255,255,0.1); border-radius: 10px;
            overflow: hidden; margin-bottom: 30px;
        }
        .progress-fill {
            height: 100%; background: linear-gradient(90deg, var(--success), #10b981);
            transition: width 0.5s ease;
        }
        .section {
            background: var(--glass-bg); border: 1px solid var(--glass-border);
            border-radius: 16px; padding: 20px; margin-bottom: 20px;
        }
        .section h3 {
            font-size: 1.1em; margin-bottom: 15px; display: flex;
            align-items: center; gap: 10px;
        }
        .task-list { display: flex; flex-direction: column; gap: 10px; }
        .task-item {
            background: rgba(0,0,0,0.2); border-radius: 10px; padding: 12px 15px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .task-item .title { font-weight: 500; }
        .task-item .meta { color: var(--text-dim); font-size: 0.85em; }
        .badge {
            padding: 4px 10px; border-radius: 20px; font-size: 0.8em; font-weight: 600;
        }
        .badge.complete { background: rgba(34,197,94,0.2); color: var(--success); }
        .badge.in-progress { background: rgba(59,130,246,0.2); color: var(--info); }
        .badge.failed { background: rgba(239,68,68,0.2); color: var(--error); }
        .badge.backlog { background: rgba(245,158,11,0.2); color: var(--warning); }
        .badge.review { background: rgba(168,85,247,0.2); color: #a855f7; }
        .blocking-issues {
            background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3);
            border-radius: 12px; padding: 15px; margin-bottom: 20px;
        }
        .blocking-issues h4 { color: var(--error); margin-bottom: 10px; }
        .blocking-issues ul { list-style: none; }
        .blocking-issues li { padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.05); }
        .manifest-info {
            color: var(--text-dim); font-size: 0.85em; margin-top: 10px;
        }
        .empty-state { text-align: center; padding: 40px; color: var(--text-dim); }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="/" class="back-link">← Back to Kanban</a>
            <h1>Epic Reconciliation</h1>
            <p style="color: var(--text-dim);">Compare decomposed tasks against deliverables</p>
        </div>

        <div class="epic-selector">
            <select id="epicSelect">
                <option value="">Select an epic...</option>
            </select>
            <button onclick="loadReconciliation()">Load Reconciliation</button>
        </div>

        <div id="content">
            <div class="empty-state">Select an epic to view reconciliation status</div>
        </div>
    </div>

    <script>
        async function loadEpics() {
            try {
                const resp = await fetch('/api/epics/with-solutions');
                const data = await resp.json();
                const select = document.getElementById('epicSelect');
                (data.epics || []).forEach(epic => {
                    const opt = document.createElement('option');
                    opt.value = epic.slug;
                    const pct = Number.isFinite(Number(epic.progress_pct)) ? Number(epic.progress_pct) : 0;
                    const complete = Number(epic.complete_count || 0);
                    const expected = Number(epic.expected_count || 0);
                    opt.textContent = `${epic.name || epic.slug} (${pct}% • ${complete}/${expected})`;
                    select.appendChild(opt);
                });
            } catch (e) {
                console.error('Failed to load epics:', e);
            }
        }

        async function loadReconciliation() {
            const slug = document.getElementById('epicSelect').value;
            if (!slug) return alert('Please select an epic');

            const content = document.getElementById('content');
            content.innerHTML = '<div class="empty-state">Loading...</div>';

            try {
                const resp = await fetch(`/api/epics/${slug}/full-reconciliation`);
                const data = await resp.json();
                renderReconciliation(data);
            } catch (e) {
                content.innerHTML = '<div class="empty-state">Error loading reconciliation</div>';
            }
        }

        function renderReconciliation(data) {
            const content = document.getElementById('content');
            const s = data.summary || {};
            const pct = s.delivery_pct || 0;

            let html = `
                <div class="summary-grid">
                    <div class="summary-card">
                        <div class="count">${s.expected || 0}</div>
                        <div class="label">Expected</div>
                    </div>
                    <div class="summary-card complete">
                        <div class="count">${s.complete || 0}</div>
                        <div class="label">Complete</div>
                    </div>
                    <div class="summary-card in-progress">
                        <div class="count">${s.in_progress || 0}</div>
                        <div class="label">In Progress</div>
                    </div>
                    <div class="summary-card" style="--count-color: #a855f7;">
                        <div class="count" style="color: #a855f7;">${s.review || 0}</div>
                        <div class="label">In Review</div>
                    </div>
                    <div class="summary-card backlog">
                        <div class="count">${s.backlog || 0}</div>
                        <div class="label">Backlog</div>
                    </div>
                    <div class="summary-card failed">
                        <div class="count">${s.failed || 0}</div>
                        <div class="label">Failed</div>
                    </div>
                </div>

                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${pct}%"></div>
                </div>
                <p style="text-align: center; margin-bottom: 20px; font-size: 1.2em;">
                    <strong>${pct}%</strong> Delivery Progress
                </p>
            `;

            if (data.blocking_issues && data.blocking_issues.length > 0) {
                html += `<div class="blocking-issues">
                    <h4>⚠️ Blocking Issues</h4>
                    <ul>${data.blocking_issues.map(i => `<li>${i.message}</li>`).join('')}</ul>
                </div>`;
            }

            const statusSections = [
                { key: 'failed', label: '❌ Failed', badge: 'failed' },
                { key: 'in_progress', label: '🔄 In Progress', badge: 'in-progress' },
                { key: 'review', label: '👀 In Review', badge: 'review' },
                { key: 'backlog', label: '📋 Backlog', badge: 'backlog' },
                { key: 'complete', label: '✅ Complete', badge: 'complete' },
                { key: 'not_found', label: '❓ Not Started', badge: 'backlog' },
            ];

            const tasks = data.tasks_by_status || {};
            statusSections.forEach(sec => {
                const items = tasks[sec.key] || [];
                if (items.length === 0) return;
                html += `<div class="section">
                    <h3><span class="badge ${sec.badge}">${items.length}</span> ${sec.label}</h3>
                    <div class="task-list">
                        ${items.map(t => `
                            <div class="task-item">
                                <div>
                                    <div class="title">${t.title || t.filename || 'Untitled'}</div>
                                    <div class="meta">${t.task_id || ''} ${t.agent ? '• ' + t.agent : ''} ${t.retry_count ? '• Retries: ' + t.retry_count : ''}</div>
                                </div>
                            </div>
                        `).join('')}
                    </div>
                </div>`;
            });

            if (data.manifest_found) {
                html += `<div class="manifest-info">
                    📄 Manifest found | Decomposed: ${data.decomposed_at || 'Unknown'} | Source: ${data.source_epic_path || 'Unknown'}
                </div>`;
            } else {
                html += `<div class="manifest-info" style="color: var(--warning);">
                    ⚠️ No decomposition manifest found - using fallback task detection
                </div>`;
            }

            content.innerHTML = html;
        }

        loadEpics();
    </script>
</body>
</html>'''


def _render_epic_decomposition_html() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Epic Decomposition</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
    <style>
        :root {
            --bg-dark: #0f1225;
            --bg-card: rgba(30, 35, 60, 0.8);
            --text-main: #f0f0f5;
            --text-dim: #9ca3af;
            --accent-purple: #8b5cf6;
            --accent-green: #10b981;
            --accent-blue: #3b82f6;
            --border-color: rgba(139, 92, 246, 0.3);
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', system-ui, sans-serif;
            background: linear-gradient(135deg, #0f1225 0%, #1a1f3a 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding: 24px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 24px;
        }
        .header h1 { font-size: 1.8rem; display: flex; align-items: center; gap: 12px; }
        .back-btn {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 10px 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            color: var(--text-main);
            text-decoration: none;
            font-weight: 500;
            transition: all 0.2s;
        }
        .back-btn:hover { background: rgba(255,255,255,0.15); }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }
        .panel {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
        }
        .panel-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .panel-header h2 { font-size: 1.1rem; color: var(--accent-purple); }
        .breadcrumb {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-bottom: 12px;
            flex-wrap: wrap;
        }
        .breadcrumb span { cursor: pointer; }
        .breadcrumb span:hover { color: var(--accent-purple); }
        .file-list {
            max-height: 400px;
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 8px;
        }
        .file-item {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 14px;
            cursor: pointer;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            transition: background 0.15s;
        }
        .file-item:hover { background: rgba(139, 92, 246, 0.15); }
        .file-item.selected { background: rgba(139, 92, 246, 0.3); }
        .file-item.folder { color: var(--accent-blue); }
        .file-item i { width: 20px; text-align: center; }
        .preview-content {
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 16px;
            max-height: 300px;
            overflow-y: auto;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.85rem;
            white-space: pre-wrap;
            color: var(--text-dim);
        }
        .workstream-list {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-top: 16px;
        }
        .workstream-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px 16px;
            background: rgba(0,0,0,0.2);
            border-radius: 10px;
            border-left: 4px solid var(--accent-purple);
        }
        .workstream-item .ws-name {
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .workstream-item .ws-letter {
            background: var(--accent-purple);
            color: white;
            width: 28px;
            height: 28px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
        }
        .workstream-item select {
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background: rgba(0,0,0,0.3);
            color: var(--text-main);
            font-size: 0.9rem;
        }
        .actions-panel {
            grid-column: 1 / -1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }
        .btn-primary {
            background: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
            color: white;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4); }
        .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .btn-secondary {
            background: rgba(255,255,255,0.1);
            color: var(--text-main);
            border: 1px solid var(--border-color);
        }
        .status-area {
            padding: 16px;
            border-radius: 10px;
            background: rgba(0,0,0,0.2);
            display: none;
        }
        .status-area.visible { display: block; }
        .status-area.success { border-left: 4px solid var(--accent-green); }
        .status-area.error { border-left: 4px solid #ef4444; }
        .task-count { font-size: 0.9rem; color: var(--text-dim); }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-dim);
        }
        .empty-state i { font-size: 2rem; margin-bottom: 12px; opacity: 0.5; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1><i class="fas fa-project-diagram"></i> Epic Decomposition</h1>
            <div style="display: flex; gap: 12px;">
                <a href="/" class="back-btn"><i class="fas fa-arrow-left"></i> Kanban</a>
                <a href="/epic-review" class="back-btn"><i class="fas fa-tasks"></i> Epic Review</a>
            </div>
        </div>

        <div class="main-grid">
            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-folder-open"></i> Browse Epic Document</h2>
                    <span class="task-count" id="fileCount">0 files</span>
                </div>
                <div class="breadcrumb" id="breadcrumb"></div>
                <div class="file-list" id="fileList">
                    <div class="empty-state">
                        <i class="fas fa-spinner fa-spin"></i>
                        <p>Loading files...</p>
                    </div>
                </div>
            </div>

            <div class="panel">
                <div class="panel-header">
                    <h2><i class="fas fa-eye"></i> Preview</h2>
                    <span id="selectedFile" style="color: var(--text-dim); font-size: 0.85rem;">No file selected</span>
                </div>
                <div class="preview-content" id="previewContent">
                    Select a markdown file to preview its contents.
                </div>
            </div>

            <div class="panel actions-panel">
                <div style="display:flex; flex-direction:column; gap:10px; min-width: 420px;">
                    <div style="color: var(--text-dim); font-size: 0.9rem;">
                        <i class="fas fa-info-circle"></i> Select an epic file, then click Decompose. Tasks will be created in the destination folder below.
                    </div>
                    <label style="display:flex; flex-direction:column; gap:6px; color: var(--text-dim); font-size:0.85rem;">
                        <span>Destination Folder</span>
                        <input type="text" id="destinationFolder" value="workstream/100_backlog" style="padding:10px 12px; border-radius:10px; border:1px solid var(--border-color); background:rgba(0,0,0,0.25); color:var(--text-main); font-family:'JetBrains Mono', monospace; font-size:0.85rem;">
                    </label>
                </div>
                <div style="display: flex; gap: 12px; align-items: center;">
                    <span id="taskPreviewCount" style="color: var(--text-dim);"></span>
                    <button class="btn btn-primary" onclick="executeDecomposition()" id="decomposeBtn" disabled>
                        <i class="fas fa-magic"></i> Decompose Epic
                    </button>
                </div>
            </div>

            <div class="panel status-area" id="statusArea" style="grid-column: 1 / -1;">
                <div id="statusContent"></div>
            </div>
        </div>
    </div>

    <script>
        let currentPath = '';
        let selectedFilePath = '';

        document.addEventListener('DOMContentLoaded', () => {
            loadFiles('workstream/000_epic');
        });

        async function loadFiles(path) {
            currentPath = path;
            updateBreadcrumb();
            const fileList = document.getElementById('fileList');
            fileList.innerHTML = '<div class="empty-state"><i class="fas fa-spinner fa-spin"></i><p>Loading...</p></div>';

            try {
                const resp = await fetch(`/api/browse-files?path=${encodeURIComponent(path)}`);
                const data = await resp.json();
                renderFileList(data.items || []);
            } catch (err) {
                fileList.innerHTML = '<div class="empty-state"><i class="fas fa-exclamation-triangle"></i><p>Error loading files</p></div>';
            }
        }

        function updateBreadcrumb() {
            const parts = currentPath.split('/').filter(p => p);
            const bc = document.getElementById('breadcrumb');
            let html = '<span onclick="loadFiles(\\'\\')"><i class="fas fa-home"></i></span>';
            let accumulated = '';
            parts.forEach((part, idx) => {
                accumulated += (accumulated ? '/' : '') + part;
                const pathCopy = accumulated;
                html += ` / <span onclick="loadFiles('${pathCopy}')">${part}</span>`;
            });
            bc.innerHTML = html;
        }

        function renderFileList(items) {
            const fileList = document.getElementById('fileList');
            const folders = items.filter(i => i.is_dir).sort((a,b) => a.name.localeCompare(b.name));
            const files = items.filter(i => !i.is_dir && i.name.endsWith('.md')).sort((a,b) => a.name.localeCompare(b.name));

            document.getElementById('fileCount').textContent = `${files.length} files, ${folders.length} folders`;

            if (folders.length === 0 && files.length === 0) {
                fileList.innerHTML = '<div class="empty-state"><i class="fas fa-folder-open"></i><p>No markdown files found</p></div>';
                return;
            }

            let html = '';
            // Parent directory
            if (currentPath) {
                const parentPath = currentPath.split('/').slice(0, -1).join('/');
                html += `<div class="file-item folder" onclick="loadFiles('${parentPath}')"><i class="fas fa-level-up-alt"></i> ..</div>`;
            }
            folders.forEach(f => {
                const fullPath = currentPath ? `${currentPath}/${f.name}` : f.name;
                html += `<div class="file-item folder" onclick="loadFiles('${fullPath}')"><i class="fas fa-folder"></i> ${f.name}</div>`;
            });
            files.forEach(f => {
                const fullPath = currentPath ? `${currentPath}/${f.name}` : f.name;
                html += `<div class="file-item" data-path="${fullPath}" onclick="selectFile('${fullPath}', this)"><i class="fas fa-file-alt"></i> ${f.name}</div>`;
            });
            fileList.innerHTML = html;
        }

        async function selectFile(path, el) {
            document.querySelectorAll('.file-item.selected').forEach(e => e.classList.remove('selected'));
            el.classList.add('selected');
            selectedFilePath = path;
            document.getElementById('selectedFile').textContent = path.split('/').pop();

            try {
                const resp = await fetch(`/api/file-preview?path=${encodeURIComponent(path)}`);
                const data = await resp.json();
                document.getElementById('previewContent').textContent = data.content || 'Unable to load preview';
                // Enable decompose button when file is selected
                document.getElementById('decomposeBtn').disabled = false;
            } catch (err) {
                document.getElementById('previewContent').textContent = 'Error loading file preview';
            }
        }

        async function executeDecomposition() {
            if (!selectedFilePath) return;

            document.getElementById('decomposeBtn').disabled = true;
            document.getElementById('decomposeBtn').innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';

            try {
                const resp = await fetch('/api/decompose-epic', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        epic_path: selectedFilePath,
                        destination_folder: document.getElementById('destinationFolder')?.value || 'workstream/100_backlog'
                    })
                });
                const data = await resp.json();
                if (data.success) {
                    const epicFolder = data.epic_output_folder ? `<br>Epic output folder: <code>${data.epic_output_folder}</code>` : '';
                    const destFolder = data.destination_folder ? `<br>Destination folder: <code>${data.destination_folder}</code>` : '';
                    showStatus('success', `Successfully created ${data.tasks_created.length} task files.${destFolder}${epicFolder}<br><br><a href="/epic-review" style="color: var(--accent-purple); font-weight: 600;">Open Epic Review to manage tasks →</a>`);
                } else {
                    showStatus('error', data.error || 'Decomposition failed');
                }
            } catch (err) {
                showStatus('error', 'Error executing decomposition: ' + err.message);
            } finally {
                document.getElementById('decomposeBtn').disabled = false;
                document.getElementById('decomposeBtn').innerHTML = '<i class="fas fa-magic"></i> Decompose Epic';
            }
        }

        function showStatus(type, message) {
            const area = document.getElementById('statusArea');
            area.className = `panel status-area visible ${type}`;
            document.getElementById('statusContent').innerHTML = message;
        }
    </script>
</body>
</html>'''


def _extract_heading_section(content: str, heading: str) -> str:
    pattern = rf"(?im)^##?\s*{re.escape(heading)}\s*$\n(.*?)(?=^\s*##?\s+|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_metadata(content: str, label: str) -> str:
    match = re.search(rf"(?im)^\*\*{re.escape(label)}:\*\*\s*(.+)$", content)
    if match:
        return match.group(1).strip()
    match = re.search(rf"(?im)^{re.escape(label)}:\s*(.+)$", content)
    return match.group(1).strip() if match else ""


def _strip_known_suffixes(value: str) -> str:
    cleaned = str(value or "").strip().strip("`")
    while cleaned.lower().endswith(".md") or cleaned.lower().endswith(".result"):
        if cleaned.lower().endswith(".md"):
            cleaned = cleaned[:-3]
        elif cleaned.lower().endswith(".result"):
            cleaned = cleaned[:-7]
    return cleaned


def _canonical_epic_family(value: str | None) -> str:
    raw = _strip_known_suffixes(str(value or ""))
    if not raw:
        return ""
    lowered = raw.lower().replace("-", "_").replace(" ", "_")
    lowered = re.sub(r"[`/\\]+", "_", lowered)
    lowered = re.sub(r"_+", "_", lowered).strip("_")
    lowered = re.sub(r"^\d{8}_\d{6}_", "", lowered)

    for family, patterns in EPIC_FAMILY_PATTERNS:
        if any(pattern in lowered for pattern in patterns):
            return family

    if lowered.startswith(("codex_", "gemini_", "claude_", "general_")):
        parts = lowered.split("_", 1)
        lowered = parts[1] if len(parts) > 1 else lowered
        for family, patterns in EPIC_FAMILY_PATTERNS:
            if any(pattern in lowered for pattern in patterns):
                return family

    return lowered


def _family_from_project(project: str | None) -> str:
    project_clean = _canonical_epic_family(project)
    if project_clean in {"general", "codex", "gemini", "claude", "root", "unassigned", "task", "blocker"}:
        return ""
    if project_clean in {"mvp"}:
        return "mvp_prd_mobile_quarterly_export"
    if project_clean in {"strategy"}:
        return "strategy_warehouse_marketing_engine"
    return project_clean


def _project_from_filename(filename: str) -> str:
    pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
    match = pattern.match(str(filename or ""))
    if not match:
        return ""
    _, part1, rest = match.groups()
    if part1.lower() in {"codex", "gemini", "claude", "general"}:
        if "_" in rest:
            return rest.split("_", 1)[0]
        return rest
    return part1


def _detect_epic_family_from_content(content: str, path_hint: str = "") -> str:
    candidates = [
        _extract_metadata(content, "Epic"),
        _extract_metadata(content, "Source"),
        _extract_metadata(content, "Source Epic Path"),
        _extract_metadata(content, "Project"),
        path_hint,
    ]
    for candidate in candidates:
        family = _canonical_epic_family(candidate)
        if family:
            return family

    project_family = _family_from_project(_project_from_filename(Path(path_hint).name if path_hint else ""))
    if project_family:
        return project_family

    combined = " ".join(filter(None, [path_hint, content[:2000]]))
    return _canonical_epic_family(combined)


def _detect_epic_family_for_file(task_path: str | Path) -> str:
    path_obj = Path(task_path)
    try:
        content = path_obj.read_text(encoding="utf-8", errors="replace")
    except Exception:
        content = ""
    return _detect_epic_family_from_content(content, str(path_obj))


def _pending_path_for_file(task_path: Path, state_folder: str) -> Path:
    state_root = Path(WORKSTREAM_DIR) / state_folder
    rel_path = task_path.relative_to(state_root)
    if rel_path.parts and rel_path.parts[0] == PIPELINE_PENDING_DIRNAME:
        return task_path
    return state_root / PIPELINE_PENDING_DIRNAME / rel_path


def _restore_path_from_pending(task_path: Path, state_folder: str) -> Path:
    state_root = Path(WORKSTREAM_DIR) / state_folder
    pending_root = state_root / PIPELINE_PENDING_DIRNAME
    rel_path = task_path.relative_to(pending_root)
    return state_root / rel_path


def _move_file_preserving_uniqueness(src: Path, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    target = dest
    if target.exists():
        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        target = target.with_name(f"{target.stem}_{suffix}{target.suffix}")
    shutil.move(str(src), str(target))
    return target


def _iter_state_markdown_files(state_folder: str) -> list[Path]:
    state_root = Path(WORKSTREAM_DIR) / state_folder
    if not state_root.exists():
        return []
    return [path for path in state_root.rglob("*.md") if path.is_file()]


def _extract_task_id(title: str) -> str:
    match = re.search(r"\b([A-Z]\d+(?:\.\d+)?)\b", title)
    if match:
        return match.group(1)
    match = re.search(r"\btask[_\s-]*(\d+)\b", title, re.IGNORECASE)
    return f"TASK-{match.group(1)}" if match else "N/A"


def _extract_workstream_group(workstream: str, filename: str) -> str:
    match = re.search(r"\b([A-Z])\b", workstream)
    if match:
        return match.group(1)
    match = re.search(r"workstream([a-z])", filename, re.IGNORECASE)
    return match.group(1).upper() if match else "General"


def _extract_rejection_reason(content: str) -> str | None:
    match = re.search(r"(?im)^Rejection Reason:\s*(.+)$", content)
    return match.group(1).strip() if match else None


def _task_title_from_content(content: str, filename: str) -> str:
    first_heading = re.search(r"(?im)^#\s*(.+)$", content)
    if first_heading:
        return first_heading.group(1).strip()
    return filename.rsplit(".", 1)[0]


def _repo_root() -> Path:
    return Path(WORKSTREAM_DIR).parent


def _resolve_repo_path(rel_path: str) -> Path:
    base_dir = _repo_root().resolve()
    target = (base_dir / str(rel_path or "").strip()).resolve()
    if target != base_dir and base_dir not in target.parents:
        raise ValueError(f"path_outside_repo: {rel_path}")
    return target


def _retag_task_filename(filename: str, target_agent: str | None = None) -> str:
    pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
    match = pattern.match(filename)
    if not match or target_agent not in {"codex", "gemini", "claude", "general"}:
        return filename
    timestamp, part1, rest = match.groups()
    if part1.lower() in {"codex", "gemini", "claude", "general"}:
        return f"{timestamp}_{target_agent}_{rest}.md"
    return f"{timestamp}_{target_agent}_{part1}_{rest}.md"


def _epic_review_task_files(folder_path: str | None = None) -> list[Path]:
    task_files: list[Path] = []
    if folder_path:
        target_dir = _resolve_repo_path(folder_path)
        if target_dir.exists():
            task_files.extend([p for p in target_dir.rglob("*.md") if p.is_file()])
        return task_files

    root = Path(WORKSTREAM_DIR)
    for folder in EPIC_REVIEW_STATE_FOLDERS:
        state_dir = root / folder
        if state_dir.exists():
            task_files.extend(state_dir.rglob("*.md"))
    return task_files


def _list_epic_documents(path: str = "workstream/000_epic") -> list[dict[str, Any]]:
    epic_root = _resolve_repo_path(path)
    if not epic_root.exists():
        return []
    epics: dict[str, dict[str, Any]] = {}
    for epic_file in epic_root.rglob("*.md"):
        if not epic_file.is_file():
            continue
        try:
            rel_parts = epic_file.relative_to(epic_root).parts
        except ValueError:
            rel_parts = epic_file.parts
        if any(part in EPIC_REVIEW_MODEL_FOLDERS for part in rel_parts[:-1]):
            continue
        lowered = epic_file.name.lower()
        if lowered.endswith("_processed.md") or lowered.endswith("_review.md"):
            continue
        content = epic_file.read_text(encoding="utf-8", errors="replace")
        name = _task_title_from_content(content, epic_file.name)
        slug = _slugify(name)
        epics.setdefault(
            slug,
            {
                "slug": slug,
                "name": name,
                "path": str(epic_file.relative_to(Path(WORKSTREAM_DIR).parent)).replace("\\", "/"),
            },
        )
    return sorted(epics.values(), key=lambda item: item["name"].lower())


def _parse_epic_review_task(task_file: Path) -> EpicReviewTask:
    root = Path(WORKSTREAM_DIR)
    content = task_file.read_text(encoding="utf-8", errors="replace")
    try:
        rel_parts = task_file.relative_to(root).parts
        status_folder = rel_parts[0]
        agent = rel_parts[1] if len(rel_parts) > 2 and rel_parts[1] in EPIC_REVIEW_MODEL_FOLDERS else None
    except ValueError:
        rel_parts = ()
        status_folder = "external"
        agent = None
    filename = task_file.name
    title = _task_title_from_content(content, filename)
    workstream = _extract_metadata(content, "Workstream") or "Unknown"
    epic = _extract_metadata(content, "Epic") or "Unspecified Epic"
    priority_raw = _extract_metadata(content, "Priority") or "3"
    try:
        priority = int(re.search(r"\d+", priority_raw).group(0))
    except Exception:
        priority = 3
    timestamp_match = re.match(r"(\d{8}_\d{6})", filename)
    return EpicReviewTask(
        path=task_file,
        filename=filename,
        title=title,
        workstream=workstream,
        workstream_group=_extract_workstream_group(workstream, filename),
        task_id=_extract_task_id(title),
        epic=epic,
        epic_slug=_slugify(epic),
        priority=priority,
        status_folder=status_folder,
        agent=agent,
        content=content,
        purpose=_extract_heading_section(content, "Purpose"),
        input_text=_extract_heading_section(content, "Input"),
        output_text=_extract_heading_section(content, "Output"),
        verification_text=_extract_heading_section(content, "Verification"),
        dependency_text=_extract_heading_section(content, "Dependency"),
        rejection_reason=_extract_rejection_reason(content),
        timestamp=timestamp_match.group(1) if timestamp_match else "",
    )


def _parse_task_dependencies(content: str) -> list[str]:
    section = _extract_heading_section(content, "Dependency")
    if not section:
        return []
    raw = section.strip()
    if re.search(r"(?im)^Dependency:\s*None\s*$", raw):
        return []

    dependencies: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        stripped = re.sub(r"^-+\s*", "", stripped)
        stripped = re.sub(r"^Dependency:\s*", "", stripped, flags=re.IGNORECASE)
        matches = re.findall(r"([A-Za-z0-9_:-]+\.md)", stripped)
        if matches:
            for match in matches:
                dependencies.append(Path(match).name)
        elif stripped and stripped.lower() != "none":
            dependencies.append(stripped.strip("`"))
    seen: set[str] = set()
    ordered: list[str] = []
    for dep in dependencies:
        name = Path(dep).name.strip()
        if name and name not in seen:
            seen.add(name)
            ordered.append(name)
    return ordered


def _completed_task_filenames() -> set[str]:
    complete_root = Path(WORKSTREAM_DIR) / "300_complete"
    if not complete_root.exists():
        return set()
    return {path.name for path in complete_root.rglob("*.md") if path.is_file()}


def _task_dependencies_ready(task_path: str | Path, completed_files: set[str]) -> tuple[bool, list[str]]:
    try:
        content = Path(task_path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return False, ["__read_error__"]
    dependencies = _parse_task_dependencies(content)
    unmet = [dep for dep in dependencies if dep not in completed_files]
    return len(unmet) == 0, unmet


def _extract_task_date(filename: str) -> str | None:
    match = re.match(r"(\d{8})", filename)
    return match.group(1) if match else None


def _count_inprogress_for_date(root: str, target_date: str | None, focus_family: str | None = None) -> int:
    if not target_date:
        return 0
    count = 0
    for current_root, _, files in os.walk(root):
        count += sum(
            1
            for name in files
            if name.endswith(".md")
            and not name.startswith(".")
            and name.startswith(target_date)
            and PIPELINE_PENDING_DIRNAME not in Path(current_root).parts
            and (
                not focus_family
                or _detect_epic_family_for_file(os.path.join(current_root, name)) == _canonical_epic_family(focus_family)
            )
            and not _task_has_execution_evidence(os.path.join(current_root, name))
        )
    return count


def _task_has_execution_evidence(task_path: str) -> bool:
    try:
        with open(task_path, encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False
    return "## Execution Evidence" in content


agent_controller_proc: subprocess.Popen | None = None

def _launch_agent_controller():
    script = Path(WORKSTREAM_DIR) / "run_agent.py"
    proc = subprocess.Popen(
        [
            sys.executable,
            str(script)
        ],
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    print(f"Agent controller started: {datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
    return proc

def agent_controller_monitor():
    global agent_controller_proc
    while True:
        if agent_controller_proc is None or agent_controller_proc.poll() is not None:
            agent_controller_proc = _launch_agent_controller()
        time.sleep(5)


def _task_waiting_for_verification(content: str) -> bool:
    return "awaiting user verification" in content.lower()


def _execute_task(agent, task_file, source_dir, todo_dir, inprog_dir, review_dir, failed_dir, complete_dir, is_resume=False):
    source_path = os.path.join(source_dir, task_file)
    if not is_resume:
        try:
            os.rename(source_path, os.path.join(inprog_dir, task_file))
        except OSError:
            return False
    inprog_path = os.path.join(inprog_dir, task_file)
    gate_ok, gate_reason = _task_quality_gate(inprog_path)
    if not gate_ok:
        print(f"[Lane Worker: {agent.upper()}] QUALITY_GATE blocked {task_file}: {gate_reason}")
        time.sleep(2)
        return False
    cli_command = _build_agent_execution_command(agent, inprog_path)
    if not cli_command:
        print(f"[Lane Worker: {agent.upper()}] EXECUTION_CONFIG missing for {task_file}; set KANBAN_AGENT_EXEC_CMD_{agent.upper()} or KANBAN_AGENT_EXEC_CMD.")
        if not is_resume and os.path.exists(inprog_path):
            os.rename(inprog_path, source_path)
        time.sleep(2)
        return False
    print(f"[Lane Worker: {agent.upper()}] Launching headless agent execution on {task_file}...")
    _set_lane_active_task(agent, inprog_path)
    try:
        result = subprocess.run(cli_command, capture_output=True, text=True, timeout=1800, encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"[Lane Worker: {agent.upper()}] Exception executing {task_file}: {e}")
        failed_path = os.path.join(failed_dir, task_file)
        if os.path.exists(inprog_path):
            os.rename(inprog_path, failed_path)
        _set_lane_active_task(agent, None)
        return False
    finally:
        _set_lane_active_task(agent, None)
    try:
        with open(inprog_path, 'a', encoding='utf-8') as f:
            f.write("\n\n## Execution Evidence\n")
            f.write(f"- Agent lane: {agent}\n")
            f.write(f"- Command: {' '.join(cli_command)}\n")
            f.write(f"- Return code: {result.returncode}\n")
            out = (result.stdout or "").strip()
            err = (result.stderr or "").strip()
            if out:
                f.write("- Stdout:\n```text\n" + out[-4000:] + "\n```\n")
            if err:
                f.write("- Stderr:\n```text\n" + err[-4000:] + "\n```\n")
    except Exception as ev_err:
        print(f"[Lane Worker: {agent.upper()}] Failed to append execution evidence: {ev_err}")
    is_awaiting_verification = False
    try:
        with open(inprog_path, 'r', encoding='utf-8') as f:
            is_awaiting_verification = _task_waiting_for_verification(f.read())
    except Exception:
        pass
    final_ok, final_reason = _task_completion_gate(inprog_path)
    if result.returncode != 0:
        print(f"[Lane Worker: {agent.upper()}] Failed or Blocked: {task_file}")
        blocker_dir = _blocker_dir("200_inprogress", agent)
        blocker_dir.mkdir(parents=True, exist_ok=True)
        blocker_path = blocker_dir / task_file
        _append_retry_history(
            inprog_path,
            f"Execution failed in lane `{agent}` and was parked in `200_inprogress/blocker/{agent}` pending same-column retry. Error tail: {(result.stderr or '').strip()[-500:]}",
        )
        shutil.move(inprog_path, blocker_path)
        return False
    if is_awaiting_verification:
        print(f"[Lane Worker: {agent.upper()}] Task completed but requires manual review: {task_file}")
        review_path = os.path.join(review_dir, task_file)
        os.rename(inprog_path, review_path)
        return True
    if not final_ok:
        print(f"[Lane Worker: {agent.upper()}] COMPLETION_GATE blocked {task_file}: {final_reason}")
        failed_path = os.path.join(failed_dir, task_file)
        os.rename(inprog_path, failed_path)
        return False
    complete_path = os.path.join(complete_dir, task_file)
    os.rename(inprog_path, complete_path)
    return True


def _list_epics(folder_path: str | None = None) -> list[dict[str, Any]]:
    epics: dict[str, dict[str, Any]] = {}
    for task_file in _epic_review_task_files(folder_path):
        task = _parse_epic_review_task(task_file)
        entry = epics.setdefault(
            task.epic_slug,
            {"slug": task.epic_slug, "name": task.epic, "task_count": 0, "workstreams": set()},
        )
        entry["task_count"] += 1
        entry["workstreams"].add(task.workstream_group)
    return sorted(
        [
            {
                "slug": epic["slug"],
                "name": epic["name"],
                "task_count": epic["task_count"],
                "workstreams": sorted(epic["workstreams"]),
            }
            for epic in epics.values()
        ],
        key=lambda item: item["name"].lower(),
    )


def get_epic_tasks(
    epic_slug: str,
    workstream: str | None = None,
    status: str | None = None,
    priority: int | None = None,
    sort_by: str = "priority",
    folder_path: str | None = None,
) -> list[dict[str, Any]]:
    tasks: list[EpicReviewTask] = []
    for task_file in _epic_review_task_files(folder_path):
        task = _parse_epic_review_task(task_file)
        if task.epic_slug != epic_slug:
            continue
        if workstream and task.workstream_group != workstream:
            continue
        if status and task.status_folder != status:
            continue
        if priority and task.priority != priority:
            continue
        tasks.append(task)
    sorters = {
        "priority": lambda item: (item.priority, item.workstream_group, item.timestamp),
        "workstream": lambda item: (item.workstream_group, item.priority, item.timestamp),
        "timestamp": lambda item: (item.timestamp, item.priority, item.workstream_group),
    }
    ordered = sorted(tasks, key=sorters.get(sort_by, sorters["priority"]))
    return [
        {
            "path": str(task.path),
            "filename": task.filename,
            "title": task.title,
            "workstream": task.workstream,
            "workstream_group": task.workstream_group,
            "task_id": task.task_id,
            "epic": task.epic,
            "epic_slug": task.epic_slug,
            "priority": task.priority,
            "status_folder": task.status_folder,
            "agent": task.agent,
            "content": task.content,
            "purpose": task.purpose,
            "input": task.input_text,
            "output": task.output_text,
            "verification": task.verification_text,
            "rejection_reason": task.rejection_reason,
            "timestamp": task.timestamp,
        }
        for task in ordered
    ]


def _normalize_epic_reference(value: str | None) -> str:
    raw = str(value or "").strip().strip("`")
    if not raw:
        return ""
    name = Path(raw).name
    stem = name[:-3] if name.lower().endswith(".md") else name
    stem = re.sub(r"^\d{8}_\d{6}_", "", stem)
    stem = re.sub(r"_processed$", "", stem, flags=re.IGNORECASE)
    return _slugify(stem)


def _normalize_task_title_for_match(title: str | None) -> str:
    raw = str(title or "").strip()
    raw = re.sub(r"^task\s+[a-z]\d+:\s*", "", raw, flags=re.IGNORECASE)
    return re.sub(r"[^a-z0-9]+", " ", raw.lower()).strip()


def get_epic_delivery_reconciliation(epic_slug: str) -> dict[str, Any]:
    expected_tasks = get_epic_tasks(epic_slug=epic_slug, sort_by="workstream")
    if not expected_tasks:
        return {
            "epic_slug": epic_slug,
            "epic_name": None,
            "summary": {
                "expected_count": 0,
                "delivered_count": 0,
                "matched_count": 0,
                "missing_count": 0,
                "misfiled_count": 0,
            },
            "expected_tasks": [],
            "delivered_tasks": [],
            "missing_tasks": [],
            "misfiled_tasks": [],
            "extra_delivered_tasks": [],
        }

    epic_name = expected_tasks[0]["epic"]
    expected_by_task_id: dict[str, dict[str, Any]] = {}
    expected_by_title: dict[str, dict[str, Any]] = {}
    for task in expected_tasks:
        task_id = str(task.get("task_id") or "").strip().upper()
        title_key = _normalize_task_title_for_match(task.get("title"))
        if task_id:
            expected_by_task_id[task_id] = task
        if title_key:
            expected_by_title[title_key] = task

    delivered_for_epic: list[dict[str, Any]] = []
    delivered_other_epics: list[dict[str, Any]] = []
    complete_root = Path(WORKSTREAM_DIR) / "300_complete"
    if complete_root.exists():
        for task_file in complete_root.rglob("*.md"):
            if not task_file.is_file():
                continue
            content = task_file.read_text(encoding="utf-8", errors="replace")
            title = _task_title_from_content(content, task_file.name)
            task_id = _extract_task_id(title)
            epic_meta = _extract_metadata(content, "Epic")
            source_meta = _extract_metadata(content, "Source") or _extract_metadata(content, "Source Epic Path")
            epic_meta_slug = _slugify(epic_meta) if epic_meta else ""
            source_epic_slug = _normalize_epic_reference(source_meta)
            delivered_entry = {
                "path": str(task_file),
                "filename": task_file.name,
                "title": title,
                "task_id": task_id,
                "epic_meta": epic_meta,
                "epic_meta_slug": epic_meta_slug,
                "source_epic": source_meta,
                "source_epic_slug": source_epic_slug,
                "folder": str(task_file.parent.relative_to(Path(WORKSTREAM_DIR))).replace("\\", "/"),
            }
            if epic_meta_slug == epic_slug or source_epic_slug == epic_slug:
                delivered_for_epic.append(delivered_entry)
            else:
                delivered_other_epics.append(delivered_entry)

    delivered_by_task_id = {
        str(item.get("task_id") or "").strip().upper(): item
        for item in delivered_for_epic
        if str(item.get("task_id") or "").strip()
    }
    delivered_by_title = {
        _normalize_task_title_for_match(item.get("title")): item
        for item in delivered_for_epic
        if _normalize_task_title_for_match(item.get("title"))
    }

    matched_expected: list[dict[str, Any]] = []
    missing_tasks: list[dict[str, Any]] = []
    misfiled_tasks: list[dict[str, Any]] = []
    matched_keys: set[str] = set()

    for expected in expected_tasks:
        task_id = str(expected.get("task_id") or "").strip().upper()
        title_key = _normalize_task_title_for_match(expected.get("title"))
        delivered_match = delivered_by_task_id.get(task_id) if task_id else None
        if not delivered_match and title_key:
            delivered_match = delivered_by_title.get(title_key)
        if delivered_match:
            matched_expected.append({
                "expected": expected,
                "delivered": delivered_match,
            })
            matched_keys.add(delivered_match["filename"])
            continue

        misfiled_match = None
        for other in delivered_other_epics:
            other_task_id = str(other.get("task_id") or "").strip().upper()
            other_title_key = _normalize_task_title_for_match(other.get("title"))
            if task_id and other_task_id == task_id:
                misfiled_match = other
                break
            if title_key and other_title_key == title_key:
                misfiled_match = other
                break
        if misfiled_match:
            misfiled_tasks.append({
                "expected": expected,
                "delivered": misfiled_match,
            })
            continue

        missing_tasks.append(expected)

    extra_delivered_tasks = [
        item for item in delivered_for_epic
        if item["filename"] not in matched_keys
    ]

    return {
        "epic_slug": epic_slug,
        "epic_name": epic_name,
        "summary": {
            "expected_count": len(expected_tasks),
            "delivered_count": len(delivered_for_epic),
            "matched_count": len(matched_expected),
            "missing_count": len(missing_tasks),
            "misfiled_count": len(misfiled_tasks),
        },
        "expected_tasks": expected_tasks,
        "delivered_tasks": delivered_for_epic,
        "matched_tasks": matched_expected,
        "missing_tasks": missing_tasks,
        "misfiled_tasks": misfiled_tasks,
        "extra_delivered_tasks": extra_delivered_tasks,
    }


def get_epic_full_reconciliation(epic_slug: str) -> dict[str, Any]:
    """Full reconciliation showing task status across ALL workflow states.

    Compares original decomposition manifest against current task locations.
    Tracks every decomposed task through: backlog → in_progress → review → complete/failed
    """
    # Try to load decomposition manifest first (source of truth for original tasks)
    base_dir = _repo_root()
    manifest_path = base_dir / f"ep_{epic_slug}" / "decomposition_manifest.json"
    manifest = None
    expected_tasks = []

    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            # Only include non-archived tasks for reconciliation
            # Archived tasks were decomposed into subtasks which replace them
            all_tasks = manifest.get("tasks", [])
            expected_tasks = [t for t in all_tasks if not t.get("archived")]
            archived_tasks = [t for t in all_tasks if t.get("archived")]
        except Exception:
            manifest = None
            archived_tasks = []
    else:
        archived_tasks = []

    # Fallback to get_epic_tasks if no manifest
    if not expected_tasks:
        fallback_tasks = get_epic_tasks(epic_slug=epic_slug, sort_by="workstream")
        expected_tasks = [
            {
                "task_id": t.get("task_id", ""),
                "filename": t.get("filename", ""),
                "workstream": t.get("workstream", ""),
                "title": t.get("title", ""),
                "suggested_agent": t.get("suggested_agent", "general"),
            }
            for t in fallback_tasks
        ]

    if not expected_tasks:
        return {
            "epic_slug": epic_slug,
            "epic_name": manifest.get("epic_name") if manifest else None,
            "manifest_found": manifest is not None,
            "decomposed_at": manifest.get("decomposed_at") if manifest else None,
            "summary": {
                "expected": 0, "backlog": 0, "in_progress": 0,
                "review": 0, "complete": 0, "failed": 0, "not_found": 0,
                "delivery_pct": 0,
            },
            "tasks_by_status": {},
            "blocking_issues": [],
        }

    epic_name = manifest.get("epic_name", epic_slug) if manifest else epic_slug

    # Build lookup for expected tasks
    expected_by_id: dict[str, dict] = {}
    expected_by_title: dict[str, dict] = {}
    for task in expected_tasks:
        task_id = str(task.get("task_id") or "").strip().upper()
        title_key = _normalize_task_title_for_match(task.get("title"))
        if task_id:
            expected_by_id[task_id] = task
        if title_key:
            expected_by_title[title_key] = task

    # Scan all workflow states
    state_folders = {
        "backlog": "100_backlog",
        "in_progress": "200_inprogress",
        "review": "050_review",
        "complete": "300_complete",
        "failed": "400_failed",
    }

    # Collect tasks from each state that match this epic
    found_tasks: dict[str, list[dict]] = {state: [] for state in state_folders}
    matched_expected_ids: set[str] = set()

    for state_name, folder_name in state_folders.items():
        state_root = Path(WORKSTREAM_DIR) / folder_name
        if not state_root.exists():
            continue
        for task_file in state_root.rglob("*.md"):
            if not task_file.is_file():
                continue
            try:
                content = task_file.read_text(encoding="utf-8", errors="replace")
            except Exception:
                continue

            # Check if task belongs to this epic
            epic_meta = _extract_metadata(content, "Epic")
            source_meta = _extract_metadata(content, "Source") or _extract_metadata(content, "Source Epic Path")
            epic_meta_slug = _slugify(epic_meta) if epic_meta else ""
            source_epic_slug = _normalize_epic_reference(source_meta)

            if epic_meta_slug != epic_slug and source_epic_slug != epic_slug:
                continue

            title = _task_title_from_content(content, task_file.name)
            task_id = _extract_task_id(title)
            title_key = _normalize_task_title_for_match(title)

            # Parse retry count for failed tasks
            retry_count = 0
            if state_name == "failed":
                retry_match = re.search(r"Retry-Count:\s*(\d+)", content, re.IGNORECASE)
                retry_count = int(retry_match.group(1)) if retry_match else 0

            task_entry = {
                "path": str(task_file),
                "filename": task_file.name,
                "title": title,
                "task_id": task_id,
                "agent": _resolve_agent_name(str(task_file)),
                "retry_count": retry_count,
                "folder": str(task_file.parent.relative_to(Path(WORKSTREAM_DIR))).replace("\\", "/"),
            }
            found_tasks[state_name].append(task_entry)

            # Track which expected tasks we've found
            if task_id and task_id in expected_by_id:
                matched_expected_ids.add(task_id)
            elif title_key and title_key in expected_by_title:
                matched_expected_ids.add(title_key)

    # Find tasks not yet in any state (not started)
    not_found: list[dict] = []
    for task in expected_tasks:
        task_id = str(task.get("task_id") or "").strip().upper()
        title_key = _normalize_task_title_for_match(task.get("title"))
        if task_id not in matched_expected_ids and title_key not in matched_expected_ids:
            not_found.append(task)

    # Calculate summary
    counts = {state: len(tasks) for state, tasks in found_tasks.items()}
    counts["not_found"] = len(not_found)
    counts["expected"] = len(expected_tasks)

    total_expected = len(expected_tasks)
    completed = counts["complete"]
    delivery_pct = min(100, int((completed / total_expected * 100))) if total_expected > 0 else 0

    # Identify blocking issues
    blocking_issues = []
    if counts["failed"] > 0:
        for task in found_tasks["failed"]:
            if task["retry_count"] >= 2:
                blocking_issues.append({
                    "type": "max_retries",
                    "task": task["title"],
                    "message": f"Task '{task['title']}' has reached max retries ({task['retry_count']})",
                })
            else:
                blocking_issues.append({
                    "type": "failed_pending_retry",
                    "task": task["title"],
                    "message": f"Task '{task['title']}' failed, retry {task['retry_count'] + 1} pending",
                })
    if counts["not_found"] > 0:
        blocking_issues.append({
            "type": "not_started",
            "count": counts["not_found"],
            "message": f"{counts['not_found']} tasks not yet allocated to any agent",
        })

    return {
        "epic_slug": epic_slug,
        "epic_name": epic_name,
        "manifest_found": manifest is not None,
        "decomposed_at": manifest.get("decomposed_at") if manifest else None,
        "source_epic_path": manifest.get("source_epic_path") if manifest else None,
        "summary": {
            **counts,
            "delivery_pct": delivery_pct,
            "archived": len(archived_tasks),  # Tasks decomposed into subtasks
        },
        "original_tasks": expected_tasks,
        "archived_tasks": archived_tasks,  # Tasks that were further decomposed
        "tasks_by_status": {
            "backlog": found_tasks["backlog"],
            "in_progress": found_tasks["in_progress"],
            "review": found_tasks["review"],
            "complete": found_tasks["complete"],
            "failed": found_tasks["failed"],
            "not_found": not_found,
        },
        "blocking_issues": blocking_issues,
    }


def _update_decomposition_manifest(
    epic_slug: str,
    new_tasks: list[dict[str, Any]],
    archived_task_ids: list[str] | None = None,
    source: str = "unknown"
) -> bool:
    """Update the decomposition manifest with new tasks from augmentation or extended decomposition.

    Args:
        epic_slug: The epic slug to update
        new_tasks: List of new task dicts with keys: task_id, filename, workstream, title, suggested_agent
        archived_task_ids: Optional list of task IDs that were decomposed into subtasks (mark as archived)
        source: Source of the update (e.g., 'augment_epic', 'extend_decomposition')

    Returns:
        True if manifest was updated, False if no manifest exists
    """
    base_dir = _repo_root()
    manifest_path = base_dir / f"ep_{epic_slug}" / "decomposition_manifest.json"

    if not manifest_path.exists():
        # Create new manifest if epic folder exists but no manifest
        epic_dir = base_dir / f"ep_{epic_slug}"
        if not epic_dir.exists():
            return False
        manifest = {
            "epic_slug": epic_slug,
            "epic_name": epic_slug,
            "source_epic_path": "unknown",
            "decomposed_at": datetime.datetime.now().isoformat(),
            "total_tasks": 0,
            "workstreams": [],
            "tasks": [],
            "updates": [],
        }
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception:
            return False

    # Ensure updates array exists
    if "updates" not in manifest:
        manifest["updates"] = []

    # Add new tasks
    existing_ids = {t.get("task_id") for t in manifest.get("tasks", [])}
    added_tasks = []
    for task in new_tasks:
        task_id = task.get("task_id", "")
        if task_id and task_id not in existing_ids:
            manifest["tasks"].append({
                "task_id": task_id,
                "filename": task.get("filename", ""),
                "workstream": task.get("workstream", ""),
                "title": task.get("title", ""),
                "suggested_agent": task.get("suggested_agent", "general"),
                "added_via": source,
                "added_at": datetime.datetime.now().isoformat(),
            })
            added_tasks.append(task_id)
            existing_ids.add(task_id)

    # Mark archived tasks (decomposed into subtasks)
    if archived_task_ids:
        for task in manifest.get("tasks", []):
            if task.get("task_id") in archived_task_ids:
                task["archived"] = True
                task["archived_reason"] = "decomposed_into_subtasks"
                task["archived_at"] = datetime.datetime.now().isoformat()

    # Update totals
    active_tasks = [t for t in manifest.get("tasks", []) if not t.get("archived")]
    manifest["total_tasks"] = len(active_tasks)
    manifest["workstreams"] = list(set(t.get("workstream", "") for t in active_tasks if t.get("workstream")))

    # Log the update
    manifest["updates"].append({
        "timestamp": datetime.datetime.now().isoformat(),
        "source": source,
        "tasks_added": len(added_tasks),
        "tasks_archived": len(archived_task_ids) if archived_task_ids else 0,
        "added_task_ids": added_tasks,
        "archived_task_ids": archived_task_ids or [],
    })

    # Write updated manifest
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return True


def allocate_tasks(task_paths: list[str], target_model: str) -> dict[str, list[dict[str, str]]]:
    if target_model not in EPIC_REVIEW_MODEL_FOLDERS:
        raise ValueError(f"Unsupported model: {target_model}")
    target_dir = Path(WORKSTREAM_DIR) / "100_backlog" / target_model
    target_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        try:
            task = _parse_epic_review_task(src)
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": f"Task parse failed: {exc}"})
            continue
        if task.status_folder != "100_backlog":
            results["failed"].append(
                {
                    "path": task_path,
                    "error": f"Only 100_backlog tasks can be allocated from Epic Review (got {task.status_folder})",
                }
            )
            continue
        dest = target_dir / src.name
        try:
            if src.resolve() == dest.resolve():
                results["success"].append({"path": task_path, "dest": str(dest), "note": "Already assigned"})
                continue
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


def move_tasks_to_general_backlog(task_paths: list[str]) -> dict[str, list[dict[str, str]]]:
    target_dir = Path(WORKSTREAM_DIR) / "100_backlog" / "general"
    target_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        dest = target_dir / _retag_task_filename(src.name, "general")
        try:
            if src.resolve() == dest.resolve():
                results["success"].append({"path": task_path, "dest": str(dest), "note": "Already in general backlog"})
                continue
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


def reject_tasks(task_paths: list[str], reason: str) -> dict[str, list[dict[str, str]]]:
    failed_root = Path(WORKSTREAM_DIR) / "400_failed"
    failed_root.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        try:
            task = _parse_epic_review_task(src)
            target_dir = failed_root / task.agent if task.agent else failed_root
            target_dir.mkdir(parents=True, exist_ok=True)
            src.write_text(task.content.rstrip() + f"\n\nRejection Reason: {reason}\n", encoding="utf-8")
            dest = target_dir / src.name
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


def delete_tasks_bulk(task_paths: list[str]) -> dict[str, Any]:
    """Permanently delete multiple tasks. Only tasks in 100_backlog or 050_review can be deleted."""
    results: dict[str, Any] = {"success": True, "deleted": [], "failed": []}
    allowed_folders = {"100_backlog", "050_review"}

    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue

        # Check if task is in an allowed folder
        path_parts = str(src).replace("\\", "/").lower()
        is_allowed = any(f"/{folder}/" in path_parts or path_parts.endswith(f"/{folder}")
                        for folder in allowed_folders)

        if not is_allowed:
            results["failed"].append({"path": task_path, "error": "Only tasks in 100_backlog or 050_review can be deleted"})
            continue

        try:
            os.remove(str(src))
            results["deleted"].append({"path": task_path})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})

    if results["failed"]:
        results["success"] = False
    return results


def extend_decomposition(task_paths: list[str]) -> dict[str, Any]:
    """Run extended decomposition on selected tasks to generate more granular sub-tasks."""
    results: dict[str, Any] = {"success": True, "subtasks_created": [], "failed": [], "original_tasks_archived": []}
    base_dir = Path(WORKSTREAM_DIR).parent

    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue

        try:
            task = _parse_epic_review_task(src)
            subtasks = _run_extended_decomposition(src, task)

            # Generate sub-task files
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            target_dir = src.parent

            for seq, subtask in enumerate(subtasks):
                subtask_id = f"{task.task_id}.{seq + 1}"
                subtask["id"] = subtask_id
                subtask["source_epic_path"] = task_path
                subtask["parent_task_id"] = task.task_id

                filename = f"{timestamp}_{_slugify(subtask['title'])[:50]}_{seq}.md"
                subtask_path = target_dir / filename
                subtask_content = _generate_subtask_content(subtask, task)
                subtask_path.write_text(subtask_content, encoding="utf-8")

                results["subtasks_created"].append({
                    "path": str(subtask_path),
                    "task_id": subtask_id,
                    "title": subtask["title"],
                    "parent_task_id": task.task_id,
                })

            # Archive original task by adding decomposition note
            archive_note = f"\n\n---\n\n## Extended Decomposition\n\nThis task was decomposed into {len(subtasks)} sub-tasks on {datetime.datetime.now().isoformat()}:\n"
            for st in results["subtasks_created"][-len(subtasks):]:
                archive_note += f"- {st['task_id']}: {st['title']}\n"
            src.write_text(task.content + archive_note, encoding="utf-8")
            results["original_tasks_archived"].append(task_path)

            # Update decomposition manifest with new subtasks
            epic_slug = _slugify(task.epic) if task.epic else None
            if epic_slug:
                new_subtask_entries = [
                    {
                        "task_id": st["task_id"],
                        "filename": Path(st["path"]).name,
                        "workstream": task.workstream or "",
                        "title": st["title"],
                        "suggested_agent": "general",
                        "parent_task_id": task.task_id,
                    }
                    for st in results["subtasks_created"][-len(subtasks):]
                ]
                _update_decomposition_manifest(
                    epic_slug=epic_slug,
                    new_tasks=new_subtask_entries,
                    archived_task_ids=[task.task_id] if task.task_id else None,
                    source="extend_decomposition"
                )

        except Exception as exc:
            import traceback
            error_detail = f"{str(exc)}\n{traceback.format_exc()}"
            print(f"[Extended Decomposition Error] {error_detail}")
            results["failed"].append({"path": task_path, "error": str(exc)})

    if results["failed"]:
        results["success"] = len(results["subtasks_created"]) > 0
        # Add top-level error message for frontend
        results["error"] = "; ".join(f["error"] for f in results["failed"])
    return results


def _run_extended_decomposition(task_path: Path, task: Any) -> list[dict[str, Any]]:
    """Run LLM-based extended decomposition on a single task."""
    epic_skill_path = Path(WORKSTREAM_DIR).parent / "skills" / "epic-decomposition" / "SKILL.md"
    ui_skill_path = Path(WORKSTREAM_DIR).parent / "skills" / "ui-delivery-viewability" / "SKILL.md"

    epic_skill = epic_skill_path.read_text(encoding="utf-8") if epic_skill_path.exists() else ""
    ui_skill = ui_skill_path.read_text(encoding="utf-8") if ui_skill_path.exists() else ""

    prompt = f"""You are performing EXTENDED DECOMPOSITION on an existing task.

The goal is to break this task into 3-5 MORE GRANULAR sub-tasks that are:
1. Independently implementable in a single session
2. Have concrete, verifiable outputs
3. Small enough to be completed without further decomposition

CRITICAL: Think deeply about WHY this task needs subdivision:
- Identify the distinct implementation steps
- Consider dependencies between sub-components
- Ensure each sub-task has clear boundaries

Original Task Content:
```markdown
{task.content}
```

Epic Decomposition Skill (for structure guidance):
{epic_skill[:2000] if epic_skill else "Not available"}

UI Delivery Skill (apply only if task involves UI):
{ui_skill[:1000] if ui_skill else "Not available"}

Output JSON array of sub-tasks with this structure:
{{
  "reasoning": "Why this task needs subdivision and how you broke it down",
  "subtasks": [
    {{
      "title": "Concise sub-task title",
      "purpose": "What this sub-task accomplishes",
      "input": "What's needed to start",
      "output": "Concrete deliverable",
      "action": "Step-by-step implementation",
      "verification": ["Checklist item 1", "Checklist item 2", "Checklist item 3"],
      "priority": 1,
      "ui_viewability": false
    }}
  ]
}}

Generate 3-5 sub-tasks. Each must be independently completable.
"""

    # Use codex CLI for decomposition
    codex_bin = (
        shutil.which("codex")
        or shutil.which("codex.cmd")
        or shutil.which("codex.exe")
        or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")
    )

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "reasoning": {"type": "string"},
            "subtasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "title": {"type": "string"},
                        "purpose": {"type": "string"},
                        "input": {"type": "string"},
                        "output": {"type": "string"},
                        "action": {"type": "string"},
                        "verification": {"type": "array", "items": {"type": "string"}},
                        "priority": {"type": "integer"},
                        "ui_viewability": {"type": "boolean"}
                    },
                    "required": ["title", "purpose", "input", "output", "action", "verification", "priority", "ui_viewability"]
                }
            }
        },
        "required": ["reasoning", "subtasks"]
    }

    scratch_dir = Path(WORKSTREAM_DIR) / "artefacts" / f"extend_decomp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    scratch_dir.mkdir(parents=True, exist_ok=True)
    schema_path = scratch_dir / "schema.json"
    output_path = scratch_dir / "output.json"
    schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")

    cmd = [
        codex_bin, "exec",
        "--skip-git-repo-check",
        "--sandbox", "read-only",
        "--output-schema", str(schema_path),
        "-o", str(output_path),
        "-C", str(Path(WORKSTREAM_DIR).parent),
        "-"
    ]

    print(f"[Extended Decomposition] Running command: {' '.join(cmd)}")
    print(f"[Extended Decomposition] Codex binary: {codex_bin}")
    print(f"[Extended Decomposition] Schema path: {schema_path}")
    print(f"[Extended Decomposition] Output path: {output_path}")

    try:
        proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)
    except subprocess.TimeoutExpired:
        raise RuntimeError("Extended decomposition timed out after 120 seconds")
    except FileNotFoundError as e:
        raise RuntimeError(f"Codex CLI not found at {codex_bin}: {e}")

    print(f"[Extended Decomposition] Return code: {proc.returncode}")
    print(f"[Extended Decomposition] Stdout: {(proc.stdout or '')[:500]}")
    print(f"[Extended Decomposition] Stderr: {(proc.stderr or '')[:500]}")

    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Codex failed (rc={proc.returncode}): {err[-1000:]}")

    if not output_path.exists():
        raise RuntimeError("Extended decomposition did not produce output")

    result = json.loads(output_path.read_text(encoding="utf-8"))
    return result.get("subtasks", [])


def _generate_subtask_content(subtask: dict[str, Any], parent_task: Any) -> str:
    """Generate markdown content for a sub-task."""
    lines = [
        f"# SUB-TASK {subtask['id']}: {subtask['title']}",
        "",
        f"**Parent Task:** {parent_task.task_id}",
        f"**Workstream:** {parent_task.workstream}",
        f"**Priority:** {subtask.get('priority', 2)}",
        f"**Source:** {subtask.get('source_epic_path', 'Extended decomposition')}",
        f"**UI Deliverable:** {'Yes' if subtask.get('ui_viewability') else 'No'}",
        "**Status:** [ ] Not Started",
        "",
        "---",
        "",
        "## Purpose",
        "",
        subtask.get("purpose", ""),
        "",
        "## Input",
        "",
        subtask.get("input", ""),
        "",
        "## Output",
        "",
        subtask.get("output", ""),
        "",
        "## Action",
        "",
        subtask.get("action", ""),
        "",
        "## Verification",
        "",
    ]
    for item in subtask.get("verification", []):
        lines.append(f"- [ ] {item}")
    lines.extend([
        "",
        "---",
        "",
        "## Notes",
        "",
        f"- Generated via extended decomposition from parent task: `{parent_task.task_id}`",
        "- This sub-task should be independently implementable.",
    ])
    return "\n".join(lines) + "\n"


def _model_status() -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for model in EPIC_REVIEW_MODEL_FOLDERS:
        folder = Path(WORKSTREAM_DIR) / "100_backlog" / model
        count = len(list(folder.glob("*.md"))) if folder.exists() else 0
        output.append({"model": model, "count": count})
    return output


def _list_epics_with_solutions() -> list[dict[str, Any]]:
    """List epics that have solution folders (ep_*)."""
    base_dir = Path(WORKSTREAM_DIR).parent  # C:/Users/edebe/eds
    epics = []

    # Find all ep_* folders
    for folder in base_dir.iterdir():
        if folder.is_dir() and folder.name.startswith("ep_"):
            solution_path = folder / "solution"
            if solution_path.exists() and solution_path.is_dir():
                # Count files in solution
                file_count = sum(1 for _ in solution_path.rglob("*") if _.is_file())
                if file_count > 0:
                    epic_slug = folder.name[3:]
                    epic_name = epic_slug.replace("_", " ").title()
                    recon = get_epic_full_reconciliation(epic_slug)
                    summary = recon.get("summary", {})
                    epics.append({
                        "slug": epic_slug,
                        "name": epic_name,
                        "solution_path": str(folder.relative_to(base_dir)).replace("\\", "/"),
                        "file_count": file_count,
                        "progress_pct": summary.get("delivery_pct", 0),
                        "expected_count": summary.get("expected", 0),
                        "complete_count": summary.get("complete", 0),
                        "in_progress_count": summary.get("in_progress", 0),
                        "backlog_count": summary.get("backlog", 0),
                        "review_count": summary.get("review", 0),
                        "failed_count": summary.get("failed", 0),
                    })

    return sorted(epics, key=lambda x: (-int(x.get("progress_pct", 0)), x["name"]))


def _analyze_solution_folder(solution_path: str) -> dict[str, Any]:
    """Analyze an existing solution folder to understand its structure."""
    base_dir = Path(WORKSTREAM_DIR).parent
    full_path = base_dir / solution_path

    if not full_path.exists():
        return {"error": f"Path not found: {solution_path}"}

    analysis = {
        "total_files": 0,
        "total_dirs": 0,
        "has_backend": False,
        "has_frontend": False,
        "has_tests": False,
        "has_infra": False,
        "has_docs": False,
        "backend_details": "",
        "frontend_details": "",
        "test_details": "",
        "infra_details": "",
        "key_files": []
    }

    # Count files and directories
    all_files = []
    for item in full_path.rglob("*"):
        if item.is_file():
            analysis["total_files"] += 1
            rel_path = str(item.relative_to(full_path)).replace("\\", "/")
            all_files.append(rel_path)
        elif item.is_dir():
            analysis["total_dirs"] += 1

    # Detect backend
    backend_indicators = ["backend", "server", "api", "src/app.js", "src/index.js", "main.py", "app.py"]
    for indicator in backend_indicators:
        if any(indicator in f.lower() for f in all_files) or (full_path / "solution" / "backend").exists() or (full_path / "backend").exists():
            analysis["has_backend"] = True
            # Try to detect framework
            if any("express" in f.lower() or "app.js" in f.lower() for f in all_files):
                analysis["backend_details"] = "Express/Node.js API"
            elif any("fastapi" in f.lower() or "uvicorn" in f.lower() for f in all_files):
                analysis["backend_details"] = "FastAPI/Python"
            elif any("flask" in f.lower() for f in all_files):
                analysis["backend_details"] = "Flask/Python"
            else:
                analysis["backend_details"] = "Backend API"
            break

    # Detect frontend
    frontend_indicators = ["frontend", "src/pages", "src/components", "public/index.html", "vite.config", "next.config", "App.jsx", "App.tsx"]
    for indicator in frontend_indicators:
        if any(indicator in f for f in all_files) or (full_path / "solution" / "frontend").exists() or (full_path / "frontend").exists():
            analysis["has_frontend"] = True
            if any("react" in f.lower() or ".jsx" in f.lower() or ".tsx" in f.lower() for f in all_files):
                analysis["frontend_details"] = "React application"
            elif any("vue" in f.lower() for f in all_files):
                analysis["frontend_details"] = "Vue application"
            else:
                analysis["frontend_details"] = "Web UI"
            break

    # Detect tests
    test_indicators = ["test", "tests", "spec", "__tests__", ".test.", ".spec."]
    if any(any(indicator in f.lower() for indicator in test_indicators) for f in all_files):
        analysis["has_tests"] = True
        test_files = [f for f in all_files if any(indicator in f.lower() for indicator in test_indicators)]
        analysis["test_details"] = f"{len(test_files)} test file(s)"

    # Detect infrastructure
    infra_indicators = ["docker", "Dockerfile", "docker-compose", "setup.sh", "setup.bat", ".env.example", "Makefile"]
    if any(any(indicator in f for indicator in infra_indicators) for f in all_files):
        analysis["has_infra"] = True
        if any("docker" in f.lower() for f in all_files):
            analysis["infra_details"] = "Docker configuration"
        elif any("setup" in f.lower() for f in all_files):
            analysis["infra_details"] = "Setup scripts"
        else:
            analysis["infra_details"] = "Infrastructure files"

    # Detect documentation
    doc_indicators = ["README", "docs/", "CHANGELOG", "API.md", "CONTRIBUTING"]
    if any(any(indicator in f for indicator in doc_indicators) for f in all_files):
        analysis["has_docs"] = True

    # Key files (important files to reference)
    key_patterns = ["package.json", "requirements.txt", "schema.sql", "app.js", "index.js", "main.py", "routes", "models", "controllers"]
    analysis["key_files"] = sorted([f for f in all_files if any(p in f for p in key_patterns)])[:20]

    return analysis


def augment_epic(epic_slug: str, solution_path: str, augment_types: list[str], feature_description: str = "") -> dict[str, Any]:
    """Generate augmentation tasks for an existing epic solution."""
    base_dir = Path(WORKSTREAM_DIR).parent
    full_solution_path = base_dir / solution_path

    if not full_solution_path.exists():
        return {"success": False, "error": f"Solution path not found: {solution_path}", "tasks_created": []}

    # Analyze the existing solution
    analysis = _analyze_solution_folder(solution_path)

    # Build context about existing solution
    existing_files = []
    for item in full_solution_path.rglob("*"):
        if item.is_file() and not any(skip in str(item) for skip in ["node_modules", ".git", "__pycache__", ".venv"]):
            rel_path = str(item.relative_to(full_solution_path)).replace("\\", "/")
            existing_files.append(rel_path)

    # Read key files for context
    key_file_contents = {}
    key_files_to_read = ["package.json", "requirements.txt", "src/app.js", "schema.sql"]
    for key_file in key_files_to_read:
        key_path = full_solution_path / "solution" / "backend" / key_file
        if not key_path.exists():
            key_path = full_solution_path / key_file
        if key_path.exists():
            try:
                content = key_path.read_text(encoding="utf-8", errors="replace")
                key_file_contents[key_file] = content[:2000]  # Limit size
            except:
                pass

    # Run augmentation via LLM
    tasks_created = _run_augmentation_llm(
        epic_slug=epic_slug,
        solution_path=solution_path,
        analysis=analysis,
        existing_files=existing_files[:100],  # Limit for prompt size
        key_file_contents=key_file_contents,
        augment_types=augment_types,
        feature_description=feature_description
    )

    # Update decomposition manifest with augmented tasks
    if tasks_created:
        augment_task_entries = [
            {
                "task_id": t.get("task_id", ""),
                "filename": t.get("filename", ""),
                "workstream": "AUG",  # Augmentation workstream
                "title": t.get("title", ""),
                "suggested_agent": "general",
                "augment_types": augment_types,
            }
            for t in tasks_created
        ]
        _update_decomposition_manifest(
            epic_slug=epic_slug,
            new_tasks=augment_task_entries,
            archived_task_ids=None,
            source=f"augment_epic:{','.join(augment_types)}"
        )

    return {
        "success": True,
        "tasks_created": tasks_created,
        "augment_types": augment_types
    }


def _run_augmentation_llm(
    epic_slug: str,
    solution_path: str,
    analysis: dict[str, Any],
    existing_files: list[str],
    key_file_contents: dict[str, str],
    augment_types: list[str],
    feature_description: str
) -> list[dict[str, Any]]:
    """Run LLM to generate augmentation tasks."""

    # Build augmentation description
    augment_desc_parts = []
    if "ui" in augment_types:
        augment_desc_parts.append("- **UI/Frontend**: Create React + Vite frontend that integrates with existing backend APIs")
    if "tests" in augment_types:
        augment_desc_parts.append("- **Tests**: Create test suite (unit tests, integration tests) for existing code")
    if "docs" in augment_types:
        augment_desc_parts.append("- **Documentation**: Create README, API documentation, usage guides")
    if "infra" in augment_types:
        augment_desc_parts.append("- **Infrastructure**: Create setup scripts, Docker configuration, CI/CD")
    if "feature" in augment_types and feature_description:
        augment_desc_parts.append(f"- **New Feature**: {feature_description}")

    augment_desc = "\n".join(augment_desc_parts)

    # Build existing solution summary
    files_summary = "\n".join(f"  - {f}" for f in existing_files[:50])

    key_files_summary = ""
    for filename, content in key_file_contents.items():
        key_files_summary += f"\n### {filename}\n```\n{content[:1000]}\n```\n"

    prompt = f"""You are generating AUGMENTATION TASKS for an existing epic solution.

## Existing Solution Context

**Epic:** {epic_slug}
**Solution Path:** {solution_path}

### Current Solution Analysis
- Total Files: {analysis.get('total_files', 0)}
- Has Backend: {analysis.get('has_backend', False)} ({analysis.get('backend_details', '')})
- Has Frontend: {analysis.get('has_frontend', False)} ({analysis.get('frontend_details', '')})
- Has Tests: {analysis.get('has_tests', False)} ({analysis.get('test_details', '')})
- Has Infrastructure: {analysis.get('has_infra', False)} ({analysis.get('infra_details', '')})

### Existing Files (sample)
{files_summary}

{key_files_summary}

## Augmentation Request

Generate tasks to ADD the following to the existing solution:
{augment_desc}

## Requirements

1. Tasks MUST reference existing files and APIs from the solution
2. Tasks MUST build ON TOP OF the existing codebase, not replace it
3. New code should be placed in appropriate subdirectories:
   - UI: `{solution_path}/solution/frontend/`
   - Tests: `{solution_path}/solution/backend/tests/` or `{solution_path}/solution/frontend/tests/`
   - Docs: `{solution_path}/` (README.md, docs/)
   - Infrastructure: `{solution_path}/` (setup.sh, docker-compose.yml, etc.)
4. Include specific file paths, API endpoints to consume, and integration points
5. Each task should be independently implementable

Generate 3-8 tasks depending on complexity.
"""

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "reasoning": {"type": "string"},
            "tasks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": "string"},
                        "title": {"type": "string"},
                        "workstream_letter": {"type": "string"},
                        "workstream_name": {"type": "string"},
                        "purpose": {"type": "string"},
                        "input": {"type": "string"},
                        "output": {"type": "string"},
                        "action": {"type": "string"},
                        "verification": {"type": "array", "items": {"type": "string"}},
                        "existing_files_to_reference": {"type": "array", "items": {"type": "string"}},
                        "new_files_to_create": {"type": "array", "items": {"type": "string"}},
                        "priority": {"type": "integer"}
                    },
                    "required": ["id", "title", "workstream_letter", "workstream_name", "purpose", "input", "output", "action", "verification", "existing_files_to_reference", "new_files_to_create", "priority"]
                }
            }
        },
        "required": ["reasoning", "tasks"]
    }

    # Run codex CLI
    import shutil
    import tempfile

    codex_bin = (
        shutil.which("codex")
        or shutil.which("codex.cmd")
        or shutil.which("codex.exe")
        or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        schema_path = Path(tmp_dir) / "schema.json"
        output_path = Path(tmp_dir) / "output.json"

        schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")

        cmd = [
            codex_bin,
            "exec",
            "--skip-git-repo-check",
            "--sandbox", "read-only",
            "--output-schema", str(schema_path),
            "-o", str(output_path),
            "-C", str(Path(WORKSTREAM_DIR).parent),
            "-"
        ]

        try:
            proc = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError("Augmentation timed out after 180 seconds")

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip()
            raise RuntimeError(f"Augmentation failed (rc={proc.returncode}): {err[-2000:]}")

        if not output_path.exists():
            raise RuntimeError("Augmentation did not produce output")

        payload = json.loads(output_path.read_text(encoding="utf-8"))

    # Generate task files
    tasks_created = []
    timestamp_base = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for idx, task in enumerate(payload.get("tasks", [])):
        task_id = task.get("id", f"AUG{idx+1}")

        # Generate task file content
        content_lines = [
            f"# TASK {task_id}: {task.get('title', 'Untitled')}",
            "",
            f"**Workstream:** {task.get('workstream_letter', 'X')} - {task.get('workstream_name', 'AUGMENTATION')}",
            f"**Epic:** {epic_slug}",
            f"**Source:** Augmentation of existing solution at `{solution_path}`",
            f"**Priority:** {task.get('priority', 2)}",
            "**Status:** [ ] Not Started",
            "",
            "---",
            "",
            "## Purpose",
            "",
            task.get("purpose", ""),
            "",
            "## Input",
            "",
            task.get("input", ""),
            "",
            "## Output",
            "",
            task.get("output", ""),
            "",
        ]

        # Add existing files to reference
        existing_refs = task.get("existing_files_to_reference", [])
        if existing_refs:
            content_lines.extend([
                "## Existing Files to Reference",
                "",
            ])
            for ref in existing_refs:
                content_lines.append(f"- `{ref}`")
            content_lines.append("")

        # Add new files to create
        new_files = task.get("new_files_to_create", [])
        if new_files:
            content_lines.extend([
                "## New Files to Create",
                "",
            ])
            for nf in new_files:
                content_lines.append(f"- `{nf}`")
            content_lines.append("")

        content_lines.extend([
            "## Action",
            "",
            task.get("action", ""),
            "",
            "## Verification",
            "",
        ])
        for v in task.get("verification", []):
            content_lines.append(f"- [ ] {v}")

        content_lines.extend([
            "",
            "---",
            "",
            "## Notes",
            "",
            f"- Generated via epic augmentation on {datetime.datetime.now().isoformat()}",
            f"- Builds on existing solution: `{solution_path}`",
        ])

        content = "\n".join(content_lines) + "\n"

        # Generate filename
        task_slug = "_".join(task.get("title", "task").lower().split()[:5])
        task_slug = "".join(c if c.isalnum() or c == "_" else "_" for c in task_slug)
        filename = f"{timestamp_base}_{epic_slug}_augment_{task_slug}.md"

        # Write to 100_backlog/general
        output_dir = Path(WORKSTREAM_DIR) / "100_backlog" / "general"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename
        output_path.write_text(content, encoding="utf-8")

        tasks_created.append({
            "task_id": task_id,
            "title": task.get("title", "Untitled"),
            "path": str(output_path),
            "filename": filename
        })

    return tasks_created


def bulk_allocate_by_workstream(epic_slug: str, allocation_map: dict[str, str]) -> dict[str, list[Any]]:
    tasks = get_epic_tasks(epic_slug)
    results: dict[str, list[Any]] = {model: [] for model in EPIC_REVIEW_MODEL_FOLDERS}
    results["unallocated"] = []
    for task in tasks:
        letter = task["workstream_group"]
        target_model = allocation_map.get(letter)
        if target_model in EPIC_REVIEW_MODEL_FOLDERS:
            result = allocate_tasks([task["path"]], target_model)
            results[target_model].extend(result["success"])
        else:
            results["unallocated"].append(task["path"])
    return results


# ============================================================================
# EPIC DECOMPOSITION FUNCTIONS
# ============================================================================

def _parse_epic_workstreams(content: str) -> list[dict[str, Any]]:
    """Extract workstreams from epic document."""
    ws_pattern = r"^(#+)\s*WORKSTREAM\s+([A-Z])\s*[—–-]\s*(.+)$"
    workstreams = []
    lines = content.split('\n')
    current_ws = None
    current_content = []

    for i, line in enumerate(lines):
        match = re.match(ws_pattern, line, re.IGNORECASE)
        if match:
            if current_ws:
                current_ws['content'] = '\n'.join(current_content)
                workstreams.append(current_ws)
            current_ws = {
                'letter': match.group(2).upper(),
                'name': match.group(3).strip(),
                'tasks': []
            }
            current_content = []
        elif current_ws:
            current_content.append(line)

    if current_ws:
        current_ws['content'] = '\n'.join(current_content)
        workstreams.append(current_ws)

    # Parse tasks within each workstream
    for ws in workstreams:
        ws['tasks'] = _parse_workstream_tasks(ws['content'], ws['letter'])

    return workstreams


def _parse_workstream_tasks(content: str, ws_letter: str) -> list[dict[str, Any]]:
    """Extract tasks from a workstream section."""
    task_pattern = r"^(#+)\s*TASK\s+([A-Z]\d+)\s+(.+)$"
    tasks = []
    lines = content.split('\n')
    current_task = None
    current_content = []

    for line in lines:
        match = re.match(task_pattern, line, re.IGNORECASE)
        if match:
            if current_task:
                _populate_task_fields(current_task, '\n'.join(current_content))
                tasks.append(current_task)
            current_task = {
                'id': match.group(2).upper(),
                'title': match.group(3).strip(),
                'workstream': ws_letter
            }
            current_content = []
        elif current_task:
            current_content.append(line)

    if current_task:
        _populate_task_fields(current_task, '\n'.join(current_content))
        tasks.append(current_task)

    return tasks


def _populate_task_fields(task: dict, content: str) -> None:
    """Extract Purpose, Input, Output, Fields, Action, Verification from task content."""
    task['purpose'] = _extract_heading_section(content, 'Purpose') or ''
    task['input'] = _extract_heading_section(content, 'Input') or ''
    task['output'] = _extract_heading_section(content, 'Output') or ''
    task['fields'] = _extract_heading_section(content, 'Fields') or ''
    task['action'] = _extract_heading_section(content, 'Action') or ''
    task['verification'] = _extract_heading_section(content, 'Verification') or ''


def _generate_task_filename(timestamp_base: str, epic_slug: str, ws_letter: str, task_name: str, seq: int) -> str:
    """Generate filename: {yyyymmdd}_{hhmmss}_{epic}_workstream{X}_{task}.md"""
    base_dt = datetime.datetime.strptime(timestamp_base, "%Y%m%d_%H%M%S")
    adjusted_ts = (base_dt + datetime.timedelta(seconds=seq)).strftime("%Y%m%d_%H%M%S")

    # Clean task name to snake_case
    task_slug = re.sub(r'[^a-z0-9]+', '_', task_name.lower()).strip('_')

    return f"{adjusted_ts}_{epic_slug}_workstream{ws_letter}_{task_slug}.md"


def _build_epic_decompose_command(epic_path: Path) -> list[str]:
    cmd_tpl = os.environ.get("KANBAN_EPIC_DECOMP_CMD", "").strip()
    if cmd_tpl:
        formatted = cmd_tpl.format(
            epic_path=str(epic_path),
            epic_file=epic_path.name,
            repo_root=str(Path(WORKSTREAM_DIR).parent),
        )
        return shlex.split(formatted, posix=False)
    return [sys.executable, str(EPIC_DECOMPOSE_CLI_PATH), "--input", str(epic_path)]


def _normalize_verification_lines(task: dict[str, Any]) -> list[str]:
    verification = [str(item).strip() for item in task.get("verification") or [] if str(item).strip()]
    if task.get("ui_viewability"):
        ui_requirements = [
            "Provide or update a simple local access/start script that prints the localhost URL for this UI.",
            "Smoke-test the local startup path and confirm the UI loads without an immediate crash.",
            "Capture screenshot evidence of the working UI in the epic verification folder.",
        ]
        existing = {item.lower() for item in verification}
        for requirement in ui_requirements:
            if requirement.lower() not in existing:
                verification.append(requirement)
    if len(verification) < 2:
        verification.extend(
            [
                "Implementation aligns with the epic scope for this deliverable.",
                "Validation evidence is captured for Epic Review and downstream execution.",
            ][: 2 - len(verification)]
        )
    return verification


def _validate_epic_decomposition_payload(payload: dict[str, Any], source_relpath: str) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Epic decomposition payload must be an object.")
    epic_name = str(payload.get("epic_name") or "").strip()
    epic_slug = str(payload.get("epic_slug") or "").strip()
    tasks = payload.get("tasks")
    if not epic_name or not epic_slug:
        raise ValueError("Epic decomposition payload missing epic_name or epic_slug.")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Epic decomposition payload missing tasks.")
    normalized_tasks: list[dict[str, Any]] = []
    for idx, item in enumerate(tasks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Task {idx} is not an object.")
        title = str(item.get("title") or "").strip()
        task_id = str(item.get("id") or "").strip()
        workstream_letter = (str(item.get("workstream_letter") or "G").strip() or "G")[0].upper()
        workstream_name = str(item.get("workstream_name") or f"Workstream {workstream_letter}").strip()
        purpose = str(item.get("purpose") or "").strip()
        input_text = str(item.get("input") or "").strip()
        output_text = str(item.get("output") or "").strip()
        if not title or not task_id or not purpose or not input_text or not output_text:
            raise ValueError(f"Task {idx} missing required fields.")
        priority = item.get("priority", 2)
        try:
            priority = int(priority)
        except Exception:
            priority = 2
        if priority not in {1, 2, 3}:
            priority = 2
        normalized_tasks.append(
            {
                "id": task_id,
                "title": title,
                "workstream_letter": workstream_letter,
                "workstream_name": workstream_name,
                "workstream_goal": str(item.get("workstream_goal") or "").strip(),
                "purpose": purpose,
                "input": input_text,
                "output": output_text,
                "fields": [str(v).strip() for v in item.get("fields") or [] if str(v).strip()],
                "action": str(item.get("action") or "").strip(),
                "verification": _normalize_verification_lines(item),
                "priority": priority,
                "dependencies": [str(v).strip() for v in item.get("dependencies") or [] if str(v).strip()],
                "suggested_agent": str(item.get("suggested_agent") or "").strip().lower(),
                "ui_viewability": bool(item.get("ui_viewability", False)),
                "source_epic_path": source_relpath,
            }
        )
    return {
        "epic_name": epic_name,
        "epic_slug": epic_slug,
        "summary": str(payload.get("summary") or "").strip(),
        "warnings": [str(v).strip() for v in payload.get("warnings") or [] if str(v).strip()],
        "tasks": normalized_tasks,
    }


def _run_epic_decomposition(epic_path: Path, source_relpath: str) -> dict[str, Any]:
    if not EPIC_DECOMPOSE_CLI_PATH.exists():
        raise FileNotFoundError(f"Epic decomposition CLI not found: {EPIC_DECOMPOSE_CLI_PATH}")
    cmd = _build_epic_decompose_command(epic_path)
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Epic decomposition failed (rc={proc.returncode}): {err[-2000:]}")
    raw = (proc.stdout or "").strip()
    if not raw:
        raise RuntimeError("Epic decomposition returned empty stdout.")
    payload = json.loads(raw)
    normalized = _validate_epic_decomposition_payload(payload, source_relpath)
    normalized["command"] = cmd
    return normalized


def _generate_task_content(task: dict[str, Any], epic_name: str) -> str:
    lines = [
        f"# TASK {task['id']}: {task['title']}",
        "",
        f"**Workstream:** {task['workstream_letter']} — {task['workstream_name']}",
        f"**Epic:** {epic_name}",
        f"**Priority:** {task['priority']}",
        f"**Source Epic Path:** {task['source_epic_path']}",
        f"**Epic Output Folder:** {task.get('epic_output_folder') or 'N/A'}",
        f"**Suggested Agent:** {task.get('suggested_agent') or 'general'}",
        f"**UI Deliverable:** {'Yes' if task.get('ui_viewability') else 'No'}",
        "**Status:** [ ] Not Started",
    ]
    if task.get("workstream_goal"):
        lines.append(f"**Workstream Goal:** {task['workstream_goal']}")
    lines.extend(
        [
            "",
            "---",
            "",
            "## Purpose",
            "",
            task["purpose"],
            "",
            "## Input",
            "",
            task["input"],
            "",
            "## Output",
            "",
            task["output"],
        ]
    )
    if task.get("fields"):
        lines.extend(["", "## Fields / Components", ""])
        lines.extend(f"- {field}" for field in task["fields"])
    if task.get("dependencies"):
        lines.extend(["", "## Dependencies", ""])
        lines.extend(f"- {dependency}" for dependency in task["dependencies"])
    if task.get("action"):
        lines.extend(["", "## Action", "", task["action"]])
    lines.extend(["", "## Verification", ""])
    lines.extend(f"- [ ] {item}" for item in task["verification"])
    lines.extend(
        [
            "",
            "---",
            "",
            "## Notes",
            "",
            f"- Generated from source epic: `{task['source_epic_path']}`",
            "- This task is intended for Epic Review allocation before execution.",
        ]
    )
    if task.get("ui_viewability"):
        lines.append("- UI delivery requirements were expanded per `skills/ui-delivery-viewability/SKILL.md`.")
    return "\n".join(lines).strip() + "\n"


def decompose_epic_preview(epic_path: str, agent_assignments: dict[str, str]) -> dict[str, Any]:
    base_dir = Path(WORKSTREAM_DIR).parent
    file_path = (base_dir / epic_path).resolve()
    if not file_path.exists():
        return {"error": "Epic file not found", "task_count": 0}
    source_relpath = str(file_path.relative_to(base_dir)).replace("\\", "/")
    result = _run_epic_decomposition(file_path, source_relpath)
    grouped: dict[str, dict[str, Any]] = {}
    for task in result["tasks"]:
        entry = grouped.setdefault(
            task["workstream_letter"],
            {"letter": task["workstream_letter"], "name": task["workstream_name"], "task_count": 0},
        )
        entry["task_count"] += 1
    return {
        "task_count": len(result["tasks"]),
        "workstreams": sorted(grouped.values(), key=lambda item: item["letter"]),
        "summary": result.get("summary", ""),
        "warnings": result.get("warnings", []),
        "epic_name": result["epic_name"],
        "epic_slug": result["epic_slug"],
    }


def decompose_epic(epic_path: str, agent_assignments: dict[str, str] | None = None, destination_folder: str | None = None) -> dict[str, Any]:
    base_dir = _repo_root()
    file_path = (base_dir / epic_path).resolve()
    if not file_path.exists():
        return {"success": False, "error": "Epic file not found", "tasks_created": []}
    source_relpath = str(file_path.relative_to(base_dir)).replace("\\", "/")
    result = _run_epic_decomposition(file_path, source_relpath)
    timestamp_base = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Create ep_{epic_slug}/ folder structure for implementation outputs
    epic_output_dir = base_dir / f"ep_{result['epic_slug']}"
    epic_output_dir.mkdir(parents=True, exist_ok=True)
    (epic_output_dir / "solution").mkdir(exist_ok=True)
    (epic_output_dir / "verification").mkdir(exist_ok=True)
    (epic_output_dir / "deploy").mkdir(exist_ok=True)
    (epic_output_dir / "workstreams").mkdir(exist_ok=True)

    # Create workstream subfolders
    workstream_letters = set(task["workstream_letter"] for task in result["tasks"])
    for letter in workstream_letters:
        (epic_output_dir / "workstreams" / letter.upper()).mkdir(exist_ok=True)

    destination_rel = str(destination_folder or "workstream/100_backlog").strip()
    target_dir = _resolve_repo_path(destination_rel)
    target_dir.mkdir(parents=True, exist_ok=True)
    tasks_created = []
    for seq, task in enumerate(result["tasks"]):
        # Add epic output folder path to task metadata
        task["epic_output_folder"] = str(epic_output_dir)
        filename = _generate_task_filename(
            timestamp_base,
            result["epic_slug"],
            task["workstream_letter"],
            task["title"],
            seq,
        )
        task_path = target_dir / filename
        task_path.write_text(_generate_task_content(task, result["epic_name"]), encoding="utf-8")
        tasks_created.append(
            {
                "filename": filename,
                "path": str(task_path),
                "workstream": task["workstream_letter"],
                "task_id": task["id"],
                "suggested_agent": task.get("suggested_agent") or "general",
                "ui_viewability": task.get("ui_viewability", False),
            }
        )

    # Create decomposition manifest to track original task list for reconciliation
    manifest = {
        "epic_slug": result["epic_slug"],
        "epic_name": result["epic_name"],
        "source_epic_path": source_relpath,
        "decomposed_at": datetime.datetime.now().isoformat(),
        "total_tasks": len(tasks_created),
        "workstreams": list(workstream_letters),
        "tasks": [
            {
                "task_id": t["task_id"],
                "filename": t["filename"],
                "workstream": t["workstream"],
                "suggested_agent": t["suggested_agent"],
                "title": next((task["title"] for task in result["tasks"] if task["id"] == t["task_id"]), t["filename"]),
            }
            for t in tasks_created
        ],
    }
    manifest_path = epic_output_dir / "decomposition_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    return {
        "success": True,
        "tasks_created": tasks_created,
        "epic_slug": result["epic_slug"],
        "epic_name": result["epic_name"],
        "epic_output_folder": str(epic_output_dir),
        "manifest_path": str(manifest_path),
        "destination_folder": str(target_dir.relative_to(base_dir)).replace("\\", "/"),
        "summary": result.get("summary", ""),
        "warnings": result.get("warnings", []),
    }


def _send_json(handler: BaseHTTPRequestHandler, status: int, payload: Any) -> None:
    handler.send_response(status)
    handler.send_header("Content-type", "application/json")
    handler.end_headers()
    handler.wfile.write(_json_bytes(payload))

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class KanbanHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass # Suppress logging to keep console clean

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            rendered_html = HTML_PAGE.replace('##TICKER_SCROLL_SPEED##', str(TICKER_SCROLL_SPEED_SECONDS))
            self.wfile.write(rendered_html.encode('utf-8'))

        elif self.path == '/epic-review' or self.path.startswith('/epic-review?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(_render_epic_review_html().encode('utf-8'))

        elif self.path == '/epic-decomposition' or self.path.startswith('/epic-decomposition?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(_render_epic_decomposition_html().encode('utf-8'))

        elif self.path == '/epic-reconciliation' or self.path.startswith('/epic-reconciliation?'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(_render_epic_reconciliation_html().encode('utf-8'))

        elif self.path == '/api/epics' or self.path.startswith('/api/epics?'):
            parsed = urlparse(self.path)
            params = parse_qs(parsed.query)
            folder_path = params.get("folder", [None])[0]
            mode = params.get("mode", [None])[0]
            normalized_folder = (folder_path or "").replace("\\", "/").lower()
            if mode == "documents" or normalized_folder.startswith("workstream/000_epic"):
                _send_json(self, 200, {"epics": _list_epic_documents(folder_path or "workstream/000_epic")})
            else:
                _send_json(self, 200, {"epics": _list_epics(folder_path)})

        elif re.match(r"^/api/epics/[^/]+/tasks(?:\?.*)?$", self.path):
            parsed = urlparse(self.path)
            epic_slug = parsed.path.split("/")[3]
            params = parse_qs(parsed.query)
            priority_raw = params.get("priority", [None])[0]
            try:
                priority = int(priority_raw) if priority_raw else None
            except ValueError:
                priority = None
            _send_json(
                self,
                200,
                {
                    "tasks": get_epic_tasks(
                        epic_slug=epic_slug,
                        workstream=params.get("workstream", [None])[0],
                        status=params.get("status", [None])[0],
                        priority=priority,
                        sort_by=params.get("sort_by", ["priority"])[0],
                        folder_path=params.get("folder", [None])[0],
                    )
                },
            )

        elif re.match(r"^/api/epics/[^/]+/delivery-reconciliation(?:\?.*)?$", self.path):
            parsed = urlparse(self.path)
            epic_slug = parsed.path.split("/")[3]
            _send_json(self, 200, get_epic_delivery_reconciliation(epic_slug))

        elif re.match(r"^/api/epics/[^/]+/full-reconciliation(?:\?.*)?$", self.path):
            # Full reconciliation showing task status across ALL workflow states
            parsed = urlparse(self.path)
            epic_slug = parsed.path.split("/")[3]
            _send_json(self, 200, get_epic_full_reconciliation(epic_slug))

        elif self.path == '/api/models/status':
            _send_json(self, 200, {"models": _model_status()})

        elif self.path == '/api/epics/with-solutions':
            # List epics that have solution folders (ep_*)
            try:
                epics_with_solutions = _list_epics_with_solutions()
                _send_json(self, 200, {"epics": epics_with_solutions})
            except Exception as e:
                _send_json(self, 500, {"error": str(e), "epics": []})

        elif self.path.startswith('/api/analyze-solution'):
            # Analyze an existing solution folder structure
            query_components = parse_qs(urlparse(self.path).query)
            solution_path = query_components.get('path', [''])[0]
            try:
                analysis = _analyze_solution_folder(solution_path)
                _send_json(self, 200, {"analysis": analysis})
            except Exception as e:
                _send_json(self, 500, {"error": str(e), "analysis": {}})

        elif self.path.startswith('/api/browse-files'):
            query_components = parse_qs(urlparse(self.path).query)
            rel_path = query_components.get('path', [''])[0]
            base_dir = Path(WORKSTREAM_DIR).parent  # C:/Users/edebe/eds
            target_dir = base_dir / rel_path if rel_path else base_dir
            try:
                if not target_dir.exists():
                    _send_json(self, 200, {"items": [], "path": rel_path})
                else:
                    items = []
                    for entry in target_dir.iterdir():
                        items.append({
                            "name": entry.name,
                            "is_dir": entry.is_dir(),
                            "path": str(entry.relative_to(base_dir)).replace("\\", "/")
                        })
                    _send_json(self, 200, {"items": items, "path": rel_path})
            except Exception as e:
                _send_json(self, 500, {"error": str(e), "items": []})

        elif self.path.startswith('/api/file-preview'):
            query_components = parse_qs(urlparse(self.path).query)
            rel_path = query_components.get('path', [''])[0]
            base_dir = Path(WORKSTREAM_DIR).parent
            file_path = base_dir / rel_path
            try:
                if file_path.exists() and file_path.is_file():
                    content = file_path.read_text(encoding='utf-8', errors='replace')
                    _send_json(self, 200, {"content": content, "path": rel_path})
                else:
                    _send_json(self, 404, {"error": "File not found", "content": ""})
            except Exception as e:
                _send_json(self, 500, {"error": str(e), "content": ""})

        elif self.path.startswith('/api/file-content'):
            query_components = parse_qs(urlparse(self.path).query)
            folder = query_components.get('folder', [''])[0]
            filename = query_components.get('filename', [''])[0]
            
            if folder and filename:
                filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                if os.path.exists(filepath):
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                            content = f.read()
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": True, "content": content}).encode('utf-8'))
                        return
                    except Exception as e:
                        pass
            
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": False, "error": "File not found"}).encode('utf-8'))

        elif self.path.startswith('/api/search'):
            query_components = parse_qs(urlparse(self.path).query)
            q = query_components.get('q', [''])[0].lower()
            
            results = []
            if q:
                for folder in FOLDERS:
                    folder_path = os.path.join(WORKSTREAM_DIR, folder)
                    if not os.path.exists(folder_path):
                        continue
                        
                    for filename in os.listdir(folder_path):
                        if not filename.endswith(".md"):
                            continue
                        
                        filepath = os.path.join(folder_path, filename)
                        state = folder.split('_', 1)[1].title() if '_' in folder else folder.title()
                        if state.lower() == 'inprogress':
                            state = 'In Progress'
                        elif state.lower() == 'todo':
                            state = 'Todo'
                        
                        pattern = re.compile(r"^(\d{8}_\d{6})_")
                        match = pattern.match(filename)
                        date_str = "Unknown"
                        if match:
                            ts = match.group(1)
                            if len(ts) == 15:
                                date_str = f"{ts[0:4]}-{ts[4:6]}-{ts[6:8]} {ts[9:11]}:{ts[11:13]}"
                        
                        try:
                            with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
                                content = f.read()
                                
                            snippet = ""
                            if q in filename.lower():
                                snippet = "Match in filename."
                            else:
                                match_index = content.lower().find(q)
                                if match_index != -1:
                                    start = max(0, match_index - 40)
                                    end = min(len(content), match_index + len(q) + 40)
                                    snippet = "... " + content[start:end].replace('\\n', ' ') + " ..."
                            
                            if snippet:
                                results.append({
                                    "filename": filename,
                                    "folder": folder,
                                    "state": state,
                                    "date": date_str,
                                    "snippet": snippet
                                })
                        except Exception as e:
                            pass
                            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "results": results}).encode('utf-8'))

        elif self.path.startswith('/api/tasks'):
            query_components = parse_qs(urlparse(self.path).query)
            # Support date range filtering (startDate, endDate) or single date for backward compat
            start_date_raw = query_components.get('startDate', [''])[0]
            end_date_raw = query_components.get('endDate', [''])[0]
            # Backward compatibility: if old 'date' param is used
            if not start_date_raw and not end_date_raw:
                single_date = query_components.get('date', [''])[0]
                if single_date:
                    start_date_raw = single_date
                    end_date_raw = single_date
            start_date_str = start_date_raw.replace('-', '') if start_date_raw else ''
            end_date_str = end_date_raw.replace('-', '') if end_date_raw else ''

            tasks = []
            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
            
            for folder in FOLDERS:
                folder_path = os.path.join(WORKSTREAM_DIR, folder)
                if not os.path.exists(folder_path):
                    continue
                
                for filename in os.listdir(folder_path):
                    if not filename.endswith(".md"):
                        continue

                    match = pattern.match(filename)
                    filepath = os.path.join(folder_path, filename)
                    content = ""
                    source_epic = None
                    if match:
                        timestamp, part1, rest = match.groups()
                        if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                            if '_' in rest:
                                project, unique_task = rest.split('_', 1)
                            else:
                                project = "Unassigned"
                                unique_task = rest
                        else:
                            project = part1
                            unique_task = rest
                        title = unique_task.replace('_', ' ').title()
                    else:
                        # Auto-rename if format doesn't match
                        try:
                            ctime = os.path.getctime(filepath)
                            dt = datetime.datetime.fromtimestamp(ctime)
                            timestamp_str = dt.strftime("%Y%m%d_%H%M%S")
                            
                            # Ensure the file respects the schema: {timestamp}_{project}_{task}.md
                            parts = filename[:-3].split('_')
                            if len(parts) >= 2:
                                # Has at least two sections, maybe {project}_{task}
                                new_filename = f"{timestamp_str}_{filename}"
                            else:
                                new_filename = f"{timestamp_str}_unassigned_{filename}"
                            
                            new_filepath = os.path.join(folder_path, new_filename)
                            # Avoid trying to rename open files by catching any exception
                            os.rename(filepath, new_filepath)
                            
                            # Update references for continued processing
                            filename = new_filename
                            filepath = new_filepath
                            
                            # Recalculate match
                            match = pattern.match(filename)
                            if match:
                                timestamp, project, unique_task = match.groups()
                                title = unique_task.replace('_', ' ').title()
                            else:
                                timestamp = timestamp_str
                                project = "Unassigned"
                                title = filename[:-3].replace('_', ' ').title()
                        except Exception as e:
                            print(f"[Kanban API] Info: Could not rename file {filename}: {e}")
                            timestamp = ""
                            project = "Unassigned"
                            title = filename.replace('.md', '').replace('_', ' ').title()
                            
                    # [V_KANBAN_DATE_FILTER] - Date range filtering
                    if start_date_str or end_date_str:
                        file_date = timestamp[:8] if len(timestamp) >= 8 else ""
                        try:
                            mtime = os.path.getmtime(filepath)
                            mtime_date = datetime.datetime.fromtimestamp(mtime).strftime("%Y%m%d")
                        except Exception:
                            mtime_date = ""

                        # Use the most relevant date (filename date or modification date)
                        check_date = file_date if file_date else mtime_date
                        if not check_date:
                            continue

                        # Check if date falls within range
                        in_range = True
                        if start_date_str and check_date < start_date_str:
                            in_range = False
                        if end_date_str and check_date > end_date_str:
                            in_range = False

                        if not in_range:
                            continue
                    
                    # Extract robust summary
                    summary = "No summary provided."
                    changes_made = "No specific changes listed."
                    validation = "No validation steps provided."
                    progress = None
                    needs_verification = False
                    needs_feedback = False
                    priority = 2
                    evidence_items = []
                    objective_delivery_coverage = None
                    auto_acceptance = True
                    
                    try:
                        filepath = os.path.join(folder_path, filename)
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                            
                            prio_match = re.search(r"Priority:\s*(\d)", content, re.IGNORECASE)
                            if prio_match:
                                priority = int(prio_match.group(1))
                            
                            # Extract Progress Marker if it exists
                            p_match = re.search(r"Progress:\s*(\d+)%?", content, re.IGNORECASE)
                            if not p_match:
                                p_match = re.search(r"\[(\d+)/100\]", content)
                            if p_match:
                                progress = int(p_match.group(1))
                                
                            # Find Task Summary section
                            s_match = re.search(r"#\s*Task Summary\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if s_match:
                                summary = s_match.group(1).strip()
                                # Clean up formatting for display
                                summary = re.sub(r'[\r\n]+', ' ', summary)
                                if len(summary) > 120:
                                    summary = summary[:120] + "..."
                                    
                            c_match = re.search(r"#\s*Changes Made\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if c_match:
                                changes_made = c_match.group(1).strip()
                                
                            v_match = re.search(r"#\s*Validation\s*\n(.*?)(?=\n#|$)", content, re.DOTALL | re.IGNORECASE)
                            if v_match:
                                validation = v_match.group(1).strip()

                            evidence_section = _extract_markdown_section(content, "Evidence")
                            evidence_items = _parse_evidence_items(evidence_section)
                            objective_delivery_coverage = _parse_objective_delivery_coverage(evidence_section, content)
                            auto_acceptance = _parse_auto_acceptance(evidence_section, content)

                            # [2026-03-17 V20260317_1730] Extract Source Epic for Delivered Column grouping
                            source_epic = _extract_metadata(content, "Source") or _extract_metadata(content, "Epic")
                            if not source_epic:
                                # Try matching epic filename in common patterns
                                epic_slug_match = re.search(r"(\d{8}_\d{6}_.+)\.md", content)
                                if epic_slug_match:
                                    source_epic = epic_slug_match.group(1)

                            # Clean source_epic path to just filename if possible
                            if source_epic:
                                source_epic = Path(source_epic).name.strip('`').strip()

                            if "awaiting user verification" in content.lower():                                needs_verification = True
                                
                            if "provide user feedback" in content.lower():
                                needs_feedback = True

                            # Extract Deliverable info for "Show Me" feature
                            deliverable_type = None
                            deliverable_url = None
                            # First try explicit metadata
                            dt_match = re.search(r"Deliverable-Type:\s*(\w+)", content, re.IGNORECASE)
                            if dt_match:
                                deliverable_type = dt_match.group(1).strip()
                            du_match = re.search(r"Deliverable-URL:\s*(\S+)", content, re.IGNORECASE)
                            if du_match:
                                deliverable_url = du_match.group(1).strip()
                            # Also check for Deliverable-Path
                            if not deliverable_url:
                                dp_match = re.search(r"Deliverable-Path:\s*(\S+)", content, re.IGNORECASE)
                                if dp_match:
                                    deliverable_url = dp_match.group(1).strip()

                            # Auto-detect deliverables from content if not explicitly set
                            if not deliverable_url:
                                # Look for localhost URLs in content
                                url_match = re.search(r"(https?://localhost[:\d]*/[^\s\)\"\'<>]*)", content)
                                if url_match:
                                    deliverable_url = url_match.group(1).strip()
                                    deliverable_type = "UI"
                                # Look for file paths (.html, .py, .js, .tsx files)
                                if not deliverable_url:
                                    file_match = re.search(r"[`\*]?(/[^\s`\*]+\.(html|py|js|tsx|ts|css))[`\*]?", content)
                                    if not file_match:
                                        file_match = re.search(r"[`\*]?([A-Za-z]:[\\\/][^\s`\*]+\.(html|py|js|tsx|ts|css))[`\*]?", content)
                                    if file_match:
                                        deliverable_url = file_match.group(1).strip()
                                        deliverable_type = "Code"

                            if not evidence_items and deliverable_url:
                                evidence_items = [{
                                    "type": str(deliverable_type or "url"),
                                    "artifact": deliverable_url,
                                    "objective_proved": "Legacy deliverable access path",
                                    "status": "captured",
                                }]

                            agent = _resolve_agent_name(folder)
                            if (
                                folder.startswith("200_inprogress")
                                and needs_verification
                                and objective_delivery_coverage == 100
                                and auto_acceptance
                            ):
                                _auto_accept_task(filepath, agent)
                                continue

                    except Exception as e:
                        print(f"Error reading {filename}: {e}")
                        pass
                    
                    tasks.append({
                        "filename": filename,
                        "folder": folder,
                        "timestamp": timestamp,
                        "project": project,
                        "epic_family": _detect_epic_family_from_content(content if 'content' in locals() else "", filepath),
                        "title": title,
                        "summary": summary,
                        "progress": progress,
                        "needs_verification": needs_verification,
                        "needs_feedback": needs_feedback,
                        "changes_made": changes_made,
                        "validation": validation,
                        "priority": priority,
                        "deliverable_type": deliverable_type,
                        "deliverable_url": deliverable_url,
                        "evidence_items": evidence_items,
                        "objective_delivery_coverage": objective_delivery_coverage,
                        "auto_acceptance": auto_acceptance,
                        "source_epic": source_epic if 'source_epic' in locals() else None,
                    })
            
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(tasks).encode('utf-8'))
            except Exception as e:
                # Silently catch ConnectionAbortedError (WinError 10053) when browser refreshes during poll
                pass

        elif self.path == '/api/pipeline-focus':
            try:
                status = _pipeline_focus_status()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": True, **status}).encode('utf-8'))
                return
            except Exception as e:
                print(f"Error fetching pipeline focus status: {e}")
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                return

        elif self.path == '/api/workers/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({
                "excluded_workers": get_excluded_workers(),
                "workers": {
                    "codex": {"excluded": is_worker_excluded("codex")},
                    "gemini": {"excluded": is_worker_excluded("gemini")},
                    "claude": {"excluded": is_worker_excluded("claude")}
                }
            }).encode('utf-8'))

        elif self.path == '/api/process-pending':
            # Trigger agentic processing: auto-accept validated tasks, retry failed tasks
            try:
                results = _process_pending_tasks()
                _send_json(self, 200, {
                    "success": True,
                    "accepted": results["accepted"],
                    "retried": results["retried"],
                    "skipped": results["skipped"],
                    "errors": results["errors"],
                    "summary": {
                        "accepted_count": len(results["accepted"]),
                        "retried_count": len(results["retried"]),
                        "skipped_count": len(results["skipped"]),
                        "error_count": len(results["errors"])
                    }
                })
            except Exception as e:
                _send_json(self, 500, {"success": False, "error": str(e)})

        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/open-file':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    file_path = data.get('path', '')
                    mode = str(data.get('mode', 'default') or 'default').strip().lower()
                    folder = data.get('folder')
                    filename = data.get('filename')

                    if not file_path and folder and filename:
                        file_path = os.path.join(WORKSTREAM_DIR, folder, filename)

                    if file_path and os.path.exists(file_path):
                        if mode == 'code':
                            subprocess.Popen(['code', file_path], shell=True)
                        else:
                            os.startfile(file_path)
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                        return
                except Exception as e:
                    print(f"Error opening file: {e}")
            self.send_error(400)

        elif self.path == '/api/tasks/allocate':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    results = allocate_tasks(data.get("task_paths", []), data.get("target_model", ""))
                    _send_json(self, 200, results)
                    return
                except ValueError as exc:
                    _send_json(self, 400, {"error": str(exc)})
                    return
                except Exception as e:
                    print(f"Error allocating tasks: {e}")
            self.send_error(400)

        elif self.path == '/api/tasks/move-to-general':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    results = move_tasks_to_general_backlog(data.get("task_paths", []))
                    _send_json(self, 200, results)
                    return
                except Exception as e:
                    print(f"Error moving tasks to general backlog: {e}")
            self.send_error(400)

        elif self.path == '/api/tasks/reject':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    reason = data.get("reason", "").strip()
                    if not reason:
                        _send_json(self, 400, {"error": "Rejection reason is required"})
                        return
                    results = reject_tasks(data.get("task_paths", []), reason)
                    _send_json(self, 200, results)
                    return
                except Exception as e:
                    print(f"Error rejecting tasks: {e}")
            self.send_error(400)

        elif self.path == '/api/tasks/delete-bulk':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    task_paths = data.get("task_paths", [])
                    results = delete_tasks_bulk(task_paths)
                    _send_json(self, 200, results)
                    return
                except Exception as e:
                    print(f"Error deleting tasks: {e}")
                    _send_json(self, 500, {"success": False, "error": str(e), "deleted": [], "failed": []})
                    return
            self.send_error(400)

        elif self.path == '/api/tasks/extend-decomposition':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    task_paths = data.get("task_paths", [])
                    results = extend_decomposition(task_paths)
                    _send_json(self, 200, results)
                    return
                except Exception as e:
                    print(f"Error extending decomposition: {e}")
                    _send_json(self, 500, {"success": False, "error": str(e), "subtasks_created": []})
                    return
            self.send_error(400)

        elif self.path == '/api/decomposition-preview':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    epic_path = data.get("epic_path", "")
                    agent_assignments = data.get("agent_assignments", {})
                    result = decompose_epic_preview(epic_path, agent_assignments)
                    _send_json(self, 200, result)
                    return
                except Exception as e:
                    _send_json(self, 500, {"error": str(e), "task_count": 0})
                    return
            self.send_error(400)

        elif self.path == '/api/decompose-epic':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    epic_path = data.get("epic_path", "")
                    agent_assignments = data.get("agent_assignments", {})
                    destination_folder = data.get("destination_folder")
                    result = decompose_epic(epic_path, agent_assignments, destination_folder)
                    _send_json(self, 200, result)
                    return
                except Exception as e:
                    _send_json(self, 500, {"success": False, "error": str(e), "tasks_created": []})
                    return
            self.send_error(400)

        elif self.path == '/api/augment-epic':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    epic_slug = data.get("epic_slug", "")
                    solution_path = data.get("solution_path", "")
                    augment_types = data.get("augment_types", [])
                    feature_description = data.get("feature_description", "")
                    result = augment_epic(epic_slug, solution_path, augment_types, feature_description)
                    _send_json(self, 200, result)
                    return
                except Exception as e:
                    print(f"Error augmenting epic: {e}")
                    import traceback
                    traceback.print_exc()
                    _send_json(self, 500, {"success": False, "error": str(e), "tasks_created": []})
                    return
            self.send_error(400)

        elif self.path == '/api/move-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    source_folder = data.get('source_folder')
                    target_folder = data.get('target_folder')
                    filename = data.get('filename')
                    
                    if source_folder and target_folder and filename:
                        target_agent = target_folder.split('/')[-1] if '/' in target_folder else None
                        
                        source_path = os.path.join(WORKSTREAM_DIR, source_folder, filename)
                        
                        new_filename = filename
                        
                        if target_agent in ['codex', 'gemini', 'claude', 'general']:
                            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
                            match = pattern.match(filename)
                            if match:
                                timestamp, part1, rest = match.groups()
                                if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                                    new_filename = f"{timestamp}_{target_agent}_{rest}.md"
                                else:
                                    new_filename = f"{timestamp}_{target_agent}_{part1}_{rest}.md"
                        else:
                            # Moving out of an agent folder, strip the agent tag if present
                            pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$")
                            match = pattern.match(filename)
                            if match:
                                timestamp, part1, rest = match.groups()
                                if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
                                    new_filename = f"{timestamp}_{rest}.md"

                        target_path = os.path.join(WORKSTREAM_DIR, target_folder, new_filename)
                        
                        if os.path.exists(source_path):
                            os.rename(source_path, target_path)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                            return
                except Exception as e:
                    print(f"Error moving file: {e}")
            self.send_error(400)

        elif self.path == '/api/delete-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    
                    if folder in ['000_epic/general', '000_epic'] and filename:
                        # Safety Check: Does the file have derived tasks?
                        core_name = filename.replace('.md', '').replace('_processed', '')
                        has_children = False
                        
                        # Just grab all files in the system and see if they contain 'from_{core_name}'
                        search_dirs = [os.path.join(WORKSTREAM_DIR, f) for f in FOLDERS]
                        for sd in search_dirs:
                            if not os.path.exists(sd): continue
                            for ch in os.listdir(sd):
                                if ch.endswith(".md") and f"from_{core_name}" in ch:
                                    has_children = True
                                    break
                            if has_children: break
                        
                        if has_children:
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "Cannot delete: Child tasks derived from this backlog item currently exist in the system."}).encode('utf-8'))
                            return
                        else:
                            f_path = os.path.join(WORKSTREAM_DIR, folder, filename)
                            if os.path.exists(f_path):
                                os.remove(f_path)
                                self.send_response(200)
                                self.send_header('Content-type', 'application/json')
                                self.end_headers()
                                self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                                return
                except Exception as e:
                    print(f"Error deleting file: {e}")
            self.send_error(400)

        elif self.path == '/api/dump-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')

                    if folder and filename:
                        # Don't allow dumping from 300_complete or 500_dump
                        if '300_complete' in folder or '500_dump' in folder:
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "Cannot dump tasks from Complete or Dump folders."}).encode('utf-8'))
                            return

                        source_path = os.path.join(WORKSTREAM_DIR, folder, filename)

                        # Determine target dump folder (preserve agent subfolder if present)
                        agent = None
                        if '/' in folder:
                            agent = folder.split('/')[-1]
                            if agent in ['codex', 'gemini', 'claude', 'general']:
                                target_folder = f"500_dump/{agent}"
                            else:
                                target_folder = "500_dump"
                        else:
                            target_folder = "500_dump"

                        target_dir = os.path.join(WORKSTREAM_DIR, target_folder)
                        os.makedirs(target_dir, exist_ok=True)
                        target_path = os.path.join(target_dir, filename)

                        if os.path.exists(source_path):
                            shutil.move(source_path, target_path)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True, "target": target_folder}).encode('utf-8'))
                            return
                        else:
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": False, "error": "Source file not found."}).encode('utf-8'))
                            return
                except Exception as e:
                    print(f"Error dumping file: {e}")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                    return
            self.send_error(400)

        elif self.path == '/api/verify-task':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    action = data.get('action')
                    
                    filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                    if not os.path.exists(filepath):
                        self.send_error(404)
                        return
                    
                    agent = folder.split('/')[-1] if '/' in folder else 'general'
                    
                    if action == 'pass':
                        # Append feedback
                        with open(filepath, 'a', encoding='utf-8') as f:
                            f.write("\n\n# User Feedback\nUser Verified: PASS\n")
                        # Move to 300_complete
                        target_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
                        os.makedirs(target_dir, exist_ok=True)
                        os.rename(filepath, os.path.join(target_dir, filename))
                        
                    elif action == 'fail':
                        feedback = data.get('feedback', '')
                        with open(filepath, 'a', encoding='utf-8') as f:
                            f.write(f"\n\n# User Feedback\nUser Verified: FAIL\nDetails: {feedback}\n")
                        # Move back to 100_backlog
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{agent}")
                        os.makedirs(target_dir, exist_ok=True)
                        os.rename(filepath, os.path.join(target_dir, filename))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling verify: {e}")
            self.send_error(400)

        elif self.path == '/api/open-file':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    file_path = data.get('path', '')
                    mode = str(data.get('mode', 'default') or 'default').strip().lower()

                    if file_path and os.path.exists(file_path):
                        try:
                            if mode == 'code':
                                subprocess.Popen(['code', file_path], shell=True)
                            else:
                                os.startfile(file_path)
                            self.send_response(200)
                            self.send_header('Content-type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                            return
                        except Exception as e:
                            print(f"Could not open file: {e}")
                            self.send_error(500, f"Could not open file: {e}")
                            return
                except Exception as e:
                    print(f"Error handling open-file: {e}")
            self.send_error(400)

        elif self.path == '/api/submit-feedback':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    folder = data.get('folder')
                    filename = data.get('filename')
                    action = data.get('action')
                    feedback = data.get('feedback', '')
                    
                    filepath = os.path.join(WORKSTREAM_DIR, folder, filename)
                    if not os.path.exists(filepath):
                        self.send_error(404)
                        return
                    
                    agent = folder.split('/')[-1] if '/' in folder else 'general'
                    
                    with open(filepath, 'r+', encoding='utf-8') as f:
                        content = f.read()
                        f.seek(0)
                        f.truncate()
                        content = re.sub(r"- `Completion Status`:.*", "- `Completion Status`: Feedback provided", content, count=1, flags=re.IGNORECASE)
                        content += f"\n\n# User Formulated Feedback\n{feedback}\n"
                        f.write(content)

                    if action == 'complete':
                        target_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
                    else:
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{agent}")
                        
                    os.makedirs(target_dir, exist_ok=True)
                    os.rename(filepath, os.path.join(target_dir, filename))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling feedback: {e}")
            self.send_error(400)

        elif self.path == '/api/create-entry':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    entry_type = data.get('type')  # task vs backlog
                    agent = data.get('agent')
                    priority = data.get('priority', '2')
                    completion_action = data.get('completionAction', 'Awaiting user verification')
                    project = data.get('project', 'general')
                    title = data.get('title', 'new_task')
                    content = data.get('content', '')
                    
                    is_edit = data.get('is_edit', False)
                    original_folder = data.get('original_folder')
                    original_filename = data.get('original_filename')
                    
                    if entry_type == 'backlog':
                        target_dir = os.path.join(WORKSTREAM_DIR, f"000_epic/{agent}" if agent else "000_epic")
                    else:
                        target_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{agent}" if agent else "100_backlog")
                    
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    
                    if is_edit and original_folder and original_filename:
                        # Keep it in original state category
                        target_dir = os.path.join(WORKSTREAM_DIR, original_folder)
                        if agent and '/' not in original_folder:
                             target_dir = os.path.join(WORKSTREAM_DIR, f"{original_folder}/{agent}")
                        elif agent and '/' in original_folder:
                             base_folder = original_folder.split('/')[0]
                             target_dir = os.path.join(WORKSTREAM_DIR, f"{base_folder}/{agent}")
                             
                        match = re.search(r"^(\d{8}_\d{6})", original_filename)
                        if match:
                            ts = match.group(1)
                            
                        # Delete original to cleanly rename
                        orig_path = os.path.join(WORKSTREAM_DIR, original_folder, original_filename)
                        if os.path.exists(orig_path):
                            os.remove(orig_path)
                            
                    os.makedirs(target_dir, exist_ok=True)
                    
                    if agent:
                        filename = f"{ts}_{agent}_{project}_{title}.md"
                    else:
                        filename = f"{ts}_{project}_{title}.md"
                        
                    filepath = os.path.join(target_dir, filename)
                    
                    full_content = f"Priority: {priority}\n\n" + content + f"\n\n- `Completion Status`: {completion_action}\n"
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(full_content)
                        
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error creating entry: {e}")
            self.send_error(400)

        elif self.path == '/api/pipeline-focus':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    enabled = bool(data.get('enabled'))
                    epic_family = _canonical_epic_family(data.get('epic_family'))
                    cfg = _save_pipeline_focus_config({
                        "enabled": enabled and bool(epic_family),
                        "epic_family": epic_family,
                        "mode": PIPELINE_FOCUS_MODE_SELECTED_ONLY,
                    })
                    status = _pipeline_focus_status()
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True, "config": cfg, **status}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error setting pipeline focus: {e}")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": False, "error": str(e)}).encode('utf-8'))
                    return
            self.send_error(400)

        elif self.path in ['/api/review-approve', '/api/review-modify', '/api/review-reject']:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                try:
                    data = json.loads(post_data.decode('utf-8'))
                    agent = data.get('agent')
                    core_name = data.get('coreName')
                    
                    review_dir = os.path.join(WORKSTREAM_DIR, f"050_review/{agent}")
                    todo_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{agent}")
                    backlog_dir = os.path.join(WORKSTREAM_DIR, f"000_epic/{agent}")
                    
                    backlog_review_file = os.path.join(backlog_dir, f"{core_name}_review.md")
                    
                    if self.path == '/api/review-approve':
                        # Move drafts to todo
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.rename(os.path.join(review_dir, f), os.path.join(todo_dir, f))
                        # Rename backlog to processed
                        if os.path.exists(backlog_review_file):
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}_processed.md"))
                            
                    elif self.path == '/api/review-modify':
                        feedback = data.get('feedback', '')
                        # Delete drafts
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.remove(os.path.join(review_dir, f))
                        # Revert backlog to raw .md, append feedback
                        if os.path.exists(backlog_review_file):
                            with open(backlog_review_file, 'a', encoding='utf-8') as blf:
                                blf.write(f"\\n\\n# User Feedback (Task Generation)\\n{feedback}\\n")
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}.md"))
                            
                    elif self.path == '/api/review-reject':
                        # Delete drafts
                        for f in os.listdir(review_dir):
                            if f.endswith('.md') and core_name in f:
                                os.remove(os.path.join(review_dir, f))
                        # Mark backlog suspended
                        if os.path.exists(backlog_review_file):
                            os.rename(backlog_review_file, os.path.join(backlog_dir, f"{core_name}_suspended.md"))
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
                    return
                except Exception as e:
                    print(f"Error handling review gate: {e}")
            self.send_error(400)

        elif self.path == '/api/workers/toggle':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                try:
                    post_data = self.rfile.read(content_length)
                    data = json.loads(post_data.decode('utf-8'))
                    agent = data.get('agent', '').lower()
                    excluded = data.get('excluded', False)

                    if agent in ('codex', 'gemini', 'claude'):
                        set_worker_excluded(agent, excluded)
                        self.send_response(200)
                        self.send_header('Content-type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            "success": True,
                            "agent": agent,
                            "excluded": excluded,
                            "excluded_workers": get_excluded_workers()
                        }).encode('utf-8'))
                        return
                except Exception as e:
                    print(f"Error toggling worker: {e}")
            self.send_error(400)

        else:
            self.send_error(404)

import threading
import time
import subprocess

# Worker exclusion state management - workers can be excluded when rate limited
# Uses file-based storage so run_agent.py can also read the state
_excluded_workers: set[str] = set()
_excluded_workers_lock = threading.Lock()
_EXCLUDED_WORKERS_FILE = Path(WORKSTREAM_DIR) / "excluded_workers.txt"
_pipeline_focus_lock = threading.Lock()
_lane_active_task_lock = threading.Lock()
_lane_active_tasks: dict[str, str] = {}

def _load_excluded_workers() -> set[str]:
    """Load excluded workers from file."""
    if not _EXCLUDED_WORKERS_FILE.exists():
        return set()
    try:
        return set(_EXCLUDED_WORKERS_FILE.read_text(encoding="utf-8").strip().lower().split())
    except Exception:
        return set()

def _save_excluded_workers(excluded: set[str]) -> None:
    """Save excluded workers to file."""
    try:
        _EXCLUDED_WORKERS_FILE.write_text(" ".join(sorted(excluded)), encoding="utf-8")
    except Exception as e:
        print(f"[Worker Control] Failed to save exclusion file: {e}")


def _default_pipeline_focus_config() -> dict[str, Any]:
    return {
        "enabled": False,
        "epic_family": "",
        "mode": PIPELINE_FOCUS_MODE_SELECTED_ONLY,
        "updated_at": None,
        "released_at": None,
    }


def _load_pipeline_focus_config() -> dict[str, Any]:
    if not PIPELINE_FOCUS_CONFIG_PATH.exists():
        return _default_pipeline_focus_config()
    try:
        raw = json.loads(PIPELINE_FOCUS_CONFIG_PATH.read_text(encoding="utf-8"))
        cfg = _default_pipeline_focus_config()
        cfg.update(raw if isinstance(raw, dict) else {})
        cfg["enabled"] = bool(cfg.get("enabled"))
        cfg["epic_family"] = _canonical_epic_family(cfg.get("epic_family"))
        cfg["mode"] = PIPELINE_FOCUS_MODE_SELECTED_ONLY
        return cfg
    except Exception:
        return _default_pipeline_focus_config()


def _save_pipeline_focus_config(config: dict[str, Any]) -> dict[str, Any]:
    cfg = _default_pipeline_focus_config()
    cfg.update(config or {})
    cfg["enabled"] = bool(cfg.get("enabled") and cfg.get("epic_family"))
    cfg["epic_family"] = _canonical_epic_family(cfg.get("epic_family"))
    cfg["mode"] = PIPELINE_FOCUS_MODE_SELECTED_ONLY
    cfg["updated_at"] = datetime.datetime.now().isoformat()
    PIPELINE_FOCUS_CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    PIPELINE_FOCUS_CONFIG_PATH.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return cfg


def _set_lane_active_task(agent: str, task_path: str | None) -> None:
    with _lane_active_task_lock:
        if task_path:
            _lane_active_tasks[agent.lower()] = str(task_path)
        else:
            _lane_active_tasks.pop(agent.lower(), None)


def _get_lane_active_task_paths() -> set[str]:
    with _lane_active_task_lock:
        return set(_lane_active_tasks.values())


def _available_epic_families() -> list[str]:
    families: set[str] = set()
    for state_folder in PIPELINE_FOCUS_STATE_FOLDERS:
        for task_path in _iter_state_markdown_files(state_folder):
            family = _detect_epic_family_for_file(task_path)
            if family and family in KNOWN_EPIC_FAMILIES:
                families.add(family)
    return sorted(families)


def _pipeline_focus_remaining_counts(epic_family: str) -> dict[str, int]:
    family = _canonical_epic_family(epic_family)
    counts = {folder: 0 for folder in PIPELINE_FOCUS_STATE_FOLDERS}
    if not family:
        return counts
    for state_folder in PIPELINE_FOCUS_STATE_FOLDERS:
        for task_path in _iter_state_markdown_files(state_folder):
            if _detect_epic_family_for_file(task_path) == family:
                counts[state_folder] += 1
    return counts


def _restore_parked_focus_items() -> list[str]:
    restored: list[str] = []
    for state_folder in PIPELINE_FOCUS_ACTIVE_FOLDERS:
        pending_root = Path(WORKSTREAM_DIR) / state_folder / PIPELINE_PENDING_DIRNAME
        if not pending_root.exists():
            continue
        pending_files = sorted([path for path in pending_root.rglob("*.md") if path.is_file()])
        for task_path in pending_files:
            dest = _restore_path_from_pending(task_path, state_folder)
            moved_to = _move_file_preserving_uniqueness(task_path, dest)
            restored.append(f"{task_path} -> {moved_to}")
    return restored


def _restore_selected_focus_items(epic_family: str) -> list[str]:
    restored: list[str] = []
    family = _canonical_epic_family(epic_family)
    if not family:
        return restored
    for state_folder in PIPELINE_FOCUS_ACTIVE_FOLDERS:
        pending_root = Path(WORKSTREAM_DIR) / state_folder / PIPELINE_PENDING_DIRNAME
        if not pending_root.exists():
            continue
        pending_files = sorted([path for path in pending_root.rglob("*.md") if path.is_file()])
        for task_path in pending_files:
            if _detect_epic_family_for_file(task_path) != family:
                continue
            dest = _restore_path_from_pending(task_path, state_folder)
            moved_to = _move_file_preserving_uniqueness(task_path, dest)
            restored.append(f"{task_path} -> {moved_to}")
    return restored


def _park_non_focus_items(epic_family: str) -> dict[str, list[str]]:
    family = _canonical_epic_family(epic_family)
    active_paths = _get_lane_active_task_paths()
    moved: dict[str, list[str]] = {folder: [] for folder in PIPELINE_FOCUS_ACTIVE_FOLDERS}
    if not family:
        return moved

    for state_folder in PIPELINE_FOCUS_ACTIVE_FOLDERS:
        state_root = Path(WORKSTREAM_DIR) / state_folder
        if not state_root.exists():
            continue
        for task_path in sorted([path for path in state_root.rglob("*.md") if path.is_file()]):
            if PIPELINE_PENDING_DIRNAME in task_path.parts:
                continue
            if str(task_path) in active_paths:
                continue
            if _detect_epic_family_for_file(task_path) == family:
                continue
            dest = _pending_path_for_file(task_path, state_folder)
            moved_to = _move_file_preserving_uniqueness(task_path, dest)
            moved[state_folder].append(f"{task_path} -> {moved_to}")
    return moved


def _sync_pipeline_focus_state() -> dict[str, Any]:
    with _pipeline_focus_lock:
        cfg = _load_pipeline_focus_config()
        actions = {
            "parked": {folder: [] for folder in PIPELINE_FOCUS_ACTIVE_FOLDERS},
            "restored": [],
            "released": False,
        }

        if not cfg.get("enabled") or not cfg.get("epic_family"):
            actions["restored"] = _restore_parked_focus_items()
            return {
                "config": cfg,
                "remaining": _pipeline_focus_remaining_counts(cfg.get("epic_family", "")),
                "actions": actions,
            }

        remaining = _pipeline_focus_remaining_counts(cfg["epic_family"])
        outstanding = sum(remaining.get(folder, 0) for folder in PIPELINE_FOCUS_STATE_FOLDERS if folder != "300_complete")
        if outstanding == 0:
            cfg["enabled"] = False
            cfg["released_at"] = datetime.datetime.now().isoformat()
            cfg = _save_pipeline_focus_config(cfg)
            actions["released"] = True
            actions["restored"] = _restore_parked_focus_items()
            return {
                "config": cfg,
                "remaining": remaining,
                "actions": actions,
            }

        actions["restored"] = _restore_selected_focus_items(cfg["epic_family"])
        actions["parked"] = _park_non_focus_items(cfg["epic_family"])
        return {
            "config": cfg,
            "remaining": remaining,
            "actions": actions,
        }


def _pipeline_focus_status() -> dict[str, Any]:
    sync_result = _sync_pipeline_focus_state()
    cfg = sync_result["config"]
    remaining = _pipeline_focus_remaining_counts(cfg.get("epic_family", "")) if cfg.get("epic_family") else {folder: 0 for folder in PIPELINE_FOCUS_STATE_FOLDERS}
    parked = {}
    for state_folder in PIPELINE_FOCUS_ACTIVE_FOLDERS:
        pending_root = Path(WORKSTREAM_DIR) / state_folder / PIPELINE_PENDING_DIRNAME
        parked[state_folder] = len([path for path in pending_root.rglob("*.md") if path.is_file()]) if pending_root.exists() else 0
    return {
        "enabled": bool(cfg.get("enabled")),
        "epic_family": cfg.get("epic_family", ""),
        "mode": cfg.get("mode", PIPELINE_FOCUS_MODE_SELECTED_ONLY),
        "remaining": remaining if isinstance(remaining, dict) else _pipeline_focus_remaining_counts(cfg.get("epic_family", "")),
        "parked": parked,
        "released": bool(sync_result["actions"].get("released")),
        "available_epics": _available_epic_families(),
        "active_lane_tasks": sorted(_get_lane_active_task_paths()),
    }

def is_worker_excluded(agent: str) -> bool:
    """Check if a worker is currently excluded."""
    with _excluded_workers_lock:
        return agent.lower() in _excluded_workers

def set_worker_excluded(agent: str, excluded: bool) -> None:
    """Set the exclusion state for a worker."""
    global _excluded_workers
    with _excluded_workers_lock:
        agent_lower = agent.lower()
        if excluded:
            _excluded_workers.add(agent_lower)
            print(f"[Worker Control] {agent.upper()} excluded from task polling")
        else:
            _excluded_workers.discard(agent_lower)
            print(f"[Worker Control] {agent.upper()} re-enabled for task polling")
        _save_excluded_workers(_excluded_workers)

def get_excluded_workers() -> list[str]:
    """Get list of currently excluded workers."""
    with _excluded_workers_lock:
        return list(_excluded_workers)

# Load exclusions on startup
_excluded_workers = _load_excluded_workers()

def _extract_project_from_core_name(core_name):
    project = "unassigned"
    pattern = re.compile(r"^(\d{8}_\d{6})_([^_]+)_(.+)$")
    match = pattern.match(core_name)
    if not match:
        return project
    _, part1, rest = match.groups()
    if part1.lower() in ['codex', 'gemini', 'claude', 'general']:
        if '_' in rest:
            project, _ = rest.split('_', 1)
        else:
            project = rest
    else:
        project = part1
    return (project or "unassigned").lower()

def _build_decompose_command(agent, backlog_path):
    """
    Returns command list for real decomposition call.
    Supports env override:
      KANBAN_LLM_DECOMP_CMD='python path\\to\\script.py --agent {agent} --input "{backlog_path}"'
    """
    cmd_tpl = os.environ.get("KANBAN_LLM_DECOMP_CMD", "").strip()
    if cmd_tpl:
        formatted = cmd_tpl.format(
            agent=agent,
            backlog_path=backlog_path,
            backlog_file=os.path.basename(backlog_path),
        )
        return shlex.split(formatted, posix=False)

    # Default integration path. If script is not present, worker logs and retries later.
    default_script = os.path.join(WORKSTREAM_DIR, "llm_decompose_cli.py")
    return [sys.executable, default_script, "--agent", agent, "--input", backlog_path]

def _validate_decomposition_payload(payload):
    """
    Accept either:
      - list[task]
      - { "tasks": list[task] }
    where task minimally includes:
      title, summary (or description), and optional tests/acceptance_criteria/steps.
    """
    tasks = payload.get("tasks") if isinstance(payload, dict) else payload
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("Decomposition payload missing non-empty task list.")

    normalized = []
    for idx, item in enumerate(tasks, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Task {idx} is not an object.")
        title = str(item.get("title") or "").strip()
        summary = str(item.get("summary") or item.get("description") or "").strip()
        if not title or not summary:
            raise ValueError(f"Task {idx} missing required title/summary.")
        tests = item.get("tests") or item.get("acceptance_criteria") or item.get("validation") or []
        if isinstance(tests, str):
            tests = [tests]
        if not isinstance(tests, list):
            tests = []
        steps = item.get("steps") or []
        if isinstance(steps, str):
            steps = [steps]
        if not isinstance(steps, list):
            steps = []
        normalized.append({
            "title": title,
            "summary": summary,
            "tests": [str(t).strip() for t in tests if str(t).strip()],
            "steps": [str(s).strip() for s in steps if str(s).strip()],
            "priority": item.get("priority", 2),
            "source_backlog": str(item.get("source_backlog") or "").strip(),
        })
    return normalized

def _render_generated_task_md(item, core_name, idx, agent, backlog_review_relpath):
    tests = item.get("tests") or []
    steps = item.get("steps") or []
    lines = []
    lines.append(f"Priority: {item.get('priority', 2)}")
    lines.append("")
    lines.append(f"# {item['title']}")
    lines.append("")
    lines.append(f"- Source backlog: `{core_name}.md`")
    lines.append(f"- Source backlog path: `{backlog_review_relpath}`")
    lines.append(f"- Parent backlog id: `{core_name}`")
    lines.append(f"- Generated by: real_llm_decomposition")
    lines.append(f"- Required skill: `C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md`")
    lines.append("")
    lines.append("## Prerequisite")
    lines.append("- [ ] Read `C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md` before starting implementation.")
    lines.append("")
    lines.append("## Task Summary")
    lines.append(item["summary"])
    lines.append("")
    lines.append("## Plan")
    if steps:
        for step_idx, step in enumerate(steps, start=1):
            lines.append(f"- [ ] {step_idx}. {step}")
            step_test = tests[(step_idx - 1) % len(tests)] if tests else f"Verify completion evidence for step {step_idx}."
            lines.append(f"  - [ ] Test: {step_test}")
            lines.append(f"  - [ ] Evidence: pending")
    else:
        lines.append(f"- [ ] 1. Implement `{item['title']}` according to summary.")
        lines.append("  - [ ] Test: Verify implementation evidence and updated files for this task.")
        lines.append("  - [ ] Evidence: pending")
    lines.append("")
    lines.append("## Validation")
    if tests:
        for t in tests:
            lines.append(f"- [ ] {t}")
    else:
        lines.append("- [ ] Add and run implementation-specific validation.")
    lines.append("")
    lines.append(f"## Notes")
    lines.append(f"- Generated item index: {idx}")
    lines.append(f"- Generated for lane: {agent}")
    return "\n".join(lines).strip() + "\n"

def _append_generated_tasks_to_backlog(backlog_review_path, review_rel_dir, generated_files):
    if not generated_files:
        return
    try:
        existing = ""
        if os.path.exists(backlog_review_path):
            with open(backlog_review_path, "r", encoding="utf-8") as f:
                existing = f.read()
        lines = []
        lines.append("")
        lines.append("## Generated Tasks")
        lines.append("| Task | File |")
        lines.append("|------|------|")
        for fname in generated_files:
            title = fname.replace(".md", "")
            rel = f"{review_rel_dir}/{fname}".replace("\\", "/")
            lines.append(f"| {title} | `{rel}` |")
        lines.append("")
        block = "\n".join(lines)
        if "## Generated Tasks" in existing:
            existing = re.sub(r"## Generated Tasks[\s\S]*?$", block.strip() + "\n", existing.strip(), flags=re.MULTILINE)
            content = existing
        else:
            content = existing.rstrip() + "\n" + block
        with open(backlog_review_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as exc:
        print(f"[DECOMP] Failed to append generated task links to backlog review: {exc}")

def _extract_section(raw, section_name):
    pattern = re.compile(
        rf"^\s*##\s*{re.escape(section_name)}\s*$([\s\S]*?)(?=^\s*##\s+|\Z)",
        flags=re.MULTILINE | re.IGNORECASE
    )
    m = pattern.search(raw or "")
    return (m.group(1) if m else "").strip()

def _checkbox_stats(raw):
    lines = (raw or "").splitlines()
    boxes = [ln for ln in lines if re.search(r"^\s*[-*]\s+\[[ xX]\]\s+", ln)]
    checked = [ln for ln in boxes if re.search(r"\[[xX]\]", ln)]
    return len(boxes), len(checked)

def _plan_step_stats(raw):
    lines = (raw or "").splitlines()
    steps = [ln for ln in lines if re.search(r"^\s*-\s+\[[ xX]\]\s+\d+\.\s+", ln)]
    checked = [ln for ln in steps if re.search(r"\[[xX]\]", ln)]
    return len(steps), len(checked)

def _test_line_count(raw):
    return len([ln for ln in (raw or "").splitlines() if re.search(r"^\s*-\s*(\[[ xX]\]\s*)?Test:\s+", ln, flags=re.IGNORECASE)])

def _evidence_line_count(raw):
    return len([ln for ln in (raw or "").splitlines() if re.search(r"^\s*-\s*(\[[ xX]\]\s*)?Evidence:\s+", ln, flags=re.IGNORECASE)])

def _checked_test_count(raw):
    return len([ln for ln in (raw or "").splitlines() if re.search(r"^\s*-\s*\[[xX]\]\s*Test:\s+", ln, flags=re.IGNORECASE)])

def _checked_evidence_count(raw):
    return len([ln for ln in (raw or "").splitlines() if re.search(r"^\s*-\s*\[[xX]\]\s*Evidence:\s+", ln, flags=re.IGNORECASE)])

def _task_quality_gate(task_path):
    """
    Relaxed Quality Gate:
    Warnings instead of blocking so user-generated backlog items execute freely.
    """
    return True, "ok"

def _task_completion_gate(task_path):
    """
    Enforce completion quality:
    - Plan/Validation checklist structure exists
    - Plan has Test lines for each checklist item
    - All Plan and Validation checkboxes are checked
    """
    try:
        raw = Path(task_path).read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return False, f"read_error: {exc}"

    plan = _extract_section(raw, "Plan")
    val = _extract_section(raw, "Validation")
    step_total, step_checked = _plan_step_stats(plan)
    plan_total, plan_checked = _checkbox_stats(plan)
    val_total, val_checked = _checkbox_stats(val)
    plan_tests = _test_line_count(plan)
    plan_evidence = _evidence_line_count(plan)
    checked_tests = _checked_test_count(plan)
    checked_evidence = _checked_evidence_count(plan)

    if step_total <= 0:
        return False, "missing_plan_checklist"
    if val_total <= 0:
        return False, "missing_validation_checklist"
    if plan_tests < step_total:
        return False, "missing_plan_tests"
    if plan_evidence < step_total:
        return False, "missing_plan_evidence"
    if checked_tests < step_total:
        return False, "tests_not_fully_checked"
    if checked_evidence < step_total:
        return False, "evidence_not_fully_checked"
    if step_checked < step_total:
        return False, "plan_not_fully_checked"
    if val_checked < val_total:
        return False, "validation_not_fully_checked"
    return True, "ok"

def _mark_all_checkboxes_complete(task_path):
    try:
        raw = Path(task_path).read_text(encoding="utf-8", errors="ignore")
        updated = re.sub(r"^(\s*[-*]\s+\[)\s(\]\s+)", r"\1x\2", raw, flags=re.MULTILINE)
        if updated != raw:
            Path(task_path).write_text(updated, encoding="utf-8")
    except Exception as exc:
        print(f"[Worker] failed to mark checklist complete for {task_path}: {exc}")

def _decompose_backlog_real(agent, backlog_path, timeout_sec=120):
    started = time.time()
    cmd = _build_decompose_command(agent, backlog_path)
    print(f"[Lane Worker: {agent.upper()}] [DECOMP] invoking command: {' '.join(cmd)}")
    if len(cmd) >= 2 and cmd[1].endswith("llm_decompose_cli.py") and not os.path.exists(cmd[1]):
        raise RuntimeError(f"LLM decomposition script not found: {cmd[1]}")
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_sec)
    duration = round(time.time() - started, 2)
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Decomposition command failed (rc={proc.returncode}, {duration}s): {err[-600:]}")
    raw = (proc.stdout or "").strip()
    if not raw:
        raise ValueError("Decomposition command returned empty stdout.")
    payload = json.loads(raw)
    tasks = _validate_decomposition_payload(payload)
    print(f"[Lane Worker: {agent.upper()}] [DECOMP] success: {len(tasks)} tasks in {duration}s")
    return tasks, duration

def _build_agent_execution_command(agent, task_path):
    """
    Real execution command resolver.
    Supported env vars:
    - KANBAN_AGENT_EXEC_CMD_<AGENT> (e.g., ..._CODEX)
    - KANBAN_AGENT_EXEC_CMD (fallback)
    Placeholders: {agent}, {task_path}, {task_file}
    """
    key_specific = f"KANBAN_AGENT_EXEC_CMD_{agent.upper()}"
    tpl = os.environ.get(key_specific, "").strip() or os.environ.get("KANBAN_AGENT_EXEC_CMD", "").strip()
    if not tpl:
        agent_lower = agent.lower()
        if agent_lower in {"codex", "gemini", "claude"}:
            # [2026-03-17 V20260317_1715] Use agent-specific binary and syntax
            agent_bin = _resolve_agent_binary(agent)
            prompt = (
                "Execute this task file end-to-end. "
                "Read and follow C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md first. "
                f"Task file: {task_path}. "
                "Implement required changes in the workspace, run validations, and update checklist items."
            )
            
            # Agent-specific command structures
            if agent_lower == "gemini":
                return [agent_bin, "--prompt", prompt, "--yolo"]
            elif agent_lower == "claude":
                return [agent_bin, "-p", prompt, "--permission-mode", "acceptEdits"]
            else: # codex
                return [agent_bin, "exec", "-C", r"C:\Users\edebe\eds", prompt]
        return None
    formatted = tpl.format(
        agent=agent,
        task_path=task_path,
        task_file=os.path.basename(task_path),
    )
    return shlex.split(formatted, posix=False)

def multi_model_lane_worker(agent):
    print(f"[Agent Worker: {agent.upper()}] Lane daemon started...")
    while True:
        try:
            _sync_pipeline_focus_state()
            focus_cfg = _load_pipeline_focus_config()
            focus_family = _canonical_epic_family(focus_cfg.get("epic_family"))
            focus_enabled = bool(focus_cfg.get("enabled") and focus_family)

            # Check if worker is excluded (e.g., due to rate limits)
            if is_worker_excluded(agent):
                time.sleep(30)  # Sleep longer when excluded
                continue

            todo_dir = os.path.join(WORKSTREAM_DIR, f"100_backlog/{agent}")
            general_todo_dir = os.path.join(WORKSTREAM_DIR, "100_backlog", "general")
            inprog_dir = os.path.join(WORKSTREAM_DIR, f"200_inprogress/{agent}")
            failed_dir = os.path.join(WORKSTREAM_DIR, f"400_failed/{agent}")
            complete_dir = os.path.join(WORKSTREAM_DIR, f"300_complete/{agent}")
            backlog_dir = os.path.join(WORKSTREAM_DIR, f"000_epic/{agent}")
            review_dir = os.path.join(WORKSTREAM_DIR, f"050_review/{agent}")
            inprogress_root = os.path.join(WORKSTREAM_DIR, "200_inprogress")

            # Check capacity constraints
            active_tasks = []
            if os.path.exists(todo_dir):
                for name in os.listdir(todo_dir):
                    if not name.endswith(".md") or name.startswith("."):
                        continue
                    if focus_enabled and _detect_epic_family_for_file(os.path.join(todo_dir, name)) != focus_family:
                        continue
                    active_tasks.append(name)
            if os.path.exists(inprog_dir):
                for name in os.listdir(inprog_dir):
                    if not name.endswith(".md") or name.startswith("."):
                        continue
                    if focus_enabled and _detect_epic_family_for_file(os.path.join(inprog_dir, name)) != focus_family:
                        continue
                    active_tasks.append(name)
            if os.path.exists(review_dir):
                for name in os.listdir(review_dir):
                    if not name.endswith(".md") or name.startswith("."):
                        continue
                    if focus_enabled and _detect_epic_family_for_file(os.path.join(review_dir, name)) != focus_family:
                        continue
                    active_tasks.append(name)

            if len(active_tasks) == 0:
                reclaimed, details = _claim_blocked_task_for_lane(agent)
                if reclaimed:
                    print(f"[Lane Worker: {agent.upper()}] Re-queued blocked task: {details}")
                    time.sleep(2)
                    continue

            # Poll Backlog Decomposition if capacity is zero
            if len(active_tasks) == 0 and os.path.exists(backlog_dir):
                backlogs = [f for f in os.listdir(backlog_dir) if f.endswith(".md") and not f.endswith("_processed.md") and not f.endswith("_review.md") and not f.endswith("_suspended.md") and not f.startswith(".")]
                if focus_enabled:
                    backlogs = [
                        name for name in backlogs
                        if _detect_epic_family_for_file(os.path.join(backlog_dir, name)) == focus_family
                    ]
                if backlogs:
                    backlogs.sort()
                    bl_file = backlogs[0]
                    bl_src = os.path.join(backlog_dir, bl_file)
                    
                    print(f"[Lane Worker: {agent.upper()}] Decomposing Backlog Item: {bl_file} ...")
                    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    core_name = bl_file.replace(".md", "")
                    project = _extract_project_from_core_name(core_name)
                    try:
                        tasks, duration = _decompose_backlog_real(agent, bl_src, timeout_sec=120)
                    except subprocess.TimeoutExpired:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] timeout for {bl_file}; will retry.")
                        time.sleep(2)
                        continue
                    except Exception as decomp_err:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] failed for {bl_file}: {decomp_err}")
                        time.sleep(2)
                        continue

                    generated = 0
                    generated_files = []
                    bl_new_name = f"{core_name}_review.md"
                    bl_review_path = os.path.join(backlog_dir, bl_new_name)
                    if os.path.exists(bl_review_path):
                        suffix = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        bl_new_name = f"{core_name}_review_{suffix}.md"
                        bl_review_path = os.path.join(backlog_dir, bl_new_name)
                    backlog_review_relpath = f"000_epic/{agent}/{bl_new_name}"
                    for idx, item in enumerate(tasks, start=1):
                        new_task = f"{ts}_{agent}_{project}_task_{idx:02d}_from_{core_name}.md"
                        task_path = os.path.join(review_dir, new_task)
                        with open(task_path, "w", encoding="utf-8") as tf:
                            tf.write(_render_generated_task_md(item, core_name, idx, agent, backlog_review_relpath))
                        generated += 1
                        generated_files.append(new_task)

                    if generated <= 0:
                        print(f"[Lane Worker: {agent.upper()}] [DECOMP] no tasks produced for {bl_file}; keeping backlog for retry.")
                        time.sleep(2)
                        continue

                    # Mark Backlog as pending review only after successful generation
                    os.rename(bl_src, bl_review_path)
                    _append_generated_tasks_to_backlog(bl_review_path, f"050_review/{agent}", generated_files)
                    print(f"[Lane Worker: {agent.upper()}] [DECOMP] pending review: {bl_new_name} (generated={generated}, duration={duration}s)")
                    time.sleep(2)
                    continue # Skip directly to next iteration to let UI update

            # Resume any existing tasks sitting in the model lane before claiming new ones.
            if os.path.exists(inprog_dir):
                pending = [f for f in os.listdir(inprog_dir) if f.endswith(".md") and not f.startswith(".")]
                pending.sort()
                resumed = False
                for task_file in pending:
                    inprog_path = os.path.join(inprog_dir, task_file)
                    if _task_has_execution_evidence(inprog_path):
                        continue
                    resumed = _execute_task(agent, task_file, inprog_dir, todo_dir, inprog_dir, review_dir, failed_dir, complete_dir, is_resume=True)
                    break
                if resumed:
                    continue

            # Poll dependency-ready tasks from general backlog first, then agent-specific backlog.
            if os.path.exists(todo_dir) or os.path.exists(general_todo_dir):
                current_inprogress = 0
                if os.path.exists(inprogress_root):
                    for current_root, _, files in os.walk(inprogress_root):
                        current_inprogress += sum(
                            1 for name in files
                            if name.endswith(".md") and not name.startswith(".")
                            and PIPELINE_PENDING_DIRNAME not in Path(current_root).parts
                            and (
                                not focus_enabled
                                or _detect_epic_family_for_file(os.path.join(current_root, name)) == focus_family
                            )
                            and not _task_has_execution_evidence(os.path.join(current_root, name))
                        )

                if current_inprogress >= MAX_CONCURRENT_INPROGRESS_TASKS:
                    time.sleep(2)
                    continue

                backlog_sources = []
                if os.path.exists(general_todo_dir):
                    backlog_sources.append(general_todo_dir)
                if os.path.exists(todo_dir):
                    backlog_sources.append(todo_dir)

                parsed_tasks = []
                completed_files = _completed_task_filenames()
                for source_dir in backlog_sources:
                    tasks = [f for f in os.listdir(source_dir) if f.endswith(".md") and not f.startswith(".")]
                    for t_file in tasks:
                        priority = 2
                        source_path = os.path.join(source_dir, t_file)
                        if focus_enabled and _detect_epic_family_for_file(source_path) != focus_family:
                            continue
                        try:
                            with open(source_path, 'r', encoding='utf-8') as f:
                                raw = f.read()
                                p_match = re.search(r"Priority:\s*(\d)", raw[:2048], re.IGNORECASE)
                                if p_match:
                                    priority = int(p_match.group(1))
                        except Exception:
                            raw = ""
                        ready, unmet = _task_dependencies_ready(source_path, completed_files)
                        parsed_tasks.append({
                            'filename': t_file,
                            'p': priority,
                            'source_dir': source_dir,
                            'ready': ready,
                            'unmet': unmet,
                        })

                ready_tasks = [item for item in parsed_tasks if item['ready']]
                if ready_tasks:
                    ready_tasks.sort(key=lambda x: (x['p'], x['filename']))
                    candidate = ready_tasks[0]
                    target_date = _extract_task_date(candidate['filename'])
                    current_inprogress = _count_inprogress_for_date(inprogress_root, target_date, focus_family if focus_enabled else None)
                    if current_inprogress >= MAX_CONCURRENT_INPROGRESS_TASKS:
                        continue
                    success = _execute_task(agent, candidate['filename'], candidate['source_dir'], todo_dir, inprog_dir, review_dir, failed_dir, complete_dir)
                    if success:
                        continue

        except Exception as e:
            print(f"[Agent Worker: {agent.upper()}] Master Loop error: {e}")
        time.sleep(10)


# Agentic processing interval in seconds (default: 60 seconds)
AGENTIC_PROCESS_INTERVAL = 60


def agentic_processor_daemon():
    """Background daemon that periodically processes pending tasks.

    Runs _process_pending_tasks() at regular intervals to:
    - Auto-accept tasks in review that meet validation criteria
    - Retry failed tasks by reassigning to different agents
    """
    print("[Agentic Processor] Starting background daemon...")
    while True:
        try:
            time.sleep(AGENTIC_PROCESS_INTERVAL)
            results = _process_pending_tasks()
            accepted = len(results.get("accepted", []))
            retried = len(results.get("retried", []))
            errors = len(results.get("errors", []))
            if accepted > 0 or retried > 0 or errors > 0:
                print(f"[Agentic Processor] Processed: {accepted} accepted, {retried} retried, {errors} errors")
        except Exception as e:
            print(f"[Agentic Processor] Error: {e}")


import subprocess

if __name__ == '__main__':

    monitor_thread = threading.Thread(target=agent_controller_monitor, daemon=True)
    monitor_thread.start()

    # Start Agentic Processor Daemon (auto-accept, retry failed tasks)
    agentic_thread = threading.Thread(target=agentic_processor_daemon, daemon=True)
    agentic_thread.start()

    # Start Multi-Model Lane Worker Daemon Threads (Parallel Execution)
    agents = ['codex', 'gemini', 'claude']
    for agent in agents:
        worker_t = threading.Thread(target=multi_model_lane_worker, args=(agent,), daemon=True)
        worker_t.start()

    PORT = 8080
    server = ThreadedHTTPServer(('localhost', PORT), KanbanHandler)
    print(f"Real-Time Kanban Dashboard starting on http://localhost:{PORT}")
    print("Keep this terminal open, or run in background. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nKanban Dashboard stopped.")
