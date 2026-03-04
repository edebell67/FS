# Task Summary
Write a one-off utility function or script to retrofit all EXISTING tasks currently sitting in `100_todo` and `200_inprogress` with a default `Priority: 2` tag so that they visually display the P2 badge and properly integrate into the new priority-queuing system.

# Context
We just implemented a Priority UI and Queue system (P1/P2/P3), but older existing tasks do not have the `Priority: 2` string explicitly written inside them. While the backend logic defaults them to P2 under the hood if it is missing, the Frontend UI relies on that tag explicitly existing in the `.md` file to visually render the `⚙️ P2` badge correctly on the Kanban card. 
To keep the UI clean, all legacy alive tasks need this tag prefixed to their contents.

# Implementation Plan
1. Create a quick python loop that iterates through:
   - `C:\Users\edebe\eds\workstream\100_todo` subdirectories
   - `C:\Users\edebe\eds\workstream\200_inprogress` subdirectories
2. Read each `.md` file.
3. Check if `Priority: X` already exists in the file.
4. If it does not exist, prepend `Priority: 2\n\n` to the very top of the `.md` file and save.

# Validation Steps
* [ ] Run the retrofit script.
* [ ] Refresh the Kanban Dashboard and verify that all tasks in `To Do` and `In Progress` successfully display the purple `⚙️ P2` badge on their UI cards.
