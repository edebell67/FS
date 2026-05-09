// This was a thought trace, not specific code replacement yet.



let chart;



let rawData = {}; // Full JSON from _summary_net.json



let activeKeys = []; // List of "Strategy|Product" keys to plot



const MAX_OVERLAYS = 10;



let refreshInterval;
let autoRefreshEnabled = true;
let nextRefreshTime = 0;
let isAutoRankingActive = false; // Persistent ranking mode

// Playback State
let isPlaybackMode = false;
let isPlaying = false;
let playbackTime = null; // Date object representing the current playback position
let playbackSpeed = 1; // Multiplier (1x, 10x, 100x etc.)
let playbackInterval = null;
let lastTickTime = null;
const speeds = [1, 10, 60, 300, 1800, 3600]; // Speed options 

let datasetEarliestTime = null;
let datasetLatestTime = null;
let currentStartTime = null;
let isStartTimeCustom = false;
let lastDataSignature = null;
let tradeBucketLimit = 5;
let overlayDeltas = {};
const currencyFormatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });







// Init Date



document.getElementById('tradeDate').valueAsDate = new Date();







// Color Palette



const colors = [



    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',



    '#ec4899', '#06b6d4', '#84cc16', '#fbbf24', '#6366f1'



];







function initEventHandlers() {



    const runModeSelect = document.getElementById('runMode');



    if (runModeSelect) {



        runModeSelect.addEventListener('change', fetchData);



    }



    const tradeDateInput = document.getElementById('tradeDate');



    if (tradeDateInput) {



        tradeDateInput.addEventListener('change', fetchData);



    }



    const metricSelect = document.getElementById('metricSelector');



    if (metricSelect) {



        metricSelect.addEventListener('change', updateChart);



    }



    const addButton = document.getElementById('addBtn');



    if (addButton) {



        addButton.addEventListener('click', addOverlay);



    }



    const rankButton = document.getElementById('rankApplyButton');



    if (rankButton) {



        rankButton.addEventListener('click', applyRankSelection);



    }



    const saveButton = document.getElementById('saveViewButton');



    if (saveButton) {



        saveButton.addEventListener('click', saveCurrentView);



    }



    const loadDropdown = document.getElementById('loadViewDropdown');



    if (loadDropdown) {



        loadDropdown.addEventListener('change', (event) => loadView(event.target.value));



    }
    const clearButton = document.getElementById('clearAllButton');
    if (clearButton) {
        clearButton.addEventListener('click', () => {
            isAutoRankingActive = false;
            clearAllOverlays();
        });
    }

    const deleteViewBtn = document.getElementById('deleteViewButton');
    if (deleteViewBtn) {
        deleteViewBtn.addEventListener('click', deleteView);
    }

    // Playback Handlers
    document.getElementById('playbackPlay').addEventListener('click', togglePlayback);
    document.getElementById('playbackReset').addEventListener('click', resetPlayback);
    document.getElementById('playbackSlower').addEventListener('click', slowerPlayback);
    document.getElementById('playbackFaster').addEventListener('click', fasterPlayback);
    document.getElementById('playbackEnd').addEventListener('click', endPlayback);
    document.getElementById('timeSlider').addEventListener('input', onSliderInput);
    document.getElementById('timeSlider').addEventListener('change', onSliderChange);

    const startTimeInput = document.getElementById('startTimeInput');
    if (startTimeInput) {
        startTimeInput.addEventListener('change', onStartTimeInputChange);
    }

    const displayButton = document.getElementById('displayButton');
    if (displayButton) {
        displayButton.addEventListener('click', displayCurrentSelection);
    }


    const tradeBucketButton = document.getElementById('tradeBucketButton');
    if (tradeBucketButton) {
        tradeBucketButton.addEventListener('click', createTradeBucket);
    }

    // 2026-01-19 03:41 - V20260119_0341: Reset start time button handler
    const resetStartTimeButton = document.getElementById('resetStartTimeButton');
    if (resetStartTimeButton) {
        resetStartTimeButton.addEventListener('click', resetStartTimeTo00);
    }

    // 2026-01-22 18:57 - [V20260122_1857]: Auto Refresh checkbox handler
    const autoRefreshCheck = document.getElementById('autoRefreshCheck');
    if (autoRefreshCheck) {
        autoRefreshCheck.addEventListener('change', (e) => {
            autoRefreshEnabled = e.target.checked;
            initAutoRefresh();
        });
    }
}

function initAutoRefresh() {
    if (refreshInterval) clearInterval(refreshInterval);
    if (autoRefreshEnabled && !isPlaying) {
        nextRefreshTime = Date.now() + 5000;
        refreshInterval = setInterval(() => {
            if (Date.now() >= nextRefreshTime) {
                fetchData();
                nextRefreshTime = Date.now() + 5000;
            }
            updateRefreshIndicator();
        }, 1000);
    }
}

