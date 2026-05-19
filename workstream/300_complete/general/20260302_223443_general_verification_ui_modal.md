# Task Summary
Implement a "Verification Required" UI Modal on the Kanban board to allow users to formally Pass or Fail tasks completed by headless agents. Crucially, the modal must extract and display the context of the task (Summary, Changes Made, and Validation steps) so the user knows exactly what they are verifying.

# Context
Headless background agents cannot communicate interactively. When an agent finishes coding but requires human validation (e.g., checking a UI change or DB state), it currently writes "Awaiting user verification" at the bottom of the `.md` file and leaves it in `200_inprogress`. 
The user currently has to manually open the file in an external editor, read it, type a response, and manually drag it to the next column. This breaks the dashboard experience.

# Implementation Plan
1. **Detect Verification State**:
   - Update the `/api/tasks` endpoint in `kanban_dashboard.py` to scan the contents of tasks in `200_inprogress`.
   - If a file contains the phrase `Awaiting user verification` (or similar formal state markers), flag it in the JSON payload (e.g., `awaiting_verification: true`).
   
2. **Dashboard UI Updates**:
   - For tasks flagged as `awaiting_verification`, render a bright "🔍 Verify" badge/button directly on the Kanban card.
   - When clicked, open a specialized **Verification Modal**.
   
3. **Information Surfacing (Critical)**:
   - The Verification Modal must parse the markdown content of the task and cleanly display the specific sections the user needs to read:
     - **Task Summary**: What was the agent supposed to do?
     - **Changes Made**: What files/code did it actually change?
     - **Validation**: What specific steps is the agent asking the user to manually test?
     
4. **Action Outcomes**:
   - **✅ Pass**: User clicks Pass. The backend API appends `# User Feedback\nUser Verified: PASS` to the file and moves it strictly from `200_inprogress` to `300_complete`.
   - **❌ Fail**: User clicks Fail. A text box drops down asking for the failure details (e.g., "The button is still red, not blue"). The backend appends `# User Feedback\nUser Verified: FAIL - [Details]` to the file, and moves the task *back* to `100_todo/{agent}` so the headless agent instantly picks it back up for a retry.

# Validation Steps
* [ ] Create a dummy task in `200_inprogress` containing "Awaiting user verification" and validation instructions.
* [ ] Verify the "Verify" button appears on the card.
* [ ] Click it and ensure the modal cleanly displays the task summary and validation instructions without showing raw markdown clutter.
* [ ] Test the "Pass" flow and verify the file moves to complete.
* [ ] Test the "Fail" flow, enter feedback, and verify the file moves back to "todo" with the feedback explicitly written inside.
