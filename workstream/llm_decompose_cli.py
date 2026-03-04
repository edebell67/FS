import argparse
import json
import re
from pathlib import Path


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def _extract_title(md: str, fallback_name: str) -> str:
    m = re.search(r"^\s*#\s+(.+)$", md, flags=re.MULTILINE)
    if m:
        return _clean(m.group(1))
    return fallback_name.replace("_", " ").strip() or "Backlog Task"


def _extract_summary(md: str) -> str:
    for label in ["Task Summary", "Mission", "Objective", "Summary"]:
        m = re.search(rf"^\s*[-*]?\s*`?{re.escape(label)}`?\s*:\s*(.+)$", md, flags=re.IGNORECASE | re.MULTILINE)
        if m:
            return _clean(m.group(1))
    # fallback: first non-empty paragraph after first heading
    body = re.split(r"^\s*#\s+.+$", md, maxsplit=1, flags=re.MULTILINE)
    if len(body) > 1:
        paras = [p.strip() for p in body[1].split("\n\n") if p.strip()]
        if paras:
            return _clean(paras[0][:500])
    return "Decompose and implement the backlog objective."


def _extract_checklist_lines(md: str) -> list[str]:
    lines = []
    for line in md.splitlines():
        m = re.match(r"^\s*[-*]\s+\[\s*[ xX]?\s*\]\s+(.+)$", line)
        if m:
            lines.append(_clean(m.group(1)))
    return [l for l in lines if l]


def _extract_bullet_lines(md: str) -> list[str]:
    lines = []
    for line in md.splitlines():
        m = re.match(r"^\s*[-*]\s+(.+)$", line)
        if m and not m.group(1).startswith("["):
            txt = _clean(m.group(1))
            if txt and len(txt) > 8:
                lines.append(txt)
    return lines


def _make_tasks(agent: str, backlog_path: str, md: str) -> list[dict]:
    fallback_name = Path(backlog_path).stem
    title = _extract_title(md, fallback_name)
    summary = _extract_summary(md)
    checklist = _extract_checklist_lines(md)
    bullets = _extract_bullet_lines(md)

    analysis_steps = checklist[:5] if checklist else bullets[:5]
    if not analysis_steps:
        analysis_steps = [
            "Read backlog and identify required deliverables",
            "Break scope into independently testable tasks",
            "Define validation checks for each task",
        ]

    tests = [
        "Each generated task includes a concrete implementation plan",
        "Each generated task includes at least one validation step",
    ]

    task1 = {
        "title": f"Decompose: {title}",
        "summary": f"Agent {agent} should decompose the backlog into actionable implementation tasks. Source summary: {summary}",
        "steps": analysis_steps,
        "tests": tests,
        "priority": 2,
        "source_backlog": backlog_path,
    }

    task2_steps = checklist[5:10] if len(checklist) > 5 else [
        "Implement highest-priority decomposition items first",
        "Add traceability links from generated tasks to parent backlog",
        "Prepare review-ready drafts in 050_review",
    ]
    task2 = {
        "title": f"Implement & validate: {title}",
        "summary": "Execute decomposed work items and confirm validations before approval.",
        "steps": task2_steps,
        "tests": [
            "Generated files in 050_review are non-placeholder and source-linked",
            "Backlog review file contains generated task references",
        ],
        "priority": 2,
        "source_backlog": backlog_path,
    }
    return [task1, task2]


def main() -> None:
    parser = argparse.ArgumentParser(description="Default decomposition CLI for kanban worker")
    parser.add_argument("--agent", required=True)
    parser.add_argument("--input", required=True, help="Path to backlog markdown file")
    args = parser.parse_args()

    in_path = Path(args.input)
    if not in_path.exists():
        raise SystemExit(json.dumps({"error": f"input_not_found: {in_path}"}))

    md = in_path.read_text(encoding="utf-8", errors="ignore")
    tasks = _make_tasks(args.agent, str(in_path), md)
    print(json.dumps({"tasks": tasks}, ensure_ascii=False))


if __name__ == "__main__":
    main()
