import json
import os

json_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\top10_by_date_equity_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    data_json = f.read()

template = """<!DOCTYPE html>
<!--
 * top10_5min_equity_curves.html — Top 10 Strategy Models: 5-Min Directional Split, Replay from Baseline, Baseline Initializer & Delta Hiding
 *
 * VERSION HISTORY
 * v1.5.0 · 2026-09-20 · [V20260920_1640] When a baseline is set at a specific point, replay playback starts directly from that point forward; dynamic rewind/restart to baseline; preserves all existing features.
 * v1.4.0 · 2026-09-20 · [V20260920_1615] Appends full Replay Mode (Play/Pause, Step ±5m, Speeds 1x/3x/10x, Scrubber Bar) and Win Rate threshold filter while preserving all directional splits, baseline initialization, delta hiding, and model visibility controls.
 * v1.3.0 · 2026-09-20 · Adds independent Net Delta, Buy Delta, and Sell Delta line hiding toggles.
 * v1.2.0 · 2026-09-20 · Adds individual model curve hiding toggles and Show/Hide All controls.
 * v1.1.0 · 2026-09-20 · Adds dynamic baseline re-centering from arbitrary timestamps.
 * v1.0.0 · 2026-09-20 · Initial version with 5-minute snapshot progression and date filtering.
-->
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Top 10 Strategy Models - Replay from Baseline, Directional Split & Baseline Initializer</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 12px;
      background-color: #080c14;
      color: #f1f5f9;
      -webkit-tap-highlight-color: transparent;
    }
    .chart-container {
      position: relative;
      width: 100%;
      height: 480px;
    }
    @media (max-width: 640px) {
      .chart-container {
        height: 360px;
      }
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
      opacity: 0.35;
      border-style: dashed;
    }
    .date-pill {
      transition: all 0.15s ease-in-out;
    }
    .eye-toggle-btn:hover {
      background-color: rgba(255, 255, 255, 0.15);
    }
    .delta-toggle-btn {
      transition: all 0.15s ease-in-out;
      user-select: none;
    }
    .delta-toggle-btn.off {
      opacity: 0.35;
      border-style: dashed !important;
      text-decoration: line-through;
    }
    /* Replay Scrubber Track */
    .scrubber-track {
      position: relative;
      width: 100%;
      height: 10px;
      border-radius: 9999px;
      background: #1e293b;
      cursor: pointer;
    }
    .scrubber-fill {
      position: absolute;
      top: 0;
      left: 0;
      height: 100%;
      border-radius: 9999px;
      background: linear-gradient(90deg, #0284c7, #38bdf8);
      pointer-events: none;
    }
    .scrubber-thumb {
      position: absolute;
      top: 50%;
      transform: translate(-50%, -50%);
      width: 18px;
      height: 18px;
      border-radius: 9999px;
      background: #ffffff;
      border: 3px solid #0284c7;
      box-shadow: 0 0 10px rgba(56, 189, 248, 0.8);
      pointer-events: none;
      transition: transform 0.05s ease;
    }
    .baseline-marker {
      position: absolute;
      top: -4px;
      bottom: -4px;
      width: 3px;
      background: #f59e0b;
      box-shadow: 0 0 8px #f59e0b;
      z-index: 20;
      pointer-events: none;
    }
    .baseline-badge {
      position: absolute;
      bottom: -22px;
      transform: translateX(-50%);
      font-size: 9px;
      font-weight: 700;
      background: #f59e0b;
      color: #000;
      padding: 1px 4px;
      border-radius: 4px;
      white-space: nowrap;
      pointer-events: none;
    }
    .custom-range {
      accent-color: #38bdf8;
    }
  </style>
</head>
<body class="p-2 sm:p-4 bg-slate-950 text-slate-100 antialiased min-h-screen">
  <div class="max-w-7xl mx-auto bg-slate-900/90 border border-slate-800 rounded-xl p-3 sm:p-6 shadow-2xl backdrop-blur-md">
    
    <!-- Header -->
    <div class="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800">
      <div>
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            5-Min Snapshot & Replay Engine
          </span>
          <h1 class="text-xl sm:text-2xl font-black tracking-tight text-white font-mono">
            Top 10 Models: Replay from Baseline & Directional Split
          </h1>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          Replay from selected baseline &bull; Inspect Total Net, <span class="text-sky-400 font-semibold">Buy Net</span> & <span class="text-amber-400 font-semibold">Sell Net</span> &bull; Toggle delta lines &bull; Re-center baseline from any timestamp
        </p>
      </div>

      <!-- Controls (Date Selector, Split Mode, Win Rate Filter) -->
      <div class="flex flex-wrap items-center gap-2.5">
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

    <!-- Interactive Replay & Baseline Scrubber Bar -->
    <div class="mt-3 p-3 bg-slate-950 border border-slate-800 rounded-xl flex flex-col gap-2.5 shadow-lg font-mono">
      <!-- Replay Controls & Stats Header -->
      <div class="flex flex-wrap items-center justify-between gap-3 text-xs">
        <div class="flex items-center gap-2">
          <!-- Play / Pause / Step Controls -->
          <button id="playBtn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow transition active:scale-95">
            <span id="playIcon">▶</span>
            <span id="playBtnText">Play from Base</span>
          </button>
          <button id="stepBackBtn" title="Step back 5 min" class="p-1.5 px-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 font-bold transition">
            ◀ -5m
          </button>
          <button id="stepFwdBtn" title="Step forward 5 min" class="p-1.5 px-2.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 font-bold transition">
            +5m ▶
          </button>
          <button id="restartBtn" title="Rewind to baseline" class="p-1.5 px-2 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700 font-bold transition">
            ↺ Base (00:00)
          </button>

          <!-- Replay Speeds -->
          <div class="flex items-center bg-slate-900 rounded-lg p-0.5 border border-slate-800 text-[11px] ml-1">
            <button id="speed1x" class="px-2 py-0.5 rounded font-bold bg-sky-600 text-white transition">1x</button>
            <button id="speed3x" class="px-2 py-0.5 rounded font-bold text-slate-400 hover:text-white transition">3x</button>
            <button id="speed10x" class="px-2 py-0.5 rounded font-bold text-slate-400 hover:text-white transition">10x</button>
          </div>
        </div>

        <!-- Replay Status & Baseline Badge -->
        <div class="flex flex-wrap items-center gap-3">
          <div class="flex items-center gap-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
            <span class="text-slate-400">Replay Head:</span>
            <span class="font-bold text-sky-300" id="replayTimeBadge">23:55</span>
            <span class="text-[10px] text-slate-500" id="replayProgressPercent">(100%)</span>
          </div>

          <div class="flex items-center gap-1.5 bg-slate-900 px-2.5 py-1 rounded-lg border border-slate-800">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <span class="text-slate-400">Baseline:</span>
            <span class="font-bold text-amber-400" id="baselineTimeBadge">00:00</span>
            <button id="setBaseAtHeadBtn" class="ml-1 text-[10px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border border-amber-500/30 transition">
              Set at Head
            </button>
            <button id="resetBaselineBtn" title="Reset baseline to 00:00" class="text-[10px] text-slate-500 hover:text-white transition">↺</button>
          </div>
        </div>
      </div>

      <!-- Scrubber Track Slider -->
      <div class="scrubber-track my-1" id="scrubberTrack">
        <div class="scrubber-fill" id="scrubberFill" style="width: 100%;"></div>
        <div class="scrubber-thumb" id="scrubberThumb" style="left: 100%;"></div>
        <div class="baseline-marker hidden" id="baselineMarker" style="left: 0%;">
          <div class="baseline-badge" id="baselineBadge">Base: 00:00</div>
        </div>
      </div>
    </div>

    <!-- Active Ribbon Inspector with Financial Metrics & Quick Actions -->
    <div class="mt-3 p-3 bg-slate-950/70 border border-slate-800 rounded-xl flex flex-wrap items-center justify-between gap-3 font-mono">
      <div class="flex items-center gap-3">
        <div class="w-2.5 h-10 rounded-full bg-sky-500" id="indicatorBar"></div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-base sm:text-lg font-black text-white" id="ribbonModelName">Top 10 Aggregate View</span>
            <span class="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-slate-800 text-sky-300" id="ribbonProduct">ALL</span>
            <span class="text-xs text-slate-400 hidden sm:inline" id="ribbonStrategy">Mode: Total Net Curves</span>
          </div>
          <div class="text-[11px] text-slate-400 mt-0.5 flex flex-wrap items-center gap-2">
            <span>Window: <b class="text-sky-300" id="activeDateLabel">Full Week</b></span>
            <span>&bull; Filter: <b class="text-emerald-400" id="winRateDisplayBadge">All Win Rates (≥0%)</b></span>
            <span>&bull; Replay Start: <b class="text-amber-400" id="replayStartBadge">From Baseline</b></span>
          </div>
        </div>
      </div>

      <!-- Quick Show/Hide Models & Directional Totals -->
      <div class="flex items-center gap-4">
        <!-- Visibility Action Buttons -->
        <div class="flex flex-col gap-1 border-r border-slate-800 pr-3">
          <button id="showAllBtn" class="px-2 py-0.5 text-[10px] font-semibold rounded bg-sky-600/30 text-sky-300 hover:bg-sky-600 hover:text-white border border-sky-500/30 transition">
            👁 Show All Models
          </button>
          <button id="hideAllBtn" class="px-2 py-0.5 text-[10px] font-semibold rounded bg-slate-800 text-slate-400 hover:bg-slate-700 hover:text-white border border-slate-700 transition">
            ✕ Hide All Models
          </button>
        </div>

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
    </div>

    <!-- Canvas Chart Card -->
    <div class="mt-3 p-3 bg-slate-950/80 rounded-xl border border-slate-800/80 relative">
      <div class="chart-container">
        <canvas id="top10Canvas"></canvas>
        <div id="tooltip" class="tooltip-box"></div>
      </div>

      <!-- Chart Header Controls: Delta Visibility Toggles & Baseline Guide -->
      <div class="flex flex-wrap items-center justify-between text-xs text-slate-400 pt-3 border-t border-slate-800/70 mt-2 font-mono gap-3">
        <!-- Delta Hiding / Showing Toggles -->
        <div class="flex flex-wrap items-center gap-2" id="deltaControlsBar">
          <span class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-1">Delta Lines:</span>
          
          <button id="toggleNetDeltaBtn" class="delta-toggle-btn flex items-center gap-1.5 px-2.5 py-1 rounded bg-emerald-500/15 border border-emerald-500/40 text-emerald-300 font-bold hover:bg-emerald-500/25 transition">
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
          </button>
        </div>

        <!-- Win Rate Slider Filter -->
        <div class="flex items-center gap-2 bg-slate-900 px-3 py-1 rounded-lg border border-slate-800">
          <span class="text-[11px] text-slate-400">Min Win Rate:</span>
          <input type="range" id="winRateSlider" min="0" max="100" step="5" value="0" class="w-24 custom-range h-1.5 bg-slate-800 rounded-lg cursor-pointer">
          <span class="text-[11px] font-bold text-sky-300" id="winRateValBadge">≥ 0%</span>
        </div>

        <div class="text-[11px] text-amber-300/90 flex items-center gap-1.5 ml-auto">
          <span class="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
          <span>Tip: Click chart/scrubber to <b>Set Baseline</b> &bull; Click <b>Play</b> to animate from baseline</span>
        </div>
      </div>
    </div>

    <!-- Interactive Top 10 Model Cards / Selectors -->
    <div class="mt-4">
      <div class="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center justify-between font-mono">
        <span id="cardsGridTitle">Top 10 Models for Selected Window</span>
        <span class="text-[10px] text-slate-500 font-normal">Click card to isolate/split &bull; Click eye button to hide individual curve</span>
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
    let currentFrameIndex = -1; // -1 means end of series (full view)
    let minWinRate = 0; // Win rate filter threshold (default 0%)
    let visibleModels = new Set();

    // Directional Delta Hiding States (Net Delta, Buy Delta, Sell Delta)
    let showNetDelta = true;
    let showBuyDelta = true;
    let showSellDelta = true;

    // Replay Animation State
    let isPlaying = false;
    let replayInterval = null;
    let replaySpeed = 1; // 1x, 3x, 10x
    const BASE_INTERVAL_MS = 250;

    const availableDates = [
      { id: 'WEEK_OVERALL', label: 'Full Week' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' }
    ];

    // DOM Elements
    const dateTabsContainer = document.getElementById('dateTabsContainer');
    const activeDateLabel = document.getElementById('activeDateLabel');
    const winRateDisplayBadge = document.getElementById('winRateDisplayBadge');
    const replayStartBadge = document.getElementById('replayStartBadge');
    const cardsGridTitle = document.getElementById('cardsGridTitle');
    const canvas = document.getElementById('top10Canvas');
    const ctx = canvas.getContext('2d');
    const tooltip = document.getElementById('tooltip');
    const modelCardsContainer = document.getElementById('modelCardsContainer');

    const metricAll = document.getElementById('metricAll');
    const metricBuy = document.getElementById('metricBuy');
    const metricSell = document.getElementById('metricSell');
    const metricTriSplit = document.getElementById('metricTriSplit');

    const showAllBtn = document.getElementById('showAllBtn');
    const hideAllBtn = document.getElementById('hideAllBtn');

    // Replay DOM Elements
    const playBtn = document.getElementById('playBtn');
    const playIcon = document.getElementById('playIcon');
    const playBtnText = document.getElementById('playBtnText');
    const stepBackBtn = document.getElementById('stepBackBtn');
    const stepFwdBtn = document.getElementById('stepFwdBtn');
    const restartBtn = document.getElementById('restartBtn');
    const speed1x = document.getElementById('speed1x');
    const speed3x = document.getElementById('speed3x');
    const speed10x = document.getElementById('speed10x');

    const replayTimeBadge = document.getElementById('replayTimeBadge');
    const replayProgressPercent = document.getElementById('replayProgressPercent');
    const baselineTimeBadge = document.getElementById('baselineTimeBadge');
    const setBaseAtHeadBtn = document.getElementById('setBaseAtHeadBtn');
    const resetBaselineBtn = document.getElementById('resetBaselineBtn');

    const scrubberTrack = document.getElementById('scrubberTrack');
    const scrubberFill = document.getElementById('scrubberFill');
    const scrubberThumb = document.getElementById('scrubberThumb');
    const baselineMarker = document.getElementById('baselineMarker');
    const baselineBadge = document.getElementById('baselineBadge');

    const winRateSlider = document.getElementById('winRateSlider');
    const winRateValBadge = document.getElementById('winRateValBadge');

    // Delta Toggle Elements
    const toggleNetDeltaBtn = document.getElementById('toggleNetDeltaBtn');
    const toggleBuyDeltaBtn = document.getElementById('toggleBuyDeltaBtn');
    const toggleSellDeltaBtn = document.getElementById('toggleSellDeltaBtn');
    const netDeltaCheck = document.getElementById('netDeltaCheck');
    const buyDeltaCheck = document.getElementById('buyDeltaCheck');
    const sellDeltaCheck = document.getElementById('sellDeltaCheck');

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

    function init() {
      setupDateTabs();
      setupEventListeners();
      updateDeltaButtonsUI();
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

    function getEligibleModels() {
      const all = ALL_DATE_DATA[currentDate] || [];
      return all.filter(m => m.win_rate >= minWinRate);
    }

    function getMaxFrames() {
      const eligible = getEligibleModels();
      if (!eligible.length) return 1;
      return Math.max(...eligible.map(m => m.series.length));
    }

    function switchDate(dateKey) {
      pauseReplay();
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

      const maxF = getMaxFrames();
      currentFrameIndex = maxF - 1; // default to full view

      const eligible = getEligibleModels();
      visibleModels = new Set(eligible.map(m => m.model));
      selectedModelIndex = 0;

      updateScrubberUI();
      updateRibbon();
      renderCards();
      drawChart();
    }

    function updateDeltaButtonsUI() {
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
    }

    // ==========================================
    // REPLAY CONTROLLER & SCRUBBER (REPLAY FROM BASELINE)
    // ==========================================
    function setReplaySpeed(spd) {
      replaySpeed = spd;
      [speed1x, speed3x, speed10x].forEach(b => {
        b.className = 'px-2 py-0.5 rounded font-bold text-slate-400 hover:text-white transition';
      });
      if (spd === 1) speed1x.className = 'px-2 py-0.5 rounded font-bold bg-sky-600 text-white transition';
      if (spd === 3) speed3x.className = 'px-2 py-0.5 rounded font-bold bg-sky-600 text-white transition';
      if (spd === 10) speed10x.className = 'px-2 py-0.5 rounded font-bold bg-sky-600 text-white transition';

      if (isPlaying) {
        clearInterval(replayInterval);
        startPlaybackLoop();
      }
    }

    function togglePlay() {
      if (isPlaying) {
        pauseReplay();
      } else {
        startReplay();
      }
    }

    function startReplay() {
      const maxF = getMaxFrames();
      // If at end of session OR if current head is before the baseline point, restart directly from baseline
      if (currentFrameIndex >= maxF - 1 || currentFrameIndex < baselineFrameIndex) {
        currentFrameIndex = baselineFrameIndex;
      }
      isPlaying = true;
      playIcon.textContent = '⏸';
      playBtnText.textContent = 'Pause';
      playBtn.classList.remove('bg-sky-600', 'hover:bg-sky-500');
      playBtn.classList.add('bg-amber-600', 'hover:bg-amber-500');
      startPlaybackLoop();
    }

    function pauseReplay() {
      isPlaying = false;
      playIcon.textContent = '▶';
      playBtnText.textContent = baselineFrameIndex > 0 ? 'Play from Base' : 'Play';
      playBtn.classList.add('bg-sky-600', 'hover:bg-sky-500');
      playBtn.classList.remove('bg-amber-600', 'hover:bg-amber-500');
      if (replayInterval) {
        clearInterval(replayInterval);
        replayInterval = null;
      }
    }

    function startPlaybackLoop() {
      const intervalMs = BASE_INTERVAL_MS / replaySpeed;
      replayInterval = setInterval(() => {
        const maxF = getMaxFrames();
        if (currentFrameIndex < maxF - 1) {
          currentFrameIndex++;
          updateScrubberUI();
          updateRibbon();
          renderCards();
          drawChart();
        } else {
          pauseReplay();
        }
      }, intervalMs);
    }

    function step(delta) {
      pauseReplay();
      const maxF = getMaxFrames();
      currentFrameIndex = Math.max(0, Math.min(maxF - 1, currentFrameIndex + delta));
      updateScrubberUI();
      updateRibbon();
      renderCards();
      drawChart();
    }

    function seekToPct(pct) {
      pauseReplay();
      const maxF = getMaxFrames();
      currentFrameIndex = Math.round(pct * (maxF - 1));
      updateScrubberUI();
      updateRibbon();
      renderCards();
      drawChart();
    }

    function updateScrubberUI() {
      const eligible = getEligibleModels();
      if (!eligible.length) return;

      const longestSeries = eligible.reduce((max, m) => m.series.length > max.series.length ? m : max, eligible[0]).series;
      const maxF = longestSeries.length;
      if (maxF <= 1) return;

      const safeIdx = Math.max(0, Math.min(maxF - 1, currentFrameIndex));
      const pct = (safeIdx / (maxF - 1)) * 100;

      scrubberFill.style.width = `${pct}%`;
      scrubberThumb.style.left = `${pct}%`;

      const headTime = longestSeries[safeIdx] ? longestSeries[safeIdx].time : '00:00';
      replayTimeBadge.textContent = headTime;
      replayProgressPercent.textContent = `(${Math.round(pct)}%)`;

      // Baseline marker position on scrubber & button label
      if (baselineFrameIndex > 0) {
        const basePct = (baselineFrameIndex / (maxF - 1)) * 100;
        baselineMarker.classList.remove('hidden');
        baselineMarker.style.left = `${basePct}%`;
        const baseTime = longestSeries[Math.min(baselineFrameIndex, maxF - 1)].time;
        baselineBadge.textContent = `Base: ${baseTime}`;
        baselineTimeBadge.textContent = baseTime;
        restartBtn.textContent = `↺ Base (${baseTime})`;
        if (!isPlaying) playBtnText.textContent = `Play from ${baseTime}`;
        replayStartBadge.textContent = `From ${baseTime}`;
      } else {
        baselineMarker.classList.add('hidden');
        baselineTimeBadge.textContent = '00:00';
        restartBtn.textContent = '↺ 00:00';
        if (!isPlaying) playBtnText.textContent = 'Play';
        replayStartBadge.textContent = 'From Session Start';
      }
    }

    function setupEventListeners() {
      metricAll.onclick = () => setSplitMode('ALL_NET');
      metricBuy.onclick = () => setSplitMode('BUY_NET');
      metricSell.onclick = () => setSplitMode('SELL_NET');
      metricTriSplit.onclick = () => setSplitMode('TRI_SPLIT');

      // Delta Hiding Toggles
      toggleNetDeltaBtn.onclick = () => {
        showNetDelta = !showNetDelta;
        updateDeltaButtonsUI();
        drawChart();
      };

      toggleBuyDeltaBtn.onclick = () => {
        showBuyDelta = !showBuyDelta;
        updateDeltaButtonsUI();
        drawChart();
      };

      toggleSellDeltaBtn.onclick = () => {
        showSellDelta = !showSellDelta;
        updateDeltaButtonsUI();
        drawChart();
      };

      // Replay playback
      playBtn.onclick = togglePlay;
      stepBackBtn.onclick = () => step(-1);
      stepFwdBtn.onclick = () => step(1);
      restartBtn.onclick = () => {
        pauseReplay();
        // Rewind directly to baseline point
        currentFrameIndex = baselineFrameIndex;
        updateScrubberUI();
        updateRibbon();
        renderCards();
        drawChart();
      };

      speed1x.onclick = () => setReplaySpeed(1);
      speed3x.onclick = () => setReplaySpeed(3);
      speed10x.onclick = () => setReplaySpeed(10);

      // Scrubber dragging / clicking
      let isScrubbing = false;
      function handleScrub(e) {
        const rect = scrubberTrack.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
        seekToPct(pct);
      }

      scrubberTrack.addEventListener('mousedown', (e) => {
        isScrubbing = true;
        handleScrub(e);
      });
      window.addEventListener('mousemove', (e) => {
        if (isScrubbing) handleScrub(e);
      });
      window.addEventListener('mouseup', () => { isScrubbing = false; });

      scrubberTrack.addEventListener('touchstart', (e) => {
        isScrubbing = true;
        handleScrub(e);
      }, { passive: true });
      window.addEventListener('touchmove', (e) => {
        if (isScrubbing) handleScrub(e);
      }, { passive: true });
      window.addEventListener('touchend', () => { isScrubbing = false; });

      // Baseline buttons
      setBaseAtHeadBtn.onclick = () => {
        const maxF = getMaxFrames();
        baselineFrameIndex = Math.max(0, Math.min(maxF - 1, currentFrameIndex));
        // When setting baseline, automatically set head to baseline for instant replay
        currentFrameIndex = baselineFrameIndex;
        updateScrubberUI();
        updateRibbon();
        renderCards();
        drawChart();
      };

      resetBaselineBtn.onclick = () => {
        baselineFrameIndex = 0;
        updateScrubberUI();
        updateRibbon();
        renderCards();
        drawChart();
      };

      // Win Rate Slider
      winRateSlider.oninput = (e) => {
        minWinRate = parseInt(e.target.value);
        winRateValBadge.textContent = `≥ ${minWinRate}%`;
        winRateDisplayBadge.textContent = minWinRate === 0 ? 'All Win Rates (≥0%)' : `Win Rate ≥ ${minWinRate}%`;

        const eligible = getEligibleModels();
        visibleModels = new Set(eligible.map(m => m.model));
        if (selectedModelIndex >= eligible.length) selectedModelIndex = 0;

        const maxF = getMaxFrames();
        currentFrameIndex = Math.min(currentFrameIndex, maxF - 1);

        updateScrubberUI();
        updateRibbon();
        renderCards();
        drawChart();
      };

      // Show All / Hide All Models
      showAllBtn.onclick = () => {
        const eligible = getEligibleModels();
        visibleModels = new Set(eligible.map(m => m.model));
        updateRibbon();
        renderCards();
        drawChart();
      };

      hideAllBtn.onclick = () => {
        visibleModels.clear();
        updateRibbon();
        renderCards();
        drawChart();
      };

      // Click on canvas to set baseline and immediately start replay from that point
      canvas.addEventListener('click', e => {
        const eligible = getEligibleModels();
        if (!eligible.length) return;

        const longestSeries = eligible.reduce((max, m) => m.series.length > max.series.length ? m : max, eligible[0]).series;
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
        currentFrameIndex = baselineFrameIndex; // set replay head at baseline point
        pauseReplay();

        updateScrubberUI();
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

    function getReplayHeadPoint(series) {
      if (!series || !series.length) return { net: 0, buy: 0, sell: 0, time: '00:00' };
      const safeIdx = Math.max(0, Math.min(currentFrameIndex, series.length - 1));
      return series[safeIdx];
    }

    function updateRibbon() {
      const eligible = getEligibleModels();
      if (!eligible.length) {
        ribbonModelName.textContent = 'No Models Matching Filter';
        ribbonTotNet.textContent = '£0.00';
        ribbonBuyNet.textContent = '£0.00';
        ribbonSellNet.textContent = '£0.00';
        return;
      }

      const longestSeries = eligible.reduce((max, m) => m.series.length > max.series.length ? m : max, eligible[0]).series;
      const baseTime = longestSeries[Math.min(baselineFrameIndex, longestSeries.length - 1)].time;
      const headTime = longestSeries[Math.min(currentFrameIndex, longestSeries.length - 1)].time;

      if (baselineFrameIndex === 0) {
        totalNetLabel.textContent = `Total Net (${headTime})`;
        buyNetLabel.textContent = 'Cum Buy Net';
        sellNetLabel.textContent = 'Cum Sell Net';
      } else {
        totalNetLabel.textContent = `Δ Net (${baseTime} → ${headTime})`;
        buyNetLabel.textContent = `Δ Buy since ${baseTime}`;
        sellNetLabel.textContent = `Δ Sell since ${baseTime}`;
      }

      const fmt = (v) => (v >= 0 ? '+£' : '-£') + Math.abs(v).toFixed(2);

      if (splitMode === 'TRI_SPLIT') {
        const m = eligible[selectedModelIndex] || eligible[0];
        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);

        const deltaNet = headPt.net - basePt.net;
        const deltaBuy = headPt.buy - basePt.buy;
        const deltaSell = headPt.sell - basePt.sell;

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
        const activeModels = eligible.filter(m => visibleModels.has(m.model));
        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          const headPt = getReplayHeadPoint(m.series);
          totNet += (headPt.net - basePt.net);
          totBuy += (headPt.buy - basePt.buy);
          totSell += (headPt.sell - basePt.sell);
        });

        ribbonModelName.textContent = `Active Models (${activeModels.length} of ${eligible.length})`;
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
      const eligible = getEligibleModels();

      if (!eligible.length) {
        modelCardsContainer.innerHTML = `
          <div class="col-span-full py-8 text-center text-slate-500 font-mono text-xs">
            No strategies match Win Rate ≥ ${minWinRate}%. Drag the slider lower to reveal models.
          </div>
        `;
        return;
      }

      eligible.forEach((m, idx) => {
        const card = document.createElement('div');
        const isTri = splitMode === 'TRI_SPLIT';
        const isSelected = isTri && idx === selectedModelIndex;
        const isVisible = isTri ? isSelected : visibleModels.has(m.model);

        const basePt = getBasePoint(m.series);
        const headPt = getReplayHeadPoint(m.series);
        const deltaNet = headPt.net - basePt.net;
        const deltaBuy = headPt.buy - basePt.buy;
        const deltaSell = headPt.sell - basePt.sell;

        card.className = `model-pill p-2.5 rounded-lg border flex flex-col justify-between ${
          isSelected 
            ? 'border-purple-500 bg-purple-500/15' 
            : (!isVisible ? 'dimmed border-slate-800 bg-slate-950/40' : 'border-slate-800 bg-slate-950/80')
        }`;

        // Clicking card body isolates/selects
        card.onclick = (e) => {
          if (e.target.closest('.eye-toggle-btn')) {
            e.stopPropagation();
            if (visibleModels.has(m.model)) {
              visibleModels.delete(m.model);
            } else {
              visibleModels.add(m.model);
            }
            updateRibbon();
            renderCards();
            drawChart();
            return;
          }

          if (splitMode === 'TRI_SPLIT') {
            selectedModelIndex = idx;
            updateRibbon();
            renderCards();
            drawChart();
          } else {
            if (visibleModels.has(m.model)) {
              if (visibleModels.size === 1) {
                visibleModels = new Set(eligible.map(x => x.model));
              } else {
                visibleModels.delete(m.model);
              }
            } else {
              visibleModels.add(m.model);
            }
            updateRibbon();
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
              <div class="flex items-center gap-1">
                <span class="text-[9px] uppercase font-bold px-1.5 py-0.5 rounded bg-slate-800 text-sky-300">${m.product}</span>
                <button title="${isVisible ? 'Hide chart' : 'Show chart'}" class="eye-toggle-btn p-0.5 rounded text-xs leading-none transition ${isVisible ? 'text-sky-400' : 'text-slate-600'}">
                  ${isVisible ? '👁' : '✕'}
                </button>
              </div>
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

      const eligible = getEligibleModels();
      if (!eligible.length) {
        ctx.fillStyle = '#64748b';
        ctx.font = '13px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(`No models match Win Rate ≥ ${minWinRate}%.`, width / 2, height / 2);
        return;
      }

      const padLeft = 65;
      const padRight = 30;
      const padTop = 30;
      const padBottom = 40;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      const longestSeries = eligible.reduce((max, m) => m.series.length > max.series.length ? m : max, eligible[0]).series;
      const totalLen = longestSeries.length;
      const drawUpTo = Math.max(0, Math.min(totalLen - 1, currentFrameIndex));
      const baseTime = longestSeries[Math.min(baselineFrameIndex, totalLen - 1)].time;
      const headTime = longestSeries[drawUpTo].time;

      if (splitMode === 'TRI_SPLIT') {
        const m = eligible[selectedModelIndex] || eligible[0];
        const basePt = getBasePoint(m.series);

        // Check if all deltas are hidden
        if (!showNetDelta && !showBuyDelta && !showSellDelta) {
          ctx.fillStyle = '#64748b';
          ctx.font = '13px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('All delta curves hidden. Click any Delta button above (Net / Buy / Sell) to display.', width / 2, height / 2);
          return;
        }

        // Calculate min/max over the slice up to drawUpTo
        let deltas = [];
        const sliceLen = Math.min(m.series.length, drawUpTo + 1);
        for (let i = 0; i < sliceLen; i++) {
          const pt = m.series[i];
          if (showNetDelta) deltas.push(pt.net - basePt.net);
          if (showBuyDelta) deltas.push(pt.buy - basePt.buy);
          if (showSellDelta) deltas.push(pt.sell - basePt.sell);
        }

        let minVal = Math.min(0, ...deltas);
        let maxVal = Math.max(0, ...deltas);
        if (minVal === maxVal) { minVal -= 50; maxVal += 50; }

        const span = maxVal - minVal;
        minVal -= span * 0.08;
        maxVal += span * 0.08;

        const getY = val => padTop + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
        const getX = idx => padLeft + (idx / (m.series.length - 1 || 1)) * plotW;

        drawGridAndAxes(width, height, padLeft, padRight, padTop, padBottom, plotW, plotH, minVal, maxVal, m.series, getY, getX);

        if (baselineFrameIndex > 0) {
          const bX = getX(Math.min(baselineFrameIndex, m.series.length - 1));
          drawBaselineMarker(bX, padTop, height - padBottom, baseTime);
        }

        // Render curves up to drawUpTo
        const subSeries = m.series.slice(0, drawUpTo + 1);
        const lastIdx = subSeries.length - 1;
        const lastPt = subSeries[lastIdx];

        if (showBuyDelta) {
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
        }

        // Draw Replay Vertical Cursor
        drawReplayCursor(getX(drawUpTo), padTop, height - padBottom, headTime);

        timeAxisPoints = subSeries.map((s, idx) => ({
          x: getX(idx),
          idx: idx,
          time: s.time,
          data: s
        }));

      } else {
        // Group modes (ALL_NET, BUY_NET, SELL_NET)
        let activeMetric = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');
        let isMetricVisible = (activeMetric === 'net' && showNetDelta) ||
                              (activeMetric === 'buy' && showBuyDelta) ||
                              (activeMetric === 'sell' && showSellDelta);

        const activeModels = eligible.filter(m => visibleModels.has(m.model));
        if (!activeModels.length) {
          ctx.fillStyle = '#64748b';
          ctx.font = '13px monospace';
          ctx.textAlign = 'center';
          ctx.fillText('All model lines hidden. Click "Show All Models" or any card to display curves.', width / 2, height / 2);
          return;
        }

        if (!isMetricVisible) {
          ctx.fillStyle = '#64748b';
          ctx.font = '13px monospace';
          ctx.textAlign = 'center';
          const label = activeMetric === 'net' ? 'Net Delta' : (activeMetric === 'buy' ? 'Buy Delta' : 'Sell Delta');
          ctx.fillText(`Current metric (${label}) is hidden. Click the "${label}" toggle button above to reveal.`, width / 2, height / 2);
          return;
        }

        let allDeltas = [];
        activeModels.forEach(m => {
          const basePt = getBasePoint(m.series);
          const sliceLen = Math.min(m.series.length, drawUpTo + 1);
          for (let i = 0; i < sliceLen; i++) {
            allDeltas.push(m.series[i][activeMetric] - basePt[activeMetric]);
          }
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
          const subSeries = m.series.slice(0, drawUpTo + 1);
          renderDeltaLine(subSeries, activeMetric, basePt[activeMetric], m.color, 2.2, [], getX, getY);
          if (subSeries.length) {
            const lastIdx = subSeries.length - 1;
            const deltaVal = subSeries[lastIdx][activeMetric] - basePt[activeMetric];
            drawPointLabel(getX(lastIdx), getY(deltaVal), `${m.model} (£${deltaVal.toFixed(0)})`, m.color);
          }
        });

        // Draw Replay Vertical Cursor
        drawReplayCursor(getX(drawUpTo), padTop, height - padBottom, headTime);

        timeAxisPoints = longestSeries.slice(0, drawUpTo + 1).map((s, idx) => ({
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

    function drawReplayCursor(x, yTop, yBottom, timeStr) {
      ctx.strokeStyle = '#38bdf8';
      ctx.lineWidth = 1.6;
      ctx.setLineDash([3, 3]);
      ctx.beginPath();
      ctx.moveTo(x, yTop);
      ctx.lineTo(x, yBottom);
      ctx.stroke();
      ctx.setLineDash([]);

      ctx.fillStyle = '#38bdf8';
      ctx.font = 'bold 9px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(`NOW: ${timeStr}`, x, yTop - 8);
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

        const eligible = getEligibleModels();

        if (splitMode === 'TRI_SPLIT') {
          const m = eligible[selectedModelIndex] || eligible[0];
          const basePt = getBasePoint(m.series);
          const pt = m.series[closest.idx] || m.series[m.series.length - 1];

          const dNet = pt.net - basePt.net;
          const dBuy = pt.buy - basePt.buy;
          const dSell = pt.sell - basePt.sell;

          let rows = '';
          if (showNetDelta) {
            rows += `
              <div class="flex justify-between">
                <span class="text-emerald-400 font-semibold">Δ Total Net:</span>
                <span class="font-bold ${dNet >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dNet.toFixed(2)}</span>
              </div>
            `;
          }
          if (showBuyDelta) {
            rows += `
              <div class="flex justify-between">
                <span class="text-sky-400 font-semibold">Δ Buy Net:</span>
                <span class="font-bold ${dBuy >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dBuy.toFixed(2)}</span>
              </div>
            `;
          }
          if (showSellDelta) {
            rows += `
              <div class="flex justify-between">
                <span class="text-amber-400 font-semibold">Δ Sell Net:</span>
                <span class="font-bold ${dSell >= 0 ? 'text-emerald-400' : 'text-rose-400'}">£${dSell.toFixed(2)}</span>
              </div>
            `;
          }

          tooltip.innerHTML = `
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
          `;
        } else {
          const metricKey = splitMode === 'BUY_NET' ? 'buy' : (splitMode === 'SELL_NET' ? 'sell' : 'net');
          const activeModels = eligible.filter(m => visibleModels.has(m.model));
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

# Save in brain
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
with open(brain_path, "w", encoding="utf-8") as f:
    f.write(full_html)

# Save in epic
epic_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(epic_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("SUCCESS: Updated top10_5min_equity_curves.html to replay directly from baseline point!")
