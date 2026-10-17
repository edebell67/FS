// epics/ep_057_sql_to_pgsql/scenario_engine_v2/tools/thin_runner.js — runs the page's ORIGINAL overlay / rotation functions and the engine-client copy's STUBS on the same inputs (Node VM).
//
// VERSION HISTORY
// v1.1.0 · 2026-10-17 · Date is frozen (spec.now) so the live-date staleness path is reproducible; a failed engine answer is thrown into the page like a failed request.
// v1.0.0 · 2026-10-17 · Initial version: mode "collect" records the requests the stubs make; mode "answer" feeds them engine responses (computed in Python) and returns both sides' results.
'use strict';
const fs = require('fs');
const vm = require('vm');

const spec = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));

function extract(pagePath, inventoryPath, names) {
  const lines = fs.readFileSync(pagePath, 'utf8').split(/\r?\n/);
  const inv = JSON.parse(fs.readFileSync(inventoryPath, 'utf8'));
  const byName = new Map();
  for (const f of inv.functions) byName.set(f.name, f);
  return names.map(n => {
    const f = byName.get(n);
    if (!f) throw new Error('function not found: ' + n);
    return lines.slice(f.start_line - 1, f.end_line).join('\n');
  }).join('\n');
}

const origSrc = extract(spec.page, spec.inventory, spec.origFunctions);
const thinSrc = extract(spec.thinPage, spec.thinInventory, spec.thinFunctions);

const DEFAULTS = { currentReturnType: 'NET', baselineFrameIndex: 0, currentFrameIndex: -1, exitThreshold: 0, overlayTopX: 1, dailyTarget: 500, activePortfolioName: null,
  currentDate: '', currentProductType: 'forex', currentProduct: 'all', LIVE_DATE: '2099-01-01', PORTFOLIO_VIEW_REFRESH_MS: 300000, __rule: null, __maxFrames: 1 };

function makeContext(src, c, engine) {
  const NOW = spec.now;
  class FrozenDate extends Date { constructor(...a) { super(...(a.length ? a : [NOW])); } static now() { return NOW; } }
  const sandbox = { console, Math, Number, String, Map, Set, Array, JSON, Infinity, Date: FrozenDate, __engine: engine };
  const ctx = vm.createContext(sandbox);
  Object.assign(ctx, DEFAULTS, c.globals, { __rule: c.rule || null, __maxFrames: c.maxFrames == null ? 1 : c.maxFrames, assignedOverlayTradeCache: new Map(c.cache || []) });
  vm.runInContext('function activePortfolioOverlayRule(){ return __rule; } function getMaxFrames(){ return __maxFrames; }', ctx);
  vm.runInContext(src, ctx, { filename: 'page_functions.js' });
  return ctx;
}

function resolveArgs(c) {
  const models = c.dataset ? JSON.parse(JSON.stringify(spec.datasets[c.dataset])) : null;
  return c.args.map(a => {
    if (a && typeof a === 'object' && !Array.isArray(a) && '$ds' in a) return models;
    if (a && typeof a === 'object' && !Array.isArray(a) && '$longest' in a) return models.reduce((best, m) => m.series.length > best.series.length ? m : best, models[0]).series;
    return a;
  });
}

const strip = r => r && r.trades ? { signals: r.signals, trades: r.trades.map(t => { const { curveModel, ...x } = t; return x; }), threshold: r.threshold, targetSignal: r.targetSignal } : r;
const linked = r => !(r && r.trades) || r.trades.every(t => t.curveModel && t.curveModel.model === t.model);
const DUMMY = { signals: [], trades: [], threshold: 0, targetSignal: null };

const out = [];
for (const c of spec.cases) {
  const requests = [];
  const engine = {
    call(req) {
      const key = JSON.stringify(req);
      requests.push(key);
      if (spec.mode === 'collect') return req.fn === 'computeTradeOverlaySignals' ? [] : (req.fn === 'computeSplitTargetSignal' ? null : (req.fn === 'pairOverlayTrades' ? [] : DUMMY));
      if (!(key in spec.responses)) throw new Error('no engine response recorded for ' + req.fn);
      const text = spec.responses[key];
      if (text.startsWith('ERROR:')) throw new Error(text);
      return JSON.parse(text);
    }
  };
  const row = { id: c.id, requests };
  try {
    const thin = makeContext(thinSrc, c, engine);
    const tr = thin[c.fn](...resolveArgs(c));
    row.thin = strip(JSON.parse(JSON.stringify(tr === undefined ? null : tr)));
    row.thinLinked = linked(tr);
    if (spec.mode === 'answer') {
      const orig = makeContext(origSrc, c, { call() { throw new Error('the original must not call the engine'); } });
      const or = orig[c.fn](...resolveArgs(c));
      row.orig = strip(JSON.parse(JSON.stringify(or === undefined ? null : or)));
    }
  } catch (e) { row.error = String(e && e.message || e); }
  out.push(row);
}
fs.writeFileSync(process.argv[3], JSON.stringify(out));
