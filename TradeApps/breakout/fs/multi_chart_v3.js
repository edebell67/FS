// [V20260126_1230] Multi-Chart V3 - Playback-Aware Ranking & Live Grid Toggle
// State
let charts = {}; // Map of Group Names to Chart instances
let rawData = []; // Flat list from SQL API
let processedSeries = {};
let activeOverlays = []; // Array of { key: "model|prod", group: "GroupName", color: "hex", metric: "net_return_sum/alt_net_return_sum" }
let firstRankOneTimes = {}; // [V20260202_1330] Map of "strat|prod" -> timestamp (ms) of first Rank #1
const MAX_OVERLAYS = 100;

let refreshInterval;
let autoRefreshEnabled = true;
let nextRefreshTime = 0;
let isAutoRankingActive = false;

// Playback State
let isPlaying = false;
let playbackTime = null;
let playbackSpeed = 1;
let playbackInterval = null;
let lastTickTime = null;
const speeds = [1, 10, 60, 300, 1800, 3600];

let datasetEarliestTime = null;
let datasetLatestTime = null;
let currentStartTime = null;
let isStartTimeCustom = false;
let lastDataSignature = null;
const selectedPresetNames = new Set();
let loadedBuckets = [];
const currencyFormatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

// Init Date
document.getElementById('tradeDate').valueAsDate = new Date();

const colors = [
    '#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa',
    '#f472b6', '#22d3ee', '#a3e635', '#fb923c', '#818cf8',
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'
];

function getCurrentWorkflowImportProductTypeV3(payload) {
    const params = new URLSearchParams(window.location.search || '');
    const queryValue = String(params.get('product_type') || '').trim().toLowerCase();
    if (queryValue) return queryValue;
    const payloadType = String(payload?.product_type || '').trim().toLowerCase();
    if (payloadType) return payloadType;
    const firstPayloadType = String((Array.isArray(payload?.product_types) ? payload.product_types[0] : '') || '').trim().toLowerCase();
    if (firstPayloadType) return firstPayloadType;
    const firstItemType = String(payload?.items?.[0]?.product_type || '').trim().toLowerCase();
    return firstItemType || 'forex';
}

function buildWorkflowImportPresetNameV3(baseName, productType) {
    const cleanBase = String(baseName || '').trim() || `WF_PROFILE_${new Date().toISOString().slice(0, 10)}`;
    const cleanType = String(productType || '').trim().toLowerCase();
    return cleanType ? `${cleanBase} [${cleanType.toUpperCase()}]` : cleanBase;
}


