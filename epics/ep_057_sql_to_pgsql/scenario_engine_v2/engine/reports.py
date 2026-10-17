# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/reports.py — the hourly family report: the request the page makes and how it reads the answer (loadHourlyReport, data half).
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: load_hourly_report (request defaults, URL, error message); rendering the report stays in the page.
"""loadHourlyReport builds a request from its form controls, fetches it and then renders a table. Only the first two steps (and the error text) are data;
the table stays in the page. A request that is superseded by a newer one is dropped by the page (hourlyReportRequest); a headless caller is sequential."""
from __future__ import annotations

from . import page_utils as pu
from .data_client import FetchError, url_search_params
from .selected_time import js_or


def hourly_report_params(*, report_date, live_date, product_type_value, product_value, family, interval_value, report_interval=60) -> list:
    """The query exactly as loadHourlyReport builds it: date falls back to LIVE_DATE, product type / product to 'all', the interval to the last-used one, then 60."""
    interval = pu._number(js_or(interval_value, report_interval, 60))
    return [("date", js_or(report_date, live_date)), ("product_type", js_or(product_type_value, "all")), ("product", js_or(product_value, "all")),
            ("family", family), ("interval_minutes", pu.js_str(interval))]


def load_hourly_report(client, **kw) -> dict:
    """-> {"url": ..., "ok": True, "payload": ...} or {"url": ..., "ok": False, "error": <the message the page shows after 'Report unavailable: '>}."""
    url = f"{client.api}/api/hourly_family_report?{url_search_params(hourly_report_params(**kw))}"
    try:
        status, payload = client._get(url)
        if not (200 <= int(status) < 300):
            raise FetchError(pu.js_str(js_or(payload.get("error") if isinstance(payload, dict) else None, f"HTTP {status}")))
        return {"url": url, "ok": True, "payload": payload}
    except Exception as e:  # noqa: BLE001 - shown as 'Report unavailable'
        return {"url": url, "ok": False, "error": str(e)}
