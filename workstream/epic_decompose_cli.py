import argparse
import json
import os
import datetime
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(r"C:\Users\edebe\eds")
EPIC_SKILL_PATH = REPO_ROOT / "skills" / "epic-decomposition" / "SKILL.md"
UI_VIEWABILITY_SKILL_PATH = REPO_ROOT / "skills" / "ui-delivery-viewability" / "SKILL.md"

OUTPUT_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "epic_name": {"type": "string"},
        "epic_slug": {"type": "string"},
        "summary": {"type": "string"},
        "warnings": {"type": "array", "items": {"type": "string"}},
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "title": {"type": "string"},
                    "workstream_letter": {"type": "string"},
                    "workstream_name": {"type": "string"},
                    "workstream_goal": {"type": "string"},
                    "purpose": {"type": "string"},
                    "input": {"type": "string"},
                    "output": {"type": "string"},
                    "fields": {"type": "array", "items": {"type": "string"}},
                    "action": {"type": "string"},
                    "verification": {"type": "array", "items": {"type": "string"}},
                    "priority": {"type": "integer"},
                    "dependencies": {"type": "array", "items": {"type": "string"}},
                    "suggested_agent": {"type": "string"},
                    "ui_viewability": {"type": "boolean"},
                },
                "required": [
                    "id",
                    "title",
                    "workstream_letter",
                    "workstream_name",
                    "workstream_goal",
                    "purpose",
                    "input",
                    "output",
                    "fields",
                    "action",
                    "verification",
                    "priority",
                    "dependencies",
                    "suggested_agent",
                    "ui_viewability",
                ],
            },
        },
    },
    "required": ["epic_name", "epic_slug", "summary", "warnings", "tasks"],
}


def _slugify(value: str) -> str:
    return "_".join(
        chunk for chunk in "".join(ch.lower() if ch.isalnum() else "_" for ch in value).split("_") if chunk
    )


