from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

WORKSTREAM_ROOT = Path(r"C:\Users\edebe\eds\workstream")
APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
STATE_FOLDERS = ("100_backlog", "200_inprogress", "300_complete", "400_failed")
MODEL_FOLDERS = ("gemini", "claude", "codex")


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return cleaned or "unclassified"


@dataclass(frozen=True)
class ParsedTask:
    path: Path
    filename: str
    title: str
    workstream: str
    workstream_group: str
    task_id: str
    epic: str
    epic_slug: str
    priority: int
    status_folder: str
    agent: str | None
    content: str
    purpose: str
    input_text: str
    output_text: str
    verification_text: str
    rejection_reason: str | None
    timestamp: str


class AllocateRequest(BaseModel):
    task_paths: list[str] = Field(default_factory=list)
    target_model: str


class RejectRequest(BaseModel):
    task_paths: list[str] = Field(default_factory=list)
    reason: str = Field(min_length=1)


class MoveToGeneralRequest(BaseModel):
    task_paths: list[str] = Field(default_factory=list)


def _extract_heading_section(content: str, heading: str) -> str:
    pattern = rf"(?im)^##?\s*{re.escape(heading)}\s*$\n(.*?)(?=^\s*##?\s+|\Z)"
    match = re.search(pattern, content, re.DOTALL | re.MULTILINE)
    return match.group(1).strip() if match else ""


def _extract_metadata(content: str, label: str) -> str:
    match = re.search(rf"(?im)^\*\*{re.escape(label)}:\*\*\s*(.+)$", content)
    if match:
        return match.group(1).strip()
    match = re.search(rf"(?im)^{re.escape(label)}:\s*(.+)$", content)
    return match.group(1).strip() if match else ""


def _extract_task_id(title: str) -> str:
    match = re.search(r"\b([A-Z]\d+(?:\.\d+)?)\b", title)
    if match:
        return match.group(1)
    match = re.search(r"\btask[_\s-]*(\d+)\b", title, re.IGNORECASE)
    return f"TASK-{match.group(1)}" if match else "N/A"


def _extract_workstream_group(workstream: str, filename: str) -> str:
    match = re.search(r"\b([A-Z])\b", workstream)
    if match:
        return match.group(1)
    match = re.search(r"workstream([a-z])", filename, re.IGNORECASE)
    return match.group(1).upper() if match else "General"


def _extract_rejection_reason(content: str) -> str | None:
    match = re.search(r"(?im)^Rejection Reason:\s*(.+)$", content)
    return match.group(1).strip() if match else None


def _task_title_from_content(content: str, filename: str) -> str:
    first_heading = re.search(r"(?im)^#\s*(.+)$", content)
    if first_heading:
        return first_heading.group(1).strip()
    return filename.rsplit(".", 1)[0]


def _parse_task(task_file: Path, root: Path) -> ParsedTask:
    content = task_file.read_text(encoding="utf-8")
    try:
        rel_parts = task_file.relative_to(root).parts
        status_folder = rel_parts[0]
        agent = rel_parts[1] if len(rel_parts) > 2 and rel_parts[1] in MODEL_FOLDERS else None
    except ValueError:
        rel_parts = ()
        status_folder = "external"
        agent = None
    filename = task_file.name
    title = _task_title_from_content(content, filename)
    workstream = _extract_metadata(content, "Workstream") or "Unknown"
    epic = _extract_metadata(content, "Epic") or "Unspecified Epic"
    priority_raw = _extract_metadata(content, "Priority") or "3"
    try:
        priority = int(re.search(r"\d+", priority_raw).group(0))  # type: ignore[union-attr]
    except Exception:
        priority = 3
    timestamp_match = re.match(r"(\d{8}_\d{6})", filename)
    return ParsedTask(
        path=task_file,
        filename=filename,
        title=title,
        workstream=workstream,
        workstream_group=_extract_workstream_group(workstream, filename),
        task_id=_extract_task_id(title),
        epic=epic,
        epic_slug=slugify(epic),
        priority=priority,
        status_folder=status_folder,
        agent=agent,
        content=content,
        purpose=_extract_heading_section(content, "Purpose"),
        input_text=_extract_heading_section(content, "Input"),
        output_text=_extract_heading_section(content, "Output"),
        verification_text=_extract_heading_section(content, "Verification"),
        rejection_reason=_extract_rejection_reason(content),
        timestamp=timestamp_match.group(1) if timestamp_match else "",
    )


