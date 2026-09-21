"""
Patch top10_5min_equity_curves.html to include:
1. Return Type selector: [ Net Return | Alt Net Return ]
2. Mon 21 (Today Live) in availableDates
3. Dynamic metric mappings for NET vs ALT throughout the dashboard
Datetime: 2026-09-21 02:08 - [V20260921_0155]
"""
import re

html_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Header comments
v_head = """ * top10_5min_equity_curves.html — Universal Strategy Scenario Engine: Return Type Filter (Net Return vs Alt Net Return), Today Live (Sep 21), 5-Min Directional Split, Replay from Baseline & Delta Hiding
 *
 * VERSION HISTORY
 * v2.3.0 · 2026-09-21 · [V20260921_0155] Adds 'Return Type' filter (Net Return vs Alt Net Return) with counterfactual alt return evaluation across all models, rankings, directional splits, ribbons, cards, deltas, and overlay signals; appends Mon 21 (Today Live) data feed from PostgreSQL."""

text = text.replace(
    """ * top10_5min_equity_curves.html — Universal Strategy Scenario Engine: Scenario / Criteria Selection Modal, 5-Min Directional Split, Replay from Baseline & Delta Hiding
 *
 * VERSION HISTORY
 * v2.2.0 · 2026-09-20 · [V20260920_2348]""",
    v_head + """
 * v2.2.0 · 2026-09-20 · [V20260920_2348]"""
)

# 2. Add Return Type toggle markup right next to Scenario button
old_controls = """        <!-- Criteria / Scenario Modal Trigger Button -->
        <div class="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-sky-500/50 font-mono text-xs shadow-inner">
          <span class="text-[10px] uppercase font-bold text-slate-400 px-1.5 hidden sm:inline">Scenario:</span>
          <button id="openScenarioModalBtn" class="px-3 py-1 font-bold rounded bg-sky-600 hover:bg-sky-500 text-white transition flex items-center gap-1.5 shadow active:scale-95">
            <span id="activeScenarioIcon">★</span>
            <span id="activeScenarioName">Top 10 Net Return</span>
            <span class="text-[10px] bg-sky-700/80 px-1.5 py-0.2 rounded text-sky-200 ml-1">Change ▾</span>
          </button>
        </div>"""

new_controls = """        <!-- Return Type Selector (Net Return vs Alt Net Return) -->
        <div class="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-indigo-500/40 font-mono text-xs shadow-inner">
          <span class="text-[10px] uppercase font-bold text-slate-400 px-1.5 hidden sm:inline">Return:</span>
          <button id="returnTypeNetBtn" class="px-2.5 py-1 font-bold rounded bg-indigo-600 text-white transition flex items-center gap-1 shadow">
            <span>Net Return</span>
          </button>
          <button id="returnTypeAltBtn" class="px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1">
            <span>⚡ Alt Net</span>
          </button>
        </div>

        <!-- Criteria / Scenario Modal Trigger Button -->
        <div class="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-sky-500/50 font-mono text-xs shadow-inner">
          <span class="text-[10px] uppercase font-bold text-slate-400 px-1.5 hidden sm:inline">Scenario:</span>
          <button id="openScenarioModalBtn" class="px-3 py-1 font-bold rounded bg-sky-600 hover:bg-sky-500 text-white transition flex items-center gap-1.5 shadow active:scale-95">
            <span id="activeScenarioIcon">★</span>
            <span id="activeScenarioName">Top 10 Net Return</span>
            <span class="text-[10px] bg-sky-700/80 px-1.5 py-0.2 rounded text-sky-200 ml-1">Change ▾</span>
          </button>
        </div>"""

text = text.replace(old_controls, new_controls)

# 3. Add Mon 21 to availableDates
old_dates = """    const availableDates = [
      { id: 'WEEK_OVERALL', label: 'Full Week' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' }
    ];"""

new_dates = """    const availableDates = [
      { id: 'WEEK_OVERALL', label: 'Full Week' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' },
      { id: '2026-09-21', label: 'Mon 21 (Today Live)' }
    ];"""

