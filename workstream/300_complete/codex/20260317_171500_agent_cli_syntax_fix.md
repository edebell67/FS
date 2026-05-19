# Task: Fix Agent CLI Syntax Mismatch

`Source`: `C:\Users\edebe\eds\plans\20260317_1715_V20260317_1715_Agent_CLI_Syntax_Fix.md`
`Task Summary`: Correct the Kanban dashboard and agent controller to use the proper CLI flags for Gemini and Claude, as they do not support the Codex-specific "exec -C" syntax.
`Context`: `workstream\kanban_dashboard.py`, `workstream\run_agent.py`, `TradeApps\breakout\fs\constants.py`
`Dependency`: None

## Plan
- [ ] 1. Update `_build_agent_execution_command` in `kanban_dashboard.py` with agent-specific CLI flags.
  - Test: Check logs to ensure `gemini` is called without `exec -C`.
  - Evidence: Refactored function using conditional logic for codex/gemini/claude.
- [ ] 2. Update `build_agent_execution_command` in `run_agent.py` with matching logic.
  - Test: Manual execution of agent controller.
  - Evidence: Matching code changes in `run_agent.py`.
- [ ] 3. Update version in `constants.py`.
  - Test: Check `VERSION` is `V20260317_1715`.
  - Evidence: `constants.py` updated.

## Evidence
Objective-Delivery-Coverage: 0%
Auto-Acceptance: true

- Evidence-Type: diff
  - Artifact: `workstream\kanban_dashboard.py`
  - Objective-Proved: Command builder fixed for all agents.
  - Status: planned
- Evidence-Type: diff
  - Artifact: `workstream\run_agent.py`
  - Objective-Proved: Standalone controller command builder fixed.
  - Status: planned
- Evidence-Type: file_output
  - Artifact: `TradeApps\breakout\fs\constants.py`
  - Objective-Proved: Version bumped to V20260317_1715.
  - Status: planned

## Implementation Log
- 2026-03-17 15:20: Task initiated.

## Changes Made
- (Pending)

## Validation
- (Pending)

## Risks/Notes
- None.

## Completion Status
**PENDING**


## Execution Evidence
- Agent lane: gemini
- Command: C:\Users\edebe\AppData\Roaming\npm\gemini.CMD exec -C C:\Users\edebe\eds Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress/gemini\20260317_171500_agent_cli_syntax_fix.md. Implement required changes in the workspace, run validations, and update checklist items.
- Return code: 1
- Stderr:
```text
Unknown argument: C
Usage: gemini [options] [command]

Gemini CLI - Defaults to interactive mode. Use -p/--prompt for non-interactive (headless) mode.

Commands:
  gemini [query..]             Launch Gemini CLI  [default]
  gemini mcp                   Manage MCP servers
  gemini extensions <command>  Manage Gemini CLI extensions.  [aliases: extension]
  gemini skills <command>      Manage agent skills.  [aliases: skill]
  gemini hooks <command>       Manage Gemini CLI hooks.  [aliases: hook]

Positionals:
  query  Initial prompt. Runs in interactive mode by default; use -p/--prompt for non-interactive.

Options:
  -d, --debug                     Run in debug mode (open debug console with F12)  [boolean] [default: false]
  -m, --model                     Model  [string]
  -p, --prompt                    Run in non-interactive (headless) mode with the given prompt. Appended to input on stdin (if any).  [string]
  -i, --prompt-interactive        Execute the provided prompt and continue in interactive mode  [string]
  -s, --sandbox                   Run in sandbox?  [boolean]
  -y, --yolo                      Automatically accept all actions (aka YOLO mode, see https://www.youtube.com/watch?v=xvFZjo5PgG0 for more details)?  [boolean] [default: false]
      --approval-mode             Set the approval mode: default (prompt for approval), auto_edit (auto-approve edit tools), yolo (auto-approve all tools), plan (read-only mode)  [string] [choices: "default", "auto_edit", "yolo", "plan"]
      --policy                    Additional policy files or directories to load (comma-separated or multiple --policy)  [array]
      --acp                       Starts the agent in ACP mode  [boolean]
      --experimental-acp          Starts the agent in ACP mode (deprecated, use --acp instead)  [boolean]
      --allowed-mcp-server-names  Allowed MCP server names  [array]
      --allowed-tools             [DEPRECATED: Use Policy Engine instead See https://geminicli.com/docs/core/policy-engine] Tools that are allowed to run without confirmation  [array]
  -e, --extensions                A list of extensions to use. If not provided, all extensions are used.  [array]
  -l, --list-extensions           List all available extensions and exit.  [boolean]
  -r, --resume                    Resume a previous session. Use "latest" for most recent or index number (e.g. --resume 5)  [string]
      --list-sessions             List available sessions for the current project and exit.  [boolean]
      --delete-session            Delete a session by index number (use --list-sessions to see available sessions).  [string]
      --include-directories       Additional directories to include in the workspace (comma-separated or multiple --include-directories)  [array]
      --screen-reader             Enable screen reader mode for accessibility.  [boolean]
  -o, --output-format             The format of the CLI output.  [string] [choices: "text", "json", "stream-json"]
      --raw-output                Disable sanitization of model output (e.g. allow ANSI escape sequences). WARNING: This can be a security risk if the model output is untrusted.  [boolean]
      --accept-raw-output-risk    Suppress the security warning when using --raw-output.  [boolean]
  -v, --version                   Show version number  [boolean]
  -h, --help                      Show help  [boolean]
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
