# TASK D4: Create Signal Card Renderer

## Source
- `C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md`

## Task Summary
Create a reusable signal card renderer that combines generated signal text with the rendered chart image to produce `signal_card.png` from real workspace trading-signal artefacts.

## Context
- `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py`
- `C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py`
- `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png`
- `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
- `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06`

## Plan
- [x] 1. Inspect the existing signal text and chart artefacts, then define the renderer input contract around the real workspace sample data.
  - [x] Test: `@'` newline `from pathlib import Path` newline `assert Path(r"C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png").exists()` newline `print("inputs_ok")` newline `'@ | python -`
  - Evidence: Command passed and printed `inputs_ok`, confirming the renderer can target the existing text generator, chart generator, and rendered chart artefact without introducing a new data source.
- [x] 2. Implement the reusable signal card renderer and supporting tests to combine signal text, chart art, and entry/TP/SL metadata.
  - [x] Test: `python -m py_compile TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py TradeApps/breakout/piphunter/marketing/tests/test_signal_card_renderer.py` completes without syntax errors.
  - Evidence: `py_compile` completed with exit code `0` after adding `signal_card_renderer.py`, exporting it from `marketing/content/__init__.py`, and adding `test_signal_card_renderer.py`.
- [x] 3. Execute the renderer against the sample trading-signal artefacts and verify that `signal_card.png` is generated with entry, TP, and SL details.
  - [x] Test: `python TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py --chart C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png --trade-file C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06\breakout_R_Rev_2_tp5.0_sl50.0_a274dc8a_GBPAUD_C_20260306_161433_2_0.00015_5.0_50.0_op.json --feed C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json --out C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png`
  - Evidence: Command passed and printed `{"title": "GBPAUD_C SHORT", "subtitle": "breakout_R_Rev_2_tp5.0_sl50.0 | Trade 69 | OPEN", "detail_labels": ["Entry", "TP", "SL", "Current"], "image_bytes": 149116}`. Follow-up image validation confirmed `signal_card.png` exists at `1600x900`.

## Implementation Log
- 2026-03-09 18:xx GMT: Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the D4 task stub, and replaced it with the required lifecycle structure and ordered test-backed checklist.
- 2026-03-09 18:xx GMT: Inspected the existing `signal_text_generator.py`, the generated `signal_chart.png`, the sample mini-app feed, and the representative live trade JSON to define a renderer contract anchored on the real 2026-03-06 artefacts.
- 2026-03-09 18:xx GMT: Added `TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py` with trade-context loading, signal enrichment from feed data, reusable payload assembly, PIL-based card rendering, and a CLI entry point for end-to-end generation.
- 2026-03-09 18:xx GMT: Added `TradeApps/breakout/piphunter/marketing/tests/test_signal_card_renderer.py` covering payload construction and sparse-signal enrichment, and exported the renderer surface from `marketing/content/__init__.py`.
- 2026-03-09 18:xx GMT: Initial direct CLI execution failed because running the file directly did not place the repo root on `sys.path`; added a repo-root fallback for direct script execution and reran successfully.
- 2026-03-09 18:xx GMT: An initial attempt to unit-test full synthetic image rendering proved flaky under Windows temp-file cleanup, so the automated test was narrowed to deterministic payload behavior while the real image render remained covered by the end-to-end validation command.

## Changes Made
- Added `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_card_renderer.py`.
- Added `TradeCardContext`, `DetailRow`, and `SignalCardPayload` to normalize trade metadata, detail chips, and card copy inputs.
- Added `trade_context_from_trade_file()` and `signal_from_feed()` so the renderer can enrich sparse feed data with concrete trade entry, TP, SL, and status information.
- Added `render_signal_card()` to compose a two-panel PNG with strategy/product heading, signal-text body, entry/TP/SL/current detail chips, and the existing rendered chart image.
- Added CLI support to generate a card directly from workspace artefacts using `--chart`, `--trade-file`, `--feed`, and `--out`.
- Updated `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\__init__.py` to export the new renderer surface.
- Added `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_card_renderer.py`.
- Generated evidence image `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png`.

## Validation
- `@'` newline `from pathlib import Path` newline `assert Path(r"C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png").exists()` newline `print("inputs_ok")` newline `'@ | python -`
  - Result: `inputs_ok`
- `python -m py_compile TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py TradeApps/breakout/piphunter/marketing/tests/test_signal_card_renderer.py`
  - Result: Pass.
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_card_renderer -v`
  - Result: Pass. Output summary: `Ran 2 tests in 0.000s` / `OK`.
- `python TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py --chart C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png --trade-file C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06\breakout_R_Rev_2_tp5.0_sl50.0_a274dc8a_GBPAUD_C_20260306_161433_2_0.00015_5.0_50.0_op.json --feed C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json --out C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png`
  - Result: Pass. Printed output path and JSON summary with `detail_labels` equal to `["Entry", "TP", "SL", "Current"]` and `image_bytes` equal to `149116`.
- `@'` newline `from PIL import Image` newline `from pathlib import Path` newline `path = Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png")` newline `with Image.open(path) as img:` newline `    print(path)` newline `    print(img.size)` newline `'@ | python -`
  - Result: Output image exists and reports size `(1600, 900)`.
