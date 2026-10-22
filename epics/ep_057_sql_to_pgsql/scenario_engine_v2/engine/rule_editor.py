# epics/ep_057_sql_to_pgsql/scenario_engine_v2/engine/rule_editor.py — the overlay-rule editor: form -> rule config, begin / cancel edit, save a named rule, assign a rule to a portfolio.
#
# VERSION HISTORY
# v1.0.0 · 2026-10-17 · Initial version: config_from_overlay_editor, begin_edit_named_overlay_rule, cancel_edit_named_overlay_rule, save_named_overlay_rule, assign_overlay_rule; differential-tested against the page's own functions.
"""The page's editor reads and writes DOM controls; here the controls are one `RuleForm` object (plain data), so a headless race can build a rule
without a browser. Writes (POST / PUT of rules and assignments) go through `DataClient.send`, which refuses unless a write transport is supplied."""
from __future__ import annotations

from dataclasses import dataclass, field

from . import page_utils as pu
from .data_client import _is_ok
from .selected_time import js_or, js_truthy

RANKED_TYPES = ("ranked", "group_ranked", "ranked_top", "ranked_bottom", "group_ranked_top", "group_ranked_bottom")
GROUP_TYPES = ("group_ranked", "group_ranked_top", "group_ranked_bottom")
LDQ, RDQ = "“", "”"


@dataclass
class RuleForm:
    interval: object = ""
    metric: object = ""
    group: object = ""
    trade_side: object = ""
    hold_rank: object = ""
    exit_threshold: object = ""
    rule_checks: list = field(default_factory=list)         # [{"value": type, "checked": bool}] in page order
    eligibility_checks: list = field(default_factory=list)
    save_text: str = "Name and save rule"
    cancel_hidden: bool = True
    status: str = ""
    name_input: str = ""
    modal_status: str = ""
    save_disabled: bool = False
    panel_open: bool = False
    editor_open: bool = False
    selector: dict | None = None                            # the portfolio list's rule <select> for the portfolio being assigned

    def snapshot(self) -> dict:
        return {k: getattr(self, k) for k in self.__dataclass_fields__}


_UNDEF = object()


def tpl(value) -> str:
    """A value inside a JavaScript template literal: null -> 'null', a missing property -> 'undefined'."""
    if value is _UNDEF:
        return "undefined"
    return "null" if value is None else pu.js_str(value)


def _has_property(obj, key) -> bool:
    return isinstance(obj, dict) and key in obj


def _find_rule(library, rule_id):
    for rule in library.get("rules") or []:
        if _has_property(rule, "id") and rule["id"] == rule_id:   # `rule.id === ruleId`
            return rule
    return None


