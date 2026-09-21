import json

json_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\top10_by_date_equity_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    data_json = f.read()

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Top 10 Strategy Models - Directional Split & Baseline Delta Initializer</title>
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
      min-width: 250px;
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
            5-Min Snapshot Directional Split
          </span>
          <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white font-mono">
            Top 10 Models: Directional Split & Baseline Initializer
          </h1>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Inspect Total Net, <span class="text-sky-400 font-semibold">Cum Buy Net (Longs)</span>, and <span class="text-amber-400 font-semibold">Cum Sell Net (Shorts)</span> &bull; Tap chart to re-center curves from any timestamp
        </p>
      </div>

      <!-- Controls (Date Selector & Split Metric Mode) -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- Date Selector Pills -->
        <div class="flex items-center bg-slate-950 p-1 rounded-lg border border-slate-800" id="dateTabsContainer"></div>

        <!-- Directional Split Mode Selector -->
        <div class="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-slate-800 font-mono text-xs">
          <button id="metricAll" class="px-2.5 py-1 font-semibold rounded bg-sky-600 text-white transition">
            Total Net (All 10)
          </button>
          <button id="metricBuy" class="px-2.5 py-1 font-semibold rounded text-slate-400 hover:text-white transition">
            Cum Buy Net
          </button>
          <button id="metricSell" class="px-2.5 py-1 font-semibold rounded text-slate-400 hover:text-white transition">
            Cum Sell Net
          </button>
          <button id="metricTriSplit" class="px-2.5 py-1 font-semibold rounded text-purple-400 hover:text-white transition">
            Tri-Split (Single Model)
          </button>
        </div>
      </div>
    </div>

    <!-- Active Ribbon Inspector with Baseline Controls -->
    <div class="mt-3 p-3 bg-slate-950/70 border border-slate-800 rounded-xl flex flex-wrap items-center justify-between gap-3 font-mono">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-10 rounded-full bg-sky-500" id="indicatorBar"></div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-base sm:text-lg font-black text-white" id="ribbonModelName">Top 10 Aggregate View</span>
            <span class="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-slate-800 text-sky-300" id="ribbonProduct">ALL</span>
            <span class="text-xs text-slate-400 hidden sm:inline" id="ribbonStrategy">Mode: Total Net Curves</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5 flex flex-wrap items-center gap-2" id="ribbonSubtitle">
            <span>Window: <b class="text-sky-300" id="activeDateLabel">Full Week</b></span>
            <span>&bull; Baseline Point: <b class="text-amber-400" id="baselineDisplayBadge">Session Open (00:00)</b></span>
            <button id="resetBaselineBtn" title="Reset baseline to session start" class="text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border border-amber-500/30 transition">
              ↺ Reset to Start
            </button>
          </div>
        </div>
      </div>

      <!-- Financial Metric Display (Shows Delta relative to baseline) -->
      <div class="flex items-center gap-5 text-right">
        <div>
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
        </div>
      </div>
    </div>

    <!-- Canvas Chart Card -->
    <div class="mt-3 p-3 bg-slate-950/80 rounded-xl border border-slate-800/80 relative">
      <div class="chart-container">
        <canvas id="top10Canvas"></canvas>
        <div id="tooltip" class="tooltip-box"></div>
      </div>

      <!-- Chart Footer Legend & Baseline Instructions -->
      <div class="flex flex-wrap items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800/70 mt-2 font-mono">
        <div class="flex items-center gap-4" id="chartLegend">
          <span class="text-slate-300">Displaying: Multi-model Total Net curves</span>
        </div>
        <div class="text-[11px] text-amber-300/90 flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
          <span>Tip: <b>Click anywhere on the chart</b> to set a baseline (e.g. 03:00) and show changes since then</span>
        </div>
      </div>
    </div>

    <!-- Interactive Top 10 Model Cards / Selectors -->
    <div class="mt-4">
      <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between font-mono">
        <span id="cardsGridTitle">Top 10 Models for Selected Window</span>
        <span class="text-[10px] text-slate-500 font-normal">Click a card to inspect its Buy vs Sell split</span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-2.5" id="modelCardsContainer"></div>
    </div>

  </div>

  <script>
    const ALL_DATE_DATA = __DATA_JSON_PLACEHOLDER__;

    let currentDate = 'WEEK_OVERALL';
    let splitMode = 'ALL_NET'; // 'ALL_NET', 'BUY_NET', 'SELL_NET', 'TRI_SPLIT'
    let selectedModelIndex = 0; // for TRI_SPLIT mode
    let baselineFrameIndex = 0; // 0 means session start
    let visibleModels = new Set();

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
    const chartLegend = document.getElementById('chartLegend');

    const metricAll = document.getElementById('metricAll');
    const metricBuy = document.getElementById('metricBuy');
    const metricSell = document.getElementById('metricSell');
    const metricTriSplit = document.getElementById('metricTriSplit');

    const ribbonModelName = document.getElementById('ribbonModelName');
    const ribbonProduct = document.getElementById('ribbonProduct');
    const ribbonStrategy = document.getElementById('ribbonStrategy');
    const ribbonTotNet = document.getElementById('ribbonTotNet');
    const ribbonBuyNet = document.getElementById('ribbonBuyNet');
    const ribbonSellNet = document.getElementById('ribbonSellNet');
    const totalNetLabel = document.getElementById('totalNetLabel');
    const buyNetLabel = document.getElementById('buyNetLabel');
    const sellNetLabel = document.getElementById('sellNetLabel');
    const indicatorBar = document.getElementById('indicatorBar');
    const baselineDisplayBadge = document.getElementById('baselineDisplayBadge');
    const resetBaselineBtn = document.getElementById('resetBaselineBtn');

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

    function setSplitMode(mode) {
      splitMode = mode;
      [metricAll, metricBuy, metricSell, metricTriSplit].forEach(b => {
        b.className = 'px-2.5 py-1 font-semibold rounded text-slate-400 hover:text-white transition';
      });

      if (mode === 'ALL_NET') metricAll.className = 'px-2.5 py-1 font-semibold rounded bg-sky-600 text-white transition';
      if (mode === 'BUY_NET') metricBuy.className = 'px-2.5 py-1 font-semibold rounded bg-sky-500 text-white transition';
      if (mode === 'SELL_NET') metricSell.className = 'px-2.5 py-1 font-semibold rounded bg-amber-500 text-white transition';
      if (mode === 'TRI_SPLIT') metricTriSplit.className = 'px-2.5 py-1 font-semibold rounded bg-purple-600 text-white transition';

      updateRibbon();
      renderCards();
      drawChart();
    }

    function switchDate(dateKey) {
      currentDate = dateKey;
      baselineFrameIndex = 0; // reset baseline when switching date
      const dObj = availableDates.find(d => d.id === dateKey);
      activeDateLabel.textContent = dObj ? (dObj.id === 'WEEK_OVERALL' ? 'Full Week (Sep 14–18)' : dObj.id) : dateKey;
      cardsGridTitle.textContent = `Top 10 Models for ${activeDateLabel.textContent}`;

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
      selectedModelIndex = 0;

      updateRibbon();
      renderCards();
      drawChart();
    }

    function setupEventListeners() {
      metricAll.onclick = () => setSplitMode('ALL_NET');
      metricBuy.onclick = () => setSplitMode('BUY_NET');
      metricSell.onclick = () => setSplitMode('SELL_NET');
      metricTriSplit.onclick = () => setSplitMode('TRI_SPLIT');

      resetBaselineBtn.onclick = () => {
        baselineFrameIndex = 0;
        updateRibbon();
        renderCards();
        drawChart();
      };

      // Click on canvas to set baseline
      canvas.addEventListener('click', e => {
        const currentModels = ALL_DATE_DATA[currentDate] || [];
        if (!currentModels.length) return;

        const longestSeries = currentModels.reduce((max, m) => m.series.length > max.series.length ? m : max, currentModels[0]).series;
        if (!longestSeries.length) return;

        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const padLeft = 65;
        const padRight = 30;
        const plotW = rect.width - padLeft - padRight;
        if (plotW <= 0) return;

        let pct = (clickX - padLeft) / plotW;
        pct = Math.max(0, Math.min(1, pct));

        baselineFrameIndex = Math.round(pct * (longestSeries.length - 1));
        updateRibbon();
        renderCards();
        drawChart();
      });

      window.addEventListener('resize', () => {
        drawChart();
      });
    }

    function getBasePoint(series) {
      if (!series || !series.length) return { net: 0, buy: 0, sell: 0, time: '00:00' };
      const idx = Math.min(baselineFrameIndex, series.length - 1);
      return series[idx];
    }

    function updateRibbon() {
      const currentModels = ALL_DATE_DATA[currentDate] || [];
      if (!currentModels.length) return;

      const longestSeries = currentModels.reduce((max, m) => m.series.length > max.series.length ? m : max, currentModels[0]).series;
      const baseTime = longestSeries[Math.min(baselineFrameIndex, longestSeries.length - 1)].time;

      if (baselineFrameIndex === 0) {
        baselineDisplayBadge.textContent = `Session Start (${baseTime})`;
        totalNetLabel.textContent = 'Total Net';
        buyNetLabel.textContent = 'Cum Buy Net';
        sellNetLabel.textContent = 'Cum Sell Net';
      } else {
        baselineDisplayBadge.textContent = `Baseline: ${baseTime}`;
        totalNetLabel.textContent = `Δ Net since ${baseTime}`;
        buyNetLabel.textContent = `Δ Buy since ${baseTime}`;
        sellNetLabel.textContent = `Δ Sell since ${baseTime}`;
      }

      const fmt = (v) => (v >= 0 ? '+£' : '-£') + Math.abs(v).toFixed(2);

      if (splitMode === 'TRI_SPLIT') {
        const m = currentModels[selectedModelIndex] || currentModels[0];
        const basePt = getBasePoint(m.series);
        const lastPt = m.series[m.series.length - 1] || basePt;

        const deltaNet = lastPt.net - basePt.net;
        const deltaBuy = lastPt.buy - basePt.buy;
        const deltaSell = lastPt.sell - basePt.sell;

        ribbonModelName.textContent = `#${m.rank} ${m.model}`;
        ribbonProduct.textContent = m.product;
        ribbonStrategy.textContent = m.strategy;
        indicatorBar.style.backgroundColor = m.color;

        ribbonTotNet.textContent = fmt(deltaNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${deltaNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}`;

        ribbonBuyNet.textContent = fmt(deltaBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${deltaBuy >= 0 ? 'text-sky-400' : 'text-rose-400'}`;

        ribbonSellNet.textContent = fmt(deltaSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${deltaSell >= 0 ? 'text-amber-400' : 'text-rose-400'}`;
      } else {
        let totNet = 0, totBuy = 0, totSell = 0;
        currentModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          const lastPt = m.series[m.series.length - 1] || basePt;
          totNet += (lastPt.net - basePt.net);
          totBuy += (lastPt.buy - basePt.buy);
          totSell += (lastPt.sell - basePt.sell);
        });

        ribbonModelName.textContent = 'Top 10 Group View';
        ribbonProduct.textContent = 'ALL';
        ribbonStrategy.textContent = splitMode === 'ALL_NET' ? 'Mode: Total Net Curves' : (splitMode === 'BUY_NET' ? 'Mode: Cum Buy Net (Longs)' : 'Mode: Cum Sell Net (Shorts)');
        indicatorBar.style.backgroundColor = '#38bdf8';

        ribbonTotNet.textContent = fmt(totNet);
        ribbonTotNet.className = `text-base sm:text-lg font-black ${totNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}`;

        ribbonBuyNet.textContent = fmt(totBuy);
        ribbonBuyNet.className = `text-xs sm:text-sm font-bold ${totBuy >= 0 ? 'text-sky-400' : 'text-rose-400'}`;

        ribbonSellNet.textContent = fmt(totSell);
        ribbonSellNet.className = `text-xs sm:text-sm font-bold ${totSell >= 0 ? 'text-amber-400' : 'text-rose-400'}`;
      }
    }

    function renderCards() {
      modelCardsContainer.innerHTML = '';
      const currentModels = ALL_DATE_DATA[currentDate] || [];

      currentModels.forEach((m, idx) => {
        const card = document.createElement('div');
        const isTri = splitMode === 'TRI_SPLIT';
        const isSelected = isTri && idx === selectedModelIndex;
        const isVisible = isTri ? isSelected : visibleModels.has(m.model);

        const basePt = getBasePoint(m.series);
        const lastPt = m.series[m.series.length - 1] || basePt;
        const deltaNet = lastPt.net - basePt.net;
        const deltaBuy = lastPt.buy - basePt.buy;
        const deltaSell = lastPt.sell - basePt.sell;

        card.className = `model-pill p-2.5 rounded-lg border flex flex-col justify-between ${
          isSelected 
            ? 'border-purple-500 bg-purple-500/15' 
            : (!isVisible ? 'dimmed border-slate-800 bg-slate-950/40' : 'border-slate-800 bg-slate-950/80')
        }`;

        card.onclick = () => {
          if (splitMode === 'TRI_SPLIT') {
            selectedModelIndex = idx;
            updateRibbon();
            renderCards();
            drawChart();
          } else {
            if (visibleModels.has(m.model)) {
              if (visibleModels.size === 1) {
                visibleModels = new Set(currentModels.map(x => x.model));
              } else {
                visibleModels.delete(m.model);
              }
            } else {
              visibleModels.add(m.model);
            }
            renderCards();
            drawChart();
          }
        };

        const fmt = (v) => (v >= 0 ? '+£' : '-£') + Math.abs(v).toFixed(0);

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
            <div class="text-[10px] text-slate-400 font-mono mt-0.5">
              ${m.trades} trades &bull; <b class="text-slate-300">${m.win_rate}% win</b>
            </div>
          </div>
          <div class="mt-2 pt-1 border-t border-slate-800/80 flex items-center justify-between text-[11px] font-mono">
            <span class="${deltaNet >= 0 ? 'text-emerald-400' : 'text-rose-400'} font-bold">Δ ${fmt(deltaNet)}</span>
            <span class="text-[10px] text-slate-400">
              <b class="text-sky-400">B:${fmt(deltaBuy)}</b> <b class="text-amber-400">S:${fmt(deltaSell)}</b>
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
      if (!currentModels.length) return;

      const padLeft = 65;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 40;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      const longestSeries = currentModels.reduce((max, m) => m.series.length > max.series.length ? m : max, currentModels[0]).series;
      const baseTime = longestSeries[Math.min(baselineFrameIndex, longestSeries.length - 1)].time;

      if (splitMode === 'TRI_SPLIT') {
        const m = currentModels[selectedModelIndex] || currentModels[0];
        const basePt = getBasePoint(m.series);

        chartLegend.innerHTML = `
          <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-emerald-400 inline-block"></span><span class="text-emerald-300 font-bold">Δ Total Net</span></span>
          <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-sky-400 inline-block"></span><span class="text-sky-300 font-bold">Δ Cum Buy Net</span></span>
          <span class="flex items-center gap-1.5"><span class="w-3 h-0.5 bg-amber-400 inline-block"></span><span class="text-amber-300 font-bold">Δ Cum Sell Net</span></span>
        `;

        let deltas = [];
        m.series.forEach(pt => {
          deltas.push(pt.net - basePt.net, pt.buy - basePt.buy, pt.sell - basePt.sell);
        });

        let minVal = Math.min(0, ...deltas);
        let maxVal = Math.max(0, ...deltas);
        if (minVal === maxVal) { minVal -= 50; maxVal += 50; }

        const span = maxVal - minVal;
        minVal -= span * 0.08;
        maxVal += span * 0.08;

        const getY = val => padTop + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
        const getX = idx => padLeft + (idx / (m.series.length - 1 || 1)) * plotW;

        drawGridAndAxes(width, height, padLeft, padRight, padTop, padBottom, plotW, plotH, minVal, maxVal, m.series, getY, getX);

        // Draw Baseline Vertical Marker if set
        if (baselineFrameIndex > 0) {
          const bX = getX(Math.min(baselineFrameIndex, m.series.length - 1));
          drawBaselineMarker(bX, padTop, height - padBottom, baseTime);
        }

        renderDeltaLine(m.series, 'buy', basePt.buy, '#38bdf8', 2.2, [4, 3], getX, getY);
        renderDeltaLine(m.series, 'sell', basePt.sell, '#fbbf24', 2.2, [4, 3], getX, getY);
        renderDeltaLine(m.series, 'net', basePt.net, '#34d399', 3.0, [], getX, getY);

        const lastIdx = m.series.length - 1;
        const lastPt = m.series[lastIdx];
        drawPointLabel(getX(lastIdx), getY(lastPt.net - basePt.net), `Net: £${(lastPt.net - basePt.net).toFixed(0)}`, '#34d399');
        drawPointLabel(getX(lastIdx), getY(lastPt.buy - basePt.buy), `Buy: £${(lastPt.buy - basePt.buy).toFixed(0)}`, '#38bdf8');
        drawPointLabel(getX(lastIdx), getY(lastPt.sell - basePt.sell), `Sell: £${(lastPt.sell - basePt.sell).toFixed(0)}`, '#fbbf24');

        timeAxisPoints = m.series.map((s, idx) => ({
          x: getX(idx),
          idx: idx,
          time: s.time,
          data: s
        }));

      } else {
        const metricKey = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');
        const metricName = splitMode === 'BUY_NET' ? 'Cum Buy Net (Longs)' : (splitMode === 'SELL_NET' ? 'Cum Sell Net (Shorts)' : 'Total Net');
        chartLegend.innerHTML = `<span>Displaying: <strong class="text-white">Δ ${metricName}</strong> relative to <b>${baseTime}</b></span>`;

        const activeModels = currentModels.filter(m => visibleModels.has(m.model));
        if (!activeModels.length) {
          ctx.fillStyle = '#64748b';
          ctx.font = '13px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('All lines hidden. Select models below to display curves.', width / 2, height / 2);
          return;
        }

        let allDeltas = [];
        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          m.series.forEach(pt => allDeltas.push(pt[metricKey] - basePt[metricKey]));
        });

        let minVal = Math.min(0, ...allDeltas);
        let maxVal = Math.max(0, ...allDeltas);
        if (minVal === maxVal) { minVal -= 50; maxVal += 50; }

        const span = maxVal - minVal;
        minVal -= span * 0.08;
        maxVal += span * 0.08;

        const getY = val => padTop + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
        const getX = idx => padLeft + (idx / (longestSeries.length - 1 || 1)) * plotW;

        drawGridAndAxes(width, height, padLeft, padRight, padTop, padBottom, plotW, plotH, minVal, maxVal, longestSeries, getY, getX);

        if (baselineFrameIndex > 0) {
          const bX = getX(Math.min(baselineFrameIndex, longestSeries.length - 1));
          drawBaselineMarker(bX, padTop, height - padBottom, baseTime);
        }

        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          renderDeltaLine(m.series, metricKey, basePt[metricKey], m.color, 2.2, [], getX, getY);
          if (m.series.length) {
            const lastIdx = m.series.length - 1;
            const deltaVal = m.series[lastIdx][metricKey] - basePt[metricKey];
            drawPointLabel(getX(lastIdx), getY(deltaVal), `${m.model} (£${deltaVal.toFixed(0)})`, m.color);
          }
        });

        timeAxisPoints = longestSeries.map((s, idx) => ({
          x: getX(idx),
          idx: idx,
          time: s.time
        }));
      }
    }

    function drawBaselineMarker(x, yTop, yBottom, timeStr) {
      ctx.strokeStyle = '#f59e0b';
      ctx.lineWidth = 1.8;
      ctx.setLineDash([5, 3]);
      ctx.beginPath();
      ctx.moveTo(x, yTop);
      ctx.lineTo(x, yBottom);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#f59e0b';
      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`BASE: ${timeStr}`, x, yTop - 8);
    }

    function renderDeltaLine(series, key, baseVal, color, lineWidth, dash, getX, getY) {
      ctx.lineWidth = lineWidth;
      ctx.strokeStyle = color;
      ctx.setLineDash(dash);
      ctx.beginPath();
      series.forEach((pt, idx) => {
        const delta = pt[key] - baseVal;
        const x = getX(idx);
        const y = getY(delta);
        if (idx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.stroke();
      ctx.setLineDash([]);
    }

    function drawPointLabel(x, y, text, color) {
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, 3.5, 0, Math.PI * 2);
      ctx.fill();

      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'left';
      ctx.fillText(text, x + 6, y + 3);
    }

    function drawGridAndAxes(width, height, padLeft, padRight, padTop, padBottom, plotW, plotH, minVal, maxVal, series, getY, getX) {
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
      const labelInterval = Math.max(1, Math.floor(series.length / 8));
      ctx.fillStyle = '#64748b';
      ctx.font = '10px monospace';
      ctx.textAlign = 'center';

      for (let i = 0; i < series.length; i += labelInterval) {
        const x = getX(i);
        ctx.fillText(series[i].time, x, height - padBottom + 18);
        ctx.strokeStyle = '#1e293b';
        ctx.beginPath();
        ctx.moveTo(x, padTop);
        ctx.lineTo(x, height - padBottom);
        ctx.stroke();
      }
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

        const currentModels = ALL_DATE_DATA[currentDate] || [];

        if (splitMode === 'TRI_SPLIT') {
          const m = currentModels[selectedModelIndex] || currentModels[0];
          const basePt = getBasePoint(m.series);
          const pt = m.series[closest.idx] || m.series[m.series.length - 1];

          const dNet = pt.net - basePt.net;
          const dBuy = pt.buy - basePt.buy;
          const dSell = pt.sell - basePt.sell;

          tooltip.innerHTML = `
            <div class="font-mono font-bold text-white border-b border-slate-700 pb-1 mb-1.5 flex justify-between">
              <span>${closest.time}</span>
              <span class="text-sky-300 font-bold">${m.model}</span>
            </div>
            <div class="space-y-1 font-mono text-[11px]">
              <div class="flex justify-between">
                <span class="text-emerald-400 font-semibold">Δ Total Net:</span>
                <span class="font-bold ${dNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dNet.toFixed(2)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-sky-400 font-semibold">Δ Buy Net:</span>
                <span class="font-bold ${dBuy >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dBuy.toFixed(2)}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-amber-400 font-semibold">Δ Sell Net:</span>
                <span class="font-bold ${dSell >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dSell.toFixed(2)}</span>
              </div>
              <div class="flex justify-between border-t border-slate-800 pt-1 text-[10px] text-slate-400">
                <span>Trades / Open:</span>
                <span class="text-slate-300 font-bold">${pt.trades} / ${pt.open}</span>
              </div>
            </div>
          `;
        } else {
          const metricKey = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');
          const activeModels = currentModels.filter(m => visibleModels.has(m.model));
          let rowsHtml = '';
          activeModels.slice(0, 7).forEach(m => {
            const basePt = getBasePoint(m.series);
            const pt = m.series[closest.idx] || m.series[m.series.length - 1];
            const dVal = pt[metricKey] - basePt[metricKey];
            rowsHtml += `
              <div class="flex justify-between items-center text-[10px] font-mono py-0.5">
                <span class="flex items-center gap-1">
                  <span class="w-2 h-2 rounded-full inline-block" style="background:${m.color}"></span>
                  <span class="text-slate-300 font-bold">${m.model}</span>
                </span>
                <span class="font-bold ${dVal >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dVal.toFixed(0)}</span>
              </div>
            `;
          });

          tooltip.innerHTML = `
            <div class="font-mono font-bold text-white border-b border-slate-700 pb-1 mb-1.5 flex justify-between">
              <span>Snapshot: ${closest.time}</span>
              <span class="text-slate-400 uppercase text-[9px]">${splitMode.replace('_', ' ')}</span>
            </div>
            <div class="space-y-0.5">
              ${rowsHtml}
            </div>
          `;
        }
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

# Update in brain
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
with open(brain_path, "w", encoding="utf-8") as f:
    f.write(full_html)

# Update in epic
epic_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(epic_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Updated top10_5min_equity_curves.html with Baseline Reset in both locations!")
