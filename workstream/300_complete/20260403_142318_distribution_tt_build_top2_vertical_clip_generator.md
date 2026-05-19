## Objective

Create code under `C:\Users\edebe\eds\distribution_TT` that generates a vertical social clip package from source-derived top-2 leader data, using rendered image frames plus an `ffmpeg` video assembly step.

## Task Attributes

- project: distribution_tt
- task_type: implementation
- area: media_generation
- priority: high
- status: todo

## Requirements

- Build the implementation in `C:\Users\edebe\eds\distribution_TT`
- Use Python with `PIL` / `Pillow` for frame rendering
- Support input fields:
  - `leader`
  - `leader_pnl`
  - `challenger`
  - `challenger_pnl`
  - `gap`
  - `state`
- Generate individual vertical frames sized for `1080x1920`
- Assemble the frames into a short MP4 using `ffmpeg`
- Use source-derived values only; do not fabricate labels, timestamps, PnL, gap values, or state text
- Handle font loading robustly rather than assuming `arial.ttf` is in the working directory
- Use a safer subprocess execution path instead of `os.system`

## Desired Output

- Python implementation under `C:\Users\edebe\eds\distribution_TT`
- A callable entry point that can generate:
  - frame images
  - final MP4 output
- Clear input contract, output paths, and runtime dependencies
- Validation evidence showing the generator runs successfully on sample source-shaped input

## Plan

1. Inspect `C:\Users\edebe\eds\distribution_TT` and decide the target file layout.
2. Implement a robust vertical clip generator based on the provided concept.
3. Add sample invocation or CLI entry support.
4. Run the generator and verify frames plus MP4 output are produced.
5. Record exact commands and outputs.

## Progress Log

- 2026-04-03 14:24:30 Confirmed `C:\Users\edebe\eds\distribution_TT` did not yet exist and scaffolded a new implementation folder.
- 2026-04-03 14:26:12 Added `top2_vertical_clip.py`, `README.md`, and `sample_top2_data.json`.
- 2026-04-03 14:27:03 Validated frame rendering with `--frames-only`; frames were written to `distribution_TT\output\frames`.
- 2026-04-03 14:28:22 Added `--ffmpeg-binary` support for environments where `ffmpeg` is not on `PATH`.
- 2026-04-03 14:28:57 Verified MP4 assembly currently fails with a concrete environment blocker: `RuntimeError: ffmpeg is not available: ffmpeg`.

## Validation

- `distribution_TT` contains the new generator code
- The generator successfully renders frame images
- The generator successfully produces an MP4 when `ffmpeg` is available
- The implementation uses width/height calculations correctly for centered text
- The implementation does not rely on fabricated market data

## Notes

- Treat the user-provided snippet as a starting concept, not final production code.
- Prefer reusable module structure over a one-off script if the folder layout supports it.
- If `ffmpeg` is unavailable, record the concrete blocker and keep frame generation independently testable.

## Implementation

- Created [top2_vertical_clip.py](C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py) as the reusable clip generator entry point
- Added [sample_top2_data.json](C:\Users\edebe\eds\distribution_TT\sample_top2_data.json) for source-shaped test input
- Added [README.md](C:\Users\edebe\eds\distribution_TT\README.md) with usage and runtime notes

Implemented behavior:
- Robust font loading from common Windows font paths with safe fallback
- Correct centered text measurement using `textbbox` width/height differences
- Frame generation to `1080x1920` PNGs
- Safer video assembly via `subprocess.run`
- Optional `--frames-only` mode
- Optional `--ffmpeg-binary` override for explicit ffmpeg paths

## Validation

Commands run:

```powershell
python C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py --input C:\Users\edebe\eds\distribution_TT\sample_top2_data.json --output-dir C:\Users\edebe\eds\distribution_TT\output --frames-only
```

Result:
- Success
- Output: `frames_dir=C:\Users\edebe\eds\distribution_TT\output\frames`
- Generated frames:
  - `f1.png`
  - `f2.png`
  - `f3.png`
  - `f4.png`

MP4 attempt:

```powershell
python C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py --input C:\Users\edebe\eds\distribution_TT\sample_top2_data.json --output-dir C:\Users\edebe\eds\distribution_TT\output
```

Result:
- Blocked by environment
- Exact error: `RuntimeError: ffmpeg is not available: ffmpeg`

## Outcome

Completed with an environment blocker on MP4 assembly only.

The code is implemented and frame rendering is validated. To enable MP4 generation, install `ffmpeg` on `PATH` or rerun with `--ffmpeg-binary C:\path\to\ffmpeg.exe`.