function getMetricValueV3(pt, metric) {
    if (!pt) return 0;
    if (metric === 'alt' || metric === 'alt_net_return_sum') return pt.alt ?? 0;
    if (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') return pt.buy_net ?? pt.buy ?? 0;
    if (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') return pt.sell_net ?? pt.sell ?? 0;
    return pt.net ?? 0;
}

function buildSteppedSeriesV3(series, metric, startMs, axisMaxMs) {
    let baseline = 0;
    let lastVal = 0;
    const data = [{ x: startMs, y: 0 }];
    for (const pt of series) {
        const val = getMetricValueV3(pt, metric);
        if (pt.ms <= startMs) {
            baseline = val;
            continue;
        }
        if (pt.ms > axisMaxMs) break;
        const delta = val - baseline;
        data.push({ x: pt.ms, y: lastVal });
        data.push({ x: pt.ms, y: delta });
        lastVal = delta;
    }
    data.push({ x: axisMaxMs, y: lastVal });
    return data;
}

function ensureGroupCharts(groupName) {
    if (!charts[groupName]) charts[groupName] = { net: null, buy: null, sell: null };
    return charts[groupName];
}

function destroyGroupCharts(groupName) {
    const entry = charts[groupName];
    if (!entry) return;
    ['net', 'buy', 'sell'].forEach(slot => {
        if (entry[slot]) {
            entry[slot].destroy();
            entry[slot] = null;
        }
    });
    delete charts[groupName];
}

function getGroupSplitState(groupName) {
    const configs = activeOverlays.filter(o => o.group === groupName);
    
    if (configs.length === 1) {
        const metric = configs[0].metric;
        if (!metric || metric === 'net' || metric === 'global') {
            return { action: 'split', label: 'Split Chart', icon: 'fa-columns' };
        }
    }
    
    // Check if it's exactly 2 overlays, one buy_net and one sell_net
    if (configs.length === 2) {
        const metrics = configs.map(c => c.metric);
        const hasBuy = metrics.includes('buy_net') || metrics.includes('buy');
        const hasSell = metrics.includes('sell_net') || metrics.includes('sell');
        if (hasBuy && hasSell) {
            return { action: 'combo', label: 'Combo Chart', icon: 'fa-compress' };
        }
    }
    return null;
}

function handleSplitComboAction(event, groupName) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    const state = getGroupSplitState(groupName);
    if (!state) return;
    
    const configs = activeOverlays.filter(o => o.group === groupName);
    if (configs.length === 0) return;
    
    const newOverlays = [];
    let groupHandled = false;
    
    for (let i = 0; i < activeOverlays.length; i++) {
        const o = activeOverlays[i];
        if (o.group === groupName) {
            if (!groupHandled) {
                groupHandled = true;
                if (state.action === 'split') {
                    newOverlays.push({
                        key: configs[0].key,
                        group: groupName,
                        metric: 'buy_net',
                        color: '#10b981', // green for buy
                        isLive: configs[0].isLive,
                        _originalColor: configs[0].color
                    });
                    newOverlays.push({
                        key: configs[0].key,
                        group: groupName,
                        metric: 'sell_net',
                        color: '#ef4444', // red for sell
                        isLive: configs[0].isLive,
                        _originalColor: configs[0].color
                    });
                } else if (state.action === 'combo') {
                    const overlayKey = configs[0].key;
                    const isLive = configs.some(c => c.isLive);
                    const restoredColor = configs[0]._originalColor || colors[newOverlays.length % colors.length];
                    
                    newOverlays.push({
                        key: overlayKey,
                        group: groupName,
                        metric: null, // default to net
                        color: restoredColor,
                        isLive: isLive
                    });
                }
            }
            // Do NOT push the old `o` if it matches groupName; we've handled the entire group in the block above!
        } else {
            newOverlays.push(o);
        }
    }
    
    activeOverlays = newOverlays;
    updateCharts();
}
// [V20260202_1330] Activation/Rank1 Dots Plugin
const activationDotsPlugin = {
    id: 'activationDots',
    afterDatasetsDraw(chart, args, options) {
        const { ctx, scales: { x, y } } = chart;
        chart.data.datasets.forEach((dataset, i) => {
            // [V20260202_1330] Fluorescent Yellow Dot for First Rank #1
            const cleanKey = dataset._key.replace(/\s+\|\s+/g, '|'); // Key from overlay might have spaces "Strat | Prod"
            const rankOneTime = firstRankOneTimes[cleanKey];

            if (rankOneTime && rankOneTime >= x.min && rankOneTime <= x.max) {
                let pointY = 0;
                if (dataset.data && dataset.data.length > 0) {
                    for (let j = 0; j < dataset.data.length; j++) {
                        if (dataset.data[j].x <= rankOneTime) {
                            pointY = dataset.data[j].y;
                        } else {
                            break;
                        }
                    }
                }

                const xPos = x.getPixelForValue(rankOneTime);
                const yPos = y.getPixelForValue(pointY);

                ctx.save();
                // Fluorescent Yellow Dot
                ctx.shadowColor = 'black';
                ctx.shadowBlur = 4;

                ctx.beginPath();
                ctx.arc(xPos, yPos, 10, 0, 2 * Math.PI); // [V20260202_1340] Increased size
                ctx.fillStyle = '#CCFF00'; // Fluorescent Yellow
                ctx.fill();

                // Black border for contrast
                ctx.lineWidth = 3;
                ctx.strokeStyle = '#000000';
                ctx.stroke();

                ctx.restore();
            }
        });
    }
};

function initEventHandlers() {
    document.getElementById('tradeDate').addEventListener('change', fetchData);
    document.getElementById('metricSelector').addEventListener('change', updateCharts);
    document.getElementById('addBtn').addEventListener('click', addOverlayHandler);
    document.getElementById('rankApplyButton').addEventListener('click', applyRankSelection);
    document.getElementById('btnShowRankOnes').addEventListener('click', loadRankOneStrategies); // [V20260202_1520]
    document.getElementById('saveViewButton').addEventListener('click', saveCurrentView);

    // Register Plugin
    Chart.register(activationDotsPlugin);
    document.getElementById('loadViewDropdown').addEventListener('change', (event) => loadView(event.target.value));
    document.getElementById('clearAllButton').addEventListener('click', clearAllOverlays);

    const tradeBucketBtn = document.getElementById('tradeBucketButton');
    if (tradeBucketBtn) {
        tradeBucketBtn.addEventListener('click', saveAllCardsToBucket);
    }

    const deleteViewBtn = document.getElementById('deleteViewButton');
    if (deleteViewBtn) deleteViewBtn.addEventListener('click', deleteView);
    const presetSelectorButton = document.getElementById('presetSelectorButton');
    if (presetSelectorButton) presetSelectorButton.addEventListener('click', togglePresetSelectorPanel);
    const presetSelectorDoneButton = document.getElementById('presetSelectorDoneButton');
    if (presetSelectorDoneButton) presetSelectorDoneButton.addEventListener('click', closePresetSelectorPanel);
    const presetSelectorDeleteButton = document.getElementById('presetSelectorDeleteButton');
    if (presetSelectorDeleteButton) presetSelectorDeleteButton.addEventListener('click', deleteView);

    const closeModalBtn = document.getElementById('closeAddOverlayModal');
    if (closeModalBtn) closeModalBtn.onclick = closeModal;

    const modalAddBtn = document.getElementById('modalAddBtn');
    if (modalAddBtn) modalAddBtn.onclick = submitModalOverlay;

    document.getElementById('playbackPlay').addEventListener('click', togglePlayback);
    document.getElementById('playbackReset').addEventListener('click', resetPlayback);
    document.getElementById('playbackSlower').addEventListener('click', slowerPlayback);
    document.getElementById('playbackFaster').addEventListener('click', fasterPlayback);
    document.getElementById('playbackEnd').addEventListener('click', endPlayback);
    document.getElementById('timeSlider').addEventListener('input', onSliderInput);
    document.getElementById('timeSlider').addEventListener('change', onSliderChange);

    const startTimeInput = document.getElementById('startTimeInput');
    if (startTimeInput) startTimeInput.addEventListener('change', onStartTimeInputChange);

    document.getElementById('displayButton').addEventListener('click', () => fetchData());

    const resetStartTimeButton = document.getElementById('resetStartTimeButton');
    if (resetStartTimeButton) resetStartTimeButton.addEventListener('click', resetStartTimeTo00);

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
        nextRefreshTime = Date.now() + 60000; // Longer refresh for SQL API (heavy)
        refreshInterval = setInterval(() => {
            if (Date.now() >= nextRefreshTime) {
                fetchData();
                nextRefreshTime = Date.now() + 120000;
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
    const date = document.getElementById('tradeDate').value;
    const db = 'tradedb';
    const url = `http://127.0.0.1:8001/api/vwCombined_trades_output_top200?db=${db}&created_gt=${date}T00:00:00&created_lt=${date}T23:59:59&page_size=5000&_t=${Date.now()}`;

    try {
        const res = await fetch(url);
        const json = await res.json();

        // [V20260202_1330] Fetch Frequency Data for Rank #1 Dots
        try {
            // Assuming mode='live' for SQL V3
            const freqUrl = `/api/trade_file?mode=live&date=${date}&filename=_frequency.json&_t=${Date.now()}`;
            const fRes = await fetch(freqUrl);
            if (fRes.ok) {
                const fJson = await fRes.json();
                const fData = fJson.content || fJson;
                if (fData.snapshots) {
                    processFrequencyData(fData.snapshots);
                }
            }
        } catch (e) {
            console.warn("Frequency data fetch failed", e);
            firstRankOneTimes = {}; // Reset on fail
        }

        if (json.data) {
            rawData = json.data;
            const newProcessedSeries = {};

            const { startOfDay, endOfDay } = getPlaybackBoundaries();
            const minMs = startOfDay.getTime();
            const maxMs = endOfDay.getTime();

            rawData.forEach(item => {
                const model = item.model;
                const product = item.product;
                const key = `${model}|${product}`;

                const iso = item.created.endsWith('Z') ? item.created : item.created + 'Z';
                const ptMs = new Date(iso).getTime();

                // [V20260125_2245] Strict Date Filter: Drop records outside the 24h window
                if (ptMs < minMs || ptMs > maxMs) return;

                if (!newProcessedSeries[key]) {
                    newProcessedSeries[key] = [];
                }

                newProcessedSeries[key].push({
                    t: iso,
                    ms: ptMs,
                    signal: item.signal,
                    net_return: item.net_return || 0,
                    net: item.net_return_sum || 0,
                    alt: item.alt_net_return_sum || 0,
                    buy: item.buy_net_return_sum || 0,
                    sell: item.sell_net_return_sum || 0,
                    trade_count: item.trade_count || 0,
                    exit_time: item.exit_time || null,
                    status: item.status || 'OPEN',
                    is_live: item.is_live || 'No'
                });
            });

            for (const key in newProcessedSeries) {
                newProcessedSeries[key].sort((a, b) => a.ms - b.ms);
            }

            processedSeries = newProcessedSeries;
            document.getElementById('lastUpdate').innerText = new Date().toLocaleTimeString();

            // [V20260126_0400] Ensure Auto Refresh jumps to the latest time if not playing
            const boundaries = getPlaybackBoundaries();
            if (!playbackTime || (autoRefreshEnabled && !isPlaying)) {
                playbackTime = boundaries.endOfDay;
            }

            updateDatasetTimeBounds();
            populateSelectors();
            updateCharts();
            initAutoRefresh();
        }
    } catch (e) {
        console.error("Fetch error:", e);
        alert("Make sure the SQL API is running on port 8001 and CORS is enabled.");
    }
}

function populateSelectors() {
    const prodSel = document.getElementById('productSelector'), stratSel = document.getElementById('strategySelector');
    const products = new Set(), strategies = new Set();

    for (const key in processedSeries) {
        const [strat, prod] = key.split('|');
        strategies.add(strat);
        products.add(prod);
    }

    updateSelectOptions(prodSel, Array.from(products).sort(), prodSel.value);
    updateSelectOptions(stratSel, Array.from(strategies).sort(), stratSel.value);
}

function updateSelectOptions(selectElement, optionsArray, currentValue) {
    selectElement.innerHTML = '<option value="">-- Select --</option>';
    optionsArray.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt; el.textContent = opt;
        selectElement.appendChild(el);
    });
    if (currentValue && optionsArray.includes(currentValue)) selectElement.value = currentValue;
}

function addOverlayHandler() {
    const prod = document.getElementById('productSelector').value;
    const strat = document.getElementById('strategySelector').value;
    const metric = document.getElementById('lineMetricSelector').value;
    const group = document.getElementById('groupLabelInput').value.trim();

    if (!prod || !strat) return;
    const key = `${strat} | ${prod}`;
    const groupName = group || key;

    const normalizedMetric = metric === 'global' ? null : metric;

    // Check if duplicate in this group
    const exists = activeOverlays.find(o => o.key === key && o.group === groupName && o.metric === normalizedMetric);
    if (exists) return;

    activeOverlays.push({
        key: key,
        group: groupName,
        metric: normalizedMetric,
        color: colors[activeOverlays.length % colors.length]
    });

    updateCharts();
}

/**
 * Modal Handling for Overlay Selection
 */
function openAddOverlayModal(groupName) {
    document.getElementById('modalTargetGroup').value = groupName;
    populateModalSelectors();
    document.getElementById('addOverlayModal').style.display = 'flex';
}

function closeModal() {
    document.getElementById('addOverlayModal').style.display = 'none';
}

function populateModalSelectors() {
    const products = new Set(), strategies = new Set();
    for (const key in processedSeries) {
        const [strat, prod] = key.split('|');
        strategies.add(strat);
        products.add(prod);
    }

    updateSelectOptions(document.getElementById('modalProductSelector'), Array.from(products).sort());
    updateSelectOptions(document.getElementById('modalStrategySelector'), Array.from(strategies).sort());
}

function submitModalOverlay() {
    const prod = document.getElementById('modalProductSelector').value;
    const strat = document.getElementById('modalStrategySelector').value;
    const metric = document.getElementById('modalMetricSelector').value;
    const groupName = document.getElementById('modalTargetGroup').value;

    if (!prod || !strat) return;
    const key = `${strat} | ${prod}`;

    const exists = activeOverlays.find(o => o.key === key && o.group === groupName && o.metric === metric);
    if (!exists) {
        activeOverlays.push({
            key: key,
            group: groupName,
            metric: metric,
            color: colors[activeOverlays.length % colors.length]
        });
        updateCharts();
    }
    closeModal();
}

/**
 * [V20260203_1330] Add Remaining Strategies (Exact Set of 4) for V3
 * Matches: breakout, breakout_R, breakout_Rev, breakout_R_Rev
 * With same Version & TP/SL parameters.
 */
/**
 * [V20260220_0036] Add All Window Variations
 * Matches same base prefix and same tp/sl, but different window size.
 */
function addAllWindows(groupName) {
    const overlay = activeOverlays.find(o => o.group === groupName);
    if (!overlay) return;

    const parts = overlay.key.includes(' | ') ? overlay.key.split(' | ') : overlay.key.split('|');
    if (parts.length < 2) return;
    const refStrategy = parts[0].trim();
    const product = parts[1].trim();

    const paramMatch = refStrategy.match(/^(.*?)_(\d+)(_tp[\d\.]+_sl[\d\.]+)$/);
    if (!paramMatch) {
        alert("Could not extract prefix/window/params from strategy name (expected format: ..._N_tpX_slY).");
        return;
    }
    const prefix = paramMatch[1];
    const originalWindow = paramMatch[2];
    const suffix = paramMatch[3];

    let addedCount = 0;

    for (const key in processedSeries) {
        const stratProd = key.split('|');
        if (stratProd.length < 2) continue;
        const strat = stratProd[0];
        const prod = stratProd[1];

        if (prod === product && strat !== refStrategy && strat.startsWith(prefix + '_') && strat.endsWith(suffix)) {
            const stratMatch = strat.match(/^(.*?)_(\d+)(_tp[\d\.]+_sl[\d\.]+)$/);
            if (stratMatch && stratMatch[1] === prefix && stratMatch[3] === suffix) {
                const overlayKey = `${strat} | ${product}`;
                const exists = activeOverlays.find(o => o.group === groupName && (o.key === overlayKey || o.key === key));

                if (!exists) {
                    activeOverlays.push({
                        key: overlayKey,
                        group: groupName,
                        metric: null,
                        color: colors[activeOverlays.length % colors.length]
                    });
                    addedCount++;
                }
            }
        }
    }

    if (addedCount > 0) {
        updateCharts();
    } else {
        alert("No other window sizes found in data.");
    }
}

// [V20260308_1941] Duplicate all metrics for related strategies
function addRelatedStrategies(groupName) {
    const overlaysInGroup = activeOverlays.filter(o => o.group === groupName);
    if (!overlaysInGroup.length) return;

    const parts = overlaysInGroup[0].key.includes(' | ') ? overlaysInGroup[0].key.split(' | ') : overlaysInGroup[0].key.split('|');
    if (parts.length < 2) return;
    const refStrategy = parts[0].trim();
    const product = parts[1].trim();

    // 1. Extract Parameter Suffix
    const paramMatch = refStrategy.match(/_(\d+)_tp([\d\.]+)_sl([\d\.]+)/);
    if (!paramMatch) {
        alert("Could not extract version/params from strategy name (expected format: ..._N_tpX_slY).");
        return;
    }
    const paramsSuffix = paramMatch[0];

    // [V20260308_1941] Identify all distinct metrics in the active chart group
    const metricsToApply = [...new Set(overlaysInGroup.map(o => o.metric || null))];

    const prefixes = ['breakout', 'breakout_R', 'breakout_Rev', 'breakout_R_Rev'];
    let addedCount = 0;

    prefixes.forEach(prefix => {
        const targetName = prefix + paramsSuffix;
        const key = `${targetName}|${product}`;

        if (processedSeries[key]) {
            const overlayKey = `${targetName} | ${product}`;

            metricsToApply.forEach(inheritedMetric => {
                const exists = activeOverlays.find(o => o.group === groupName && (o.key === overlayKey || o.key === key) && (o.metric || null) === inheritedMetric);

                if (!exists) {
                    activeOverlays.push({
                        key: overlayKey,
                        group: groupName,
                        metric: inheritedMetric,
                        color: colors[activeOverlays.length % colors.length]
                    });
                    addedCount++;
                }
            });
        }
    });

    if (addedCount > 0) {
        updateCharts();
    } else {
        alert("No other strategies from the set (Breakout, R, Rev, R_Rev) found in data.");
    }
}

function removeOverlay(key, groupPrefix, metric) {
    activeOverlays = activeOverlays.filter(o => {
        return !(o.key === key && o.group === groupPrefix && (o.metric === metric || (!o.metric && metric === 'null')));
    });
    updateCharts();
}

function removeGroup(groupName) {
    activeOverlays = activeOverlays.filter(o => o.group !== groupName);
    updateCharts();
}

/**
 * [V20260128_2145] Reorder cards by moving their associated overlays in activeOverlays
 */
function moveGroup(groupName, direction) {
    const orderedGroups = [];
    activeOverlays.forEach(o => { if (!orderedGroups.includes(o.group)) orderedGroups.push(o.group); });

    const idx = orderedGroups.indexOf(groupName);
    if (idx === -1) return;

    const targetIdx = idx + direction;
    if (targetIdx < 0 || targetIdx >= orderedGroups.length) return;

    const temp = orderedGroups[idx];
    orderedGroups[idx] = orderedGroups[targetIdx];
    orderedGroups[targetIdx] = temp;

    const newOverlays = [];
    orderedGroups.forEach(g => {
        const members = activeOverlays.filter(o => o.group === g);
        newOverlays.push(...members);
    });

    activeOverlays = newOverlays;
    updateCharts();
}

function clearAllOverlays() {
    activeOverlays = [];
    Object.keys(charts).forEach(destroyGroupCharts);
    updateCharts();
}

/**
 * [V20260125_1840] Signal Flipping Logic
 * net_return -> use signal as is
 * alt_net_return -> flip signal
 */
function getDisplaySignal(baseSignal, metric) {
    if (!baseSignal) return '-';
    const isAlt = (metric === 'alt' || metric === 'alt_net_return_sum');
    if (!isAlt) return baseSignal;
    return baseSignal === 'BUY' ? 'SELL' : (baseSignal === 'SELL' ? 'BUY' : baseSignal);
}

function updateCharts(filterTime = null) {
    const grid = document.getElementById('chartGrid');
    const globalMetric = document.getElementById('metricSelector').value;

    if (activeOverlays.length === 0) {
        grid.innerHTML = '<div class="empty-grid-msg">No charts added. Use Auto or Add Chart to compare.</div>';
        Object.keys(charts).forEach(destroyGroupCharts);
        return;
    }

    const emptyMsg = grid.querySelector('.empty-grid-msg');
    if (emptyMsg) emptyMsg.remove();

    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    const startMs = (getActiveStartTime() || startOfDay).getTime();
    const axisMaxMs = (filterTime || playbackTime || datasetLatestTime || endOfDay).getTime();

    const groupMap = {};
    activeOverlays.forEach(o => {
        if (!groupMap[o.group]) groupMap[o.group] = [];
        groupMap[o.group].push(o);
    });

    grid.querySelectorAll('.chart-card').forEach(card => {
        if (!groupMap[card.dataset.group]) {
            const g = card.dataset.group;
            destroyGroupCharts(g);
            card.remove();
        }
    });

    const orderedGroupNames = [];
    activeOverlays.forEach(o => { if (!orderedGroupNames.includes(o.group)) orderedGroupNames.push(o.group); });

    orderedGroupNames.forEach((groupName, index) => {
        const configs = groupMap[groupName];
        if (!configs) return;
        let card = grid.querySelector(`.chart-card[data-group="${groupName}"]`);
        if (!card) card = createGroupCard(groupName);
        
        const splitState = getGroupSplitState(groupName);
        const actionsDiv = card.querySelector('.chart-actions');
        if (actionsDiv) {
            let toggleBtn = actionsDiv.querySelector('.split-toggle');
            if (splitState) {
                if (!toggleBtn) {
                    toggleBtn = document.createElement('button');
                    toggleBtn.className = 'action-btn split-toggle';
                    toggleBtn.onclick = (e) => handleSplitComboAction(e, groupName);
                    const delBtn = actionsDiv.querySelector('.delete');
                    if (delBtn) actionsDiv.insertBefore(toggleBtn, delBtn);
                    else actionsDiv.appendChild(toggleBtn);
                }
                toggleBtn.title = splitState.label;
                toggleBtn.innerHTML = `<i class="fas ${splitState.icon}"></i>`;
            } else if (toggleBtn) {
                toggleBtn.remove();
            }
        }
        
        if (grid.children[index] !== card) {
            grid.insertBefore(card, grid.children[index] || null);
        }

        const isGroupLive = configs.some(o => o.isLive);
        let leaderKey = null, maxDelta = -Infinity;
        configs.forEach(config => {
            const lookupKey = config.key.replace(' | ', '|');
            const series = processedSeries[lookupKey] || [];
            const metric = config.metric || globalMetric;
            const lastPt = series[series.length - 1] || {};
            const val = getMetricValueV3(lastPt, metric);
            if (val > maxDelta) { maxDelta = val; leaderKey = config.key; }
        });

        const datasets = configs.map(config => {
            const lookupKey = config.key.replace(' | ', '|');
            const series = processedSeries[lookupKey] || [];
            const metric = config.metric || globalMetric;
            const steppedData = buildSteppedSeriesV3(series, metric, startMs, axisMaxMs);
            const metricLabel = (metric === 'alt' || metric === 'alt_net_return_sum') ? 'Alt' :
                (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') ? 'Buy' :
                    (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') ? 'Sell' : 'Net';

            return {
                label: `${config.key} (${metricLabel})`,
                data: steppedData,
                borderColor: config.color,
                backgroundColor: config.color + '01',
                fill: true,
                borderWidth: (isGroupLive && config.key === leaderKey) ? 4 : 2,
                pointRadius: 0,
                parsing: false,
                _metric: metric,
                _key: config.key
            };
        });

        renderGroupChartsV3({
            groupName,
            card,
            configs,
            datasets,
            startMs,
            axisMaxMs
        });

        const listEl = card.querySelector('.group-values-list');
        listEl.innerHTML = configs.map(c => {
            const metric = c.metric || globalMetric;
            const ds = datasets.find(d => d._key === c.key && d._metric === metric);
            const lastVal = ds ? ds.data.slice(-1)[0].y : 0;
            const colorClass = lastVal > 0 ? '#10b981' : lastVal < 0 ? '#ef4444' : '#9ca3af';
            const isLive = c.isLive;
            const isLeader = (isGroupLive && c.key === leaderKey);
            const pulse = isLive ? '<span class="live-pulse"></span>' : '';
            const leaderBadge = isLeader ? '<span style="color:var(--accent-primary); font-size:0.6rem; border:1px solid; border-radius:4px; padding:0 4px; margin-right:4px;">L-TRADE</span>' : '';

            return `<div class="group-value-item" style="font-size: 0.65rem;">
                        <span class="dot" style="background:${c.color}"></span>
                        <div style="flex: 1; display: flex; flex-direction: column;">
                            <span class="lbl" title="${c.key}">${pulse}${leaderBadge}${c.key.split(' | ')[0]}</span>
                        </div>
                        <span class="val" style="color:${colorClass}; align-self: center;">${currencyFormatter.format(lastVal)}</span>
                        <i class="fas fa-times-circle" style="align-self: center;" onclick="removeOverlay('${c.key}', '${groupName}', '${c.metric}')"></i>
                    </div>`;
        }).join('');
    });
}

function renderGroupChartsV3({ groupName, card, configs, datasets, startMs, axisMaxMs }) {
    const netContainer = card.querySelector('.chart-container.net-view');
    if (netContainer) netContainer.style.display = 'flex';
    renderNetChartV3(groupName, card, datasets, startMs, axisMaxMs);
}

function renderNetChartV3(groupName, card, datasets, minX, maxX) {
    const canvas = card.querySelector(`#group-chart-${groupName}-net`);
    renderChartOnCanvasV3(groupName, 'net', canvas, datasets, minX, maxX);
}



function renderChartOnCanvasV3(groupName, slot, canvas, datasets, minX, maxX) {
    if (!canvas) return;
    const entry = ensureGroupCharts(groupName);
    const existing = entry[slot];
    if (existing) {
        existing.data.datasets = datasets;
        existing.options.scales.x.min = minX;
        existing.options.scales.x.max = maxX;
        existing.update('none');
        return;
    }
    const ctx = canvas.getContext('2d');
    entry[slot] = new Chart(ctx, {
        type: 'line',
        data: { datasets },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            animation: false,
            parsing: false,
            plugins: { legend: { display: false }, tooltip: { mode: 'index', intersect: false } },
            scales: {
                x: {
                    type: 'time',
                    time: { unit: 'minute', displayFormats: { minute: 'HH:mm' } },
                    min: minX,
                    max: maxX,
                    ticks: { color: 'rgba(255,255,255,0.4)', font: { size: 9 } },
                    grid: { display: true, color: 'rgba(255,255,255,0.03)', drawBorder: false }
                },
                y: {
                    ticks: { color: 'rgba(255,255,255,0.4)', font: { size: 9 } },
                    grid: { display: true, color: 'rgba(255,255,255,0.03)', drawBorder: false }
                }
            }
        }
    });
}


function createGroupCard(groupName) {
    const div = document.createElement('div');
    div.className = 'chart-card';
    div.dataset.group = groupName;
    div.style.height = 'auto';
    div.style.minHeight = '420px';
    div.title = "Double-click to view trade list";
    div.ondblclick = () => showTradeDrilldown(groupName);
    const liveConfig = activeOverlays.find(o => o.group === groupName && o.isLive);
    const liveClass = liveConfig ? 'active' : '';
    const liveText = liveConfig ? 'LIVE: ON' : 'LIVE: OFF';
    const splitState = getGroupSplitState(groupName);
    const splitButton = splitState
        ? `<button class="action-btn split-toggle" onclick="handleSplitComboAction(event, '${groupName}')" title="${splitState.label}">
               <i class="fas ${splitState.icon}"></i>
           </button>`
        : '';

    div.innerHTML = `
        <div class="chart-card-header" style="flex-direction:column; align-items:stretch; gap:10px;">     
            <div class="chart-header-row">
                <div class="chart-title-group">
                    <div class="chart-card-title">${groupName}</div>
                    <button class="live-btn ${liveClass}" onclick="toggleLiveMode(event, '${groupName}')" title="Toggle live leader monitoring for this card">
                        <i class="fas fa-satellite-dish"></i> <span>${liveText}</span>
                        ${liveConfig ? '<span class="live-pulse"></span>' : ''}
                    </button>
                </div>
                <div class="chart-actions">
                    <!-- [V20260128_2145] Move Buttons -->
                    <button class="action-btn" onclick="moveGroup('${groupName}', -1)" title="Move card left">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button class="action-btn" onclick="moveGroup('${groupName}', 1)" title="Move card right">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                    <button class="action-btn" onclick="openTransferModal('${groupName}')" title="Move card to another view">
                        <i class="fas fa-exchange-alt"></i>
                    </button>

                    <button class="action-btn" onclick="addRelatedStrategies('${groupName}')" title="Add all strategies with same parameters (Complete Set)">
                        <i class="fas fa-clone"></i>
                    </button>
                    <button class="action-btn" onclick="addAllWindows('${groupName}')" title="Add all window sizes for this strategy">
                        <i class="fas fa-layer-group"></i>
                    </button>
                    
                    <button class="action-btn add" onclick="openAddOverlayModal('${groupName}')" title="Add specific comparison to this card">
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="action-btn save" onclick="saveToBucket('${groupName}')" title="Save this card as a trade bucket">
                        <i class="fas fa-save"></i>
                    </button>
                    ${splitButton}
                    <button class="action-btn delete" onclick="removeGroup('${groupName}')" title="Remove this card">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>
            </div>
            <div class="group-values-list" style="display:grid; grid-template-columns: 1fr 1fr; gap:5px; font-size:0.7rem;"></div>
        </div>
        <div class="chart-container net-view" style="height:300px; margin-top:10px;" data-mode="net">
            <canvas id="group-chart-${groupName}-net"></canvas>
        </div>
    `;
    return div;
}

function getPlaybackBoundaries() {
    const dateVal = document.getElementById('tradeDate').value;
    const startOfDay = new Date(dateVal + 'T00:00:00Z');
    const now = new Date();
    const isToday = (dateVal === now.getUTCFullYear() + '-' + String(now.getUTCMonth() + 1).padStart(2, '0') + '-' + String(now.getUTCDate()).padStart(2, '0'));
    let endOfDay = isToday ? now : new Date(dateVal + 'T23:59:59Z');
    return { startOfDay, endOfDay };
}

function updateDatasetTimeBounds() {
    const { startOfDay, endOfDay } = getPlaybackBoundaries();

    // [V20260203_1320] Start at the Hour of the earliest data (V3)
    let earliest = null;
    let latest = null;

    for (const key in processedSeries) {
        const series = processedSeries[key];
        if (series.length > 0) {
            const first = series[0].ms;
            const last = series[series.length - 1].ms;
            if (!earliest || first < earliest) earliest = first;
            if (!latest || last > latest) latest = last;
        }
    }

    if (earliest) {
        const d = new Date(earliest);
        d.setMinutes(0, 0, 0);
        datasetEarliestTime = d < startOfDay ? startOfDay : d;
    } else {
        datasetEarliestTime = startOfDay;
    }

    datasetLatestTime = endOfDay;
    updateStartTimeUI();
}

function updateStartTimeUI() {
    const input = document.getElementById('startTimeInput'), rangeLabel = document.getElementById('startTimeRangeLabel');
    if (!input || !datasetEarliestTime) return;
    const minStr = datasetEarliestTime.toISOString().substring(11, 19), maxStr = datasetLatestTime.toISOString().substring(11, 19);
    rangeLabel.innerText = `${minStr} -> ${maxStr}`;
    if (!currentStartTime || !isStartTimeCustom) currentStartTime = new Date(datasetEarliestTime.getTime());
    input.value = currentStartTime.toISOString().substring(11, 19);
}

function onStartTimeInputChange(e) {
    currentStartTime = new Date(`${document.getElementById('tradeDate').value}T${e.target.value}Z`);
    isStartTimeCustom = true; updateCharts();
}
function resetStartTimeTo00() {
    currentStartTime = new Date(getPlaybackBoundaries().startOfDay.getTime());
    isStartTimeCustom = true; updateStartTimeUI(); updateCharts();
}
function getActiveStartTime() { return currentStartTime || datasetEarliestTime; }

function applyRankSelection() {
    // [V20260125_1650] Support ranking by trade count or profit
    const count = parseInt(document.getElementById('rankCount').value) || 6;
    const minTrades = parseInt(document.getElementById('minTradesCount').value) || 10;
    const rankBasis = document.getElementById('rankBasisSelector')?.value || 'profit';
    const metric = document.getElementById('metricSelector').value;
    const field = metric === 'alt_net_return_sum' ? 'alt' :
        metric === 'buy_net_return_sum' ? 'buy' :
            metric === 'sell_net_return_sum' ? 'sell' : 'net';
    const startMs = getActiveStartTime().getTime(), evalMs = playbackTime ? playbackTime.getTime() : Date.now();

    const candidates = [];
    for (const key in processedSeries) {
        const series = processedSeries[key];
        if (series.length === 0) continue;

        let sVal = 0, eVal = 0, tradesAtEval = 0;
        for (const pt of series) {
            if (pt.ms <= startMs) {
                sVal = pt[field];
            }
            if (pt.ms <= evalMs) {
                eVal = pt[field];
                tradesAtEval = pt.trade_count;
            }
            if (pt.ms > evalMs) break;
        }

        // Apply Min Trades filter based on count AT THAT TIME
        if (tradesAtEval < minTrades) continue;

        const delta = eVal - sVal;
        // Keep winners only (Positive Profit)
        if (delta > 0) {
            candidates.push({
                key: key.replace('|', ' | '),
                delta: delta,
                trades: tradesAtEval
            });
        }
    }

    // Sort based on the state at evaluation time
    if (rankBasis === 'trades') {
        candidates.sort((a, b) => b.trades - a.trades);
    } else {
        candidates.sort((a, b) => b.delta - a.delta);
    }
    const result = candidates.slice(0, count);

    result.forEach((c) => {
        const exists = activeOverlays.find(o => o.key === c.key && o.group === c.key);
        if (!exists) {
            activeOverlays.push({
                key: c.key,
                group: c.key,
                metric: null,
                color: colors[activeOverlays.length % colors.length]
            });
        }
    });

    updateCharts();
}

function togglePlayback() {
    isPlaying = !isPlaying;
    const btn = document.getElementById('playbackPlay');
    if (isPlaying) {
        btn.innerHTML = '<i class="fas fa-pause"></i> <span>Pause</span>';
        lastTickTime = Date.now();
        playbackInterval = setInterval(playbackTick, 100);
    } else {
        btn.innerHTML = '<i class="fas fa-play"></i> <span>Play</span>';
        clearInterval(playbackInterval);
    }
}

function playbackTick() {
    const now = Date.now(), elapsedMs = now - lastTickTime;
    lastTickTime = now;
    playbackTime = new Date(playbackTime.getTime() + elapsedMs * playbackSpeed);
    const { endOfDay } = getPlaybackBoundaries();
    if (playbackTime >= endOfDay) { playbackTime = endOfDay; isPlaying = false; togglePlayback(); }
    updatePlaybackUI(); updateCharts();
}

function onSliderInput(e) {
    playbackTime = new Date(getPlaybackBoundaries().startOfDay.getTime() + e.target.value * 1000);
    updatePlaybackUI(); if (!isPlaying) updateCharts();
}
function onSliderChange() { if (!isPlaying) updateCharts(); }
function resetPlayback() { playbackTime = getActiveStartTime(); updatePlaybackUI(); updateCharts(); }
function endPlayback() { playbackTime = getPlaybackBoundaries().endOfDay; updatePlaybackUI(); updateCharts(); }
function slowerPlayback() { playbackSpeed = speeds[Math.max(0, speeds.indexOf(playbackSpeed) - 1)]; updateSpeedUI(); }
function fasterPlayback() { playbackSpeed = speeds[Math.min(speeds.length - 1, speeds.indexOf(playbackSpeed) + 1)]; updateSpeedUI(); }
function updateSpeedUI() { document.getElementById('playbackSpeedLabel').innerText = `${playbackSpeed}x SPEED`; }
function updatePlaybackUI() {
    if (!playbackTime) return;
    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    document.getElementById('currentPlaybackTime').innerText = playbackTime.toISOString().substring(11, 19);
    const slider = document.getElementById('timeSlider');
    slider.max = Math.floor((endOfDay - startOfDay) / 1000);
    slider.value = Math.floor((playbackTime - startOfDay) / 1000);
}

async function loadView(name) {
    if (!name) return;
    const viewNameEl = document.getElementById('viewNameInput');
    if (viewNameEl) viewNameEl.value = name;
    if (name.startsWith('BUCKET:')) {
        const bucketName = name.replace('BUCKET:', '');
        const globalMetric = document.getElementById('metricSelector').value || 'net_return_sum';
        let newOverlays = [];
        if (bucketName === 'ALL') {
            loadedBuckets.forEach(b => {
                (b.strategies || []).forEach(s => {
                    newOverlays.push({
                        key: s.key,
                        group: b.name,
                        metric: s.metric || globalMetric,
                        color: colors[newOverlays.length % colors.length]
                    });
                });
            });
        } else {
            const bucket = loadedBuckets.find(b => b.name === bucketName);
            if (!bucket) return alert("Bucket detail not found in cache. Refresh the page.");
            newOverlays = (bucket.strategies || []).map((s, idx) => ({
                key: s.key,
                group: bucket.name,
                metric: s.metric || globalMetric,
                color: colors[idx % colors.length]
            }));
        }
        activeOverlays = [];
        const seen = new Set();
        newOverlays.forEach(o => {
            const k = `${o.key}|${o.group}|${o.metric || 'net_return_sum'}`;
            if (seen.has(k)) return;
            seen.add(k);
            activeOverlays.push(o);
        });
        updateCharts();
        return;
    }
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}'), v = views[name];
    if (v) {
        activeOverlays = v.overlays || [];
        document.getElementById('metricSelector').value = v.metric || 'net_return_sum';
        updateCharts();
    }
}
function saveCurrentView() {
    const name = document.getElementById('viewNameInput').value.trim();
    if (!name) return alert("Enter name");
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    views[name] = { overlays: activeOverlays, metric: document.getElementById('metricSelector').value };
    localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
    alert("Saved"); populateSavedViews();
}

/**
 * [V20260204_1255] Save Group as Trade Bucket
 */
function saveToBucket(groupName) {
    const now = new Date();
    const mmdd = String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
    const hhmmss = String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0') + String(now.getSeconds()).padStart(2, '0');
    const ts = mmdd + '_' + hhmmss + '_' + String(now.getMilliseconds()).padStart(3, '0');

    const overlays = activeOverlays.filter(o => o.group === groupName);
    if (overlays.length < 2) return alert("Cannot create Trade Bucket: single-row buckets are not allowed.");

    // Validation
    const strategyUsage = {};
    const strategyAndMetricKeys = new Set();
    const globalMetricRaw = document.getElementById('metricSelector').value;
    const localGlobalMetric = globalMetricRaw === 'global' ? 'net' : globalMetricRaw;

    for (const o of overlays) {
        let metricPart = o.metric ? o.metric : localGlobalMetric;
        if (metricPart === 'buy') metricPart = 'buy_net';
        if (metricPart === 'sell') metricPart = 'sell_net';
        if (metricPart === 'alt') metricPart = 'alt_net';
        
        const fullKey = `${o.key} | ${metricPart}`;
        if (strategyAndMetricKeys.has(fullKey)) {
             return alert(`Cannot create Trade Bucket: Duplicate strategy and metric '${fullKey}' is not allowed.`);
        }
        strategyAndMetricKeys.add(fullKey);

        if (!strategyUsage[o.key]) strategyUsage[o.key] = new Set();
        strategyUsage[o.key].add(metricPart);
    }

    for (const [key, metrics] of Object.entries(strategyUsage)) {
        if (metrics.size > 1 && metrics.has('net')) {
            return alert(`Cannot create Trade Bucket: Strategy '${key}' is included multiple times, but one uses the [N] (net) metric. When combining the same strategy, you must use distinct directional metrics like [B] and [S].`);
        }
    }
    const axisMaxMs = (playbackTime || datasetLatestTime || new Date()).getTime();
    const startMs = getActiveStartTime().getTime();

    let leader = null;
    let maxDelta = -Infinity;

    overlays.forEach(o => {
        const lookupKey = o.key.replace(' | ', '|');
        const series = processedSeries[lookupKey] || [];
        const metric = o.metric || localGlobalMetric;
        let baseline = 0, lastVal = 0;

        for (let i = 0; i < series.length; i++) {
            const pt = series[i];
            const val = (metric === 'alt' || metric === 'alt_net_return_sum') ? pt.alt :
                (metric === 'buy' || metric === 'buy_net_return_sum') ? pt.buy :
                    (metric === 'sell' || metric === 'sell_net_return_sum') ? pt.sell : (pt.net || 0);

            if (pt.ms <= startMs) baseline = val;
            if (pt.ms <= axisMaxMs) lastVal = val - baseline;
            else break;
        }
        if (lastVal > maxDelta) { maxDelta = lastVal; leader = o; }
    });

    if (!leader) return alert("Could not determine leader.");

    // Parse naming: {mmdd_hhmmss_mmm}_{product}_{strategy}_{params}
    const keyParts = leader.key.split(' | ');
    const fullStratName = keyParts[0];
    const product = keyParts[1];

    let strategyBase = fullStratName;
    let params = "default";
    const breakoutMatch = fullStratName.match(/(_\d+)?_tp[\d\.]+_sl[\d\.]+/);
    if (breakoutMatch) {
        strategyBase = fullStratName.substring(0, breakoutMatch.index);
        params = fullStratName.substring(breakoutMatch.index + 1);
    } else if (fullStratName.includes('_')) {
        const parts = fullStratName.split('_');
        params = parts[parts.length - 1];
        strategyBase = parts.slice(0, -1).join('_');
    }

    const bucketName = `${ts}_${product}_${strategyBase}_${params}`.replace(/\s+/g, '');
    const strategiesToSave = overlays.map(o => {
        const metricPart = o.metric ? o.metric : 'net';
        return `${o.key} | ${metricPart}`;
    });
    const mode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';
    const activeStart = getActiveStartTime();

    fetch('/api/trade_buckets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: bucketName,
            strategies: strategiesToSave,
            mode: mode,
            // Persist true TB creation time (not chart start-time) so markers align correctly.
            start_time: now.toISOString(),
            chart_start_time: (activeStart ? activeStart.toISOString() : null),
            minimum_difference: 5.0,
            date: (document.getElementById('tradeDate') ? document.getElementById('tradeDate').value : '')
        })
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                alert(`Bucket "${bucketName}" saved successfully.`);
            } else {
                alert(`Failed: ${data.message}`);
            }
        })
        .catch(err => alert(`Error: ${err}`));
}

