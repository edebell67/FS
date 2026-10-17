/* epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/static/launch_panel.js — "Virtual race" panel for the engine-client copy of the scenario page.
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-10-17 · Initial version: floating button + panel; builds a race request from the page's current view (start strategy, competitors, top-N scenario leaders, date, return type,
 *                       split mode, thresholds, assigned rule), POSTs it to the runner, follows the race, links to the dashboard; live portfolios are refused.
 *
 * Injected after the page's main script by tools/build_thin_page.py, so the page's top-level variables (currentDate, splitMode, ...) are visible here by name. Races are virtual: the runner
 * replays recorded curves; nothing here can place an order or change shared data. */
(function () {
  'use strict';
  var BASE = (window.__engine && window.__engine.base) || location.origin;
  var LIVE = ['LIVE', 'LIVE_ALT'];

  function val(fn, fallback) { try { var v = fn(); return v === undefined ? fallback : v; } catch (e) { return fallback; } }
  function el(tag, props, children) {
    var e = document.createElement(tag);
    Object.keys(props || {}).forEach(function (k) { if (k === 'style') e.style.cssText = props[k]; else if (k === 'text') e.textContent = props[k]; else e[k] = props[k]; });
    (children || []).forEach(function (c) { e.appendChild(c); });
    return e;
  }

  /* the request the panel would send for the page's current view (pure: also used by the tests) */
  function currentView() {
    var models = val(function () { return getEligibleModels(); }, []);
    var visible = val(function () { return visibleModels; }, new Set());
    var ids = models.map(function (m) { return m.model; });
    var shown = ids.filter(function (id) { return !visible.size || visible.has(id); });
    var idx = val(function () { return selectedModelIndex; }, 0);
    var selected = (models[idx] && shown.indexOf(models[idx].model) >= 0) ? models[idx].model : (shown[0] || null);
    var rule = val(function () { return activePortfolioName ? activePortfolioOverlayRule() : null; }, null);
    var date = val(function () { return currentDate; }, '');
    if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) date = val(function () { return LIVE_DATE; }, '') || '';
    return {
      ids: ids, shown: shown, selected: selected, date: date, scenario: val(function () { return currentCriteria; }, 'top_net'),
      returnType: val(function () { return currentReturnType; }, 'NET'), splitMode: val(function () { return splitMode; }, 'ALL_NET'),
      exitThreshold: Number(val(function () { return exitThreshold; }, 0)) || 0, holdRank: Math.max(1, Math.min(5, Number(val(function () { return overlayTopX; }, 1)) || 1)),
      dailyTarget: Number(val(function () { return dailyTarget; }, 500)) || 0, baseline: Math.max(0, Number(val(function () { return baselineFrameIndex; }, 0)) || 0),
      productType: val(function () { return currentProductType; }, 'all'), product: val(function () { return currentProduct; }, 'all'),
      family: val(function () { return currentStrategyFamily; }, 'all'), limit: Math.max(1, Math.min(50, Number(val(function () { return modelLimit; }, 10)) || 10)),
      portfolio: val(function () { return activePortfolioName; }, null), ruleId: rule ? rule.id : null, ruleName: rule ? rule.name : null
    };
  }

  function buildRequest(view, form) {
    var start = form.start || null;
    var add = (form.competitors || []).filter(function (id) { return id && id !== start; });
    var req = {
      name: (start || form.scenario) + ' race', start_model: start, add_models: add.slice(0, 19), add_scenario_top: Math.max(0, Math.min(19, form.addTop || 0)),
      scenario: form.scenario || view.scenario, date: form.date || view.date, product_type: view.productType, product: view.product, strategy_family: view.family,
      return_type: form.returnType || view.returnType, limit: view.limit, split_mode: view.splitMode, baseline_index: view.baseline, exit_threshold: view.exitThreshold,
      daily_target: view.dailyTarget, hold_rank: view.holdRank
    };
    if (form.useRule && view.ruleId) req.overlay_rule_id = view.ruleId;
    return req;
  }

  var panel = null, button = null;

  function css() {
    if (document.getElementById('vr-style')) return;
    var s = el('style', { id: 'vr-style' });
    s.textContent = '#vr-btn{position:fixed;right:14px;bottom:14px;z-index:9998;min-height:44px;padding:0 16px;border-radius:99px;border:1px solid #0e7490;background:#0891b2;color:#04202e;font:600 13px system-ui,sans-serif;cursor:pointer;box-shadow:0 4px 14px rgba(0,0,0,.4)}'
      + '#vr-panel{position:fixed;right:14px;bottom:70px;z-index:9999;width:min(92vw,420px);max-height:78vh;overflow:auto;background:#0f172a;color:#e2e8f0;border:1px solid #334155;border-radius:14px;padding:14px;font:13px/1.4 system-ui,sans-serif;box-shadow:0 10px 30px rgba(0,0,0,.5)}'
      + '#vr-panel h2{margin:0 0 8px;font-size:15px}#vr-panel label{display:block;margin:8px 0 2px;color:#94a3b8;font-size:11px;text-transform:uppercase;letter-spacing:.04em}'
      + '#vr-panel select,#vr-panel input[type=number],#vr-panel input[type=date]{width:100%;min-height:36px;background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:8px;padding:6px 8px}'
      + '#vr-panel .vr-chk{display:flex;align-items:center;gap:8px;margin:2px 0;color:#e2e8f0;font-size:12px;text-transform:none;letter-spacing:0}'
      + '#vr-panel .vr-row{display:flex;gap:8px}#vr-panel .vr-row>div{flex:1}'
      + '#vr-panel button{min-height:38px;border-radius:8px;border:1px solid #334155;background:#1e293b;color:#e2e8f0;padding:0 14px;cursor:pointer;font:600 13px system-ui,sans-serif}'
      + '#vr-panel button.vr-go{background:#0891b2;border-color:#0891b2;color:#04202e}#vr-panel button:disabled{opacity:.5;cursor:default}'
      + '#vr-status{margin-top:10px;font-size:12px;color:#cbd5e1;word-break:break-word}#vr-status a{color:#38bdf8}#vr-status .vr-bad{color:#f87171}';
    document.head.appendChild(s);
  }

  function openPanel() {
    css();
    if (panel) { panel.remove(); panel = null; return; }
    var view = currentView();
    var live = view.portfolio && LIVE.indexOf(String(view.portfolio).toUpperCase()) >= 0;
    panel = el('div', { id: 'vr-panel', role: 'dialog', ariaLabel: 'Launch a virtual race' });
    panel.appendChild(el('h2', { text: 'Virtual race' }));
    panel.appendChild(el('div', { style: 'color:#94a3b8;font-size:12px', text: 'Replays recorded curves on the engine. No orders, no shared data changes.' }));
    if (live) { panel.appendChild(el('div', { className: 'vr-bad', style: 'margin-top:10px', text: 'Live portfolios cannot be raced. Switch to an ordinary portfolio or scenario.' })); document.body.appendChild(panel); return; }
    var start = el('select', { id: 'vr-start' });
    view.ids.forEach(function (id) { var o = el('option', { value: id, text: id }); if (id === view.selected) o.selected = true; start.appendChild(o); });
    var comp = el('div', { id: 'vr-comp' });
    function renderComp() {
      comp.replaceChildren();
      view.ids.filter(function (id) { return id !== start.value; }).forEach(function (id) {
        var cb = el('input', { type: 'checkbox', value: id, checked: view.shown.indexOf(id) >= 0 });
        comp.appendChild(el('label', { className: 'vr-chk' }, [cb, el('span', { text: id })]));
      });
    }
    start.onchange = renderComp; renderComp();
    var addTop = el('input', { id: 'vr-addtop', type: 'number', min: 0, max: 19, value: 0 });
    var date = el('input', { id: 'vr-date', type: 'date', value: view.date });
    var ret = el('select', { id: 'vr-ret' }, ['NET', 'ALT'].map(function (t) { var o = el('option', { value: t, text: t }); if (t === view.returnType) o.selected = true; return o; }));
    var rule = el('input', { id: 'vr-rule', type: 'checkbox', checked: !!view.ruleId });
    var go = el('button', { className: 'vr-go', type: 'button', text: 'Launch race' });
    var status = el('div', { id: 'vr-status', role: 'status' });
    panel.appendChild(el('label', { text: 'Start strategy' })); panel.appendChild(start);
    panel.appendChild(el('label', { text: 'Competitors' })); panel.appendChild(comp);
    panel.appendChild(el('div', { className: 'vr-row' }, [el('div', {}, [el('label', { text: 'Add top N of ' + view.scenario }), addTop]), el('div', {}, [el('label', { text: 'Return' }), ret])]));
    panel.appendChild(el('label', { text: 'Date' })); panel.appendChild(date);
    if (view.ruleId) panel.appendChild(el('label', { className: 'vr-chk' }, [rule, el('span', { text: 'Use assigned rule: ' + (view.ruleName || view.ruleId) })]));
    panel.appendChild(el('div', { style: 'margin-top:12px' }, [go]));
    panel.appendChild(status);
    go.onclick = function () {
      var form = { start: start.value || null, competitors: [].slice.call(comp.querySelectorAll('input:checked')).map(function (c) { return c.value; }), addTop: parseInt(addTop.value, 10) || 0,
        date: date.value, returnType: ret.value, scenario: view.scenario, useRule: rule.checked };
      var req = buildRequest(view, form);
      go.disabled = true; status.textContent = 'Launching…';
      fetch(BASE + '/api/races', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(req) })
        .then(function (r) { return r.json().then(function (j) { if (!r.ok) throw new Error(j.detail || ('HTTP ' + r.status)); return j; }); })
        .then(function (race) { follow(race, status); })
        .catch(function (e) { status.replaceChildren(el('span', { className: 'vr-bad', text: 'Could not launch: ' + e.message })); })
        .then(function () { go.disabled = false; });
    };
    document.body.appendChild(panel);
  }

  function follow(race, status) {
    var link = el('a', { href: BASE + '/dashboard', target: '_blank', rel: 'noopener', text: 'Open dashboard' });
    var tries = 0;
    (function tick() {
      fetch(BASE + '/api/races/' + race.race_id).then(function (r) { return r.json(); }).then(function (s) {
        status.replaceChildren(document.createTextNode(s.name + ' — ' + s.state + (s.state === 'running' ? ' ' + s.pct + '%' : '') + (s.leader ? ' · leader ' + s.leader : '') + (s.error ? ' · ' + s.error : '') + ' · '), link);
        if ((s.state === 'queued' || s.state === 'running') && ++tries < 120) setTimeout(tick, 1000);
      }).catch(function () { status.textContent = 'Lost contact with the race runner.'; });
    })();
  }

  function init() {
    css();
    if (button) return;
    button = el('button', { id: 'vr-btn', type: 'button', text: '▶ Virtual race', title: 'Launch a headless virtual race from this view' });
    button.onclick = openPanel;
    document.body.appendChild(button);
  }

  window.__virtualRace = { openPanel: openPanel, currentView: currentView, buildRequest: buildRequest };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
