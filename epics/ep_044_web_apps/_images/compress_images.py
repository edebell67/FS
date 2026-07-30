"""
compress_images.py — brings epics/ep_044_web_apps/_images/ under the
200KB-per-file git limit before the folder is first committed.

VERSION HISTORY
v1.0.0 · 2026-07-30 · Initial version: dedupes byte-identical PNG pairs
  (the "user-provided" vs "Gemini_Generated" copies of the same asset),
  then downscales + re-encodes any remaining file over the size limit as
  JPEG (or WebP for images with an alpha channel) at shrinking widths/
  quality until it fits. Dry-run by default; --apply writes changes.

Usage:
  python compress_images.py          # report only, no changes
  python compress_images.py --apply  # dedupe + compress in place
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

from PIL import Image

SIZE_LIMIT = 200 * 1024  # 200KB
IMAGES_DIR = Path(__file__).parent
MAX_WIDTH = 1600
MIN_WIDTH = 640


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def find_duplicates(files: list[Path]) -> list[Path]:
    """Return files that are byte-identical to an earlier file in the list (to delete)."""
    seen: dict[str, Path] = {}
    dupes: list[Path] = []
    for f in files:
        h = file_hash(f)
        if h in seen:
            dupes.append(f)
        else:
            seen[h] = f
    return dupes


def compress_to_limit(path: Path, apply: bool) -> tuple[int, int, Path]:
    """Downscale/re-encode path until under SIZE_LIMIT. Returns (before, after, final_path)."""
    before = path.stat().st_size
    img = Image.open(path)
    has_alpha = img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info)

    ext = ".webp" if has_alpha else ".jpg"
    target = path.with_suffix(ext)

    width = min(img.width, MAX_WIDTH)
    quality = 85

    while True:
        scale = width / img.width
        resized = img.resize((width, max(1, int(img.height * scale))), Image.LANCZOS)
        if has_alpha:
            resized = resized.convert("RGBA")
            save_kwargs = {"format": "WEBP", "quality": quality, "method": 6}
        else:
            resized = resized.convert("RGB")
            save_kwargs = {"format": "JPEG", "quality": quality, "optimize": True}

        if apply:
            resized.save(target, **save_kwargs)
            size = target.stat().st_size
        else:
            import io
            buf = io.BytesIO()
            resized.save(buf, **save_kwargs)
            size = buf.tell()

        if size <= SIZE_LIMIT or (width <= MIN_WIDTH and quality <= 40):
            if apply and target != path:
                path.unlink()
            return before, size, target

        if quality > 40:
            quality -= 10
        else:
            width = max(MIN_WIDTH, int(width * 0.85))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="write changes; default is dry-run")
    args = parser.parse_args()

    all_images = sorted(
        p for p in IMAGES_DIR.rglob("*")
        if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp") and p.name != Path(__file__).name
    )

    print(f"Found {len(all_images)} image files under {IMAGES_DIR}\n")

    by_dir: dict[Path, list[Path]] = {}
    for p in all_images:
        by_dir.setdefault(p.parent, []).append(p)

    to_delete: list[Path] = []
    for _, files in by_dir.items():
        to_delete.extend(find_duplicates(files))

    if to_delete:
        print(f"Duplicate (byte-identical) files: {len(to_delete)}")
        for d in to_delete:
            print(f"  {'DELETE' if args.apply else '[dry-run] would delete'}: {d.relative_to(IMAGES_DIR)}")
            if args.apply:
                d.unlink()
    else:
        print("No byte-identical duplicates found.")

    remaining = [p for p in all_images if p not in to_delete and p.exists()]
    oversized = [p for p in remaining if p.stat().st_size > SIZE_LIMIT]
    print(f"\n{len(oversized)} files over {SIZE_LIMIT // 1024}KB after dedupe.\n")

    still_over = []
    for p in oversized:
        before, after, final_path = compress_to_limit(p, args.apply)
        status = "OK" if after <= SIZE_LIMIT else "STILL OVER"
        if status == "STILL OVER":
            still_over.append(final_path)
        action = "compressed" if args.apply else "[dry-run] would compress"
        print(f"  {action}: {p.relative_to(IMAGES_DIR)} "
              f"{before/1024:.0f}KB -> {after/1024:.0f}KB ({final_path.suffix}) [{status}]")

    print(f"\n{'Applied' if args.apply else 'Dry-run complete, no files changed'}.")
    if still_over:
        print(f"WARNING: {len(still_over)} file(s) still over limit even at minimum width/quality:")
        for f in still_over:
            print(f"  {f.relative_to(IMAGES_DIR)}")


if __name__ == "__main__":
    main()
