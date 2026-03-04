# Task: Fix Voice Booking Action and Dashboard Totals Sync (20260223_101500)

## Status
COMPLETED

## Task Summary
Resolve two critical functional issues:
1.  **Voice Action Failure**: Fixed a `ReferenceError` where `captureIntents` was used before definition, and improved keyword matching for "Book".
2.  **Totals Out of Sync**: Fixed dashboard calculation logic to include 'confirmed' items (voice-captured items are confirmed by default).

## Context
- Web version v1.1.5 is active.
- **Root Cause 1**: `captureIntents` mapping was defined after its first usage in the "last image" feature block, crashing voice processing for certain phrases.
- **Root Cause 2**: Intent keywords like "Book" were using strict word-boundary regex which failed with some speech-to-text punctuation.
- **Root Cause 3**: Dashboard totals were filtering out 'confirmed' items, but voice capture sets items to 'confirmed' immediately.

## Sub-tasks
- [x] Bug (Voice): Moved `captureIntents` to the top of `processVoice` to prevent `ReferenceError`.
- [x] Bug (Voice): Switched to `text.includes('book')` for more robust keyword matching.
- [x] Bug (Voice): Fixed `amountMatch` regex to prevent it from stealing numbers from time signatures (e.g. "5pm" no longer becomes "£5.00").
- [x] Bug (Stats): Updated `App.jsx` totals to include all non-archived items in the card values.
- [x] Bug (Sync): Added `payment_status` support to `createItemInternal` for lifecycle consistency.
- [x] Bug (Frontend): Added a 500ms delay to `fetchAllData` after voice processing to ensure DB triggers finish.
- [x] Verification: Confirmed "Book Tom..." now correctly hits `capture_booking`.

## Implementation Log
- [2026-02-23 10:15] Task created.
- [2026-02-23 10:20] Identified syntax error in `voiceController.js`.
- [2026-02-23 10:30] Updated `App.jsx` with more inclusive summing logic.
- [2026-02-23 10:45] Verified backend parsing now distinguishes between currency and time.

## Completion Status
COMPLETED (2026-02-23 10:50)