text = text.replace(old_dates, new_dates)

# 4. Add currentReturnType state variable
old_vars = """    let currentCriteria = 'top_net'; // Active Scenario ID ('top_net', 'top_win', 'strongest_three', etc.)
    // Default to most recent trading date (datetime stamp: 2026-09-20 21:36 - [V20260920_2136])
    let currentDate = '2026-09-18';"""

new_vars = """    let currentReturnType = 'NET'; // 'NET' (default) or 'ALT'
    let currentCriteria = 'top_net'; // Active Scenario ID ('top_net', 'top_alt_net', 'top_win', etc.)
    // Default to most recent trading date (datetime stamp: 2026-09-21 02:08 - [V20260921_0155])
    let currentDate = '2026-09-21';"""

text = text.replace(old_vars, new_vars)

# 5. Add DOM references
old_dom = """    // DOM Elements
    const openScenarioModalBtn = document.getElementById('openScenarioModalBtn');"""

new_dom = """    // DOM Elements
    const returnTypeNetBtn = document.getElementById('returnTypeNetBtn');
    const returnTypeAltBtn = document.getElementById('returnTypeAltBtn');
    const openScenarioModalBtn = document.getElementById('openScenarioModalBtn');"""

text = text.replace(old_dom, new_dom)

# 6. Add setReturnType function & UI update
return_type_fn = """
    // ==========================================
    // RETURN TYPE FILTER (NET RETURN vs ALT NET RETURN)
    // ==========================================
    function setReturnType(type) {
      if (currentReturnType === type) return;
      currentReturnType = type;

      if (type === 'NET') {
        returnTypeNetBtn.className = 'px-2.5 py-1 font-bold rounded bg-indigo-600 text-white transition flex items-center gap-1 shadow';
        returnTypeAltBtn.className = 'px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1';
        // Switch back to top_net if currently on top_alt_net
        if (currentCriteria === 'top_alt_net') {
          currentCriteria = 'top_net';
          updateScenarioUI();
        }
      } else {
        returnTypeNetBtn.className = 'px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1';
        returnTypeAltBtn.className = 'px-2.5 py-1 font-bold rounded bg-amber-600 text-white transition flex items-center gap-1 shadow';
        // Auto select top_alt_net scenario if currently on top_net
        if (currentCriteria === 'top_net') {
          currentCriteria = 'top_alt_net';
          updateScenarioUI();
        }
      }

      updateDateLabelAndTitle();
      updateRibbon();
      renderCards();
      drawChart();
    }
"""

text = text.replace("    function init() {", return_type_fn + "\n    function init() {")

# 7. Add return type button listeners in setupEventListeners
old_listeners = """      // Scenario Modal Events"""
new_listeners = """      // Return Type Filter Events
      if (returnTypeNetBtn) returnTypeNetBtn.onclick = () => setReturnType('NET');
      if (returnTypeAltBtn) returnTypeAltBtn.onclick = () => setReturnType('ALT');

      // Scenario Modal Events"""

text = text.replace(old_listeners, new_listeners)

# 8. Metric Key Helper: returns active key names based on currentReturnType
metric_helpers = """
    function getMetricKeys() {
      const isAlt = currentReturnType === 'ALT';
      return {
        netKey: isAlt ? 'alt_net' : 'net',
        buyKey: isAlt ? 'alt_buy' : 'buy',
        sellKey: isAlt ? 'alt_sell' : 'sell',
        cumNetKey: isAlt ? 'cum_alt_net' : 'cum_net',
        buyNetKey: isAlt ? 'buy_alt_net' : 'buy_net',
        sellNetKey: isAlt ? 'sell_alt_net' : 'sell_net',
        winRateKey: isAlt ? 'alt_win_rate' : 'win_rate',
        winsKey: isAlt ? 'alt_wins' : 'wins'
      };
    }
"""