/**
 * [V20260311_1020] Save ALL active overlays as a single Trade Bucket
 */
function saveAllCardsToBucket() {
    if (activeOverlays.length < 2) return alert("Cannot create Trade Bucket: single-row buckets are not allowed.");

    const strategyUsage = {};
    const strategyAndMetricKeys = new Set();
    const globalMetricRaw = document.getElementById('metricSelector').value;
    const globalMetric = globalMetricRaw === 'global' ? 'net' : globalMetricRaw;

    for (const o of activeOverlays) {
        let metricPart = o.metric ? o.metric : globalMetric;
        if (metricPart === 'buy') metricPart = 'buy_net';
        if (metricPart === 'sell') metricPart = 'sell_net';
        if (metricPart === 'alt') metricPart = 'alt_net';
        
        const fullKey = `${o.key} | ${metricPart}`;
        if (strategyAndMetricKeys.has(fullKey)) {
             return alert(`Cannot create Trade Bucket: Duplicate strategy and metric '${fullKey}' is not allowed.`);
        }
        strategyAndMetricKeys.add(fullKey);

        if (!strategyUsage[o.key]) strategyUsage[o.key] = new Set();
        strategyUsage[o.key].add(metricPart);
    }

    for (const [key, metrics] of Object.entries(strategyUsage)) {
        if (metrics.size > 1 && metrics.has('net')) {
            return alert(`Cannot create Trade Bucket: Strategy '${key}' is included multiple times, but one uses the [N] (net) metric. When combining the same strategy, you must use distinct directional metrics like [B] and [S].`);
        }
    }

    const now = new Date();
    const mmdd = String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
    const hhmmss = String(now.getHours()).padStart(2, '0') + String(now.getMinutes()).padStart(2, '0') + String(now.getSeconds()).padStart(2, '0');
    const ts = mmdd + '_' + hhmmss + '_' + String(now.getMilliseconds()).padStart(3, '0');

    // Generating generic multi-TB name
    const bucketName = `MULTI_TB_${ts}`;
    const strategiesToSave = Array.from(strategyAndMetricKeys);
    const mode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';

    fetch('/api/trade_buckets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: bucketName,
            strategies: strategiesToSave,
            mode: mode,
            start_time: now.toISOString(),
            chart_start_time: (getActiveStartTime() ? getActiveStartTime().toISOString() : null),
            minimum_difference: 5.0,
            date: (document.getElementById('tradeDate') ? document.getElementById('tradeDate').value : '')
        })
    })
    .then(res => res.json())
    .then(async data => {
        if (data.success) {
            await populateSavedViews();
            const selDate = (document.getElementById('tradeDate') ? document.getElementById('tradeDate').value : '') || '';
            alert(`Trade Bucket "${bucketName}" saved successfully. Opening Trade Bucket page now.`);
            window.open(`trade_bucket.html?mode=${encodeURIComponent(mode)}&date=${encodeURIComponent(selDate)}&bucket=${encodeURIComponent(bucketName)}`, '_blank');
        } else {
            alert(`Failed: ${data.message}`);
        }
    })
    .catch(err => alert(`Error: ${err}`));
}
function deleteView() {
    const names = selectedPresetNames.size > 0
        ? Array.from(selectedPresetNames)
        : [String((document.getElementById('loadViewDropdown') || {}).value || '').trim()].filter(Boolean);
    if (names.length === 0) return;
    if (!confirm(`Delete ${names.length} preset(s)?`)) return;
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    let removed = 0;
    names.forEach(name => {
        if (Object.prototype.hasOwnProperty.call(views, name)) {
            delete views[name];
            selectedPresetNames.delete(name);
            removed++;
        }
    });
    localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
    populateSavedViews();
    alert(`Removed ${removed} preset(s).`);
}
function deleteWorkflowViews() {
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    let removed = 0;
    Object.keys(views).forEach(k => {
        if (/^WF_/i.test(k)) {
            delete views[k];
            removed++;
        }
    });
    localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
    activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_'));
    updateCharts();
    populateSavedViews();
    alert(`Removed ${removed} workflow preset(s).`);
}
async function populateSavedViews() {
    const sel = document.getElementById('loadViewDropdown'), views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    Array.from(selectedPresetNames).forEach(name => {
        if (String(name).startsWith('BUCKET:')) return;
        if (!views[name]) selectedPresetNames.delete(name);
    });
    sel.innerHTML = '<option value="">-- Presets --</option>';
    Object.keys(views).forEach(k => { const o = document.createElement('option'); o.value = k; o.innerText = k; sel.appendChild(o); });
    let bucketNames = [];
    try {
        const mode = document.getElementById('runMode').value;
        const date = document.getElementById('tradeDate').value;
        const res = await fetch(`/api/trade_buckets?mode=${mode}&date=${date}`);
        if (res.ok) {
            const data = await res.json();
            loadedBuckets = data.buckets || [];
            if (loadedBuckets.length > 0) {
                const sep = document.createElement('option');
                sep.disabled = true;
                sep.innerText = '────── TRADE BUCKETS ──────';
                sel.appendChild(sep);
                if (loadedBuckets.length > 1) {
                    const allOpt = document.createElement('option');
                    allOpt.value = 'BUCKET:ALL';
                    allOpt.innerText = '📦 ALL TRADE BUCKETS (' + loadedBuckets.length + ')';
                    sel.appendChild(allOpt);
                }
                loadedBuckets.forEach(b => {
                    const o = document.createElement('option');
                    o.value = 'BUCKET:' + b.name;
                    o.innerText = '📦 ' + b.name;
                    sel.appendChild(o);
                });
                bucketNames = loadedBuckets.map(b => String(b.name || '')).filter(Boolean);
            }
        }
    } catch (e) {
        console.warn("[POPULATE] Failed to fetch trade buckets:", e);
    }
    renderPresetSelectorList(views, bucketNames);
}