class RuleEditor:
    def __init__(self, page, form: RuleForm | None = None):
        self.page, self.form = page, form or RuleForm()

    # ---- configFromOverlayEditor ----
    def config_from_overlay_editor(self) -> dict:
        f = self.form
        interval = pu._number(f.interval)
        metric = f.metric
        group = str(f.group).strip()
        rules = []
        for check in f.rule_checks:
            if not check["checked"]:
                continue
            typ = check["value"]
            grouped = typ in ("group_ranked_top", "group_ranked_bottom")
            ranked = typ in ("ranked_top", "ranked_bottom") or grouped
            rules.append({"type": typ, "metric": metric if ranked else ("loss_rate" if typ == "higher_loss_rate" else "cum_net"),
                          "group": group if grouped else ""})
        hold = pu._number(f.hold_rank if js_truthy(f.hold_rank) else 1)
        exit_t = pu._number(f.exit_threshold if js_truthy(f.exit_threshold) else 0)
        return {"interval_minutes": interval, "rules": rules,
                "eligibility_filters": [c["value"] for c in f.eligibility_checks if c["checked"]],
                "trade_side": f.trade_side, "hold_rank": hold, "exit_threshold": exit_t}

    # ---- beginEditNamedOverlayRule / cancelEditNamedOverlayRule ----
    def begin_edit_named_overlay_rule(self, rule_id) -> None:
        s, f = self.page.s, self.form
        selected = _find_rule(self.page.client.overlay_rule_library, rule_id)
        if selected is None:
            return
        config = selected.get("config")
        config = config if js_truthy(config) else {}
        rules = config.get("rules")
        rules = rules if js_truthy(rules) else []
        s.editing_rule_id = selected.get("id")
        s.pending_rule_config = None
        f.interval = js_or(config.get("interval_minutes"), 30)
        rank_rule = next((r for r in rules if r.get("type") in RANKED_TYPES), None)
        f.metric = js_or((rank_rule or {}).get("metric"), "cum_net")
        group_rule = next((r for r in rules if r.get("type") in GROUP_TYPES), None)
        f.group = js_or((group_rule or {}).get("group"), "")
        f.trade_side = js_or(config.get("trade_side"), "both")
        for check in f.rule_checks:
            check["checked"] = any(r.get("type") == check["value"] for r in rules)
        filters = config.get("eligibility_filters")
        filters = filters if js_truthy(filters) else []
        for check in f.eligibility_checks:
            check["checked"] = check["value"] in filters
        f.hold_rank = pu.js_str(js_or(config.get("hold_rank"), 1))
        exit_t = config.get("exit_threshold")
        f.exit_threshold = pu.js_str(0 if exit_t is None else exit_t)
        name = tpl(selected.get("name") if "name" in selected else _UNDEF)
        f.save_text = f"Update {LDQ}{name}{RDQ}"
        f.cancel_hidden = False
        f.status = f"Editing {LDQ}{name}{RDQ}. Change its criteria above, then save changes."
        self.page.fx("overlayRuleLibraryModal.close")
        f.panel_open = True
        f.editor_open = True
        self.page.fx("scrollIntoView")

    def cancel_edit_named_overlay_rule(self) -> None:
        s, f = self.page.s, self.form
        s.editing_rule_id = None
        s.pending_rule_config = None
        f.save_text = "Name and save rule"
        f.cancel_hidden = True
        f.status = "Rule edit cancelled."

    # ---- saveNamedOverlayRule ----
    def save_named_overlay_rule(self) -> None:
        page, s, f, client = self.page, self.page.s, self.form, self.page.client
        name = str(f.name_input).strip()
        if not name:
            f.modal_status = "Enter a name for this rule."
            return
        pending = s.pending_rule_config
        if not js_truthy(pending):
            f.modal_status = "Choose the overlay criteria first."
            return
        if not pending["rules"]:
            f.modal_status = "Select at least one top-side or bottom-side criterion in the portfolio rules editor."
            return
        if any(r["type"] in ("group_ranked_top", "group_ranked_bottom") for r in pending["rules"]) and not any(js_truthy(r.get("group")) for r in pending["rules"]):
            f.modal_status = "Enter a group key in the rules editor, for example family:breakout."
            return
        f.save_disabled = True
        try:
            editing = _find_rule(client.overlay_rule_library, s.editing_rule_id)
            method = "PUT" if editing else "POST"
            url = (f"{client.api}/api/overlay_rules/{pu_encode(editing['id'])}" if editing else f"{client.api}/api/overlay_rules")
            status, result = client.send(method, url, {"name": name, "config": pending})
            if not _is_ok(status):
                raise RuntimeError(pu.js_str(js_or(result.get("detail"), f"HTTP {status}")))
            s.pending_rule_config = None
            s.editing_rule_id = None
            page.fx("overlayRuleNameModal.close")
            page._await(client.begin_load_overlay_rule_library())
            page.fx("renderPortfolioList")
            f.save_text = "Name and save rule"
            f.cancel_hidden = True
            rule = result.get("rule") if isinstance(result, dict) else None
            if not isinstance(rule, dict):
                raise RuntimeError(f"Cannot read properties of {'null' if _has_property(result, 'rule') and rule is None else 'undefined'} (reading 'name')")
            rname = tpl(rule.get("name") if "name" in rule else _UNDEF)
            f.status = (f"Updated {LDQ}{rname}{RDQ} in PostgreSQL. Existing portfolio assignments are unchanged." if editing
                        else f"Saved {LDQ}{rname}{RDQ} with the selected criteria. Assign it to any portfolio below.")
            assignments = client.overlay_rule_library.get("assignments") or {}
            values = list(assignments.values()) if isinstance(assignments, dict) else list(assignments)
            if (rule.get("id") in values and s.active_portfolio
                    and isinstance(assignments, dict) and assignments.get(s.active_portfolio) == rule.get("id")):
                page.fx("drawChart")
        except Exception as error:  # noqa: BLE001 - shown in the dialog
            f.modal_status = f"Could not save rule: {error}"
        finally:
            f.save_disabled = False

    # ---- assignOverlayRule ----
    def assign_overlay_rule(self, portfolio, rule_id) -> None:
        page, s, f, client = self.page, self.page.s, self.form, self.page.client
        if f.selector is not None:
            f.selector["disabled"] = True
        try:
            status, result = client.send("PUT", f"{client.api}/api/overlay_rules/assignments/{pu_encode(portfolio)}",
                                         {"rule_id": rule_id if js_truthy(rule_id) else None})
            if not _is_ok(status):
                raise RuntimeError(pu.js_str(js_or(result.get("detail"), f"HTTP {status}")))
            page._await(client.begin_load_overlay_rule_library())
            page.fx("renderPortfolioList")
            if s.active_portfolio == portfolio:
                s.use_assigned_rule = js_truthy(rule_id)
                page.fx("syncAssignedOverlayRuleUI")
                page.persist_portfolio_view_config(portfolio)
            if s.active_portfolio == portfolio:
                page.fx("drawChart")
            if js_truthy(rule_id):
                found = _find_rule(client.overlay_rule_library, rule_id)
                f.status = f"Assigned {tpl(js_or((found or {}).get('name'), 'saved rule'))} to {tpl(portfolio)}."
            else:
                f.status = f"Removed the saved overlay rule from {tpl(portfolio)}."
        except Exception as error:  # noqa: BLE001
            if f.selector is not None:
                f.selector["disabled"] = False
                assignments = client.overlay_rule_library.get("assignments")
                f.selector["value"] = js_or(assignments.get(portfolio) if isinstance(assignments, dict) else None, "")
            f.status = f"Could not assign rule: {error}"


def pu_encode(value) -> str:
    from .data_client import encode_uri_component
    return encode_uri_component(pu.js_str(value))