function updateRefreshIndicator() {
    const label = document.querySelector('label[for="autoRefreshCheck"]');
    if (!label) return;
    if (autoRefreshEnabled && !isPlaying) {
        const remaining = Math.max(0, Math.ceil((nextRefreshTime - Date.now()) / 1000));
        label.innerText = `Auto (${remaining}s)`;
    } else {
        label.innerText = 'Auto';
    }
}




async function fetchData() {



    const mode = document.getElementById('runMode').value;
    const date = document.getElementById('tradeDate').value;
    const signature = `${mode}|${date}`;
    const datasetChanged = signature !== lastDataSignature;

    // [V20260122_FS] Updated to use file-based summary endpoint
    const url = `/api/trade_file?mode=${mode}&date=${date}&filename=_summary_net.json&_t=${Date.now()}`;

    try {

        const res = await fetch(url);


        const json = await res.json();

        if (json.success) {
            if (datasetChanged) {
                lastDataSignature = signature;
                currentStartTime = null;
                isStartTimeCustom = false;
            }

            rawData = json.content;
            document.getElementById('lastUpdate').innerText = new Date().toLocaleTimeString();

            // Initialize playback time if not set
            if (!playbackTime) {
                const { endOfDay } = getPlaybackBoundaries();
                playbackTime = new Date(endOfDay.getTime());
            }
            updatePlaybackUI();

            updateDatasetTimeBounds();
            populateSelectors();

            // [V20260123_0020] Persistent Auto-Ranking
            if (isAutoRankingActive) {
                applyRankSelection(false); // Don't alert on auto
            } else {
                updateChart();
            }

        } else {

            console.warn("Failed to load summary data:", json.message);

            rawData = {};
            updateDatasetTimeBounds();
            updateChart(); // Clear chart if failed

        }


    } catch (e) {

        console.error("Fetch error:", e);

    }



}







function populateSelectors() {



    const prodSel = document.getElementById('productSelector');



    const stratSel = document.getElementById('strategySelector');



    const parmSel = document.getElementById('paramSelector');







    // Preserve current selections if possible



    const currProd = prodSel.value;



    const currStrat = stratSel.value;



    const currParm = parmSel.value;







    const products = new Set();



    const strategies = new Set();



    const params = new Set();







    if (rawData.strategies) {



        for (const [stratName, prodMap] of Object.entries(rawData.strategies)) {



            // Split Strategy / Params



            // Heuristic: Split at first "_tp" if present, else use full name or custom split



            let baseStrat = stratName;



            let parm = "Default";







            const tpIndex = stratName.indexOf('_tp');



            if (tpIndex !== -1) {



                baseStrat = stratName.substring(0, tpIndex);



                parm = stratName.substring(tpIndex + 1); // remove leading _



            }







            strategies.add(baseStrat);



            params.add(parm);







            Object.keys(prodMap).forEach(p => products.add(p));



        }



    }







    // Populate Product



    updateSelectOptions(prodSel, Array.from(products).sort(), currProd);



    // Populate Strategy



    updateSelectOptions(stratSel, Array.from(strategies).sort(), currStrat);



    // Populate Params



    updateSelectOptions(parmSel, Array.from(params).sort(), currParm);



}







function updateSelectOptions(selectElement, optionsArray, currentValue) {



    selectElement.innerHTML = '<option value="">-- Select --</option>';



    optionsArray.forEach(opt => {



        const el = document.createElement('option');



        el.value = opt;



        el.textContent = opt;



        selectElement.appendChild(el);



    });



    if (currentValue && optionsArray.includes(currentValue)) {



        selectElement.value = currentValue;



    }



}







function addOverlay() {



    const prod = document.getElementById('productSelector').value;



    const strat = document.getElementById('strategySelector').value;



    const parm = document.getElementById('paramSelector').value;







    if (!prod || !strat) return; // Parm can be optional/default







    // Reconstruct full strategy name



    let fullStratName = strat;



    if (parm && parm !== "Default") {



        fullStratName = `${strat}_${parm}`;



    }







    // Verify existence



    if (!rawData.strategies?.[fullStratName]?.[prod]) {



        alert(`No data found for:\nStrategy: ${fullStratName}\nProduct: ${prod}`);



        return;



    }







    const key = `${fullStratName} | ${prod}`;







    if (activeKeys.includes(key)) {



        alert("Already added!");



        return;



    }



    if (activeKeys.length >= MAX_OVERLAYS) {



        alert(`Max ${MAX_OVERLAYS} overlays allowed.`);



        return;



    }







    isAutoRankingActive = false; // V20260123_0950: Disable auto-ranking on manual selection
    activeKeys.push(key);



    renderActiveTags();



    updateChart();



}







