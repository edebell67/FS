# Top 10 History Evaluation Screen

## 1. Understanding of Requirements
The objective is to build a new screen/UI to visualize the `_top10_history.json` data. This screen will serve as an evaluation tool to analyze the effectiveness of the `pick_now` (referred to as `pick_me`) logic. 

Specifically, the user needs to:
* View all historical snapshots from `_top10_history.json` in reverse chronological order (most recent first).
* Filter the data by `strategy` and `product`.
* See all relevant fields (Timestamp, Strategy, Product, Net, Pick Now).
* Evaluate patterns: 
  - Do all strategies that ultimately end up in the Top 20 trigger `pick_now: true`? 
  - Do all strategies that trigger `pick_now: true` stay in the Top 10 by the end of the session?

## 2. Plan of Approach
1. **Backend API Endpoint**: 
   - Add a new route in `fs/trade_viewer_api.py` (e.g., `/api/top10_history`) that reads `_top10_history.json` for the requested date and returns its contents.
2. **New UI Page (`top10_history.html`)**:
   - Create a clean HTML layout utilizing the project's existing CSS (e.g., matching `trade_bucket.html` or `strategy_performance.html`).
   - Add input/dropdown filters for `Strategy` and `Product` at the top of the page.
   - Include a robust data table below the filters.
3. **Frontend JavaScript**:
   - Fetch the data from `/api/top10_history`.
   - Flatten the nested snapshot array (`[ {timestamp, top10: [...]}, ... ]`) into a single list of rows.
   - Sort the rows by `timestamp` DESC (most recent first).
   - Implement real-time filtering logic based on the user's `Strategy` and `Product` inputs.
   - Render the table, highlighting rows where `pick_now` is true for easy visual scanning.
4. **Navigation Integration**:
   - Add a link to "Top 10 History" in the main navigation sidebar/header so it's easily accessible.

## 3. List of Changes
- [ ] Modify `fs/trade_viewer_api.py` to add `@app.route('/api/top10_history')` endpoint.
- [ ] Create `fs/top10_history.html` with filtering UI and data table.
- [ ] Create `fs/top10_history.js` containing fetch, flatten, sort, filter, and render logic.
- [ ] Update `fs/sidebar-loader.js` (or relevant navigation menus) to link to `top10_history.html`.
- [ ] Double-check AND VERIFY THAT ALL NEW changes HAVE BEEN IMPLEMENTED correctly. Update Version Number.

## 4. Documentation & Version
- Check off each checklist item as completed. 
- Ensure comments refer to this plan.
- UPDATE VERSION NUMBER in `Constants.py` when done.
