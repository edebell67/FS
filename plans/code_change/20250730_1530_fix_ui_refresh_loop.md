### 1. Plan of Approach

The UI is not refreshing because the method responsible for checking for updates from the background thread (`_check_worker_output_queue`) only runs once. To fix this, I will modify this method to schedule itself to run again continuously. This creates a persistent loop that will listen for refresh signals from the trade engine and update the UI accordingly, without reintroducing the deadlock issue.

### 2. Checklist of Changes

*   **Create Plan Directory**
    *   [ ] Check for `C:/Users/edebe/eds/algo_viewer/tradepanel/plans`.
    *   [ ] If it doesn't exist, create it.

*   **Save Plan**
    *   [ ] Save this plan to a file named `20250730_1530_fix_ui_refresh_loop.md` in the `plans` directory.

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/ui/main_window.py`**
    *   [ ] In the `_check_worker_output_queue` method, add a `finally` block containing `self.root.after(100, self._check_worker_output_queue)` to create a polling loop.
    *   [ ] Add the comment `# 2025-07-30: Added self-scheduling to create a continuous loop - v64.3.14` to the modified section.

*   **`C:/Users/edebe/eds/algo_viewer/tradepanel/constants.py`**
    *   [ ] Update `VERSION` to `"64.3.14"`.
    *   [ ] Add the comment `#2025-07-30: Fixed UI refresh loop` to the version line.

### 3. Confirmation

Please review the plan. I will proceed upon your approval.