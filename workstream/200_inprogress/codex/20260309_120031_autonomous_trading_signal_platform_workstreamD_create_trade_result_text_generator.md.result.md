OpenAI Codex v0.115.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d06ea-d1a9-72c3-8137-9d13d5da283e
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m loading the required lifecycle skill and the specified task file first, then I’ll inspect the codebase context those instructions point to before making any edits.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\eds succeeded in 2.20s:
---
name: workstream-task-lifecycle
description: Create and maintain timestamped task documentation files in the workstream lifecycle folders (`workstream/000_epic`, `workstream/100_backlog`, `workstream/200_inprogress`, `workstream/300_complete`). Use when a user asks to document changes, track progress for a distinct task, or enforce file movement across backlog/in-progress/complete states.
---

# Workstream Task Lifecycle

Execute this workflow whenever a distinct task needs a documented trail.

## Folder Structure
```
workstream/
├── 000_epic/        ← High-level specs, PRDs, strategic documents
│                      Source material for task decomposition
│                      Items remain here permanently as reference
│
├── 100_backlog/     ← Atomic tasks decomposed from epics
│                      Ready to be picked up
│
├── 200_inprogress/  ← Currently active work
 succeeded in 2.18s:
# TASK D2: Create Trade Result Text Generator

**Workstream:** D — MARKETING CONTENT ENGINE
**Epic:** Autonomous Trading Signal Platform
**Epic Sequence:** 4.2
**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
**Blocks:** none
**Readiness:** ready
**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
**Status:** [ ] Not Started

---

## Purpose

Generate marketing text from trade results.

## Input

Trade result
codex
I have the lifecycle rules and the task stub. Next I’m locating the existing marketing content code, the upstream dependency output, and the current task file structure so I can convert this task doc into the required lifecycle format before implementation.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg --files 'C:\\Users\\edebe\\eds' | rg \"signal_text|trade_result|marketing|content|autonomous_trading_signal_platform|text_generator\"" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Recurse -File 'C:\\Users\\edebe\\eds\\ep_autonomous_trading_signal_platform' | Select-Object -ExpandProperty FullName" in C:\Users\edebe\eds exited 1 in 3.68s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\workstream\200_inprogress\codex\[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mCannot find path 'C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md' because it does not exist.[0m
 exited 1 in 6.87s:
C:\Users\edebe\eds\algo_simulate\blog_trade_capture_and_gen_content_llm.py
C:\Users\edebe\eds\algo_forex\blog_trade_capture_and_gen_content_llm.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\workstreams\A\social_content_matrix.md
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\verification\generated_social_content_samples.json
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\frontend\Dockerfile
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\verify_tiktok_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\verify_model.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\test_tiktok_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_rate_limiting.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_post_thread.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_post_text.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_post_media.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_connector_init.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_twitter_auth.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_reddit_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_posting_rules.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_linkedin_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_growth_optimization_service.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_discord_connector.py
C:\Users\edebe\eds\ep_strategy_warehouse_marketing\solution\backend\tests\test_content_generation_service.py
 succeeded in 7.78s:
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\online_db_schema.sql
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_config.json
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_signal_schema.json
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\strategy_schema.json
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__init__.py
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\config.py
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\signal_sync_service.py
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\strategy_performance_sync_service.py
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\trade_result_sync_service.py
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\__init__.cpython-312.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\__init__.cpython-313.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\config.cpython-312.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\config.cpython-313.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\signal_sync_service.cpython-312.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\signal_sync_service.cpython-313.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\strategy_performance_sync_service.cpython-312.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\strategy_performance_sync_service.cpython-313.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\trade_result_sync_service.cpython-312.pyc
C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\sync_engine\__pycache__\trade_result_sync_service.cpython-313.pyc
codex
The task stub points to an upstream dependency that now lives in `300_complete`, so I’m reading that completed task and the target solution area to mirror its implementation pattern instead of inventing a new one.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"signal text|trade result text|text generator|generator\" 'C:\\Users\\edebe\\eds\\ep_autonomous_trading_signal_platform\\solution'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\ep_autonomous_trading_signal_platform\\solution'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\claude\\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md'" in C:\Users\edebe\eds succeeded in 2.98s:

    Directory: C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          10/03/2026    15:09                [44;1mjson[0m
d----          10/03/2026    15:09                [44;1msync_engine[0m
d----          10/03/2026    15:09                [44;1mtests[0m
-a---          09/03/2026    17:05           3576 online_db_schema.sql
-a---          09/03/2026    17:11           1962 sync_config.json

 exited 1 in 2.85s:

 succeeded in 4.17s:
# TASK D1: Create Signal Text Generator

**Workstream:** D — MARKETING CONTENT ENGINE
**Epic:** Autonomous Trading Signal Platform
**Status:** [ ] Awaiting User Verification

## Source
- `C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md`

## Task Summary
Generate reusable marketing text from publishable signal data and wire it into the existing PipHunter marketing flow so signal posts can be produced consistently from live signal payloads.

## Context
- `TradeApps/breakout/piphunter/marketing/content/x_poster.py`
- `TradeApps/breakout/piphunter/marketing/automation/scheduler.py`
- `TradeApps/breakout/piphunter/api/services/breakout_bridge.py`
- `TradeApps/breakout/piphunter/api/routes/signals.py`

## Plan
- [x] 1. Inspect the existing PipHunter marketing and signal data flow, then define the concrete generator target and interfaces.
codex
The current epic solution folder only contains sync services, while the upstream task for the same workstream implemented against the existing `TradeApps/breakout/piphunter` marketing pipeline. I’m verifying that target path and reading the current marketing modules before editing.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\signal_text_generator.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\x_poster.py'" in C:\Users\edebe\eds succeeded in 5.74s:
"""
Reusable generator for publishable signal marketing copy.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def _as_float(value: Any) -> Optional[float]:
    try:
        if value in (None, ""):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _format_price(value: Any) -> Optional[str]:
    numeric = _as_float(value)
 succeeded in 6.12s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          10/03/2026    02:31                [44;1m__pycache__[0m
-a---          09/03/2026    17:44            528 [32;1m__init__.py[0m
-a---          09/03/2026    17:24           2762 [32;1mcontent_queue.py[0m
-a---          09/03/2026    17:44           3210 [32;1mdiscord_poster.py[0m
-a---          09/03/2026    17:15          13051 [32;1msignal_card_renderer.py[0m
-a---          09/03/2026    17:51           8653 [32;1msignal_text_generator.py[0m
-a---          09/03/2026    17:39           3344 [32;1mtelegram_poster.py[0m
-a---          09/03/2026    22:07          12071 [32;1mx_poster.py[0m

 succeeded in 2.77s:
"""
X (Twitter) Content Poster
Automates posting trading signals and market updates to X.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from dotenv import load_dotenv

from .content_queue import ContentQueue, ContentQueueItem
from .signal_text_generator import SignalTextGenerator

load_dotenv()

# Check if tweepy is available
try:
    import tweepy
    TWEEPY_AVAILABLE = True
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\tests'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"generate_trade_closed_post|TRADE CLOSED|trade result|post trade|daily summary\" 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\tests\\test_signal_text_generator.py'" in C:\Users\edebe\eds succeeded in 3.56s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          10/03/2026    02:40                [44;1m__pycache__[0m
-a---          09/03/2026    16:53             23 [32;1m__init__.py[0m
-a---          09/03/2026    17:27           2224 [32;1mtest_content_queue.py[0m
-a---          09/03/2026    17:44           3420 [32;1mtest_discord_publisher.py[0m
-a---          09/03/2026    22:08           4164 [32;1mtest_marketing_engine.py[0m
-a---          09/03/2026    17:52           4993 [32;1mtest_posting_rules.py[0m
-a---          09/03/2026    17:20           2074 [32;1mtest_signal_card_renderer.py[0m
-a---          09/03/2026    16:53           2291 [32;1mtest_signal_text_generator.py[0m
-a---          09/03/2026    17:39           3390 [32;1mtest_telegram_publisher.py[0m
-a---          09/03/2026    17:34           3312 [32;1mtest_x_publisher.py[0m

 succeeded in 3.52s:
import unittest

from TradeApps.breakout.piphunter.marketing.content.signal_text_generator import (
    SignalTextGenerator,
)


class SignalTextGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = SignalTextGenerator(app_url="https://piphunter.app")

    def test_generates_publishable_signal_post(self) -> None:
        signal = {
            "signal_id": "sig_ab12cd",
            "asset": "GBP/USD",
            "direction": "BUY",
            "entry": 1.27145,
            "tp": 1.278,
            "sl": 1.266,
            "strategy": "breakout_rev",
 succeeded in 5.02s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\api\sync_to_supabase.py:588:        Create aggregated daily summary.
C:\Users\edebe\eds\TradeApps\breakout\piphunter\api\sync_to_supabase.py:626:            print(f"[DRY RUN] Would sync daily summary: ${record['total_pnl']:.0f} P&L, {record['signal_count']} signals")
C:\Users\edebe\eds\TradeApps\breakout\piphunter\api\sync_to_supabase.py:633:            print(f"[OK] Synced daily summary: ${record['total_pnl']:.0f} P&L, {record['signal_count']} signals")
C:\Users\edebe\eds\TradeApps\breakout\piphunter\api\sync_to_supabase.py:636:            print(f"[ERROR] Failed to sync daily summary: {e}")
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:22:[OK] Synced daily summary: $4425 P&L, 20 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:54:[OK] Synced daily summary: $5542 P&L, 20 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:87:[OK] Synced daily summary: $24372 P&L, 307 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:120:[OK] Synced daily summary: $31240 P&L, 333 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:155:[OK] Synced daily summary: $29095 P&L, 279 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:190:[OK] Synced daily summary: $30150 P&L, 274 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:225:[OK] Synced daily summary: $30150 P&L, 274 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:260:[OK] Synced daily summary: $31245 P&L, 267 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:293:[OK] Synced daily summary: $29228 P&L, 212 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:326:[OK] Synced daily summary: $29800 P&L, 212 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:360:[OK] Synced daily summary: $30420 P&L, 212 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:393:[OK] Synced daily summary: $30420 P&L, 212 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:426:[OK] Synced daily summary: $30420 P&L, 212 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:459:[OK] Synced daily summary: $31022 P&L, 199 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:491:[OK] Synced daily summary: $1655 P&L, 121 signals
C:\Users\edebe\eds\TradeApps\breakout\piphunter\sync_log.txt:521:[OK] Synced daily summary: $10445 P&L, 505 signals
codex
The codebase already has a partial trade-result formatter wired into posting rules, so this task looks like it needs hardening and explicit validation rather than a blank implementation. I’m reading the posting rules and X publisher tests now to identify the exact missing coverage and behavior gaps.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\automation\\posting_rules.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\tests\\test_x_publisher.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\tests\\test_posting_rules.py'" in C:\Users\edebe\eds succeeded in 3.15s:
"""Event-driven posting rules for PipHunter social distribution."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from TradeApps.breakout.piphunter.marketing.content import (
    ContentQueue,
    ContentQueueItem,
    DiscordPoster,
    SignalTextGenerator,
    TelegramPoster,
)
from TradeApps.breakout.piphunter.marketing.content.x_poster import XPoster


@dataclass
class PostingDispatchRecord:
    event_type: str
    platform: str
 succeeded in 3.83s:
import unittest
from pathlib import Path
from uuid import uuid4

from TradeApps.breakout.piphunter.marketing.automation.x_publisher import XPublisher
from TradeApps.breakout.piphunter.marketing.content.content_queue import ContentQueue
from TradeApps.breakout.piphunter.marketing.content.x_poster import XPoster


class StubPoster(XPoster):
    def __init__(self, responses):
        super().__init__(dry_run=True)
        self.responses = list(responses)
        self.published = []

    def publish_queue_item(self, item):
        self.published.append(item.queue_id)
        if not self.responses:
            return None
        return self.responses.pop(0)
 succeeded in 2.88s:
import unittest
from pathlib import Path
from uuid import uuid4

from TradeApps.breakout.piphunter.marketing.automation.posting_rules import PostingRulesEngine
from TradeApps.breakout.piphunter.marketing.content.content_queue import ContentQueue
from TradeApps.breakout.piphunter.marketing.content.discord_poster import DiscordPoster
from TradeApps.breakout.piphunter.marketing.content.telegram_poster import TelegramPoster
from TradeApps.breakout.piphunter.marketing.content.x_poster import XPoster


class StubXPoster(XPoster):
    def __init__(self) -> None:
        super().__init__(dry_run=True)


class StubTelegramPoster(TelegramPoster):
    def __init__(self) -> None:
        super().__init__(dry_run=True)

🌐 Searching the web...
🌐 Searched the web
codex
I’ve confirmed the trade-result generator exists but only as an internal method on the shared text generator; there’s no direct X poster entry point or dedicated test coverage for its output shape. I’m checking the package exports and the actual task stub requirements before I patch both code and lifecycle documentation in one pass.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\__init__.py'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\claude' | Where-Object {"'$_.Name -like '"'*120031*' -or "'$_.Name -like '"'*120032*' -or "'$_.Name -like '"'*120033*'} | Select-Object -ExpandProperty FullName" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\eds succeeded in 2.79s:
"""Content generation modules."""

from .content_queue import ContentQueue, ContentQueueItem
from .discord_poster import DiscordPoster
from .signal_card_renderer import SignalCardPayload, TradeCardContext, render_signal_card
from .signal_text_generator import SignalTextGenerator
from .telegram_poster import TelegramPoster

__all__ = [
    "ContentQueue",
    "ContentQueueItem",
    "DiscordPoster",
    "SignalTextGenerator",
    "SignalCardPayload",
    "TradeCardContext",
    "TelegramPoster",
    "render_signal_card",
]

 succeeded in 3.54s:
C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120032_autonomous_trading_signal_platform_workstreamD_create_signal_chart_generator.md
C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120033_autonomous_trading_signal_platform_workstreamD_create_signal_card_renderer.md
 succeeded in 6.13s:
M  DataInsights/src/Constants.py
 M TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
R  workstream/000_backlog/.keep -> workstream/000_epic/.keep
RD "workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md" -> "workstream/000_epic/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md"
RD workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md -> workstream/000_epic/20260225_104010_live_market_data_pipeline_prompt.md
RD workstream/000_backlog/20260227_022357_sFX_Technical_Design_Brief_v2.md -> workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
AD workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
AD workstream/000_epic/20260313_165611_bizPA_epic.md
AD "workstream/000_epic/20260313_165611_unassigned_Autonomous Trading Signal Platform.md"
AD workstream/000_epic/20260313_165611_unassigned_bizPA.md
A  workstream/000_epic/bizPA_disccussion.txt
R  workstream/000_backlog/claude/.keep -> workstream/000_epic/claude/.keep
A  workstream/000_epic/claude/20260305_100142_claude_etrmui_etrui_processed.md
R  workstream/000_backlog/codex/.keep -> workstream/000_epic/codex/.keep
R  workstream/000_backlog/codex/20260303_152309_codex_afrix_build_prompt_processed.md -> workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_processed.md
A  workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_review.md
R  workstream/000_backlog/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md -> workstream/000_epic/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
R  workstream/000_backlog/codex/20260304_142350_codex_linkage_verification_processed.md -> workstream/000_epic/codex/20260304_142350_codex_linkage_verification_processed.md
codex
I’m checking the publishable trade-result schema next. That will tell me whether the current formatter actually matches the intended payload contract or whether it only works for one ad hoc shape.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"publishable_trade|trade_result|realized_pnl|closed_at|exit|outcome|status\" 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\ep_autonomous_trading_signal_platform\\solution\\json\\publishable_trade_schema.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\300_complete\\20260309_120001_autonomous_trading_signal_platform_workstreamA_define_publishable_trade_result_schema.md'" in C:\Users\edebe\eds succeeded in 2.35s:
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "publishable_trade_schema.json",
  "title": "PublishableTradeResult",
  "description": "Public-facing closed trade result payload derived from local trading system trade records. Only publishable summary fields are exposed.",
  "type": "object",
  "additionalProperties": false,
  "required": [
    "trade_id",
    "signal_id",
    "open_time",
    "close_time",
    "entry_price",
    "exit_price",
    "profit_loss"
  ],
  "properties": {
    "trade_id": {
      "type": "string",
      "minLength": 1,
 succeeded in 2.78s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\plans\20260217_1615_V20260217_1615_Docker_Cloud_Deployment.md:51:    CMD curl -f http://localhost:5001/health || exit 1
C:\Users\edebe\eds\TradeApps\breakout\piphunter\plans\20260217_1615_V20260217_1615_Docker_Cloud_Deployment.md:219:| `/health` | `{"status":"healthy"}` |
C:\Users\edebe\eds\TradeApps\breakout\piphunter\supabase_schema.sql:55:    status VARCHAR(20),
C:\Users\edebe\eds\TradeApps\breakout\piphunter\supabase_schema.sql:97:    status VARCHAR(20) NOT NULL,
C:\Users\edebe\eds\TradeApps\breakout\piphunter\supabase_schema.sql:113:CREATE INDEX IF NOT EXISTS idx_live_trades_status ON live_trades(status);
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\android\gradlew.bat:85:if not ""=="%GRADLE_EXIT_CONSOLE%" exit %EXIT_CODE%
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\android\gradlew.bat:86:exit /b %EXIT_CODE%
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260228_0350_fxpilot_sortable_trades_exit_time.md:4:Enhance the expanded trade view with sortable columns and display exit time for closed trades.
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260228_0350_fxpilot_sortable_trades_exit_time.md:38:- Show exit time for CLOSED trades
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260228_0350_fxpilot_sortable_trades_exit_time.md:40:- Include exit reason if available (e.g., "TP Hit", "SL Hit")
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260228_0350_fxpilot_sortable_trades_exit_time.md:65:  <td style={{padding:"0.35rem 0.6rem",fontSize:"0.52rem",color:t.status==="CLOSED"?"#60a5fa":"#2a4060"}}>
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\android\gradlew:37:#         * compound commands having a testable exit status, especially «case»;
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\android\gradlew:87:APP_HOME=$( cd "${APP_HOME:-./}" > /dev/null && pwd -P ) || exit
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\android\gradlew:100:    exit 1
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:53:  - `exit_time` for timestamp
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:55:  - `exit_reason` for result
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:72:- Changed order from `trade_date` to `exit_time`
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:79:- Updated trade card to display: product, direction, time, net_return, exit_reason
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:91:    exit_time TIMESTAMPTZ,
C:\Users\edebe\eds\TradeApps\breakout\piphunter\workstream\300_complete\20260222_154500_piphunter_mobile_trades_and_equity.md:93:    exit_price NUMERIC,
 succeeded in 2.89s:
# TASK A2: Define Publishable Trade Result Schema

**Workstream:** A — DATA LAYER
**Epic:** Autonomous Trading Signal Platform
**Status:** [x] Complete

## Source

- [Autonomous Trading Signal Platform](C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md)

## Task Summary

Define the minimal public-facing closed trade result dataset, store it as `publishable_trade_schema.json`, and document how current local closed-trade fields map into the publishable contract.

## Context

- Local closed-trade sources currently expose internal fields such as `guid`, `created`, `last_update`, `entry_price`, `latest_price`, `net_return`, `trade_reason`, and `close_type`.
- Relevant references reviewed:
  - `db_scripts/create_combined_trades_closed_arc_pg.sql`
  - `api_server_sql/main.py`
codex
The schema confirms a real gap: the current trade-result generator doesn’t read the publishable contract fields like `profit_loss`, `entry_price`, or `exit_price`. I’m patching the generator to normalize trade-result payloads properly and adding tests around that contract plus length trimming.
codex
Plan:
1. Normalize publishable trade-result payloads in the shared marketing text generator so closed-trade posts work with the schema defined in workstream A.
2. Add focused tests for publishable trade results, legacy trade payloads, and constrained-length output.
3. Run the exact validation commands, capture results, and rewrite the lifecycle file into the required format with checklist evidence and current completion state.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\app\\app\\signal\\[id].tsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"app_url.*trade|/trade/|/results/|/signal/\" 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter'" in C:\Users\edebe\eds succeeded in 7.91s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py:31:        self.assertIn("https://piphunter.app/signal/sig_ab12cd", text)
C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py:68:        self.assertIn("https://piphunter.app/signal/sig_trim01", text)
C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py:191:            return f"{self.app_url}/signal/{payload.signal_id}"
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\app\(tabs)\index.tsx:220:            onPress={() => router.push(`/signal/${signal.id}`)}
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\app\(tabs)\signals.tsx:74:      onPress={() => router.push(`/signal/${item.id}`)}
C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\package-lock.json:3666:      "resolved": "https://registry.npmjs.org/@expo/results/-/results-1.0.0.tgz",
 exited 1 in 8.03s:
[31;1mGet-Content: [0m
[31;1m[36;1mLine |[0m
[31;1m[36;1m[36;1m   2 | [0m [36;1mGet-Content -Raw 'C:\Users\edebe\eds\TradeApps\breakout\piphunter\app[0m …[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m     | [31;1m ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~[0m
[31;1m[36;1m[36;1m[0m[36;1m[0m[36;1m[31;1m[31;1m[36;1m     | [31;1mAn object at the specified path C:\Users\edebe\eds\TradeApps\breakout\piphunter\app\app\signal\[id].tsx does not exist, or has been filtered by the -Include or -Exclude parameter.[0m
codex
I’m editing the shared formatter and its tests now. The code change is scoped to the marketing content generator and its unit coverage; the lifecycle file update will follow once the validation output is in hand.
file update
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py
@@ -38,2 +38,17 @@
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
@@ -44,2 +59,3 @@
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
@@ -50,2 +66,3 @@
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
@@ -71,3 +88,4 @@
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
@@ -82,2 +100,3 @@
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
@@ -112,3 +131,4 @@
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
@@ -124,3 +144,3 @@
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
@@ -188,2 +208,32 @@
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
@@ -199,9 +249,15 @@
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
apply_patch(auto_approved=true) exited 0 in 4.48s:
Success. Updated the following files:
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:

file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:

file update
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py
@@ -69,2 +69,60 @@
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
apply_patch(auto_approved=true) exited 0 in 1.74s:
Success. Updated the following files:
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()

file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()

codex
The formatter and its tests are patched. I’m running syntax and unit validation now so I can record exact evidence in the lifecycle file instead of backfilling it loosely.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "python -m py_compile 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\signal_text_generator.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\x_poster.py'" in C:\Users\edebe\eds succeeded in 3.21s:

 succeeded in 4.54s:
test_generates_publishable_signal_post (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_generates_publishable_signal_post) ... ok
test_generates_publishable_trade_result_post (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_generates_publishable_trade_result_post) ... ok
test_supports_existing_breakout_bridge_signal_shape (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_supports_existing_breakout_bridge_signal_shape) ... ok
test_supports_existing_trade_result_shape (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_supports_existing_trade_result_shape) ... ok
test_trade_post_trims_to_requested_length (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_trade_post_trims_to_requested_length) ... ok
test_trims_to_requested_length (TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator.SignalTextGeneratorTests.test_trims_to_requested_length) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.001s

OK
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()

codex
The direct generator tests passed. I’m running the posting-rules regression as a second check because this formatter is consumed through the multi-platform dispatch path, not just unit calls.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v' in C:\Users\edebe\eds succeeded in 4.26s:
Warning: tweepy not installed. X posting will be in dry-run mode.
Warning: tweepy not installed. X posting will be in dry-run mode.

[DRY RUN] 2026-03-19 16:31:06 - Would post daily_summary:
----------------------------------------
DAILY SUMMARY

Net +126 | Signals 8 | Win rate 62%
Leader USD/JPY

See the full board: https://piphunter.app

#DailySummary #ForexSignals #PipHunter
----------------------------------------

[DRY RUN] 2026-03-19 16:31:06 - Would post daily_summary to Telegram:
----------------------------------------
DAILY SUMMARY

Net +126 | Signals 8 | Win rate 62%
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()

codex
I have the validation output needed for the task record. I’m rewriting the assigned lifecycle file into the required structure now, with checked steps for completed work and an explicit pending user-verification step so the status is accurate.
file update
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
# TASK D2: Create Trade Result Text Generator

**Workstream:** D — MARKETING CONTENT ENGINE
**Epic:** Autonomous Trading Signal Platform
**Epic Sequence:** 4.2
**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
**Blocks:** none
**Readiness:** ready
**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
**Status:** [ ] Not Started

---

## Purpose

Generate marketing text from trade results.

## Input

Trade result

## Output

Result post text

## Verification

- [ ] Trade results formatted

---

## Notes

_Add implementation notes here_


## Execution Evidence
- Agent lane: claude
- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
- Return code: 0
- Stdout:
```text
claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 2.47s:
Success. Updated the following files:
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
deleted file mode 100644
index 21b0431d346fa824ec104af8d7d68865b38e0efe..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ /dev/null
@@ -1,49 +0,0 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
deleted file mode 100644
index 21b0431d346fa824ec104af8d7d68865b38e0efe..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ /dev/null
@@ -1,49 +0,0 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
# TASK D2: Create Trade Result Text Generator