function removeOverlay(key) {
    isAutoRankingActive = false; // V20260123_0950: Disable auto-ranking on manual removal
    activeKeys = activeKeys.filter(k => k !== key);
    delete overlayDeltas[key];
    renderActiveTags();
    updateChart();
}









function renderActiveTags() {
    const container = document.getElementById('activeOverlays');
    container.innerHTML = '';

    activeKeys.forEach((key, idx) => {
        const color = colors[idx % colors.length];
        const div = document.createElement('div');
        div.className = 'active-item';
        div.style.borderColor = color;
        div.style.background = `${color}33`;
        div.dataset.overlayKey = key;
        div.style.display = 'flex';
        div.style.alignItems = 'center';

        const indicator = document.createElement('span');
        indicator.style.width = '8px';
        indicator.style.height = '8px';
        indicator.style.borderRadius = '50%';
        indicator.style.background = color;
        indicator.style.display = 'inline-block';
        indicator.style.marginRight = '6px';

        const label = document.createElement('span');
        label.textContent = key;
        label.style.flex = '1';
        label.style.marginRight = '8px';

        const valueSpan = document.createElement('span');
        valueSpan.className = 'overlay-value';
        valueSpan.dataset.overlayKey = key;
        valueSpan.style.marginRight = '8px';
        valueSpan.style.fontFamily = 'Courier New, monospace';
        valueSpan.style.fontSize = '0.85em';
        valueSpan.textContent = '--';

        const removeIcon = document.createElement('i');
        removeIcon.className = 'fas fa-times';
        removeIcon.style.cursor = 'pointer';
        removeIcon.addEventListener('click', () => removeOverlay(key));

        div.appendChild(indicator);
        div.appendChild(label);
        div.appendChild(valueSpan);
        div.appendChild(removeIcon);
        container.appendChild(div);
    });

    updateOverlayDeltaDisplay();
}









function getLocalDateFromInput(dateStr) {



    if (!dateStr) {



        return null;



    }



    const parts = dateStr.split('-').map(Number);



    if (parts.length !== 3 || parts.some(isNaN)) {



        return null;



    }



    return new Date(parts[0], parts[1] - 1, parts[2]);



}



function formatTimeForInput(dateObj) {
    if (!dateObj) return '';
    return dateObj.toISOString().substring(11, 19);
}

function parseTimeInput(value) {
    const dateVal = document.getElementById('tradeDate').value;
    if (!value || !dateVal) {
        return null;
    }
    const normalized = value.length === 5 ? `${value}:00` : value;
    return new Date(`${dateVal}T${normalized}Z`);
}

function updateDatasetTimeBounds() {
    let earliest = null;
    let latest = null;

    if (rawData.strategies) {
        for (const strat in rawData.strategies) {
            const prodMap = rawData.strategies[strat] || {};
            for (const prod in prodMap) {
                const series = prodMap[prod] || [];
                series.forEach(pt => {
                    if (!pt || !pt.t) return;
                    const iso = pt.t.endsWith('Z') ? pt.t : pt.t + 'Z';
                    const ts = new Date(iso);
                    if (!earliest || ts < earliest) {
                        earliest = ts;
                    }
                    if (!latest || ts > latest) {
                        latest = ts;
                    }
                });
            }
        }
    }

    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    const minCandidate = earliest ? Math.min(earliest.getTime(), startOfDay.getTime()) : startOfDay.getTime();
    const maxCandidate = latest ? Math.max(latest.getTime(), startOfDay.getTime()) : endOfDay.getTime();

    datasetEarliestTime = new Date(minCandidate);
    datasetLatestTime = new Date(maxCandidate);

    if (!earliest || !latest) {
        currentStartTime = null;
        isStartTimeCustom = false;
    }

    updateStartTimeUI();
}

function updateStartTimeUI() {
    const input = document.getElementById('startTimeInput');
    const rangeLabel = document.getElementById('startTimeRangeLabel');

    if (!input || !rangeLabel) {
        return;
    }

    if (!datasetEarliestTime || !datasetLatestTime) {
        input.value = '';
        input.disabled = true;
        input.removeAttribute('min');
        input.removeAttribute('max');
        rangeLabel.innerText = '--:--:-- -> --:--:--';
        return;
    }

    input.disabled = false;
    const minStr = formatTimeForInput(datasetEarliestTime);
    const maxStr = formatTimeForInput(datasetLatestTime);
    input.min = minStr;
    input.max = maxStr;
    rangeLabel.innerText = `${minStr} -> ${maxStr}`;

    if (!currentStartTime || !isStartTimeCustom) {
        currentStartTime = new Date(datasetEarliestTime.getTime());
    }

    if (currentStartTime < datasetEarliestTime) {
        currentStartTime = new Date(datasetEarliestTime.getTime());
    }
    if (currentStartTime > datasetLatestTime) {
        currentStartTime = new Date(datasetLatestTime.getTime());
    }

    input.value = formatTimeForInput(currentStartTime);
}

