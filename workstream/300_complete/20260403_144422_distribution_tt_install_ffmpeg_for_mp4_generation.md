## Objective

Install `ffmpeg` so `C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py` can generate MP4 output in addition to frames.

## Task Attributes

- project: distribution_tt
- task_type: environment_setup
- area: media_generation
- priority: high
- status: todo

## Plan

1. Install `ffmpeg` on the local machine.
2. Verify the executable is callable.
3. Rerun the clip generator against the live top-2 package.
4. Confirm MP4 output is produced.

## Progress Log

- 2026-04-03 14:45:18 Installed `Gyan.FFmpeg` via `winget`.
- 2026-04-03 14:46:03 Verified the package binary location at `C:\Users\edebe\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe`.
- 2026-04-03 14:47:35 Ran the clip generator against the live `2026-04-03` top-2 package using the explicit `--ffmpeg-binary` path and produced `out.mp4`.

## Validation

Install command:

```powershell
winget install --id Gyan.FFmpeg --exact --accept-package-agreements --accept-source-agreements
```

Generator command:

```powershell
python C:\Users\edebe\eds\distribution_TT\top2_vertical_clip.py --top2-package-json C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\2026-04-03\top2_cross_product_post.json --output-dir C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03_mp4 --ffmpeg-binary C:\Users\edebe\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1-full_build\bin\ffmpeg.exe
```

Result:
- Success
- MP4 output: `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03_mp4\out.mp4`
- File size: `36011` bytes
- Resolved input audit file: `C:\Users\edebe\eds\distribution_TT\output\live_2026_04_03_mp4\resolved_clip_input.json`

Resolved source-derived values:
- leader: `NQ`
- leader_pnl: `1460.0`
- challenger: `ES`
- challenger_pnl: `740.0`
- gap: `720.0`
- state: `live`

## Outcome

Completed successfully.

`ffmpeg` is installed and MP4 generation is now working for the live top-2 package path.
