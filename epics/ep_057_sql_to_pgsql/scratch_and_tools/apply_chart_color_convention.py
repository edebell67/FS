# Script to apply color updates to top10_5min_equity_curves.html
# buy_net -> Green (#10b981), sell_net -> Red (#ef4444), total_net -> Blue (#0284c7 / #38bdf8)
# Datetime stamp: 2026-09-20 23:09 - [V20260920_2309]

html_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update version history header
old_v = "* v1.8.0 · 2026-09-20 · [V20260920_2136]"
new_v = "* v1.9.0 · 2026-09-20 · [V20260920_2309] Standardizes chart line colors and metric UI badges to financial conventions: buy_net = Green (#10b981), sell_net = Red (#ef4444), and total_net = Blue (#0284c7 / #38bdf8); preserves all universal replay, baseline, scenario modal, and directional split controls.\n * v1.8.0 · 2026-09-20 · [V20260920_2136]"

if old_v in text:
    text = text.replace(old_v, new_v, 1)

# 2. Header description subtitle
text = text.replace(
    'Inspect Total Net, <span class="text-sky-400 font-semibold">Buy Net</span> & <span class="text-amber-400 font-semibold">Sell Net</span>',
    'Inspect <span class="text-sky-400 font-semibold">Total Net (Blue)</span>, <span class="text-emerald-400 font-semibold">Buy Net (Green)</span> & <span class="text-rose-400 font-semibold">Sell Net (Red)</span>'
)

# 3. Directional Split Mode Buttons styling in setSplitMode(mode)
old_split_modes = """      if (mode === 'ALL_NET') metricAll.className = 'px-2.5 py-1 font-semibold rounded bg-sky-600 text-white transition';
      if (mode === 'BUY_NET') metricBuy.className = 'px-2.5 py-1 font-semibold rounded bg-sky-500 text-white transition';
      if (mode === 'SELL_NET') metricSell.className = 'px-2.5 py-1 font-semibold rounded bg-amber-500 text-white transition';
      if (mode === 'TRI_SPLIT') metricTriSplit.className = 'px-2.5 py-1 font-semibold rounded bg-purple-600 text-white transition';"""

new_split_modes = """      if (mode === 'ALL_NET') metricAll.className = 'px-2.5 py-1 font-semibold rounded bg-sky-600 text-white transition shadow';
      if (mode === 'BUY_NET') metricBuy.className = 'px-2.5 py-1 font-semibold rounded bg-emerald-600 text-white transition shadow';
      if (mode === 'SELL_NET') metricSell.className = 'px-2.5 py-1 font-semibold rounded bg-rose-600 text-white transition shadow';
      if (mode === 'TRI_SPLIT') metricTriSplit.className = 'px-2.5 py-1 font-semibold rounded bg-purple-600 text-white transition shadow';"""

assert old_split_modes in text, "old_split_modes not found!"
text = text.replace(old_split_modes, new_split_modes, 1)

# 4. Ribbon Net / Buy / Sell labels and values in Tri-Split and Group
# Ribbon Net: Blue (#38bdf8 / text-sky-400), Buy: Green (text-emerald-400), Sell: Red (text-rose-400)
# Update Tri-split ribbon lines:
old_tri_ribbon = """        ribbonTotNet.textContent = fmt(deltaNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${deltaNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}`;

        ribbonBuyNet.textContent = fmt(deltaBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${deltaBuy >= 0 ? 'text-sky-400' : 'text-rose-400'}`;

        ribbonSellNet.textContent = fmt(deltaSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${deltaSell >= 0 ? 'text-amber-400' : 'text-rose-400'}`;"""

new_tri_ribbon = """        ribbonTotNet.textContent = fmt(deltaNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${deltaNet >= 0 ? 'text-sky-400' : 'text-sky-300'}`;

        ribbonBuyNet.textContent = fmt(deltaBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${deltaBuy >= 0 ? 'text-emerald-400' : 'text-emerald-300'}`;

        ribbonSellNet.textContent = fmt(deltaSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${deltaSell >= 0 ? 'text-rose-400' : 'text-rose-300'}`;"""

assert old_tri_ribbon in text, "old_tri_ribbon not found!"
text = text.replace(old_tri_ribbon, new_tri_ribbon, 1)

# Update Group ribbon lines:
old_grp_ribbon = """        ribbonTotNet.textContent = fmt(totNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${totNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}`;

        ribbonBuyNet.textContent = fmt(totBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${totBuy >= 0 ? 'text-sky-400' : 'text-rose-400'}`;

        ribbonSellNet.textContent = fmt(totSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${totSell >= 0 ? 'text-amber-400' : 'text-rose-400'}`;"""