- User verification requested: Confirm that `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png` is acceptable for the implemented behaviors below.
  - Behavior 1: entry, TP, and SL details are visible in the left-side card metadata chips.
  - Behavior 2: the rendered chart is embedded cleanly and remains readable inside the card frame.
  - Behavior 3: the combined card text and chart are suitable for downstream social/marketing use.

## Risks/Notes
- The sample mini-app feed contains sparse signal fields, so the renderer may need to enrich the card from the sample trade JSON in order to guarantee visible entry, TP, and SL values.
- Because this task changes generated visual output, user verification is required before moving the task to `workstream/300_complete`.

## Completion Status
- Awaiting user verification as of 2026-03-09 18:xx GMT. Technical implementation and automated validation are complete; do not move to `workstream/300_complete` until user pass/fail feedback is captured.


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260309_120033_workstreamD_create_signal_card_renderer.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the signal card renderer and generated the evidence card at [signal_card.png](/C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/signal_card.png). The new renderer lives at [signal_card_renderer.py](/C:/Users/edebe/eds/TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py), with tests in [test_signal_card_renderer.py](/C:/Users/edebe/eds/TradeApps/breakout/piphunter/marketing/tests/test_signal_card_renderer.py), and I updated the lifecycle file at [20260309_120033_workstreamD_create_signal_card_renderer.md](/C:/Users/edebe/eds/workstream/200_inprogress/claude/20260309_120033_workstreamD_create_signal_card_renderer.md).

Validation passed:
- `python -m py_compile ...signal_card_renderer.py ...test_signal_card_renderer.py`
- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_card_renderer -v`
- end-to-end render command produced `detail_labels: ["Entry", "TP", "SL", "Current"]`, `image_bytes: 149116`
- image inspection confirmed `signal_card.png` is `1600x900`

User verification is still required before this task can be moved to complete. Please check [signal_card.png](/C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/signal_card.png) and reply pass/fail for:
1. entry, TP, and SL visibility
2. chart readability inside the card
3. suitability for downstream social/marketing use
```
- Stderr:
```text
y`.
+- Added `TradeCardContext`, `DetailRow`, and `SignalCardPayload` to normalize trade metadata, detail chips, and card copy inputs.
+- Added `trade_context_from_trade_file()` and `signal_from_feed()` so the renderer can enrich sparse feed data with concrete trade entry, TP, SL, and status information.
+- Added `render_signal_card()` to compose a two-panel PNG with strategy/product heading, signal-text body, entry/TP/SL/current detail chips, and the existing rendered chart image.
+- Added CLI support to generate a card directly from workspace artefacts using `--chart`, `--trade-file`, `--feed`, and `--out`.
+- Updated `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\__init__.py` to export the new renderer surface.
+- Added `C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\tests\test_signal_card_renderer.py`.
+- Generated evidence image `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png`.
+
+## Validation
+- `@'` newline `from pathlib import Path` newline `assert Path(r"C:\Users\edebe\eds\TradeApps\breakout\piphunter\marketing\content\signal_text_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py").exists()` newline `assert Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png").exists()` newline `print("inputs_ok")` newline `'@ | python -`
+  - Result: `inputs_ok`
+- `python -m py_compile TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py TradeApps/breakout/piphunter/marketing/tests/test_signal_card_renderer.py`
+  - Result: Pass.
+- `python -m unittest TradeApps.breakout.piphunter.marketing.tests.test_signal_card_renderer -v`
+  - Result: Pass. Output summary: `Ran 2 tests in 0.000s` / `OK`.
+- `python TradeApps/breakout/piphunter/marketing/content/signal_card_renderer.py --chart C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png --trade-file C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06\breakout_R_Rev_2_tp5.0_sl50.0_a274dc8a_GBPAUD_C_20260306_161433_2_0.00015_5.0_50.0_op.json --feed C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json --out C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png`
+  - Result: Pass. Printed output path and JSON summary with `detail_labels` equal to `["Entry", "TP", "SL", "Current"]` and `image_bytes` equal to `149116`.
+- `@'` newline `from PIL import Image` newline `from pathlib import Path` newline `path = Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png")` newline `with Image.open(path) as img:` newline `    print(path)` newline `    print(img.size)` newline `'@ | python -`
+  - Result: Output image exists and reports size `(1600, 900)`.
+- User verification requested: Confirm that `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_card.png` is acceptable for the implemented behaviors below.
+  - Behavior 1: entry, TP, and SL details are visible in the left-side card metadata chips.
+  - Behavior 2: the rendered chart is embedded cleanly and remains readable inside the card frame.
+  - Behavior 3: the combined card text and chart are suitable for downstream social/marketing use.
+
+## Risks/Notes
+- The sample mini-app feed contains sparse signal fields, so the renderer may need to enrich the card from the sample trade JSON in order to guarantee visible entry, TP, and SL values.
+- Because this task changes generated visual output, user verification is required before moving the task to `workstream/300_complete`.
+
+## Completion Status
+- Awaiting user verification as of 2026-03-09 18:xx GMT. Technical implementation and automated validation are complete; do not move to `workstream/300_complete` until user pass/fail feedback is captured.

tokens used
76,234
```

# User Feedback
User Verified: PASS
