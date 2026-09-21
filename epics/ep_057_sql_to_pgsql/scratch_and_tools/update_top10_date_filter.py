import json

json_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\top10_by_date_equity_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    data_json = f.read()

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Top 10 Strategy Models 5-Minute Continuous Equity Curves</title>
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
      min-width: 240px;
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
      opacity: 0.30;
    }
    .date-pill {
      transition: all 0.15s ease-in-out;
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
            5-Minute Snapshot Telemetry
          </span>
          <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white font-mono">
            Top 10 Models Equity Curves
          </h1>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          High-resolution 5-minute snapshot progression filtered by trading date (PostgreSQL <code class="text-sky-300 font-mono">tbl_dna_model_summary_snapshots_5min</code>)
        </p>
      </div>

      <!-- Date Switcher & Actions -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- Date Selector Pills -->
        <div class="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800" id="dateTabsContainer"></div>

        <!-- Quick Visibility Actions -->
        <div class="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-800">
          <button id="selectAllBtn" class="px-2.5 py-1 text-xs font-semibold rounded bg-sky-600 text-white transition hover:bg-sky-500">
            Show All 10
          </button>
          <button id="isolateTop1Btn" class="px-2.5 py-1 text-xs font-semibold rounded bg-slate-800 text-slate-300 hover:text-white transition">
            Isolate #1
          </button>
        </div>
      </div>
    </div>

    <!-- Active Window Sub-Header -->
    <div class="mt-3 px-1 flex items-center justify-between text-xs font-mono text-slate-400">
      <div class="flex items-center gap-2">
        <span>Active Date Window:</span>
        <span class="text-sky-400 font-bold" id="activeDateLabel">Full Week (Sep 14–18)</span>
        <span class="text-slate-500">&bull; Total Session Models: 10</span>
      </div>
      <div class="text-[11px] text-slate-500 hidden sm:inline">
        Hover / scrub over chart to inspect snapshot values at any timestamp
      </div>
    </div>

    <!-- Canvas Chart Card -->
    <div class="mt-3 p-3 bg-slate-950/70 rounded-xl border border-slate-800/80 relative">
      <div class="chart-container">
        <canvas id="top10Canvas"></canvas>
        <div id="tooltip" class="tooltip-box"></div>
      </div>

      <!-- Chart Footer Legend & Info -->
      <div class="flex flex-wrap items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800/70 mt-2 font-mono">
        <div class="flex items-center gap-4">
          <span class="text-slate-300">Click any card below to toggle line visibility or isolate specific curves</span>
        </div>
        <div class="text-[11px] text-slate-500">
          5-Minute Intervals &bull; Continuous Trajectory &bull; Directional Real-Time Engine
        </div>
      </div>
    </div>

    <!-- Interactive Top 10 Model Cards / Selectors -->
    <div class="mt-4">
      <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between font-mono">
        <span id="cardsGridTitle">Top 10 Models for Selected Window</span>
        <span class="text-[10px] text-slate-500 font-normal">Ranked by Total Cumulative Net P&L</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2.5" id="modelCardsContainer"></div>
    </div>

  </div>

  <script>
    const ALL_DATE_DATA = __DATA_JSON_PLACEHOLDER__;

    let currentDate = 'WEEK_OVERALL';
    let visibleModels = new Set();
    let highlightedModel = null;

    const availableDates = [
      { id: 'WEEK_OVERALL', label: 'Full Week' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' }
    ];

    const dateTabsContainer = document.getElementById('dateTabsContainer');
    const activeDateLabel = document.getElementById('activeDateLabel');
    const cardsGridTitle = document.getElementById('cardsGridTitle');
    const canvas = document.getElementById('top10Canvas');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('tooltip');
    const modelCardsContainer = document.getElementById('modelCardsContainer');

    const selectAllBtn = document.getElementById('selectAllBtn');
    const isolateTop1Btn = document.getElementById('isolateTop1Btn');

    function init() {
      setupDateTabs();
      setupEventListeners();
      switchDate(currentDate);
    }

    function setupDateTabs() {
      dateTabsContainer.innerHTML = '';
      availableDates.forEach(d => {
        const btn = document.createElement('button');
        btn.id = `tab_${d.id}`;
        btn.className = `date-pill px-2.5 py-1 text-xs font-bold font-mono rounded ${
          d.id === currentDate ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
        }`;
        btn.textContent = d.label;
        btn.onclick = () => switchDate(d.id);
        dateTabsContainer.appendChild(btn);
      });
    }

    function switchDate(dateKey) {
      currentDate = dateKey;
      const dObj = availableDates.find(d => d.id === dateKey);
      activeDateLabel.textContent = dObj ? (dObj.id === 'WEEK_OVERALL' ? 'Full Week (Sep 14–18)' : dObj.id) : dateKey;
      cardsGridTitle.textContent = `Top 10 Models for ${activeDateLabel.textContent}`;

      // Update pill classes
      availableDates.forEach(d => {
        const tab = document.getElementById(`tab_${d.id}`);
        if (tab) {
          tab.className = `date-pill px-2.5 py-1 text-xs font-bold font-mono rounded ${
            d.id === currentDate ? 'bg-sky-600 text-white shadow' : 'text-slate-400 hover:text-white'
          }`;
        }
      });

      const currentModels = ALL_DATE_DATA[currentDate] || [];
      visibleModels = new Set(currentModels.map(m => m.model));
      highlightedModel = null;

      renderCards();
      drawChart();
    }

    function setupEventListeners() {
      selectAllBtn.onclick = () => {
        const currentModels = ALL_DATE_DATA[currentDate] || [];
        visibleModels = new Set(currentModels.map(m => m.model));
        highlightedModel = null;
        renderCards();
        drawChart();
      };

      isolateTop1Btn.onclick = () => {
        const currentModels = ALL_DATE_DATA[currentDate] || [];
        if (currentModels.length) {
          visibleModels = new Set([currentModels[0].model]);
          highlightedModel = currentModels[0].model;
          renderCards();
          drawChart();
        }
      };

      window.addEventListener('resize', () => {
        drawChart();
      });
    }

    function renderCards() {
      modelCardsContainer.innerHTML = '';
      const currentModels = ALL_DATE_DATA[currentDate] || [];

      currentModels.forEach((m, idx) => {
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
              visibleModels = new Set(currentModels.map(x => x.model));
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
            <span class="font-black ${m.cum_net >= 0 ? 'text-emerald-400' : 'text-rose-400'}">
              ${m.cum_net >= 0 ? '+£' : '-£'}${Math.abs(m.cum_net).toFixed(0)}
            </span>
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

      const currentModels = ALL_DATE_DATA[currentDate] || [];
      const activeModels = currentModels.filter(m => visibleModels.has(m.model));
      if (!activeModels.length) {
        ctx.fillStyle = '#64748b';
        ctx.font = '13px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('All lines hidden. Click "Show All 10" or any card to display curves.', width / 2, height / 2);
        return;
      }

      const padLeft = 65;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 40;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

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

      // Render Active Model Curves
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

      timeAxisPoints = longestSeries.map((s, idx) => ({
        x: getX(idx),
        idx: idx,
        time: s.time
      }));
    }

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

        const currentModels = ALL_DATE_DATA[currentDate] || [];
        const activeModels = currentModels.filter(m => visibleModels.has(m.model));
        let rowsHtml = '';
        activeModels.slice(0, 7).forEach(m => {
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

full_html = template.replace("__DATA_JSON_PLACEHOLDER__", data_json)

# 1. Update primary brain artifact
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
with open(brain_path, "w", encoding="utf-8") as f:
    f.write(full_html)

# 2. Update epics artifact
epic_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(epic_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Updated top10_5min_equity_curves.html with Date Filter in both locations!")
