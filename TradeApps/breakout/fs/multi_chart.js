// [V20260319_1745] Multi-Chart Overlay Support (Refined Markers & Scaling)
// [V20260130_1650] Standardized Local Time Parsing Helper
function safeParseDate(s) {
    if (!s) return null;
    // Standardize to YYYY-MM-DD HH:MM:SS by replacing T and Z
    const clean = s.replace('T', ' ').replace('Z', '').split('.')[0];
    const parts = clean.split(' ');
    const dParts = parts[0].split('-');
    const tParts = (parts[1] || '00:00:00').split(':');
    if (dParts.length < 3) return new Date(s); // Fallback
    // Construct local date manually: new Date(yr, mo-1, day, hr, min, sec)
    const d = new Date(
        parseInt(dParts[0]),
        parseInt(dParts[1]) - 1,
        parseInt(dParts[2]),
        parseInt(tParts[0] || 0),
        parseInt(tParts[1] || 0),
        parseInt(tParts[2] || 0)
    );
    return isNaN(d.getTime()) ? null : d;
}



// [V20260312_0225] Sanitize strings for use in DOM IDs (replaces spaces/pipes/etc with underscores)
function sanitizeId(id) {
    if (!id) return '';
    return id.toString().replace(/[^a-z0-9_-]/gi, '_');
}

// State
let charts = {}; // Map of Group Names to Chart instances
let rawData = {};
let processedSeries = {};
let activeOverlays = []; // Array of { key: "strat|prod", group: "GroupName", color: "hex", metric: "net/buy_net/sell_net" }
let selectedChartGroups = new Set();
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
let availableProductTypes = ['forex'];
let drilldownModelFilter = ''; // [V20260205_0955]
let drilldownSignalFilter = 'all'; // [V20260311_1330]
const selectedPresetNames = new Set();
const liveMonitor = new LiveMonitor('/api/grid_live'); // [V20260127_1610] Fixed endpoint to match trade_viewer_api.py
const currencyFormatter = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });
let nonLivePruneInterval = null;

// Init Date
document.getElementById('tradeDate').valueAsDate = new Date();

const colors = [
    '#60a5fa', '#34d399', '#fbbf24', '#f87171', '#a78bfa',
    '#f472b6', '#22d3ee', '#a3e635', '#fb923c', '#818cf8',
    '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'
];

function getSelectedProductType() {
    return document.getElementById('productTypeSelect')?.value || 'forex';
}

function getCurrentWorkflowImportProductType(payload) {
    const selected = String(getSelectedProductType() || '').trim().toLowerCase();
    if (selected) return selected;
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

function buildWorkflowImportPresetName(baseName, productType) {
    const cleanBase = String(baseName || '').trim() || `WF_PROFILE_${new Date().toISOString().slice(0, 10)}`;
    const cleanType = String(productType || '').trim().toLowerCase();
    return cleanType ? `${cleanBase} [${cleanType.toUpperCase()}]` : cleanBase;
}

function buildProductTypeQuery() {
    return `product_type=${encodeURIComponent(getSelectedProductType())}`;
}

function populateProductTypeSelect(config) {
    const select = document.getElementById('productTypeSelect');
    if (!select) return;
    const defaults = Array.isArray(config?.product_types) && config.product_types.length > 0
        ? config.product_types
        : [config?.product_type || 'forex'];
    availableProductTypes = [...new Set(defaults.map(v => String(v).trim()).filter(Boolean))];
    if (availableProductTypes.length === 0) availableProductTypes = ['forex'];
    const params = new URLSearchParams(window.location.search);
    const preferred = params.get('product_type') || config?.product_type || availableProductTypes[0];
    select.innerHTML = availableProductTypes.map(pt => `<option value="${pt}">${pt}</option>`).join('');
    select.value = availableProductTypes.includes(preferred) ? preferred : availableProductTypes[0];
}



function getMetricValue(pt, metric) {
    if (!pt) return 0;
    if (metric === 'alt' || metric === 'alt_net_return_sum') return pt.alt ?? 0;
    if (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum' || metric === 'buy_trades') return pt.buy_net ?? pt.buy ?? 0;
    if (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum' || metric === 'sell_trades') return pt.sell_net ?? pt.sell ?? 0;
    return pt.net ?? 0;
}

function buildSteppedSeries(series, metric, startMs, axisMaxMs) {
    const getter = (pt) => getMetricValue(pt, metric);
    let baseline = 0;
    const dataPoints = [];
    dataPoints.push({ x: startMs, y: 0 });
    for (const pt of series) {
        if (pt.ms > axisMaxMs) break;
        if (pt.ms <= startMs) {
            baseline = getter(pt);
            continue;
        }
        const delta = getter(pt) - baseline;
        dataPoints.push({ x: pt.ms, y: delta });
    }
    if (dataPoints.length === 1) {
        dataPoints.push({ x: axisMaxMs, y: 0 });
    } else {
        const lastY = dataPoints[dataPoints.length - 1].y;
        dataPoints.push({ x: axisMaxMs, y: lastY });
    }
    return dataPoints;
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

function getOrderedGroupNames() {
    const ordered = [];
    activeOverlays.forEach(o => {
        if (!ordered.includes(o.group)) ordered.push(o.group);
    });
    return ordered;
}

function syncSelectedChartGroups() {
    const activeGroups = new Set(getOrderedGroupNames());
    selectedChartGroups.forEach(groupName => {
        if (!activeGroups.has(groupName)) selectedChartGroups.delete(groupName);
    });
    updateMergeControls();
}

function updateMergeControls() {
    const selectedCount = selectedChartGroups.size;
    const mergeBtn = document.getElementById('mergeSelectedCardsButton');
    const meta = document.getElementById('mergeSelectionMeta');
    if (mergeBtn) {
        mergeBtn.disabled = selectedCount < 2;
        mergeBtn.title = selectedCount < 2
            ? 'Select at least two cards to merge'
            : `Merge ${selectedCount} selected cards into one shared-scale card`;
    }
    if (meta) {
        meta.textContent = `${selectedCount} card${selectedCount === 1 ? '' : 's'} selected`;
    }

    document.querySelectorAll('.chart-card').forEach(card => {
        const isSelected = selectedChartGroups.has(card.dataset.group);
        card.classList.toggle('selected-for-merge', isSelected);
        const selectBtn = card.querySelector('.action-btn.select');
        if (selectBtn) {
            selectBtn.classList.toggle('active', isSelected);
            selectBtn.title = isSelected ? 'Deselect card from merge' : 'Select card for merge';
        }
    });
}

function toggleCardMergeSelection(event, groupName) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    if (selectedChartGroups.has(groupName)) selectedChartGroups.delete(groupName);
    else selectedChartGroups.add(groupName);
    updateMergeControls();
}

function getUniqueMergedGroupName(baseName) {
    const existing = new Set(getOrderedGroupNames());
    const rootName = String(baseName || '').trim() || 'Merged Card';
    let candidate = rootName;
    let suffix = 2;
    while (existing.has(candidate)) {
        candidate = `${rootName} (${suffix})`;
        suffix += 1;
    }
    return candidate;
}

function buildDefaultMergedGroupName(selectedGroups) {
    const now = new Date();
    const hh = String(now.getHours()).padStart(2, '0');
    const mm = String(now.getMinutes()).padStart(2, '0');
    const ss = String(now.getSeconds()).padStart(2, '0');
    return `MERGED_${selectedGroups.length}_${hh}${mm}${ss}`;
}

function mergeSelectedCards() {
    const orderedGroups = getOrderedGroupNames();
    const selectedGroups = orderedGroups.filter(groupName => selectedChartGroups.has(groupName));
    if (selectedGroups.length < 2) {
        alert('Select at least two chart cards to merge.');
        return;
    }

    const defaultName = buildDefaultMergedGroupName(selectedGroups);
    const requestedName = window.prompt('Merged card name', defaultName);
    if (requestedName === null) return;
    const mergedGroupName = getUniqueMergedGroupName(requestedName || defaultName);
    const selectedSet = new Set(selectedGroups);
    const mergedOverlays = activeOverlays
        .filter(o => selectedSet.has(o.group))
        .map((o, idx) => ({
            ...o,
            group: mergedGroupName,
            color: o.color || colors[idx % colors.length]
        }));

    const nextOverlays = [];
    let insertedMergedGroup = false;
    orderedGroups.forEach(groupName => {
        if (selectedSet.has(groupName)) {
            if (!insertedMergedGroup) {
                nextOverlays.push(...mergedOverlays);
                insertedMergedGroup = true;
            }
            destroyGroupCharts(groupName);
            if (liveMonitor.isGroupActive(groupName)) liveMonitor.deactivateGroup(groupName);
            return;
        }
        nextOverlays.push(...activeOverlays.filter(o => o.group === groupName));
    });

    activeOverlays = nextOverlays;
    selectedChartGroups.clear();
    selectedChartGroups.add(mergedGroupName);
    updateCharts();
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

/**
 * [V20260130_1540] Pulsating Animation Logic
 */
/**
 * [V20260130_1540] Pulsating Animation Logic
 * [V20260130_2130] RE-ENABLED LOOP (User Request) - X-Axis fix stabilized the chart, so animation is safe.
 */
let globalPulse = 0;
let lastPulseTick = 0;
const PULSE_FPS = 10;
const PULSE_INTERVAL = 1000 / PULSE_FPS;

function animatePulse(timestamp) {
    if (timestamp - lastPulseTick < PULSE_INTERVAL) {
        requestAnimationFrame(animatePulse);
        return;
    }
    lastPulseTick = timestamp;

    globalPulse = (Math.sin(Date.now() / 300) + 1) / 2; // Oscillates 0 to 1
    
    // Request a re-draw for all active charts to animate the dots
    Object.values(charts).forEach(entry => {
        ['net', 'buy', 'sell'].forEach(slot => {
            const chart = entry[slot];
            // Only update if chart is visible and has a canvas
            if (chart && chart.canvas && chart.canvas.offsetParent !== null) {
                chart.update('none'); 
            }
        });
    });
    requestAnimationFrame(animatePulse);
}
requestAnimationFrame(animatePulse);

/**
 * [V20260130_1515] Activation Dots Plugin
 * [V20260130_1540] Pulsating Support
 */
const activationDotsPlugin = {
    id: 'activationDots',
    afterDatasetsDraw(chart, args, options) {
        // [V20260130_2020] Dots Re-enabled (Static - No Jumpy Animation Loop)
        const { ctx, scales: { x, y } } = chart;
        const yAtTime = (dataset, t) => {
            let py = 0;
            if (dataset.data && dataset.data.length > 0) {
                for (let j = 0; j < dataset.data.length; j++) {
                    if (dataset.data[j].x <= t) py = dataset.data[j].y;
                    else break;
                }
            }
            return py;
        };

        // [V20260320_0007] Leadership Change Detection:
        // Walk all timestamps across all datasets in this chart to find where leadership switches.
        // A leadership change = the strategy with the highest net value changes from one key to another.
        const allDatasets = chart.data.datasets;
        const leadershipChanges = {}; // keyed by unique ID (key|metric), array of timestamps where it BECAME leader
        if (allDatasets.length > 1) {
            // [V20260323_1700] Use composite key (Strat|Prod + Metric) to distinguish Buy/Sell of same strategy
            const tsSet = new Set();
            allDatasets.forEach(ds => {
                if (ds.data) ds.data.forEach(pt => tsSet.add(pt.x));
            });
            const allTimestamps = Array.from(tsSet).sort((a, b) => a - b);

            let earliestBucketMs = 0;
            allDatasets.forEach(ds => {
                const bms = Number(ds._bucketStartMs || 0);
                if (bms > 0 && (earliestBucketMs === 0 || bms < earliestBucketMs)) earliestBucketMs = bms;
            });

            let prevLeaderId = null;
            for (const ts of allTimestamps) {
                let maxVal = -Infinity, curLeaderId = null;
                allDatasets.forEach(ds => {
                    const val = yAtTime(ds, ts);
                    if (val > maxVal) {
                        maxVal = val;
                        // Unique ID for this series within the card
                        curLeaderId = ds._key + '|' + (ds._metric || 'net');
                    }
                });

                if (earliestBucketMs > 0 && ts <= earliestBucketMs) {
                    prevLeaderId = curLeaderId;
                    continue;
                }
                
                if (curLeaderId && curLeaderId !== prevLeaderId && prevLeaderId !== null) {
                    if (!leadershipChanges[curLeaderId]) leadershipChanges[curLeaderId] = [];
                    leadershipChanges[curLeaderId].push(ts);
                }
                prevLeaderId = curLeaderId;
            }
        }

        chart.data.datasets.forEach((dataset, i) => {
            // [V20260130_1545] Use attached _group for robust lookup
            // [V20260130_1555] Fix Case Sensitivity for metric comparisons
            const metricKey = (dataset._metric || 'net').toLowerCase();
            const overlay = activeOverlays.find(o =>
                o.key === dataset._key &&
                o.group === dataset._group &&
                (o.metric || 'net').toLowerCase() === metricKey
            );

            // [V20260130_1535] Only draw dot if the group is actively being monitored (LIVE)
            if (overlay && overlay.activated_at && liveMonitor.isGroupActive(overlay.group)) {
                // [V20260130_1650] Robust Local Sync
                const d = safeParseDate(overlay.activated_at);
                const actTime = d ? d.getTime() : 0;

                // Only draw if within current visible axis range
                if (actTime >= x.min && actTime <= x.max) {
                    // Precision Y: find the y-value at this time in the stepped series
                    let pointY = 0;
                    if (dataset.data && dataset.data.length > 0) {
                        for (let j = 0; j < dataset.data.length; j++) {
                            if (dataset.data[j].x <= actTime) {
                                pointY = dataset.data[j].y;
                            } else {
                                break;
                            }
                        }
                    }

                    const xPos = x.getPixelForValue(actTime);
                    const yPos = y.getPixelForValue(pointY);

                    ctx.save();
                    // [V20260130_1530] Bigger & More Visible Dot
                    // High-quality composite dot: Outer Glow -> White Border -> Fill

                    // [V20260130_1600] Refined/Smaller Pulsating Dot
                    const baseRadius = 3.5;
                    const pulseRadius = baseRadius + (globalPulse * 2.0); // Radius expands 3.5 to 5.5
                    const glowRadius = 3 + (globalPulse * 6);          // Glow expands 3 to 9

                    // 1. Shadow/Glow (Pulsating)
                    ctx.shadowColor = dataset.borderColor;
                    ctx.shadowBlur = glowRadius;

                    // 2. White Outer Ring
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, pulseRadius + 1, 0, 2 * Math.PI);
                    ctx.strokeStyle = '#ffffff';
                    ctx.lineWidth = 1.0 + (globalPulse * 0.5);
                    ctx.stroke();

                    // 3. Inner Solid Fill (Strategy Color)
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, pulseRadius, 0, 2 * Math.PI);
                    ctx.fillStyle = dataset.borderColor;
                    ctx.fill();

                    // 4. Center Highlight Point (Tiny)
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, 1.5, 0, 2 * Math.PI);
                    ctx.fillStyle = '#ffffff';
                    ctx.fill();

                    ctx.restore();
                }
            }


            // [V20260303_2305] Fluorescent Yellow Dot:
            // For Trade Bucket cards, use the strategy's bucket rank-1 hit time from grid_live activation.
            // For non-bucket cards, keep legacy first Rank #1 timestamp from frequency data.
            let rankOneTime = null;
            if (Number(dataset._bucketStartMs || 0) > 0) {
                const metricKeyForRank = (dataset._metric || 'net').toLowerCase();
                const sameBucketOverlays = activeOverlays.filter(o =>
                    o.key === dataset._key &&
                    o.group === dataset._group
                );
                // Prefer exact metric match, then any same key/group overlay with activation time.
                const overlayForRank =
                    sameBucketOverlays.find(o => (o.metric || 'net').toLowerCase() === metricKeyForRank && !!o.activated_at)
                    || sameBucketOverlays.find(o => !!o.activated_at)
                    || null;
                if (overlayForRank && overlayForRank.activated_at) {
                    const dRank = safeParseDate(overlayForRank.activated_at);
                    const msRank = dRank ? dRank.getTime() : 0;
                    if (msRank) rankOneTime = msRank;
                }
            } else {
                const cleanKey = dataset._key.replace(/\s+\|\s+/g, '|'); // Key from overlay might have spaces "Strat | Prod"
                rankOneTime = firstRankOneTimes[cleanKey];
            }

            if (rankOneTime && rankOneTime >= x.min && rankOneTime <= x.max) {
                const pointY = yAtTime(dataset, rankOneTime);

                const xPos = x.getPixelForValue(rankOneTime);
                const yPos = y.getPixelForValue(pointY);

                ctx.save();
                // Fluorescent Yellow Dot
                ctx.shadowColor = 'black';
                ctx.shadowBlur = 4;

                ctx.beginPath();
                ctx.arc(xPos, yPos, 4, 0, 2 * Math.PI); // [V20260319_1745] Reduced size for cleaner UI
                ctx.fillStyle = '#CCFF00'; // Fluorescent Yellow
                ctx.fill();

                // Black border for contrast
                ctx.lineWidth = 3;
                ctx.strokeStyle = '#000000';
                ctx.stroke();

                ctx.restore();
            }

            // [V20260215_0005] Trade Bucket Creation Dot:
            // show marker at the bucket creation timestamp when viewing bucket groups.
            const bucketStartMs = Number(dataset._bucketStartMs || 0);
            if (bucketStartMs && bucketStartMs >= x.min && bucketStartMs <= x.max) {
                const pointY = yAtTime(dataset, bucketStartMs);
                const xPos = x.getPixelForValue(bucketStartMs);
                const yPos = y.getPixelForValue(pointY);

                ctx.save();
                ctx.shadowColor = '#06b6d4';
                ctx.shadowBlur = 4;

                // Cyan outer ring
                ctx.beginPath();
                ctx.arc(xPos, yPos, 4, 0, 2 * Math.PI);
                ctx.strokeStyle = '#67e8f9';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                // Solid center
                ctx.beginPath();
                ctx.arc(xPos, yPos, 2, 0, 2 * Math.PI);
                ctx.fillStyle = '#06b6d4';
                ctx.fill();

                // White highlight center
                ctx.beginPath();
                ctx.arc(xPos, yPos, 1, 0, 2 * Math.PI);
                ctx.fillStyle = '#ffffff';
                ctx.fill();
                ctx.restore();
            }

            // [V20260323_1700] Draw deep green dots where this strategy took over leadership.
            const uniqueId = dataset._key + '|' + (dataset._metric || 'net');
            const myChanges = leadershipChanges[uniqueId] || [];
            myChanges.forEach(changeMs => {
                if (changeMs >= x.min && changeMs <= x.max) {
                    const pointY = yAtTime(dataset, changeMs);
                    const xPos = x.getPixelForValue(changeMs);
                    const yPos = y.getPixelForValue(pointY);

                    ctx.save();
                    ctx.shadowColor = '#00C853';
                    ctx.shadowBlur = 4;

                    // Deep green outer ring
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, 4, 0, 2 * Math.PI);
                    ctx.strokeStyle = '#00E676';
                    ctx.lineWidth = 1.5;
                    ctx.stroke();

                    // Solid deep green center
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, 2.5, 0, 2 * Math.PI);
                    ctx.fillStyle = '#00C853';
                    ctx.fill();

                    // White highlight center
                    ctx.beginPath();
                    ctx.arc(xPos, yPos, 1, 0, 2 * Math.PI);
                    ctx.fillStyle = '#ffffff';
                    ctx.fill();
                    ctx.restore();
                }
            });
        });
    }
};

