# TASK D3: Create Signal Chart Generator

Source: `C:\Users\edebe\eds\workstream\epic\Autonomous Trading Signal Platform.md`

## Task Summary

Create a reusable signal chart generator that can render `signal_chart.png` from existing signal/trade data and available price history in the workspace, using the current trading-signal mini-app artifacts as inputs where possible.

## Context

- Existing feed extractor: `C:\Users\edebe\eds\workstream\artefacts\miniapp_feed_extractor.py`
- Sample feed: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json`
- Sample live data day: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06`
- Evidence folder: `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal`

## Plan

- [x] 1. Inspect the available signal, trade, and price-history artifacts and define the generator input contract around real workspace data.
  - [x] Test: `@'` newline `import json` newline `from pathlib import Path` newline `feed = json.loads(Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json").read_text())` newline `assert "signals" in feed and "open_trades" in feed` newline `print("feed_ok", len(feed["signals"]), len(feed["open_trades"]))` newline `'@ | python -`
  - Evidence: Command passed and printed `feed_ok 4 1`, confirming the sample feed contains both signal and open-trade inputs for generator resolution.
- [x] 2. Implement the signal chart generator script and supporting logic to resolve signal context, extract price points, and render `signal_chart.png`.
  - [x] Test: `@'` newline `from pathlib import Path` newline `p = Path(r"C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py")` newline `text = p.read_text()` newline `assert "render_signal_chart" in text and "find_price_history" in text` newline `print("script_ok")` newline `'@ | python -`
  - Evidence: Added `C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py`; command passed and printed `script_ok`.
- [x] 3. Execute the generator against the sample 2026-03-06 live dataset and verify that a non-empty chart image is produced.
  - [x] Test: `python C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py --day-dir C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06 --trade-file C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06\breakout_R_Rev_2_tp5.0_sl50.0_a274dc8a_GBPAUD_C_20260306_161433_2_0.00015_5.0_50.0_op.json --out C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png`
  - Evidence: Command passed and printed the output path plus `{"strategy": "breakout_R_Rev_2_tp5.0_sl50.0", "product": "GBPAUD_C", "direction": "SHORT", "price_points": 12, "image_bytes": 102634}`. Follow-up image validation confirmed `signal_chart.png` size `(1920, 1120)`.

## Implementation Log

- 2026-03-09 17:26:00+00:00 Read `skills/workstream-task-lifecycle/SKILL.md`, reviewed the task stub, and identified that the task file had to be rewritten into the required lifecycle format before completion.
- 2026-03-09 17:29:00+00:00 Inspected the trading-signal epic, mini-app feed extractor, sample generated feed, `_trade_buckets.json`, `_live_trades.json`, and a representative trade JSON file from `TradeApps/breakout/fs/json/live/2026-03-06` to anchor the implementation on existing data.
- 2026-03-09 17:34:00+00:00 Replaced the task stub with a full lifecycle document containing ordered checklist steps, exact validation commands, and evidence placeholders.
- 2026-03-09 17:42:00+00:00 Implemented `workstream/artefacts/signal_chart_generator.py` with CLI argument parsing, trade/feed context resolution, TP/SL price derivation, price-history extraction, and PNG rendering via `matplotlib`.
- 2026-03-09 17:45:00+00:00 First end-to-end execution revealed that scanning all per-trade JSON files in the live day directory was too slow for the sample dataset; refactored history resolution to consume `_live_trades.json` first and keep per-file scanning as fallback only.
- 2026-03-09 17:47:00+00:00 Re-ran validations successfully and generated `workstream/clawd_originated/artefacts/evidence/trading_signal/signal_chart.png`.

## Changes Made

- Added `C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py`.
- Implemented `TradeContext` and loaders for both direct trade JSON input and mini-app feed input.
- Implemented `find_price_history()` to resolve same-strategy/product trade price points from `_live_trades.json`, with fallback scanning of individual trade JSON files only when the aggregate file is unavailable.
- Implemented `render_signal_chart()` to output a PNG with price path, entry/TP/SL reference lines, signal direction styling, and trade summary text.
- Generated evidence image `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png`.

## Validation

- Passed:
  - `@'` newline `import json` newline `from pathlib import Path` newline `feed = json.loads(Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\miniapp_feed_2026-03-06.json").read_text())` newline `assert "signals" in feed and "open_trades" in feed` newline `print("feed_ok", len(feed["signals"]), len(feed["open_trades"]))` newline `'@ | python -`
  - Result: `feed_ok 4 1`
- Passed:
  - `@'` newline `from pathlib import Path` newline `p = Path(r"C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py")` newline `text = p.read_text()` newline `assert "render_signal_chart" in text and "find_price_history" in text` newline `print("script_ok")` newline `'@ | python -`
  - Result: `script_ok`
- Passed:
  - `python C:\Users\edebe\eds\workstream\artefacts\signal_chart_generator.py --day-dir C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06 --trade-file C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\2026-03-06\breakout_R_Rev_2_tp5.0_sl50.0_a274dc8a_GBPAUD_C_20260306_161433_2_0.00015_5.0_50.0_op.json --out C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png`
  - Result: printed output path and JSON summary with `price_points: 12` and `image_bytes: 102634`
- Passed:
  - `@'` newline `from PIL import Image` newline `from pathlib import Path` newline `path = Path(r"C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png")` newline `img = Image.open(path)` newline `print(path)` newline `print(img.size)` newline `'@ | python -`
  - Result: output image exists and reports size `(1920, 1120)`
- User verification requested:
  - Please verify that `C:\Users\edebe\eds\workstream\clawd_originated\artefacts\evidence\trading_signal\signal_chart.png` is acceptable as the expected signal chart output and confirm pass/fail for: `1.` price path readability, `2.` entry/TP/SL visibility, `3.` overall suitability for downstream card rendering.

