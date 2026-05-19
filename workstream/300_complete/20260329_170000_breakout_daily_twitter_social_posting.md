# Task: Repeatable Daily Twitter Social Posting (2x Daily)

Source: User Request 2026-03-29
Task Summary: Execute the consolidated workflow to generate and publish the latest top 5 weekly strategy rankings to Twitter/X for Forex, Indices, Metals, and Energy. This is a repeatable task intended to run twice daily.
Context: Uses `generate_posting_package.py` and the `strategy-warehouse-social-posting` skill.
Dependency: Latest `daily_net_return.json` files for each product type.

## Repeatable Workflow Actions
- [ ] 1. **Data Refresh:** Ensure latest aggregation has run.
  - Command: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\aggregate_top_strategies.py [product_type]`
- [ ] 2. **Package Generation:** Generate the social posting package.
  - Command: `python C:\Users\edebe\eds\TradeApps\breakout\fs\tools\social_posting_package\generate_posting_package.py`
- [ ] 3. **Review & Preparation:** Open and review the generated Markdown sheet.
  - File: `C:\Users\edebe\eds\TradeApps\breakout\fs\json\live\social_posting_package\YYYY-MM-DD\top5_weekly_posting_package.md`
- [ ] 4. **Publish Thread:** Use the prepared copy to post the multi-product thread to Twitter/X.
  - Order: Intro -> Forex -> Indices -> Metals -> Energy -> Closing.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

## Implementation Log
- 2026-03-29 17:00: Consistently capturing daily actions into a single repeatable workstream task.

## Validation
- Review the generated Markdown file for accuracy of strategy rankings and Twitter copy.
- Confirm thread publication on Twitter/X.

## Risks/Notes
- Ensure `pip_multiplier` and `min_move` fixes (like RTY/BTC) are already reflected in the source stats before running this.
- If Playwright/`twitter_browser.py` is not configured, posting remains a manual copy-paste from the Markdown file.

## Completion Status
Todo
