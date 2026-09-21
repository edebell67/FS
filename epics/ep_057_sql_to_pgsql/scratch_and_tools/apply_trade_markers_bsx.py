# Script to implement overlay trade markers (B, S, X) active ONLY when viewing buy_net / sell_net
# Datetime stamp: 2026-09-20 23:31 - [V20260920_2331]

html_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"

with open(html_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Version History header
old_v = "* v1.9.0 · 2026-09-20 · [V20260920_2309]"
new_v = "* v2.0.0 · 2026-09-20 · [V20260920_2331] Implements overlay trade markers ('B', 'S', 'X') rendered on the chart when viewing with buy_net / sell_net: Buy entry/switch ('B', green), Sell entry/switch ('S', red), and Exit to flat ('X', slate); includes toolbar toggle and rich interactive tooltip.\n * v1.9.0 · 2026-09-20 · [V20260920_2309]"

if old_v in text:
    text = text.replace(old_v, new_v, 1)

# 2. Add state variable for showing trade markers
old_state = "    let showSellDelta = true;"
new_state = """    let showSellDelta = true;
    let showTradeMarkers = true; // Overlay trade markers (B, S, X) when viewing buy/sell"""

assert old_state in text, "old_state not found!"
text = text.replace(old_state, new_state, 1)

# 3. Add Trade Markers Toggle Button in deltaControlsBar HTML markup
old_controls_bar = """          <button id="toggleSellDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-500/15 border border-rose-500/40 text-rose-300 font-bold hover:bg-rose-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-rose-400"></span>
            <span>Sell Net (Red)</span>
            <span id="sellDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>
        </div>"""

new_controls_bar = """          <button id="toggleSellDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-rose-500/15 border border-rose-500/40 text-rose-300 font-bold hover:bg-rose-500/25 transition">
            <span class="w-2 h-2 rounded-full bg-rose-400"></span>
            <span>Sell Net (Red)</span>
            <span id="sellDeltaCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>

          <!-- Trade Overlay Signals Toggle -->
          <button id="toggleTradeMarkersBtn" title="Overlay B, S, X trade markers when viewing buy_net / sell_net" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-amber-500/20 border border-amber-500/50 text-amber-300 font-bold hover:bg-amber-500/30 transition shadow">
            <span class="text-[11px]">🏷</span>
            <span>Signals (B/S/X)</span>
            <span id="tradeMarkersCheck" class="text-[10px] ml-0.5 font-bold">✓</span>
          </button>
        </div>"""

assert old_controls_bar in text, "old_controls_bar not found!"
text = text.replace(old_controls_bar, new_controls_bar, 1)

# 4. Bind DOM Element & Event Listener
old_dom = "    const sellDeltaCheck = document.getElementById('sellDeltaCheck');"
new_dom = """    const sellDeltaCheck = document.getElementById('sellDeltaCheck');
    const toggleTradeMarkersBtn = document.getElementById('toggleTradeMarkersBtn');
    const tradeMarkersCheck = document.getElementById('tradeMarkersCheck');"""

assert old_dom in text, "old_dom not found!"
text = text.replace(old_dom, new_dom, 1)

# In updateDeltaButtonsUI()
old_delta_fn_end = """      // Sell Delta (Red)
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

new_delta_fn_end = """      // Sell Delta (Red)
      if (showSellDelta) {
        toggleSellDeltaBtn.classList.remove('off');
        toggleSellDeltaBtn.classList.add('bg-rose-500/15', 'border-rose-500/40', 'text-rose-300');
        sellDeltaCheck.textContent = '✓';
      } else {
        toggleSellDeltaBtn.classList.add('off');
        toggleSellDeltaBtn.classList.remove('bg-rose-500/15', 'border-rose-500/40', 'text-rose-300');
        sellDeltaCheck.textContent = '✕';
      }

      // Trade Markers Toggle (B, S, X)
      if (toggleTradeMarkersBtn && tradeMarkersCheck) {
        if (showTradeMarkers) {
          toggleTradeMarkersBtn.classList.remove('off');
          toggleTradeMarkersBtn.classList.add('bg-amber-500/20', 'border-amber-500/50', 'text-amber-300');
          tradeMarkersCheck.textContent = '✓';
        } else {
          toggleTradeMarkersBtn.classList.add('off');
          toggleTradeMarkersBtn.classList.remove('bg-amber-500/20', 'border-amber-500/50', 'text-amber-300');
          tradeMarkersCheck.textContent = '✕';
        }
      }
    }"""

assert old_delta_fn_end in text, "old_delta_fn_end not found!"
text = text.replace(old_delta_fn_end, new_delta_fn_end, 1)

# In setupEventListeners()
old_delta_events = """      toggleSellDeltaBtn.onclick = () => {
        showSellDelta = !showSellDelta;
        updateDeltaButtonsUI();
        drawChart();
      };"""

new_delta_events = """      toggleSellDeltaBtn.onclick = () => {
        showSellDelta = !showSellDelta;
        updateDeltaButtonsUI();
        drawChart();
      };

      if (toggleTradeMarkersBtn) {
        toggleTradeMarkersBtn.onclick = () => {
          showTradeMarkers = !showTradeMarkers;
          updateDeltaButtonsUI();
          drawChart();
        };
      }"""

assert old_delta_events in text, "old_delta_events not found!"
text = text.replace(old_delta_events, new_delta_events, 1)

# 5. Helper Function: computeTradeOverlaySignals(subSeries, basePt)
marker_functions = """    // ==========================================
    // OVERLAY TRADE MARKERS (B, S, X) LOGIC
    // ==========================================
    // Rule:
    // If buy_net > 0 and buy_net > sell_net -> Buy ('B') [if in sell, switch to buy]
    // If sell_net > 0 and sell_net > buy_net -> Sell ('S') [if in buy, switch to sell]
    // Exit to flat ('X') when active side falls <= 0
    function computeTradeOverlaySignals(seriesSlice, basePt) {
      const signals = [];
      let state = 'FLAT'; // 'FLAT', 'BUY', 'SELL'

      for (let i = 0; i < seriesSlice.length; i++) {
        const pt = seriesSlice[i];
        const buyDelta = pt.buy - basePt.buy;
        const sellDelta = pt.sell - basePt.sell;

        if (buyDelta > 0 && buyDelta > sellDelta) {
          if (state !== 'BUY') {
            const isSwitch = (state === 'SELL');
            state = 'BUY';
            signals.push({
              idx: i,
              time: pt.time,
              type: 'B',
              isSwitch: isSwitch,
              val: buyDelta,
              buy: buyDelta,
              sell: sellDelta,
              text: isSwitch ? 'SWITCH BUY' : 'BUY'
            });
          }
        } else if (sellDelta > 0 && sellDelta > buyDelta) {
          if (state !== 'SELL') {
            const isSwitch = (state === 'BUY');
            state = 'SELL';
            signals.push({
              idx: i,
              time: pt.time,
              type: 'S',
              isSwitch: isSwitch,
              val: sellDelta,
              buy: buyDelta,
              sell: sellDelta,
              text: isSwitch ? 'SWITCH SELL' : 'SELL'
            });
          }
        } else {
          // Neither is positive/dominant -> Exit to flat
          if (state !== 'FLAT') {
            const exitedFrom = state;
            state = 'FLAT';
            signals.push({
              idx: i,
              time: pt.time,
              type: 'X',
              isSwitch: false,
              val: exitedFrom === 'BUY' ? buyDelta : sellDelta,
              buy: buyDelta,
              sell: sellDelta,
              text: `EXIT ${exitedFrom}`
            });
          }
        }
      }
      return signals;
    }

    function drawSignalBadge(x, y, type, label) {
      ctx.save();
      const radius = 8;
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);

      if (type === 'B') {
        ctx.fillStyle = '#10b981'; // Emerald Green
        ctx.strokeStyle = '#ffffff';
      } else if (type === 'S') {
        ctx.fillStyle = '#ef4444'; // Red
        ctx.strokeStyle = '#ffffff';
      } else {
        ctx.fillStyle = '#475569'; // Slate for Exit
        ctx.strokeStyle = '#f8fafc';
      }

      ctx.lineWidth = 1.5;
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#ffffff';
      ctx.font = 'bold 10px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(type, x, y + 0.5);

      ctx.restore();
    }