function togglePresetSelectorPanel() {
    const panel = document.getElementById('presetSelectorPanel');
    if (!panel) return;
    panel.style.display = panel.style.display === 'none' || !panel.style.display ? 'block' : 'none';
}
function closePresetSelectorPanel() {
    const panel = document.getElementById('presetSelectorPanel');
    if (panel) panel.style.display = 'none';
}
function renderPresetSelectorList(views, bucketNames = []) {
    const list = document.getElementById('presetSelectorList');
    if (!list) return;
    list.innerHTML = '';
    Object.keys(views).sort().forEach(name => {
        const row = document.createElement('label');
        row.style.display = 'flex';
        row.style.alignItems = 'center';
        row.style.gap = '8px';
        row.style.fontSize = '0.8rem';
        row.style.cursor = 'pointer';
        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.checked = selectedPresetNames.has(name);
        cb.onchange = () => {
            if (cb.checked) selectedPresetNames.add(name);
            else selectedPresetNames.delete(name);
            const btn = document.getElementById('presetSelectorButton');
            if (btn) btn.innerHTML = `<i class="fas fa-filter"></i> ${selectedPresetNames.size || ''}`.trim();
        };
        const txt = document.createElement('span');
        txt.textContent = name;
        row.appendChild(cb);
        row.appendChild(txt);
        list.appendChild(row);
    });

    if (bucketNames.length > 0) {
        const sep = document.createElement('div');
        sep.style.marginTop = '8px';
        sep.style.paddingTop = '8px';
        sep.style.borderTop = '1px solid rgba(255,255,255,0.1)';
        sep.style.fontSize = '0.75rem';
        sep.style.color = 'var(--text-dim)';
        sep.textContent = 'TRADE BUCKETS';
        list.appendChild(sep);

        bucketNames.sort().forEach(name => {
            const row = document.createElement('label');
            row.style.display = 'flex';
            row.style.alignItems = 'center';
            row.style.justifyContent = 'space-between';
            row.style.gap = '8px';
            row.style.fontSize = '0.8rem';
            row.style.cursor = 'pointer';

            const left = document.createElement('div');
            left.style.display = 'flex';
            left.style.alignItems = 'center';
            left.style.gap = '8px';
            const cb = document.createElement('input');
            cb.type = 'checkbox';
            const key = `BUCKET:${name}`;
            cb.checked = selectedPresetNames.has(key);
            cb.onchange = () => {
                if (cb.checked) selectedPresetNames.add(key);
                else selectedPresetNames.delete(key);
                const btn = document.getElementById('presetSelectorButton');
                if (btn) btn.innerHTML = `<i class="fas fa-filter"></i> ${selectedPresetNames.size || ''}`.trim();
            };
            const txt = document.createElement('span');
            txt.textContent = `📦 ${name}`;
            left.appendChild(cb);
            left.appendChild(txt);

            const openBtn = document.createElement('button');
            openBtn.className = 'btn btn-secondary';
            openBtn.style.padding = '2px 8px';
            openBtn.style.fontSize = '0.72rem';
            openBtn.textContent = 'Open';
            openBtn.onclick = (e) => {
                e.preventDefault();
                loadView(`BUCKET:${name}`);
            };

            row.appendChild(left);
            row.appendChild(openBtn);
            list.appendChild(row);
        });
    }
    const btn = document.getElementById('presetSelectorButton');
    if (btn) btn.innerHTML = `<i class="fas fa-filter"></i> ${selectedPresetNames.size || ''}`.trim();
}

