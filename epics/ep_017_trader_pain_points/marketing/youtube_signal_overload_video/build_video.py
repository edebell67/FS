from __future__ import annotations

import math
import subprocess
from pathlib import Path
from typing import Iterable

import imageio.v2 as imageio
import imageio_ffmpeg
import numpy as np
from mutagen.mp3 import MP3
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
AUDIO = ROOT / "narration.mp3"
FRAMES_MP4 = ROOT / "signal_overload_visuals.mp4"
FINAL_MP4 = ROOT / "ep017_signal_overload_youtube_v1.mp4"
THUMBNAIL = ROOT / "thumbnail.png"
CONTACT = ROOT / "contact_sheet.png"

W, H = 1280, 720
FPS = 30
BG = (7, 12, 20)
PANEL = (14, 24, 38)
PANEL_2 = (19, 35, 54)
CYAN = (34, 211, 238)
GREEN = (34, 197, 94)
YELLOW = (250, 204, 21)
RED = (248, 113, 113)
WHITE = (238, 242, 255)
MUTED = (148, 163, 184)
PURPLE = (168, 85, 247)

SCRIPT = """Most active traders are not short of trade ideas anymore.

You have scanners, watchlists, alerts, Twitter threads, Discord calls, indicators, news feeds, and market dashboards.

The harder problem is knowing which opportunity actually deserves attention right now.

Is the signal early enough?
Is the data behind it trustworthy?
Is it stronger than the other ten setups you are watching?
Or is it just noise dressed up as an opportunity?

That is the trading pain point I am trying to validate.

Would a ranked opportunity feed be useful? Something that helps sort and prioritise possible trades.

Or do most traders prefer raw data and making the ranking decision themselves?

If you actively trade, I would like to know where the real pain is.

Finding ideas?
Trusting the data?
Acting early enough?
Or ranking too many possible setups?

Drop a comment with the one that costs you the most attention."""

SCENES = [
    (0.00, 7.0, "Most traders aren't short\nof trade ideas anymore.", "SIGNAL OVERLOAD", "hook"),
    (7.0, 18.0, "Scanners. Watchlists. Alerts.\nThreads. Discord. News. Dashboards.", "TOO MANY INPUTS", "inputs"),
    (18.0, 30.0, "The hard part is deciding\nwhat deserves attention now.", "ATTENTION IS THE BOTTLENECK", "funnel"),
    (30.0, 44.0, "Early enough?\nTrustworthy data?\nStronger than the other ten setups?", "WHAT ACTUALLY MATTERS?", "checks"),
    (44.0, 58.0, "A ranked opportunity feed\nmay be the missing layer.", "RANK, DON'T DROWN", "ranked"),
    (58.0, 72.0, "Or do traders prefer raw data\nand ranking it themselves?", "VALIDATION QUESTION", "split"),
    (72.0, 86.0, "What costs you the most attention?\nFinding ideas, trusting data, timing, or ranking?", "DROP A COMMENT", "cta"),
]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationMono-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation2/LiberationMono-Regular.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()

FONT_TITLE = font(58, True)
FONT_HEAD = font(34, True)
FONT_BODY = font(32, False)
FONT_SMALL = font(20, False)
FONT_TINY = font(16, False)


def lerp(a: float, b: float, x: float) -> float:
    return a + (b - a) * x


def ease(x: float) -> float:
    x = max(0.0, min(1.0, x))
    return 1 - pow(1 - x, 3)