**Workstream:** D - MARKETING CONTENT ENGINE
**Epic:** Autonomous Trading Signal Platform
**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
**Context:**
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`

## Plan
- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
- [x] 3. Add automated validation for publishable trade results, legacy trade payloads, and posting-rules integration.
  - [x] Test: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
  - Evidence: `Ran 6 tests in 0.001s` and `OK`, covering publishable signal payloads, publishable trade results, legacy trade payloads, and trim behavior.
- [ ] 4. Request user verification for the user-visible trade-result copy changes before moving the task to `300_complete`.
  - [ ] Test: User provides pass/fail feedback for the implemented trade-result formatting behaviors listed in `Validation`.
  - Evidence: Pending user verification.

## Evidence
Objective-Delivery-Coverage: 90%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
  - Objective-Proved: The trade-result formatter now accepts the publishable trade schema, preserves legacy payload support, and has direct automated coverage for closed-trade post output.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
  - Objective-Proved: The generator passes direct unit validation for publishable trade-result formatting, legacy trade-result formatting, and URL-preserving length trimming.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
  - Objective-Proved: The updated trade-result text flows through the multi-platform posting-rules engine without regressions.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User verification request pending in final response for the generated trade-result copy.
  - Objective-Proved: Confirms the user-visible copy tone and formatting meet expectations in actual review.
  - Status: planned

## Implementation Log
- 2026-03-19 16:26 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task stub, then inspected the completed upstream signal-text task to reuse the established implementation pattern.
- 2026-03-19 16:28 GMT: Reviewed `publishable_trade_schema.json`, `signal_text_generator.py`, `posting_rules.py`, and the existing marketing tests to identify the trade-result normalization gap.
- 2026-03-19 16:30 GMT: Updated `signal_text_generator.py` to normalize `entry_price`, `exit_price`, `profit_loss`, and `trade_id`, added dedicated trade detail/instrument formatting, and fixed trade P&L formatting for small decimal values.
- 2026-03-19 16:30 GMT: Expanded `test_signal_text_generator.py` with publishable trade-result, legacy trade-result, and trade trimming test coverage.
- 2026-03-19 16:31 GMT: Ran `py_compile`, direct generator tests, and posting-rules regression successfully.
- 2026-03-19 16:32 GMT: Replaced the original task stub with the required lifecycle structure and recorded the original stub metadata below.
- Original stub metadata preserved:
  - Workstream: D - MARKETING CONTENT ENGINE
  - Epic Sequence: 4.2
  - Depends On: `20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
  - Blocks: none
  - Readiness: ready
  - Epic Output Folder: `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform`
  - Initial Verification Checkbox: `Trade results formatted`
  - Original Execution Evidence: `cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md` returned exit code `0`
  - Original Retry History: `Retry-Count: 1`, retry scheduled at `2026-03-18 17:21:29`

