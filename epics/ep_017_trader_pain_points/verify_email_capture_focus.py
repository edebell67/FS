from pathlib import Path

BASE = Path(__file__).resolve().parent
PAGES = [
    BASE / "page_1_strongest_models" / "index.html",
    BASE / "page_2_early_momentum" / "index.html",
    BASE / "page_3_verifiable_data" / "index.html",
    BASE / "page_4_ranked_opportunity" / "index.html",
]

FORBIDDEN_SNIPPETS = [
    'href="#pricing"',
    'id="pricing"',
    'https://piphunter.io/login',
    'https://piphunter.io/strategies',
    'class="login-btn"',
]


def main() -> int:
    failures = []
    for page in PAGES:
        html = page.read_text(encoding="utf-8")
        for snippet in FORBIDDEN_SNIPPETS:
            if snippet in html:
                failures.append(f"{page.relative_to(BASE)} contains forbidden snippet: {snippet}")
        if 'id="lead-form"' not in html:
            failures.append(f"{page.relative_to(BASE)} is missing lead form")
        if 'type="email"' not in html:
            failures.append(f"{page.relative_to(BASE)} is missing email input")
        if 'type="submit"' not in html:
            failures.append(f"{page.relative_to(BASE)} is missing submit button")

    if failures:
        print("EMAIL CAPTURE FOCUS CHECK FAILED")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("EMAIL CAPTURE FOCUS CHECK PASSED")
    print(f"Checked {len(PAGES)} pages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
