/* epics/ep_057_sql_to_pgsql/scenario_engine_v2/runner/static/engine_client.js — the browser side of the engine call contract (engine/rpc.py).
 *
 * VERSION HISTORY
 * v1.0.0 · 2026-10-17 · Initial version: synchronous POST /engine/call with a memo of identical requests; ?engine=<base> overrides the engine location.
 *
 * The page's drawing code is synchronous, so the call is a synchronous XMLHttpRequest to the local engine service. The engine functions are pure functions of their request,
 * so an identical request is answered from the memo (a redraw with nothing changed costs no round trip). */
(function () {
  'use strict';
  var BASE = (new URLSearchParams(location.search).get('engine') || location.origin).replace(/\/$/, '');
  var MEMO_MAX = 256;
  var memo = new Map();
  var stats = { calls: 0, hits: 0, requests: 0, ms: 0 };

  function call(request) {
    var key = JSON.stringify(request);
    stats.calls++;
    if (memo.has(key)) { stats.hits++; return memo.get(key); }
    var t0 = (typeof performance !== 'undefined' ? performance.now() : Date.now());
    var xhr = new XMLHttpRequest();
    xhr.open('POST', BASE + '/engine/call', false);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(key);
    stats.requests++;
    stats.ms += (typeof performance !== 'undefined' ? performance.now() : Date.now()) - t0;
    if (xhr.status !== 200) throw new Error('engine call ' + request.fn + ' failed (' + xhr.status + '): ' + String(xhr.responseText).slice(0, 300));
    var result = JSON.parse(xhr.responseText);
    memo.set(key, result);
    if (memo.size > MEMO_MAX) memo.delete(memo.keys().next().value);
    return result;
  }

  window.__engine = { call: call, base: BASE, stats: stats, clear: function () { memo.clear(); } };
})();