## Changes Made
- Updated `SignalTextPayload` in `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py` to normalize trade-result aliases for:
  - `entry_price -> entry`
  - `exit_price/latest_price -> exit_price`
  - `profit_loss -> trade result P&L`
  - `trade_id/guid -> trade_id`
- Added `_format_signed_value()` so trade-result posts keep small decimal profit/loss values instead of rounding them down to `0`.
- Added `_build_trade_detail_line()` and `_instrument_line()` so closed-trade posts can render meaningful entry/exit details even when the publishable schema does not include asset or direction fields.
- Extended `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py` with:
  - a publishable trade-result schema test,
  - a legacy trade payload compatibility test,
  - a trade-result trimming test that preserves the review URL.

## Validation
- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
  - Result: Pass. Exit code `0`.
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
  - Result: Pass. Output summary: `Ran 6 tests in 0.001s` / `OK`.
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
  - Result: Pass. Output summary: `Ran 4 tests in 0.530s` / `OK`.
  - Notable dry-run evidence: the trade-closed dispatch printed `TRADE CLOSED`, `WIN | Move +31 pips`, and the review URL across X, Telegram, and Discord.
- User verification requested: confirm pass/fail for each behavior below before this task is moved to `300_complete`.
  - Behavior 1: publishable trade-result payloads generate closed-trade posts that include the realized result plus entry/exit pricing.
  - Behavior 2: existing trade-result payloads still generate valid posts for the posting-rules engine without extra caller-side mapping.
  - Behavior 3: shortened trade-result posts preserve the review URL instead of truncating the destination link.