def _resolve_repo_path(root: Path, rel_path: str) -> Path:
    root_resolved = root.resolve()
    target = (root_resolved.parent / str(rel_path or "").strip()).resolve()
    if target != root_resolved.parent and root_resolved.parent not in target.parents:
        raise HTTPException(status_code=400, detail=f"path_outside_repo: {rel_path}")
    return target


def get_task_files(root: Path, folder: str | None = None) -> list[Path]:
    task_files: list[Path] = []
    if folder:
        folder_path = _resolve_repo_path(root, folder)
        if folder_path.exists():
            task_files.extend(folder_path.rglob("*.md"))
        return task_files
    for folder in STATE_FOLDERS:
        folder_path = root / folder
        if not folder_path.exists():
            continue
        task_files.extend(folder_path.rglob("*.md"))
    return task_files


def list_epic_documents(root: Path, path: str = "workstream/000_epic") -> list[dict[str, Any]]:
    epic_root = _resolve_repo_path(root, path)
    if not epic_root.exists():
        return []
    epics: dict[str, dict[str, Any]] = {}
    for epic_file in epic_root.rglob("*.md"):
        if not epic_file.is_file():
            continue
        try:
            rel_parts = epic_file.relative_to(epic_root).parts
        except ValueError:
            rel_parts = epic_file.parts
        if any(part in MODEL_FOLDERS for part in rel_parts[:-1]):
            continue
        lowered = epic_file.name.lower()
        if lowered.endswith("_processed.md") or lowered.endswith("_review.md"):
            continue
        content = epic_file.read_text(encoding="utf-8", errors="replace")
        name = _task_title_from_content(content, epic_file.name)
        slug = slugify(name)
        epics.setdefault(
            slug,
            {
                "slug": slug,
                "name": name,
                "path": str(epic_file.relative_to(root.parent)).replace("\\", "/"),
            },
        )
    return sorted(epics.values(), key=lambda item: item["name"].lower())


def list_epics(root: Path, folder: str | None = None) -> list[dict[str, Any]]:
    epics: dict[str, dict[str, Any]] = {}
    for task_file in get_task_files(root, folder):
        task = _parse_task(task_file, root)
        entry = epics.setdefault(
            task.epic_slug,
            {"slug": task.epic_slug, "name": task.epic, "task_count": 0, "workstreams": set()},
        )
        entry["task_count"] += 1
        entry["workstreams"].add(task.workstream_group)
    return sorted(
        [
            {
                "slug": epic["slug"],
                "name": epic["name"],
                "task_count": epic["task_count"],
                "workstreams": sorted(epic["workstreams"]),
            }
            for epic in epics.values()
        ],
        key=lambda item: item["name"].lower(),
    )


def get_epic_tasks(
    root: Path,
    epic_slug: str,
    workstream: str | None = None,
    status: str | None = None,
    priority: int | None = None,
    sort_by: str = "priority",
    folder: str | None = None,
) -> list[dict[str, Any]]:
    tasks: list[ParsedTask] = []
    for task_file in get_task_files(root, folder):
        task = _parse_task(task_file, root)
        if task.epic_slug != epic_slug:
            continue
        if workstream and task.workstream_group != workstream:
            continue
        if status and task.status_folder != status:
            continue
        if priority and task.priority != priority:
            continue
        tasks.append(task)
    sorters = {
        "priority": lambda item: (item.priority, item.workstream_group, item.timestamp),
        "workstream": lambda item: (item.workstream_group, item.priority, item.timestamp),
        "timestamp": lambda item: (item.timestamp, item.priority, item.workstream_group),
    }
    key_fn = sorters.get(sort_by, sorters["priority"])
    ordered = sorted(tasks, key=key_fn)
    return [
        {
            "path": str(task.path),
            "filename": task.filename,
            "title": task.title,
            "workstream": task.workstream,
            "workstream_group": task.workstream_group,
            "task_id": task.task_id,
            "epic": task.epic,
            "epic_slug": task.epic_slug,
            "priority": task.priority,
            "status_folder": task.status_folder,
            "agent": task.agent,
            "content": task.content,
            "purpose": task.purpose,
            "input": task.input_text,
            "output": task.output_text,
            "verification": task.verification_text,
            "rejection_reason": task.rejection_reason,
            "timestamp": task.timestamp,
        }
        for task in ordered
    ]


