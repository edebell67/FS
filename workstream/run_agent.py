#!/usr/bin/env python3
import atexit
import datetime
import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path

WORKSTREAM_DIR = Path(__file__).resolve().parent
EDS_ROOT = WORKSTREAM_DIR.parent
SKILLS_DIR = EDS_ROOT / "skills"
LIFECYCLE_FILE = SKILLS_DIR / "workstream-task-lifecycle" / "SKILL.md"

TODO_ROOT = WORKSTREAM_DIR / "100_backlog"
WORKING_ROOT = WORKSTREAM_DIR / "200_inprogress"
COMPLETE_ROOT = WORKSTREAM_DIR / "300_complete"
FAILED_ROOT = WORKSTREAM_DIR / "400_failed"
LOG_ROOT = WORKSTREAM_DIR / "logs"
AGENT_LOCK = WORKSTREAM_DIR / "agent.lock"
WORKER_LOG = LOG_ROOT / "agent_worker.log"
CONTROLLER_LOG = LOG_ROOT / "agent_controller_py.log"

AGENTS = ["gemini", "codex", "claude"]
MAX_CONCURRENT_PER_DATE = 3
EXCLUDED_WORKERS_FILE = WORKSTREAM_DIR / "excluded_workers.txt"

def is_worker_excluded(agent: str) -> bool:
    """Check if worker is excluded via file-based config."""
    if not EXCLUDED_WORKERS_FILE.exists():
        return False
    try:
        excluded = EXCLUDED_WORKERS_FILE.read_text(encoding="utf-8").strip().lower().split()
        return agent.lower() in excluded
    except Exception:
        return False


def _resolve_agent_binary(agent: str) -> str:
    """Resolve the specific binary/CLI for a given agent. [2026-03-17 V20260317_1530]"""
    agent_lower = agent.lower()
    
    # Try system PATH first
    found = shutil.which(agent_lower) or shutil.which(f"{agent_lower}.cmd") or shutil.which(f"{agent_lower}.exe")
    if found:
        return found
        
    # Fallback to known npm global path
    npm_path = Path.home() / "AppData" / "Roaming" / "npm" / f"{agent_lower}.cmd"
    if npm_path.exists():
        return str(npm_path)
        
    # Final fallback to codex if everything else fails (legacy behavior)
    return shutil.which("codex") or shutil.which("codex.cmd") or str(Path.home() / "AppData" / "Roaming" / "npm" / "codex.cmd")

LOG_ROOT.mkdir(exist_ok=True)
WORKING_ROOT.mkdir(exist_ok=True)
FAILED_ROOT.mkdir(exist_ok=True)
COMPLETE_ROOT.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(message)s",
    handlers=[logging.FileHandler(CONTROLLER_LOG, encoding="utf-8"), logging.StreamHandler(sys.stdout)],
)


def write_worker_log(agent: str, message: str) -> None:
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{agent.upper()}] {message}\n"
    with open(WORKER_LOG, "a", encoding="utf-8") as fh:
        fh.write(line)


def acquire_lock() -> None:
    if AGENT_LOCK.exists():
        try:
            existing = int(AGENT_LOCK.read_text().strip())
        except ValueError:
            existing = None
        if existing:
            try:
                check = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {existing}"],
                    capture_output=True,
                    text=True,
                    timeout=3,
                )
                if "No tasks are running" in check.stdout:
                    existing = None
            except Exception:
                existing = None
        if existing:
            logging.error("Another controller instance is running (PID %s).", existing)
            sys.exit(1)
        AGENT_LOCK.unlink(missing_ok=True)
    AGENT_LOCK.write_text(str(os.getpid()))
    atexit.register(release_lock)


def release_lock() -> None:
    AGENT_LOCK.unlink(missing_ok=True)


def load_workflow() -> str:
    if not LIFECYCLE_FILE.exists():
        return ""
    return LIFECYCLE_FILE.read_text(encoding="utf-8")


def load_support_skills() -> str:
    builder = []
    for md in SKILLS_DIR.rglob("*.md"):
        try:
            relative = md.relative_to(SKILLS_DIR)
        except ValueError:
            continue
        if md == LIFECYCLE_FILE:
            continue
        try:
            content = md.read_text(encoding="utf-8")
        except OSError:
            continue
        builder.append(f"----- SKILL: {relative} -----\n{content}")
    return "\n".join(builder)