## Risks/Notes
- The publishable trade-result schema does not include asset or direction, so trade posts fall back to generic identifiers when those fields are absent from the payload.
- No live platform post was executed; validation was limited to syntax checks and local dry-run/unit-test coverage.
- Because this changes user-visible marketing copy, user verification is still required before completion.

## Completion Status
Awaiting user verification as of 2026-03-19 16:32 GMT. Implementation and technical validation are complete; do not move this task to `300_complete` until user pass/fail feedback is captured.
apply_patch(auto_approved=true) exited 0 in 814ms:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
index 21b0431d346fa824ec104af8d7d68865b38e0efe..960f0c9e817944f84df4632f1af685a2309ea52c
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
@@ -1,49 +1,98 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# TASK D2: Create Trade Result Text Generator
+
+**Workstream:** D - MARKETING CONTENT ENGINE
+**Epic:** Autonomous Trading Signal Platform
+**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
+**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
+**Context:**
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
+- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
+**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+
+## Plan
+- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
+  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
+  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
+- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
+  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
+- [x] 3. Add automated validation for publishable trade results, legacy trade payloads, and posting-rules integration.
+  - [x] Test: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Evidence: `Ran 6 tests in 0.001s` and `OK`, covering publishable signal payloads, publishable trade results, legacy trade payloads, and trim behavior.
+- [ ] 4. Request user verification for the user-visible trade-result copy changes before moving the task to `300_complete`.
+  - [ ] Test: User provides pass/fail feedback for the implemented trade-result formatting behaviors listed in `Validation`.
+  - Evidence: Pending user verification.
+
+## Evidence
+Objective-Delivery-Coverage: 90%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+  - Objective-Proved: The trade-result formatter now accepts the publishable trade schema, preserves legacy payload support, and has direct automated coverage for closed-trade post output.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Objective-Proved: The generator passes direct unit validation for publishable trade-result formatting, legacy trade-result formatting, and URL-preserving length trimming.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Objective-Proved: The updated trade-result text flows through the multi-platform posting-rules engine without regressions.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request pending in final response for the generated trade-result copy.
+  - Objective-Proved: Confirms the user-visible copy tone and formatting meet expectations in actual review.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:26 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task stub, then inspected the completed upstream signal-text task to reuse the established implementation pattern.
+- 2026-03-19 16:28 GMT: Reviewed `publishable_trade_schema.json`, `signal_text_generator.py`, `posting_rules.py`, and the existing marketing tests to identify the trade-result normalization gap.
+- 2026-03-19 16:30 GMT: Updated `signal_text_generator.py` to normalize `entry_price`, `exit_price`, `profit_loss`, and `trade_id`, added dedicated trade detail/instrument formatting, and fixed trade P&L formatting for small decimal values.
+- 2026-03-19 16:30 GMT: Expanded `test_signal_text_generator.py` with publishable trade-result, legacy trade-result, and trade trimming test coverage.
+- 2026-03-19 16:31 GMT: Ran `py_compile`, direct generator tests, and posting-rules regression successfully.
+- 2026-03-19 16:32 GMT: Replaced the original task stub with the required lifecycle structure and recorded the original stub metadata below.
+- Original stub metadata preserved:
+  - Workstream: D - MARKETING CONTENT ENGINE
+  - Epic Sequence: 4.2
+  - Depends On: `20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+  - Blocks: none
+  - Readiness: ready
+  - Epic Output Folder: `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform`
+  - Initial Verification Checkbox: `Trade results formatted`
+  - Original Execution Evidence: `cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md` returned exit code `0`
+  - Original Retry History: `Retry-Count: 1`, retry scheduled at `2026-03-18 17:21:29`
+
+## Changes Made
+- Updated `SignalTextPayload` in `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py` to normalize trade-result aliases for:
+  - `entry_price -> entry`
+  - `exit_price/latest_price -> exit_price`
+  - `profit_loss -> trade result P&L`
+  - `trade_id/guid -> trade_id`
+- Added `_format_signed_value()` so trade-result posts keep small decimal profit/loss values instead of rounding them down to `0`.
+- Added `_build_trade_detail_line()` and `_instrument_line()` so closed-trade posts can render meaningful entry/exit details even when the publishable schema does not include asset or direction fields.
+- Extended `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py` with:
+  - a publishable trade-result schema test,
+  - a legacy trade payload compatibility test,
+  - a trade-result trimming test that preserves the review URL.
+
+## Validation
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Result: Pass. Exit code `0`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Result: Pass. Output summary: `Ran 6 tests in 0.001s` / `OK`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Result: Pass. Output summary: `Ran 4 tests in 0.530s` / `OK`.
+  - Notable dry-run evidence: the trade-closed dispatch printed `TRADE CLOSED`, `WIN | Move +31 pips`, and the review URL across X, Telegram, and Discord.
+- User verification requested: confirm pass/fail for each behavior below before this task is moved to `300_complete`.
+  - Behavior 1: publishable trade-result payloads generate closed-trade posts that include the realized result plus entry/exit pricing.
+  - Behavior 2: existing trade-result payloads still generate valid posts for the posting-rules engine without extra caller-side mapping.
+  - Behavior 3: shortened trade-result posts preserve the review URL instead of truncating the destination link.
+
+## Risks/Notes
+- The publishable trade-result schema does not include asset or direction, so trade posts fall back to generic identifiers when those fields are absent from the payload.
+- No live platform post was executed; validation was limited to syntax checks and local dry-run/unit-test coverage.
+- Because this changes user-visible marketing copy, user verification is still required before completion.
+
+## Completion Status
+Awaiting user verification as of 2026-03-19 16:32 GMT. Implementation and technical validation are complete; do not move this task to `300_complete` until user pass/fail feedback is captured.

file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
index 21b0431d346fa824ec104af8d7d68865b38e0efe..960f0c9e817944f84df4632f1af685a2309ea52c
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
@@ -1,49 +1,98 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# TASK D2: Create Trade Result Text Generator
+
+**Workstream:** D - MARKETING CONTENT ENGINE
+**Epic:** Autonomous Trading Signal Platform
+**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
+**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
+**Context:**
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
+- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
+**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+
+## Plan
+- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
+  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
+  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
+- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
+  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
+- [x] 3. Add automated validation for publishable trade results, legacy trade payloads, and posting-rules integration.
+  - [x] Test: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Evidence: `Ran 6 tests in 0.001s` and `OK`, covering publishable signal payloads, publishable trade results, legacy trade payloads, and trim behavior.
+- [ ] 4. Request user verification for the user-visible trade-result copy changes before moving the task to `300_complete`.
+  - [ ] Test: User provides pass/fail feedback for the implemented trade-result formatting behaviors listed in `Validation`.
+  - Evidence: Pending user verification.
+
+## Evidence
+Objective-Delivery-Coverage: 90%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+  - Objective-Proved: The trade-result formatter now accepts the publishable trade schema, preserves legacy payload support, and has direct automated coverage for closed-trade post output.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Objective-Proved: The generator passes direct unit validation for publishable trade-result formatting, legacy trade-result formatting, and URL-preserving length trimming.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Objective-Proved: The updated trade-result text flows through the multi-platform posting-rules engine without regressions.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request pending in final response for the generated trade-result copy.
+  - Objective-Proved: Confirms the user-visible copy tone and formatting meet expectations in actual review.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:26 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task stub, then inspected the completed upstream signal-text task to reuse the established implementation pattern.
+- 2026-03-19 16:28 GMT: Reviewed `publishable_trade_schema.json`, `signal_text_generator.py`, `posting_rules.py`, and the existing marketing tests to identify the trade-result normalization gap.
+- 2026-03-19 16:30 GMT: Updated `signal_text_generator.py` to normalize `entry_price`, `exit_price`, `profit_loss`, and `trade_id`, added dedicated trade detail/instrument formatting, and fixed trade P&L formatting for small decimal values.
+- 2026-03-19 16:30 GMT: Expanded `test_signal_text_generator.py` with publishable trade-result, legacy trade-result, and trade trimming test coverage.
+- 2026-03-19 16:31 GMT: Ran `py_compile`, direct generator tests, and posting-rules regression successfully.
+- 2026-03-19 16:32 GMT: Replaced the original task stub with the required lifecycle structure and recorded the original stub metadata below.
+- Original stub metadata preserved:
+  - Workstream: D - MARKETING CONTENT ENGINE
+  - Epic Sequence: 4.2
+  - Depends On: `20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+  - Blocks: none
+  - Readiness: ready
+  - Epic Output Folder: `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform`
+  - Initial Verification Checkbox: `Trade results formatted`
+  - Original Execution Evidence: `cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md` returned exit code `0`
+  - Original Retry History: `Retry-Count: 1`, retry scheduled at `2026-03-18 17:21:29`
+
+## Changes Made
+- Updated `SignalTextPayload` in `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py` to normalize trade-result aliases for:
+  - `entry_price -> entry`
+  - `exit_price/latest_price -> exit_price`
+  - `profit_loss -> trade result P&L`
+  - `trade_id/guid -> trade_id`
+- Added `_format_signed_value()` so trade-result posts keep small decimal profit/loss values instead of rounding them down to `0`.
+- Added `_build_trade_detail_line()` and `_instrument_line()` so closed-trade posts can render meaningful entry/exit details even when the publishable schema does not include asset or direction fields.
+- Extended `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py` with:
+  - a publishable trade-result schema test,
+  - a legacy trade payload compatibility test,
+  - a trade-result trimming test that preserves the review URL.
+
+## Validation
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Result: Pass. Exit code `0`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Result: Pass. Output summary: `Ran 6 tests in 0.001s` / `OK`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Result: Pass. Output summary: `Ran 4 tests in 0.530s` / `OK`.
+  - Notable dry-run evidence: the trade-closed dispatch printed `TRADE CLOSED`, `WIN | Move +31 pips`, and the review URL across X, Telegram, and Discord.
+- User verification requested: confirm pass/fail for each behavior below before this task is moved to `300_complete`.
+  - Behavior 1: publishable trade-result payloads generate closed-trade posts that include the realized result plus entry/exit pricing.
+  - Behavior 2: existing trade-result payloads still generate valid posts for the posting-rules engine without extra caller-side mapping.
+  - Behavior 3: shortened trade-result posts preserve the review URL instead of truncating the destination link.
+
+## Risks/Notes
+- The publishable trade-result schema does not include asset or direction, so trade posts fall back to generic identifiers when those fields are absent from the payload.
+- No live platform post was executed; validation was limited to syntax checks and local dry-run/unit-test coverage.
+- Because this changes user-visible marketing copy, user verification is still required before completion.
+
+## Completion Status
+Awaiting user verification as of 2026-03-19 16:32 GMT. Implementation and technical validation are complete; do not move this task to `300_complete` until user pass/fail feedback is captured.