def _load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _build_prompt(epic_path: Path, epic_text: str, epic_skill: str, ui_skill: str) -> str:
    return f"""You are decomposing a product/engineering epic into executable markdown task files.

Follow these instructions in order:
1. Use the epic decomposition skill as the primary contract for structure, naming intent, metadata, and decomposition completeness.
2. Apply the UI delivery viewability skill only when a generated task is user-facing UI, dashboard, screen, or operator workflow work. For those tasks, include verification criteria covering:
   - an access/start script,
   - the localhost URL to open,
   - startup smoke validation,
   - screenshot capture evidence.
3. Decompose the epic into MANY deliverable tasks. Do not collapse whole product areas into one vague task. Split work into implementable increments that a model can execute independently.
4. Preserve and infer missing detail conservatively. If the epic is under-specified, derive sensible tasks, dependencies, and verification based on the stated MVP goals.
5. Ensure every task links cleanly to the source epic and is review/allocation ready.

Output JSON only, matching the provided schema exactly.

Epic path: {epic_path}

Epic Decomposition Skill:
{epic_skill}

UI Delivery Viewability Skill:
{ui_skill}

Epic Markdown:
```markdown
{epic_text}
```

Output requirements:
- epic_name: the canonical epic title
- epic_slug: snake_case slug matching epic_name
- summary: short summary of the decomposition
- warnings: any caveats, assumptions, or inferred areas
- tasks: list of executable tasks

Task requirements:
- id: stable task id like A1, A2, B1, etc
- title: concise but descriptive deliverable title
- workstream_letter: single letter if available, otherwise assign a sensible letter grouping
- workstream_name: meaningful workstream name
- workstream_goal: optional overall goal for this workstream
- purpose, input, output, action: concrete and implementation-oriented
- fields: include only if materially useful
- verification: checklist-ready items, at least 2 for normal tasks and more for risky/UI tasks
- priority: 1, 2, or 3
- dependencies: explicit task ids where appropriate
- suggested_agent: optional recommendation from {{codex, gemini, claude, general}}
- ui_viewability: true only for UI-visible deliverables

Quality bar:
- Cover the full epic, especially MVP-critical areas.
- Prefer 10+ tasks for a large epic unless the document is genuinely tiny.
- Make each task independently reviewable and allocatable.
- Avoid placeholders like "implement feature" without scope.

MANDATORY INFRASTRUCTURE TASKS:
Every decomposition MUST include a dedicated infrastructure/DevOps workstream (typically Workstream Z or the last letter) containing these tasks:
1. setup.sh / setup.bat - Automated setup script that installs dependencies, creates databases, applies migrations, and configures environment
2. docker-compose.yml - Local development environment with all required services (database, cache, message queue, etc.)
3. README.md - Installation instructions, environment variables, API documentation, and usage examples
4. .env.example - Template for all required environment variables with descriptions
5. Database initialization - Schema creation, seed data, and migration scripts that run automatically
6. Health check / smoke test - Script or endpoint to verify the deployment is working

These infrastructure tasks should:
- Be marked as priority 1 (high priority)
- Have clear verification criteria (e.g., "Running setup.sh creates database and starts server on port X")
- Block application tasks that depend on working infrastructure
- Include concrete file paths and commands in their Output section

Do NOT generate a solution that requires manual setup steps not captured in scripts.

MANDATORY UI WORKSTREAM (when applicable):
If the epic describes ANY user-facing functionality (dashboards, admin panels, user interfaces, forms, visual displays, user interactions), you MUST include a dedicated UI/Frontend workstream containing:
1. UI Scaffold - Framework setup (React + Vite recommended), directory structure, dev server
2. Core Layout - Navigation, header, routing, shared components
3. Authentication UI - Login/logout screens if auth is required
4. Primary Views - One task per major screen/page described in the epic
5. API Integration - Connect frontend to backend endpoints
6. Responsive Design - Mobile and desktop layout support

Detection: Include UI workstream if epic mentions: dashboard, admin panel, interface, frontend, user can see/view/browse, display, forms, buttons, tables, charts, or any visual interaction.

UI task requirements:
- Specify route/URL path for each view
- List components to create
- Reference API endpoints consumed
- Include visual verification (localhost URL + expected behavior)
- Depend on backend API tasks

Do NOT generate a backend-only solution when the epic clearly describes user-facing features.

UI SKILL REFERENCES:
Each UI task MUST include a "Required Skills" section referencing:
- skills/skills-main/skills/frontend-design/SKILL.md - Design aesthetics, avoid generic AI slop
- skills/skills-main/skills/web-artifacts-builder/SKILL.md - React + Vite + Tailwind + shadcn/ui
- skills/skills-main/skills/webapp-testing/SKILL.md - Playwright UI testing
- skills/ui-delivery-viewability/SKILL.md - Starter scripts, screenshot evidence

UI Design Quality (from frontend-design skill):
AVOID: Generic fonts (Inter, Roboto), purple gradients, uniform rounded corners, centered layouts
INCLUDE: Distinctive typography, cohesive color palettes, motion/animations, atmospheric backgrounds
"""


def _default_command(repo_root: Path, schema_path: Path, output_path: Path) -> list[str]:
    codex_bin = (
        shutil.which("codex")
        or shutil.which("codex.cmd")
        or shutil.which("codex.exe")
        or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")
    )
    return [
        codex_bin,
        "exec",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--output-schema",
        str(schema_path),
        "-o",
        str(output_path),
        "-C",
        str(repo_root),
        "-",
    ]


def _build_command(
    repo_root: Path,
    input_path: Path,
    schema_path: Path,
    output_path: Path,
    prompt_path: Path,
) -> list[str]:
    override = os.environ.get("KANBAN_EPIC_DECOMP_CMD", "").strip()
    if not override:
        return _default_command(repo_root, schema_path, output_path)
    formatted = override.format(
        repo_root=str(repo_root),
        input_path=str(input_path),
        schema_path=str(schema_path),
        output_path=str(output_path),
        prompt_path=str(prompt_path),
    )
    return shlex.split(formatted, posix=False)