function onStartTimeInputChange(e) {
    if (!datasetEarliestTime || !datasetLatestTime) {
        return;
    }

    const desired = parseTimeInput(e.target.value);
    if (!desired) {
        updateStartTimeUI();
        return;
    }

    let clamped = desired;
    if (clamped < datasetEarliestTime) {
        clamped = new Date(datasetEarliestTime.getTime());
    }
    if (clamped > datasetLatestTime) {
        clamped = new Date(datasetLatestTime.getTime());
    }

    currentStartTime = clamped;
    isStartTimeCustom = true;
    updateStartTimeUI();
    updateChart();
}

function getActiveStartTime() {
    if (currentStartTime) {
        return currentStartTime;
    }

    if (datasetEarliestTime) {
        return datasetEarliestTime;
    }

    const { startOfDay } = getPlaybackBoundaries();
    return startOfDay;
}

// 2026-01-19 03:41 - V20260119_0341: Reset start time to 00:00:00
function resetStartTimeTo00() {
    const { startOfDay } = getPlaybackBoundaries();
    currentStartTime = new Date(startOfDay.getTime());
    isStartTimeCustom = true;
    updateStartTimeUI();
    updateChart();
}



async function displayCurrentSelection() {
    isAutoRankingActive = false; // V20260123_0955: Manual refresh preserves current view
    await fetchData();
}


function resolveMetricField(metric) {
    if (metric === 'buy_trades') return 'buy_net';
    if (metric === 'sell_trades') return 'sell_net';
    return metric;
}

function computeSeriesDelta(series, metricField, startMs, evalMs) {
    if (!Array.isArray(series) || series.length === 0) {
        return null;
    }

    const sanitized = series.map(pt => {
        if (!pt || !pt.t) return null;
        const iso = pt.t.endsWith('Z') ? pt.t : pt.t + 'Z';
        const ts = new Date(iso).getTime();
        if (Number.isNaN(ts)) return null;
        const value = Number(pt[metricField]) || 0;
        return { ms: ts, value };
    }).filter(Boolean).sort((a, b) => a.ms - b.ms);

    if (sanitized.length === 0) {
        return null;
    }

    const baselineTarget = Math.max(0, startMs);
    const evalTarget = Math.max(baselineTarget, evalMs);

    let baseline = 0;
    let current = sanitized[0].value;

    sanitized.forEach(point => {
        if (point.ms <= baselineTarget) {
            baseline = point.value;
        }
        if (point.ms <= evalTarget) {
            current = point.value;
        }
    });

    return current - baseline;
}



function formatOverlayDelta(value) {
    if (typeof value !== 'number' || Number.isNaN(value)) {
        return '--';
    }
    if (value === 0) {
        return currencyFormatter.format(0);
    }
    const formatted = currencyFormatter.format(Math.abs(value));
    return `${value > 0 ? '+' : '-'}${formatted}`;
}

function getSeriesValueAtTime(series, metricField, targetMs) {
    if (!Array.isArray(series) || series.length === 0) {
        return 0;
    }

    let value = null;
    series.forEach(pt => {
        if (!pt || !pt.t) return;
        const iso = pt.t.endsWith('Z') ? pt.t : pt.t + 'Z';
        const ts = new Date(iso).getTime();
        if (Number.isNaN(ts)) return;
        if (ts <= targetMs) {
            value = Number(pt[metricField]) || 0;
        }
    });

    if (value === null) {
        return 0;
    }
    return value;
}



function updateOverlayDeltaDisplay() {
    document.querySelectorAll('.overlay-value').forEach(node => {
        const key = node.dataset.overlayKey;
        const val = overlayDeltas[key];
        node.textContent = formatOverlayDelta(val);
        if (typeof val === 'number') {
            node.style.color = val > 0 ? '#10b981' : val < 0 ? '#ef4444' : '#e0e0e0';
        } else {
            node.style.color = '#e0e0e0';
        }
    });
}


async function fetchTradeBucketMeta() {
    try {
        const resp = await fetch('/api/trade_buckets');
        if (!resp.ok) {
            throw new Error(`HTTP ${resp.status}`);
        }
        const data = await resp.json();
        if (data.success && typeof data.max_strategies === 'number') {
            tradeBucketLimit = data.max_strategies;
        }
    } catch (err) {
        console.warn('Failed to load trade bucket metadata', err);
    }
}