def wrap_text(draw: ImageDraw.ImageDraw, text: str, fnt: ImageFont.ImageFont, max_width: int) -> list[str]:
    lines: list[str] = []
    for raw in text.split("\n"):
        words = raw.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            test = f"{line} {word}"
            if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
                line = test
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_text_block(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str, fnt: ImageFont.ImageFont, fill, max_width: int, spacing: int = 10):
    x, y = xy
    lines = wrap_text(draw, text, fnt, max_width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += draw.textbbox((0, 0), line or " ", font=fnt)[3] + spacing


def rounded(draw: ImageDraw.ImageDraw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def draw_grid(draw: ImageDraw.ImageDraw, t: float):
    for x in range(0, W, 80):
        alpha = 18 if x % 160 else 28
        col = (30, 55, 78, alpha)
        draw.line((x, 0, x, H), fill=col, width=1)
    for y in range(0, H, 80):
        draw.line((0, y, W, y), fill=(30, 55, 78, 20), width=1)


def draw_signal_chart(draw: ImageDraw.ImageDraw, box, t: float, color=CYAN, label="signal noise"):
    x1, y1, x2, y2 = box
    rounded(draw, box, 18, PANEL, (44, 72, 102), 1)
    draw.text((x1 + 18, y1 + 14), label.upper(), font=FONT_TINY, fill=MUTED)
    pts = []
    n = 90
    for i in range(n):
        x = lerp(x1 + 18, x2 - 18, i / (n - 1))
        base = math.sin(i * 0.28 + t * 2.1) * 0.35 + math.sin(i * 0.09 + t * 1.2) * 0.22
        spike = 0.65 * math.exp(-((i - (34 + 8 * math.sin(t))) / 7) ** 2)
        y = lerp(y2 - 38, y1 + 62, (base + spike + 1.2) / 2.4)
        pts.append((x, y))
    for gy in np.linspace(y1 + 60, y2 - 35, 4):
        draw.line((x1 + 18, gy, x2 - 18, gy), fill=(43, 70, 98), width=1)
    draw.line(pts, fill=color, width=4)
    peak = max(pts, key=lambda p: y2 - p[1])
    draw.ellipse((peak[0] - 7, peak[1] - 7, peak[0] + 7, peak[1] + 7), fill=YELLOW)


def draw_dashboard(draw: ImageDraw.ImageDraw, t: float, emphasis: str = ""):
    rounded(draw, (720, 92, 1208, 618), 24, PANEL, (46, 78, 110), 2)
    draw.text((748, 120), "OPPORTUNITY FEED", font=FONT_SMALL, fill=CYAN)
    rows = [
        ("GBPUSD breakout", 91, GREEN),
        ("NAS100 reversal", 84, CYAN),
        ("EURJPY momentum", 76, YELLOW),
        ("BTC noise spike", 42, RED),
    ]
    for i, (name, score, col) in enumerate(rows):
        y = 170 + i * 86
        fill = PANEL_2 if i != 0 else (18, 48, 47)
        rounded(draw, (748, y, 1180, y + 62), 14, fill, (55, 87, 120), 1)
        draw.text((766, y + 16), name, font=FONT_TINY, fill=WHITE)
        draw.text((1090, y + 14), str(score), font=FONT_SMALL, fill=col)
        bar_w = int(230 * score / 100)
        draw.rounded_rectangle((766, y + 43, 766 + bar_w, y + 50), 4, fill=col)
        draw.rounded_rectangle((766 + bar_w, y + 43, 996, y + 50), 4, fill=(42, 63, 85))
    if emphasis == "ranked":
        draw.rounded_rectangle((740, 160, 1188, 242), 18, outline=YELLOW, width=4)
        draw.text((758, 250), "prioritise what deserves attention", font=FONT_TINY, fill=YELLOW)


def draw_scene_specific(draw: ImageDraw.ImageDraw, kind: str, t: float, local: float):
    if kind == "hook":
        for i in range(18):
            x = 690 + (i % 3) * 150
            y = 135 + (i // 3) * 68
            col = [CYAN, GREEN, YELLOW, RED, PURPLE][i % 5]
            rounded(draw, (x, y, x + 122, y + 42), 12, (18, 31, 48), col, 1)
            draw.text((x + 16, y + 12), ["alert", "scan", "feed", "call", "news"][i % 5], font=FONT_TINY, fill=col)
    elif kind == "inputs":
        labels = ["scanner", "watchlist", "X thread", "Discord", "news", "indicator", "alert", "dashboard"]
        cx, cy = 950, 355
        for i, label in enumerate(labels):
            ang = i / len(labels) * math.tau + t * 0.15
            r = 145 + 18 * math.sin(t + i)
            x, y = cx + math.cos(ang) * r, cy + math.sin(ang) * r
            draw.line((x, y, cx, cy), fill=(48, 78, 108), width=2)
            rounded(draw, (x - 62, y - 22, x + 62, y + 22), 12, PANEL_2, (61, 100, 130), 1)
            draw.text((x - 48, y - 8), label, font=FONT_TINY, fill=WHITE)
        draw.ellipse((890, 295, 1010, 415), fill=(25, 45, 65), outline=YELLOW, width=3)
        draw.text((914, 342), "YOU", font=FONT_SMALL, fill=YELLOW)
    elif kind == "funnel":
        top = [(760, 140), (1160, 140), (1040, 360), (880, 360)]
        draw.polygon(top, fill=(18, 36, 58), outline=CYAN)
        draw.polygon([(880, 360), (1040, 360), (1000, 535), (920, 535)], fill=(18, 48, 47), outline=GREEN)
        draw.text((808, 190), "many possible setups", font=FONT_SMALL, fill=WHITE)
        draw.text((898, 430), "attention", font=FONT_SMALL, fill=GREEN)
        for i in range(12):
            y = 120 + ((t * 45 + i * 42) % 230)
            x = 805 + (i % 5) * 70
            draw.circle((x, y), 8, fill=[CYAN, YELLOW, RED, PURPLE][i % 4])
    elif kind == "checks":
        qs = [("EARLY?", CYAN), ("TRUSTED?", GREEN), ("STRONGER?", YELLOW), ("NOISE?", RED)]
        for i, (q, col) in enumerate(qs):
            x = 740 + (i % 2) * 225
            y = 190 + (i // 2) * 150
            rounded(draw, (x, y, x + 188, y + 94), 16, PANEL, col, 2)
            draw.text((x + 28, y + 34), q, font=FONT_SMALL, fill=col)
    elif kind == "ranked":
        draw_dashboard(draw, t, "ranked")
    elif kind == "split":
        rounded(draw, (715, 165, 955, 500), 22, (18, 48, 47), GREEN, 2)
        rounded(draw, (980, 165, 1220, 500), 22, (42, 28, 52), PURPLE, 2)
        draw.text((750, 215), "RANKED\nFEED", font=FONT_HEAD, fill=GREEN)
        draw.text((1016, 215), "RAW\nDATA", font=FONT_HEAD, fill=PURPLE)
        draw.text((742, 340), "sorted\nprioritised\nattention-first", font=FONT_SMALL, fill=WHITE)
        draw.text((1008, 340), "flexible\nunfiltered\nmanual ranking", font=FONT_SMALL, fill=WHITE)
    else:
        rounded(draw, (720, 140, 1190, 520), 26, PANEL, YELLOW, 2)
        opts = ["1. Finding ideas", "2. Trusting the data", "3. Acting early", "4. Ranking setups"]
        for i, opt in enumerate(opts):
            y = 190 + i * 72
            rounded(draw, (758, y, 1152, y + 48), 14, PANEL_2, (61, 92, 120), 1)
            draw.text((780, y + 12), opt, font=FONT_SMALL, fill=WHITE if i != 3 else YELLOW)


def current_scene(t: float):
    for start, end, body, head, kind in SCENES:
        if start <= t < end:
            return start, end, body, head, kind
    return SCENES[-1]


def frame_at(t: float) -> Image.Image:
    base = Image.new("RGBA", (W, H), BG + (255,))
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow, "RGBA")
    gd.ellipse((860 + 80 * math.sin(t * 0.2), -160, 1380, 360), fill=(34, 211, 238, 36))
    gd.ellipse((-200, 430 + 40 * math.sin(t * 0.3), 440, 900), fill=(168, 85, 247, 28))
    glow = glow.filter(ImageFilter.GaussianBlur(46))
    base.alpha_composite(glow)
    draw = ImageDraw.Draw(base, "RGBA")
    draw_grid(draw, t)

    start, end, body, head, kind = current_scene(t)
    local = (t - start) / max(0.001, end - start)
    fade = ease(min(local * 4, (1 - local) * 4, 1))

    # Left narrative panel
    rounded(draw, (58, 78, 664, 626), 28, (10, 18, 30, 230), (44, 72, 102), 2)
    draw.text((92, 112), head, font=FONT_HEAD, fill=CYAN if kind not in ["cta", "ranked"] else YELLOW)
    draw.line((92, 164, 616, 164), fill=(53, 91, 125), width=2)
    body_font = FONT_TITLE if (len(body) < 75 and body.count("\n") <= 1) else FONT_BODY
    draw_text_block(draw, (92, 214), body, body_font, WHITE, 505, 12)
    draw.text((92, 570), "EP017 trader pain-point validation", font=FONT_TINY, fill=MUTED)

    # Right visual panel
    if kind != "ranked":
        draw_signal_chart(draw, (718, 500, 1210, 638), t, CYAN, "live market signals")
    draw_scene_specific(draw, kind, t, local)

    # Progress bar
    progress = min(1, t / max(1, DURATION))
    draw.rounded_rectangle((58, 660, 1222, 668), 4, fill=(31, 48, 68))
    draw.rounded_rectangle((58, 660, 58 + int(1164 * progress), 668), 4, fill=CYAN if progress < 0.75 else YELLOW)
    return base.convert("RGB")


def save_thumbnail():
    img = frame_at(23.0)
    img.save(THUMBNAIL)


def save_contact_sheet(times: Iterable[float]):
    thumbs = [frame_at(t).resize((320, 180)) for t in times]
    sheet = Image.new("RGB", (640, 540), BG)
    for idx, im in enumerate(thumbs[:6]):
        x = (idx % 2) * 320
        y = (idx // 2) * 180
        sheet.paste(im, (x, y))
    sheet.save(CONTACT)


def render_video(duration: float):
    with imageio.get_writer(
        FRAMES_MP4,
        fps=FPS,
        codec="libx264",
        quality=8,
        macro_block_size=16,
        ffmpeg_params=["-pix_fmt", "yuv420p", "-movflags", "+faststart"],
    ) as writer:
        total = int(math.ceil(duration * FPS))
        for i in range(total):
            t = i / FPS
            writer.append_data(np.asarray(frame_at(t)))
            if i % (FPS * 10) == 0:
                print(f"rendered {i}/{total} frames")


def mux_audio():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    cmd = [
        ffmpeg,
        "-y",
        "-i", str(FRAMES_MP4),
        "-i", str(AUDIO),
        "-c:v", "copy",
        "-c:a", "aac",
        "-b:a", "160k",
        "-shortest",
        str(FINAL_MP4),
    ]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)


def probe():
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    ffprobe = str(Path(ffmpeg).with_name("ffprobe"))
    if not Path(ffprobe).exists():
        print("ffprobe not found next to ffmpeg; using ffmpeg presence as mux validation")
        return
    out = subprocess.check_output([
        ffprobe, "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height", "-of", "default=nw=1", str(FINAL_MP4)
    ], text=True)
    (ROOT / "ffprobe_output.txt").write_text(out, encoding="utf-8")
    print(out)


if __name__ == "__main__":
    audio = MP3(AUDIO)
    DURATION = float(audio.info.length) + 0.5
    print(f"audio duration: {audio.info.length:.2f}s; render duration: {DURATION:.2f}s")
    save_thumbnail()
    save_contact_sheet([3, 12, 24, 38, 51, 70])
    render_video(DURATION)
    mux_audio()
    probe()
    print(f"DONE {FINAL_MP4}")