def _ensure_model(target_model: str) -> None:
    if target_model not in MODEL_FOLDERS:
        raise HTTPException(status_code=400, detail=f"Unsupported model: {target_model}")


def allocate_tasks(task_paths: list[str], target_model: str, root: Path) -> dict[str, list[dict[str, str]]]:
    _ensure_model(target_model)
    target_dir = root / "100_backlog" / target_model
    target_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        dest = target_dir / src.name
        try:
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


def reject_tasks(task_paths: list[str], reason: str, root: Path) -> dict[str, list[dict[str, str]]]:
    failed_root = root / "400_failed"
    failed_root.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        task = _parse_task(src, root)
        target_dir = failed_root / task.agent if task.agent else failed_root
        target_dir.mkdir(parents=True, exist_ok=True)
        dest = target_dir / src.name
        try:
            src.write_text(task.content.rstrip() + f"\n\nRejection Reason: {reason}\n", encoding="utf-8")
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


def model_status(root: Path) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for model in MODEL_FOLDERS:
        folder = root / "100_backlog" / model
        count = len(list(folder.glob("*.md"))) if folder.exists() else 0
        output.append({"model": model, "count": count})
    return output


def _retag_task_filename(filename: str, target_agent: str = "general") -> str:
    match = re.match(r"^(\d{8}_\d{6})_([^_]+)_(.+)\.md$", filename)
    if not match:
        return filename
    timestamp, part1, rest = match.groups()
    if part1.lower() in MODEL_FOLDERS + ("general",):
        return f"{timestamp}_{target_agent}_{rest}.md"
    return f"{timestamp}_{target_agent}_{part1}_{rest}.md"


def move_tasks_to_general(task_paths: list[str], root: Path) -> dict[str, list[dict[str, str]]]:
    target_dir = root / "100_backlog" / "general"
    target_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, list[dict[str, str]]] = {"success": [], "failed": []}
    for task_path in task_paths:
        src = Path(task_path)
        if not src.exists():
            results["failed"].append({"path": task_path, "error": "File not found"})
            continue
        dest = target_dir / _retag_task_filename(src.name, "general")
        try:
            if src.resolve() == dest.resolve():
                results["success"].append({"path": task_path, "dest": str(dest), "note": "Already in general backlog"})
                continue
            shutil.move(str(src), str(dest))
            results["success"].append({"path": task_path, "dest": str(dest)})
        except Exception as exc:
            results["failed"].append({"path": task_path, "error": str(exc)})
    return results


class AugmentEpicRequest(BaseModel):
    epic_slug: str
    solution_path: str
    augment_types: list[str] = Field(default_factory=list)
    feature_description: str = ""


def list_epics_with_solutions(root: Path) -> list[dict[str, Any]]:
    """List epics that have solution folders (ep_*)."""
    base_dir = root.parent  # C:/Users/edebe/eds
    epics: list[dict[str, Any]] = []

    for item in base_dir.iterdir():
        if item.is_dir() and item.name.startswith("ep_"):
            solution_dir = item / "solution"
            if solution_dir.exists():
                epic_slug = item.name[3:]  # Remove 'ep_' prefix
                epics.append({
                    "slug": epic_slug,
                    "name": epic_slug.replace("_", " ").title(),
                    "path": str(item.relative_to(base_dir)).replace("\\", "/"),
                    "solution_path": str(item.relative_to(base_dir)).replace("\\", "/"),
                    "has_solution": True
                })

    return sorted(epics, key=lambda x: x["name"].lower())


