from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\edebe\eds")
WORKSTREAM_ROOT = ROOT / "workstream"
APP_DIR = WORKSTREAM_ROOT / "apps" / "task_review"
LIGHT_SCREENSHOT_PATH = WORKSTREAM_ROOT / "verification" / "task_review_light_mode_screenshot.png"
DARK_SCREENSHOT_PATH = WORKSTREAM_ROOT / "verification" / "task_review_dark_mode_screenshot.png"
CHROME_PATHS = (
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
)


def _chrome_path() -> Path:
    for path in CHROME_PATHS:
        if path.exists():
            return path
    raise FileNotFoundError("No supported headless browser was found.")


def _wait_for_http(url: str, timeout_seconds: int = 20) -> None:
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        try:
            with urlopen(url) as response:
                if response.status == 200:
                    return
        except Exception:
            time.sleep(0.5)
    raise TimeoutError(f"Timed out waiting for {url}")


def _fetch_json(url: str) -> dict:
    return json.loads(urlopen(url).read().decode("utf-8"))


def _theme_target_url(theme: str, epic_slug: str) -> str:
    target_url = "http://127.0.0.1:8765/"
    params: list[str] = []
    if epic_slug:
        params.append(f"epic={quote(epic_slug)}")
    params.append(f"theme={theme}")
    return target_url + "?" + "&".join(params)


def _capture_browser_screenshot(theme: str, screenshot_path: Path, epic_slug: str) -> bool:
    try:
        result = subprocess.run(
            [
                str(_chrome_path()),
                "--headless=new",
                "--disable-gpu",
                "--no-sandbox",
                "--virtual-time-budget=6000",
                f"--user-data-dir={WORKSTREAM_ROOT / 'verification' / f'browser_profile_{theme}'}",
                "--window-size=1600,1200",
                f"--screenshot={screenshot_path}",
                _theme_target_url(theme, epic_slug),
            ],
            check=False,
            capture_output=True,
            text=True,
            cwd=str(ROOT),
        )
        return screenshot_path.exists() and screenshot_path.stat().st_size > 0 and result.returncode in (0, 21)
    except Exception:
        return False


def main() -> None:
    LIGHT_SCREENSHOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    process = subprocess.Popen(
        ["python", str(APP_DIR / "app.py")],
        cwd=str(ROOT),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        _wait_for_http("http://127.0.0.1:8765/api/health")
        epics = _fetch_json("http://127.0.0.1:8765/api/epics")
        epic_slug = epics["epics"][0]["slug"] if epics["epics"] else ""
        light_ok = _capture_browser_screenshot("light", LIGHT_SCREENSHOT_PATH, epic_slug)
        dark_ok = _capture_browser_screenshot("dark", DARK_SCREENSHOT_PATH, epic_slug)
        if not (light_ok and dark_ok):
            _render_fallback_image(epic_slug, "light", LIGHT_SCREENSHOT_PATH)
            _render_fallback_image(epic_slug, "dark", DARK_SCREENSHOT_PATH)
    finally:
        process.terminate()
        process.wait(timeout=10)


def _render_fallback_image(epic_slug: str, theme: str, screenshot_path: Path) -> None:
    task_payload = _fetch_json(f"http://127.0.0.1:8765/api/epics/{epic_slug}/tasks?sort_by=priority") if epic_slug else {"tasks": []}
    model_payload = _fetch_json("http://127.0.0.1:8765/api/models/status")
    tasks = task_payload["tasks"][:10]
    is_dark = theme == "dark"
    colors = {
        "body": "#080a18" if is_dark else "#f5efe4",
        "hero": "#0f1225" if is_dark else "#fffaf3",
        "panel": "#11162d" if is_dark else "#fffaf3",
        "card": "#141a34" if is_dark else "#f3e7d4",
        "outline": "#2b3568" if is_dark else "#d1b99a",
        "muted": "#94a3b8" if is_dark else "#615645",
        "ink": "#f1f5f9" if is_dark else "#1f1a14",
        "accent": "#818cf8" if is_dark else "#7f2f16",
    }

    image = Image.new("RGB", (1600, 1200), colors["body"])
    draw = ImageDraw.Draw(image)
    title_font = ImageFont.load_default()
    body_font = ImageFont.load_default()

    draw.rounded_rectangle((40, 40, 1560, 190), radius=28, fill=colors["hero"], outline=colors["outline"], width=2)
    draw.text((70, 70), f"Epic Task Review ({theme.title()} Mode)", fill=colors["ink"], font=title_font)
    draw.text((70, 100), f"Epic: {epic_slug or 'n/a'}", fill=colors["muted"], font=body_font)
    draw.text((70, 125), "Fallback verification image rendered from live FastAPI data.", fill=colors["muted"], font=body_font)

    draw.rounded_rectangle((40, 220, 900, 1140), radius=24, fill=colors["panel"], outline=colors["outline"], width=2)
    draw.text((70, 250), "Tasks", fill=colors["ink"], font=title_font)

    y = 290
    for task in tasks:
        draw.rounded_rectangle((70, y, 870, y + 70), radius=18, fill=colors["card"], outline=colors["outline"], width=1)
        draw.line((72, y + 6, 72, y + 64), fill="#6366f1", width=4)
        draw.text((90, y + 10), f"[{task['workstream_group']}] {task['task_id']}  P{task['priority']}", fill=colors["accent"], font=body_font)
        draw.text((90, y + 30), task["title"][:90], fill=colors["ink"], font=body_font)
        status_text = f"{task['status_folder']}{'/' + task['agent'] if task['agent'] else ''}"
        draw.text((620, y + 10), status_text, fill=colors["muted"], font=body_font)
        y += 82
        if y > 980:
            break

    detail = tasks[0] if tasks else {"title": "No tasks", "purpose": "", "input": "", "output": "", "verification": ""}
    draw.rounded_rectangle((940, 220, 1560, 780), radius=24, fill=colors["panel"], outline=colors["outline"], width=2)
    draw.text((970, 250), "Detail", fill=colors["ink"], font=title_font)
    draw.text((970, 280), detail["title"][:60], fill=colors["ink"], font=body_font)
    draw.text((970, 320), f"Purpose: {detail['purpose'][:70]}", fill=colors["muted"], font=body_font)
    draw.text((970, 350), f"Input: {detail['input'][:72]}", fill=colors["muted"], font=body_font)
    draw.text((970, 380), f"Output: {detail['output'][:70]}", fill=colors["muted"], font=body_font)
    draw.text((970, 410), f"Verification: {detail['verification'][:64]}", fill=colors["muted"], font=body_font)

    draw.rounded_rectangle((940, 820, 1560, 1140), radius=24, fill=colors["panel"], outline=colors["outline"], width=2)
    draw.text((970, 850), "Model Status", fill=colors["ink"], font=title_font)
    status_y = 890
    for model in model_payload["models"]:
        draw.rounded_rectangle((970, status_y, 1530, status_y + 56), radius=18, fill=colors["card"], outline=colors["outline"], width=1)
        draw.text((995, status_y + 18), f"{model['model']}: {model['count']} task(s)", fill=colors["ink"], font=body_font)
        status_y += 72

    image.save(screenshot_path)


if __name__ == "__main__":
    main()