## Risks/Notes

- The sample mini-app feed does not itself contain full candle history, so the generator must resolve price history from the day directory and degrade gracefully if only sparse trade price points are available.
- This task changes generated output, so final lifecycle completion remains gated on user verification per the lifecycle skill.

## Completion Status

Awaiting user verification - 2026-03-09 17:48:00+00:00


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260309_120032_workstreamD_create_signal_chart_generator.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 0
- Stdout:
```text
Implemented the signal chart generator in [signal_chart_generator.py](C:/Users/edebe/eds/workstream/artefacts/signal_chart_generator.py) and validated it against the real `2026-03-06` live dataset. The generated evidence image is [signal_chart.png](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/signal_chart.png), and the successful run produced `12` price points with a `102634` byte PNG at `1920x1120`.

I also rewrote and updated the lifecycle file at [20260309_120032_workstreamD_create_signal_chart_generator.md](C:/Users/edebe/eds/workstream/200_inprogress/claude/20260309_120032_workstreamD_create_signal_chart_generator.md) to the required format, checked off all technical checklist items, recorded validation evidence, and left the task in `Awaiting user verification` per the lifecycle rules.

Please verify [signal_chart.png](C:/Users/edebe/eds/workstream/clawd_originated/artefacts/evidence/trading_signal/signal_chart.png) and confirm pass/fail for:
1. price path readability
2. entry/TP/SL visibility
3. suitability for downstream card rendering
```
- Stderr:
```text
oint(parse_timestamp(str(exit_time)), to_float(exit_price), "exit"))
+    elif trade.get("current_price") is not None:
+        current_time_value = trade.get("sent_at") or trade.get("tb_leader_set_at") or entry_time
+        if current_time_value:
+            points.append(build_point(parse_timestamp(str(current_time_value)), to_float(trade.get("current_price")), "current"))
+
+
+def render_signal_chart(context: TradeContext, price_points: list[dict[str, Any]], output_path: Path) -> None:
+    output_path.parent.mkdir(parents=True, exist_ok=True)
+
+    times = [point["time"] for point in price_points]
+    prices = [point["price"] for point in price_points]
+    direction = str(context.direction).upper()
+    line_color = "#0f766e" if direction in {"BUY", "LONG"} else "#b91c1c"
+    bg_color = "#f8fafc"
+
+    fig, ax = plt.subplots(figsize=(12, 7), constrained_layout=True)
+    fig.patch.set_facecolor(bg_color)
+    ax.set_facecolor("white")
+
+    ax.plot(times, prices, color=line_color, linewidth=2.5, marker="o", markersize=4)
+    ax.axhline(context.entry_price, color="#1d4ed8", linestyle="--", linewidth=1.2, label=f"Entry {context.entry_price:.5f}")
+    ax.axhline(context.tp_price, color="#15803d", linestyle=":", linewidth=1.2, label=f"TP {context.tp_price:.5f}")
+    ax.axhline(context.sl_price, color="#dc2626", linestyle=":", linewidth=1.2, label=f"SL {context.sl_price:.5f}")
+    ax.scatter([times[-1]], [prices[-1]], color="#111827", s=40, zorder=5)
+
+    for point in price_points[-3:]:
+        ax.annotate(
+            point["label"],
+            (point["time"], point["price"]),
+            textcoords="offset points",
+            xytext=(0, 8),
+            ha="center",
+            fontsize=8,
+            color="#334155",
+        )
+
+    ax.set_title(f"{context.strategy} | {context.product} | {direction}", fontsize=16, fontweight="bold", color="#0f172a")
+    ax.set_xlabel("Time")
+    ax.set_ylabel("Price")
+    ax.grid(True, alpha=0.2)
+    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
+    fig.autofmt_xdate()
+
+    summary = (
+        f"Trade {context.trade_id}  Status {context.status}  "
+        f"Entry {context.entry_price:.5f}  Current {context.current_price:.5f}"
+    )
+    ax.text(0.01, 0.01, summary, transform=ax.transAxes, fontsize=10, color="#334155")
+    ax.legend(loc="upper left")
+
+    fig.savefig(output_path, dpi=160)
+    plt.close(fig)
+
+
+def parse_args() -> argparse.Namespace:
+    parser = argparse.ArgumentParser(description="Render a signal chart image from workspace trade data.")
+    parser.add_argument("--day-dir", required=True, help="Live day directory containing trade JSON files.")
+    parser.add_argument("--trade-file", help="Specific trade JSON file to render.")
+    parser.add_argument("--feed", help="Mini-app feed JSON path.")
+    parser.add_argument("--signal-id", help="Signal identifier to resolve when using --feed.")
+    parser.add_argument("--out", required=True, help="Output PNG path.")
+    return parser.parse_args()
+
+
+def main() -> None:
+    args = parse_args()
+    day_dir = Path(args.day_dir)
+    output_path = Path(args.out)
+
+    if args.trade_file:
+        context = trade_context_from_trade_file(Path(args.trade_file))
+    elif args.feed:
+        context = trade_context_from_feed(Path(args.feed), args.signal_id)
+    else:
+        raise SystemExit("Either --trade-file or --feed must be provided.")
+
+    price_points = find_price_history(day_dir, context)
+    render_signal_chart(context, price_points, output_path)
+
+    print(output_path)
+    print(
+        json.dumps(
+            {
+                "strategy": context.strategy,
+                "product": context.product,
+                "direction": context.direction,
+                "price_points": len(price_points),
+                "image_bytes": output_path.stat().st_size,
+            }
+        )
+    )
+
+
+if __name__ == "__main__":
+    main()

tokens used
130,439
```

# User Feedback
User Verified: PASS