async function consumeWorkflowImportPayloadV3() {
    try {
        const res = await fetch('/api/workflows/multi_chart_payload');
        const data = await res.json();
        if (!data || !data.success || !data.payload || !Array.isArray(data.payload.items) || data.payload.items.length === 0) return;
        const payload = data.payload;
        const currentProductType = getCurrentWorkflowImportProductTypeV3(payload);
        const isProfileWorkflow = String(payload.source || '') === 'profile_match_workflow';
        const isTopXWorkflow = String(payload.source || '') === 'top_x_multi_chart_workflow';
        const runId = String(payload.run_id || '');
        if (runId) {
            const lastRunId = localStorage.getItem(`multi_chart_v3_workflow_import_run_id_${currentProductType}`) || '';
            if (lastRunId === runId) return;
            localStorage.setItem(`multi_chart_v3_workflow_import_run_id_${currentProductType}`, runId);
        }

        if (isProfileWorkflow) {
            // 1) Replace WF_PROFILE cards on each profile workflow run.
            activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_PROFILE_'));
            // 2) Prune stale WF_PROFILE presets so only current workflow output remains.
            try {
                const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
                Object.keys(views || {}).forEach(name => {
                    if (String(name).startsWith('WF_PROFILE_')) delete views[name];
                });
                localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
                populateSavedViews();
            } catch (_) { }
        }
        if (isTopXWorkflow) {
            // 1) Replace WF_TOPX cards on each Top X workflow run.
            activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_TOPX_'));
            // 2) Prune stale WF_TOPX presets so only current workflow output remains.
            try {
                const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
                Object.keys(views || {}).forEach(name => {
                    if (String(name).startsWith('WF_TOPX_')) delete views[name];
                });
                localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
                populateSavedViews();
            } catch (_) { }
        }

        const allowedSet = new Set(Object.keys(processedSeries));
        let added = 0;
        const addedGroups = new Set();
        for (const item of payload.items) {
            const itemProductType = String(item.product_type || payload.product_type || '').trim().toLowerCase();
            if (itemProductType && itemProductType !== currentProductType) continue;
            const strategy = String(item.strategy || '').trim();
            const product = String(item.product || '').trim();
            if (!strategy || !product) continue;
            const lookup = `${strategy}|${product}`;
            if (!allowedSet.has(lookup)) continue;
            const key = `${strategy} | ${product}`;
            const groupName = String(item.group || key);
            if (isProfileWorkflow || isTopXWorkflow) {
                // Profile/TopX workflows must not create duplicates by strategy/product across groups.
                const existsAny = activeOverlays.find(o => o.key === key);
                if (existsAny) continue;
            }
            const exists = activeOverlays.find(o => o.key === key && o.group === groupName && !o.metric);
            if (exists) continue;
            activeOverlays.push({
                key: key,
                group: groupName,
                metric: null,
                color: colors[activeOverlays.length % colors.length]
            });
            added++;
            addedGroups.add(groupName);
        }

        if (added > 0) {
            updateCharts();
            const presetName = buildWorkflowImportPresetNameV3(
                String(payload.preset_name || payload.group || payload.run_id || `WF_PROFILE_${new Date().toISOString().slice(0, 10)}`),
                currentProductType
            );
            const groups = new Set(Array.from(addedGroups));
            const overlaysForPreset = activeOverlays.filter(o => groups.has(o.group));
            if (overlaysForPreset.length > 0) {
                const signature = JSON.stringify(
                    overlaysForPreset
                        .map(o => `${String(o.key || '').trim()}|${String(o.metric || 'global').trim().toLowerCase()}`)
                        .sort()
                );
                const lastSig = localStorage.getItem(`multi_chart_v3_workflow_last_signature_${currentProductType}`) || '';
                if (signature === lastSig) {
                    console.log('[MULTI-CHART-V3-WF-IMPORT] Skipped preset save (identical workflow chart set).');
                    return;
                }
                const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
                views[presetName] = {
                    overlays: overlaysForPreset,
                    metric: document.getElementById('metricSelector') ? document.getElementById('metricSelector').value : 'net'
                };
                localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
                localStorage.setItem(`multi_chart_v3_workflow_last_signature_${currentProductType}`, signature);
                populateSavedViews();
            }
        }
    } catch (e) {
        console.warn('[MULTI-CHART-V3-WF-IMPORT] Failed:', e);
    }
}