"""

# Insert marker functions right before drawChart()
pos_draw_chart = text.find("    function drawChart() {")
assert pos_draw_chart != -1, "drawChart not found!"
text = text[:pos_draw_chart] + marker_functions + "\n" + text[pos_draw_chart:]

# 6. Render Trade Markers in Tri-Split mode inside drawChart()
# Markers are rendered when viewing buy_net / sell_net (showBuyDelta or showSellDelta active, and not viewing pure Total Net only)
old_tri_render = """        if (showNetDelta) {
          renderDeltaLine(subSeries, 'net', basePt.net, '#0284c7', 3.0, [], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.net - basePt.net), `Total Net: £${(lastPt.net - basePt.net).toFixed(0)}`, '#38bdf8');
        }

        // Draw Replay Vertical Cursor
        drawReplayCursor(getX(drawUpTo), padTop, height - padBottom, headTime);"""

new_tri_render = """        if (showNetDelta) {
          renderDeltaLine(subSeries, 'net', basePt.net, '#0284c7', 3.0, [], getX, getY);
          if (lastPt) drawPointLabel(getX(lastIdx), getY(lastPt.net - basePt.net), `Total Net: £${(lastPt.net - basePt.net).toFixed(0)}`, '#38bdf8');
        }

        // Draw Overlay Trade Markers (B, S, X) when viewing buy_net / sell_net
        let activeSignals = [];
        if (showTradeMarkers && (showBuyDelta || showSellDelta)) {
          activeSignals = computeTradeOverlaySignals(subSeries, basePt);
          activeSignals.forEach(sig => {
            const sigX = getX(sig.idx);
            // Position on corresponding curve
            const sigY = sig.type === 'B' ? getY(sig.buy) : (sig.type === 'S' ? getY(sig.sell) : getY(sig.val));
            drawSignalBadge(sigX, sigY, sig.type, sig.text);
          });
        }

        // Draw Replay Vertical Cursor
        drawReplayCursor(getX(drawUpTo), padTop, height - padBottom, headTime);"""

assert old_tri_render in text, "old_tri_render not found!"
text = text.replace(old_tri_render, new_tri_render, 1)

# Store activeSignals in timeAxisPoints for tooltip
old_tri_axis = """        timeAxisPoints = subSeries.map((s, idx) => ({
          x: getX(idx),
          idx: idx,
          time: s.time,
          data: s
        }));"""

new_tri_axis = """        timeAxisPoints = subSeries.map((s, idx) => {
          const matchedSignal = activeSignals ? activeSignals.find(sig => sig.idx === idx) : null;
          return {
            x: getX(idx),
            idx: idx,
            time: s.time,
            data: s,
            signal: matchedSignal
          };
        });"""

assert old_tri_axis in text, "old_tri_axis not found!"
text = text.replace(old_tri_axis, new_tri_axis, 1)

# 7. Update Tooltip in Tri-Split to display active Trade Marker
old_tooltip_tri_end = """          tooltip.innerHTML = `
            <div class="font-mono font-bold text-white border-b border-slate-700 pb-1 mb-1.5 flex justify-between">
              <span>${closest.time}</span>
              <span class="text-sky-300 font-bold">${m.model}</span>
            </div>
            <div class="space-y-1 font-mono text-[11px]">
              ${rows}
              <div class="flex justify-between border-t border-slate-800 pt-1 text-[10px] text-slate-400">
                <span>Trades / Open:</span>
                <span class="text-slate-300 font-bold">${pt.trades} / ${pt.open}</span>
              </div>
            </div>
          `;"""

new_tooltip_tri_end = """          let signalBadgeHtml = '';
          if (closest.signal) {
            const sig = closest.signal;
            const badgeColor = sig.type === 'B' ? 'bg-emerald-500/30 text-emerald-200 border-emerald-500/50' : (sig.type === 'S' ? 'bg-rose-500/30 text-rose-200 border-rose-500/50' : 'bg-slate-700 text-slate-200 border-slate-600');
            signalBadgeHtml = `
              <div class="my-1.5 px-2 py-1 rounded border flex items-center justify-between font-bold text-[10px] ${badgeColor}">
                <span>SIGNAL: [${sig.type}] ${sig.text}</span>
                <span>@ ${sig.time}</span>
              </div>
            `;
          }

          tooltip.innerHTML = `
            <div class="font-mono font-bold text-white border-b border-slate-700 pb-1 mb-1.5 flex justify-between">
              <span>${closest.time}</span>
              <span class="text-sky-300 font-bold">${m.model}</span>
            </div>
            ${signalBadgeHtml}
            <div class="space-y-1 font-mono text-[11px]">
              ${rows}
              <div class="flex justify-between border-t border-slate-800 pt-1 text-[10px] text-slate-400">
                <span>Trades / Open:</span>
                <span class="text-slate-300 font-bold">${pt.trades} / ${pt.open}</span>
              </div>
            </div>
          `;"""

assert old_tooltip_tri_end in text, "old_tooltip_tri_end not found!"
text = text.replace(old_tooltip_tri_end, new_tooltip_tri_end, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(text)

with open(brain_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully injected B, S, X trade markers logic into top10_5min_equity_curves.html and brain artifact!")
