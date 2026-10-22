# epics/ep_057_sql_to_pgsql/cross_signal_prototype/build_cross_page.py — builds cross_signal.html from cross_signal.template.html
#
# VERSION HISTORY
# v1.2.0 · 2026-10-01 · Page now loads data from the server API; the build no longer embeds data or touches the database.
# v1.1.0 · 2026-10-01 · Adds a build stamp so a stale cached page is recognisable.
# v1.0.0 · 2026-09-30 · Initial version: embeds combined_trades_closed history (or a capture day) into the page template.
"""Build cross_signal.html from the template. The page loads quote data for the chosen day from serve_nocache.py (/api/*)."""
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    product = sys.argv[1] if len(sys.argv) > 1 else "gbp"
    tpl = (HERE / "cross_signal.template.html").read_text(encoding="utf-8")
    html = (tpl.replace("__BUILD__", datetime.now().strftime("%d %b %H:%M")).replace("__PRODUCT__", product)
            .replace("__DATA__", "[]").replace("__LIVE__", "true"))
    (HERE / "cross_signal.html").write_text(html, encoding="utf-8")
    print(f"{product}: cross_signal.html built")


if __name__ == "__main__":
    main()