// [V20260128_2145] Inter-View Transfer Logic
function openTransferModal(groupName) {
    document.getElementById('transferTargetGroup').value = groupName;
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    const sel = document.getElementById('transferViewSelector');
    sel.innerHTML = '<option value="">-- Select Target Preset --</option>';
    Object.keys(views).forEach(v => {
        const op = document.createElement('option');
        op.value = v;
        op.innerText = v;
        sel.appendChild(op);
    });
    document.getElementById('transferCardModal').style.display = 'flex';
}
function closeTransferModal() {
    document.getElementById('transferCardModal').style.display = 'none';
}
function submitTransfer() {
    const groupName = document.getElementById('transferTargetGroup').value;
    const targetName = document.getElementById('transferViewSelector').value;
    if (!targetName) return alert("Select view");
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi_v3') || '{}');
    if (!views[targetName]) return alert("View not found");
    const cardOverlays = activeOverlays.filter(o => o.group === groupName);
    if (cardOverlays.length === 0) return alert("Nothing to move");
    if (!views[targetName].overlays) views[targetName].overlays = [];
    views[targetName].overlays.push(...cardOverlays);
    localStorage.setItem('pnl_graph_views_multi_v3', JSON.stringify(views));
    activeOverlays = activeOverlays.filter(o => o.group !== groupName);
    alert(`Moved "${groupName}" to preset "${targetName}"`);
    closeTransferModal();
    updateCharts();
}