codex
The code and lifecycle record are updated. I’m doing one quick pass over the diff for the touched files only, then I’ll close with the validation status and the specific user verification still required by the lifecycle gate.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\content\\signal_text_generator.py' 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\marketing\\tests\\test_signal_text_generator.py' 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Raw 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md'" in C:\Users\edebe\eds succeeded in 1.71s:

 succeeded in 1.53s:
# TASK D2: Create Trade Result Text Generator

**Workstream:** D - MARKETING CONTENT ENGINE
**Epic:** Autonomous Trading Signal Platform
**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
**Context:**
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`

## Plan
- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
index 21b0431d346fa824ec104af8d7d68865b38e0efe..960f0c9e817944f84df4632f1af685a2309ea52c
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
@@ -1,49 +1,98 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# TASK D2: Create Trade Result Text Generator
+
+**Workstream:** D - MARKETING CONTENT ENGINE
+**Epic:** Autonomous Trading Signal Platform
+**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
+**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
+**Context:**
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
+- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
+**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+
+## Plan
+- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
+  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
+  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
+- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
+  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
+- [x] 3. Add automated validation for publishable trade results, legacy trade payloads, and posting-rules integration.
+  - [x] Test: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Evidence: `Ran 6 tests in 0.001s` and `OK`, covering publishable signal payloads, publishable trade results, legacy trade payloads, and trim behavior.
+- [ ] 4. Request user verification for the user-visible trade-result copy changes before moving the task to `300_complete`.
+  - [ ] Test: User provides pass/fail feedback for the implemented trade-result formatting behaviors listed in `Validation`.
+  - Evidence: Pending user verification.
+
+## Evidence
+Objective-Delivery-Coverage: 90%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+  - Objective-Proved: The trade-result formatter now accepts the publishable trade schema, preserves legacy payload support, and has direct automated coverage for closed-trade post output.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Objective-Proved: The generator passes direct unit validation for publishable trade-result formatting, legacy trade-result formatting, and URL-preserving length trimming.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Objective-Proved: The updated trade-result text flows through the multi-platform posting-rules engine without regressions.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request pending in final response for the generated trade-result copy.
+  - Objective-Proved: Confirms the user-visible copy tone and formatting meet expectations in actual review.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:26 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task stub, then inspected the completed upstream signal-text task to reuse the established implementation pattern.
+- 2026-03-19 16:28 GMT: Reviewed `publishable_trade_schema.json`, `signal_text_generator.py`, `posting_rules.py`, and the existing marketing tests to identify the trade-result normalization gap.
+- 2026-03-19 16:30 GMT: Updated `signal_text_generator.py` to normalize `entry_price`, `exit_price`, `profit_loss`, and `trade_id`, added dedicated trade detail/instrument formatting, and fixed trade P&L formatting for small decimal values.
+- 2026-03-19 16:30 GMT: Expanded `test_signal_text_generator.py` with publishable trade-result, legacy trade-result, and trade trimming test coverage.
+- 2026-03-19 16:31 GMT: Ran `py_compile`, direct generator tests, and posting-rules regression successfully.
+- 2026-03-19 16:32 GMT: Replaced the original task stub with the required lifecycle structure and recorded the original stub metadata below.
+- Original stub metadata preserved:
+  - Workstream: D - MARKETING CONTENT ENGINE
+  - Epic Sequence: 4.2
+  - Depends On: `20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+  - Blocks: none
+  - Readiness: ready
+  - Epic Output Folder: `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform`
+  - Initial Verification Checkbox: `Trade results formatted`
+  - Original Execution Evidence: `cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md` returned exit code `0`
+  - Original Retry History: `Retry-Count: 1`, retry scheduled at `2026-03-18 17:21:29`
+
+## Changes Made
+- Updated `SignalTextPayload` in `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py` to normalize trade-result aliases for:
+  - `entry_price -> entry`
+  - `exit_price/latest_price -> exit_price`
+  - `profit_loss -> trade result P&L`
+  - `trade_id/guid -> trade_id`
+- Added `_format_signed_value()` so trade-result posts keep small decimal profit/loss values instead of rounding them down to `0`.
+- Added `_build_trade_detail_line()` and `_instrument_line()` so closed-trade posts can render meaningful entry/exit details even when the publishable schema does not include asset or direction fields.
+- Extended `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py` with:
+  - a publishable trade-result schema test,
+  - a legacy trade payload compatibility test,
+  - a trade-result trimming test that preserves the review URL.
+
+## Validation
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Result: Pass. Exit code `0`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Result: Pass. Output summary: `Ran 6 tests in 0.001s` / `OK`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Result: Pass. Output summary: `Ran 4 tests in 0.530s` / `OK`.
+  - Notable dry-run evidence: the trade-closed dispatch printed `TRADE CLOSED`, `WIN | Move +31 pips`, and the review URL across X, Telegram, and Discord.
+- User verification requested: confirm pass/fail for each behavior below before this task is moved to `300_complete`.
+  - Behavior 1: publishable trade-result payloads generate closed-trade posts that include the realized result plus entry/exit pricing.
+  - Behavior 2: existing trade-result payloads still generate valid posts for the posting-rules engine without extra caller-side mapping.
+  - Behavior 3: shortened trade-result posts preserve the review URL instead of truncating the destination link.
+
+## Risks/Notes
+- The publishable trade-result schema does not include asset or direction, so trade posts fall back to generic identifiers when those fields are absent from the payload.
+- No live platform post was executed; validation was limited to syntax checks and local dry-run/unit-test coverage.
+- Because this changes user-visible marketing copy, user verification is still required before completion.
+
+## Completion Status
+Awaiting user verification as of 2026-03-19 16:32 GMT. Implementation and technical validation are complete; do not move this task to `300_complete` until user pass/fail feedback is captured.