function updateChart(filterTime = null) {
    const metric = document.getElementById('metricSelector').value; // net, buy_net, sell_net, buy_trades, sell_trades
    const ctx = document.getElementById('pnlChart').getContext('2d');

    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    const startBoundary = getActiveStartTime() || startOfDay;
    const startBoundaryIso = startBoundary.toISOString();
    const startBoundaryMs = startBoundary.getTime();

    const playbackFilterTime = filterTime || (isPlaying ? playbackTime : null);
    let axisMaxDate = playbackFilterTime || datasetLatestTime || endOfDay;
    if (axisMaxDate.getTime() < startBoundaryMs) {
        axisMaxDate = new Date(startBoundaryMs);
    }
    const axisMaxIso = axisMaxDate.toISOString();
    const axisMaxMs = axisMaxDate.getTime();

    const datasets = [];
    const computedOverlayDeltas = {};

    const allTimestamps = new Set([startBoundaryIso, axisMaxIso]);

    activeKeys.forEach((key, idx) => {
        const [strat, prod] = key.split(' | ');
        const series = rawData.strategies?.[strat]?.[prod] || [];

        if (series.length === 0) {
            computedOverlayDeltas[key] = null;
            return;
        }

        const sorted = [...series].map(pt => {
            let yVal = 0;
            if (metric === 'buy_trades') yVal = pt.buy_net || 0;
            else if (metric === 'sell_trades') yVal = pt.sell_net || 0;
            else yVal = pt[metric] || 0;

            const iso = pt.t.endsWith('Z') ? pt.t : pt.t + 'Z';
            return {
                x: iso,
                y: yVal,
                ms: new Date(iso).getTime()
            };
        }).sort((a, b) => a.ms - b.ms);

        if (sorted.length === 0) {
            return;
        }

        // 2026-01-19 03:57 - V20260119_0357: Start at $0 at start time, show cumulative from there
        const filtered = [];

        sorted.forEach(pt => {
            if (pt.ms >= startBoundaryMs && pt.ms <= axisMaxMs) {
                filtered.push(pt);
            }
        });

        if (filtered.length === 0) {
            return;
        }

        // 2026-01-19 04:24 - V20260119_0424: Calculate baseline for delta display
        // Find the value at or before the start time to use as baseline
        let baselineValue = 0;
        sorted.forEach(pt => {
            if (pt.ms <= startBoundaryMs) {
                baselineValue = pt.y;
            }
        });

        // 2026-01-19 04:10 - V20260119_0410: Manually create stepped points for correct rendering
        // Add $0 point at start time
        const steppedData = [{
            x: startBoundaryIso,
            y: 0,
            ms: startBoundaryMs
        }];

        // For each actual data point, subtract baseline to show delta
        filtered.forEach((pt, idx) => {
            // Add the actual point with baseline subtracted
            steppedData.push({
                x: pt.x,
                y: pt.y - baselineValue,  // Show delta from start time
                ms: pt.ms
            });
        });

        const normalized = steppedData;


        const lastPoint = normalized[normalized.length - 1];
        if (lastPoint.ms < axisMaxMs) {
            normalized.push({
                x: axisMaxIso,
                y: lastPoint.y,
                ms: axisMaxMs
            });
        }

        normalized.forEach(pt => allTimestamps.add(pt.x));
        computedOverlayDeltas[key] = normalized[normalized.length - 1].y;

        datasets.push({
            label: key,
            data: normalized.map(pt => ({ x: pt.x, y: pt.y })),
            borderColor: colors[idx % colors.length],
            backgroundColor: 'transparent',
            borderWidth: 2,
            stepped: true, // 2026-01-19 04:16 - V20260119_0416: Changed to true to fix value display
            pointRadius: 0
        });
    });

    overlayDeltas = {};
    activeKeys.forEach(key => {
        overlayDeltas[key] = Object.prototype.hasOwnProperty.call(computedOverlayDeltas, key) ? computedOverlayDeltas[key] : null;
    });

    const sortedLabels = Array.from(allTimestamps).sort((a, b) => new Date(a) - new Date(b));

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: sortedLabels, // Explicitly define the X-axis categories in order
            datasets: datasets
        },
        options: {
            animation: {
                duration: 400,
                easing: 'easeOutQuart'
            },
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                mode: 'nearest',
                intersect: false
            },
            plugins: {
                decimation: {
                    enabled: true,
                    algorithm: 'lttb',
                    samples: 1000
                },
                legend: { display: false },
                tooltip: {
                    backgroundColor: 'rgba(15, 18, 37, 0.9)',
                    titleFont: { family: 'Outfit', size: 14, weight: 'bold' },
                    bodyFont: { family: 'Outfit', size: 13 },
                    padding: 12,
                    cornerRadius: 12,
                    borderColor: 'rgba(255, 255, 255, 0.1)',
                    borderWidth: 1,
                    displayColors: true,
                    callbacks: {
                        label: function (context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'time',
                    display: true,
                    time: {
                        unit: 'minute',
                        displayFormats: {
                            minute: 'HH:mm',
                            hour: 'HH:mm'
                        },
                        tooltipFormat: 'HH:mm:ss'
                    },
                    min: startBoundaryIso,
                    max: axisMaxIso,
                    ticks: {
                        maxTicksLimit: 10,
                        color: 'rgba(255, 255, 255, 0.5)',
                        font: { family: 'Outfit', size: 11 }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.03)',
                        drawBorder: false
                    }
                },
                y: {
                    display: true,
                    ticks: {
                        color: 'rgba(255, 255, 255, 0.5)',
                        font: { family: 'Outfit', size: 11 }
                    },
                    grid: {
                        color: 'rgba(255, 255, 255, 0.03)',
                        drawBorder: false
                    }
                }
            }
        }
    });
    updateOverlayDeltaDisplay();
}