initEventHandlers();
fetchData();
populateSavedViews();
loadGridLiveStatus();
setTimeout(() => { consumeWorkflowImportPayloadV3(); }, 1200);
setInterval(consumeWorkflowImportPayloadV3, 15000);

const closeDrilldownModalBtn = document.getElementById('closeTradeDrilldownModal');
if (closeDrilldownModalBtn) closeDrilldownModalBtn.onclick = closeDrilldownModal;

/**
 * [V20260126_0900] Sync Live status from Backend
 */
async function loadGridLiveStatus() {
    try {
        const response = await fetch(`http://127.0.0.1:8001/api/grid_live`);
        const data = await response.json();
        if (data.success) {
            const liveGroups = data.live_models; // Object: { "GroupName": [{model, product}] }
            activeOverlays.forEach(o => {
                if (liveGroups[o.group]) {
                    o.isLive = true;
                }
            });
            updateCharts();
        }
    } catch (e) {
        console.warn("Could not load Grid Live status:", e);
    }
}

/**
 * [V20260126_1215] Trade Drilldown Logic
 */
let currentDrilldownTrades = [];
let drilldownSortColumn = 0;
let drilldownSortDir = 1; // 1 = ASC, -1 = DESC
const drilldownTradeDetailStore = {};
let drilldownTradeDetailSeq = 0;

function showTradeDrilldown(groupName) {
    const listBody = document.getElementById('drilldownTableBody');
    const titleEl = document.getElementById('drilldownTitle');
    const modal = document.getElementById('tradeDrilldownModal');
    const globalMetric = document.getElementById('metricSelector').value;

    if (!listBody || !modal) return;
    currentDrilldownTrades = [];
    titleEl.innerText = `Viewing trades for card: ${groupName}`;

    const overlays = activeOverlays.filter(o => o.group === groupName);
    const axisMaxMs = (playbackTime || datasetLatestTime || new Date()).getTime();

    overlays.forEach(o => {
        const lookupKey = o.key.replace(' | ', '|');
        const series = processedSeries[lookupKey] || [];
        const metric = o.metric || globalMetric;
        const isAlt = (metric === 'alt' || metric === 'alt_net_return_sum');
        const norm = (v) => String(v || '').trim().toLowerCase();
        const baseModel = (name) => {
            const v = norm(name);
            const m = v.match(/^(.*)_\d+_tp[\d.]+_sl[\d.]+$/);
            return m ? m[1] : v;
        };
        const expectedModel = norm(o.key.split(' | ')[0]);
        const expectedBase = baseModel(expectedModel);

        series.forEach(pt => {
            if (pt.ms <= axisMaxMs) {
                const tModelRaw = norm(pt.script_name || pt.app_name || o.key.split(' | ')[0]);
                const tBase = baseModel(tModelRaw);
                const tParams = norm(pt.strategy || pt.strategy_key || '');
                const tModelWithParams = tParams ? `${tBase}_${tParams}` : tBase;
                const stratMatch =
                    tModelRaw === expectedModel ||
                    tBase === expectedBase ||
                    tModelRaw.startsWith(`${expectedBase}_`) ||
                    tModelWithParams === expectedModel ||
                    expectedModel.startsWith(`${tBase}_`);
                if (!stratMatch) return;

                const displaySig = getDisplaySignal(pt.signal, metric);
                const indivReturn = isAlt ? (pt.net_return * -1) : pt.net_return;
                const rollingPnL = (metric === 'alt' || metric === 'alt_net_return_sum') ? pt.alt :
                    (metric === 'buy' || metric === 'buy_net_return_sum') ? pt.buy :
                        (metric === 'sell' || metric === 'sell_net_return_sum') ? pt.sell : pt.net;

                currentDrilldownTrades.push({
                    ms: pt.ms,
                    t: pt.t.substring(11, 19),
                    model: o.key.split(' | ')[0],
                    type: isAlt ? 'A' : 'N',
                    signal: displaySig,
                    result: indivReturn,
                    total: rollingPnL,
                    exit: pt.exit_time ? pt.exit_time.substring(11, 19) : '-',
                    status: pt.status,
                    live: pt.is_live,
                    filename: pt.filename || pt.source_file || ''
                });
            }
        });
    });

    // Default Sort: Time DESC
    drilldownSortColumn = 0;
    drilldownSortDir = -1;
    sortDrilldownTable(0, true);

    modal.style.display = 'flex';
}