def _normalize_task(task: dict, fallback_epic_slug: str) -> dict:
    workstream_letter = (str(task.get("workstream_letter") or "G").strip() or "G")[0].upper()
    workstream_name = str(task.get("workstream_name") or f"Workstream {workstream_letter}").strip()
    verification = [str(item).strip() for item in task.get("verification") or [] if str(item).strip()]
    if len(verification) < 2:
        verification.extend(
            [
                "Implementation matches the epic requirements for this deliverable.",
                "Validation evidence is captured for review and allocation handoff.",
            ][: 2 - len(verification)]
        )
    priority = task.get("priority", 2)
    try:
        priority = int(priority)
    except Exception:
        priority = 2
    if priority not in {1, 2, 3}:
        priority = 2
    normalized = {
        "id": str(task.get("id") or "").strip() or "TASK",
        "title": str(task.get("title") or "").strip() or "Untitled Task",
        "workstream_letter": workstream_letter,
        "workstream_name": workstream_name,
        "workstream_goal": str(task.get("workstream_goal") or "").strip(),
        "purpose": str(task.get("purpose") or "").strip() or "Deliver the scoped work for this task.",
        "input": str(task.get("input") or "").strip() or f"Source epic context from {fallback_epic_slug}.",
        "output": str(task.get("output") or "").strip() or "Task deliverables completed and documented.",
        "fields": [str(item).strip() for item in task.get("fields") or [] if str(item).strip()],
        "action": str(task.get("action") or "").strip(),
        "verification": verification,
        "priority": priority,
        "dependencies": [str(item).strip() for item in task.get("dependencies") or [] if str(item).strip()],
        "suggested_agent": str(task.get("suggested_agent") or "").strip().lower(),
        "ui_viewability": bool(task.get("ui_viewability", False)),
    }
    return normalized


def _normalize_payload(payload: dict, input_path: Path) -> dict:
    epic_name = str(payload.get("epic_name") or input_path.stem).strip() or input_path.stem
    epic_slug = _slugify(str(payload.get("epic_slug") or epic_name)) or _slugify(input_path.stem) or "epic"
    tasks_raw = payload.get("tasks")
    if not isinstance(tasks_raw, list) or not tasks_raw:
        raise ValueError("LLM decomposition returned no tasks.")
    tasks = [_normalize_task(task, epic_slug) for task in tasks_raw if isinstance(task, dict)]
    if not tasks:
        raise ValueError("LLM decomposition returned no valid tasks.")
    return {
        "epic_name": epic_name,
        "epic_slug": epic_slug,
        "summary": str(payload.get("summary") or "").strip() or f"Decomposed {epic_name} into {len(tasks)} tasks.",
        "warnings": [str(item).strip() for item in payload.get("warnings") or [] if str(item).strip()],
        "tasks": tasks,
    }


def run_decomposition(input_path: Path) -> dict:
    epic_text = _load_text(input_path)
    epic_skill = _load_text(EPIC_SKILL_PATH)
    ui_skill = _load_text(UI_VIEWABILITY_SKILL_PATH)
    prompt = _build_prompt(input_path, epic_text, epic_skill, ui_skill)
    scratch_root = REPO_ROOT / "workstream" / "artefacts"
    scratch_root.mkdir(parents=True, exist_ok=True)
    tmp_root = scratch_root / f"epic_decomp_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    tmp_root.mkdir(parents=True, exist_ok=False)
    schema_path = tmp_root / "epic_decomp_schema.json"
    output_path = tmp_root / "epic_decomp_output.json"
    prompt_path = tmp_root / "epic_decomp_prompt.txt"
    schema_path.write_text(json.dumps(OUTPUT_SCHEMA, indent=2), encoding="utf-8")
    prompt_path.write_text(prompt, encoding="utf-8")
    cmd = _build_command(REPO_ROOT, input_path, schema_path, output_path, prompt_path)
    proc = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        err = (proc.stderr or proc.stdout or "").strip()
        raise RuntimeError(f"Epic decomposition command failed (rc={proc.returncode}): {err[-2000:]}")
    if not output_path.exists():
        raise RuntimeError("Epic decomposition command did not produce an output file.")
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    result = _normalize_payload(payload, input_path)
    result["command"] = cmd
    result["artefact_dir"] = str(tmp_root)
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="LLM-backed epic decomposition CLI")
    parser.add_argument("--input", required=True, help="Path to the source epic markdown file")
    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        raise SystemExit(json.dumps({"error": f"input_not_found: {input_path}"}))
    result = run_decomposition(input_path)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