def build_agent_execution_command(agent: str, task_path: str) -> list[str] | None:
    key_specific = f"KANBAN_AGENT_EXEC_CMD_{agent.upper()}"
    tpl = os.environ.get(key_specific, "").strip() or os.environ.get("KANBAN_AGENT_EXEC_CMD", "").strip()
    if tpl:
        formatted = tpl.format(
            agent=agent,
            task_path=task_path,
            task_file=os.path.basename(task_path),
        )
        return shlex.split(formatted, posix=False)
    if not tpl:
        agent_lower = agent.lower()
        if agent_lower in {"codex", "gemini", "claude"}:
            # [2026-03-17 V20260317_1715] Use agent-specific binary and syntax
            agent_bin = _resolve_agent_binary(agent)
            prompt = (
                "Execute this task file end-to-end. "
                "Read and follow C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md first. "
                f"Task file: {task_path}. "
                "Implement required changes in the workspace, run validations, and update checklist items."
            )
            
            # Agent-specific command structures
            if agent_lower == "gemini":
                return [agent_bin, "--prompt", prompt, "--yolo"]
            elif agent_lower == "claude":
                return [agent_bin, "-p", prompt, "--permission-mode", "acceptEdits"]
            else: # codex
                return [agent_bin, "exec", "-C", str(EDS_ROOT), prompt]
        return None


@dataclass
class TaskMetadata:
    path: Path
    priority: int
    epic: str
    epic_sequence: str
    depends_on: list[str]
    readiness: str
    suggested_agent: str
    lane: str
    major_layer: int
    sequence_sort_key: str
    date_prefix: str | None
    mtime: float
    state: str


def sequence_sort_key(sequence: str) -> str:
    if not sequence:
        return "999999"
    parts = sequence.split(".")
    normalized = []
    for part in parts:
        if part.isdigit():
            normalized.append(f"{int(part):06d}")
        else:
            normalized.append("999999")
    return ".".join(normalized)


def extract_date_prefix(name: str) -> str | None:
    match = re.match(r"^(\d{8})", name)
    return match.group(1) if match else None


