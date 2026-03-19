# TASK E4: Implement voice intents, confirmation chip, and undo flow

**Workstream:** E — Mobile UX And Voice
**Epic:** MVP PRD — Mobile Quarterly Export in 10 Minutes (UK Sole Traders, Bank-Feed First)
**Priority:** 1
**Source Epic Path:** workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
**Epic Output Folder:** C:\Users\edebe\eds\ep_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first
**Suggested Agent:** codex
**UI Deliverable:** Yes
**Status:** [ ] Not Started
**Workstream Goal:** Provide the mobile-first screens and voice-assisted workflows that make quarterly triage and close achievable in minutes.

---

## Purpose

Support the MVP voice command set for inbox and Finish Now workflows while keeping every applied action immediately visible and easily reversible.

## Input

B2 micro-decision actions, D3 evidence confirmation actions, and epic voice command set and confirmation-chip rule.

## Output

Voice intent handling layer and UI feedback components for category, business/personal, split, attach receipt, match ranking, and no-match commands.

## Fields / Components

- intent_name
- parsed_value
- applied_action
- confirmation_chip
- undo_state

## Dependencies

- B2
- D3
- E1
- E2

## Action

Implement voice intent parsing or provider integration, map intents to the same action handlers as taps, and show a single confirmation chip with one-tap undo.

## Verification

- [ ] Voice commands 'Category: {X}', 'Business', 'Personal', 'Split {n}%', 'Attach receipt', 'Match first/second/third', and 'No match' are recognized and routed correctly.
- [ ] Applied voice actions show a single confirmation chip summarizing the change and offering undo.
- [ ] Provide or update a simple local access/start script that launches the app locally, prints the localhost URL, and is documented for voice-flow verification.
- [ ] Smoke-test the local startup path and confirm the voice-enabled UI loads without immediate crashes.
- [ ] Capture screenshot evidence of the confirmation chip in the epic verification folder.
- [ ] The acceptance test 'Voice Category: Travel applies and is undoable with one tap' passes.

---

## Notes

- Generated from source epic: `workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md`
- This task is intended for Epic Review allocation before execution.
- UI delivery requirements were expanded per `skills/ui-delivery-viewability/SKILL.md`.


## Retry History
Retry-Count: 2
- Retry scheduled at 2026-03-18 17:21:30


## Execution Evidence
- Agent lane: claude
- Command: C:\Users\edebe\AppData\Roaming\npm\claude.CMD -p Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/claude\20260314_034045_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole_traders_bank_feed_first_workstreamE_implement_voice_intents_confirmation_chip_and_undo_flow.md. Implement required changes in the workspace, run validations, and update checklist items. --permission-mode acceptEdits
- Return code: 1
- Stdout:
```text
You've hit your limit · resets 7pm (Europe/London)
```
- Retry scheduled at 2026-03-18 17:30:31
