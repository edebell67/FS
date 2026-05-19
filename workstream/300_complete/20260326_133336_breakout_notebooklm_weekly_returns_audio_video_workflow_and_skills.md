# Task: NotebookLM Weekly Returns Audio Video Workflow And Skills

## Source
- User Directive: 2026-03-26

## Task Summary
Fully document a repeatable workflow for generating NotebookLM audio and video outputs from weekly returns data, and create reusable skills to support the process as a regular output.

## Context
- Prior NotebookLM exploration is recorded in:
  - `C:\Users\edebe\eds\plans\chats\chat_gemini_20260325_1200.txt`
- Existing weekly returns sources:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\forex\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\indices\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\metals\stats\daily_net_return.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\energy\stats\daily_net_return.json`
- Related reusable posting package workflow:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\README.md`

## Goal
- Define the regular NotebookLM media workflow using weekly returns data.
- Capture the exact preparation, upload, generation, status-check, and download steps.
- Package the process into reusable skills that other models can run consistently.

## Scope
- NotebookLM audio outputs
- NotebookLM video outputs
- Weekly returns data preparation and restriction/summarization where required
- Repeatable operator workflow for regular production
- Reusable skills stored in `C:\Users\edebe\eds\skills`

## Plan
- [x] 1. Review the prior NotebookLM chat flow and extract the working command patterns.
- [x] 2. Define the weekly returns input package and any required restricted-summary transformations.
- [x] 3. Document the full end-to-end workflow for NotebookLM audio/video generation.
- [x] 4. Design reusable skills for preparation, generation, and retrieval steps.
- [x] 5. Validate the documented commands and expected outputs against the current repo/tooling state.

## Notes
- This is intended to become a regular output, not a one-off experiment.
- Documentation should distinguish between reusable local tooling and external NotebookLM session/auth requirements.
- Reusable implementation artifacts should go under an appropriately named `tools` subfolder if code/scripts are added later.

## Implementation Log
- **2026-03-26 13:33**: Task moved to in progress.
- **2026-03-26 13:49**: Added local NotebookLM prep tooling under `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\notebooklm_weekly_returns`.
- **2026-03-26 13:49**: Added two reusable skills in `C:\Users\edebe\eds\skills` for prep and media workflow execution.
- **2026-03-26 13:50**: Generated the first dated local NotebookLM media package for weekly returns.

## Changes Made
- Added:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\notebooklm_weekly_returns\generate_notebooklm_weekly_returns_source.py`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\tools\notebooklm_weekly_returns\README.md`
  - `C:\Users\edebe\eds\skills\notebooklm-weekly-returns-prep\SKILL.md`
  - `C:\Users\edebe\eds\skills\notebooklm-weekly-returns-prep\agents\openai.yaml`
  - `C:\Users\edebe\eds\skills\notebooklm-weekly-returns-media\SKILL.md`
  - `C:\Users\edebe\eds\skills\notebooklm-weekly-returns-media\agents\openai.yaml`
- Generated:
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\notebooklm_media\2026-03-26\weekly_returns_notebooklm_package.json`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\notebooklm_media\2026-03-26\weekly_returns_notebooklm_source.md`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\notebooklm_media\2026-03-26\weekly_returns_notebooklm_source.txt`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\notebooklm_media\2026-03-26\weekly_returns_audio_prompt.txt`
  - `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\notebooklm_media\2026-03-26\weekly_returns_video_prompt.txt`

## Validation
- Local prep validation command:
  - `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\notebooklm_weekly_returns\generate_notebooklm_weekly_returns_source.py`
- Result:
  - dated local NotebookLM source package generated successfully
  - skills created in `C:\Users\edebe\eds\skills`
- Environment check:
  - `C:\Users\edebe\AppData\Roaming\Python\Python312\Scripts\nlm.exe` was not present on 2026-03-26 in this environment
  - therefore NotebookLM CLI generation/download commands are documented from prior recorded workflow but were not live-verified in this task
  - documentation explicitly records this caveat

## Completion Status
**Complete** - 2026-03-26 13:50
