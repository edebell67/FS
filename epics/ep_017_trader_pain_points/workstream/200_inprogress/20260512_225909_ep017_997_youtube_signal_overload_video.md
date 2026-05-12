# EP017 YouTube Signal Overload Video

Source: User asked to build a YouTube content video from the same EP017 trader pain-point source.

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: true
- workflow_name: EP017 YouTube content validation
- workflow_stage: in_progress
- depends_on:
  - EP017 trader pain-point landing page series and Reddit signal-overload draft
- feeds_into:
  - YouTube validation posts and future content variants

Task Summary: Create a ready-to-review MP4 video asset that tests the signal-overload/ranked-opportunity-feed proposition without hard-selling the product.

Context:
- Core proposition: traders are not short of signals; they need to know which opportunity deserves attention first.
- Output should be suitable for YouTube use and reusable for broader marketing validation.

Destination Folder: `epics/ep_017_trader_pain_points/marketing/youtube_signal_overload_video/`

Dependency: Local video generation stack must support image/audio rendering and ffmpeg muxing.

## Plan

- [x] 1. Create video project folder and production script.
  - [x] Test: Files exist under destination folder with script/storyboard content.
  - Evidence: `marketing/youtube_signal_overload_video/build_video.py` and `storyboard.md` created.

- [x] 2. Generate narration audio.
  - [x] Test: Audio file exists and can be probed for duration.
  - Evidence: `narration.mp3` exists, 377,568 bytes, duration 62.93 seconds via `uv run --with mutagen`.

- [x] 3. Render video frames and mux final MP4.
  - [x] Test: media probe reports a playable MP4 with video and audio streams.
  - Evidence: `validation_output.txt` reports H.264 video, AAC audio, 1280x720, 30fps, 62.93s.

- [x] 4. Capture review evidence and package outputs.
  - [x] Test: Generated thumbnail/contact sheet exists and final artifact paths are recorded.
  - Evidence: `thumbnail.png`, `contact_sheet.png`, `storyboard.md`, `build_video.py`, and final MP4 are present.

## Evidence

Objective-Delivery-Coverage: 90%
Auto-Acceptance: false

- Evidence-Type: file_output
  - Artifact: `epics/ep_017_trader_pain_points/marketing/youtube_signal_overload_video/ep017_signal_overload_youtube_v1.mp4`
  - Objective-Proved: Video deliverable was created.
  - Status: captured

- Evidence-Type: test_output
  - Artifact: `epics/ep_017_trader_pain_points/marketing/youtube_signal_overload_video/validation_output.txt`
  - Objective-Proved: MP4 is technically valid and playable: H.264 video, AAC audio, 1280x720, 30fps, 62.93s.
  - Status: captured

- Evidence-Type: screenshot
  - Artifact: `epics/ep_017_trader_pain_points/marketing/youtube_signal_overload_video/contact_sheet.png`
  - Objective-Proved: Visual review evidence exists and quick visual QA found no obvious clipping/overlap after adjustment.
  - Status: captured

- Evidence-Type: user_feedback
  - Artifact: pending user review
  - Objective-Proved: User has accepted or requested changes to the video.
  - Status: planned

## Implementation Log

- 2026-05-12 22:59 BST: Created lifecycle task and started video production.
- 2026-05-12 23:00 BST: Created storyboard and Python production script for a 1280x720 voiceover-led YouTube explainer.
- 2026-05-12 23:01 BST: Generated narration audio via TTS at `narration.mp3`.
- 2026-05-12 23:05 BST: Rendered first MP4, then visually reviewed contact sheet and found one dense text scene.
- 2026-05-12 23:07 BST: Adjusted typography logic for multi-line scenes and re-rendered final MP4.

## Changes Made

- Created `marketing/youtube_signal_overload_video/storyboard.md`.
- Created `marketing/youtube_signal_overload_video/build_video.py`.
- Created `marketing/youtube_signal_overload_video/narration.mp3`.
- Created `marketing/youtube_signal_overload_video/signal_overload_visuals.mp4`.
- Created `marketing/youtube_signal_overload_video/ep017_signal_overload_youtube_v1.mp4`.
- Created `marketing/youtube_signal_overload_video/thumbnail.png`.
- Created `marketing/youtube_signal_overload_video/contact_sheet.png`.
- Created `marketing/youtube_signal_overload_video/validation_output.txt`.

## Validation

Commands/checks run:

```text
uv run --with mutagen python - <<'PY'
# narration.mp3 exists, 377568 bytes, duration_seconds 62.93
PY

uv run --with pillow --with imageio --with imageio-ffmpeg --with mutagen --with numpy python epics/ep_017_trader_pain_points/marketing/youtube_signal_overload_video/build_video.py
# rendered 1903 frames; muxed H.264 video with AAC audio; DONE final MP4

uv run --with imageio --with imageio-ffmpeg --with mutagen python - <<'PY'
# final MP4 exists, 3,773,441 bytes
# codec h264, audio_codec aac, fps 30.0, size 1280x720, duration 62.93
PY
```

Visual QA:
- Contact sheet reviewed after re-render; no obvious clipping/overlap remained.

User verification requested:
- Final MP4 delivered for review; awaiting pass/fail or requested edits.

## Risks/Notes

- First version prioritises speed and clear proposition validation over cinematic polish.
- Landscape format is suitable for standard YouTube upload; a vertical Shorts cut can be created as a follow-up if this direction is accepted.
- Final completion requires user review because this is a user-visible media asset.

## Completion Status

Status: Awaiting user verification — final MP4 built and delivered for review.
Timestamp: 2026-05-12 23:07:00 BST