codex
Implemented the trade-result text generator updates in [signal_text_generator.py](C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py) and expanded coverage in [test_signal_text_generator.py](C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py). The formatter now supports the publishable trade schema fields (`profit_loss`, `entry_price`, `exit_price`, `trade_id`), preserves legacy trade payloads, and keeps small decimal P&L values instead of rounding them to zero. I also updated the lifecycle record and checklist in [20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md).

Validation passed:
- `python -m py_compile ...signal_text_generator.py ...x_poster.py`
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`

The task remains in `200_inprogress` because the lifecycle gate requires user verification for this user-visible copy change. Reply with pass/fail for:
1. Publishable trade-result payloads now generate sensible closed-trade posts with realized result plus entry/exit pricing.
2. Existing trade-result payloads still generate valid posts without extra mapping.
3. Shortened trade-result posts preserve the review URL.
file update:
diff --git a/breakout/piphunter/marketing/content/signal_text_generator.py b/breakout/piphunter/marketing/content/signal_text_generator.py
index 299fda2ffd76b07e06098b0ce1b6b71dc1ef6e7c..c727535fe4331e5f66f213e85870263a4f64ec7a
--- a/breakout/piphunter/marketing/content/signal_text_generator.py
+++ b/breakout/piphunter/marketing/content/signal_text_generator.py
@@ -36,18 +36,35 @@
     return f"{prefix}{rounded}{suffix}"
 
 
+def _format_signed_value(value: Any) -> Optional[str]:
+    numeric = _as_float(value)
+    if numeric is None:
+        return None
+
+    formatted = _format_price(abs(numeric))
+    if formatted is None:
+        return None
+
+    prefix = "+" if numeric > 0 else "-" if numeric < 0 else ""
+    if prefix:
+        return f"{prefix}{formatted}"
+    return formatted
+
+
 @dataclass(frozen=True)
 class SignalTextPayload:
     asset: str
     direction: str
     confidence: Optional[int]
     entry: Optional[str]
+    exit_price: Optional[str]
     take_profit: Optional[str]
     stop_loss: Optional[str]
     strategy: Optional[str]
     strategy_hint: Optional[str]
     potential_pips: Optional[str]
     signal_id: Optional[str]
+    trade_id: Optional[str]
 
     @classmethod
     def from_signal(cls, signal: Dict[str, Any]) -> "SignalTextPayload":
@@ -69,7 +86,8 @@
             asset=str(asset),
             direction=direction,
             confidence=confidence,
-            entry=_format_price(signal.get("entry")),
+            entry=_format_price(signal.get("entry") or signal.get("entry_price")),
+            exit_price=_format_price(signal.get("exit_price") or signal.get("latest_price")),
             take_profit=_format_price(signal.get("tp") or signal.get("take_profit")),
             stop_loss=_format_price(signal.get("sl") or signal.get("stop_loss")),
             strategy=signal.get("strategy") or signal.get("strategy_name"),
@@ -80,6 +98,7 @@
                 else _format_signed_int(signal.get("expected_pips"), " pips")
             ),
             signal_id=signal.get("signal_id") or signal.get("id"),
+            trade_id=signal.get("trade_id") or signal.get("guid"),
         )
 
 
@@ -110,7 +129,8 @@
     def generate_trade_closed_post(self, trade: Dict[str, Any], max_length: int = 280) -> str:
         payload = SignalTextPayload.from_signal(trade)
         result_text = self._trade_result_text(trade)
-        body_lines: List[str] = ["TRADE CLOSED", "", f"{payload.asset} {payload.direction}".strip()]
+        instrument_line = self._instrument_line(payload, fallback_label="Closed trade")
+        body_lines: List[str] = ["TRADE CLOSED", "", instrument_line]
 
         stat_parts: List[str] = []
         if result_text:
@@ -122,7 +142,7 @@
         if stat_parts:
             body_lines.append(" | ".join(stat_parts))
 
-        detail_line = self._build_detail_line(payload)
+        detail_line = self._build_trade_detail_line(payload)
         if detail_line:
             body_lines.append(detail_line)
 
@@ -186,6 +206,36 @@
             return None
         return " | ".join(parts)
 
+    def _build_trade_detail_line(self, payload: SignalTextPayload) -> Optional[str]:
+        parts: List[str] = []
+        if payload.entry:
+            parts.append(f"Entry {payload.entry}")
+        if payload.exit_price:
+            parts.append(f"Exit {payload.exit_price}")
+        elif payload.take_profit:
+            parts.append(f"Exit {payload.take_profit}")
+        if payload.strategy_hint:
+            parts.append(payload.strategy_hint)
+        elif payload.strategy:
+            parts.append(str(payload.strategy))
+        if not parts:
+            return None
+        return " | ".join(parts)
+
+    def _instrument_line(self, payload: SignalTextPayload, fallback_label: str) -> str:
+        parts = [payload.asset]
+        if payload.direction and payload.direction != "NEUTRAL":
+            parts.append(payload.direction)
+
+        text = " ".join(part for part in parts if part).strip()
+        if text and text != "Unknown":
+            return text
+        if payload.trade_id:
+            return f"Trade {payload.trade_id}"
+        if payload.signal_id:
+            return f"Signal {payload.signal_id}"
+        return fallback_label
+
     def _signal_url(self, payload: SignalTextPayload) -> str:
         if payload.signal_id:
             return f"{self.app_url}/signal/{payload.signal_id}"
@@ -197,13 +247,19 @@
             if value not in (None, ""):
                 return str(value).upper()
 
-        pnl = _as_float(trade.get("realized_pnl") or trade.get("net_pnl") or trade.get("pnl"))
+        pnl = _as_float(
+            trade.get("realized_pnl")
+            or trade.get("net_pnl")
+            or trade.get("pnl")
+            or trade.get("profit_loss")
+        )
         if pnl is None:
             return None
+        formatted_pnl = _format_signed_value(pnl)
         if pnl > 0:
-            return f"WIN {int(round(pnl)):+d}"
+            return f"WIN {formatted_pnl}"
         if pnl < 0:
-            return f"LOSS {int(round(pnl)):+d}"
+            return f"LOSS {formatted_pnl}"
         return "FLAT 0"
 
     def _fit_to_length(self, lines: List[str], max_length: int) -> str:
diff --git a/breakout/piphunter/marketing/tests/test_signal_text_generator.py b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
index a8392064122c820256f949967484afadb810b1d3..960d6065caf1f1c2f9c0ff047cd9a32fdbf5f46c
--- a/breakout/piphunter/marketing/tests/test_signal_text_generator.py
+++ b/breakout/piphunter/marketing/tests/test_signal_text_generator.py
@@ -67,6 +67,64 @@
         self.assertLessEqual(len(text), 180)
         self.assertIn("https://piphunter.app/signal/sig_trim01", text)
 
+    def test_generates_publishable_trade_result_post(self) -> None:
+        trade = {
+            "trade_id": "trade_ab12",
+            "signal_id": "sig_trade01",
+            "open_time": "2026-03-08T18:49:52Z",
+            "close_time": "2026-03-08T19:19:12Z",
+            "entry_price": 2.455702,
+            "exit_price": 2.45879,
+            "profit_loss": 0.003088,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("TRADE CLOSED", text)
+        self.assertIn("WIN +0.00309", text)
+        self.assertIn("Entry 2.4557", text)
+        self.assertIn("Exit 2.4588", text)
+        self.assertIn("https://piphunter.app/signal/sig_trade01", text)
+        self.assertLessEqual(len(text), 280)
+
+    def test_supports_existing_trade_result_shape(self) -> None:
+        trade = {
+            "signal_id": "sig_rule_02",
+            "asset": "EUR/USD",
+            "direction": "SELL",
+            "result": "win",
+            "net_pnl": 48,
+            "expected_pips": 31,
+            "entry": 1.08125,
+            "exit_price": 1.07645,
+        }
+
+        text = self.generator.generate_trade_closed_post(trade)
+
+        self.assertIn("EUR/USD SELL", text)
+        self.assertIn("WIN", text)
+        self.assertIn("Move +31 pips", text)
+        self.assertIn("Exit 1.0764", text)
+
+    def test_trade_post_trims_to_requested_length(self) -> None:
+        trade = {
+            "trade_id": "trade_trim_01",
+            "signal_id": "sig_trade_trim",
+            "asset": "GBP/JPY",
+            "direction": "BUY",
+            "status": "take profit hit after volatility expansion",
+            "profit_loss": 127.456,
+            "expected_pips": 88,
+            "entry_price": 191.245,
+            "exit_price": 192.62,
+            "strategy_hint": "London breakout continuation with macro catalyst follow-through",
+        }
+
+        text = self.generator.generate_trade_closed_post(trade, max_length=180)
+
+        self.assertLessEqual(len(text), 180)
+        self.assertIn("https://piphunter.app/signal/sig_trade_trim", text)
+
 
 if __name__ == "__main__":
     unittest.main()
diff --git a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
index 21b0431d346fa824ec104af8d7d68865b38e0efe..960f0c9e817944f84df4632f1af685a2309ea52c
--- a/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
+++ b/workstream/200_inprogress/codex/20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
@@ -1,49 +1,98 @@
-# TASK D2: Create Trade Result Text Generator
-
-**Workstream:** D — MARKETING CONTENT ENGINE
-**Epic:** Autonomous Trading Signal Platform
-**Epic Sequence:** 4.2
-**Depends On:** 20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md
-**Blocks:** none
-**Readiness:** ready
-**Epic Output Folder:** C:\Users\edebe\eds\ep_autonomous_trading_signal_platform
-**Status:** [ ] Not Started
-
----
-
-## Purpose
-
-Generate marketing text from trade results.
-
-## Input
-
-Trade result
-
-## Output
-
-Result post text
-
-## Verification
-
-- [ ] Trade results formatted
-
----
-
-## Notes
-
-_Add implementation notes here_
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# TASK D2: Create Trade Result Text Generator
+
+**Workstream:** D - MARKETING CONTENT ENGINE
+**Epic:** Autonomous Trading Signal Platform
+**Source:** Assigned task file `C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md`
+**Task Summary:** Normalize publishable trade-result payloads into reusable marketing copy, preserve compatibility with the existing PipHunter marketing pipeline, and validate the generated closed-trade posts.
+**Context:**
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\automation\posting_rules.py`
+- `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution\json\publishable_trade_schema.json`
+**Dependency:** `C:\Users\edebe\eds\workstream\300_complete\claude\20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+
+## Plan
+- [x] 1. Inspect the upstream signal-text implementation, the current PipHunter trade-post flow, and the publishable trade-result schema to identify the formatter gap.
+  - [x] Test: `rg -n "generate_trade_closed_post|trade_closed|profit_loss|entry_price|exit_price" C:\Users\edebe\eds\TradeApps\breakout\piphunter C:\Users\edebe\eds\ep_autonomous_trading_signal_platform\solution -S` returns the active generator integration points and the trade schema fields to support.
+  - Evidence: Confirmed `PostingRulesEngine.handle_event("trade_closed", ...)` already routes through `SignalTextGenerator.generate_trade_closed_post()`, while `publishable_trade_schema.json` uses `profit_loss`, `entry_price`, and `exit_price` fields that the existing formatter did not normalize.
+- [x] 2. Update the shared text generator to support publishable trade-result payloads and retain compatibility with the existing trade payload shape.
+  - [x] Test: `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Evidence: `py_compile` completed with exit code `0` after adding trade-result field normalization (`profit_loss`, `entry_price`, `exit_price`, `trade_id`) and a dedicated trade-detail formatter.
+- [x] 3. Add automated validation for publishable trade results, legacy trade payloads, and posting-rules integration.
+  - [x] Test: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Evidence: `Ran 6 tests in 0.001s` and `OK`, covering publishable signal payloads, publishable trade results, legacy trade payloads, and trim behavior.
+- [ ] 4. Request user verification for the user-visible trade-result copy changes before moving the task to `300_complete`.
+  - [ ] Test: User provides pass/fail feedback for the implemented trade-result formatting behaviors listed in `Validation`.
+  - Evidence: Pending user verification.
+
+## Evidence
+Objective-Delivery-Coverage: 90%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`, `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py`
+  - Objective-Proved: The trade-result formatter now accepts the publishable trade schema, preserves legacy payload support, and has direct automated coverage for closed-trade post output.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Objective-Proved: The generator passes direct unit validation for publishable trade-result formatting, legacy trade-result formatting, and URL-preserving length trimming.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Objective-Proved: The updated trade-result text flows through the multi-platform posting-rules engine without regressions.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request pending in final response for the generated trade-result copy.
+  - Objective-Proved: Confirms the user-visible copy tone and formatting meet expectations in actual review.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:26 GMT: Read `skills/workstream-task-lifecycle/SKILL.md` and the assigned task stub, then inspected the completed upstream signal-text task to reuse the established implementation pattern.
+- 2026-03-19 16:28 GMT: Reviewed `publishable_trade_schema.json`, `signal_text_generator.py`, `posting_rules.py`, and the existing marketing tests to identify the trade-result normalization gap.
+- 2026-03-19 16:30 GMT: Updated `signal_text_generator.py` to normalize `entry_price`, `exit_price`, `profit_loss`, and `trade_id`, added dedicated trade detail/instrument formatting, and fixed trade P&L formatting for small decimal values.
+- 2026-03-19 16:30 GMT: Expanded `test_signal_text_generator.py` with publishable trade-result, legacy trade-result, and trade trimming test coverage.
+- 2026-03-19 16:31 GMT: Ran `py_compile`, direct generator tests, and posting-rules regression successfully.
+- 2026-03-19 16:32 GMT: Replaced the original task stub with the required lifecycle structure and recorded the original stub metadata below.
+- Original stub metadata preserved:
+  - Workstream: D - MARKETING CONTENT ENGINE
+  - Epic Sequence: 4.2
+  - Depends On: `20260309_120030_autonomous_trading_signal_platform_workstreamD_create_signal_text_generator.md`
+  - Blocks: none
+  - Readiness: ready
+  - Epic Output Folder: `C:\Users\edebe\eds\ep_autonomous_trading_signal_platform`
+  - Initial Verification Checkbox: `Trade results formatted`
+  - Original Execution Evidence: `cmd /c echo claude processing 20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md` returned exit code `0`
+  - Original Retry History: `Retry-Count: 1`, retry scheduled at `2026-03-18 17:21:29`
+
+## Changes Made
+- Updated `SignalTextPayload` in `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py` to normalize trade-result aliases for:
+  - `entry_price -> entry`
+  - `exit_price/latest_price -> exit_price`
+  - `profit_loss -> trade result P&L`
+  - `trade_id/guid -> trade_id`
+- Added `_format_signed_value()` so trade-result posts keep small decimal profit/loss values instead of rounding them down to `0`.
+- Added `_build_trade_detail_line()` and `_instrument_line()` so closed-trade posts can render meaningful entry/exit details even when the publishable schema does not include asset or direction fields.
+- Extended `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py` with:
+  - a publishable trade-result schema test,
+  - a legacy trade payload compatibility test,
+  - a trade-result trimming test that preserves the review URL.
+
+## Validation
+- `python -m py_compile C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\x_poster.py`
+  - Result: Pass. Exit code `0`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
+  - Result: Pass. Output summary: `Ran 6 tests in 0.001s` / `OK`.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`
+  - Result: Pass. Output summary: `Ran 4 tests in 0.530s` / `OK`.
+  - Notable dry-run evidence: the trade-closed dispatch printed `TRADE CLOSED`, `WIN | Move +31 pips`, and the review URL across X, Telegram, and Discord.
+- User verification requested: confirm pass/fail for each behavior below before this task is moved to `300_complete`.
+  - Behavior 1: publishable trade-result payloads generate closed-trade posts that include the realized result plus entry/exit pricing.
+  - Behavior 2: existing trade-result payloads still generate valid posts for the posting-rules engine without extra caller-side mapping.
+  - Behavior 3: shortened trade-result posts preserve the review URL instead of truncating the destination link.
+
+## Risks/Notes
+- The publishable trade-result schema does not include asset or direction, so trade posts fall back to generic identifiers when those fields are absent from the payload.
+- No live platform post was executed; validation was limited to syntax checks and local dry-run/unit-test coverage.
+- Because this changes user-visible marketing copy, user verification is still required before completion.
+
+## Completion Status
+Awaiting user verification as of 2026-03-19 16:32 GMT. Implementation and technical validation are complete; do not move this task to `300_complete` until user pass/fail feedback is captured.

tokens used
86,795
Implemented the trade-result text generator updates in [signal_text_generator.py](C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py) and expanded coverage in [test_signal_text_generator.py](C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_text_generator.py). The formatter now supports the publishable trade schema fields (`profit_loss`, `entry_price`, `exit_price`, `trade_id`), preserves legacy trade payloads, and keeps small decimal P&L values instead of rounding them to zero. I also updated the lifecycle record and checklist in [20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260309_120031_autonomous_trading_signal_platform_workstreamD_create_trade_result_text_generator.md).

Validation passed:
- `python -m py_compile ...signal_text_generator.py ...x_poster.py`
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_text_generator -v`
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_posting_rules -v`

The task remains in `200_inprogress` because the lifecycle gate requires user verification for this user-visible copy change. Reply with pass/fail for:
1. Publishable trade-result payloads now generate sensible closed-trade posts with realized result plus entry/exit pricing.
2. Existing trade-result payloads still generate valid posts without extra mapping.
3. Shortened trade-result posts preserve the review URL.