// --- New Logic for Ranking and Views ---








function applyRankSelection(manual = true) {
    if (manual) isAutoRankingActive = true;
    const rankTypeEl = document.getElementById('rankType');
    const rankCountEl = document.getElementById('rankCount');
    const metricSelect = document.getElementById('metricSelector');

    if (!rankTypeEl || !rankCountEl || !metricSelect) {
        updateChart();
        return false;
    }

    const rankType = (rankTypeEl.value || 'top').toLowerCase();
    const requestedCount = parseInt(rankCountEl.value, 10) || 5;
    const count = Math.min(MAX_OVERLAYS, Math.max(1, requestedCount));
    const metric = metricSelect.value || 'net';

    if (!rawData.strategies) {
        alert('Strategy data not loaded yet. Fetch data first.');
        return false;
    }

    const startBoundary = getActiveStartTime() || new Date();
    const startMs = startBoundary.getTime();
    const evalTime = playbackTime || new Date();
    const evalMs = Math.max(startMs, evalTime.getTime());
    const metricField = resolveMetricField(metric);

    const candidates = [];

    for (const strat in rawData.strategies) {
        const products = rawData.strategies[strat];
        if (!products) continue;
        for (const prod in products) {
            const series = products[prod];
            const delta = computeSeriesDelta(series, metricField, startMs, evalMs);
            if (delta === null) continue;
            candidates.push({ key: `${strat} | ${prod}`, value: delta });
        }
    }

    if (candidates.length === 0) {
        alert('No ranking candidates available for the selected metric.');
        return false;
    }

    candidates.sort((a, b) => a.value - b.value);
    const ordered = rankType === 'bottom' ? candidates : [...candidates].reverse();
    const selected = ordered.slice(0, count);

    if (selected.length === 0) {
        alert('Unable to find strategies to display.');
        return false;
    }

    activeKeys = selected.map(item => item.key);
    overlayDeltas = {};
    renderActiveTags();
    updateChart();
    return true;
}








function clearAllOverlays() {
    activeKeys = [];
    overlayDeltas = {};
    renderActiveTags();
    updateChart();
}








function saveCurrentView(nameOverride = null, silent = false) {
    // 2026-01-19 04:43 - V20260119_0443: Ignore event objects
    let name = nameOverride;
    if (name && typeof name === 'object') {
        // nameOverride is an event object, ignore it
        name = null;
    }

    if (!name) {
        const input = document.getElementById('viewNameInput');
        if (input) name = input.value.trim();
    }

    if (!name) {
        if (!silent) alert('Please enter a view name');
        return;
    }

    if (activeKeys.length === 0) {
        if (!silent) alert('No overlays to save');
        return;
    }

    const views = JSON.parse(localStorage.getItem('pnl_graph_views') || '{}');

    views[name] = {
        keys: activeKeys,
        metric: document.getElementById('metricSelector').value,
        startTime: currentStartTime ? currentStartTime.toISOString() : null
    };

    localStorage.setItem('pnl_graph_views', JSON.stringify(views));

    if (!silent) {
        alert(`View "${name}" saved!`);
    }

    populateSavedViews();
}