function initEventHandlers() {
    document.getElementById('runMode').addEventListener('change', () => { fetchData(); populateSavedViews(); });
    document.getElementById('tradeDate').addEventListener('change', () => { fetchData(); populateSavedViews(); });
    document.getElementById('productTypeSelect')?.addEventListener('change', () => { fetchData(); populateSavedViews(); });
    document.getElementById('metricSelector').addEventListener('change', updateCharts);
    document.getElementById('addBtn').addEventListener('click', addOverlayHandler);
    document.getElementById('rankApplyButton').addEventListener('click', applyRankSelection);
    document.getElementById('btnShowRankOnes').addEventListener('click', loadRankOneStrategies); // [V20260202_1345]
    const mergeSelectedCardsButton = document.getElementById('mergeSelectedCardsButton');
    if (mergeSelectedCardsButton) mergeSelectedCardsButton.addEventListener('click', mergeSelectedCards);
    document.getElementById('saveViewButton').addEventListener('click', saveCurrentView);
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

    // [V20260130_1515] Register Plugin Globals
    Chart.register(activationDotsPlugin);

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

    const exportCsvBtn = document.getElementById('exportDrilldownCsvBtn');
    if (exportCsvBtn) exportCsvBtn.addEventListener('click', exportDrilldownToCSV);

    const modelSelect = document.getElementById('drilldownModelSelect');
    if (modelSelect) {
        modelSelect.addEventListener('change', (e) => {
            drilldownModelFilter = e.target.value.toLowerCase().trim();
            renderDrilldownTable();
        });
    }

    const signalSelect = document.getElementById('drilldownSignalSelect');
    if (signalSelect) {
        signalSelect.addEventListener('change', (e) => {
            drilldownSignalFilter = e.target.value.toLowerCase();
            renderDrilldownTable();
        });
    }

    document.getElementById('displayButton').addEventListener('click', () => fetchData());


    // [V20260205_1230] Batch Create Logic
    const openBatchBtn = document.getElementById('openBatchCreateBtn');
    if (openBatchBtn) openBatchBtn.addEventListener('click', openBatchCreator);

    const closeBatchBtn = document.getElementById('closeBatchCreateModal');
    if (closeBatchBtn) closeBatchBtn.onclick = () => document.getElementById('batchCreateModal').style.display = 'none';

    const cancelBatchBtn = document.getElementById('cancelBatchCreate');
    if (cancelBatchBtn) cancelBatchBtn.onclick = () => document.getElementById('batchCreateModal').style.display = 'none';

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
                nextRefreshTime = Date.now() + 10000; // [V20260128_1720] Faster refresh
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
    // [V20260131_0315] Sync mode to liveMonitor
    if (liveMonitor && liveMonitor.setMode) liveMonitor.setMode(mode);

    const date = document.getElementById('tradeDate').value;
    const url = `/api/trade_file?mode=${mode}&date=${date}&filename=_summary_net.json&${buildProductTypeQuery()}&_t=${Date.now()}`;

    try {
        const res = await fetch(url);
        const json = await res.json();

        // [V20260202_1330] Fetch Frequency Data for Rank #1 Dots
        try {
            const freqUrl = `/api/trade_file?mode=${mode}&date=${date}&filename=_frequency.json&${buildProductTypeQuery()}&_t=${Date.now()}`;
            const fRes = await fetch(freqUrl);
            if (fRes.ok) {
                const fJson = await fRes.json();
                // API wraps content in "content" or returns direct? 
                // trade_viewer_api returns {success:true, content: ...} usually
                const fData = fJson.content || fJson;
                if (fData.snapshots) {
                    processFrequencyData(fData.snapshots);
                }
            }
        } catch (e) {
            console.warn("Frequency data fetch failed", e);
            firstRankOneTimes = {}; // Reset on fail
        }

        // [V20260129_1055] Periodic re-sync logic (datetime: 2026-01-29 11:00)
        try {
            const liveRes = await fetch(`/api/grid_live?mode=${mode}`);
            const liveData = await liveRes.json();
            if (liveData.success) {
                const gridData = liveData.data || [];
                let gridDirty = false;

                // gridData is now a List of {group, model, product, metric}
                if (Array.isArray(gridData)) {
                    gridData.forEach(m => {
                        const groupName = m.group;
                        const key = `${m.model} | ${m.product}`;
                        const normalizedMetric = (m.metric === 'net') ? null : m.metric;
                        const exists = activeOverlays.find(o => o.key === key && o.group === groupName && o.metric === normalizedMetric);

                        if (!exists) {
                            activeOverlays.push({
                                key: key,
                                group: groupName,
                                metric: normalizedMetric,
                                activated_at: m.activated_at, // [V20260130_1515] Capture activation time
                                color: colors[activeOverlays.length % colors.length]
                            });
                            gridDirty = true;
                        } else {
                            // [V20260130_1530] Ensure activation time is synced even for existing
                            exists.activated_at = m.activated_at;
                        }
                        if (!liveMonitor.isGroupActive(groupName)) {
                            liveMonitor.activeGroups.add(groupName);
                        }
                    });

                    // [V20260130_1635] Sync LiveMonitor internal memory to prevent redundant updates
                    liveMonitor.syncState(gridData);
                }
                if (gridDirty) {
                    console.log("[Auto-Sync] Added new cards from grid_live.json");
                }
            }
        } catch (e) { console.warn("Grid sync failed:", e); }

        if (json.success) {
            rawData = json.content;
            const newProcessedSeries = {};
            if (rawData.strategies) {
                for (const strat in rawData.strategies) {
                    for (const prod in rawData.strategies[strat]) {
                        const key = `${strat}|${prod}`;
                        const series = rawData.strategies[strat][prod] || [];
                        newProcessedSeries[key] = series.map(pt => {
                            // [V20260130_1550] Force Local Time: Strip 'Z' if present
                            const ts = pt.t.endsWith('Z') ? pt.t.slice(0, -1) : pt.t;
                            const dt = new Date(ts);
                            return {
                                t: ts,
                                ms: dt.getTime(),
                                net: pt.net || 0,
                                buy_net: pt.buy_net || 0,
                                sell_net: pt.sell_net || 0,
                                trade_count: (pt.b_c || 0) + (pt.s_c || 0)
                            };
                        })
                            .filter(pt => pt.ms && !isNaN(pt.ms)) // [V20260130_1935] Filter invalid dates
                            .sort((a, b) => a.ms - b.ms);
                    }
                }
            }
            processedSeries = newProcessedSeries;
            document.getElementById('lastUpdate').innerText = new Date().toLocaleTimeString();
            if (!playbackTime) playbackTime = getPlaybackBoundaries().endOfDay;

            updateDatasetTimeBounds();
            populateSelectors();
            updateCharts();
        }
    } catch (e) {
        console.error("Fetch error:", e);
        document.getElementById('lastUpdate').innerText = "Retry...";
    }
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

// [V20260126_1430] The loadGridLiveStatus function was removed. It is replaced by the LiveMonitor class.
// [V20260128_1428] Helper to build groupMap from activeOverlays
function buildGroupMap() {
    const groupMap = {};
    activeOverlays.forEach(o => {
        if (!groupMap[o.group]) groupMap[o.group] = [];
        groupMap[o.group].push(o);
    });
    return groupMap;
}

// [V20260128_1428] Helper to set the LIVE button visual state
function setLiveButtonState(groupName, isActive) {
    const cards = Array.from(document.querySelectorAll('.chart-card'));
    const card = cards.find(c => c.dataset.group === groupName);
    if (!card) return;

    const btn = card.querySelector('.live-btn');
    if (!btn) return;

    const span = btn.querySelector('span');

    if (isActive) {
        btn.classList.add('active');
        if (span) span.innerText = 'LIVE: ON';
        if (!btn.querySelector('.live-pulse')) {
            const pulseEl = document.createElement('span');
            pulseEl.className = 'live-pulse';
            btn.appendChild(pulseEl);
        }
    } else {
        btn.classList.remove('active');
        if (span) span.innerText = 'LIVE: OFF';
        const pulse = btn.querySelector('.live-pulse');
        if (pulse) pulse.remove();
    }
}

function toggleLiveMode(event, groupName) {
    event.stopPropagation();
    // [V20260129_1055] Continuous Leader Monitoring toggle (datetime: 20260129 11:00)
    const isCurrentlyActive = liveMonitor.isGroupActive(groupName);
    const nextState = !isCurrentlyActive;

    if (nextState) {
        // [V20260129_1042] Identify current top performer for this card
        const overlays = activeOverlays.filter(o => o.group === groupName);
        if (overlays.length === 0) return;

        const globalMetric = document.getElementById('metricSelector').value;
        const startMs = (getActiveStartTime() || new Date(0)).getTime();
        const evalMs = (playbackTime || new Date()).getTime();

        let bestLeader = null;
        let maxDelta = -Infinity;

        overlays.forEach(o => {
            const metric = o.metric || globalMetric;
            const field = (metric === 'buy_net' || metric === 'buy_trades') ? 'buy_net' :
                (metric === 'sell_net' || metric === 'sell_trades') ? 'sell_net' : 'net';

            const series = processedSeries[o.key.replace(' | ', '|')];
            if (!series) return;

            let sVal = 0, eVal = 0;
            for (const pt of series) {
                if (pt.ms <= startMs) sVal = pt[field] || 0;
                if (pt.ms <= evalMs) eVal = pt[field] || 0;
                if (pt.ms > evalMs) break;
            }
            const delta = eVal - sVal;

            if (delta > maxDelta || !bestLeader) {
                maxDelta = delta;
                const parts = o.key.includes(' | ') ? o.key.split(' | ') : o.key.split('|');
                bestLeader = {
                    model: parts[0],
                    product: parts[1],
                    metric: metric
                };
            }
        });

        if (bestLeader) {
            liveMonitor.activateGroup(groupName, bestLeader);
        }
    } else {
        liveMonitor.deactivateGroup(groupName);
    }

    setLiveButtonState(groupName, nextState);
}

function populateSelectors() {
    const prodSel = document.getElementById('productSelector'), stratSel = document.getElementById('strategySelector');
    const products = new Set(), strategies = new Set();
    if (rawData.strategies) {
        for (const [stratName, prodMap] of Object.entries(rawData.strategies)) {
            strategies.add(stratName);
            Object.keys(prodMap).forEach(p => products.add(p));
        }
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

    const normalizedMetric = (metric === 'global' || metric === 'net') ? null : metric;

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
    if (rawData.strategies) {
        for (const [stratName, prodMap] of Object.entries(rawData.strategies)) {
            strategies.add(stratName);
            Object.keys(prodMap).forEach(p => products.add(p));
        }
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

    const normalizedMetric = (metric === 'net') ? null : metric;

    const exists = activeOverlays.find(o => o.key === key && o.group === groupName && o.metric === normalizedMetric);
    if (!exists) {
        activeOverlays.push({
            key: key,
            group: groupName,
            metric: normalizedMetric,
            color: colors[activeOverlays.length % colors.length]
        });
        updateCharts();
    }
    closeModal();
}

/**
 * [V20260203_1315] Add Remaining Strategies (Exact Set of 4)
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

    // 1. Extract Parameter Suffix (e.g. "_4_tp20.0_sl6.0")
    // Looks for underscore, digit(s), underscore, tp
    const paramMatch = refStrategy.match(/_(\d+)_tp([\d\.]+)_sl([\d\.]+)/);
    if (!paramMatch) {
        alert("Could not extract version/params from strategy name (expected format: ..._N_tpX_slY).");
        return;
    }
    const paramsSuffix = paramMatch[0]; // e.g. "_4_tp20.0_sl6.0"

    // [V20260308_1941] Identify all distinct metrics in the active chart group
    const metricsToApply = [...new Set(overlaysInGroup.map(o => o.metric || null))];

    // 2. Define the 4 Standard Prefixes
    const prefixes = ['breakout', 'breakout_R', 'breakout_Rev', 'breakout_R_Rev'];

    let addedCount = 0;

    // 3. Construct and Add Targets
    prefixes.forEach(prefix => {
        const targetName = prefix + paramsSuffix;

        // Skip if it's the reference strategy (already known to exist, likely already in chart)
        // But we check existence in activeOverlays anyway.

        if (rawData.strategies && rawData.strategies[targetName] && rawData.strategies[targetName][product]) {
            const key = `${targetName} | ${product}`;
            
            metricsToApply.forEach(inheritedMetric => {
                const exists = activeOverlays.find(o => o.group === groupName && o.key === key && (o.metric || null) === inheritedMetric);

                if (!exists) {
                    activeOverlays.push({
                        key: key,
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
        alert("No other strategies from the set (Breakout, R, Rev, R_Rev) found.");
    }
}

function addMetricsToGroup(groupName) {
    // This is now legacy/unused as we use the Modal, but kept for compatibility
    const firstOverlay = activeOverlays.find(o => o.group === groupName);
    if (!firstOverlay) return;

    const key = firstOverlay.key;
    const metricsToAdd = ['net', 'buy_net', 'sell_net'];

    metricsToAdd.forEach(m => {
        const normalizedM = (m === 'net') ? null : m;
        const exists = activeOverlays.find(o => o.key === key && o.group === groupName && o.metric === normalizedM);
        if (!exists) {
            activeOverlays.push({
                key: key,
                group: groupName,
                metric: normalizedM,
                color: colors[activeOverlays.length % colors.length]
            });
        }
    });
    updateCharts();
}

function removeOverlay(key, groupPrefix, metric) {
    const targetMetric = (metric === 'null' || metric === 'undefined') ? null : metric;
    activeOverlays = activeOverlays.filter(o => {
        const metricMatch = (o.metric === targetMetric) || (targetMetric === 'net' && (o.metric === null || o.metric === 'net'));
        return !(o.key === key && o.group === groupPrefix && metricMatch);
    });
    updateCharts();
}

function removeGroup(groupName) {
    activeOverlays = activeOverlays.filter(o => o.group !== groupName);
    updateCharts();
}

function computeGroupNetDelta(groupName, forcedMetric = null) {
    const globalMetric = document.getElementById('metricSelector').value || 'net';
    const { startOfDay } = getPlaybackBoundaries();
    const startMs = (getActiveStartTime() || startOfDay).getTime();
    const axisMaxMs = (playbackTime || datasetLatestTime || new Date()).getTime();
    const configs = activeOverlays.filter(o => o.group === groupName);
    let total = 0;

    configs.forEach(config => {
        const lookupKey = config.key.replace(' | ', '|');
        const series = processedSeries[lookupKey] || [];
        const metric = forcedMetric || config.metric || globalMetric;
        let baseline = 0;
        let lastVal = 0;
        for (let i = 0; i < series.length; i++) {
            const pt = series[i];
            const val = (metric === 'alt' || metric === 'alt_net_return_sum') ? pt.alt :
                (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') ? (pt.buy_net ?? pt.buy ?? 0) :
                    (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') ? (pt.sell_net ?? pt.sell ?? 0) : (pt.net || 0);
            if (pt.ms <= startMs) baseline = val;
            if (pt.ms <= axisMaxMs) lastVal = val - baseline;
            else break;
        }
        total += (Number(lastVal) || 0);
    });

    return total;
}

function computeOverlayNetDelta(config, forcedMetric = null) {
    const globalMetric = document.getElementById('metricSelector').value || 'net';
    const { startOfDay } = getPlaybackBoundaries();
    const startMs = (getActiveStartTime() || startOfDay).getTime();
    const axisMaxMs = (playbackTime || datasetLatestTime || new Date()).getTime();
    const lookupKey = String(config.key || '').replace(' | ', '|');
    const series = processedSeries[lookupKey] || [];
    const metric = forcedMetric || config.metric || globalMetric;
    let baseline = 0;
    let lastVal = 0;

    for (let i = 0; i < series.length; i++) {
        const pt = series[i];
        const val = (metric === 'alt' || metric === 'alt_net_return_sum') ? pt.alt :
            (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') ? (pt.buy_net ?? pt.buy ?? 0) :
                (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') ? (pt.sell_net ?? pt.sell ?? 0) : (pt.net || 0);
        if (pt.ms <= startMs) baseline = val;
        if (pt.ms <= axisMaxMs) lastVal = val - baseline;
        else break;
    }
    return Number(lastVal) || 0;
}

async function runNegativeNonLiveCardPruneWorkflow() {
    try {
        const resp = await fetch('/api/workflows');
        const data = await resp.json();
        if (!data.success) return;
        const wf = (data.workflows || []).find(w => String(w.id) === 'multi_chart_prune_negative_non_live');
        if (!wf || !wf.enabled || !wf.active_now) return;

        const cfg = (wf.config && typeof wf.config === 'object') ? wf.config : {};
        const negativeThreshold = Number(cfg.negative_threshold ?? 0);
        const groups = [...new Set(activeOverlays.map(o => o.group))];
        const toRemove = [];

        groups.forEach(groupName => {
            if (liveMonitor.isGroupActive(groupName)) return;
            const groupOverlays = activeOverlays.filter(o => o.group === groupName);
            if (!groupOverlays.length) return;
            const allNegative = groupOverlays.every(o => computeOverlayNetDelta(o, 'net') < negativeThreshold);
            if (allNegative) toRemove.push(groupName);
        });

        if (!toRemove.length) return;
        activeOverlays = activeOverlays.filter(o => !toRemove.includes(o.group));
        updateCharts();
        console.log(`[WF] multi_chart_prune_negative_non_live removed ${toRemove.length} card(s):`, toRemove);
    } catch (e) {
        console.warn('[WF] multi_chart_prune_negative_non_live failed:', e);
    }
}

/**
 * [V20260128_2130] Reorder cards by moving their associated overlays in activeOverlays
 */
function moveGroup(groupName, direction) {
    // 1. Get unique groups in current order
    const orderedGroups = [];
    activeOverlays.forEach(o => {
        if (!orderedGroups.includes(o.group)) {
            orderedGroups.push(o.group);
        }
    });

    const idx = orderedGroups.indexOf(groupName);
    if (idx === -1) return;

    const targetIdx = idx + direction;
    if (targetIdx < 0 || targetIdx >= orderedGroups.length) return;

    // 2. Swap group names
    const temp = orderedGroups[idx];
    orderedGroups[idx] = orderedGroups[targetIdx];
    orderedGroups[targetIdx] = temp;

    // 3. Reconstruct activeOverlays in the new group order
    const newOverlays = [];
    orderedGroups.forEach(g => {
        const members = activeOverlays.filter(o => o.group === g);
        newOverlays.push(...members);
    });

    activeOverlays = newOverlays;
    updateCharts();
}

// [V20260202_1345] Load all strategies that have hit Rank #1
function loadRankOneStrategies() {
    if (!firstRankOneTimes || Object.keys(firstRankOneTimes).length === 0) {
        alert("No Rank #1 strategies found in current frequency data range.");
        return;
    }

    // Sort keys by time (earliest attainment of Rank #1 first)
    // Key format in firstRankOneTimes is "Strat|Prod"
    const sortedKeys = Object.keys(firstRankOneTimes).sort((a, b) => firstRankOneTimes[a] - firstRankOneTimes[b]);

    let addedCount = 0;
    sortedKeys.forEach(rawKey => {
        const parts = rawKey.split('|');
        if (parts.length < 2) return;

        const strategy = parts[0];
        const product = parts[1];

        // Construct overlay key: "Strat | Prod"
        const overlayKey = `${strategy} | ${product}`;
        const groupName = overlayKey; // Default grouping

        // Check if exists
        const exists = activeOverlays.find(o => o.key === overlayKey && o.group === groupName && !o.metric);

        if (!exists) {
            activeOverlays.push({
                key: overlayKey,
                group: groupName,
                metric: null, // Default 'net'
                color: colors[activeOverlays.length % colors.length],
                isLive: false
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

function clearAllOverlays() {
    activeOverlays = [];
    Object.keys(charts).forEach(destroyGroupCharts);
    updateCharts();
}

const visibleGroups = new Set();
const chartObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        const group = entry.target.dataset.group;
        if (entry.isIntersecting) {
            visibleGroups.add(group);
            // Trigger an immediate update for this newly visible card
            updateCharts(); 
        } else {
            visibleGroups.delete(group);
        }
    });
}, { threshold: 0.05 });

let updateChartsTimeout = null;
function updateCharts(filterTime = null) {
    if (updateChartsTimeout) return;
    updateChartsTimeout = setTimeout(() => {
        updateChartsImmediate(filterTime);
        updateChartsTimeout = null;
    }, 50); // 50ms debounce
}

function updateChartsImmediate(filterTime = null) {
    const grid = document.getElementById('chartGrid');
    const globalMetric = document.getElementById('metricSelector').value;
    if (activeOverlays.length === 0) {
        grid.innerHTML = '<div class="empty-grid-msg">No charts added. Use Auto or Add Chart to compare.</div>';
        Object.keys(charts).forEach(destroyGroupCharts);
        selectedChartGroups.clear();
        updateMergeControls();
        return;
    }

    const emptyMsg = grid.querySelector('.empty-grid-msg');
    if (emptyMsg) emptyMsg.remove();

    const { startOfDay, endOfDay } = getPlaybackBoundaries();
    const startMs = (getActiveStartTime() || startOfDay).getTime();
    const axisMaxMs = (filterTime || (isPlaying ? playbackTime : null) || datasetLatestTime).getTime();

    const groupMap = {};
    activeOverlays.forEach(o => {
        if (!groupMap[o.group]) groupMap[o.group] = [];
        groupMap[o.group].push(o);
    });
    syncSelectedChartGroups();

    liveMonitor.update(processedSeries, groupMap, globalMetric, startMs, axisMaxMs);

    grid.querySelectorAll('.chart-card').forEach(card => {
        if (!groupMap[card.dataset.group]) {
            const g = card.dataset.group;
            destroyGroupCharts(g);
            selectedChartGroups.delete(g);
            card.remove();
        }
    });

    const fetchProms = [];
    const orderedGroupNames = [];
    activeOverlays.forEach(o => { if (!orderedGroupNames.includes(o.group)) orderedGroupNames.push(o.group); });

    orderedGroupNames.forEach((groupName, idx) => {
        const configs = groupMap[groupName];
        if (!configs) return;
        const cards = Array.from(grid.querySelectorAll('.chart-card'));
        let card = cards.find(c => c.dataset.group === groupName);
        if (!card) {
            card = createGroupCard(groupName);
            chartObserver.observe(card); // [V20260424_2245] Monitor for visibility
        }

        // [V20260424_2245] Performance optimization: Skip rendering logic for off-screen cards
        if (!visibleGroups.has(groupName)) {
            // Ensure card is in correct DOM position even if not rendered
            if (grid.children[idx] !== card) {
                grid.insertBefore(card, grid.children[idx] || null);
            }
            return;
        }
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
        if (grid.children[idx] !== card) {
            grid.insertBefore(card, grid.children[idx] || null);
        }

        const isGroupLive = liveMonitor.isGroupActive(groupName);
        let leaderKey = null, maxDelta = -Infinity;

        const dsPre = configs.map(config => {
            const lookupKey = config.key.replace(' | ', '|');
            const series = processedSeries[lookupKey] || [];
            const metric = config.metric || globalMetric;

            let baseline = 0;
            let lastVal = 0;
            for (const pt of series) {
                const val = getMetricValue(pt, metric);
                if (pt.ms <= startMs) baseline = val;
                if (pt.ms <= axisMaxMs) lastVal = val - baseline;
                else break;
            }
            if (lastVal > maxDelta) { maxDelta = lastVal; leaderKey = config.key; }
            return { config, lookupKey, metric };
        });

        const datasets = dsPre.map(pre => {
            const series = processedSeries[pre.lookupKey] || [];
            const metric = pre.metric;
            const dataPoints = buildSteppedSeries(series, metric, startMs, axisMaxMs);
            const isLeader = (isGroupLive && pre.config.key === leaderKey);
            const metricLabel = (metric === 'alt' || metric === 'alt_net_return_sum') ? 'Alt' :
                (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') ? 'Buy' :
                    (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') ? 'Sell' : 'Net';

            const ds = {
                label: `${pre.config.key} (${metricLabel})`,
                data: dataPoints,
                borderColor: pre.config.color,
                backgroundColor: 'transparent',
                fill: false,
                stepped: true,
                borderWidth: isLeader ? 3 : 1.5,
                pointRadius: 0,
                pointHoverRadius: 0,
                pointHitRadius: 10,
                parsing: false,
                _metric: metric,
                _key: pre.config.key,
                _group: groupName,
                _bucketStartMs: 0
            };

            const bucketMeta = loadedBuckets.find(b => b.name === groupName);
            if (bucketMeta && bucketMeta.start_time) {
                const d_bucket = safeParseDate(String(bucketMeta.start_time));
                if (d_bucket && !isNaN(d_bucket.getTime())) {
                    ds._bucketStartMs = d_bucket.getTime();
                }
            }

            return ds;
        });

        Promise.all(fetchProms).then(() => {
            renderGroupCharts({
                groupName,
                card,
                configs,
                datasets,
                startMs,
                axisMaxMs,
                leaderKey,
                isGroupLive
            });
            const listEl = card.querySelector('.group-values-list');
            listEl.innerHTML = configs.map(c => {
                const metric = c.metric || globalMetric;
                const ds = datasets.find(d => d._key === c.key && d._metric === metric);
                const lastVal = ds ? ds.data.slice(-1)[0].y : 0;
                const colorClass = lastVal > 0 ? '#10b981' : lastVal < 0 ? '#ef4444' : '#9ca3af';
                const metricLabel = (metric === 'buy' || metric === 'buy_net' || metric === 'buy_trades' || metric === 'buy_net_return_sum') ? 'B' :
                    (metric === 'sell' || metric === 'sell_net' || metric === 'sell_trades' || metric === 'sell_net_return_sum') ? 'S' : 'T';
                const isLive = c.isLive;
                const isLeader = (isGroupLive && c.key === leaderKey);
                const pulse = isLive ? '<span class="live-pulse"></span>' : '';
                const leaderBadge = isLeader ? '<span style="color:var(--accent-primary); font-size:0.6rem; border:1px solid; border-radius:4px; padding:0 4px; margin-right:4px;">L-TRADE</span>' : '';

                return `<div class="group-value-item">
                            <span class="dot" style="background:${c.color}"></span>
                            <span class="lbl" title="${c.key}">${pulse}${leaderBadge}${c.key.split(' | ')[0]} [${metricLabel}]</span>
                            <span class="val" style="color:${colorClass}">${currencyFormatter.format(lastVal)}</span>
                            <i class="fas fa-times-circle" onclick="removeOverlay('${c.key}', '${groupName}', '${c.metric}')"></i>
                        </div>`;
            }).join('');
        });
    });
    updateMergeControls();
}

function renderGroupCharts({ groupName, card, configs, datasets, startMs, axisMaxMs, leaderKey, isGroupLive }) {
    const netContainer = card.querySelector('.chart-container.net-view');
    if (netContainer) netContainer.style.display = 'flex';
    renderNetChart(groupName, card, datasets, startMs, axisMaxMs, leaderKey, isGroupLive);
}

function renderNetChart(groupName, card, datasets, minX, maxX, leaderKey, isGroupLive) {
    const canvasId = `group-chart-${sanitizeId(groupName)}-net`;
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    renderChartOnCanvas(groupName, 'net', canvas, datasets, minX, maxX);
}



function renderChartOnCanvas(groupName, slot, canvas, datasets, minX, maxX) {
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
        data: { datasets: datasets },
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
    div.style.minHeight = '250px'; // [V20260129_1400] Reduced from 420px (datetime: 20260129 14:00)
    div.title = "Double-click to view trade list";
    div.ondblclick = () => showTradeDrilldown(groupName);

    const isLive = liveMonitor.isGroupActive(groupName); // [V20260126_1430]
    const mode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';
    const isSim = mode === 'sim';
    const liveClass = isLive ? (isSim ? 'active sim' : 'active') : '';
    const liveText = isLive ? (isSim ? 'SIM: ON' : 'LIVE: ON') : 'LIVE: OFF';
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
                        ${isLive ? '<span class="live-pulse"></span>' : ''}
                    </button>
                </div>
                <div class="chart-actions">
                    <!-- [V20260413_1410] Added event.stopPropagation() to both click and dblclick below -->
                    <button class="action-btn" onclick="event.stopPropagation(); moveGroup('${groupName}', -1)" ondblclick="event.stopPropagation()" title="Move card left">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); moveGroup('${groupName}', 1)" ondblclick="event.stopPropagation()" title="Move card right">
                        <i class="fas fa-chevron-right"></i>
                    </button>

                    <button class="action-btn" onclick="event.stopPropagation(); openTransferModal('${groupName}')" ondblclick="event.stopPropagation()" title="Move this card to another saved preset">
                        <i class="fas fa-exchange-alt"></i>
                    </button>

                    <button class="action-btn select" onclick="toggleCardMergeSelection(event, '${groupName}')" ondblclick="event.stopPropagation()" title="Select card for merge">
                        <i class="fas fa-check-square"></i>
                    </button>

                    <button class="action-btn" onclick="event.stopPropagation(); addRelatedStrategies('${groupName}')" ondblclick="event.stopPropagation()" title="Add all strategies with same parameters (Complete Set)">
                        <i class="fas fa-clone"></i>
                    </button>
                    <button class="action-btn" onclick="event.stopPropagation(); addAllWindows('${groupName}')" ondblclick="event.stopPropagation()" title="Add all window sizes for this strategy">
                        <i class="fas fa-layer-group"></i>
                    </button>

                    <button class="action-btn add" onclick="event.stopPropagation(); openAddOverlayModal('${groupName}')" ondblclick="event.stopPropagation()" title="Add specific comparison to this card">      
                        <i class="fas fa-plus"></i>
                    </button>
                    <button class="action-btn save" onclick="event.stopPropagation(); saveToBucket('${groupName}')" ondblclick="event.stopPropagation()" title="Create Trade Bucket from this card">
                        <i class="fas fa-folder-plus"></i>
                    </button>
                    ${splitButton}
                    <button class="action-btn delete" onclick="event.stopPropagation(); removeGroup('${groupName}')" ondblclick="event.stopPropagation()" title="Remove this card">
                        <i class="fas fa-trash-alt"></i>
                    </button>
                </div>            </div>
        <div class="group-values-list" style="display:grid; grid-template-columns: 1fr 1fr; gap:5px; font-size:0.7rem;"></div>
        </div>
        <div class="chart-container net-view" style="height:150px; margin-top:10px;" data-mode="net">
            <canvas id="group-chart-${sanitizeId(groupName)}-net"></canvas>
        </div>
    `;
    div.classList.toggle('selected-for-merge', selectedChartGroups.has(groupName));
    return div;
}

function getPlaybackBoundaries() {
    const dateVal = document.getElementById('tradeDate').value;
    // [V20260130_1550] Use Local Time (no T...Z)
    const startOfDay = new Date(dateVal + 'T00:00:00');
    const now = new Date();
    const isToday = (dateVal === now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0'));
    let endOfDay = isToday ? now : new Date(dateVal + 'T23:59:59');
    return { startOfDay, endOfDay };
}

function updateDatasetTimeBounds() {
    let earliest = null, latest = null;
    for (const key in processedSeries) {
        const series = processedSeries[key];
        if (series.length > 0) {
            const first = series[0].ms, last = series[series.length - 1].ms;
            if (!earliest || first < earliest) earliest = first;
            if (!latest || last > latest) latest = last;
        }
    }
    const { startOfDay, endOfDay } = getPlaybackBoundaries();

    if (earliest) {
        // [V20260319_1650] Ensure chart always starts at midnight of the selected date if data exists
        datasetEarliestTime = startOfDay;
    } else {
        datasetEarliestTime = startOfDay;
    }

    datasetLatestTime = new Date(latest ? Math.max(latest, startOfDay.getTime()) : endOfDay.getTime());
    updateStartTimeUI();
}

function updateStartTimeUI() {
    const input = document.getElementById('startTimeInput'), rangeLabel = document.getElementById('startTimeRangeLabel');
    if (!input || !datasetEarliestTime) return;
    const minStr = datasetEarliestTime.toISOString().substring(11, 19), maxStr = datasetLatestTime.toISOString().substring(11, 19);
    rangeLabel.innerText = `${minStr} -> ${maxStr}`;
    if (!currentStartTime || !isStartTimeCustom) currentStartTime = new Date(datasetEarliestTime.getTime());
    const pad = (n) => String(n).padStart(2, '0');
    const localTimeStr = `${pad(currentStartTime.getHours())}:${pad(currentStartTime.getMinutes())}:${pad(currentStartTime.getSeconds())}`;
    input.value = localTimeStr;
}

function onStartTimeInputChange(e) {
    currentStartTime = new Date(`${document.getElementById('tradeDate').value}T${e.target.value}`);
    isStartTimeCustom = true; updateCharts();
}
function getActiveStartTime() { return currentStartTime || datasetEarliestTime; }

function applyRankSelection() {
    const type = document.getElementById('rankType').value, count = parseInt(document.getElementById('rankCount').value) || 6;
    const metric = document.getElementById('metricSelector').value;
    const rankBy = document.getElementById('rankBy').value;
    const field = rankBy === 'trades' ? 'trade_count' :
        ((metric === 'buy_trades' || metric === 'buy_net') ? 'buy_net' :
            (metric === 'sell_trades' || metric === 'sell_net' ? 'sell_net' : 'net'));

    const startMs = getActiveStartTime().getTime(), evalMs = playbackTime ? playbackTime.getTime() : Date.now();

    const candidates = [];
    for (const key in processedSeries) {
        const series = processedSeries[key];
        let sVal = 0, eVal = 0;
        for (const pt of series) {
            if (pt.ms <= startMs) sVal = pt[field];
            if (pt.ms <= evalMs) eVal = pt[field];
            if (pt.ms > evalMs) break;
        }
        candidates.push({ key: key.replace('|', ' | '), delta: eVal - sVal });
    }
    candidates.sort((a, b) => b.delta - a.delta);
    const filtered = candidates.filter(c => Math.abs(c.delta) > 0); // Hide zeros
    const result = (type === 'top' ? filtered : filtered.reverse()).slice(0, count);

    // Append instead of Replace, with duplicate check
    result.forEach((c, i) => {
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
    // [V20260130_1550] Display as Local Time
    document.getElementById('currentPlaybackTime').innerText = playbackTime.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
    const slider = document.getElementById('timeSlider');
    slider.max = Math.floor((endOfDay - startOfDay) / 1000);
    slider.value = Math.floor((playbackTime - startOfDay) / 1000);
}

async function loadView(name) {
    if (!name) return;
    const viewNameEl = document.getElementById('viewNameInput');
    if (viewNameEl) viewNameEl.value = name;

    // [V20260204_1610] Handle Trade Bucket loading
    if (name.startsWith('BUCKET:')) {
        const bucketName = name.replace('BUCKET:', '');
        // Strategies in bucket are { key, ... }. Map them to activeOverlays group
        const globalMetric = document.getElementById('metricSelector').value || 'net';
        let newOverlays = [];
        let bucketStartTimes = [];

        if (bucketName === 'ALL') {
            // [V20260205_1635] Load ALL strategies from ALL buckets
            loadedBuckets.forEach(b => {
                if (b.start_time) bucketStartTimes.push(b.start_time);
                b.strategies.forEach(s => {
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
            if (bucket.start_time) bucketStartTimes.push(bucket.start_time);
            newOverlays = bucket.strategies.map((s, idx) => ({
                key: s.key,
                group: bucket.name,
                metric: s.metric || globalMetric,
                color: colors[idx % colors.length]
            }));
        }

        // Bucket load should restore a clean captured view, not append to existing overlays.
        activeOverlays = [];
        const seen = new Set();
        newOverlays.forEach(o => {
            const k = `${o.key}|${o.group}|${o.metric || 'net'}`;
            if (seen.has(k)) return;
            seen.add(k);
            if (!o.color) o.color = colors[activeOverlays.length % colors.length];
            activeOverlays.push(o);
        });

        // Do not force chart start to bucket start-time.
        // Bucket creation is shown by marker dots on the existing timeline.
        updateCharts();
        return;
    }

    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}'), v = views[name];
    if (v) {
        // [V20260204_1620] Append presets instead of replace
        const newVOverlays = v.overlays || [];
        newVOverlays.forEach(o => {
            if (!activeOverlays.find(eo => eo.key === o.key && eo.group === o.group)) {
                activeOverlays.push(o);
            }
        });
        // Only set global metric if we're adding to an empty view
        if (activeOverlays.length === newVOverlays.length) {
            document.getElementById('metricSelector').value = v.metric || 'net';
        }
        updateCharts();
    }

}
function saveCurrentView() {
    const name = document.getElementById('viewNameInput').value.trim();
    if (!name) return alert("Enter name");
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
    views[name] = { overlays: activeOverlays, metric: document.getElementById('metricSelector').value };
    localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
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
        const metric = o.metric || globalMetric;
        let baseline = 0, lastVal = 0;

        for (let i = 0; i < series.length; i++) {
            const pt = series[i];
            const val = (metric === 'alt' || metric === 'alt_net_return_sum') ? pt.alt :
                (metric === 'buy' || metric === 'buy_net' || metric === 'buy_net_return_sum') ? (pt.buy_net ?? pt.buy ?? 0) :
                    (metric === 'sell' || metric === 'sell_net' || metric === 'sell_net_return_sum') ? (pt.sell_net ?? pt.sell ?? 0) : (pt.net || 0);
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
    // [V20260308_2137] Append metric to the bucket JSON payload
    const strategiesToSave = overlays.map(o => {
        const metricPart = o.metric ? o.metric : 'net';
        return `${o.key} | ${metricPart}`;
    });
    const mode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';

    fetch('/api/trade_buckets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            name: bucketName,
            strategies: strategiesToSave,
            mode: mode,
            product_type: getSelectedProductType(),
            // Persist true TB creation time (not chart start-time) so markers align correctly.
            start_time: now.toISOString(),
            chart_start_time: getActiveStartTime().toISOString(),
            minimum_difference: 5.0,
            date: (document.getElementById('tradeDate') ? document.getElementById('tradeDate').value : '')
        })
    })
        .then(res => res.json())
        .then(async data => {
        if (data.success) {
            // Refresh bucket presets immediately in dropdown.
            await populateSavedViews();
            const selDate = (document.getElementById('tradeDate') ? document.getElementById('tradeDate').value : '') || '';
            alert(`Trade Bucket "${bucketName}" saved successfully for ${mode.toUpperCase()} ${selDate}. Opening Trade Bucket page now.`);
            const target = `trade_bucket.html?mode=${encodeURIComponent(mode)}&date=${encodeURIComponent(selDate)}&product_type=${encodeURIComponent(getSelectedProductType())}&bucket=${encodeURIComponent(bucketName)}`;
            window.location.href = target;
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
            product_type: getSelectedProductType(),
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
            window.open(`trade_bucket.html?mode=${encodeURIComponent(mode)}&date=${encodeURIComponent(selDate)}&product_type=${encodeURIComponent(getSelectedProductType())}&bucket=${encodeURIComponent(bucketName)}`, '_blank');
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
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
    let removed = 0;
    names.forEach(name => {
        if (Object.prototype.hasOwnProperty.call(views, name)) {
            delete views[name];
            selectedPresetNames.delete(name);
            removed++;
        }
    });
    localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
    populateSavedViews();
    alert(`Removed ${removed} preset(s).`);
}
function deleteWorkflowViews() {
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
    let removed = 0;
    Object.keys(views).forEach(k => {
        if (/^WF_/i.test(k)) {
            delete views[k];
            removed++;
        }
    });
    localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
    activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_'));
    updateCharts();
    populateSavedViews();
    alert(`Removed ${removed} workflow preset(s).`);
}
// [V20260128_2135] Inter-View Transfer Logic
function openTransferModal(groupName) {
    document.getElementById('transferTargetGroup').value = groupName;
    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
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

    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
    if (!views[targetName]) return alert("View not found");

    // 1. Extract card overlays
    const cardOverlays = activeOverlays.filter(o => o.group === groupName);
    if (cardOverlays.length === 0) return alert("Nothing to move");

    // 2. Add to target view
    if (!views[targetName].overlays) views[targetName].overlays = [];
    views[targetName].overlays.push(...cardOverlays);

    // 3. Save target view
    localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));

    // 4. Remove from current view
    activeOverlays = activeOverlays.filter(o => o.group !== groupName);

    // 5. Update UI
    alert(`Moved "${groupName}" to preset "${targetName}"`);
    closeTransferModal();
    updateCharts();
}
async function populateSavedViews() {
    const sel = document.getElementById('loadViewDropdown');
    if (!sel) return;

    const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
    Array.from(selectedPresetNames).forEach(name => {
        if (String(name).startsWith('BUCKET:')) return;
        if (!views[name]) selectedPresetNames.delete(name);
    });
    sel.innerHTML = '<option value="">-- Presets --</option>';

    // 1. Local storage views
    Object.keys(views).forEach(k => {
        const o = document.createElement('option');
        o.value = k;
        o.innerText = k;
        sel.appendChild(o);
    });
    let bucketNames = [];

    // 2. [V20260204_1610] Fetch Trade Buckets for current date/mode
    try {
        const mode = document.getElementById('runMode').value;
        const date = document.getElementById('tradeDate').value;
        const res = await fetch(`/api/trade_buckets?mode=${mode}&date=${date}&${buildProductTypeQuery()}`);
        if (res.ok) {
            const data = await res.json();
            loadedBuckets = data.buckets || [];

            if (loadedBuckets.length > 0) {
                // Separator option
                const sep = document.createElement('option');
                sep.disabled = true;
                sep.innerText = '────── TRADE BUCKETS ──────';
                sel.appendChild(sep);

                // [V20260205_1635] Add "All Buckets" option if multiple exist
                if (loadedBuckets.length > 1) {
                    const allOpt = document.createElement('option');
                    allOpt.value = 'BUCKET:ALL';
                    allOpt.innerText = '📦 ALL TRADE BUCKETS (' + loadedBuckets.length + ')';
                    allOpt.style.fontWeight = '700';
                    allOpt.style.color = 'var(--accent-primary)';
                    sel.appendChild(allOpt);
                }

                loadedBuckets.forEach(b => {
                    const o = document.createElement('option');
                    o.value = 'BUCKET:' + b.name;
                    o.innerText = '📦 ' + b.name; // Use box emoji to distinguish
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

/**
 * [V20260126_1245] Trade Drilldown Logic
 */
let currentDrilldownTrades = [];
let drilldownSortColumn = 0;
let drilldownSortDir = 1;
let lastDrilldownPage = 1;
const DRILLDOWN_PAGE_SIZE = 50;
let filteredDrilldownTrades = [];
const drilldownTradeDetailStore = {};
let drilldownTradeDetailSeq = 0;

function loadMoreDrilldownTrades() {
    lastDrilldownPage++;
    renderDrilldownTable(true);
}
let tradeCache = { mode: null, date: null, trades: [], fetchedAt: 0 }; // [V20260130_1630] Local cache with TTL
const TRADE_CACHE_TTL_MS = 5000;
let loadedBuckets = []; // [V20260204_1610] Global cache for trade buckets

// [V20260128_2300] Improved Trade Drill-down to be more robust and provide feedback
async function showTradeDrilldown(groupName) {
    const listBody = document.getElementById('drilldownTableBody');
    const titleEl = document.getElementById('drilldownTitle');
    const modal = document.getElementById('tradeDrilldownModal');
    const runModeEl = document.getElementById('runMode');
    const tradeDateEl = document.getElementById('tradeDate');

    if (!listBody || !modal || !runModeEl || !tradeDateEl) {
        console.error("Drilldown modal or inputs missing:", { listBody, modal, runModeEl, tradeDateEl });
        return;
    }

    const mode = runModeEl.value;
    const date = tradeDateEl.value;

    // Show loading state
    listBody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding: 20px;">Loading trades for today...</td></tr>';
    currentDrilldownTrades = [];
    lastDrilldownPage = 1;
    const btnLoadMore = document.getElementById('btnLoadMoreDrilldown');
    if (btnLoadMore) btnLoadMore.style.display = 'none';
    const statusEl = document.getElementById('drilldownRenderStatus');
    if (statusEl) statusEl.innerText = '';

    drilldownModelFilter = ''; // Reset on open [V20260205_0955]
    drilldownSignalFilter = 'all'; // [V20260311_1330]

    const signalSelect = document.getElementById('drilldownSignalSelect');
    if (signalSelect) signalSelect.value = 'all';

    const filterGroup = document.getElementById('drilldownFilterGroup');
    if (filterGroup) filterGroup.style.visibility = 'hidden';

    const modelSelect = document.getElementById('drilldownModelSelect');
    if (modelSelect) {
        modelSelect.innerHTML = '<option value="">All Models</option>';
        modelSelect.value = '';
    }

    titleEl.innerText = `Viewing trades for card: ${groupName}`;
    modal.style.display = 'flex';

    // [V20260130_1630] Performance: Use local cache if same date
    let trades = [];
    const nowMs = Date.now();
    const cacheFresh = (nowMs - Number(tradeCache.fetchedAt || 0)) < TRADE_CACHE_TTL_MS;
    if (tradeCache.mode === mode && tradeCache.date === date && tradeCache.trades.length > 0 && cacheFresh) {
        trades = tradeCache.trades;
        console.log(`[Drilldown] Using cached ${trades.length} trades for ${date}`);
    } else {
        try {
            const response = await fetch(`/api/trades?mode=${mode}&date=${date}&${buildProductTypeQuery()}&live_only=false`);
            if (response.ok) {
                const data = await response.json();
                trades = data.trades || [];
                tradeCache = { mode, date, trades, fetchedAt: nowMs }; // Update cache
                console.log(`[Drilldown] Fetched and cached ${trades.length} trades for ${date}`);
            } else {
                listBody.innerHTML = '<tr><td colspan="10" style="text-align:center; color:#f87171;">Error loading trades from API</td></tr>';
                return;
            }
        } catch (err) {
            console.error('Error fetching trades for drill-down:', err);
            listBody.innerHTML = `<tr><td colspan="10" style="text-align:center; color:#f87171;">Fetch Error: ${err.message}</td></tr>`;
            return;
        }
    }

    // Filter trades by the strategies/products in this group
    const overlays = activeOverlays.filter(o => o.group === groupName);
    const axisMaxMs = (playbackTime || datasetLatestTime || new Date()).getTime();

    const globalSeen = new Set();
    overlays.forEach(o => {
        const parts = o.key.includes(' | ') ? o.key.split(' | ') : o.key.split('|');
        const strategyName = String(parts[0] || '').trim();
        const productName = String(parts[1] || '').trim();
        const norm = (v) => String(v || '').trim().toLowerCase();
        const cleanModel = (v) => {
            let s = norm(v);
            // Strip visual prefixes/tags used in labels: [L-TRADE], [T], etc.
            s = s.replace(/^\[[^\]]+\]\s*/g, '');
            s = s.replace(/\s*\[[^\]]+\]\s*$/g, '');
            s = s.replace(/[{}()]/g, '');
            return s;
        };
        const baseModel = (name) => {
            const v = cleanModel(name);
            const m = v.match(/^(.*)_\d+_tp[\d.]+_sl[\d.]+$/);
            return m ? m[1] : v;
        };
        const hasParams = (name) => /_\d+_tp[\d.]+_sl[\d.]+$/i.test(cleanModel(name));
        const expectedModel = cleanModel(strategyName);
        const expectedBase = baseModel(strategyName);
        const expectedHasParams = hasParams(strategyName);
        const expectedProduct = norm(productName).toUpperCase();

        // [V20260130_1650] Consistent local parsing
        const d_act = safeParseDate(o.activated_at);
        const actMs = d_act ? d_act.getTime() : 0;

        let filtered = trades.filter(t => {
            const tModelRaw = cleanModel(t.script_name || t.app_name || '');
            const tBase = baseModel(tModelRaw);
            const tParams = cleanModel(t.strategy || t.strategy_key || '');
            const tModelWithParams = tParams ? `${tBase}_${tParams}` : tBase;
            const stratMatch = expectedHasParams
                ? (tModelRaw === expectedModel || tModelWithParams === expectedModel)
                : (tBase === expectedBase || tModelRaw === expectedBase);
            const prodMatch = String(t.product || '').trim().toUpperCase() === expectedProduct;

            let tradeTime = 0;
            if (t.entry_time) {
                const d_entry = safeParseDate(t.entry_time);
                tradeTime = d_entry ? d_entry.getTime() : 0;
            }
            const timeMatch = isNaN(tradeTime) || tradeTime <= axisMaxMs;

            return stratMatch && prodMatch && timeMatch;
        });

        // Fallback: if strict match yields nothing, keep same product and relaxed strategy base match.
        if (!filtered.length) {
            filtered = trades.filter(t => {
                const tModelRaw = cleanModel(t.script_name || t.app_name || '');
                const tBase = baseModel(tModelRaw);
                const prodMatch = String(t.product || '').trim().toUpperCase() === expectedProduct;
                if (!prodMatch) return false;
                let tradeTime = 0;
                if (t.entry_time) {
                    const d_entry = safeParseDate(t.entry_time);
                    tradeTime = d_entry ? d_entry.getTime() : 0;
                }
                const timeMatch = isNaN(tradeTime) || tradeTime <= axisMaxMs;
                if (!timeMatch) return false;
                return tBase === expectedBase || tModelRaw.startsWith(`${expectedBase}_`) || expectedBase.startsWith(`${tBase}_`);
            });
        }

        filtered.forEach(t => {
            const entryDate = safeParseDate(t.entry_time);
            const exitDate = safeParseDate(t.exit_time);
            const direction = (t.direction || '').toUpperCase();
            const isLive = t.is_live_trade === true || t.live_trade_executed === true || t.order_sent_net === true || t.order_sent_net === 'true';
            const actualModel = String(t.script_name || t.app_name || strategyName).trim();
            const dedupeKey = [
                t.trade_id || '',
                t.entry_time || '',
                t.exit_time || '',
                actualModel,
                String(t.product || '').trim().toUpperCase(),
                t.direction || '',
                t.filename || ''
            ].join('|');
            if (globalSeen.has(dedupeKey)) return;
            globalSeen.add(dedupeKey);

            currentDrilldownTrades.push({
                ms: entryDate ? entryDate.getTime() : 0,
                actMs: actMs,
                t: entryDate ? entryDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) : '-',
                model: actualModel,
                product: String(t.product || productName).trim().toUpperCase(), // Essential for distinguishing session start
                type: direction === 'LONG' || direction === 'BUY' ? 'B' : 'S',
                signal: direction,
                result: t.net_return || 0,
                altNet: t.alt_net || 0,
                total: t.net_return || 0,
                exit: exitDate ? exitDate.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false }) : '-',
                status: t.status || (t.exit_time ? 'CLOSED' : 'OPEN'),
                live: isLive ? 'Yes' : 'No',
                filename: t.filename || t.source_file || ''
            });
        });
    });

    if (currentDrilldownTrades.length === 0) {
        listBody.innerHTML = '<tr><td colspan="10" style="text-align:center; padding: 20px; color: var(--text-dim);">No trades found matching this card\'s filters and current playback time.</td></tr>';
    } else {
        drilldownSortColumn = 0;
        drilldownSortDir = -1; // Descending by time
        sortDrilldownTable(0, true);
    }

    // Populate model filter [V20260205_1005] Professional Select
    populateDrilldownModelFilter(currentDrilldownTrades);
}

function populateDrilldownModelFilter(trades) {
    const modelSelect = document.getElementById('drilldownModelSelect');
    const filterGroup = document.getElementById('drilldownFilterGroup');
    if (!modelSelect || !filterGroup) return;

    const uniqueModels = [...new Set(trades.map(t => t.model))].filter(Boolean).sort();

    if (uniqueModels.length > 1) {
        modelSelect.innerHTML = '<option value="">All Models</option>';
        uniqueModels.forEach(m => {
            const opt = document.createElement('option');
            opt.value = m;
            opt.innerText = m;
            modelSelect.appendChild(opt);
        });
        filterGroup.style.visibility = 'visible';
        // Show model filter only if there's more than one model [V20260311_1330]
        modelSelect.style.display = 'block';
        const modelLabel = modelSelect.previousElementSibling;
        if (modelLabel) modelLabel.style.display = 'block';
    } else {
        // If only 1 model, show it but maybe hide the dropdown?
        // Actually, let's just ALWAYS show the filter group now because Signal filter is there.
        filterGroup.style.visibility = 'visible';
        // Hide model select specifically if only 1 model exists [V20260311_1330]
        modelSelect.style.display = 'none';
        const modelLabel = modelSelect.previousElementSibling;
        if (modelLabel) modelLabel.style.display = 'none';
    }
}

function renderDrilldownTable(append = false) {
    const listBody = document.getElementById('drilldownTableBody');
    const statusEl = document.getElementById('drilldownRenderStatus');
    const btnLoadMore = document.getElementById('btnLoadMoreDrilldown');

    if (!listBody) return;

    if (!append) {
        listBody.innerHTML = '';
        lastDrilldownPage = 1;
        drilldownTradeDetailSeq = 0;

        // Apply Filters
        filteredDrilldownTrades = currentDrilldownTrades.filter(t => {
            // 1. Model Filter
            if (drilldownModelFilter && (t.model || '').toLowerCase() !== drilldownModelFilter) return false;

            // 2. Signal Filter [V20260311_1330]
            if (drilldownSignalFilter && drilldownSignalFilter !== 'all') {
                const sig = (t.signal || '').toLowerCase();
                if (drilldownSignalFilter === 'long' && (sig !== 'long' && sig !== 'buy' && t.type !== 'B')) return false;
                if (drilldownSignalFilter === 'short' && (sig !== 'short' && sig !== 'sell' && t.type !== 'S')) return false;
            }
            return true;
        });
    }

    const trades = filteredDrilldownTrades;
    const startIndex = (lastDrilldownPage - 1) * DRILLDOWN_PAGE_SIZE;
    const endIndex = startIndex + DRILLDOWN_PAGE_SIZE;
    const pageData = trades.slice(startIndex, endIndex);

    if (!append && pageData.length === 0) {
        listBody.innerHTML = '<tr><td colspan="11" style="text-align:center; padding: 20px; color: var(--text-dim);">No trades match current filters.</td></tr>';
        if (statusEl) statusEl.innerText = '0 trades found';
        if (btnLoadMore) btnLoadMore.style.display = 'none';
        return;
    }

    // Find the "First Session Trade" per activation instance (needed for visual markers)
    const modelStarts = {};
    trades.forEach(t => {
        if (t.actMs > 0 && t.ms >= t.actMs) {
            const mKey = `${t.model}|${t.product}|${t.actMs}`;
            if (!modelStarts[mKey] || t.ms < modelStarts[mKey]) {
                modelStarts[mKey] = t.ms;
            }
        }
    });

    const rowsHtml = pageData.map(t => {
        const resCol = t.result > 0 ? '#10b981' : t.result < 0 ? '#ef4444' : '#9ca3af';
        const altResCol = t.altNet > 0 ? '#10b981' : t.altNet < 0 ? '#ef4444' : '#9ca3af';
        const totCol = t.total > 0 ? '#10b981' : t.total < 0 ? '#ef4444' : '#9ca3af';
        const typeCol = t.type === 'B' ? 'var(--accent-primary)' : 'var(--text-dim)';

        const mKey = `${t.model}|${t.product}|${t.actMs}`;
        const isActiveSession = t.actMs > 0 && t.ms >= t.actMs;
        const isStart = isActiveSession && (t.ms === modelStarts[mKey]);

        const detailId = `mc_${++drilldownTradeDetailSeq}`;
        drilldownTradeDetailStore[detailId] = t;

        let rowStyle = "";
        let rowTitle = "";
        if (isStart) {
            rowStyle = "border-left: 4px solid #39ff14; background: rgba(57, 255, 20, 0.15);";
            rowTitle = "Monitoring Started Shortly Before This Trade";
        } else if (isActiveSession) {
            rowStyle = "border-left: 4px solid rgba(57, 255, 20, 0.3); background: rgba(57, 255, 20, 0.05);";
        }

        return `
            <tr style="${rowStyle}" title="${rowTitle}">
                <td>${t.t}</td>
                <td>${t.model}</td>
                <td style="color:${typeCol}; font-weight:800;">${t.type}</td>
                <td style="font-weight:700;">${t.signal}</td>
                <td style="color:${resCol}; font-weight:800;">${currencyFormatter.format(t.result)}</td>
                <td style="color:${altResCol}; font-weight:800;">${currencyFormatter.format(t.altNet)}</td>
                <td style="color:${totCol}; font-weight:800;">${currencyFormatter.format(t.total)}</td>
                <td style="color:var(--text-dim); font-size:0.8rem;">${t.exit}</td>
                <td style="font-size:0.8rem;">${t.status}</td>
                <td style="color:${t.live === 'Yes' ? 'var(--accent-primary)' : 'var(--text-dim)'}; font-weight:700;">${t.live}</td>
                <td><button class="btn btn-secondary" style="padding:3px 8px; font-size:0.75rem;" onclick="showDrilldownTradeDetails('${detailId}')">Details</button></td>
            </tr>
        `;
    }).join('');

    if (append) {
        listBody.insertAdjacentHTML('beforeend', rowsHtml);
    } else {
        listBody.innerHTML = rowsHtml;
    }

    if (statusEl) statusEl.innerText = `Showing ${Math.min(endIndex, trades.length)} of ${trades.length} trades`;
    if (btnLoadMore) btnLoadMore.style.display = endIndex < trades.length ? 'block' : 'none';
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

    const keys = ['ms', 'model', 'type', 'signal', 'result', 'altNet', 'total', 'exit', 'status', 'live'];
    const key = keys[colIdx];

    currentDrilldownTrades.sort((a, b) => {
        let vA = a[key], vB = b[key];
        if (typeof vA === 'string') {
            vA = vA.toLowerCase();
            vB = vB.toLowerCase();
        }
        if (vA < vB) return -1 * drilldownSortDir;
        if (vA > vB) return 1 * drilldownSortDir;
        return 0;
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
            const resp = await fetch(`/api/trade_file?mode=${encodeURIComponent(mode)}&date=${encodeURIComponent(date)}&filename=${encodeURIComponent(filename)}&${buildProductTypeQuery()}`);
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

function peekSummaryImportPayload() {
    const raw = localStorage.getItem('multi_chart_import_payload');
    if (!raw) return null;
    try {
        const payload = JSON.parse(raw);
        if (payload && Array.isArray(payload.items) && payload.items.length > 0) return payload;
    } catch (e) {
        console.warn('Invalid multi_chart import payload', e);
        localStorage.removeItem('multi_chart_import_payload');
    }
    return null;
}

function consumeSummaryImportPayload() {
    const raw = localStorage.getItem('multi_chart_import_payload');
    if (!raw) return { added: 0, groups: [] };
    let payload = null;
    try {
        payload = JSON.parse(raw);
    } catch (e) {
        console.warn('Invalid multi_chart import payload', e);
        localStorage.removeItem('multi_chart_import_payload');
        return { added: 0, groups: [] };
    }
    localStorage.removeItem('multi_chart_import_payload');
    if (!payload || !Array.isArray(payload.items) || payload.items.length === 0) return { added: 0, groups: [] };
    const currentProductType = getCurrentWorkflowImportProductType(payload);
    const isProfileWorkflow = String(payload.source || '') === 'profile_match_workflow';
    const isTopXWorkflow = String(payload.source || '') === 'top_x_multi_chart_workflow';
    const shouldMergeTopXCharts = isTopXWorkflow && Boolean(payload.merge_charts);
    if (isProfileWorkflow) {
        // 1) Replace WF_PROFILE cards on each profile workflow run.
        activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_PROFILE_'));
        // 2) Prune stale WF_PROFILE presets so only current workflow output remains.
        try {
            const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
            Object.keys(views || {}).forEach(name => {
                if (String(name).startsWith('WF_PROFILE_')) delete views[name];
            });
            localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
            populateSavedViews();
        } catch (_) { }
    }
    if (isTopXWorkflow) {
        // 1) Replace WF_TOPX cards on each Top X workflow run.
        activeOverlays = activeOverlays.filter(o => !String(o.group || '').startsWith('WF_TOPX_'));
        // 2) Prune stale WF_TOPX presets so only current workflow output remains.
        try {
            const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
            Object.keys(views || {}).forEach(name => {
                if (String(name).startsWith('WF_TOPX_')) delete views[name];
            });
            localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
            populateSavedViews();
        } catch (_) { }
    }
    function normalizeImportMetric(metricRaw) {
        const raw = String(metricRaw || '').toLowerCase();
        if (['buy', 'buy_net', 'buy_net_return_sum'].includes(raw)) return 'buy_net';
        if (['sell', 'sell_net', 'sell_net_return_sum'].includes(raw)) return 'sell_net';
        if (['alt', 'alt_net', 'alt_net_return_sum'].includes(raw)) return 'alt_net';
        return 'net';
    }

    const preferredMetricRaw = String(payload.preferred_metric || '').toLowerCase();
    let preferredMetric = null;
    if (preferredMetricRaw) preferredMetric = normalizeImportMetric(preferredMetricRaw);
    // [V20260306_1845] buy_sell: per-item metrics drive overlay creation (no global override needed)
    const isBuySellMode = preferredMetricRaw === 'buy_sell';

    const availableKeys = Object.keys(processedSeries);
    const available = new Set(availableKeys);
    const lowerMap = new Map();
    availableKeys.forEach(k => lowerMap.set(k.toLowerCase(), k));

    function normalizeProductVariants(product) {
        const p = String(product || '').toUpperCase();
        const variants = new Set([p]);
        if (p.endsWith('_C') || p.endsWith('_S')) {
            variants.add(p.slice(0, -2));
        } else if (p) {
            variants.add(`${p}_C`);
            variants.add(`${p}_S`);
        }
        return Array.from(variants);
    }

    function resolveLookupKey(item) {
        const strategy = String(item.strategy || '').trim();
        const parmRaw = String(item.parm_raw || '').trim();
        const products = normalizeProductVariants(item.product);
        const strictOnly = Boolean(parmRaw) || /_tp[\d.]+_sl[\d.]+/i.test(strategy);

        // 1) Exact + case-insensitive
        for (const p of products) {
            const k = `${strategy}|${p}`;
            if (available.has(k)) return k;
            const kl = lowerMap.get(k.toLowerCase());
            if (kl) return kl;
        }

        // 2) If params provided, try reconstructed strategy
        const hasEmbeddedParams = /_tp[\d.]+_sl[\d.]+/i.test(strategy);
        if (parmRaw && !hasEmbeddedParams) {
            const rebuilt = `${strategy}_${parmRaw}`;
            for (const p of products) {
                const k = `${rebuilt}|${p}`;
                if (available.has(k)) return k;
                const kl = lowerMap.get(k.toLowerCase());
                if (kl) return kl;
            }
        }

        if (strictOnly) return null;

        // 3) Fuzzy by product + strategy prefix (fallback for legacy loose payloads)
        for (const key of availableKeys) {
            const parts = key.split('|');
            if (parts.length < 2) continue;
            const s = parts[0];
            const p = parts[1].toUpperCase();
            if (!products.includes(p)) continue;
            if (s.toLowerCase() === strategy.toLowerCase()) return key;
            if (parmRaw && s.toLowerCase() === `${strategy}_${parmRaw}`.toLowerCase()) return key;
            if (s.toLowerCase().startsWith((strategy + '_').toLowerCase())) return key;
        }
        return null;
    }
    let added = 0;
    const addedGroups = new Set();
    payload.items.forEach(item => {
        const itemProductType = String(item.product_type || payload.product_type || '').trim().toLowerCase();
        if (itemProductType && itemProductType !== currentProductType) return;
        const strategy = String(item.strategy || '').trim();
        const product = String(item.product || '').trim();
        if (!strategy || !product) return;
        const resolved = resolveLookupKey(item);
        if (!resolved) return;
        const parts = resolved.split('|');
        const finalStrategy = parts[0];
        const finalProduct = parts[1];

        const key = `${finalStrategy} | ${finalProduct}`;
        const group = shouldMergeTopXCharts
            ? String(payload.group || payload.preset_name || 'WF_TOPX_MERGED')
            : String(item.group || key);
        // Always preserve explicit per-item workflow metric when provided.
        let itemMetric = preferredMetric;
        if (item.metric) itemMetric = normalizeImportMetric(item.metric);
        if (!itemMetric && isBuySellMode) return;
        if (isProfileWorkflow || isTopXWorkflow) {
            // Profile/TopX workflows must not create duplicates by strategy/product across groups.
            // [V20260306_1845] For buy_sell, allow same key if metric differs
            const existsAny = activeOverlays.find(o => o.key === key && o.metric === itemMetric);
            if (existsAny) return;
        }
        // [V20260306_1845] Duplicate check now includes metric to allow buy+sell on same key/group
        const exists = activeOverlays.find(o => o.key === key && o.group === group && o.metric === itemMetric);
        if (exists) return;

        activeOverlays.push({
            key: key,
            group: group,
            metric: itemMetric,
            color: colors[activeOverlays.length % colors.length]
        });
        added++;
        addedGroups.add(group);
    });

    if (added > 0) {
        updateCharts();
        console.log(`[MULTI-CHART-IMPORT] Added ${added} chart item(s) from summary payload.`);
    } else {
        // [V20260318_1845] Keep workflow imports silent in the UI and low-noise in the console.
        console.info('[MULTI-CHART-IMPORT] No matching strategies/products found for the imported summary selection.');
    }
    return { added: added, groups: Array.from(addedGroups) };
}

async function consumeWorkflowImportPayload() {
    try {
        const res = await fetch('/api/workflows/multi_chart_payload');
        const data = await res.json();
        if (!data || !data.success || !data.payload || !Array.isArray(data.payload.items) || data.payload.items.length === 0) return;
        const payload = data.payload;
        const currentProductType = getCurrentWorkflowImportProductType(payload);
        const runId = String(payload.run_id || '');
        if (runId) {
            const lastRunId = localStorage.getItem(`multi_chart_workflow_import_run_id_${currentProductType}`) || '';
            if (lastRunId === runId) return;
            localStorage.setItem(`multi_chart_workflow_import_run_id_${currentProductType}`, runId);
        }
        localStorage.setItem('multi_chart_import_payload', JSON.stringify(payload));
        const importResult = consumeSummaryImportPayload() || { added: 0, groups: [] };
        if (importResult.added > 0) {
            const presetName = buildWorkflowImportPresetName(
                String(payload.preset_name || payload.group || payload.run_id || `WF_PROFILE_${new Date().toISOString().slice(0, 10)}`),
                currentProductType
            );
            const groups = new Set(importResult.groups || []);
            const overlaysForPreset = activeOverlays.filter(o => groups.has(o.group));
            if (overlaysForPreset.length > 0) {
                const signature = JSON.stringify(
                    overlaysForPreset
                        .map(o => `${String(o.key || '').trim()}|${String(o.metric || 'global').trim().toLowerCase()}`)
                        .sort()
                );
                const lastSig = localStorage.getItem(`multi_chart_workflow_last_signature_${currentProductType}`) || '';
                if (signature === lastSig) {
                    console.log('[MULTI-CHART-WF-IMPORT] Skipped preset save (identical workflow chart set).');
                    return;
                }
                const views = JSON.parse(localStorage.getItem('pnl_graph_views_multi') || '{}');
                views[presetName] = {
                    overlays: overlaysForPreset,
                    metric: document.getElementById('metricSelector') ? document.getElementById('metricSelector').value : 'net'
                };
                localStorage.setItem('pnl_graph_views_multi', JSON.stringify(views));
                localStorage.setItem(`multi_chart_workflow_last_signature_${currentProductType}`, signature);
                populateSavedViews();
                console.log(`[MULTI-CHART-WF-IMPORT] Auto-saved preset '${presetName}' with ${overlaysForPreset.length} overlays.`);
            }
        }
    } catch (e) {
        console.warn('[MULTI-CHART-WF-IMPORT] Failed:', e);
    }
}

function getDisplaySignal(baseSignal, metric) {
    if (metric === 'alt' || metric === 'alt_net_return_sum') {
        return baseSignal === 'BUY' ? 'SELL' : 'BUY';
    }
    return baseSignal;
}

const closeDrilldownModalBtn = document.getElementById('closeTradeDrilldownModal');
if (closeDrilldownModalBtn) closeDrilldownModalBtn.onclick = closeDrilldownModal;

async function initMultiChart() {
    initEventHandlers();
    try {
        const cfgResp = await fetch('/api/config');
        const cfgJson = await cfgResp.json();
        populateProductTypeSelect(cfgJson.config || cfgJson);
    } catch (e) {
        populateProductTypeSelect({ product_type: 'forex', product_types: ['forex'] });
    }
    const pendingImport = peekSummaryImportPayload();
    if (pendingImport) {
        if (pendingImport.mode && document.getElementById('runMode')) {
            document.getElementById('runMode').value = String(pendingImport.mode).toLowerCase();
        }
        if (pendingImport.date && document.getElementById('tradeDate')) {
            document.getElementById('tradeDate').value = pendingImport.date;
        }
    }
    await fetchData();
    initAutoRefresh(); // [V20260128_1900] Move interval start out of fetchData to prevent it dying on error
    populateSavedViews();
    consumeSummaryImportPayload();
    await consumeWorkflowImportPayload();
    setInterval(consumeWorkflowImportPayload, 15000);
    if (nonLivePruneInterval) clearInterval(nonLivePruneInterval);
    runNegativeNonLiveCardPruneWorkflow();
    nonLivePruneInterval = setInterval(runNegativeNonLiveCardPruneWorkflow, 60000);
}
initMultiChart();

// [V20260130_1635] Restore Sticky History on Load
const initialMode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';
if (liveMonitor.setMode) liveMonitor.setMode(initialMode);
liveMonitor.loadState(buildGroupMap());

function exportDrilldownToCSV() {
    if (!currentDrilldownTrades || currentDrilldownTrades.length === 0) {
        alert("No trades to export.");
        return;
    }

    const headers = ['Time', 'Model', 'Product', 'Type', 'Signal', 'Result', 'Alt Net', 'Total', 'Exit', 'Status', 'Live'];
    const rows = currentDrilldownTrades.map(t => [
        t.t,
        t.model,
        t.product,
        t.type,
        t.signal,
        t.result,
        t.altNet,
        t.total,
        t.exit,
        t.status,
        t.live
    ]);

    let csvContent = "data:text/csv;charset=utf-8,"
        + headers.join(",") + "\n"
        + rows.map(r => r.map(val => `"${val}"`).join(",")).join("\n");

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    const date = document.getElementById('tradeDate').value;
    const groupName = document.getElementById('modalTargetGroup') ? document.getElementById('modalTargetGroup').value : 'trades';

    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `breakout_trades_${groupName}_${date}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// [V20260131_0428] System Health Loop
function updateSystemHealth() {
    const mode = document.getElementById('runMode') ? document.getElementById('runMode').value : 'live';
    const statusEl = document.getElementById('healthStatus');
    const modeEl = document.getElementById('healthModeIndicator');
    const latEl = document.getElementById('healthLatency');

    if (!statusEl) return;

    fetch(`/api/system_health?mode=${mode}`)
        .then(res => res.json())
        .then(data => {
            if (data.healthy) {
                statusEl.innerText = "HEALTHY";
                statusEl.style.background = mode === 'sim' ? "rgba(6, 182, 212, 0.2)" : "rgba(57, 255, 20, 0.2)";
                statusEl.style.color = mode === 'sim' ? "#06b6d4" : "#39ff14";
                statusEl.style.boxShadow = mode === 'sim' ? "0 0 10px rgba(6, 182, 212, 0.1)" : "0 0 10px rgba(57, 255, 20, 0.1)";
            } else {
                statusEl.innerText = "ATTENTION";
                statusEl.style.background = "rgba(244, 63, 94, 0.2)";
                statusEl.style.color = "var(--rose)";
                statusEl.style.boxShadow = "none";
            }

            modeEl.innerText = `Mode: ${mode.toUpperCase()}`;

            // Checks details: trade_files, price_feed, trade_recency
            const checks = data.checks || {};
            const feedLat = checks.feed_latency_sec >= 0 ? `${checks.feed_latency_sec}s` : 'ERR';
            latEl.innerText = `Feed: ${feedLat}`;
        })
        .catch(err => {
            statusEl.innerText = "OFFLINE";
            statusEl.style.background = "rgba(255, 255, 255, 0.1)";
            statusEl.style.color = "var(--text-dim)";
        });
}

// [V20260205_1400] Robust Batch Creation Functions
function openBatchCreator() {
    const products = new Set(), strategies = new Set(), tps = new Set(), sls = new Set(), sizes = new Set();

    // Primary Source: rawData.strategies
    const sourceData = rawData.strategies || {};

    // Fallback Source: processedSeries keys (if rawData is empty or not yet synced)
    if (Object.keys(sourceData).length === 0 && Object.keys(processedSeries).length > 0) {
        console.log("[BATCH] rawData.strategies empty, falling back to processedSeries keys");
        Object.keys(processedSeries).forEach(key => {
            const [s, p] = key.split('|');
            if (!sourceData[s]) sourceData[s] = {};
            sourceData[s][p] = true;
        });
    }

    if (Object.keys(sourceData).length === 0) {
        alert("No trade data available to generate batches. Please wait for initial data load.");
        return;
    }

    for (const [stratName, prodMap] of Object.entries(sourceData)) {
        // Extraction logic for Base Strategy: everything before {size}_tp
        // Non-greedy .+? ensures we stop at the FIRST digit followed by _tp [V20260205_1400]
        const baseMatch = stratName.match(/^(.+?)_(\d+)_tp([\d.]+)_sl([\d.]+)/);
        if (baseMatch) {
            strategies.add(baseMatch[1]); // e.g., 'breakout_R_Rev'
            sizes.add(baseMatch[2]);      // e.g., '2'
            tps.add(parseFloat(baseMatch[3]));
            sls.add(parseFloat(baseMatch[4]));
        } else {
            // Fallback for strategies without _N_tpX_slY format
            strategies.add(stratName.split('_')[0]);
        }
        // Always extract products
        Object.keys(prodMap).forEach(p => products.add(p));
    }

    // Populate Checkbox Groups
    populateCheckboxGroup('batchProductCheckboxes', Array.from(products).sort());
    populateCheckboxGroup('batchStrategyCheckboxes', Array.from(strategies).sort());
    populateCheckboxGroup('batchSizeCheckboxes', Array.from(sizes).sort((a, b) => a - b));
    populateCheckboxGroup('batchTpCheckboxes', Array.from(tps).sort((a, b) => a - b));
    populateCheckboxGroup('batchSlCheckboxes', Array.from(sls).sort((a, b) => a - b));

    // Add listeners for ALL batch checkboxes
    ['batchProductCheckboxes', 'batchStrategyCheckboxes', 'batchSizeCheckboxes', 'batchTpCheckboxes', 'batchSlCheckboxes'].forEach(id => {
        const container = document.getElementById(id);
        if (container) {
            container.querySelectorAll('input[type="checkbox"]').forEach(cb => {
                cb.onchange = updateBatchPreview;
            });
        }
    });

    updateBatchPreview();
    document.getElementById('batchCreateModal').style.display = 'flex';
}

function populateCheckboxGroup(id, options) {
    const container = document.getElementById(id);
    if (!container) return;
    container.innerHTML = '';
    options.forEach(opt => {
        const label = document.createElement('label');
        label.style.display = 'flex';
        label.style.alignItems = 'center';
        label.style.gap = '5px';
        label.style.fontSize = '0.75rem';
        label.style.cursor = 'pointer';

        const cb = document.createElement('input');
        cb.type = 'checkbox';
        cb.value = opt;
        // cb.onchange will be set after all checkboxes are created in openBatchCreator

        label.appendChild(cb);
        label.appendChild(document.createTextNode(opt));
        container.appendChild(label);
    });
}

function toggleCheckboxes(containerId, state) {
    if (containerId === 'batchCreateModal' && state === false) {
        // Full Clear
        ['batchProductCheckboxes', 'batchStrategyCheckboxes', 'batchSizeCheckboxes', 'batchTpCheckboxes', 'batchSlCheckboxes'].forEach(id => {
            const container = document.getElementById(id);
            if (container) container.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = false);
        });
    } else {
        const container = document.getElementById(containerId);
        if (container) container.querySelectorAll('input[type="checkbox"]').forEach(cb => cb.checked = state);
    }
    updateBatchPreview();
}

function populateMultiSelect(id, options) {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = '';
    options.forEach(opt => {
        const o = document.createElement('option');
        o.value = opt;
        o.innerText = opt;
        sel.appendChild(o);
    });
}

function selectAllOptions(id) {
    const sel = document.getElementById(id);
    if (!sel) return;
    for (let i = 0; i < sel.options.length; i++) sel.options[i].selected = true;
    updateBatchPreview();
}

function clearAllOptions(id) {
    const sel = document.getElementById(id);
    if (!sel) return;
    for (let i = 0; i < sel.options.length; i++) sel.options[i].selected = false;
    updateBatchPreview();
}

function updateBatchPreview() {
    const prods = getCheckedValues('batchProductCheckboxes');
    const strats = getCheckedValues('batchStrategyCheckboxes');

    // Get checkbox values
    const sizes = getCheckedValues('batchSizeCheckboxes');
    const tps = getCheckedValues('batchTpCheckboxes');
    const sls = getCheckedValues('batchSlCheckboxes');

    document.getElementById('productSelectCount').innerText = `${prods.length} selected`;
    document.getElementById('strategySelectCount').innerText = `${strats.length} selected`;

    // Param combos are strats * sizes * tps * sls
    const comboCount = sizes.length * tps.length * sls.length;
    document.getElementById('paramSelectCount').innerText = `${comboCount} combinations`;

    const total = prods.length * strats.length * comboCount;
    const previewEl = document.getElementById('batchTotalPreview');
    previewEl.innerText = total;

    const warningEl = document.getElementById('batchWarning');
    const generateBtn = document.getElementById('generateBatchBtn');

    if (total > 100) {
        warningEl.style.display = 'block';
        previewEl.style.color = 'var(--rose)';
        generateBtn.disabled = true;
        generateBtn.style.opacity = '0.5';
    } else {
        warningEl.style.display = 'none';
        previewEl.style.color = 'var(--accent-primary)';
        generateBtn.disabled = total === 0;
        generateBtn.style.opacity = total === 0 ? '0.5' : '1';
    }
}

function getCheckedValues(id) {
    const container = document.getElementById(id);
    if (!container) return [];
    return Array.from(container.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
}

function getSelectedOptions(id) {
    const sel = document.getElementById(id);
    if (!sel) return [];
    return Array.from(sel.selectedOptions).map(o => o.value);
}

function generateBatchCharts() {
    const prods = getCheckedValues('batchProductCheckboxes');
    const strats = getCheckedValues('batchStrategyCheckboxes');
    const sizes = getCheckedValues('batchSizeCheckboxes');
    const tps = getCheckedValues('batchTpCheckboxes');
    const sls = getCheckedValues('batchSlCheckboxes');
    const metric = document.getElementById('batchMetricSelector').value;
    const normalizedMetric = (metric === 'global' || metric === 'net') ? null : metric;

    if (prods.length === 0 || strats.length === 0 || sizes.length === 0 || tps.length === 0 || sls.length === 0) {
        alert("Please ensure at least one selection from each field (Products, Strategies, Size, TP, SL).");
        return;
    }

    // Generate Candidate Models
    const candidates = [];
    strats.forEach(strat => {
        sizes.forEach(size => {
            tps.forEach(tp => {
                sls.forEach(sl => {
                    // Normalize decimals to match key format (e.g., 10 -> 10.0)
                    const tpStr = parseFloat(tp).toFixed(1);
                    const slStr = parseFloat(sl).toFixed(1);
                    const modelName = `${strat}_${size}_tp${tpStr}_sl${slStr}`;
                    candidates.push(modelName);
                });
            });
        });
    });

    // Check against 100 limit
    const totalToAdd = prods.length * candidates.length;
    const totalExistingGroups = new Set(activeOverlays.map(o => o.group)).size;
    if (totalToAdd + totalExistingGroups > 100) {
        alert(`Adding ${totalToAdd} charts would exceed the 100 card limit.`);
        return;
    }

    let addedCount = 0;
    prods.forEach(p => {
        candidates.forEach(m => {
            // Check if this model actually exists in rawData
            const lookupKey = `${m}|${p}`;
            if (!processedSeries[lookupKey]) {
                // If it doesn't exist, we skip to avoid empty charts
                return;
            }

            const key = `${m} | ${p}`;
            const exists = activeOverlays.find(o => o.key === key && o.group === key && o.metric === normalizedMetric);
            if (!exists) {
                activeOverlays.push({
                    key: key,
                    group: key,
                    metric: normalizedMetric,
                    color: colors[activeOverlays.length % colors.length]
                });
                addedCount++;
            }
        });
    });

    if (addedCount === 0) {
        alert("No new valid chart combinations were found among your selections.");
    } else {
        updateCharts();
        document.getElementById('batchCreateModal').style.display = 'none';
    }
}

// Initial call and interval
setTimeout(updateSystemHealth, 1000);
setInterval(updateSystemHealth, 30000);

// Listen to incoming chart additions from Strategy Performance / Top 20
if (typeof BroadcastChannel !== 'undefined') {
    const mcChannel = new BroadcastChannel('multi_chart_channel');
    mcChannel.onmessage = (e) => {
        if (e.data === 'PING') {
            mcChannel.postMessage('PONG');
        } else if (e.data === 'IMPORT') {
            console.log("[MULTI-CHART] Cross-tab import triggered");
            consumeSummaryImportPayload();
        }
    };
}
