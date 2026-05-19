## Task

Restore `TradeApps/breakout/fs/config.json` after it was overwritten with a truncated config.

## Context

- Reported by user on 2026-04-09.
- Target file: `C:\Users\edebe\eds\TradeApps\breakout\fs\config.json`
- Recovery source: `TradeApps` git `HEAD` at `f4afe6a918e38c1bfa0c71fc0fa2deaee8fad3f4`

## Progress Log

### 2026-04-09 00:34:52

- Inspected `git -C C:\Users\edebe\eds\TradeApps status --short -- breakout/fs/config.json`.
- Confirmed file was modified in working tree.
- Compared working tree file against `HEAD` and found the current file had been reduced from 192 lines to 21 lines.
- Proceeding to restore the file content from committed `HEAD`.

## Validation

### 2026-04-09 00:34:52

- `git -C C:\Users\edebe\eds\TradeApps diff --stat -- breakout/fs/config.json` returned no output after exact restore.
- `git -C C:\Users\edebe\eds\TradeApps status --short -- breakout/fs/config.json` returned no output after exact restore.
- Recovery completed successfully.