def analyze_solution_folder(root: Path, solution_path: str) -> dict[str, Any]:
    """Analyze an existing solution folder to understand its structure."""
    base_dir = root.parent
    full_path = base_dir / solution_path

    if not full_path.exists():
        return {"error": f"Path not found: {solution_path}"}

    analysis = {
        "total_files": 0,
        "total_dirs": 0,
        "has_backend": False,
        "has_frontend": False,
        "has_mobile": False,
        "has_tests": False,
        "has_infra": False,
        "has_docs": False,
        "backend_details": "",
        "frontend_details": "",
        "mobile_details": "",
        "test_details": "",
        "infra_details": "",
        "key_files": []
    }

    # Collect all files
    all_files: list[str] = []
    for item in full_path.rglob("*"):
        if item.is_file():
            analysis["total_files"] += 1
            rel_path = str(item.relative_to(full_path)).replace("\\", "/")
            all_files.append(rel_path)
        elif item.is_dir():
            analysis["total_dirs"] += 1

    # Detect backend
    backend_indicators = ["backend", "server", "api", "src/app.js", "src/index.js", "main.py", "app.py"]
    for indicator in backend_indicators:
        if any(indicator in f.lower() for f in all_files) or (full_path / "solution" / "backend").exists() or (full_path / "backend").exists():
            analysis["has_backend"] = True
            if any("express" in f.lower() or "app.js" in f.lower() for f in all_files):
                analysis["backend_details"] = "Express/Node.js API"
            elif any("fastapi" in f.lower() or "uvicorn" in f.lower() for f in all_files):
                analysis["backend_details"] = "FastAPI/Python"
            elif any("flask" in f.lower() for f in all_files):
                analysis["backend_details"] = "Flask/Python"
            else:
                analysis["backend_details"] = "Backend API"
            break

    # Detect mobile app
    mobile_indicators = ["react-native", "expo", "App.tsx", "app.json", "eas.json", "android/", "ios/", "flutter", "pubspec.yaml"]
    for indicator in mobile_indicators:
        if any(indicator in f for f in all_files) or (full_path / "solution" / "app").exists() or (full_path / "app").exists():
            # Check file contents for mobile imports
            is_mobile = False
            for f in all_files:
                if f.endswith(".tsx") or f.endswith(".ts"):
                    try:
                        file_content = (full_path / f).read_text(encoding="utf-8", errors="replace")[:2000]
                        if "react-native" in file_content or "expo" in file_content.lower():
                            is_mobile = True
                            break
                    except Exception:
                        pass
            if is_mobile or "expo" in indicator or "react-native" in indicator or "flutter" in indicator:
                analysis["has_mobile"] = True
                if any("expo" in f.lower() for f in all_files) or is_mobile:
                    analysis["mobile_details"] = "React Native + Expo"
                elif any("flutter" in f.lower() or "pubspec" in f.lower() for f in all_files):
                    analysis["mobile_details"] = "Flutter"
                else:
                    analysis["mobile_details"] = "Mobile app"
                break

    # Detect web frontend (only if no mobile detected)
    frontend_indicators = ["frontend", "src/pages", "src/components", "public/index.html", "vite.config", "next.config"]
    if not analysis["has_mobile"]:
        for indicator in frontend_indicators:
            if any(indicator in f for f in all_files) or (full_path / "solution" / "frontend").exists() or (full_path / "frontend").exists():
                analysis["has_frontend"] = True
                if any("react" in f.lower() or ".jsx" in f.lower() or ".tsx" in f.lower() for f in all_files):
                    analysis["frontend_details"] = "React application"
                elif any("vue" in f.lower() for f in all_files):
                    analysis["frontend_details"] = "Vue application"
                else:
                    analysis["frontend_details"] = "Web UI"
                break

    # Detect tests
    test_indicators = ["test", "tests", "spec", "__tests__", ".test.", ".spec."]
    if any(any(indicator in f.lower() for indicator in test_indicators) for f in all_files):
        analysis["has_tests"] = True
        test_files = [f for f in all_files if any(indicator in f.lower() for indicator in test_indicators)]
        analysis["test_details"] = f"{len(test_files)} test file(s)"

    # Detect infrastructure
    infra_indicators = ["docker", "Dockerfile", "docker-compose", "setup.sh", "setup.bat", ".env.example", "Makefile"]
    if any(any(indicator in f for indicator in infra_indicators) for f in all_files):
        analysis["has_infra"] = True
        if any("docker" in f.lower() for f in all_files):
            analysis["infra_details"] = "Docker configuration"
        elif any("setup" in f.lower() for f in all_files):
            analysis["infra_details"] = "Setup scripts"
        else:
            analysis["infra_details"] = "Infrastructure files"

    # Detect documentation
    doc_indicators = ["README", "docs/", "CHANGELOG", "API.md", "CONTRIBUTING"]
    if any(any(indicator in f for indicator in doc_indicators) for f in all_files):
        analysis["has_docs"] = True

    # Key files
    key_patterns = ["package.json", "requirements.txt", "schema.sql", "app.js", "index.js", "main.py", "routes", "models", "controllers"]
    analysis["key_files"] = sorted([f for f in all_files if any(p in f for p in key_patterns)])[:20]

    return analysis


