# TASK D4: Create Weekly Metrics Report Generator

**Workstream:** D - ORCHESTRATION & AUTONOMY
**Workstream Goal:** Make the system self-running with appropriate controls.
**Epic:** Strategy Warehouse Autonomous Marketing Engine
**Epic Output Folder:** `C:\Users\edebe\eds\ep_strategy_warehouse_marketing\`
**Epic Sequence:** 4.4
**Depends On:** 4.2, 4.3
**Blocks:** none
**Readiness:** blocked
**Status:** [ ] Not Started

---

## Source

- **Epic:** `workstream/000_epic/20260316_135233_strategy_warehouse_autonomous_marketing_engine.md`
- **Project:** Strategy Warehouse Marketing

## Purpose

Generate automated weekly performance reports to track progress toward reach and subscriber goals.

## Input

- D2: Performance feedback data
- D3: Manual override controls

## Output

- `ep_strategy_warehouse_marketing/solution/backend/src/services/reportGeneratorService.py`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/weekly_report.html`
- `ep_strategy_warehouse_marketing/solution/backend/src/templates/weekly_report.jinja2`

## Fields

```markdown
# Weekly Marketing Report
**Week of:** {start_date} - {end_date}

## Executive Summary
- Total posts: {posts_count}
- Total impressions: {impressions}
- Follower growth: {follower_change} ({growth_percent}%)
- New subscribers: {new_subs}

## Platform Performance
| Platform | Posts | Impressions | Engagement | Followers |
|----------|-------|-------------|------------|-----------|
| Twitter  | ...   | ...         | ...        | ...       |
...

## Top Performing Content
1. {post_1} - {engagement_1}
2. {post_2} - {engagement_2}
3. {post_3} - {engagement_3}

## Conversion Funnel
- Page views: {views}
- Form submissions: {submissions}
- Confirmations: {confirmations}
- Conversion rate: {rate}%

## Recommendations
{insights_from_feedback_loop}
```

## Action

1. Aggregate weekly reach metrics from B8, B9
2. Aggregate weekly subscriber growth from C3
3. Aggregate weekly conversion rates from C4
4. Pull top performing content from D2
5. Generate HTML report from Jinja2 template
6. Generate PDF export using WeasyPrint or similar
7. Email report to configured stakeholders

## Verification

- [ ] Generate report for past 7 days
- [ ] Report includes follower growth
- [ ] Report includes subscriber growth
- [ ] Report includes conversion rates
- [ ] Report exports to PDF
- [ ] Screenshot of report captured

---

## Evidence

- Objective-Delivery-Coverage: 0%
- Auto-Acceptance: false
- Evidence-Type: file_output
  - Artifact: Generated weekly report PDF
  - Objective-Proved: Report generation works
  - Status: planned
- Evidence-Type: screenshot
  - Artifact: `ep_strategy_warehouse_marketing/verification/weekly_report_screenshot.png`
  - Objective-Proved: Report is readable and complete
  - Status: planned

## Required Skills

- `skills/ui-delivery-viewability/SKILL.md` - Screenshot evidence

## Dependency

- Requires: D2 (feedback loop), D3 (kill switch)
- Blocks: none (end of reporting)
- External: SMTP service for email delivery

## Notes

_User-visible task - requires manual verification. Key deliverable for stakeholder communication._


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\codex.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260316_232343_gemini_strategy_warehouse_marketing_engine_workstreamD_create_weekly_metrics_report_generator.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 1
- Stderr:
```text
OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019cfc23-decc-7d82-9433-d1b5dc1e06d1
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260316_232343_gemini_strategy_warehouse_marketing_engine_workstreamD_create_weekly_metrics_report_generator.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
ERROR: You've hit your usage limit. Upgrade to Pro (https://chatgpt.com/explore/pro), visit https://chatgpt.com/codex/settings/usage to purchase more credits or try again at Mar 18th, 2026 4:51 PM.
```