new_grp_ribbon = """        ribbonTotNet.textContent = fmt(totNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${totNet >= 0 ? 'text-sky-400' : 'text-sky-300'}`;

        ribbonBuyNet.textContent = fmt(totBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${totBuy >= 0 ? 'text-emerald-400' : 'text-emerald-300'}`;

        ribbonSellNet.textContent = fmt(totSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${totSell >= 0 ? 'text-rose-400' : 'text-rose-300'}`;"""

assert old_grp_ribbon in text, "old_grp_ribbon not found!"
text = text.replace(old_grp_ribbon, new_grp_ribbon, 1)

# Also update Ribbon top labels classes in HTML markup
old_ribbon_markup = """          <div>
            <div class="text-[9px] uppercase tracking-wider text-slate-400" id="totalNetLabel">Total Net</div>
            <div class="text-base sm:text-lg font-black text-emerald-400" id="ribbonTotNet">+£0.00</div>
          </div>
          <div class="border-l border-slate-800 pl-3">
            <div class="text-[9px] uppercase tracking-wider text-sky-400" id="buyNetLabel">Cum Buy Net</div>
            <div class="text-xs sm:text-sm font-bold text-sky-400" id="ribbonBuyNet">+£0.00</div>
          </div>
          <div class="border-l border-slate-800 pl-3">
            <div class="text-[9px] uppercase tracking-wider text-amber-400" id="sellNetLabel">Cum Sell Net</div>
            <div class="text-xs sm:text-sm font-bold text-amber-400" id="ribbonSellNet">+£0.00</div>
          </div>"""

new_ribbon_markup = """          <div>
            <div class="text-[9px] uppercase tracking-wider text-sky-400" id="totalNetLabel">Total Net (Blue)</div>
            <div class="text-base sm:text-lg font-black text-sky-300" id="ribbonTotNet">+£0.00</div>
          </div>
          <div class="border-l border-slate-800 pl-3">
            <div class="text-[9px] uppercase tracking-wider text-emerald-400" id="buyNetLabel">Cum Buy Net (Green)</div>
            <div class="text-xs sm:text-sm font-bold text-emerald-400" id="ribbonBuyNet">+£0.00</div>
          </div>
          <div class="border-l border-slate-800 pl-3">
            <div class="text-[9px] uppercase tracking-wider text-rose-400" id="sellNetLabel">Cum Sell Net (Red)</div>
            <div class="text-xs sm:text-sm font-bold text-rose-400" id="ribbonSellNet">+£0.00</div>
          </div>"""

assert old_ribbon_markup in text, "old_ribbon_markup not found!"
text = text.replace(old_ribbon_markup, new_ribbon_markup, 1)

# 5. Delta button styling in updateDeltaButtonsUI()
# Net: Blue, Buy: Green, Sell: Red
old_delta_btns_fn = """    function updateDeltaButtonsUI() {
      // Net Delta
      if (showNetDelta) {
        toggleNetDeltaBtn.classList.remove('off');
        toggleNetDeltaBtn.classList.add('bg-emerald-500/15', 'border-emerald-500/40', 'text-emerald-300');
        netDeltaCheck.textContent = '✓';
      } else {
        toggleNetDeltaBtn.classList.add('off');
        toggleNetDeltaBtn.classList.remove('bg-emerald-500/15', 'border-emerald-500/40', 'text-emerald-300');
        netDeltaCheck.textContent = '✕';
      }

      // Buy Delta
      if (showBuyDelta) {
        toggleBuyDeltaBtn.classList.remove('off');
        toggleBuyDeltaBtn.classList.add('bg-sky-500/15', 'border-sky-500/40', 'text-sky-300');
        buyDeltaCheck.textContent = '✓';
      } else {
        toggleBuyDeltaBtn.classList.add('off');
        toggleBuyDeltaBtn.classList.remove('bg-sky-500/15', 'border-sky-500/40', 'text-sky-300');
        buyDeltaCheck.textContent = '✕';
      }

      // Sell Delta
      if (showSellDelta) {
        toggleSellDeltaBtn.classList.remove('off');
        toggleSellDeltaBtn.classList.add('bg-amber-500/15', 'border-amber-500/40', 'text-amber-300');
        sellDeltaCheck.textContent = '✓';
      } else {
        toggleSellDeltaBtn.classList.add('off');
        toggleSellDeltaBtn.classList.remove('bg-amber-500/15', 'border-amber-500/40', 'text-amber-300');
        sellDeltaCheck.textContent = '✕';
      }
    }"""

