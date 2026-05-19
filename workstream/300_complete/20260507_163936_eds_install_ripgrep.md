# Install ripgrep

Source: User request: "can you install ripgrep"

Task Type: standard

Task Attributes:
- recurring_task: false
- looping_task: false
- splittable_task: false
- workflow_task: false

Task Summary: Install ripgrep (`rg`) in the WSL environment so Hermes file search can use the faster ripgrep backend and Hermes Doctor no longer reports ripgrep missing.

Context:
- WSL environment
- Hermes Doctor warning: `ripgrep (rg) not found`
- Package manager discovered: `/usr/bin/apt-get`

Destination Folder: None

Dependency: sudo/apt package installation access in WSL.

Plan:
- [x] 1. Move task into in-progress state and check current `rg` availability.
  - [x] Test: `command -v rg || true` should show absent before install or existing path if already installed.
  - Evidence: command produced no output, confirming `rg` was absent before install.
- [x] 2. Install ripgrep via apt.
  - [x] Test: `sudo apt-get update && sudo apt-get install -y ripgrep` exits 0.
  - Evidence: installation was completed after sudo/password access was supplied outside the agent tool session; verification found `/usr/bin/rg`.
- [x] 3. Verify ripgrep and Hermes Doctor status.
  - [x] Test: `rg --version` exits 0 and `hermes doctor` no longer reports `ripgrep (rg) not found`.
  - Evidence: `command -v rg && rg --version` returned `/usr/bin/rg` and `ripgrep 14.1.0`; `hermes doctor` reports `✓ ripgrep (rg) (faster file search)`.

Evidence:
Objective-Delivery-Coverage: 100%
Auto-Acceptance: true
- Evidence-Type: test_output
  - Artifact: `command -v rg && rg --version` -> `/usr/bin/rg`; `ripgrep 14.1.0`; features `-simd-accel,+pcre2`; PCRE2 10.42 available.
  - Objective-Proved: ripgrep installed and discoverable as `rg`.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `hermes doctor` -> External Tools section includes `✓ ripgrep (rg) (faster file search)`.
  - Objective-Proved: Hermes Doctor no longer reports missing ripgrep.
  - Status: captured

Implementation Log:
- 2026-05-07 16:39:36: Created lifecycle task in backlog for ripgrep installation.
- 2026-05-07 16:39:36: Moved lifecycle task to in-progress and verified `rg` was absent before installation.
- 2026-05-07 16:40:00: Attempted `sudo apt-get update && sudo apt-get install -y ripgrep`; blocked because sudo requires an interactive password and the command cannot read it in this non-PTY tool session.
- 2026-05-07 16:40:00: Attempted `apt-get install -y ripgrep` without sudo; blocked by dpkg lock permission denial.
- 2026-05-07 16:40:00: Confirmed passwordless sudo is unavailable with `sudo -n true` (`sudo: a password is required`).
- 2026-05-08 11:26:50 BST: User requested re-check; verified ripgrep is now installed at `/usr/bin/rg` and Hermes Doctor recognizes it.

Changes Made:
- System package installed in WSL: ripgrep 14.1.0, available at `/usr/bin/rg`.
- No repository source files changed.

Validation:
- `command -v rg && rg --version`: passed; output includes `/usr/bin/rg` and `ripgrep 14.1.0`.
- `hermes doctor`: passed for ripgrep; output includes `✓ ripgrep (rg) (faster file search)`.

Risks/Notes:
- Installation required sudo/apt access outside the original non-PTY agent tool session.
- Hermes Doctor still reports unrelated optional warnings for missing provider keys, optional tool dependencies, and submodules; those are outside this ripgrep task.

Completion Status: Complete as of 2026-05-08 11:26:50 BST.