text = text.replace("    function getEligibleModels() {", metric_helpers + "\n    function getEligibleModels() {")

# 9. Update getEligibleModels to sort by active return type and filter win rate
old_eligible = """    function getEligibleModels() {
      const dataset = ALL_CRITERIA_DATA[currentCriteria] || {};
      const all = dataset[currentDate] || [];
      return all.filter(m => m.win_rate >= minWinRate);
    }"""

new_eligible = """    function getEligibleModels() {
      const dataset = ALL_CRITERIA_DATA[currentCriteria] || {};
      const all = dataset[currentDate] || [];
      const keys = getMetricKeys();
      return all.filter(m => (m[keys.winRateKey] || m.win_rate) >= minWinRate);
    }"""

text = text.replace(old_eligible, new_eligible)

# 10. Update updateRibbon to use active return type keys
old_ribbon = """      if (splitMode === 'TRI_SPLIT') {
        const m = eligible[selectedModelIndex] || eligible[0];
        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);

        const deltaNet = headPt.net - basePt.net;
        const deltaBuy = headPt.buy - basePt.buy;
        const deltaSell = headPt.sell - basePt.sell;"""

new_ribbon = """      const keys = getMetricKeys();
      if (splitMode === 'TRI_SPLIT') {
        const m = eligible[selectedModelIndex] || eligible[0];
        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);

        const deltaNet = (headPt[keys.netKey] !== undefined ? headPt[keys.netKey] : headPt.net) - (basePt[keys.netKey] !== undefined ? basePt[keys.netKey] : basePt.net);
        const deltaBuy = (headPt[keys.buyKey] !== undefined ? headPt[keys.buyKey] : headPt.buy) - (basePt[keys.buyKey] !== undefined ? basePt[keys.buyKey] : basePt.buy);
        const deltaSell = (headPt[keys.sellKey] !== undefined ? headPt[keys.sellKey] : headPt.sell) - (basePt[keys.sellKey] !== undefined ? basePt[keys.sellKey] : basePt.sell);"""

text = text.replace(old_ribbon, new_ribbon)

# 11. Update group ribbon calculation
old_group_ribbon = """        let totNet = 0, totBuy = 0, totSell = 0;
        const activeModels = eligible.filter(m => visibleModels.has(m.model));
        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          const headPt = getReplayHeadPoint(m.series);
          totNet += (headPt.net - basePt.net);
          totBuy += (headPt.buy - basePt.buy);
          totSell += (headPt.sell - basePt.sell);
        });"""

new_group_ribbon = """        let totNet = 0, totBuy = 0, totSell = 0;
        const activeModels = eligible.filter(m => visibleModels.has(m.model));
        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          const headPt = getReplayHeadPoint(m.series);
          const ptNet = headPt[keys.netKey] !== undefined ? headPt[keys.netKey] : headPt.net;
          const bNet = basePt[keys.netKey] !== undefined ? basePt[keys.netKey] : basePt.net;
          const ptBuy = headPt[keys.buyKey] !== undefined ? headPt[keys.buyKey] : headPt.buy;
          const bBuy = basePt[keys.buyKey] !== undefined ? basePt[keys.buyKey] : basePt.buy;
          const ptSell = headPt[keys.sellKey] !== undefined ? headPt[keys.sellKey] : headPt.sell;
          const bSell = basePt[keys.sellKey] !== undefined ? basePt[keys.sellKey] : basePt.sell;

          totNet += (ptNet - bNet);
          totBuy += (ptBuy - bBuy);
          totSell += (ptSell - bSell);
        });"""

text = text.replace(old_group_ribbon, new_group_ribbon)

# 12. Update renderCards to use active keys
old_cards = """        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);
        const deltaNet = headPt.net - basePt.net;
        const deltaBuy = headPt.buy - basePt.buy;
        const deltaSell = headPt.sell - basePt.sell;"""

