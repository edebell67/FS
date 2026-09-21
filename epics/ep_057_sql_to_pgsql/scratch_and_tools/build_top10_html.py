import json

json_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\top10_5min_equity_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    top10_json = f.read()

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Top 10 Strategy Models 5-Minute Continuous Equity Curves (Sep 14–18)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 16px;
      background-color: #080c14;
      color: #f1f5f9;
    }
    .chart-container {
      position: relative;
      width: 100%;
      height: 480px;
    }
    .tooltip-box {
      position: absolute;
      display: none;
      pointer-events: none;
      background: rgba(15, 23, 42, 0.96);
      border: 1px solid #475569;
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 11px;
      box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.7);
      z-index: 50;
      transform: translate(-50%, -105%);
      min-width: 230px;
      backdrop-filter: blur(8px);
    }
    .model-pill {
      transition: all 0.15s ease-in-out;
      cursor: pointer;
    }
    .model-pill:hover {
      background-color: rgba(30, 41, 59, 0.85);
    }
    .model-pill.active {
      border-color: #38bdf8;
      background-color: rgba(56, 189, 248, 0.14);
    }
    .model-pill.dimmed {
      opacity: 0.35;
    }
  </style>
</head>
<body class="p-3 sm:p-5 bg-slate-950 text-slate-100 antialiased min-h-screen">
  <div class="max-w-7xl mx-auto bg-slate-900/90 border border-slate-800 rounded-xl p-4 sm:p-6 shadow-2xl backdrop-blur-md">
    
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-4 pb-4 border-b border-slate-800">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            5-Minute Snapshot Engine
          </span>
          <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white font-mono">
            Top 10 Strategy Models Equity Curves
          </h1>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Continuous 5-minute snapshot progression across Sep 14–18, 2026 replayed sessions (PostgreSQL <code class="text-sky-300 font-mono">tbl_dna_model_summary_snapshots_5min</code>)
        </p>
      </div>

      <!-- Quick Action Controls -->
      <div class="flex items-center gap-2">
        <button id="selectAllBtn" class="px-2.5 py-1 text-xs font-semibold rounded bg-sky-600 text-white transition hover:bg-sky-500">
          Show All 10
        </button>
        <button id="isolateTop1Btn" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-800 text-slate-300 hover:text-white transition">
          Isolate #1
        </button>
      </div>
    </div>

    <!-- Canvas Chart Card -->
    <div class="mt-4 p-3 bg-slate-950/70 rounded-xl border border-slate-800/80 relative">
      <div class="chart-container">
        <canvas id="top10Canvas"></canvas>
        <div id="tooltip" class="tooltip-box"></div>
      </div>

      <!-- Chart Footer Legend & Info -->
      <div class="flex flex-wrap items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800/70 mt-2 font-mono">
        <div class="flex items-center gap-4">
          <span class="text-slate-300">Hover / scrub over chart to inspect snapshot values at any timestamp</span>
        </div>
        <div class="text-[11px] text-slate-500">
          5-Minute Intervals &bull; 1,440 Points / Day &bull; Continuous 5-Day Trajectory
        </div>
      </div>
    </div>

    <!-- Interactive Top 10 Model Cards / Selectors -->
    <div class="mt-4">
      <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between font-mono">
        <span>Top 10 Strategy Models by Total Net Return</span>
        <span class="text-[10px] text-slate-500 font-normal">Click card to isolate or toggle line visibility</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2.5" id="modelCardsContainer"></div>
    </div>

  </div>

  <script>
    const TOP10_DATA = __TOP10_JSON_PLACEHOLDER__;

    // Track active/visible models
    let visibleModels = new Set(TOP10_DATA.map(m => m.model));
    let highlightedModel = null;

    const canvas = document.getElementById('top10Canvas');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('tooltip');
    const modelCardsContainer = document.getElementById('modelCardsContainer');

    const selectAllBtn = document.getElementById('selectAllBtn');
    const isolateTop1Btn = document.getElementById('isolateTop1Btn');

    function init() {
      renderCards();
      setupEventListeners();
      drawChart();
    }

    function setupEventListeners() {
      selectAllBtn.onclick = () => {
        visibleModels = new Set(TOP10_DATA.map(m => m.model));
        highlightedModel = null;
        renderCards();
        drawChart();
      };

      isolateTop1Btn.onclick = () => {
        visibleModels = new Set([TOP10_DATA[0].model]);
        highlightedModel = TOP10_DATA[0].model;
        renderCards();
        drawChart();
      };

      window.addEventListener('resize', () => {
        drawChart();
      });
    }

    function renderCards() {
      modelCardsContainer.innerHTML = '';

      TOP10_DATA.forEach((m, idx) => {
        const card = document.createElement('div');
        const isVisible = visibleModels.has(m.model);
        const isHigh = highlightedModel === m.model;

        card.className = `model-pill p-2.5 rounded-lg border flex flex-col justify-between ${
          !isVisible ? 'dimmed border-slate-800 bg-slate-950/40' : (isHigh ? 'border-sky-400 bg-sky-500/15' : 'border-slate-800 bg-slate-950/80')
        }`;

        card.onclick = () => {
          if (visibleModels.has(m.model)) {
            if (visibleModels.size === 1) {
              // restore all
              visibleModels = new Set(TOP10_DATA.map(x => x.model));
              highlightedModel = null;
            } else {
              visibleModels.delete(m.model);
            }
          } else {
            visibleModels.add(m.model);
          }
          renderCards();
          drawChart();
        };

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between text-[11px] font-mono">
              <div class="flex items-center gap-1.5">
                <span class="w-2.5 h-2.5 rounded-full inline-block" style="background-color: ${m.color}"></span>
                <span class="font-black text-white">#${m.rank} ${m.model}</span>
              </div>
              <span class="text-[9px] uppercase font-bold px-1.5 py-0.5 rounded bg-slate-800 text-sky-300">${m.product}</span>
            </div>
            <div class="text-[10px] text-slate-400 font-mono truncate mt-1">${m.strategy.replace('breakout_', '')}</div>
          </div>
          <div class="mt-2 pt-1 border-t border-slate-800/80 flex items-center justify-between text-xs font-mono">
            <span class="text-slate-400">${m.trades} trds (${m.win_rate}%)</span>
            <span class="font-black text-emerald-400">+£${m.cum_net.toFixed(0)}</span>
          </div>
        `;

        modelCardsContainer.appendChild(card);
      });
    }

    function setupCanvas() {
      const dpr = window.devicePixelRatio || 1;
      const rect = canvas.parentElement.getBoundingClientRect();
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;
      ctx.scale(dpr, dpr);
      canvas.style.width = `${rect.width}px`;
      canvas.style.height = `${rect.height}px`;
    }

    let timeAxisPoints = [];

    function drawChart() {
      setupCanvas();
      const rect = canvas.parentElement.getBoundingClientRect();
      const width = rect.width;
      const height = rect.height;

      ctx.clearRect(0, 0, width, height);

      const activeModels = TOP10_DATA.filter(m => visibleModels.has(m.model));
      if (!activeModels.length) {
        ctx.fillStyle = '#64748b';
        ctx.font = '13px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('All lines hidden. Click "Show All 10" or any card to display equity curves.', width / 2, height / 2);
        return;
      }

      const padLeft = 65;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 40;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      // Calculate global min and max among active models
      let allNets = [];
      activeModels.forEach(m => {
        m.series.forEach(pt => allNets.push(pt.net));
      });

      let minVal = Math.min(0, ...allNets);
      let maxVal = Math.max(0, ...allNets);
      if (minVal === maxVal) { minVal -= 50; maxVal += 50; }

      const span = maxVal - minVal;
      minVal -= span * 0.06;
      maxVal += span * 0.06;

      const longestSeries = activeModels.reduce((max, m) => m.series.length > max.series.length ? m : max, activeModels[0]).series;

      const getY = val => padTop + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
      const getX = idx => padLeft + (idx / (longestSeries.length - 1 || 1)) * plotW;

      // Grid Lines & Y-Axis Labels
      ctx.lineWidth = 1;
      const gridSteps = 6;
      for (let i = 0; i <= gridSteps; i++) {
        const v = minVal + (i / gridSteps) * (maxVal - minVal);
        const y = getY(v);

        ctx.strokeStyle = Math.abs(v) < 1 ? '#475569' : '#1e293b';
        ctx.setLineDash(Math.abs(v) < 1 ? [] : [4, 4]);
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(width - padRight, y);
        ctx.stroke();

        ctx.setLineDash([]);
        ctx.fillStyle = Math.abs(v) < 1 ? '#94a3b8' : '#64748b';
        ctx.font = '10px monospace';
        ctx.textAlign = 'right';
        ctx.fillText(`£${v.toFixed(0)}`, padLeft - 10, y + 3);
      }

      // Zero baseline
      const zeroY = getY(0);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(padLeft, zeroY);
      ctx.lineTo(width - padRight, zeroY);
      ctx.stroke();

      // X-Axis Time Labels
      const labelInterval = Math.max(1, Math.floor(longestSeries.length / 8));
      ctx.fillStyle = '#64748b';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';

      for (let i = 0; i < longestSeries.length; i += labelInterval) {
        const x = getX(i);
        ctx.fillText(longestSeries[i].time, x, height - padBottom + 18);
        ctx.strokeStyle = '#1e293b';
        ctx.beginPath();
        ctx.moveTo(x, padTop);
        ctx.lineTo(x, height - padBottom);
        ctx.stroke();
      }

      // Render Each Active Model's Equity Curve
      activeModels.forEach(m => {
        const isHighlight = highlightedModel === m.model;
        ctx.lineWidth = isHighlight ? 3.5 : 2.0;
        ctx.strokeStyle = m.color;
        ctx.beginPath();

        m.series.forEach((pt, idx) => {
          const x = getX(idx);
          const y = getY(pt.net);
          if (idx === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();

        // End Label
        if (m.series.length) {
          const lastIdx = m.series.length - 1;
          const endX = getX(lastIdx);
          const endY = getY(m.series[lastIdx].net);

          ctx.fillStyle = m.color;
          ctx.beginPath();
          ctx.arc(endX, endY, isHighlight ? 4.5 : 3, 0, Math.PI * 2);
          ctx.fill();

          ctx.font = 'bold 9px monospace';
          ctx.textAlign = 'left';
          ctx.fillText(`+£${m.cum_net.toFixed(0)}`, endX + 6, endY + 3);
        }
      });

      // Save time index points for mouse hover
      timeAxisPoints = longestSeries.map((s, idx) => ({
        x: getX(idx),
        idx: idx,
        time: s.time
      }));
    }

    // Hover tooltip
    canvas.addEventListener('mousemove', e => {
      if (!timeAxisPoints.length) return;
      const rect = canvas.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      let closest = timeAxisPoints[0];
      let minD = 999999;
      timeAxisPoints.forEach(p => {
        const d = Math.abs(p.x - mouseX);
        if (d < minD) {
          minD = d;
          closest = p;
        }
      });

      if (minD < 35) {
        tooltip.style.display = 'block';
        tooltip.style.left = `${closest.x}px`;
        tooltip.style.top = `${mouseY}px`;

        const activeModels = TOP10_DATA.filter(m => visibleModels.has(m.model));
        let rowsHtml = '';
        activeModels.slice(0, 6).forEach(m => {
          const pt = m.series[closest.idx] || m.series[m.series.length - 1];
          rowsHtml += `
            <div class="flex justify-between items-center text-[10px] font-mono py-0.5">
              <span class="flex items-center gap-1">
                <span class="w-2 h-2 rounded-full inline-block" style="background:${m.color}"></span>
                <span class="text-slate-300 font-bold">${m.model}</span>
              </span>
              <span class="font-bold ${pt.net >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${pt.net.toFixed(0)}</span>
            </div>
          `;
        });

        tooltip.innerHTML = `
          <div class="font-mono font-bold text-white border-b border-slate-700 pb-1 mb-1.5 flex justify-between">
            <span>Snapshot: ${closest.time}</span>
          </div>
          <div class="space-y-0.5">
            ${rowsHtml}
          </div>
        `;
      } else {
        tooltip.style.display = 'none';
      }
    });

    canvas.addEventListener('mouseleave', () => {
      tooltip.style.display = 'none';
    });

    init();
  </script>
</body>
</html>
"""

full_top10_html = template.replace("__TOP10_JSON_PLACEHOLDER__", top10_json)
target_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(full_top10_html)

print("Generated top10_5min_equity_curves.html successfully! File size:", len(full_top10_html))