def parse_depends_block(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    depends = []
    idx = start_idx + 1
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            break
        if line.startswith("-"):
            line = line.lstrip("-").strip()
        if line:
            depends.append(line.strip("`\""))
        idx += 1
    return depends, idx


def parse_task_metadata(path: Path, state: str) -> TaskMetadata:
    text = path.read_text(encoding="utf-8")
    priority = 3
    match = re.search(r"(?im)^\s*Priority:\s*([1-3])\s*$", text)
    if match:
        priority = int(match.group(1))
    epic = ""
    match = re.search(r"(?im)^\*\*Epic:\*\*\s*(.+?)\s*$", text)
    if match:
        epic = match.group(1).strip()
    epic_sequence = ""
    match = re.search(r"(?im)^\*\*Epic Sequence:\*\*\s*(.+?)\s*$", text)
    if match:
        epic_sequence = match.group(1).strip()
    readiness = ""
    match = re.search(r"(?im)^\*\*Readiness:\*\*\s*(.+?)\s*$", text)
    if match:
        readiness = match.group(1).strip().lower()
    suggested_agent = ""
    match = re.search(r"(?im)^\*\*Suggested Agent:\*\*\s*(.+?)\s*$", text)
    if match:
        suggested_agent = match.group(1).strip().lower()
    depends = []
    match = re.search(
        r"(?ims)^\*\*Depends On:\*\*\s*(.+?)(?=\r?\n\*\*|\r?\n##|\r?\n---|\Z)", text
    )
    if match:
        raw = match.group(1)
        for entry in re.split(r"[,\r\n]+", raw):
            entry = entry.strip().lstrip("-").strip("`\" ")
            if entry and entry.lower() != "none":
                depends.append(entry)
    if not depends:
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line.strip().startswith("Dependency:"):
                extracted, _ = parse_depends_block(lines, idx)
                for entry in extracted:
                    if entry.lower() != "none":
                        depends.append(entry)
                break
    lane = path.parent.name.lower()
    if lane not in {"gemini", "codex", "claude", "general"}:
        lane = ""
    major_layer = 0
    if epic_sequence:
        first = epic_sequence.split(".")[0]
        if first.isdigit():
            major_layer = int(first)
    return TaskMetadata(
        path=path,
        priority=priority,
        epic=epic,
        epic_sequence=epic_sequence,
        depends_on=depends,
        readiness=readiness,
        suggested_agent=suggested_agent,
        lane=lane,
        major_layer=major_layer,
        sequence_sort_key=sequence_sort_key(epic_sequence),
        date_prefix=extract_date_prefix(path.name),
        mtime=path.stat().st_mtime,
        state=state,
    )


def is_under(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


class TaskGate:
    def __init__(self, max_concurrent_per_date: int = MAX_CONCURRENT_PER_DATE):
        self.lock = threading.RLock()
        self.max_concurrent_per_date = max_concurrent_per_date

    def _structured_tasks(self, root: Path, state: str) -> list[TaskMetadata]:
        records = []
        if not root.exists():
            return records
        for path in root.rglob("*.md"):
            if path.name.startswith("."):
                continue
            records.append(parse_task_metadata(path, state))
        return records

    def _collect_all_tasks(self) -> list[TaskMetadata]:
        return (
            self._structured_tasks(TODO_ROOT, "todo")
            + self._structured_tasks(WORKING_ROOT, "in_progress")
            + self._structured_tasks(COMPLETE_ROOT, "complete")
        )

    def _epic_group(self, epic: str, vault: list[TaskMetadata]) -> list[TaskMetadata]:
        if not epic:
            return []
        return [task for task in vault if task.epic == epic]

    def _find_dependency(self, dependency: str, epic_tasks: list[TaskMetadata]) -> TaskMetadata | None:
        if not epic_tasks:
            return None
        for task in epic_tasks:
            if task.path.name == dependency or task.path.name == Path(dependency).name:
                return task
        for task in epic_tasks:
            if task.epic_sequence == dependency:
                return task
        return None

    def _test_incomplete_layers(self, metadata: TaskMetadata, epic_tasks: list[TaskMetadata]) -> list[str]:
        reasons = []
        if metadata.major_layer > 1:
            incomplete = [
                task for task in epic_tasks
                if task.path != metadata.path
                and 0 < task.major_layer < metadata.major_layer
                and task.state != "complete"
            ]
            if incomplete:
                sequences = sorted({task.epic_sequence for task in incomplete if task.epic_sequence})
                reasons.append(f"Waiting for lower epic layers ({', '.join(sequences)})")
        return reasons

    def test_task_runnable(self, metadata: TaskMetadata, all_tasks: list[TaskMetadata]) -> tuple[bool, list[str]]:
        reasons = []
        if not metadata.epic:
            return True, reasons
        epic_tasks = self._epic_group(metadata.epic, all_tasks)
        reasons.extend(self._test_incomplete_layers(metadata, epic_tasks))
        for dependency in metadata.depends_on:
            dep_task = self._find_dependency(dependency, epic_tasks)
            if not dep_task:
                reasons.append(f"Dependency not found: {dependency}")
                continue
            if dep_task.state != "complete":
                reasons.append(f"Dependency not complete: {dependency}")
        runnable = not reasons
        return runnable, reasons

    def _sort_key(self, metadata: TaskMetadata, worker: str) -> tuple:
        preference = self._worker_preference(worker, metadata)
        major = metadata.major_layer or 999999
        return (
            preference,
            metadata.priority,
            major,
            metadata.sequence_sort_key,
            metadata.mtime,
        )

    @staticmethod
    def _worker_preference(worker: str, metadata: TaskMetadata) -> int:
        worker_norm = worker.lower()
        suggested = (metadata.suggested_agent or "").lower()
        lane = (metadata.lane or "").lower()
        if suggested == worker_norm and suggested:
            return 0
        if not suggested and lane == worker_norm:
            return 1
        if suggested in {"general", ""} or lane in {"general", ""}:
            return 2
        return 3

    def _in_progress_count_for_date(self, date_prefix: str | None, all_tasks: list[TaskMetadata]) -> int:
        if not date_prefix:
            return sum(1 for task in all_tasks if task.state == "in_progress")
        return sum(
            1
            for task in all_tasks
            if task.state == "in_progress" and task.date_prefix == date_prefix
        )

    def select_next_runnable_task(self, worker: str) -> TaskMetadata | None:
        all_tasks = self._collect_all_tasks()
        todo_tasks = [task for task in all_tasks if task.state == "todo"]
        in_progress_tasks = [task for task in all_tasks if task.state == "in_progress"]
        complete_tasks = [task for task in all_tasks if task.state == "complete"]
        logging.info(f"[DEBUG:{worker}] all_tasks={len(all_tasks)}, todo={len(todo_tasks)}, in_progress={len(in_progress_tasks)}, complete={len(complete_tasks)}")

        sorted_candidates = sorted(todo_tasks, key=lambda metadata: self._sort_key(metadata, worker))
        for candidate in sorted_candidates:
            logging.info(f"[DEBUG:{worker}] Checking candidate: {candidate.path.name} (lane={candidate.lane})")
            runnable, reasons = self.test_task_runnable(candidate, all_tasks)
            if not runnable:
                logging.info(f"[DEBUG:{worker}] Not runnable: {reasons}")
                continue
            bucket = self._in_progress_count_for_date(candidate.date_prefix, all_tasks)
            if bucket >= self.max_concurrent_per_date:
                logging.info(f"[DEBUG:{worker}] Bucket full for date {candidate.date_prefix}: {bucket} >= {self.max_concurrent_per_date}")
                continue
            logging.info(f"[DEBUG:{worker}] Selected: {candidate.path.name}")
            return candidate
        logging.info(f"[DEBUG:{worker}] No runnable task found")
        return None

    def claim_next_task(self, worker: str, target_dir: Path) -> TaskMetadata | None:
        with self.lock:
            candidate = self.select_next_runnable_task(worker)
            if not candidate:
                return None
            target_dir.mkdir(parents=True, exist_ok=True)
            dest = target_dir / candidate.path.name
            candidate.path.replace(dest)
            candidate.path = dest
            candidate.state = "in_progress"
            candidate.mtime = dest.stat().st_mtime
            return candidate


class AgentController:
    def __init__(self):
        self.task_gate = TaskGate()
        self.stop_event = threading.Event()

    def run(self) -> None:
        logging.info("AI Agent Controller Starting: %s", datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
        workflow = load_workflow()
        support_skills = load_support_skills()
        threads = []
        for agent in AGENTS:
            thread = threading.Thread(
                target=self._lane_worker,
                args=(agent, workflow, support_skills),
                daemon=True,
            )
            thread.start()
            threads.append(thread)
        try:
            while not self.stop_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop_event.set()
        for thread in threads:
            thread.join()

    def _lane_worker(self, agent: str, workflow: str, support_skills: str) -> None:
        write_worker_log(agent, "Lane daemon started...")
        working_dir = WORKING_ROOT / agent
        failed_dir = FAILED_ROOT / agent
        while not self.stop_event.is_set():
            # Check if worker is excluded
            if is_worker_excluded(agent):
                time.sleep(30)
                continue
            write_worker_log(agent, f"[DEBUG] Polling for next task...")
            candidate = self.task_gate.claim_next_task(agent, working_dir)
            if not candidate:
                write_worker_log(agent, f"[DEBUG] No candidate found, sleeping 5s")
                time.sleep(5)
                continue
            write_worker_log(agent, f"claimed {candidate.path}")
            cmd = build_agent_execution_command(agent, str(candidate.path))
            if not cmd:
                write_worker_log(agent, f"EXECUTION_CONFIG missing for {candidate.path}")
                self._revert_to_backlog(candidate.path)
                time.sleep(2)
                continue
            prompt = self._build_prompt(candidate.path, workflow, support_skills)
            result_path = Path(str(candidate.path) + ".result.md")
            try:
                process = subprocess.Popen(
                    cmd,
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                stdout, _ = process.communicate(prompt)
                result_path.write_text(stdout or "", encoding="utf-8")
                target = COMPLETE_ROOT / agent
                target.mkdir(parents=True, exist_ok=True)
                candidate.path.replace(target / candidate.path.name)
                write_worker_log(agent, f"completed {candidate.path.name}")
            except Exception as exc:
                write_worker_log(agent, f"ERROR: {exc}")
                if candidate.path.exists():
                    failed_dir.mkdir(parents=True, exist_ok=True)
                    candidate.path.replace(failed_dir / candidate.path.name)
            time.sleep(1)

    def _revert_to_backlog(self, path: Path) -> None:
        back_dir = TODO_ROOT / path.parent.name
        back_dir.mkdir(parents=True, exist_ok=True)
        path.replace(back_dir / path.name)

    @staticmethod
    def _build_prompt(task_path: Path, workflow: str, support_skills: str) -> str:
        task_text = task_path.read_text(encoding="utf-8")
        return (
            "PRIMARY WORKFLOW\n"
            "---------------------------------------\n"
            f"{workflow}\n\n"
            "SUPPORTING SKILLS\n"
            "---------------------------------------\n"
            f"{support_skills}\n\n"
            "TASK\n"
            "---------------------------------------\n"
            f"{task_text}"
        )


def main() -> None:
    acquire_lock()
    controller = AgentController()
    controller.run()


if __name__ == "__main__":
    main()