new_cards = """        const keys = getMetricKeys();
        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);
        const deltaNet = (headPt[keys.netKey] !== undefined ? headPt[keys.netKey] : headPt.net) - (basePt[keys.netKey] !== undefined ? basePt[keys.netKey] : basePt.net);
        const deltaBuy = (headPt[keys.buyKey] !== undefined ? headPt[keys.buyKey] : headPt.buy) - (basePt[keys.buyKey] !== undefined ? basePt[keys.buyKey] : basePt.buy);
        const deltaSell = (headPt[keys.sellKey] !== undefined ? headPt[keys.sellKey] : headPt.sell) - (basePt[keys.sellKey] !== undefined ? basePt[keys.sellKey] : basePt.sell);
        const activeWinRate = m[keys.winRateKey] !== undefined ? m[keys.winRateKey] : m.win_rate;"""

text = text.replace(old_cards, new_cards)

# 13. Update card win rate display
text = text.replace(
    '<b class="${m.win_rate >= 80 ? \'text-emerald-400\' : \'text-slate-300\'} font-bold">${m.win_rate}% win</b>',
    '<b class="${activeWinRate >= 80 ? \'text-emerald-400\' : \'text-slate-300\'} font-bold">${activeWinRate}% win</b>'
)

# 14. Update drawChart TRI_SPLIT deltas
old_tri_chart = """        let deltas = [];
        const sliceLen = Math.min(m.series.length, drawUpTo + 1);
        for (let i = 0; i < sliceLen; i++) {
          const pt = m.series[i];
          if (showNetDelta) deltas.push(pt.net - basePt.net);
          if (showBuyDelta) deltas.push(pt.buy - basePt.buy);
          if (showSellDelta) deltas.push(pt.sell - basePt.sell);
        }"""

new_tri_chart = """        const keys = getMetricKeys();
        let deltas = [];
        const sliceLen = Math.min(m.series.length, drawUpTo + 1);
        for (let i = 0; i < sliceLen; i++) {
          const pt = m.series[i];
          const vNet = (pt[keys.netKey] !== undefined ? pt[keys.netKey] : pt.net) - (basePt[keys.netKey] !== undefined ? basePt[keys.netKey] : basePt.net);
          const vBuy = (pt[keys.buyKey] !== undefined ? pt[keys.buyKey] : pt.buy) - (basePt[keys.buyKey] !== undefined ? basePt[keys.buyKey] : basePt.buy);
          const vSell = (pt[keys.sellKey] !== undefined ? pt[keys.sellKey] : pt.sell) - (basePt[keys.sellKey] !== undefined ? basePt[keys.sellKey] : basePt.sell);
          if (showNetDelta) deltas.push(vNet);
          if (showBuyDelta) deltas.push(vBuy);
          if (showSellDelta) deltas.push(vSell);
        }"""

text = text.replace(old_tri_chart, new_tri_chart)

# 15. Update renderDeltaLine calls in TRI_SPLIT
old_lines = """        if (showBuyDelta) {
          renderDeltaLine(subSeries, 'buy', basePt.buy, '#10b981', 2.2, [4, 3], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.buy - basePt.buy), `Buy: £${(lastPt.buy - basePt.buy).toFixed(0)}`, '#10b981');
        }

        if (showSellDelta) {
          renderDeltaLine(subSeries, 'sell', basePt.sell, '#ef4444', 2.2, [4, 3], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.sell - basePt.sell), `Sell: £${(lastPt.sell - basePt.sell).toFixed(0)}`, '#ef4444');
        }

        if (showNetDelta) {
          renderDeltaLine(subSeries, 'net', basePt.net, '#0284c7', 3.0, [], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.net - basePt.net), `Total Net: £${(lastPt.net - basePt.net).toFixed(0)}`, '#38bdf8');
        }"""

