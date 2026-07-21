#!/usr/bin/env python3
"""Generate private EP044 mobile-mechanic previews from user-provided mobile leads."""
from __future__ import annotations

import json
from pathlib import Path

import generate_unprocessed_garage_previews as garage

BASE = Path(__file__).resolve().parent
DATA = BASE / "mobile_mechanic_candidate_data.json"


def candidates() -> list[dict]:
    result = []
    for raw in json.loads(DATA.read_text(encoding="utf-8")):
        mobile_numbers = raw["mobileNumbers"]
        result.append({
            "name": raw["name"],
            "folder": raw["folder"],
            "phone": mobile_numbers[0],
            "email": "",
            "address": raw["area"],
            "postcode": "",
            "candidate_id": "user-provided-mobile-mechanic-lead",
            "source_batches": ["user_provided_mobile_mechanic_leads"],
            "mobile_numbers": mobile_numbers,
        })
    return result


def ensure_readme(candidate: dict) -> None:
    folder = BASE / candidate["folder"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "README.md").write_text(
        "# Private preview — " + candidate["name"] + "\n\n"
        "Source: user-provided mobile-mechanic lead list.\n\n"
        "This is a non-official, noindex, demo-only preview. Website/social presence, business identity, "
        "services, contact-route accuracy and permission to contact remain to be manually verified. "
        "No form, booking, callback, payment or notification is live.\n",
        encoding="utf-8",
    )


def main() -> None:
    for candidate in candidates():
        ensure_readme(candidate)
        garage.build_preview(candidate)
    print(f"Generated {len(candidates())} private mobile-mechanic previews.")


if __name__ == "__main__":
    main()