new_delta_btns_fn = """    function updateDeltaButtonsUI() {
      // Net Delta (Blue)
      if (showNetDelta) {
        toggleNetDeltaBtn.classList.remove('off');
        toggleNetDeltaBtn.classList.add('bg-sky-500/15', 'border-sky-500/40', 'text-sky-300');
        netDeltaCheck.textContent = '✓';
      } else {
        toggleNetDeltaBtn.classList.add('off');
        toggleNetDeltaBtn.classList.remove('bg-sky-500/15', 'border-sky-500/40', 'text-sky-300');
        netDeltaCheck.textContent = '✕';
      }

      // Buy Delta (Green)
      if (showBuyDelta) {
        toggleBuyDeltaBtn.classList.remove('off');
        toggleBuyDeltaBtn.classList.add('bg-emerald-500/15', 'border-emerald-500/40', 'text-emerald-300');
        buyDeltaCheck.textContent = '✓';
      } else {
        toggleBuyDeltaBtn.classList.add('off');
        toggleBuyDeltaBtn.classList.remove('bg-emerald-500/15', 'border-emerald-500/40', 'text-emerald-300');
        buyDeltaCheck.textContent = '✕';
      }

      // Sell Delta (Red)
      if (showSellDelta) {
        toggleSellDeltaBtn.classList.remove('off');
        toggleSellDeltaBtn.classList.add('bg-rose-500/15', 'border-rose-500/40', 'text-rose-300');
        sellDeltaCheck.textContent = '✓';
      } else {
        toggleSellDeltaBtn.classList.add('off');
        toggleSellDeltaBtn.classList.remove('bg-rose-500/15', 'border-rose-500/40', 'text-rose-300');
        sellDeltaCheck.textContent = '✕';
      }
    }"""

assert old_delta_btns_fn in text, "old_delta_btns_fn not found!"
text = text.replace(old_delta_btns_fn, new_delta_btns_fn, 1)

# Also update Delta Buttons HTML markup
old_delta_markup = """          <button id="toggleNetDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 font-bold hover:bg-emerald-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>Net Delta</span>
            <span id="netDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>

          <button id="toggleBuyDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-sky-500/15 border border-sky-500/40 text-sky-300 font-bold hover:bg-sky-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span>Buy Delta (Longs)</span>
            <span id="buyDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>

          <button id="toggleSellDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-500/15 border border-amber-500/40 text-amber-300 font-bold hover:bg-amber-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <span>Sell Delta (Shorts)</span>
            <span id="sellDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>"""

new_delta_markup = """          <button id="toggleNetDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-sky-500/15 border border-sky-500/40 text-sky-300 font-bold hover:bg-sky-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-sky-400"></span>
            <span>Total Net (Blue)</span>
            <span id="netDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>

          <button id="toggleBuyDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 font-bold hover:bg-emerald-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>Buy Net (Green)</span>
            <span id="buyDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>

          <button id="toggleSellDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-500/15 border border-rose-500/40 text-rose-300 font-bold hover:bg-rose-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-rose-400"></span>
            <span>Sell Net (Red)</span>
            <span id="sellDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>"""

assert old_delta_markup in text, "old_delta_markup not found!"
text = text.replace(old_delta_markup, new_delta_markup, 1)

# 6. Chart curves colors in Tri-Split mode inside drawChart()
# Buy -> Green (#10b981), Sell -> Red (#ef4444), Net -> Blue (#0284c7 / #38bdf8)
old_tri_chart = """        if (showBuyDelta) {
          renderDeltaLine(subSeries, 'buy', basePt.buy, '#38bdf8', 2.2, [4, 3], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.buy - basePt.buy), `Buy: £${(lastPt.buy - basePt.buy).toFixed(0)}`, '#38bdf8');
        }

        if (showSellDelta) {
          renderDeltaLine(subSeries, 'sell', basePt.sell, '#fbbf24', 2.2, [4, 3], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.sell - basePt.sell), `Sell: £${(lastPt.sell - basePt.sell).toFixed(0)}`, '#fbbf24');
        }

        if (showNetDelta) {
          renderDeltaLine(subSeries, 'net', basePt.net, '#34d399', 3.0, [], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.net - basePt.net), `Net: £${(lastPt.net - basePt.net).toFixed(0)}`, '#34d399');
        }"""

new_tri_chart = """        if (showBuyDelta) {
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

assert old_tri_chart in text, "old_tri_chart not found!"
text = text.replace(old_tri_chart, new_tri_chart, 1)

# 7. Model Card sub-metrics color update (Buy: Green, Sell: Red)
old_card_metrics = """            <span class="text-[10px] text-slate-400">
              <b class="text-sky-400">B:${fmt(deltaBuy)}</b> <b class="text-amber-400">S:${fmt(deltaSell)}</b>
            </span>"""

new_card_metrics = """            <span class="text-[10px] text-slate-400">
              <b class="text-emerald-400">B:${fmt(deltaBuy)}</b> <b class="text-rose-400">S:${fmt(deltaSell)}</b>
            </span>"""

assert old_card_metrics in text, "old_card_metrics not found!"
text = text.replace(old_card_metrics, new_card_metrics, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

with open(brain_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Applied color updates to top10_5min_equity_curves.html and brain artifact successfully!")