def run_augmentation(
    root: Path,
    epic_slug: str,
    solution_path: str,
    augment_types: list[str],
    feature_description: str = ""
) -> dict[str, Any]:
    """Generate augmentation tasks for an existing epic solution."""
    import datetime
    import json
    import subprocess
    import tempfile

    base_dir = root.parent
    full_path = base_dir / solution_path

    if not full_path.exists():
        raise HTTPException(status_code=400, detail=f"Solution path not found: {solution_path}")

    analysis = analyze_solution_folder(root, solution_path)

    # Collect existing files
    existing_files: list[str] = []
    for item in full_path.rglob("*"):
        if item.is_file():
            existing_files.append(str(item.relative_to(full_path)).replace("\\", "/"))

    # Read key file contents for context
    key_file_contents: dict[str, str] = {}
    for key_file in analysis.get("key_files", [])[:5]:
        try:
            file_path = full_path / key_file
            if file_path.exists() and file_path.stat().st_size < 50000:
                key_file_contents[key_file] = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Build augmentation description
    augment_desc_parts = []
    if "ui" in augment_types:
        if analysis.get("has_mobile"):
            augment_desc_parts.append(f"- **Mobile UI**: Enhance existing {analysis.get('mobile_details', 'mobile app')} with additional screens and features")
        elif analysis.get("has_frontend"):
            augment_desc_parts.append(f"- **Web UI**: Enhance existing {analysis.get('frontend_details', 'web frontend')} with additional pages and features")
        else:
            augment_desc_parts.append("- **UI/Frontend**: Create React + Vite frontend that integrates with existing backend APIs")
    if "tests" in augment_types:
        augment_desc_parts.append("- **Tests**: Create test suite (unit tests, integration tests) for existing code")
    if "docs" in augment_types:
        augment_desc_parts.append("- **Documentation**: Create README, API documentation, usage guides")
    if "infra" in augment_types:
        augment_desc_parts.append("- **Infrastructure**: Create setup scripts, Docker configuration, CI/CD")
    if "feature" in augment_types and feature_description:
        augment_desc_parts.append(f"- **New Feature**: {feature_description}")

    augment_desc = "\n".join(augment_desc_parts)
    files_summary = "\n".join(f"  - {f}" for f in existing_files[:50])

    key_files_summary = ""
    for filename, content in key_file_contents.items():
        key_files_summary += f"\n### {filename}\n```\n{content[:1000]}\n```\n"

    prompt = f"""You are generating AUGMENTATION TASKS for an existing epic solution.

## Existing Solution Context

**Epic:** {epic_slug}
**Solution Path:** {solution_path}

### Current Solution Analysis
- Total Files: {analysis.get('total_files', 0)}
- Has Backend: {analysis.get('has_backend', False)} ({analysis.get('backend_details', '')})
- Has Mobile App: {analysis.get('has_mobile', False)} ({analysis.get('mobile_details', '')})
- Has Web Frontend: {analysis.get('has_frontend', False)} ({analysis.get('frontend_details', '')})
- Has Tests: {analysis.get('has_tests', False)} ({analysis.get('test_details', '')})
- Has Infrastructure: {analysis.get('has_infra', False)} ({analysis.get('infra_details', '')})

### Existing Files (sample)
{files_summary}

{key_files_summary}

## Augmentation Request

Generate tasks to ADD the following to the existing solution:
{augment_desc}

## Requirements

1. Tasks MUST reference existing files and APIs from the solution
2. Tasks MUST build ON TOP OF the existing codebase, not replace it
3. New code should be placed in appropriate subdirectories:
   - Mobile App: `{solution_path}/solution/app/` (React Native/Expo screens, components)
   - Web UI: `{solution_path}/solution/frontend/`
   - Tests: `{solution_path}/solution/backend/tests/` or `{solution_path}/solution/app/tests/`
   - Docs: `{solution_path}/` (README.md, docs/)
   - Infrastructure: `{solution_path}/` (setup.sh, docker-compose.yml, eas.json, app.json)
4. Include specific file paths, API endpoints to consume, and integration points
5. Each task should be independently implementable

Generate 3-8 tasks depending on complexity.
"""

    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "reasoning": {"type": "string"},
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
                        "purpose": {"type": "string"},
                        "input": {"type": "string"},
                        "output": {"type": "string"},
                        "action": {"type": "string"},
                        "verification": {"type": "array", "items": {"type": "string"}},
                        "existing_files_to_reference": {"type": "array", "items": {"type": "string"}},
                        "new_files_to_create": {"type": "array", "items": {"type": "string"}},
                        "priority": {"type": "integer"}
                    },
                    "required": ["id", "title", "workstream_letter", "workstream_name", "purpose", "input", "output", "action", "verification", "existing_files_to_reference", "new_files_to_create", "priority"]
                }
            }
        },
        "required": ["reasoning", "tasks"]
    }

    # Run codex CLI
    codex_bin = (
        shutil.which("codex")
        or shutil.which("codex.cmd")
        or shutil.which("codex.exe")
        or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")
    )

    with tempfile.TemporaryDirectory() as tmp_dir:
        schema_path = Path(tmp_dir) / "schema.json"
        output_path = Path(tmp_dir) / "output.json"

        schema_path.write_text(json.dumps(schema, indent=2), encoding="utf-8")

        cmd = [
            codex_bin,
            "exec",
            "--skip-git-repo-check",
            "--sandbox", "read-only",
            "--output-schema", str(schema_path),
            "-o", str(output_path),
            "-C", str(base_dir),
            "-"
        ]

        try:
            proc = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=180
            )
        except subprocess.TimeoutExpired:
            raise HTTPException(status_code=500, detail="Augmentation timed out after 180 seconds")

        if proc.returncode != 0:
            err = (proc.stderr or proc.stdout or "").strip()
            raise HTTPException(status_code=500, detail=f"Augmentation failed (rc={proc.returncode}): {err[-2000:]}")

        if not output_path.exists():
            raise HTTPException(status_code=500, detail="Augmentation did not produce output")

        payload = json.loads(output_path.read_text(encoding="utf-8"))

    # Generate task files
    tasks_created: list[dict[str, str]] = []
    timestamp_base = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    for idx, task in enumerate(payload.get("tasks", [])):
        task_id = task.get("id", f"AUG{idx+1}")

        content_lines = [
            f"# TASK {task_id}: {task.get('title', 'Untitled')}",
            "",
            f"**Workstream:** {task.get('workstream_letter', 'X')} - {task.get('workstream_name', 'AUGMENTATION')}",
            f"**Epic:** {epic_slug}",
            f"**Source:** Augmentation of existing solution at `{solution_path}`",
            f"**Priority:** {task.get('priority', 2)}",
            "**Status:** [ ] Not Started",
            "",
            "---",
            "",
            "## Purpose",
            "",
            task.get("purpose", ""),
            "",
            "## Input",
            "",
            task.get("input", ""),
            "",
            "## Output",
            "",
            task.get("output", ""),
            "",
        ]

        existing_refs = task.get("existing_files_to_reference", [])
        if existing_refs:
            content_lines.extend(["## Existing Files to Reference", ""])
            for ref in existing_refs:
                content_lines.append(f"- `{ref}`")
            content_lines.append("")

        new_files = task.get("new_files_to_create", [])
        if new_files:
            content_lines.extend(["## New Files to Create", ""])
            for nf in new_files:
                content_lines.append(f"- `{nf}`")
            content_lines.append("")

        content_lines.extend(["## Action", "", task.get("action", ""), "", "## Verification", ""])
        for v in task.get("verification", []):
            content_lines.append(f"- [ ] {v}")

        content_lines.extend([
            "",
            "---",
            "",
            "## Notes",
            "",
            f"- Generated via epic augmentation on {datetime.datetime.now().isoformat()}",
            f"- Builds on existing solution: `{solution_path}`",
        ])

        content = "\n".join(content_lines) + "\n"

        task_slug = "_".join(task.get("title", "task").lower().split()[:5])
        task_slug = "".join(c if c.isalnum() or c == "_" else "_" for c in task_slug)
        filename = f"{timestamp_base}_{epic_slug}_augment_{task_slug}.md"

        output_dir = root / "100_backlog" / "general"
        output_dir.mkdir(parents=True, exist_ok=True)
        task_path = output_dir / filename
        task_path.write_text(content, encoding="utf-8")

        tasks_created.append({
            "task_id": task_id,
            "title": task.get("title", "Untitled"),
            "path": str(task_path),
            "filename": filename
        })

    return {
        "success": True,
        "tasks_created": tasks_created,
        "count": len(tasks_created)
    }