function renderDrilldownTable() {
    const listBody = document.getElementById('drilldownTableBody');
    if (!listBody) return;
    listBody.innerHTML = '';

    currentDrilldownTrades.forEach(t => {
        const row = document.createElement('tr');
        const resCol = t.result > 0 ? '#10b981' : t.result < 0 ? '#ef4444' : '#9ca3af';
        const totCol = t.total > 0 ? '#10b981' : t.total < 0 ? '#ef4444' : '#9ca3af';
        const typeCol = t.type === 'A' ? 'var(--accent-primary)' : 'var(--text-dim)';
        const detailId = `mcv3_${++drilldownTradeDetailSeq}`;
        drilldownTradeDetailStore[detailId] = t;

        row.innerHTML = `
            <td>${t.t}</td>
            <td>${t.model}</td>
            <td style="color:${typeCol}; font-weight:800;">${t.type}</td>
            <td style="font-weight:700;">${t.signal}</td>
            <td style="color:${resCol}; font-weight:800;">${currencyFormatter.format(t.result)}</td>
            <td style="color:${totCol}; font-weight:800;">${currencyFormatter.format(t.total)}</td>
            <td style="color:var(--text-dim); font-size:0.8rem;">${t.exit}</td>
            <td style="font-size:0.8rem;">${t.status}</td>
            <td style="color:${t.live === 'Yes' ? 'var(--accent-primary)' : 'var(--text-dim)'}; font-weight:700;">${t.live}</td>
            <td><button class="btn btn-secondary" style="padding:3px 8px; font-size:0.75rem;" onclick="showDrilldownTradeDetails('${detailId}')">Details</button></td>
        `;
        listBody.appendChild(row);
    });
}

function sortDrilldownTable(colIdx, force = false) {
    if (!force) {
        if (drilldownSortColumn === colIdx) {
            drilldownSortDir *= -1;
        } else {
            drilldownSortColumn = colIdx;
            drilldownSortDir = 1;
        }
    }

    currentDrilldownTrades.sort((a, b) => {
        let valA, valB;
        switch (colIdx) {
            case 0: // Time
                valA = a.ms; valB = b.ms;
                break;
            case 1: // Model
                valA = a.model; valB = b.model;
                break;
            case 2: // Type
                valA = a.type; valB = b.type;
                break;
            case 3: // Signal
                valA = a.signal; valB = b.signal;
                break;
            case 4: // Result
                valA = a.result; valB = b.result;
                break;
            case 5: // Total
                valA = a.total; valB = b.total;
                break;
            case 6: // Exit
                valA = a.exit; valB = b.exit;
                break;
            case 7: // Status
                valA = a.status; valB = b.status;
                break;
            case 8: // live
                valA = a.live; valB = b.live;
                break;
            default:
                valA = a.ms; valB = b.ms;
        }

        if (colIdx === 0 || colIdx === 4 || colIdx === 5) {
            return (valA - valB) * drilldownSortDir;
        } else {
            return String(valA).localeCompare(String(valB)) * drilldownSortDir;
        }
    });

    renderDrilldownTable();
}

function closeDrilldownModal() {
    document.getElementById('tradeDrilldownModal').style.display = 'none';
}

async function showDrilldownTradeDetails(detailId) {
    const trade = drilldownTradeDetailStore[detailId];
    if (!trade) return;
    const mode = document.getElementById('runMode')?.value || 'live';
    const date = document.getElementById('tradeDate')?.value || new Date().toISOString().split('T')[0];
    const existing = document.getElementById('drilldownTradeJsonModal');
    if (existing) existing.remove();
    const modal = document.createElement('div');
    modal.id = 'drilldownTradeJsonModal';
    modal.className = 'modal';
    modal.style.display = 'flex';
    modal.innerHTML = `
        <div class="modal-content glass-card" style="max-width: 900px; width: 92%;">
            <div class="modal-header">
                <h2 style="font-size: 1rem;">Trade Details</h2>
                <span class="close-modal" onclick="closeDrilldownTradeDetails()">&times;</span>
            </div>
            <div class="modal-body">
                <pre id="drilldownTradeJsonBody" style="margin:0; padding:10px; max-height:60vh; overflow:auto; background:rgba(2,6,23,0.75); border:1px solid rgba(255,255,255,0.12); border-radius:8px; color:#cbd5e1; font-size:0.8rem;">Loading full trade file...</pre>
            </div>
        </div>
    `;
    modal.onclick = (e) => { if (e.target === modal) closeDrilldownTradeDetails(); };
    document.body.appendChild(modal);
    const body = document.getElementById('drilldownTradeJsonBody');
    try {
        const filename = String(trade.filename || '').trim();
        if (filename) {
            const resp = await fetch(`/api/trade_file?mode=${encodeURIComponent(mode)}&date=${encodeURIComponent(date)}&filename=${encodeURIComponent(filename)}`);
            const data = await resp.json();
            if (resp.ok && data && data.success) {
                body.textContent = JSON.stringify(data.trade_data || data.data || data, null, 2);
                return;
            }
        }
        body.textContent = JSON.stringify(trade, null, 2);
    } catch (e) {
        body.textContent = JSON.stringify(trade, null, 2);
    }
}

function closeDrilldownTradeDetails() {
    const modal = document.getElementById('drilldownTradeJsonModal');
    if (modal) modal.remove();
}

// [V20260202_1330] Validates 1st occurrence of Rank #1 for each strategy
function processFrequencyData(snapshots) {
    firstRankOneTimes = {};
    if (!snapshots || !Array.isArray(snapshots)) return;

    // Sort by time ascending
    const sorted = [...snapshots].sort((a, b) => new Date(a.time) - new Date(b.time));

    sorted.forEach(snap => {
        const ms = new Date(snap.time).getTime();
        if (snap.leaders && Array.isArray(snap.leaders)) {
            snap.leaders.forEach(l => {
                if (l.rank === 1) {
                    const k = `${l.strategy}|${l.product}`;
                    if (!firstRankOneTimes[k]) {
                        firstRankOneTimes[k] = ms;
                    }
                }
            });
        }
    });
}

// [V20260202_1345] Load all strategies that have hit Rank #1
function loadRankOneStrategies() {
    if (!firstRankOneTimes || Object.keys(firstRankOneTimes).length === 0) {
        alert("No Rank #1 strategies found in current frequency data range.");
        return;
    }

    const sortedKeys = Object.keys(firstRankOneTimes).sort((a, b) => firstRankOneTimes[a] - firstRankOneTimes[b]);

    let addedCount = 0;
    sortedKeys.forEach(rawKey => {
        const parts = rawKey.split('|');
        if (parts.length < 2) return;

        const strategy = parts[0];
        const product = parts[1];

        const overlayKey = `${strategy} | ${product}`;
        const groupName = overlayKey;

        const exists = activeOverlays.find(o => o.key === overlayKey && o.group === groupName && !o.metric);

        if (!exists) {
            activeOverlays.push({
                key: overlayKey,
                group: groupName,
                metric: null,
                color: colors[activeOverlays.length % colors.length]
            });
            addedCount++;
        }
    });

    if (addedCount > 0) {
        updateCharts();
        console.log(`Added ${addedCount} Rank #1 strategies.`);
    } else {
        alert("All Rank #1 strategies are already displayed.");
    }
}

/**
 * [V20260126_0900] Live Grid Trading Toggle
 */
async function toggleLiveMode(event, groupName) {
    event.stopPropagation(); // [V20260127_1610] Prevent dblclick drill-down from firing
    const isCurrentlyLive = activeOverlays.some(o => o.group === groupName && o.isLive);
    const newState = !isCurrentlyLive;

    // Update local state
    activeOverlays.forEach(o => {
        if (o.group === groupName) {
            o.isLive = newState;
        }
    });

    // Notify Backend (SQL API at 8001)
    const url = `http://127.0.0.1:8001/api/grid_live/toggle`;
    const globalMetric = document.getElementById('metricSelector').value;
    const cleanMetric = (globalMetric === 'alt' || globalMetric === 'alt_net_return_sum') ? 'alt' : 'net';

    try {
        const models = activeOverlays
            .filter(o => o.group === groupName)
            .map(o => ({
                model: o.key.split(' | ')[0],
                product: o.key.split(' | ')[1],
                metric: (o.metric === 'alt' || o.metric === 'alt_net_return_sum') ? 'alt' : (o.metric === 'global' ? cleanMetric : 'net')
            }));

        await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                group: groupName,
                active: newState,
                models: models,
                source: 'Trade Bucket'
            })
        });

        console.log(`[LIVE-TOGGLE] Card ${groupName} set to ${newState ? 'LIVE' : 'INACTIVE'}`);
        updateCharts();
    } catch (e) {
        console.error("Failed to sync live state to backend:", e);
        alert("Failed to sync live state! Check if SQL API (8001) is running.");
    }
}