function loadView(name) {

    if (!name) return;

    const views = JSON.parse(localStorage.getItem('pnl_graph_views') || '{}');

    const view = views[name];

    if (view) {
        isAutoRankingActive = false; // V20260123_0955: Reset auto-ranking when loading a preset
        activeKeys = view.keys || [];

        if (view.metric) {

            document.getElementById('metricSelector').value = view.metric;

        }

        if (view.startTime) {

            currentStartTime = new Date(view.startTime);

            isStartTimeCustom = true;

        } else {

            isStartTimeCustom = false;

            currentStartTime = datasetEarliestTime ? new Date(datasetEarliestTime.getTime()) : null;

        }

        updateStartTimeUI();

        renderActiveTags();

        updateChart();

    }

}






function deleteView() {

    const dropdown = document.getElementById('loadViewDropdown');

    const name = dropdown.value;



    if (!name) {

        alert('Please select a view to delete');

        return;

    }



    if (!confirm(`Are you sure you want to delete the view "${name}"?`)) {

        return;

    }



    const views = JSON.parse(localStorage.getItem('pnl_graph_views') || '{}');



    if (views[name]) {

        delete views[name];

        localStorage.setItem('pnl_graph_views', JSON.stringify(views));

        alert(`View "${name}" deleted successfully!`);



        // Reset dropdown and refresh the list

        dropdown.value = '';

        populateSavedViews();

    } else {

        alert(`View "${name}" not found`);

    }

}

// --- Playback Logic ---

function getPlaybackBoundaries() {
    const dateVal = document.getElementById('tradeDate').value;
    const now = new Date();
    // Use UTC for todayStr to match the folder/file names
    const todayStr = now.getUTCFullYear() + '-' +
        String(now.getUTCMonth() + 1).padStart(2, '0') + '-' +
        String(now.getUTCDate()).padStart(2, '0');

    const isToday = (dateVal === todayStr);

    const startOfDay = new Date(dateVal + 'T00:00:00Z');
    let endOfDay;
    if (isToday) {
        endOfDay = new Date(); // Right now (server/browser local sync - ideally UTC)
    } else {
        endOfDay = new Date(dateVal + 'T23:59:59Z');
    }
    return { startOfDay, endOfDay, isToday };
}

function updatePlaybackUI() {
    if (!playbackTime) return;

    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    const currentLocal = new Date(playbackTime.getTime());

    // Update Clock (Digital)
    const clock = document.getElementById('playbackClock');
    if (clock) clock.innerText = currentLocal.toLocaleTimeString([], { hour12: false });

    // Update Slider
    const startTs = startOfDay.getTime();
    const endTs = endOfDay.getTime();
    const currentTs = playbackTime.getTime();

    const slider = document.getElementById('timeSlider');
    slider.min = 0;
    slider.max = Math.max(1, Math.floor((endTs - startTs) / 1000));
    slider.value = Math.floor((currentTs - startTs) / 1000);

    // Update Labels
    document.getElementById('startTimeLabel').innerText = startOfDay.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
    document.getElementById('endTimeLabel').innerText = endOfDay.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
}

function togglePlayback() {
    isPlaying = !isPlaying;
    const btn = document.getElementById('playbackPlay');

    if (isPlaying) {
        btn.innerHTML = '<i class="fas fa-pause"></i> Pause';
        btn.classList.add('active');
        isPlaybackMode = true;

        // Disable auto-refresh when playback starts
        if (refreshInterval) {
            clearInterval(refreshInterval);
            refreshInterval = null;
        }

        lastTickTime = Date.now();
        playbackInterval = setInterval(playbackTick, 100); // 10 ticks per second
    } else {
        btn.innerHTML = '<i class="fas fa-play"></i> Play';
        btn.classList.remove('active');
        if (playbackInterval) {
            clearInterval(playbackInterval);
            playbackInterval = null;
        }
        initAutoRefresh();
    }
}

function playbackTick() {
    if (!isPlaying || !playbackTime) return;

    const now = Date.now();
    const deltaMs = (now - lastTickTime) * playbackSpeed;
    lastTickTime = now;

    const { endOfDay } = getPlaybackBoundaries();

    // Incremental jump
    const nextTime = new Date(playbackTime.getTime() + deltaMs);

    if (nextTime >= endOfDay) {
        playbackTime = new Date(endOfDay.getTime());
        isPlaying = false;
        const btn = document.getElementById('playbackPlay');
        btn.innerHTML = '<i class="fas fa-play"></i> Play';
        btn.classList.remove('active');
        if (playbackInterval) {
            clearInterval(playbackInterval);
            playbackInterval = null;
        }
        initAutoRefresh();
    } else {
        playbackTime = nextTime;
    }

    updatePlaybackUI();
    updateChart(playbackTime);
}

function resetPlayback() {
    const { startOfDay } = getPlaybackBoundaries();
    playbackTime = new Date(startOfDay.getTime());
    isPlaybackMode = true;
    updatePlaybackUI();
    updateChart(playbackTime);
}