new_lines = """        const bKey = keys.buyKey in lastPt ? keys.buyKey : 'buy';
        const sKey = keys.sellKey in lastPt ? keys.sellKey : 'sell';
        const nKey = keys.netKey in lastPt ? keys.netKey : 'net';

        if (showBuyDelta) {
          renderDeltaLine(subSeries, bKey, basePt[bKey] !== undefined ? basePt[bKey] : basePt.buy, '#10b981', 2.2, [4, 3], getX, getY);
          if (lastPt) {
            const vB = (lastPt[bKey] !== undefined ? lastPt[bKey] : lastPt.buy) - (basePt[bKey] !== undefined ? basePt[bKey] : basePt.buy);
            drawPointLabel(getX(lastIdx), getY(vB), `${currentReturnType === 'ALT' ? 'Alt Buy' : 'Buy'}: £${vB.toFixed(0)}`, '#10b981');
          }
        }

        if (showSellDelta) {
          renderDeltaLine(subSeries, sKey, basePt[sKey] !== undefined ? basePt[sKey] : basePt.sell, '#ef4444', 2.2, [4, 3], getX, getY);
          if (lastPt) {
            const vS = (lastPt[sKey] !== undefined ? lastPt[sKey] : lastPt.sell) - (basePt[sKey] !== undefined ? basePt[sKey] : basePt.sell);
            drawPointLabel(getX(lastIdx), getY(vS), `${currentReturnType === 'ALT' ? 'Alt Sell' : 'Sell'}: £${vS.toFixed(0)}`, '#ef4444');
          }
        }

        if (showNetDelta) {
          renderDeltaLine(subSeries, nKey, basePt[nKey] !== undefined ? basePt[nKey] : basePt.net, '#0284c7', 3.0, [], getX, getY);
          if (lastPt) {
            const vN = (lastPt[nKey] !== undefined ? lastPt[nKey] : lastPt.net) - (basePt[nKey] !== undefined ? basePt[nKey] : basePt.net);
            drawPointLabel(getX(lastIdx), getY(vN), `${currentReturnType === 'ALT' ? 'Alt Net' : 'Total Net'}: £${vN.toFixed(0)}`, '#38bdf8');
          }
        }"""

text = text.replace(old_lines, new_lines)

# 16. Update group metric in drawChart
old_grp_metric = """        // Group modes (ALL_NET, BUY_NET, SELL_NET)
        let activeMetric = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');"""

new_grp_metric = """        // Group modes (ALL_NET, BUY_NET, SELL_NET)
        const keys = getMetricKeys();
        let activeMetric = splitMode === 'BUY_NET' ? keys.buyKey : (splitMode === 'SELL_NET' ? keys.sellKey : keys.netKey);"""

text = text.replace(old_grp_metric, new_grp_metric)

# 17. Update tooltip TRI_SPLIT
old_tt_tri = """          const dNet = pt.net - basePt.net;
          const dBuy = pt.buy - basePt.buy;
          const dSell = pt.sell - basePt.sell;"""

new_tt_tri = """          const keys = getMetricKeys();
          const dNet = (pt[keys.netKey] !== undefined ? pt[keys.netKey] : pt.net) - (basePt[keys.netKey] !== undefined ? basePt[keys.netKey] : basePt.net);
          const dBuy = (pt[keys.buyKey] !== undefined ? pt[keys.buyKey] : pt.buy) - (basePt[keys.buyKey] !== undefined ? basePt[keys.buyKey] : basePt.buy);
          const dSell = (pt[keys.sellKey] !== undefined ? pt[keys.sellKey] : pt.sell) - (basePt[keys.sellKey] !== undefined ? basePt[keys.sellKey] : basePt.sell);"""

text = text.replace(old_tt_tri, new_tt_tri)

# 18. Update group tooltip metricKey
old_tt_grp = """          const metricKey = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');"""
new_tt_grp = """          const keys = getMetricKeys();
          const metricKey = splitMode === 'BUY_NET' ? keys.buyKey : (splitMode === 'SELL_NET' ? keys.sellKey : keys.netKey);"""

text = text.replace(old_tt_grp, new_tt_grp)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

# Also copy to brain artifact
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
with open(brain_path, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully patched top10_5min_equity_curves.html with Return Type filter and updated brain artifact!")