def create_app(workstream_root: Path = WORKSTREAM_ROOT) -> FastAPI:
    app = FastAPI(title="Epic Task Review")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.workstream_root = workstream_root
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/")
    def index() -> FileResponse:
        return FileResponse(STATIC_DIR / "index.html")

    @app.get("/api/epics")
    def api_epics(
        folder: str | None = Query(default=None),
        mode: str | None = Query(default=None),
    ) -> dict[str, Any]:
        normalized_folder = (folder or "").replace("\\", "/").lower()
        if mode == "documents" or normalized_folder.startswith("workstream/000_epic"):
            return {"epics": list_epic_documents(app.state.workstream_root, folder or "workstream/000_epic")}
        return {"epics": list_epics(app.state.workstream_root, folder)}

    @app.get("/api/browse-files")
    def api_browse_files(path: str = Query(default="")) -> dict[str, Any]:
        base_dir = app.state.workstream_root.parent
        target_dir = _resolve_repo_path(app.state.workstream_root, path) if path else base_dir
        if not target_dir.exists():
            return {"items": [], "path": path}
        items = [
            {
                "name": entry.name,
                "is_dir": entry.is_dir(),
                "path": str(entry.relative_to(base_dir)).replace("\\", "/"),
            }
            for entry in target_dir.iterdir()
        ]
        return {"items": items, "path": path}

    @app.get("/api/epics/{epic_slug}/tasks")
    def api_epic_tasks(
        epic_slug: str,
        workstream: str | None = Query(default=None),
        status: str | None = Query(default=None),
        priority: int | None = Query(default=None),
        sort_by: str = Query(default="priority"),
        folder: str | None = Query(default=None),
    ) -> dict[str, Any]:
        return {
            "tasks": get_epic_tasks(
                app.state.workstream_root,
                epic_slug=epic_slug,
                workstream=workstream,
                status=status,
                priority=priority,
                sort_by=sort_by,
                folder=folder,
            )
        }

    @app.post("/api/tasks/allocate")
    def api_allocate(payload: AllocateRequest) -> dict[str, Any]:
        return allocate_tasks(payload.task_paths, payload.target_model, app.state.workstream_root)

    @app.post("/api/tasks/move-to-general")
    def api_move_to_general(payload: MoveToGeneralRequest) -> dict[str, Any]:
        return move_tasks_to_general(payload.task_paths, app.state.workstream_root)

    @app.post("/api/tasks/reject")
    def api_reject(payload: RejectRequest) -> dict[str, Any]:
        return reject_tasks(payload.task_paths, payload.reason, app.state.workstream_root)

    @app.get("/api/models/status")
    def api_model_status() -> dict[str, Any]:
        return {"models": model_status(app.state.workstream_root)}

    @app.get("/api/health")
    def api_health() -> dict[str, str]:
        return {"status": "ok", "root": str(app.state.workstream_root)}

    @app.get("/api/epics/with-solutions")
    def api_epics_with_solutions() -> dict[str, Any]:
        return {"epics": list_epics_with_solutions(app.state.workstream_root)}

    @app.get("/api/analyze-solution")
    def api_analyze_solution(path: str = Query(default="")) -> dict[str, Any]:
        return {"analysis": analyze_solution_folder(app.state.workstream_root, path)}

    @app.post("/api/augment-epic")
    def api_augment_epic(payload: AugmentEpicRequest) -> dict[str, Any]:
        return run_augmentation(
            app.state.workstream_root,
            payload.epic_slug,
            payload.solution_path,
            payload.augment_types,
            payload.feature_description
        )

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8765)