function endPlayback() {
    const { endOfDay } = getPlaybackBoundaries();
    playbackTime = new Date(endOfDay.getTime());
    isPlaybackMode = true;
    updatePlaybackUI();
    updateChart(playbackTime);
}

function slowerPlayback() {
    const currIdx = speeds.indexOf(playbackSpeed);
    if (currIdx > 0) {
        playbackSpeed = speeds[currIdx - 1];
    } else {
        playbackSpeed = 1;
    }
    const badge = document.getElementById('playbackSpeedBadge');
    if (badge) badge.innerText = playbackSpeed + 'x SPEED';
}

function fasterPlayback() {
    const currIdx = speeds.indexOf(playbackSpeed);
    if (currIdx < speeds.length - 1) {
        playbackSpeed = speeds[currIdx + 1];
    } else {
        playbackSpeed = speeds[speeds.length - 1];
    }
    const badge = document.getElementById('playbackSpeedBadge');
    if (badge) badge.innerText = playbackSpeed + 'x SPEED';
}

function onSliderInput(e) {
    const secondsOffset = parseInt(e.target.value);
    const { startOfDay } = getPlaybackBoundaries();
    playbackTime = new Date(startOfDay.getTime() + secondsOffset * 1000);
    isPlaybackMode = true;
    updatePlaybackUI();
}

function onSliderChange(e) {
    updateChart(playbackTime);
}



function populateSavedViews() {



    const dropdown = document.getElementById('loadViewDropdown');



    dropdown.innerHTML = '<option value="">-- Load View --</option>';



    const views = JSON.parse(localStorage.getItem('pnl_graph_views') || '{}');



    Object.keys(views).forEach(name => {



        const opt = document.createElement('option');



        opt.value = name;



        opt.innerText = name;



        dropdown.appendChild(opt);



    });



}







// [V20260118_0230] Trade Bucket Features
async function fetchTradeBucketMeta() {
    try {
        const res = await fetch('/api/trade_buckets');
        const json = await res.json();
        if (json.success) {
            tradeBucketLimit = json.max_strategies || 5;
        }
    } catch (e) {
        console.error("Error fetching bucket meta:", e);
    }
}

async function createTradeBucket() {
    if (activeKeys.length === 0) {
        alert("No active overlays to create a bucket from.");
        return;
    }

    // Check limit
    if (activeKeys.length > tradeBucketLimit) {
        alert(`Cannot create bucket: Too many strategies (${activeKeys.length}). Max limit is ${tradeBucketLimit}.`);
        return;
    }

    const name = prompt("Enter a name for this Trade Bucket:", `Bucket_${new Date().toISOString().slice(0, 10).replace(/-/g, '')}`);
    if (!name) return;

    // Use current graph start time if set, otherwise dataset earliest, or now as fallback
    let startTime = new Date().toISOString();
    if (currentStartTime) {
        // currentStartTime is a Date object (if set from UI)
        startTime = currentStartTime.toISOString();
    } else if (datasetEarliestTime) {
        startTime = datasetEarliestTime.toISOString();
    }

    // Parse keys back to strategy objects with current P&L values
    const strategies = activeKeys.map(key => {
        const [stratFull, prod] = key.split(' | ');
        return {
            strategy: stratFull,
            product: prod,
            key: key,
            total_net: overlayDeltas[key] || 0  // 2026-01-19 04:36 - V20260119_0436: Include current P&L value
        };
    });

    const runMode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';

    // DEBUG: Confirm values
    console.log(`Creating bucket: ${name}, Mode: ${runMode}, Start: ${startTime}`);
    console.log('overlayDeltas:', overlayDeltas);
    console.log('strategies with total_net:', strategies);


    try {
        const res = await fetch('/api/trade_buckets', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                name: name,
                strategies: strategies,
                start_time: startTime,
                mode: runMode
            })
        });

        const json = await res.json();
        if (json.success) {
            // Auto-save view for this bucket
            const viewName = `TB_${name}`;
            saveCurrentView(viewName, true);

            alert(`Bucket "${name}" created and View "${viewName}" saved successfully!\nStart Time: ${startTime}`);
        } else {
            alert(`Failed to create bucket: ${json.message}`);
        }
    } catch (e) {
        alert(`Error: ${e.message}`);
    }
}


// Init saved views on load



window.addEventListener('load', () => {
    populateSavedViews();
    initEventHandlers();
    updatePlaybackUI();
    updateStartTimeUI();
    fetchTradeBucketMeta();
});







// Init



// [V20260122_1857]: Initial data fetch and auto-refresh start
fetchData();
initAutoRefresh();









