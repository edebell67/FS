import json

json_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\scratch\replay_dashboard_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    data_json = f.read()

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Breakout Mobile Strategy Replay & Delta Initializer</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      margin: 0;
      padding: 0;
      background-color: #080c14;
      color: #f1f5f9;
      -webkit-tap-highlight-color: transparent;
    }
    .chart-container {
      position: relative;
      width: 100%;
      height: 340px;
      touch-action: none;
    }
    @media (min-width: 768px) {
      .chart-container {
        height: 420px;
      }
    }
    .custom-range {
      accent-color: #38bdf8;
    }
    .pill-btn {
      transition: all 0.15s ease-in-out;
    }
    .model-card {
      transition: transform 0.12s ease, border-color 0.12s ease;
      cursor: pointer;
    }
    .model-card:active {
      transform: scale(0.97);
    }
    .model-card.active {
      border-color: #38bdf8;
      background-color: rgba(56, 189, 248, 0.14);
    }
    .scrubber-track {
      position: relative;
      width: 100%;
      height: 8px;
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
    }
    .baseline-marker {
      position: absolute;
      top: -4px;
      bottom: -4px;
      width: 2px;
      background: #f59e0b;
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
    .no-scrollbar::-webkit-scrollbar {
      display: none;
    }
    .no-scrollbar {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen antialiased flex flex-col justify-between">

  <!-- Top App Navigation Bar -->
  <header class="sticky top-0 z-40 bg-slate-900/95 border-b border-slate-800/90 backdrop-blur-md px-3 py-2.5">
    <div class="flex items-center justify-between gap-2 max-w-5xl mx-auto">
      <div class="flex items-center gap-2">
        <div class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></div>
        <div>
          <h1 class="text-sm font-black tracking-tight text-white flex items-center gap-1.5 font-mono">
            <span>REPLAY & DELTA UI</span>
            <span class="text-[9px] px-1.5 py-0.5 rounded bg-sky-500/20 text-sky-300 font-sans font-bold uppercase">5-Min DNA</span>
          </h1>
        </div>
      </div>

      <!-- Quick Filter Pills Toggle Trigger / Active Count -->
      <div class="flex items-center gap-1.5">
        <span class="text-[11px] font-mono font-bold text-amber-400 bg-amber-400/10 border border-amber-400/20 px-2 py-0.5 rounded-full" id="matchingModelsCount">
          0 Models
        </span>
        <button id="toggleSettingsBtn" class="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path></svg>
        </button>
      </div>
    </div>

    <!-- Collapsible Filter Drawer -->
    <div id="filterDrawer" class="max-w-5xl mx-auto mt-2 pt-2 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-2 gap-3 pb-1">
      <!-- Date Selector -->
      <div>
        <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Session Date</label>
        <div class="flex items-center gap-1 overflow-x-auto no-scrollbar pb-1" id="dateTabs"></div>
      </div>

      <!-- Threshold Controls -->
      <div class="flex items-center gap-4">
        <!-- Win Rate Threshold -->
        <div class="flex-1">
          <div class="flex justify-between text-[11px] font-mono mb-1">
            <span class="text-slate-400">Min Win Rate:</span>
            <span class="font-bold text-sky-400" id="winRateValBadge">≥ 100%</span>
          </div>
          <input type="range" id="winRateSlider" min="0" max="100" step="5" value="100" class="w-full custom-range h-1.5 bg-slate-800 rounded-lg cursor-pointer">
          <div class="flex justify-between text-[9px] text-slate-500 font-mono mt-0.5">
            <span>0%</span>
            <span>50%</span>
            <span>80%</span>
            <span class="text-sky-300 font-bold">100% (Default)</span>
          </div>
        </div>

        <!-- Min Trades Filter -->
        <div class="w-24">
          <label class="text-[10px] uppercase font-bold text-slate-400 block mb-1">Min Trades</label>
          <select id="minTradesSelect" class="w-full bg-slate-800 border border-slate-700 text-xs font-mono rounded px-2 py-1 text-white">
            <option value="4" selected>> 3 trades</option>
            <option value="6">> 5 trades</option>
            <option value="10">> 9 trades</option>
            <option value="20">> 19 trades</option>
          </select>
        </div>
      </div>
    </div>
  </header>

  <!-- Main Viewport -->
  <main class="max-w-5xl mx-auto w-full px-3 py-2 flex-1 flex flex-col gap-2">

    <!-- Selected Model Summary Ribbon -->
    <div class="bg-slate-900/80 border border-slate-800/90 rounded-xl p-3 flex flex-wrap items-center justify-between gap-3 shadow-lg">
      <div class="flex items-center gap-2.5">
        <div class="w-2.5 h-9 rounded-full bg-sky-500" id="ribbonBar"></div>
        <div>
          <div class="flex items-center gap-2">
            <span class="text-base font-black text-white font-mono" id="selModelCode">DNA_201105</span>
            <span class="text-[10px] font-bold uppercase px-1.5 py-0.5 rounded bg-slate-800 text-sky-300 font-mono" id="selProduct">GBP</span>
            <span class="text-xs text-slate-400 font-mono hidden sm:inline" id="selStrategy">breakout_R_Rev_3_tp3_sl50</span>
          </div>
          <div class="text-[11px] text-slate-400 font-mono mt-0.5 flex items-center gap-3">
            <span>Vol: <b class="text-amber-400" id="selTradesCount">11 trades</b></span>
            <span>Win Rate: <b class="text-emerald-400" id="selWinRate">100.0%</b></span>
            <span id="baselineOffsetDisplay" class="text-amber-300 font-semibold hidden">&bull; Base: 00:00</span>
          </div>
        </div>
      </div>

      <!-- Financial Deltas -->
      <div class="flex items-center gap-4 text-right font-mono">
        <div>
          <div class="text-[9px] uppercase tracking-wider text-slate-400" id="totalNetLabel">Net P&L</div>
          <div class="text-base sm:text-lg font-black text-emerald-400" id="dispTotalNet">+£360.00</div>
        </div>
        <div class="border-l border-slate-800 pl-3">
          <div class="text-[9px] uppercase tracking-wider text-slate-400">Buy (Longs)</div>
          <div class="text-xs sm:text-sm font-bold text-sky-400" id="dispBuyNet">+£180.00</div>
        </div>
        <div class="border-l border-slate-800 pl-3">
          <div class="text-[9px] uppercase tracking-wider text-slate-400">Sell (Shorts)</div>
          <div class="text-xs sm:text-sm font-bold text-amber-400" id="dispSellNet">+£180.00</div>
        </div>
      </div>
    </div>

    <!-- Interactive Replay & Baseline Control Bar -->
    <div class="bg-slate-900/90 border border-slate-800/90 rounded-xl p-3 flex flex-col gap-2.5 shadow-md">
      <!-- Time Header & Replay State -->
      <div class="flex items-center justify-between text-xs font-mono">
        <div class="flex items-center gap-2">
          <span class="text-slate-400 text-[11px]">Replay Head:</span>
          <span class="px-2 py-0.5 rounded bg-sky-500/20 text-sky-300 font-bold text-xs" id="replayTimeBadge">00:00</span>
          <span class="text-[10px] text-slate-500" id="replayProgressPercent">0%</span>
        </div>

        <div class="flex items-center gap-1.5">
          <!-- Baseline Initializer Indicator -->
          <div class="flex items-center gap-1 bg-slate-950 px-2 py-0.5 rounded border border-slate-800 text-[11px]">
            <span class="w-2 h-2 rounded-full bg-amber-400"></span>
            <span class="text-slate-400">Baseline Point:</span>
            <span class="font-bold text-amber-400" id="baselineTimeBadge">Start (00:00)</span>
            <button id="resetBaselineBtn" title="Reset baseline to 00:00" class="ml-1 text-[10px] text-slate-500 hover:text-white transition">↺</button>
          </div>
        </div>
      </div>

      <!-- Scrubber Track Slider -->
      <div class="scrubber-track my-1" id="scrubberTrack">
        <div class="scrubber-fill" id="scrubberFill" style="width: 0%;"></div>
        <div class="scrubber-thumb" id="scrubberThumb" style="left: 0%;"></div>
        <div class="baseline-marker hidden" id="baselineMarker" style="left: 0%;">
          <div class="baseline-badge" id="baselineBadge">Base: 03:00</div>
        </div>
      </div>

      <!-- Replay Buttons & Speeds -->
      <div class="flex items-center justify-between pt-1">
        <!-- Play / Pause / Reset -->
        <div class="flex items-center gap-2">
          <button id="playBtn" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-md transition active:scale-95">
            <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 20 20" id="playIcon"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path></svg>
            <span id="playBtnText">Play</span>
          </button>
          <button id="stepBackBtn" title="Step back 5 min" class="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path></svg>
          </button>
          <button id="stepFwdBtn" title="Step forward 5 min" class="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
          </button>
          <button id="restartBtn" title="Rewind to start" class="p-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white border border-slate-700">
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          </button>
        </div>

        <!-- Baseline Quick Set (e.g. 03:00, 08:00, or Current Point) -->
        <div class="flex items-center gap-1.5">
          <button id="setBaseAtCurrentBtn" class="px-2 py-1 text-[11px] font-semibold rounded bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 border border-amber-500/30 transition">
            Set Baseline at Head
          </button>
          
          <!-- Replay Speed Options -->
          <div class="flex items-center bg-slate-950 p-0.5 rounded border border-slate-800 text-[10px] font-mono">
            <button class="speed-btn px-1.5 py-0.5 rounded text-slate-400" data-speed="1">1x</button>
            <button class="speed-btn px-1.5 py-0.5 rounded bg-sky-600 text-white font-bold" data-speed="3">3x</button>
            <button class="speed-btn px-1.5 py-0.5 rounded text-slate-400" data-speed="8">8x</button>
            <button class="speed-btn px-1.5 py-0.5 rounded text-slate-400" data-speed="20">20x</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Canvas Chart Card -->
    <div class="bg-slate-900/90 border border-slate-800/90 rounded-xl p-2 sm:p-3 relative shadow-xl">
      <div class="chart-container">
        <canvas id="chartCanvas"></canvas>
      </div>

      <!-- Chart Footer Legend & Touch Helper -->
      <div class="flex flex-wrap items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-slate-800/80 font-mono mt-1 px-1">
        <div class="flex items-center gap-3">
          <div class="flex items-center gap-1.5">
            <span class="w-2.5 h-0.5 bg-emerald-400 rounded-full inline-block"></span>
            <span class="text-slate-200">Net Delta</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-2.5 h-0.5 bg-sky-400 rounded-full inline-block border-b border-dashed border-sky-400"></span>
            <span>Buy Delta</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-2.5 h-0.5 bg-amber-400 rounded-full inline-block border-b border-dashed border-amber-400"></span>
            <span>Sell Delta</span>
          </div>
        </div>
        <div class="text-[10px] text-slate-500 hidden sm:inline">
          Tap chart to set baseline &bull; Drag scrubber to scrub time
        </div>
      </div>
    </div>

    <!-- Models List / Swipeable Carousel -->
    <div class="mt-1">
      <div class="flex items-center justify-between mb-1.5 px-1">
        <span class="text-xs font-bold uppercase tracking-wider text-slate-400 font-mono">
          Matching Models (<span id="activeFilterLabel">Win Rate ≥ 100%, Trades > 3</span>)
        </span>
        <span class="text-[10px] text-slate-500">Tap card to load model</span>
      </div>

      <!-- Scrollable Cards Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-2" id="modelsGrid"></div>
    </div>

  </main>

  <script>
    const ALL_DATA = __DATA_JSON_PLACEHOLDER__;

    // State Variables
    let currentDate = '2026-09-17'; // default to day with rich 100% runs
    let minWinRate = 100;
    let minTrades = 4;
    let selectedModelIndex = 0;
    let currentFrameIndex = 0; // Current replay scrubber index
    let baselineFrameIndex = 0; // Baseline reference frame index (defaults to 0 / start)
    let isPlaying = false;
    let replaySpeed = 3; // frames per step interval
    let playInterval = null;

    // DOM Elements
    const dateTabs = document.getElementById('dateTabs');
    const winRateSlider = document.getElementById('winRateSlider');
    const winRateValBadge = document.getElementById('winRateValBadge');
    const minTradesSelect = document.getElementById('minTradesSelect');
    const toggleSettingsBtn = document.getElementById('toggleSettingsBtn');
    const filterDrawer = document.getElementById('filterDrawer');
    const matchingModelsCount = document.getElementById('matchingModelsCount');
    const activeFilterLabel = document.getElementById('activeFilterLabel');

    const ribbonBar = document.getElementById('ribbonBar');
    const selModelCode = document.getElementById('selModelCode');
    const selProduct = document.getElementById('selProduct');
    const selStrategy = document.getElementById('selStrategy');
    const selTradesCount = document.getElementById('selTradesCount');
    const selWinRate = document.getElementById('selWinRate');
    const baselineOffsetDisplay = document.getElementById('baselineOffsetDisplay');

    const totalNetLabel = document.getElementById('totalNetLabel');
    const dispTotalNet = document.getElementById('dispTotalNet');
    const dispBuyNet = document.getElementById('dispBuyNet');
    const dispSellNet = document.getElementById('dispSellNet');

    const replayTimeBadge = document.getElementById('replayTimeBadge');
    const replayProgressPercent = document.getElementById('replayProgressPercent');
    const baselineTimeBadge = document.getElementById('baselineTimeBadge');
    const resetBaselineBtn = document.getElementById('resetBaselineBtn');
    const setBaseAtCurrentBtn = document.getElementById('setBaseAtCurrentBtn');

    const scrubberTrack = document.getElementById('scrubberTrack');
    const scrubberFill = document.getElementById('scrubberFill');
    const scrubberThumb = document.getElementById('scrubberThumb');
    const baselineMarker = document.getElementById('baselineMarker');
    const baselineBadge = document.getElementById('baselineBadge');

    const playBtn = document.getElementById('playBtn');
    const playBtnText = document.getElementById('playBtnText');
    const playIcon = document.getElementById('playIcon');
    const stepBackBtn = document.getElementById('stepBackBtn');
    const stepFwdBtn = document.getElementById('stepFwdBtn');
    const restartBtn = document.getElementById('restartBtn');
    const speedButtons = document.querySelectorAll('.speed-btn');

    const canvas = document.getElementById('chartCanvas');
    const ctx = canvas.getContext('2d');
    const modelsGrid = document.getElementById('modelsGrid');

    // Available Dates
    const availableDates = [
      { id: '2026-09-17', label: 'Thu 17' },
      { id: '2026-09-18', label: 'Fri 18' },
      { id: '2026-09-16', label: 'Wed 16' },
      { id: '2026-09-15', label: 'Tue 15' },
      { id: '2026-09-14', label: 'Mon 14' },
      { id: 'WEEK_OVERALL', label: 'Full Week' }
    ];

    function init() {
      setupDateTabs();
      setupEventListeners();
      filterAndRenderModels();
    }

    function setupDateTabs() {
      dateTabs.innerHTML = '';
      availableDates.forEach(d => {
        const btn = document.createElement('button');
        btn.className = `pill-btn px-2.5 py-1 text-xs font-bold font-mono rounded whitespace-nowrap ${
          d.id === currentDate ? 'bg-sky-600 text-white shadow' : 'bg-slate-800 text-slate-400 hover:text-white'
        }`;
        btn.textContent = d.label;
        btn.onclick = () => {
          pauseReplay();
          currentDate = d.id;
          setupDateTabs();
          baselineFrameIndex = 0;
          currentFrameIndex = 0;
          selectedModelIndex = 0;
          filterAndRenderModels();
        };
        dateTabs.appendChild(btn);
      });
    }

    function setupEventListeners() {
      // Toggle Filter Drawer on mobile
      toggleSettingsBtn.onclick = () => {
        filterDrawer.classList.toggle('hidden');
      };

      // Win Rate Slider
      winRateSlider.oninput = (e) => {
        minWinRate = parseInt(e.target.value);
        winRateValBadge.textContent = `≥ ${minWinRate}%`;
        filterAndRenderModels();
      };

      // Min Trades Select
      minTradesSelect.onchange = (e) => {
        minTrades = parseInt(e.target.value);
        filterAndRenderModels();
      };

      // Play / Pause
      playBtn.onclick = togglePlay;

      // Steps
      stepBackBtn.onclick = () => {
        pauseReplay();
        const curModel = getActiveModel();
        if (!curModel || !curModel.series.length) return;
        currentFrameIndex = Math.max(0, currentFrameIndex - 1);
        updateView();
      };

      stepFwdBtn.onclick = () => {
        pauseReplay();
        const curModel = getActiveModel();
        if (!curModel || !curModel.series.length) return;
        currentFrameIndex = Math.min(curModel.series.length - 1, currentFrameIndex + 1);
        updateView();
      };

      restartBtn.onclick = () => {
        pauseReplay();
        currentFrameIndex = baselineFrameIndex;
        updateView();
      };

      // Speeds
      speedButtons.forEach(btn => {
        btn.onclick = () => {
          speedButtons.forEach(b => {
            b.className = 'speed-btn px-1.5 py-0.5 rounded text-slate-400';
          });
          btn.className = 'speed-btn px-1.5 py-0.5 rounded bg-sky-600 text-white font-bold';
          replaySpeed = parseInt(btn.getAttribute('data-speed'));
          if (isPlaying) {
            pauseReplay();
            startReplay();
          }
        };
      });

      // Set baseline at current head
      setBaseAtCurrentBtn.onclick = () => {
        baselineFrameIndex = currentFrameIndex;
        updateBaselineMarker();
        updateView();
      };

      // Reset baseline to start
      resetBaselineBtn.onclick = () => {
        baselineFrameIndex = 0;
        updateBaselineMarker();
        updateView();
      };

      // Touch / Click Scrubber
      const handleScrubber = (e) => {
        pauseReplay();
        const rect = scrubberTrack.getBoundingClientRect();
        const clientX = e.touches ? e.touches[0].clientX : e.clientX;
        let pct = (clientX - rect.left) / rect.width;
        pct = Math.max(0, Math.min(1, pct));

        const curModel = getActiveModel();
        if (!curModel || !curModel.series.length) return;
        currentFrameIndex = Math.round(pct * (curModel.series.length - 1));
        updateView();
      };

      scrubberTrack.addEventListener('mousedown', (e) => {
        handleScrubber(e);
        const onMouseMove = (ev) => handleScrubber(ev);
        const onMouseUp = () => {
          window.removeEventListener('mousemove', onMouseMove);
          window.removeEventListener('mouseup', onMouseUp);
        };
        window.addEventListener('mousemove', onMouseMove);
        window.addEventListener('mouseup', onMouseUp);
      });

      scrubberTrack.addEventListener('touchstart', (e) => {
        handleScrubber(e);
        const onTouchMove = (ev) => handleScrubber(ev);
        const onTouchEnd = () => {
          window.removeEventListener('touchmove', onTouchMove);
          window.removeEventListener('touchend', onTouchEnd);
        };
        window.addEventListener('touchmove', onTouchMove);
        window.addEventListener('touchend', onTouchEnd);
      });

      // Click on canvas to set baseline
      canvas.addEventListener('click', (e) => {
        const rect = canvas.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const padLeft = 45;
        const padRight = 15;
        const plotW = rect.width - padLeft - padRight;
        if (plotW <= 0) return;

        let pct = (clickX - padLeft) / plotW;
        pct = Math.max(0, Math.min(1, pct));

        const curModel = getActiveModel();
        if (!curModel || !curModel.series.length) return;
        baselineFrameIndex = Math.round(pct * (curModel.series.length - 1));
        updateBaselineMarker();
        updateView();
      });

      window.addEventListener('resize', () => {
        drawChart();
      });
    }

    function getFilteredModels() {
      const dayData = ALL_DATA[currentDate];
      if (!dayData || !dayData.models) return [];
      return dayData.models.filter(m => m.win_rate >= minWinRate && m.trades >= minTrades);
    }

    function getActiveModel() {
      const models = getFilteredModels();
      if (!models.length) return null;
      if (selectedModelIndex >= models.length) selectedModelIndex = 0;
      return models[selectedModelIndex];
    }

    function filterAndRenderModels() {
      const filtered = getFilteredModels();
      matchingModelsCount.textContent = `${filtered.length} Models`;
      activeFilterLabel.textContent = `Win Rate ≥ ${minWinRate}%, Trades ≥ ${minTrades}`;

      modelsGrid.innerHTML = '';

      if (!filtered.length) {
        modelsGrid.innerHTML = `
          <div class="col-span-full py-8 text-center text-slate-500 font-mono text-xs">
            No models matched criteria (Win Rate ≥ ${minWinRate}%, Trades ≥ ${minTrades}) for ${currentDate}.
            <br><span class="text-sky-400 underline cursor-pointer mt-1 inline-block" onclick="winRateSlider.value=80;winRateSlider.dispatchEvent(new Event('input'))">Lower threshold to 80%</span>
          </div>
        `;
        resetRibbon();
        drawEmptyChart('No matching models for current criteria');
        return;
      }

      filtered.forEach((m, idx) => {
        const card = document.createElement('div');
        const isActive = idx === selectedModelIndex;
        card.className = `model-card bg-slate-900/90 border rounded-lg p-2 flex flex-col justify-between ${
          isActive ? 'active' : 'border-slate-800'
        }`;
        card.onclick = () => {
          selectedModelIndex = idx;
          currentFrameIndex = 0;
          baselineFrameIndex = 0;
          updateActiveCardClass();
          updateBaselineMarker();
          updateView();
        };

        const winColor = m.win_rate >= 100 ? 'text-emerald-400' : 'text-sky-400';
        const netColor = m.cum_net >= 0 ? 'text-emerald-400' : 'text-rose-400';

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between text-[11px] font-mono">
              <span class="font-black text-white truncate">${m.model}</span>
              <span class="text-[9px] uppercase font-bold px-1 rounded bg-slate-800 text-sky-300">${m.product}</span>
            </div>
            <div class="text-[9px] text-slate-400 font-mono truncate mt-0.5">${m.strategy.replace('breakout_', '')}</div>
            <div class="flex items-center justify-between text-[10px] font-mono mt-1.5 pt-1 border-t border-slate-800/80">
              <span class="text-slate-400">Vol: <strong class="text-amber-300">${m.trades}</strong></span>
              <span class="${winColor} font-bold">${m.win_rate}%</span>
            </div>
          </div>
          <div class="text-right text-xs font-mono font-black mt-1 ${netColor}">
            ${m.cum_net >= 0 ? '+£' : '-£'}${Math.abs(m.cum_net).toFixed(0)}
          </div>
        `;
        modelsGrid.appendChild(card);
      });

      const curModel = getActiveModel();
      if (curModel && curModel.series.length) {
        if (currentFrameIndex === 0) currentFrameIndex = curModel.series.length - 1; // start by showing complete session
      }
      updateBaselineMarker();
      updateView();
    }

    function updateActiveCardClass() {
      const cards = modelsGrid.querySelectorAll('.model-card');
      cards.forEach((c, idx) => {
        if (idx === selectedModelIndex) c.classList.add('active');
        else c.classList.remove('active');
      });
    }

    function updateBaselineMarker() {
      const curModel = getActiveModel();
      if (!curModel || !curModel.series.length) {
        baselineMarker.classList.add('hidden');
        return;
      }
      if (baselineFrameIndex === 0) {
        baselineMarker.classList.add('hidden');
        baselineTimeBadge.textContent = `Start (${curModel.series[0].time})`;
        baselineOffsetDisplay.classList.add('hidden');
        totalNetLabel.textContent = "Net P&L";
      } else {
        const basePoint = curModel.series[baselineFrameIndex] || curModel.series[0];
        const pct = (baselineFrameIndex / (curModel.series.length - 1 || 1)) * 100;
        baselineMarker.classList.remove('hidden');
        baselineMarker.style.left = `${pct}%`;
        baselineBadge.textContent = `Base: ${basePoint.time}`;
        baselineTimeBadge.textContent = basePoint.time;
        baselineOffsetDisplay.textContent = `• Delta Ref: ${basePoint.time}`;
        baselineOffsetDisplay.classList.remove('hidden');
        totalNetLabel.textContent = `Delta since ${basePoint.time}`;
      }
    }

    function updateView() {
      const curModel = getActiveModel();
      if (!curModel || !curModel.series.length) return;

      const series = curModel.series;
      if (currentFrameIndex >= series.length) currentFrameIndex = series.length - 1;

      // Update Scrubber UI
      const pct = (currentFrameIndex / (series.length - 1 || 1)) * 100;
      scrubberFill.style.width = `${pct}%`;
      scrubberThumb.style.left = `${pct}%`;

      const curPoint = series[currentFrameIndex];
      const basePoint = series[baselineFrameIndex] || series[0];

      replayTimeBadge.textContent = curPoint.time;
      replayProgressPercent.textContent = `${Math.round(pct)}%`;

      // Update Ribbon metadata
      selModelCode.textContent = curModel.model;
      selProduct.textContent = curModel.product;
      selStrategy.textContent = curModel.strategy;
      selTradesCount.textContent = `${curModel.trades} trades (${curModel.wins}W / ${curModel.losses}L)`;
      selWinRate.textContent = `${curModel.win_rate}%`;

      // Calculate baseline delta
      const netDelta = curPoint.net - basePoint.net;
      const buyDelta = curPoint.buy - basePoint.buy;
      const sellDelta = curPoint.sell - basePoint.sell;

      const fmt = (v) => (v >= 0 ? "+£" : "-£") + Math.abs(v).toFixed(2);

      dispTotalNet.textContent = fmt(netDelta);
      dispTotalNet.className = `text-base sm:text-lg font-black font-mono ${netDelta >= 0 ? 'text-emerald-400' : 'text-rose-400'}`;

      dispBuyNet.textContent = fmt(buyDelta);
      dispBuyNet.className = `text-xs sm:text-sm font-bold font-mono ${buyDelta >= 0 ? 'text-sky-400' : 'text-rose-400'}`;

      dispSellNet.textContent = fmt(sellDelta);
      dispSellNet.className = `text-xs sm:text-sm font-bold font-mono ${sellDelta >= 0 ? 'text-amber-400' : 'text-rose-400'}`;

      drawChart();
    }

    function resetRibbon() {
      selModelCode.textContent = "-";
      selProduct.textContent = "-";
      selStrategy.textContent = "-";
      selTradesCount.textContent = "0";
      selWinRate.textContent = "0%";
      dispTotalNet.textContent = "£0.00";
      dispBuyNet.textContent = "£0.00";
      dispSellNet.textContent = "£0.00";
    }

    function togglePlay() {
      if (isPlaying) pauseReplay();
      else startReplay();
    }

    function startReplay() {
      const curModel = getActiveModel();
      if (!curModel || !curModel.series.length) return;

      isPlaying = true;
      playBtnText.textContent = "Pause";
      playBtn.className = "flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-bold text-xs shadow-md transition";
      playIcon.innerHTML = '<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd"></path>';

      if (currentFrameIndex >= curModel.series.length - 1) {
        currentFrameIndex = baselineFrameIndex; // restart from baseline
      }

      playInterval = setInterval(() => {
        if (currentFrameIndex < curModel.series.length - 1) {
          currentFrameIndex = Math.min(curModel.series.length - 1, currentFrameIndex + replaySpeed);
          updateView();
        } else {
          pauseReplay();
        }
      }, 100);
    }

    function pauseReplay() {
      isPlaying = false;
      if (playInterval) clearInterval(playInterval);
      playInterval = null;
      playBtnText.textContent = "Play";
      playBtn.className = "flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-sky-600 hover:bg-sky-500 text-white font-bold text-xs shadow-md transition active:scale-95";
      playIcon.innerHTML = '<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"></path>';
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

    function drawEmptyChart(msg) {
      setupCanvas();
      const rect = canvas.parentElement.getBoundingClientRect();
      ctx.clearRect(0, 0, rect.width, rect.height);
      ctx.fillStyle = '#64748b';
      ctx.font = '12px monospace';
      ctx.textAlign = 'center';
      ctx.fillText(msg, rect.width / 2, rect.height / 2);
    }

    function drawChart() {
      setupCanvas();
      const rect = canvas.parentElement.getBoundingClientRect();
      const width = rect.width;
      const height = rect.height;

      ctx.clearRect(0, 0, width, height);

      const curModel = getActiveModel();
      if (!curModel || !curModel.series || !curModel.series.length) {
        drawEmptyChart('No series data available');
        return;
      }

      const fullSeries = curModel.series;
      const basePoint = fullSeries[baselineFrameIndex] || fullSeries[0];
      const visibleSeries = fullSeries.slice(0, currentFrameIndex + 1);

      if (!visibleSeries.length) return;

      const padLeft = 45;
      const padRight = 15;
      const padTop = 20;
      const padBottom = 28;

      const plotW = width - padLeft - padRight;
      const plotH = height - padTop - padBottom;

      // Calculate relative delta values across the entire session to keep axis scale stable
      let allDeltas = [];
      fullSeries.forEach(pt => {
        allDeltas.push(pt.net - basePoint.net);
        allDeltas.push(pt.buy - basePoint.buy);
        allDeltas.push(pt.sell - basePoint.sell);
      });

      let minVal = Math.min(0, ...allDeltas);
      let maxVal = Math.max(0, ...allDeltas);
      if (minVal === maxVal) { minVal -= 20; maxVal += 20; }

      const span = maxVal - minVal;
      minVal -= span * 0.08;
      maxVal += span * 0.08;

      const getY = val => padTop + plotH - ((val - minVal) / (maxVal - minVal)) * plotH;
      const getX = idx => padLeft + (idx / (fullSeries.length - 1 || 1)) * plotW;

      // Draw Grid & Y-Axis Labels
      ctx.lineWidth = 1;
      const gridSteps = 5;
      for (let i = 0; i <= gridSteps; i++) {
        const v = minVal + (i / gridSteps) * (maxVal - minVal);
        const y = getY(v);

        ctx.strokeStyle = Math.abs(v) < 1 ? '#475569' : '#1e293b';
        ctx.setLineDash(Math.abs(v) < 1 ? [] : [3, 3]);
        ctx.beginPath();
        ctx.moveTo(padLeft, y);
        ctx.lineTo(width - padRight, y);
        ctx.stroke();

        ctx.setLineDash([]);
        ctx.fillStyle = Math.abs(v) < 1 ? '#94a3b8' : '#64748b';
        ctx.font = '9px monospace';
        ctx.textAlign = 'right';
        ctx.fillText(`£${v.toFixed(0)}`, padLeft - 6, y + 3);
      }

      // Zero Baseline line (Baseline reference)
      const zeroY = getY(0);
      ctx.strokeStyle = '#64748b';
      ctx.lineWidth = 1.2;
      ctx.beginPath();
      ctx.moveTo(padLeft, zeroY);
      ctx.lineTo(width - padRight, zeroY);
      ctx.stroke();

      // Vertical Baseline Marker on Canvas
      if (baselineFrameIndex > 0 && baselineFrameIndex < fullSeries.length) {
        const baseX = getX(baselineFrameIndex);
        ctx.strokeStyle = 'rgba(245, 158, 11, 0.7)';
        ctx.setLineDash([4, 2]);
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.moveTo(baseX, padTop);
        ctx.lineTo(baseX, height - padBottom);
        ctx.stroke();
        ctx.setLineDash([]);

        ctx.fillStyle = '#f59e0b';
        ctx.font = '8px monospace';
        ctx.textAlign = 'center';
        ctx.fillText('BASE', baseX, padTop - 6);
      }

      // Time labels along X-Axis
      const labelInterval = Math.max(1, Math.floor(fullSeries.length / 6));
      ctx.fillStyle = '#64748b';
      ctx.font = '9px monospace';
      ctx.textAlign = 'center';

      for (let i = 0; i < fullSeries.length; i += labelInterval) {
        const x = getX(i);
        ctx.fillText(fullSeries[i].time, x, height - padBottom + 14);
      }

      // Render Replayed Curves
      function drawSeriesLine(key, color, lineWidth, dash = []) {
        ctx.lineWidth = lineWidth;
        ctx.strokeStyle = color;
        ctx.setLineDash(dash);
        ctx.beginPath();

        visibleSeries.forEach((pt, idx) => {
          const delta = pt[key] - basePoint[key];
          const x = getX(idx);
          const y = getY(delta);
          if (idx === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.stroke();
        ctx.setLineDash([]);
      }

      // 1. Buy Net Delta (Cyan dashed)
      drawSeriesLine('buy', '#38bdf8', 1.8, [4, 3]);

      // 2. Sell Net Delta (Amber dashed)
      drawSeriesLine('sell', '#fbbf24', 1.8, [4, 3]);

      // 3. Total Net Delta (Emerald solid)
      drawSeriesLine('net', '#34d399', 2.8);

      // Current Head Marker Point
      if (visibleSeries.length) {
        const lastIdx = visibleSeries.length - 1;
        const lastPt = visibleSeries[lastIdx];
        const lastDelta = lastPt.net - basePoint.net;
        const headX = getX(lastIdx);
        const headY = getY(lastDelta);

        // Pulsing head circle
        ctx.fillStyle = '#34d399';
        ctx.beginPath();
        ctx.arc(headX, headY, 5, 0, Math.PI * 2);
        ctx.fill();

        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        ctx.arc(headX, headY, 5, 0, Math.PI * 2);
        ctx.stroke();

        // Label above head
        ctx.fillStyle = lastDelta >= 0 ? '#34d399' : '#f87171';
        ctx.font = 'bold 10px monospace';
        ctx.textAlign = 'center';
        ctx.fillText(
          `${lastDelta >= 0 ? '+£' : '-£'}${Math.abs(lastDelta).toFixed(0)}`,
          headX,
          Math.max(padTop + 10, headY - 10)
        );
      }
    }

    init();
  </script>
</body>
</html>
"""

full_html = html_template.replace("__DATA_JSON_PLACEHOLDER__", data_json)
target_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\mobile_winrate_replay_dashboard.html"

with open(target_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Generated mobile_winrate_replay_dashboard.html successfully! File size:", len(full_html))
