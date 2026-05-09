
        // Existing JS content ...
        const MAX_VIEW_ROWS = 300; // [V20260208_1700] Increased limit
        let currentData = [];
        let summaryData = null; // [V20260115_1020] Store summary net data
        let rawTrades = []; // Unprocessed trades for time filtering
        let sortCol = -1;
        let sortAsc = true;
        let refreshInterval = null;
        let top20RefreshInterval = null;
        let top20FullData = [];

        /** [V20260108_0030] Primary table CSV export */
        function exportTableToCSV() {
            if (!currentData || currentData.length === 0) {
                alert("No data displayed to export.");
                return;
            }

            // Get current filters
            const search = document.getElementById('searchInput').value.toLowerCase();
            const minNet = parseFloat(document.getElementById('netFilterInput').value) || -999999;
            const minBuy = parseInt(document.getElementById('minBuyTradesInput').value) || 0;
            const minSell = parseInt(document.getElementById('minSellTradesInput').value) || 0;

            // Apply same filter as UI
            const filtered = currentData.filter(d => {
                const matchesSearch = d.product.toLowerCase().includes(search) || d.strategy.toLowerCase().includes(search) || d.params.toLowerCase().includes(search);
                const matchesNet = d.total_net >= minNet;
                const matchesBuy = d.buy_count >= minBuy;
                const matchesSell = d.sell_count >= minSell;
                return matchesSearch && matchesNet && matchesBuy && matchesSell;
            });

            if (filtered.length === 0) {
                alert("No records match current filters.");
                return;
            }

            const headers = [
                "Product", "Strategy", "Parameters", "Total Net", "#Trades",
                "#Buy", "Buy Net", "Alt Buy", "#Sell", "Sell Net", "Alt Sell",
                "Live Buy", "Live Sell", "Auto Buy", "Auto Sell"
            ];

            const rows = filtered.map(d => [
                d.product, d.strategy, d.params, d.total_net, d.trade_count,
                d.buy_count, d.buy_net, d.buy_alt, d.sell_count, d.sell_net, d.sell_alt,
                d.live_buy_qty, d.live_sell_qty, d.auto_buy ? "ON" : "OFF", d.auto_sell ? "ON" : "OFF"
            ]);

            const csvContent = [
                headers.join(","),
                ...rows.map(r => r.map(val => `"${val}"`).join(","))
            ].join("\n");

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            const date = document.getElementById('statsDate').value;
            const filename = `performance_summary_${date}.csv`;

            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Time playback variables
        let playbackInterval = null;
        let playbackSpeed = 1;
        let minTime = null;
        let maxTime = null;
        let currentFilterTime = null;
        let currentDrillDownTrades = []; // Store trades for export
        let currentDrillDownTitle = "Trades"; // Store title for filename

        // [V20251230_2315] Activations state for Auto Buy/Sell buttons
        let activations = {};
        let referredSource = 'ui'; // [V20260206_2040]
        let scalperRatio = 5; // [V20260207_2210] Default fallback

        async function init() {
            // [V20260206_2040] Handle query parameters
            const urlParams = new URLSearchParams(window.location.search);
            const searchParam = urlParams.get('search');
            if (searchParam) document.getElementById('searchInput').value = searchParam;
            referredSource = urlParams.get('from') || 'ui';

            const dateParam = urlParams.get('date');
            if (dateParam && /^\d{4}-\d{2}-\d{2}$/.test(dateParam)) {
                document.getElementById('statsDate').value = dateParam;
            } else {
                // Set today's date default
                const today = new Date().toISOString().split('T')[0];
                document.getElementById('statsDate').value = today;

                // Load available dates fallback
                try {
                    const mode = document.getElementById('runMode').value;
                    const response = await fetch(`/api/dates?mode=${mode}`);
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    const data = await response.json();
                    if (data.success && data.dates && data.dates.length > 0) {
                        const validDate = data.dates.find(d => /^\d{4}-\d{2}-\d{2}$/.test(d));
                        if (validDate) document.getElementById('statsDate').value = validDate;
                    }
                } catch (err) {
                    console.error("Error loading dates:", err);
                }
            }
            // [V20260207_2210] Also fetch config for scalper_ratio
            try {
                const cfgResp = await fetch('/api/config');
                const cfgData = await cfgResp.json();
                if (cfgData.success && cfgData.config && cfgData.config.scalper_ratio) {
                    scalperRatio = parseFloat(cfgData.config.scalper_ratio);
                }
            } catch (ce) { }

            await loadActivations(); // [V20251230_2315] Load activations for Auto Buy/Sell

            // Ensure valid date
            if (!document.getElementById('statsDate').value) {
                document.getElementById('statsDate').value = new Date().toISOString().split('T')[0];
            }

            await loadStats();
            document.getElementById('autoRefreshCheck').addEventListener('change', startAutoRefresh);
            startAutoRefresh();
        }

        // [V20251230_2336] Load activations from API for current mode
        async function loadActivations() {
            try {
                const mode = document.getElementById('runMode').value; // Get current mode
                const response = await fetch(`/api/activations?mode=${mode}`);
                if (response.ok) {
                    const data = await response.json();
                    if (data.success) {
                        activations = data.activations || {};
                        refreshAllAutoButtons();
                    }
                }
            } catch (err) {
                console.error('Error loading activations:', err);
            }
        }

        function refreshAllAutoButtons() {
            document.querySelectorAll('.auto-toggle-btn').forEach(button => applyAutoButtonState(button));
        }

        function applyAutoButtonState(button) {
            const strategy = button.dataset.strategy;
            const parm = button.dataset.parm;
            const product = button.dataset.product;
            const direction = button.dataset.direction;
            if (!strategy || !parm || !product || !direction) return;

            const active = isAutoActive(strategy, parm, product, direction);
            button.classList.toggle('active', active);
            button.textContent = getActivationLabel(strategy, parm, product, direction);
        }

        // [V20260206_1445] Build activation key - Normalize to buy/sell
        function buildActivationKey(strategy, parm, direction) {
            let dir = direction.toLowerCase();
            if (dir === 'long') dir = 'buy';
            if (dir === 'short') dir = 'sell';
            return `${strategy}_${parm}_${dir}_net`;
        }

        // [V20251230_2315] Check if auto activation is active for strategy/product/direction
        function isAutoActive(strategy, parm, product, direction) {
            // [V20260208_1710] Check both exact directional and unified keys
            const key = buildActivationKey(strategy, parm, direction);
            const unifiedKey = `${strategy}_${parm}_net`; // Check if "Both" is active

            const entry = activations[key] || activations[unifiedKey];
            if (!entry || !entry.active) return false;
            return entry.products?.includes(product.toUpperCase()) || false;
        }

        // [V20260101_2130] Get label (A/M/OFF) for auto activation
        function getActivationLabel(strategy, parm, product, direction) {
            const key = buildActivationKey(strategy, parm, direction);
            const unifiedKey = `${strategy}_${parm}_net`;
            const entry = activations[key] || activations[unifiedKey];
            if (!entry || !entry.active || !entry.products?.includes(product.toUpperCase())) return 'OFF';
            return entry.manual ? 'M' : 'A';
        }

        // [V20251230_2336] Toggle auto activation for a strategy/product/direction
        async function toggleAutoActivation(strategy, parm, product, direction, button) {
            const mode = document.getElementById('runMode').value; // Get current mode
            console.log(`[AUTO-TOGGLE] Mode: ${mode}, Strategy: ${strategy}, Product: ${product}, Direction: ${direction}`);

            const isCurrentlyActive = isAutoActive(strategy, parm, product, direction);
            const metric = direction.toLowerCase() === 'sell' || direction.toLowerCase() === 'short' ? 'sell_net' : 'buy_net';
            const modelName = parm ? `${strategy}_${parm}` : strategy;
            const group = product;

            try {
                const gridResp = await fetch(`/api/grid_live?mode=${mode}`);
                const gridJson = gridResp.ok ? await gridResp.json() : { data: [] };
                const gridItems = Array.isArray(gridJson.data) ? gridJson.data : [];

                const groupItems = gridItems.filter(item => item.group === group);
                let models = groupItems.map(item => ({
                    model: item.model,
                    product: item.product,
                    metric: item.metric || 'net',
                    source: item.source,
                    manual: item.manual
                }));

                const matchIndex = models.findIndex(m => m.model === modelName && m.product === product && (m.metric || 'net') === metric);
                if (matchIndex > -1) {
                    models.splice(matchIndex, 1);
                } else {
                    models.push({
                        model: modelName,
                        product: product,
                        metric: metric,
                        source: 'strategy_performance',
                        manual: true
                    });
                }

                const payload = {
                    group: group,
                    models: models,
                    mode: mode,
                    source: 'strategy_performance'
                };

                console.log('[AUTO-TOGGLE] Grid payload:', JSON.stringify(payload, null, 2));

                const response = await fetch('/api/grid_live', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    await loadActivations();
                    if (button) applyAutoButtonState(button);
                    refreshAllAutoButtons();

                    // [V20260127_1610] Promote existing open trades to L-trades
                    if (!isCurrentlyActive) {  // Only promote when activating (not deactivating)
                        const date = document.getElementById('statsDate').value;
                        console.log('[PROMOTE] Calling promotion for existing trades...');

                        const promoteResponse = await fetch('/api/promote_trades', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                mode: mode,
                                strategy: strategy,
                                product: product,
                                direction: direction,
                                parm: parm,
                                date: date
                            })
                        });

                        if (promoteResponse.ok) {
                            const promoteData = await promoteResponse.json();
                            console.log('[PROMOTE] Result:', promoteData);
                            if (promoteData.promoted > 0) {
                                console.log(`[PROMOTE] ✓ Promoted ${promoteData.promoted} trade(s) to live status`);
                            } else {
                                console.log('[PROMOTE] No matching open trades found to promote');
                            }
                        } else {
                            console.error('[PROMOTE] Promotion failed:', await promoteResponse.text());
                        }
                    }
                }
            } catch (err) {
                console.error('Error toggling activation:', err);
            }
        }

        // [V20251230_2336] Handle run mode change - reload both stats and activations
        async function handleModeChange() {
            await loadActivations();  // Reload activations for new mode
            await loadStats();         // Reload stats for new mode
        }

        function handleViewLimitChange() {
            loadStats();
        }

        function startAutoRefresh() {
            if (refreshInterval) clearInterval(refreshInterval);

            const todayStr = new Date().toISOString().split('T')[0];
            const dateInput = document.getElementById('statsDate').value;
            const autoChecked = document.getElementById('autoRefreshCheck').checked;

            if (dateInput === todayStr && !playbackInterval && autoChecked) {
                document.getElementById('liveBadge').style.display = 'inline-block';
                refreshInterval = setInterval(() => loadStats(true), 15000);
            } else {
                document.getElementById('liveBadge').style.display = 'none';
            }
        }

        async function loadStats(isBackground = false) {
            const mode = document.getElementById('runMode').value;
            let date = document.getElementById('statsDate').value;
            const loading = document.getElementById('loading');
            const tbody = document.getElementById('statsBody');
            const viewLimitVal = (document.getElementById('viewLimitSelect')?.value || 'top').toLowerCase();
            const keys = ['product', 'strategy', 'parm', 'total_net', 'trade_count', 'buy_count', 'buy_net', 'buy_alt', 'sell_count', 'sell_net', 'sell_alt', 'live_buy', 'live_sell'];

            let limit = 300;
            let sort_key = 'total_net';
            let sort_dir = viewLimitVal === 'bottom' ? 'asc' : 'desc';

            // If user clicked a column header, prioritize that sort
            const activeKey = sortCol !== -1 ? keys[sortCol] : sort_key;
            const finalSortDir = sortCol !== -1 ? (sortAsc ? 'asc' : 'desc') : sort_dir;

            // [V20260130_1255] Refresh activations in the background 
            // This ensures Grid-Live promotions show up as 'A' without a full page reload
            loadActivations();

            if (!date) {
                date = new Date().toISOString().split('T')[0];
                document.getElementById('statsDate').value = date;
            }

            if (!isBackground) {
                loading.style.display = 'block';
                tbody.innerHTML = '';
            }

            try {
                // [V20260208_1700] Use dynamic limit and directional params
                const response = await fetch(`/api/stats_summary?mode=${mode}&date=${date}&limit=${limit}&view=${encodeURIComponent(viewLimitVal)}&sort_key=${encodeURIComponent(activeKey)}&sort_dir=${encodeURIComponent(finalSortDir)}`);
                if (!response.ok) throw new Error(`Stats API HTTP ${response.status}`);

                const data = await response.json();

                if (data.success) {
                    // [V20260121_1633] Map database keys to UI expectations
                    // [V20260121_2015] Fixed parm mapping - ensure parm_raw and parm are safe
                    currentData = data.data.map(d => ({
                        ...d,
                        strategy: d.strategy || '',
                        params: d.params || '',
                        parm: d.params ? `{${d.params}}` : '-',
                        parm_raw: d.params || '',
                        full_name: (d.strategy || '') + (d.params ? `_${d.params}` : ''), // [V20260207_2100] Keep for searching
                        buy_pct: d.buyPercent || 0,
                        sell_pct: d.sellPercent || 0,
                        buy_alt: d.buy_alt || 0,   // [V20260204_0450]
                        sell_alt: d.sell_alt || 0, // [V20260204_0450]
                        live_buy: d.live_buy_net || 0,
                        live_sell: d.live_sell_net || 0,
                        // [V20260208_1505] Robust combined search blob
                        search_blob: `${d.product || ''} ${d.strategy || ''} ${d.params || ''} ${(d.strategy || '')}_${(d.params || '')}`.toLowerCase()
                    }));

                    const lastUpdateEl = document.getElementById('lastUpdateTs');
                    if (lastUpdateEl) {
                        const ts = data.last_update || data.lastUpdate || data.updated_at;
                        if (ts) {
                            const parsed = new Date(ts);
                            lastUpdateEl.textContent = `Last update: ${isNaN(parsed.getTime()) ? ts : parsed.toLocaleString()}`;
                        } else {
                            lastUpdateEl.textContent = `Last update: ${new Date().toLocaleString()}`;
                        }
                    }

                    applySortIndicators();
                    filterTable();

                    if (!isBackground) {
                        startAutoRefresh();
                        loadSummaryHistory(); // [V20260206_1200] Load history for playback
                    }
                } else if (!isBackground) {
                    tbody.innerHTML = `<tr><td colspan="15" style="text-align:center;">${data.message}</td></tr>`;
                }
            } catch (err) {
                console.error('Fetch error:', err);
                if (!isBackground) tbody.innerHTML = `<tr><td colspan="15" style="text-align:center; color:red;">Connection Error (${err.message})</td></tr>`;
            } finally {
                if (!isBackground) loading.style.display = 'none';
            }
        }


        function processTrades(trades) {
            const stats = {};
            trades.forEach(t => {
                const product = t.product || 'UNKNOWN';
                const key = `${product}|${t.app_name}|${t.strategy}`;
                if (!stats[key]) {
                    stats[key] = {
                        product: product,
                        strategy: t.app_name,
                        parm: `{${t.strategy}}`,
                        parm_raw: t.strategy,
                        total_net: 0,
                        trade_count: 0, // [V20251230_2315] Total trade count
                        buy_count: 0,
                        buy_net: 0,
                        buy_pct: 0,
                        buy_alt: 0, // [V20260204_0450]
                        sell_count: 0,
                        sell_net: 0,
                        sell_pct: 0,
                        sell_alt: 0, // [V20260204_0450]
                        live_buy: 0,
                        live_sell: 0
                    };
                }

                const s = stats[key];
                const direction = (t.direction || 'UNKNOWN').toUpperCase();
                const isLive = t.order_sent_net === true || t.order_sent_net === 'true';

                if (direction === 'LONG' || direction === 'BUY') {
                    s.buy_count++;
                    const netVal = parseFloat(t.net_return || 0);
                    const altVal = parseFloat(t.alt_net_return || 0);
                    s.buy_net += netVal;
                    s.buy_alt += altVal;
                    s.total_net += netVal;
                    if (isLive) s.live_buy += netVal;
                } else if (direction === 'SHORT' || direction === 'SELL') {
                    s.sell_count++;
                    const netVal = parseFloat(t.net_return || 0);
                    const altVal = parseFloat(t.alt_net_return || 0);
                    s.sell_net += netVal;
                    s.sell_alt += altVal;
                    s.total_net += netVal;
                    if (isLive) s.live_sell += netVal;
                }
            });

            // [V20260115_1020] Enrich with percentage data from summary_net
            Object.values(stats).forEach(s => {
                s.trade_count = s.buy_count + s.sell_count;

                if (summaryData && summaryData.strategies) {
                    // Look up strategy/product in summary data
                    // Structure: summaryData.strategies[strategy][product] -> array of entries
                    let stratData = summaryData.strategies[s.strategy];

                    // [V20260115_1045] Fallback: Try stripping product suffix from strategy name
                    if (!stratData && s.product && s.strategy.endsWith('_' + s.product)) {
                        const cleanKey = s.strategy.substring(0, s.strategy.length - s.product.length - 1);
                        stratData = summaryData.strategies[cleanKey];
                    }

                    if (stratData) {
                        const prodData = stratData[s.product];
                        if (prodData && Array.isArray(prodData) && prodData.length > 0) {
                            // Get last entry
                            const lastEntry = prodData[prodData.length - 1];
                            s.buy_pct = lastEntry.buyPercent || 0;
                            s.sell_pct = lastEntry.sellPercent || 0;
                        }
                    }
                }
            });

            currentData = Object.values(stats);

            // Re-apply sort if one was active
            if (sortCol !== -1) {
                // [V20251230_2315] Updated numeric column indices for new columns
                const isNumeric = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12].includes(sortCol);
                doSort(sortCol, isNumeric, false, true); // false = don't toggle direction, true = local sort
            }

            filterTable(); // This will handle rendering and search persistence
        }

        function renderTable(data) {
            const tbody = document.getElementById('statsBody');
            tbody.innerHTML = '';

            if (!data || data.length === 0) return;

            // [V20260206_1415] Metrics for relative heat-mapping
            const maxTrades = Math.max(...data.map(d => d.trade_count), 1);
            const maxBuy = Math.max(...data.map(d => d.buy_count), 1);
            const maxSell = Math.max(...data.map(d => d.sell_count), 1);

            // [V20260210_1320] Dominant Side based on Average Net per Trade (UI Screen Approach)
            const totalBuyNet = data.reduce((sum, d) => sum + (d.buy_net || 0), 0);
            const totalBuyCount = data.reduce((sum, d) => sum + (d.buy_count || 0), 0);
            const totalSellNet = data.reduce((sum, d) => sum + (d.sell_net || 0), 0);
            const totalSellCount = data.reduce((sum, d) => sum + (d.sell_count || 0), 0);

            const avgBuyNet = totalBuyCount > 0 ? (totalBuyNet / totalBuyCount) : -Infinity;
            const avgSellNet = totalSellCount > 0 ? (totalSellNet / totalSellCount) : -Infinity;

            const buyIsDominant = avgBuyNet >= avgSellNet;
            console.log(`[BIAS-UI] Avg Buy Net: ${avgBuyNet.toFixed(2)}, Avg Sell Net: ${avgSellNet.toFixed(2)}, Dominant: ${buyIsDominant ? 'BUY' : 'SELL'}`);

            data.forEach(s => {
                const isAutoBuyActive = isAutoActive(s.strategy, s.parm_raw, s.product, 'buy');
                const isAutoSellActive = isAutoActive(s.strategy, s.parm_raw, s.product, 'sell');

                const tr = document.createElement('tr');

                // #Trades Bar Config (Brighter green, row brightness mapped)
                const tradePct = (s.trade_count / maxTrades) * 100;
                const tradeBrightness = 0.5 + (s.trade_count / maxTrades) * 1.5; // Up to 2.0x brightness

                // #Buy / #Sell Bar Config
                const buyPct = (s.buy_count / maxBuy) * 100;
                const sellPct = (s.sell_count / maxSell) * 100;

                // Column colors based on dominance
                const buyBaseAlpha = buyIsDominant ? 0.45 : 0.08;
                const sellBaseAlpha = !buyIsDominant ? 0.45 : 0.08;

                // Row brightness factors within col
                const buyRowBrightness = 0.8 + (s.buy_count / maxBuy) * 1.2;
                const sellRowBrightness = 0.8 + (s.sell_count / maxSell) * 1.2;

                // [V20260207_2150] Highlight parm if tp:sl ratio is at least 1:5
                let parmStyle = "";
                const tpMatch = s.parm_raw.match(/tp([\d.]+)/);
                const slMatch = s.parm_raw.match(/sl([\d.]+)/);
                if (tpMatch && slMatch) {
                    const tpVal = parseFloat(tpMatch[1]);
                    const slVal = parseFloat(slMatch[1]);
                    if (tpVal > 0 && slVal >= tpVal * scalperRatio) {
                        parmStyle = `color: #fbbf24; font-weight: 800; text-shadow: 0 0 8px rgba(251, 191, 36, 0.3);`;
                    }
                }

                // [V20260210_0520] Highlight Winner Take All (Highest Average Net)
                const avgBuyNet = s.buy_count > 0 ? (s.buy_net / s.buy_count) : -Infinity;
                const avgSellNet = s.sell_count > 0 ? (s.sell_net / s.sell_count) : -Infinity;
                let buyNetStyle = "";
                let sellNetStyle = "";
                // Neon Green / Fluorescent Style
                const highlightStyle = "color: #39ff14; font-weight: 900; text-shadow: 0 0 8px rgba(57, 255, 20, 0.6); border-bottom: 2px solid rgba(57, 255, 20, 0.4);";

                if (s.buy_count > 0 || s.sell_count > 0) {
                    if (avgBuyNet > -Infinity || avgSellNet > -Infinity) {
                        if (avgBuyNet > avgSellNet) {
                            buyNetStyle = highlightStyle;
                        } else if (avgSellNet > avgBuyNet) {
                            sellNetStyle = highlightStyle;
                        }
                    }
                }

                tr.innerHTML = `
                    <td class="text-mono" style="color:#fbbf24">${s.product}</td>
                    <td class="text-mono" style="color:#667eea">${s.strategy}</td>
                    <td class="text-mono" style="${parmStyle}">${s.parm}</td>
                    <td class="text-mono clickable ${getValueClass(s.total_net)}" style="font-weight: 700; background: rgba(255, 255, 255, 0.05);" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'all')">${s.total_net.toFixed(2)}</td>
                    <td class="text-mono clickable trade-count-cell" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'all')">
                        <div class="trade-bar-bg bar-trades" style="width: ${tradePct}%; filter: brightness(${tradeBrightness})"></div>
                        ${s.trade_count}
                    </td>
                    <td class="text-mono clickable trade-count-cell" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'buy')">
                        <div class="trade-bar-bg bar-buy-sell" style="width: ${buyPct}%; 
                            --bar-color-main: rgba(16, 185, 129, ${buyBaseAlpha}); 
                            --bar-color-dim: rgba(16, 185, 129, ${buyBaseAlpha * 0.2}); 
                            --bar-color-edge: rgba(16, 185, 129, ${buyBaseAlpha * 1.5});
                            filter: brightness(${buyRowBrightness})"></div>
                        ${s.buy_count}
                    </td>
                    <td class="text-mono clickable ${getValueClass(s.buy_net)}" style="${buyNetStyle}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'buy')">${s.buy_net.toFixed(2)}</td>
                    <td class="text-mono clickable ${(s.buy_alt || 0) >= 0 ? 'positive' : 'negative'}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'buy')">${(s.buy_alt || 0).toFixed(2)}</td>
                    <td class="text-mono clickable trade-count-cell" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'sell')">
                        <div class="trade-bar-bg bar-buy-sell" style="width: ${sellPct}%; 
                            --bar-color-main: rgba(16, 185, 129, ${sellBaseAlpha}); 
                            --bar-color-dim: rgba(16, 185, 129, ${sellBaseAlpha * 0.2}); 
                            --bar-color-edge: rgba(16, 185, 129, ${sellBaseAlpha * 1.5});
                            filter: brightness(${sellRowBrightness})"></div>
                        ${s.sell_count}
                    </td>
                    <td class="text-mono clickable ${getValueClass(s.sell_net)}" style="${sellNetStyle}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'sell')">${s.sell_net.toFixed(2)}</td>
                    <td class="text-mono clickable ${(s.sell_alt || 0) >= 0 ? 'positive' : 'negative'}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'sell')">${(s.sell_alt || 0).toFixed(2)}</td>
                    <td class="text-mono clickable ${getValueClass(s.live_buy)}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'buy', true)">${s.live_buy ? s.live_buy.toFixed(2) : '-'}</td>
                    <td class="text-mono clickable ${getValueClass(s.live_sell)}" onclick="showDrillDown('${s.product}', '${s.strategy}', '${s.parm_raw}', 'sell', true)">${s.live_sell ? s.live_sell.toFixed(2) : '-'}</td>
                    <td><button class="auto-toggle-btn ${isAutoBuyActive ? 'active' : ''}"
                            data-strategy="${s.strategy}"
                            data-parm="${s.parm_raw}"
                            data-product="${s.product}"
                            data-direction="buy">${getActivationLabel(s.strategy, s.parm_raw, s.product, 'buy')}</button></td>
                    <td><button class="auto-toggle-btn ${isAutoSellActive ? 'active' : ''}"
                            data-strategy="${s.strategy}"
                            data-parm="${s.parm_raw}"
                            data-product="${s.product}"
                            data-direction="sell">${getActivationLabel(s.strategy, s.parm_raw, s.product, 'sell')}</button></td>
                `;
                tbody.appendChild(tr);
            });
        }


        function getValueClass(val) {
            if (val > 0) return 'positive';
            if (val < 0) return 'negative';
            return 'neutral';
        }

        function filterTable() {
            const query = document.getElementById('searchInput').value.toLowerCase();
            const minNetStr = document.getElementById('netFilterInput').value;
            const minBuyStr = document.getElementById('minBuyTradesInput').value;
            const minSellStr = document.getElementById('minSellTradesInput').value;

            // [V20260207_2345] Cross-column multi-part matching
            // If query is "breakout_R_Rev_2_tp10.0", it splits into parts 
            // and ensures all parts exist in (product | strategy | parm)
            const queryParts = query.trim().split(/[_\s]+/).filter(p => p.length > 0);

            const minNetVal = parseFloat(minNetStr);
            const minBuyVal = parseInt(minBuyStr);
            const minSellVal = parseInt(minSellStr);

            const filtered = currentData.filter(d => {
                let matchesSearch = true;
                if (queryParts.length > 0) {
                    matchesSearch = queryParts.every(part => d.search_blob.includes(part));
                }

                const matchesNet = isNaN(minNetVal) || d.total_net > minNetVal;
                const matchesBuy = isNaN(minBuyVal) || d.buy_count >= minBuyVal;
                const matchesSell = isNaN(minSellVal) || d.sell_count >= minSellVal;

                return matchesSearch && matchesNet && matchesBuy && matchesSell;
            });

            // [V20260210_0245] Update summary modal if it is currently open (Auto-Refresh)
            const summaryModal = document.getElementById('summaryModal');
            if (summaryModal && summaryModal.style.display === 'block') {
                renderSummaryGrid(filtered);
            }

            renderTable(filtered.slice(0, MAX_VIEW_ROWS));
        }

        function sortTab(n, isNumeric = false) {
            doSort(n, isNumeric, true); // true = toggle direction
        }

        function doSort(n, isNumeric, toggle, skipFetch = false) {
            // [V20260204_0450] Updated keys array for new Alt columns
            if (toggle) {
                if (sortCol === n) sortAsc = !sortAsc;
                else { sortCol = n; sortAsc = true; }
            }

            applySortIndicators(n);

            if (!skipFetch) {
                loadStats();
                return;
            }

            const keys = ['product', 'strategy', 'parm', 'total_net', 'trade_count', 'buy_count', 'buy_net', 'buy_alt', 'sell_count', 'sell_net', 'sell_alt', 'live_buy', 'live_sell'];
            const key = keys[n];
            const ths = document.querySelectorAll('th');
            ths.forEach((th, idx) => {
                th.classList.remove('asc', 'desc');
                if (idx === n) th.classList.add(sortAsc ? 'asc' : 'desc');
            });

            currentData.sort((a, b) => {
                let v1 = a[key], v2 = b[key];
                if (isNumeric) { v1 = parseFloat(v1) || 0; v2 = parseFloat(v2) || 0; }
                else { v1 = String(v1).toLowerCase(); v2 = String(v2).toLowerCase(); }
                if (v1 < v2) return sortAsc ? -1 : 1;
                if (v1 > v2) return sortAsc ? 1 : -1;
                return 0;
            });

            filterTable();
        }

        function applySortIndicators(forceIndex = null) {
            const ths = document.querySelectorAll('th');
            ths.forEach((th, idx) => {
                th.classList.remove('asc', 'desc');
                if (sortCol !== -1 && idx === sortCol) {
                    th.classList.add(sortAsc ? 'asc' : 'desc');
                } else if (forceIndex !== null && idx === forceIndex) {
                    th.classList.add(sortAsc ? 'asc' : 'desc');
                }
            });
        }

        // ========== DRILL-DOWN LOGIC ==========
        // [V20260121_1700] Updated to fetch trades on-demand and use correct DB column names
        async function showDrillDown(product, appName, strategy, direction, onlyLive = false) {
            const modal = document.getElementById('tradeModal');
            const modalTitle = document.getElementById('modalTitle');
            const modalBody = document.getElementById('modalBody');

            // Show loading state
            modalTitle.textContent = `Loading ${product} - ${appName} trades...`;
            modalBody.innerHTML = '<div class="loading">Loading trades...</div>';
            modal.style.display = 'block';

            // Fetch trades from API on demand
            const mode = document.getElementById('runMode').value;
            const date = document.getElementById('statsDate').value;
            let trades = [];

            try {
                // [V20260128_0415] Optimization: Pass filters to backend to reduce payload size
                const cleanParams = (strategy || '').replace(/[()]/g, ''); // Remove parens if present
                const response = await fetch(`/api/trades?mode=${mode}&date=${date}&live_only=${onlyLive}&product=${encodeURIComponent(product)}&strategy=${encodeURIComponent(appName)}&params=${encodeURIComponent(cleanParams)}`);

                if (!response.ok) {
                    throw new Error(`API returned ${response.status}: ${response.statusText}`);
                }

                const data = await response.json();
                if (data.success === false) {
                    throw new Error(data.message || 'Server reported failure');
                }
                trades = data.trades || [];
            } catch (err) {
                console.error('Error fetching trades for drill-down:', err);
                modalBody.innerHTML = `<div style="padding: 30px; text-align: center; color: var(--negative);">
                    <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 15px; display: block;"></i>
                    <strong>Error loading trades</strong><br>
                    <span style="font-size: 0.9rem; opacity: 0.8;">${err.message}</span>
                </div>`;
                modal.style.display = 'block';
                return;
            }

            // [V20260129_1653] Strict filtering in drill-down
            const filtered = trades.filter(t => {
                const tProd = (t.product || 'UNKNOWN').toUpperCase();
                const fProd = product.toUpperCase();
                // [V20260210_1145] Allow 'all' products for leaderboard drill-down
                const pMatch = product === 'all' || tProd === fProd;

                // Match app_name
                const tAppName = t.script_name || t.app_name || '';
                const aMatch = !appName || appName === 'all' || tAppName === appName || tAppName.startsWith(`${appName}_`);

                // Match strategy (params)
                const tStrategy = t.strategy_key || t.strategy || '';
                // [V20260205_2200] Robust match: Check tStrategy OR check if it's contained within tAppName
                const sMatch = strategy === 'all' || tStrategy === strategy || (!tStrategy && tAppName.includes(strategy));

                const dir = (t.direction || '').toUpperCase();

                let dMatch = false;
                if (direction === 'all') {
                    dMatch = true;
                } else if (direction === 'buy') {
                    dMatch = (dir === 'LONG' || dir === 'BUY');
                } else {
                    dMatch = (dir === 'SHORT' || dir === 'SELL');
                }

                // [V20260129_1653] Restore time filtering
                const entryVal = t.entry_time ? new Date(t.entry_time).getTime() : 0;
                const timeMatch = currentFilterTime ? entryVal <= currentFilterTime : true;

                // [V20260205_2210] Robust live match (checks is_live from index OR order_sent_net)
                const isL = t.is_live === true || t.is_live === 'true' || t.order_sent_net === true || t.order_sent_net === 'true' || t.is_live_trade === true;
                const liveMatch = onlyLive ? isL : true;

                return pMatch && aMatch && sMatch && dMatch && timeMatch && liveMatch;
            });

            console.log(`[DRILLDOWN] Found ${trades.length} raw trades, ${filtered.length} after filter.`, {
                filter: { product, appName, strategy, direction, onlyLive },
                first_trade: trades.length > 0 ? {
                    product: trades[0].product,
                    script_name: trades[0].script_name,
                    app_name: trades[0].app_name,
                    strategy: trades[0].strategy,
                    strategy_key: trades[0].strategy_key
                } : null
            });

            // [V20251230_1435] Sort trades descending by Entry Time
            filtered.sort((a, b) => new Date(b.entry_time) - new Date(a.entry_time));

            // Store for export
            currentDrillDownTrades = filtered;
            currentDrillDownTitle = `${product}_${appName}_${strategy}_${direction}${onlyLive ? '_live' : ''}`;
            document.getElementById('exportCsvBtn').style.display = 'inline-block';

            modalTitle.textContent = `${product} - ${appName} [${strategy}] - ${direction === 'all' ? 'All' : direction.toUpperCase()} Trades`;

            populateDrilldownSelect(filtered);
            renderDrillDownTable();
            modal.style.display = 'block';
        }

        function populateDrilldownSelect(trades) {
            const select = document.getElementById('drilldownModelSelect');
            const group = document.getElementById('drilldownFilterGroup');
            if (!select || !group) return;

            // Reset first
            select.innerHTML = '<option value="">All Strategies</option>';
            select.value = '';
            group.style.visibility = 'hidden';

            const strategies = [...new Set(trades.map(t => t.script_name || t.app_name || '-'))].sort();

            if (strategies.length > 1) {
                select.innerHTML = '<option value="">All Strategies</option>';
                strategies.forEach(s => {
                    const opt = document.createElement('option');
                    opt.value = s;
                    opt.innerText = s;
                    select.appendChild(opt);
                });
                group.style.visibility = 'visible';
            } else {
                group.style.visibility = 'hidden';
            }
        }

        function renderDrillDownTable() {
            const modalBody = document.getElementById('modalBody');
            const trades = currentDrillDownTrades || [];
            const filterVal = document.getElementById('drilldownModelSelect').value;

            const filtered = trades.filter(t => {
                if (!filterVal) return true;
                const strat = t.script_name || t.app_name || '';
                return strat === filterVal;
            });

            let tableHTML = `
                <table class="trades-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Entry Time</th>
                            <th>Exit Time</th>
                            <th>Direction</th>
                            <th>Status</th>
                            <th>Entry</th>
                            <th>Exit Price</th>
                            <th>Net P&L</th>
                            <th>Alt Net</th>
                            <th>Live</th>
                            <th>JSON</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            filtered.forEach(t => {
                const netClass = (t.net_return || 0) >= 0 ? 'positive' : 'negative';
                const altClass = (t.alt_net || 0) >= 0 ? 'positive' : 'negative';
                // [V20260205_2210] Robust live check for table display
                const isLive = t.is_live === true || t.is_live === 'true' || t.order_sent_net === true || t.order_sent_net === 'true' || t.is_live_trade === true;
                const tradeId = t.trade_id || '-';
                const filename = t.filename || '';
                const jsonButton = filename ? `<button class="json-link-btn" onclick="viewTradeJson('${filename}', '${tradeId}')">View JSON</button>` : '-';

                const formatExitTime = (isoStr) => {
                    if (!isoStr) return '-';
                    const d = new Date(isoStr);
                    if (isNaN(d.getTime())) return '-';
                    return d.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
                };

                const tradeDir = (t.direction || '').toUpperCase();
                const dirColor = (tradeDir === 'LONG' || tradeDir === 'BUY') ? '#4ade80' : '#f87171';

                tableHTML += `
                    <tr>
                        <td>${tradeId}</td>
                        <td class="text-mono" style="font-size: 0.8rem;">${t.entry_time ? new Date(t.entry_time).toLocaleString() : '-'}</td>
                        <td class="text-mono" style="color: #fbbf24; font-size: 0.8rem;">${formatExitTime(t.exit_time)}</td>
                        <td style="color: ${dirColor}; font-weight: 700;">${t.direction || '-'}</td>
                        <td style="color: ${t.status === 'OPEN' ? '#fbbf24' : '#a0a0a0'}">${t.status || 'CLOSED'}</td>
                        <td class="text-mono">${t.entry_price ? t.entry_price.toFixed(5) : '-'}</td>
                        <td class="text-mono">${t.exit_price ? t.exit_price.toFixed(5) : '-'}</td>
                        <td class="text-mono ${netClass}" style="font-weight: 700;">$${(t.net_return || 0).toFixed(2)}</td>
                        <td class="text-mono ${altClass}" style="font-weight: 700;">$${(t.alt_net || 0).toFixed(2)}</td>
                        <td class="live-indicator ${isLive ? 'live-active' : ''}">
                            ${isLive ? '<span title="Live Order Sent" style="color: #fbbf24; font-weight: bold; font-size: 0.7rem;">⚡ LIVE</span>' : '-'}
                        </td>
                        <td>${jsonButton}</td>
                    </tr>
                `;
            });

            if (filtered.length === 0) {
                tableHTML += '<tr><td colspan="11" style="text-align:center; padding: 30px; color: var(--text-dim);">No trades found matching filter.</td></tr>';
            }

            tableHTML += '</tbody></table>';
            modalBody.innerHTML = tableHTML;
        }

        function closeModal() {
            document.getElementById('tradeModal').style.display = 'none';
        }

        // [V20260122_FS] Updated to use filename for database-backed API
        async function viewTradeJson(filename, displayId) {
            if (!filename) {
                alert('No filename available for this entry.');
                return;
            }

            const mode = document.getElementById('runMode').value;
            const date = document.getElementById('statsDate').value;
            const modal = document.getElementById('jsonModal');
            const titleEl = document.getElementById('jsonModalTitle');
            const bodyEl = document.getElementById('jsonModalBody');

            titleEl.textContent = `Loading trade ${displayId || filename}...`;
            bodyEl.textContent = 'Fetching trade data...';
            modal.style.display = 'flex';

            try {
                // [V20260122_FS] Use filename parameter
                const resp = await fetch(`/api/trade_file?mode=${mode}&filename=${encodeURIComponent(filename)}&date=${date}`);
                if (!resp.ok) {
                    throw new Error(`HTTP ${resp.status}`);
                }

                const data = await resp.json();
                if (!data.success) {
                    throw new Error(data.message || 'Failed to load trade data');
                }

                titleEl.textContent = `Trade ${displayId || filename} (${mode.toUpperCase()} ${date})`;
                bodyEl.textContent = JSON.stringify(data.content, null, 2);
            } catch (err) {
                console.error('Error fetching trade data:', err);
                titleEl.textContent = 'Unable to load trade data';
                bodyEl.textContent = err.message || 'Unknown error';
            }
        }

        function closeJsonModal() {
            const modal = document.getElementById('jsonModal');
            if (modal) {
                modal.style.display = 'none';
            }
        }

        function exportDrillDownToCSV() {
            if (!currentDrillDownTrades || currentDrillDownTrades.length === 0) {
                alert("No trades to export.");
                return;
            }

            const headers = [
                "Trade ID", "Product", "Strategy", "Direction", "Status",
                "Entry Time", "Exit Time", "Entry Price", "Exit Price",
                "Net P&L", "Alt Net", "Is Live"
            ];

            const rows = currentDrillDownTrades.map(t => [
                t.trade_id || "",
                t.product || "",
                t.app_name || "",
                t.direction || "",
                t.status || "CLOSED",
                t.entry_time || "",
                t.exit_time || "",
                t.entry_price || "",
                t.exit_price || "",
                t.net_return || "0",
                t.alt_net || "0",
                (t.order_sent_net === true || t.order_sent_net === 'true') ? "YES" : "NO"
            ]);

            const csvContent = [
                headers.join(","),
                ...rows.map(r => r.map(val => `"${val}"`).join(","))
            ].join("\n");

            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            const url = URL.createObjectURL(blob);
            const date = document.getElementById('statsDate').value;
            const filename = `stats_drilldown_${currentDrillDownTitle}_${date}.csv`.replace(/[\s{}|]+/g, '_').toLowerCase();

            link.setAttribute("href", url);
            link.setAttribute("download", filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        window.onclick = function (event) {
            const modal = document.getElementById('tradeModal');
            if (event.target === modal) closeModal();
        }

        // ========== TIME PLAYBACK SYSTEM [V20260206_1215] ==========
        let snapshotData = null; // Snapshot data from _summary_net.json

        async function loadSummaryHistory() {
            const mode = document.getElementById('runMode').value;
            const date = document.getElementById('statsDate').value;
            const url = `/api/trade_file?mode=${mode}&date=${date}&filename=_summary_net.json&_t=${Date.now()}`;

            try {
                const res = await fetch(url);
                const json = await res.json();
                if (json.success && json.content && json.content.strategies) {
                    snapshotData = json.content.strategies;
                    console.log("[PLAYBACK] Summary history loaded:", Object.keys(snapshotData).length, "strategies");
                    initializeTimePlayback();
                } else {
                    document.getElementById('playbackPanel').style.display = 'none';
                }
            } catch (e) {
                console.warn("Failed to load summary history for playback:", e);
                document.getElementById('playbackPanel').style.display = 'none';
            }
        }

        function initializeTimePlayback() {
            if (!snapshotData) return;

            let earliest = Infinity;
            let latest = -Infinity;

            // Find time bounds across all snapshot series
            Object.values(snapshotData).forEach(prodMap => {
                Object.values(prodMap).forEach(series => {
                    if (series && series.length > 0) {
                        const first = new Date(series[0].t).getTime();
                        const last = new Date(series[series.length - 1].t).getTime();
                        if (first < earliest) earliest = first;
                        if (last > latest) latest = last;
                    }
                });
            });

            if (earliest === Infinity) {
                document.getElementById('playbackPanel').style.display = 'none';
                return;
            }

            minTime = earliest;
            maxTime = latest;
            currentFilterTime = maxTime;

            const slider = document.getElementById('timeSlider');
            slider.min = minTime;
            slider.max = maxTime;
            slider.value = maxTime;

            document.getElementById('startTimeLabel').textContent = formatTime(new Date(minTime));
            document.getElementById('endTimeLabel').textContent = formatTime(new Date(maxTime));
            document.getElementById('currentPlaybackTime').textContent = formatTime(new Date(maxTime));
            document.getElementById('playbackPanel').style.display = 'block';
        }

        function onSliderInput() {
            const val = parseInt(document.getElementById('timeSlider').value);
            currentFilterTime = val;
            document.getElementById('currentPlaybackTime').textContent = formatTime(new Date(val));
            updateStatsPlayback();
        }

        function onSliderChange() {
            if (!playbackInterval) updateStatsPlayback();
        }

        function updateStatsPlayback() {
            if (!snapshotData || !currentData || currentData.length === 0) return;

            const targetMs = currentFilterTime;

            // [V20260206_1215] Robust Mapping:
            // summary_net.json uses full_strategy_key (e.g., breakout_2_tp10.0_sl10.0)
            // currentData uses d.strategy (app_name) and d.params (params).
            const playbackMappedData = currentData.map(d => {
                const prod = d.product;
                const appName = d.strategy;
                const params = d.parm_raw || d.params || '';

                // Attempt exact match with appName (if it's already full)
                let points = (snapshotData[appName] && snapshotData[appName][prod]) ? snapshotData[appName][prod] : null;

                // Attempt combined match: appName_params
                if (!points && params) {
                    const combinedKey = `${appName}_${params}`;
                    points = (snapshotData[combinedKey] && snapshotData[combinedKey][prod]) ? snapshotData[combinedKey][prod] : null;
                }

                // Fallback for suffix-stripped strategies
                if (!points && prod && appName.endsWith('_' + prod)) {
                    const cleanKey = appName.substring(0, appName.length - prod.length - 1);
                    points = (snapshotData[cleanKey] && snapshotData[cleanKey][prod]) ? snapshotData[cleanKey][prod] : null;
                }

                if (!points || points.length === 0) return d;

                // Final point search
                let bestPoint = null;
                for (let i = 0; i < points.length; i++) {
                    const ptTime = new Date(points[i].t).getTime();
                    if (ptTime <= targetMs) {
                        bestPoint = points[i];
                    } else {
                        break;
                    }
                }

                if (!bestPoint) {
                    // Start of day state (zeroed)
                    return { ...d, total_net: 0, buy_net: 0, sell_net: 0, buy_alt: 0, sell_alt: 0, live_buy: 0, live_sell: 0, buy_count: 0, sell_count: 0, trade_count: 0, buy_pct: 0, sell_pct: 0 };
                }

                return {
                    ...d,
                    total_net: bestPoint.net || 0,
                    buy_net: bestPoint.buy_net || 0,
                    sell_net: bestPoint.sell_net || 0,
                    buy_alt: bestPoint.buy_alt || 0,
                    sell_alt: bestPoint.sell_alt || 0,
                    live_buy: bestPoint.live_buy || 0,
                    live_sell: bestPoint.live_sell || 0,
                    buy_count: bestPoint.b_c || 0,
                    sell_count: bestPoint.s_c || 0,
                    trade_count: (bestPoint.b_c || 0) + (bestPoint.s_c || 0),
                    buy_pct: bestPoint.buyPercent || 0,
                    sell_pct: bestPoint.sellPercent || 0
                };
            });

            // [V20260206_1230] RE-APPLY SORTING during playback
            if (sortCol !== -1) {
                const keys = ['product', 'strategy', 'parm', 'total_net', 'trade_count', 'buy_count', 'buy_net', 'buy_alt', 'sell_count', 'sell_net', 'sell_alt', 'live_buy', 'live_sell'];
                const key = keys[sortCol];
                const isNumeric = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12].includes(sortCol);

                playbackMappedData.sort((a, b) => {
                    let v1 = a[key], v2 = b[key];
                    if (isNumeric) { v1 = parseFloat(v1) || 0; v2 = parseFloat(v2) || 0; }
                    else { v1 = String(v1).toLowerCase(); v2 = String(v2).toLowerCase(); }
                    if (v1 < v2) return sortAsc ? -1 : 1;
                    if (v1 > v2) return sortAsc ? 1 : -1;
                    return 0;
                });
            }

            // [V20260206_1230] RE-APPLY FILTERS during playback
            const query = document.getElementById('searchInput').value.toLowerCase();
            const minNetVal = parseFloat(document.getElementById('netFilterInput').value);
            const minBuyVal = parseInt(document.getElementById('minBuyTradesInput').value);
            const minSellVal = parseInt(document.getElementById('minSellTradesInput').value);

            const filtered = playbackMappedData.filter(d => {
                const matchesSearch = (d.product || "").toLowerCase().includes(query) ||
                    (d.strategy || "").toLowerCase().includes(query) ||
                    (d.parm || "").toLowerCase().includes(query);

                const matchesNet = isNaN(minNetVal) || d.total_net >= minNetVal;
                const matchesBuy = isNaN(minBuyVal) || d.buy_count >= minBuyVal;
                const matchesSell = isNaN(minSellVal) || d.sell_count >= minSellVal;

                return matchesSearch && matchesNet && matchesBuy && matchesSell;
            });

            renderTable(filtered.slice(0, MAX_VIEW_ROWS));
        }


        function togglePlayback() {
            const btn = document.getElementById('playbackPlay');
            const icon = btn.querySelector('i');
            const span = btn.querySelector('span');

            if (playbackInterval) {
                stopPlayback();
            } else {
                if (currentFilterTime >= maxTime) {
                    currentFilterTime = minTime;
                    document.getElementById('timeSlider').value = minTime;
                }
                if (span) span.textContent = 'Pause';
                if (icon) icon.className = 'fas fa-pause';
                btn.classList.add('active');

                // Disable auto-refresh during playback
                if (refreshInterval) clearInterval(refreshInterval);
                document.getElementById('liveBadge').style.display = 'none';

                let lastTick = Date.now();
                playbackInterval = setInterval(() => {
                    const now = Date.now();
                    const delta = now - lastTick;
                    lastTick = now;

                    currentFilterTime += delta * playbackSpeed; // 1x = real-time

                    if (currentFilterTime >= maxTime) {
                        currentFilterTime = maxTime;
                        stopPlayback();
                    }

                    document.getElementById('timeSlider').value = currentFilterTime;
                    document.getElementById('currentPlaybackTime').textContent = formatTime(new Date(currentFilterTime));
                    updateStatsPlayback();
                }, 100);
            }
        }

        function stopPlayback() {
            if (playbackInterval) {
                clearInterval(playbackInterval);
                playbackInterval = null;
            }
            const btn = document.getElementById('playbackPlay');
            if (btn) {
                const icon = btn.querySelector('i');
                const span = btn.querySelector('span');
                if (span) span.textContent = 'Play';
                if (icon) icon.className = 'fas fa-play';
                btn.classList.remove('active');
            }
            startAutoRefresh();
        }

        function resetPlayback() {
            stopPlayback();
            currentFilterTime = minTime;
            document.getElementById('timeSlider').value = minTime;
            document.getElementById('currentPlaybackTime').textContent = formatTime(new Date(minTime));
            updateStatsPlayback();
        }

        function jumpToEnd() {
            stopPlayback();
            currentFilterTime = maxTime;
            document.getElementById('timeSlider').value = maxTime;
            document.getElementById('currentPlaybackTime').textContent = formatTime(new Date(maxTime));
            updateStatsPlayback();
        }

        function updateSpeedUI() {
            document.getElementById('playbackSpeedLabel').textContent = `${playbackSpeed}x SPEED`;
        }

        function increaseSpeed() {
            const speeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000];
            const idx = speeds.indexOf(playbackSpeed);
            if (idx < speeds.length - 1) {
                playbackSpeed = speeds[idx + 1];
                updateSpeedUI();
            }
        }

        function decreaseSpeed() {
            const speeds = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000];
            const idx = speeds.indexOf(playbackSpeed);
            if (idx > 0) {
                playbackSpeed = speeds[idx - 1];
                updateSpeedUI();
            }
        }


        function formatTime(date) {
            return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false });
        }


        window.addEventListener('click', (event) => {
            if (event.target && event.target.id === 'jsonModal') {
                closeJsonModal();
            }
        });

        // [V20260127_1040] Event delegation for auto-toggle buttons
        document.addEventListener('click', function (event) {
            console.log('[CLICK] Target:', event.target.tagName, event.target.className);
            if (event.target.classList.contains('auto-toggle-btn')) {
                console.log('[AUTO-BTN] Button clicked!');
                const button = event.target;
                const strategy = button.dataset.strategy;
                const parm = button.dataset.parm;
                const product = button.dataset.product;
                const direction = button.dataset.direction;
                console.log('[AUTO-BTN] Data:', { strategy, parm, product, direction });

                if (strategy && parm && product && direction) {
                    console.log('[AUTO-BTN] Calling toggleAutoActivation...');
                    toggleAutoActivation(strategy, parm, product, direction, button);
                } else {
                    console.error('[AUTO-BTN] Missing data attributes!');
                }
            }
        });

        // [V20260205_1900] Top 20 Leaderboard Functions
        async function openTop20() {
            const modal = document.getElementById('top20Modal');
            modal.style.display = 'flex';
            await loadTop20();

            // [V20260205_1955] Auto-refresh Top 20
            if (top20RefreshInterval) clearInterval(top20RefreshInterval);
            top20RefreshInterval = setInterval(loadTop20, 5000);
        }

        function closeTop20() {
            document.getElementById('top20Modal').style.display = 'none';
            if (top20RefreshInterval) {
                clearInterval(top20RefreshInterval);
                top20RefreshInterval = null;
            }
        }

        async function loadTop20() {
            const mode = document.getElementById('runMode').value;
            const date = document.getElementById('statsDate').value;
            const tbody = document.getElementById('top20TableBody');

            // Only show loader on first call OR if table is empty
            if (tbody.innerHTML === '' || tbody.innerHTML.includes('fa-spinner')) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 40px; color: #fbbf24;"><i class="fas fa-spinner fa-spin"></i> Calculating Leaderboard...</td></tr>';
            }

            try {
                const res = await fetch(`/api/top20?mode=${mode}&date=${date}`);
                const data = await res.json();
                if (data.success) {
                    top20FullData = data.top20 || [];

                    // Update Model Select if it's currently empty (or has only "All Models")
                    const modelSelect = document.getElementById('top20ModelSelect');
                    if (modelSelect.options.length <= 1) {
                        const models = [...new Set(top20FullData.map(item => item.strategy))];
                        models.sort();
                        models.forEach(m => {
                            const opt = document.createElement('option');
                            opt.value = m;
                            opt.textContent = m;
                            modelSelect.appendChild(opt);
                        });
                    }

                    renderTop20Table();
                } else {
                    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color:#f43f5e;">${data.message}</td></tr>`;
                }
            } catch (err) {
                console.error("Top 20 Error:", err);
                if (tbody.innerHTML === '') {
                    tbody.innerHTML = `<tr><td colspan="7" style="text-align:center; padding: 40px; color:#f43f5e;">Failed to fetch Top 20 data.</td></tr>`;
                }
            }
        }

        function renderTop20Table() {
            const tbody = document.getElementById('top20TableBody');
            const modelFilter = document.getElementById('top20ModelSelect').value;

            const filtered = top20FullData.filter(item => {
                if (!modelFilter) return true;
                return item.strategy === modelFilter || item.strategy.startsWith(modelFilter + '_');
            });

            tbody.innerHTML = '';
            if (filtered.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align:center; padding: 40px; color: #94a3b8;">No records match your filter.</td></tr>';
                return;
            }

            // [V20260206_1515] Scale for heat-bars
            const maxTrades = Math.max(...filtered.map(d => d.trade_count), 1);

            filtered.forEach((item, index) => {
                const tradePct = (item.trade_count / maxTrades) * 100;
                const tradeBrightness = 0.6 + (item.trade_count / maxTrades) * 1.0;

                // [V20260208_0140] Scalper highlighting
                let strategyStyle = "font-weight:600; color: #f1f5f9;";
                const tpMatch = item.strategy.match(/tp([\d.]+)/);
                const slMatch = item.strategy.match(/sl([\d.]+)/);
                if (tpMatch && slMatch) {
                    const tpVal = parseFloat(tpMatch[1]);
                    const slVal = parseFloat(slMatch[1]);
                    if (tpVal > 0 && slVal >= tpVal * scalperRatio) {
                        strategyStyle = "font-weight:800; color: #fbbf24; text-shadow: 0 0 8px rgba(251, 191, 36, 0.3);";
                    }
                }

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td style="color: ${index < 3 ? '#fbbf24' : '#94a3b8'}; font-weight: 700;">#${index + 1}</td>
                    <td style="${strategyStyle}">${item.strategy} <span style="color: #6366f1; margin: 0 8px;">|</span> ${item.product}</td>
                    <td style="text-align: right; font-family: monospace; font-weight: 700;" class="${item.total_net >= 0 ? 'positive' : 'negative'}">$${item.total_net.toFixed(2)}</td>
                    <td style="color: ${item.buyPercent >= 60 ? '#4ade80' : '#f1f5f9'};">${item.buyPercent}%</td>
                    <td style="color: ${item.sellPercent >= 60 ? '#4ade80' : '#f1f5f9'};">${item.sellPercent}%</td>
                    <td class="trade-count-cell" style="color: #f1f5f9; font-family: monospace;">
                        <div class="trade-bar-bg bar-trades" style="width: ${tradePct}%; filter: brightness(${tradeBrightness})"></div>
                        ${item.trade_count}
                    </td>
                    <td style="text-align: right; min-width: 280px;">
                        <div style="display:flex; gap: 4px; justify-content: flex-end;">
                            <button class="push-btn" onclick="pushToGrid('${item.strategy}', '${item.product}', 'buy_net')" title="Push Buy Net to Grid" 
                                style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #4ade80; padding: 6px 8px;">
                                <i class="fas fa-arrow-up"></i> Buy
                            </button>
                            <button class="push-btn" onclick="pushToGrid('${item.strategy}', '${item.product}', 'sell_net')" title="Push Sell Net to Grid"
                                style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171; padding: 6px 8px;">
                                <i class="fas fa-arrow-down"></i> Sell
                            </button>
                            <button class="push-btn" onclick="pushToGrid('${item.strategy}', '${item.product}', 'net')" title="Push Both to Grid"
                                style="background: rgba(99, 102, 241, 0.2); border: 1px solid rgba(99, 102, 241, 0.5); color: #818cf8; padding: 6px 8px;">
                                <i class="fas fa-bolt"></i> Both
                            </button>
                            <div style="width: 1px; background: rgba(255,255,255,0.1); margin: 0 4px;"></div>
                            <button class="push-btn" 
                                style="background: rgba(16, 185, 129, 0.3); color: #f1f5f9; padding: 6px 8px;"
                                onclick="syncActivationFromTop20('${item.strategy}', '${item.product}', 'long')" title="Auto Buy (Long)">
                                B
                            </button>
                            <button class="push-btn" 
                                style="background: rgba(239, 68, 68, 0.3); color: #f1f5f9; padding: 6px 8px;"
                                onclick="syncActivationFromTop20('${item.strategy}', '${item.product}', 'short')" title="Auto Sell (Short)">
                                S
                            </button>
                            <button class="push-btn" 
                                style="background: rgba(251, 191, 36, 0.3); color: #f1f5f9; padding: 6px 8px;"
                                onclick="syncActivationFromTop20('${item.strategy}', '${item.product}', 'both')" title="Auto Both">
                                Both
                            </button>
                        </div>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        async function pushToGrid(strategy, product, metric = 'net', group = null) {
            const mode = document.getElementById('runMode').value;
            try {
                const res = await fetch('/api/push_to_grid_v2', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ mode, strategy, product, metric, group })
                });
                const data = await res.json();
                if (data.success) {
                    alert(`Successfully promoted ${strategy} | ${product} (${metric}) to grid_live.json ${group ? '(Group: ' + group + ')' : ''}`);
                } else {
                    alert("Grid Push Failed: " + data.message);
                }
            } catch (err) {
                alert("Network error while pushing to grid");
            }
        }

        async function syncActivationFromTop20(strategyKey, product, direction = 'both') {
            let appName = "";
            let params = "";

            if (strategyKey.includes('_')) {
                const parts = strategyKey.split('_');
                appName = parts[0];
                params = parts.slice(1).join('_');
            } else {
                appName = strategyKey;
                params = "";
            }

            try {
                if (direction === 'long' || direction === 'both') {
                    await toggleAutoActivation(appName, params, product, 'long', null);
                }
                if (direction === 'short' || direction === 'both') {
                    await toggleAutoActivation(appName, params, product, 'short', null);
                }

                alert(`Activated ${direction.toUpperCase()} Auto-Trade Monitor for ${strategyKey} on ${product}`);
                loadActivations(); // Refresh main table state
            } catch (err) {
                alert("Failed to sync activations: " + err.message);
            }
        }

        // ─────────────────────────────────────────────
        // [V20260209_1010] Bias-Flip Notification System
        // [V20260209_1330] Enhanced with visible status indicator
        // ─────────────────────────────────────────────
        let previousBias = null;
        let currentBiasData = null;
        let biasCheckInterval = null;
        let biasFlipCounter = 0; // [V20260209_1330] Track number of flips detected

        function updateBiasMonitorStatus(bias, lastCheck) {
            // [V20260209_1330] Update visible status indicator
            const currentBiasEl = document.getElementById('currentBiasDisplay');
            const lastCheckEl = document.getElementById('lastCheckTime');

            if (currentBiasEl && bias) {
                currentBiasEl.textContent = bias;
                currentBiasEl.style.color = bias === 'BUY' ? '#10b981' : '#f43f5e';
            }

            if (lastCheckEl) {
                const now = new Date();
                lastCheckEl.textContent = now.toLocaleTimeString();
            }
        }

        async function checkBiasFlip() {
            try {
                // Get current mode and date
                const mode = document.getElementById('runMode').value;
                const date = document.getElementById('statsDate').value;

                // [V20260209_1330] Update last check time
                updateBiasMonitorStatus(null, new Date());

                // Fetch config to check if notifications are suspended
                const configResp = await fetch('/api/config');
                const config = await configResp.json();

                if (config.bias_notifications_suspended) {
                    console.log('[BIAS-CHECK] Notifications suspended');
                    return;
                }

                // Fetch targeted strategies file
                const resp = await fetch(`json/${mode}/${date}/_targeted_strategies.json`);
                if (!resp.ok) {
                    console.warn('[BIAS-CHECK] Failed to fetch _targeted_strategies.json');
                    return;
                }

                const data = await resp.json();
                const currentBias = data.bias;

                // [V20260209_1330] Update visible status with current bias
                updateBiasMonitorStatus(currentBias, new Date());

                // [V20260209_1335] Log bias history every 5 minutes
                const now = Date.now();
                const lastHistoryLog = window.lastBiasHistoryLog || 0;
                if (now - lastHistoryLog >= 300000) { // 5 minutes
                    window.lastBiasHistoryLog = now;
                    await logBiasHistory(currentBias, data, mode);
                }

                // Check if bias has flipped
                if (previousBias && previousBias !== currentBias) {
                    console.log(`🔄 [BIAS FLIP DETECTED] ${previousBias} → ${currentBias}`);
                    console.log(`   Market Condition: ${data.market_condition}`);
                    console.log(`   Recent Buy P&L: $${data.recent_buy_pnl}`);
                    console.log(`   Recent Sell P&L: $${data.recent_sell_pnl}`);

                    // [V20260209_1330] Increment flip counter
                    biasFlipCounter++;
                    const flipCountEl = document.getElementById('flipCount');
                    if (flipCountEl) flipCountEl.textContent = biasFlipCounter;

                    // Store current data for action handling
                    currentBiasData = {
                        bias_from: previousBias,
                        bias_to: currentBias,
                        data: data,
                        mode: mode
                    };

                    // Show notification based on config
                    if (config.ai_picker_prompt) {
                        showBiasNotification(currentBiasData);
                    } else {
                        // Auto-activate without prompt
                        await autoActivateStrategy(currentBiasData);
                    }
                } else if (previousBias === null) {
                    console.log(`✅ [INITIAL BIAS] ${currentBias} - Monitoring started`);
                    console.log(`   Market: ${data.market_condition} | Status: ${data.status}`);
                }

                previousBias = currentBias;

            } catch (err) {
                console.error('❌ [BIAS-CHECK-ERROR]', err);
            }
        }

        // [V20260209_1335] Log bias history for tracking
        async function logBiasHistory(bias, data, mode) {
            try {
                await fetch('/api/bias_history', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        timestamp: new Date().toISOString(),
                        bias: bias,
                        market_condition: data.market_condition,
                        status: data.status,
                        recent_buy_pnl: data.recent_buy_pnl,
                        recent_sell_pnl: data.recent_sell_pnl,
                        recent_buy_count: data.recent_buy_count,
                        recent_sell_count: data.recent_sell_count,
                        run_mode: mode
                    })
                });
                console.log(`📊 [BIAS-HISTORY] Logged: ${bias} (${data.market_condition})`);
            } catch (err) {
                console.warn('[BIAS-HISTORY] Failed to log:', err);
            }
        }


        function showBiasNotification(biasData) {
            // Select best scalper for the new bias
            const scalpers = biasData.data.strategies.filter(s => s && s.scalper);
            if (!scalpers.length) {
                console.log('[WARNING] No scalpers found for bias flip');
                return;
            }

            // Sort by net P&L, then trade count
            scalpers.sort((a, b) => {
                const netA = typeof a.net === 'number' ? a.net : -Infinity;
                const netB = typeof b.net === 'number' ? b.net : -Infinity;
                if (netB !== netA) return netB - netA;
                const tradesA = typeof a.trades === 'number' ? a.trades : 0;
                const tradesB = typeof b.trades === 'number' ? b.trades : 0;
                return tradesB - tradesA;
            });

            const bestScalper = scalpers[0];

            // Update modal content
            document.getElementById('biasFrom').textContent = biasData.bias_from;
            document.getElementById('biasFrom').className = `bias-badge bias-${biasData.bias_from.toLowerCase()}`;

            document.getElementById('biasTo').textContent = biasData.bias_to;
            document.getElementById('biasTo').className = `bias-badge bias-${biasData.bias_to.toLowerCase()}`;

            document.getElementById('recommendedStrategy').textContent = bestScalper.strategy;
            document.getElementById('recommendedProduct').textContent = bestScalper.product;

            // Store recommendation for action handling
            currentBiasData.recommended_strategy = bestScalper.strategy;
            currentBiasData.recommended_product = bestScalper.product;

            // Show modal
            document.getElementById('biasNotificationOverlay').style.display = 'block';
        }

        async function handleBiasAction(action) {
            try {
                const biasData = currentBiasData;

                // Log the action
                await fetch('/api/notification_action', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        bias_from: biasData.bias_from,
                        bias_to: biasData.bias_to,
                        recommended_strategy: biasData.recommended_strategy,
                        recommended_product: biasData.recommended_product,
                        action: action,
                        run_mode: biasData.mode
                    })
                });

                // Handle specific actions
                if (action === 'activated' || action === 'auto_activate') {
                    // [V20260209_1900] FIRST: Deactivate wrong-bias strategies
                    console.log(`🔄 [BIAS-SWITCH] Deactivating ${biasData.bias_from}-bias strategies...`);

                    const deactivateResp = await fetch('/api/deactivate_wrong_bias', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            current_bias: biasData.bias_to,
                            mode: biasData.mode
                        })
                    });

                    const deactivateResult = await deactivateResp.json();
                    if (deactivateResult.success && deactivateResult.deactivated > 0) {
                        console.log(`✅ [BIAS-SWITCH] Deactivated ${deactivateResult.deactivated} wrong-bias strategies:`);
                        deactivateResult.strategies.forEach(s => console.log(`   - ${s}`));
                    }

                    // [V20260209_1900] SECOND: Activate new strategy with bias tag
                    const metric = biasData.bias_to === 'BUY' ? 'buy_net' : 'sell_net';

                    const activateResp = await fetch('/api/smart_target/activate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({
                            strategy: biasData.recommended_strategy,
                            product: biasData.recommended_product,
                            metric: metric,
                            mode: biasData.mode,
                            bias: biasData.bias_to  // [V20260209_1900] Tag with current bias
                        })
                    });

                    const activateResult = await activateResp.json();

                    if (activateResult.success) {
                        console.log(`✅ [BIAS-SWITCH] Activated ${biasData.recommended_strategy} on ${biasData.recommended_product} for ${biasData.bias_to} bias`);
                        alert(`✅ Bias Switch Complete!\n\nDeactivated: ${deactivateResult.deactivated} ${biasData.bias_from}-bias strategies\nActivated: ${biasData.recommended_strategy} on ${biasData.recommended_product} (${biasData.bias_to} bias)`);
                    } else {
                        alert(`❌ Activation failed: ${activateResult.error}`);
                    }
                }

                if (action === 'suspended') {
                    alert('🔕 Bias-flip notifications suspended. Update config.json to re-enable.');
                }

                if (action === 'auto_activate') {
                    alert('⚡ Auto-activate mode enabled. Future bias flips will activate automatically without prompts.');
                }

                // Close modal
                document.getElementById('biasNotificationOverlay').style.display = 'none';

            } catch (err) {
                console.error('[BIAS-ACTION-ERROR]', err);
                alert('Failed to process action: ' + err.message);
            }
        }

        async function autoActivateStrategy(biasData) {
            // Same as 'activated' action but without showing modal
            const scalpers = biasData.data.strategies.filter(s => s && s.scalper);
            if (!scalpers.length) return;

            scalpers.sort((a, b) => {
                const netA = typeof a.net === 'number' ? a.net : -Infinity;
                const netB = typeof b.net === 'number' ? b.net : -Infinity;
                if (netB !== netA) return netB - netA;
                return (b.trades || 0) - (a.trades || 0);
            });

            const bestScalper = scalpers[0];
            const metric = biasData.bias_to === 'BUY' ? 'buy_net' : 'sell_net';

            // Log action
            await fetch('/api/notification_action', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    bias_from: biasData.bias_from,
                    bias_to: biasData.bias_to,
                    recommended_strategy: bestScalper.strategy,
                    recommended_product: bestScalper.product,
                    action: 'auto_activated',
                    run_mode: biasData.mode
                })
            });

            // [V20260209_1900] FIRST: Deactivate wrong-bias strategies
            console.log(`🔄 [AUTO-SWITCH] Deactivating ${biasData.bias_from}-bias strategies...`);

            const deactivateResp = await fetch('/api/deactivate_wrong_bias', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    current_bias: biasData.bias_to,
                    mode: biasData.mode
                })
            });

            const deactivateResult = await deactivateResp.json();
            if (deactivateResult.success && deactivateResult.deactivated > 0) {
                console.log(`✅ [AUTO-SWITCH] Deactivated ${deactivateResult.deactivated} wrong-bias strategies`);
            }

            // [V20260209_1900] SECOND: Activate strategy with bias tag
            await fetch('/api/smart_target/activate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    strategy: bestScalper.strategy,
                    product: bestScalper.product,
                    metric: metric,
                    mode: biasData.mode,
                    bias: biasData.bias_to  // [V20260209_1900] Tag with current bias
                })
            });

            console.log(`✅ [AUTO-ACTIVATED] ${bestScalper.strategy} on ${bestScalper.product} for ${biasData.bias_to} bias`);
        }

        async function viewNotificationLog() {
            try {
                const mode = document.getElementById('runMode').value;
                const resp = await fetch(`/api/notification_log?mode=${mode}`);
                const data = await resp.json();

                if (!data.success) {
                    alert('Failed to load notification log');
                    return;
                }

                // Build HTML table
                let html = `
                    <div style="background: var(--bg-accent); padding: 30px; border-radius: 16px; max-width: 1200px; margin: 20px auto;">
                        <h2 style="margin-bottom: 20px; color: var(--accent-primary);">
                            <i class="fas fa-bell"></i> Bias-Flip Notification Log
                        </h2>
                        <table style="width: 100%; border-collapse: collapse;">
                            <thead>
                                <tr style="background: rgba(99, 102, 241, 0.1); border-bottom: 2px solid var(--accent-primary);">
                                    <th style="padding: 12px; text-align: left;">Timestamp</th>
                                    <th style="padding: 12px; text-align: center;">Bias Change</th>
                                    <th style="padding: 12px; text-align: left;">Recommended Strategy</th>
                                    <th style="padding: 12px; text-align: left;">Product</th>
                                    <th style="padding: 12px; text-align: center;">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                if (data.logs.length === 0) {
                    html += `<tr><td colspan="5" style="padding: 20px; text-align: center; color: var(--text-dim);">No notifications yet</td></tr>`;
                } else {
                    data.logs.forEach(log => {
                        const actionColors = {
                            'activated': '#10b981',
                            'auto_activate': '#f59e0b',
                            'auto_activated': '#f59e0b',
                            'dismissed': '#94a3b8',
                            'suspended': '#f43f5e'
                        };
                        const actionColor = actionColors[log.action] || '#94a3b8';

                        html += `
                            <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.05);">
                                <td style="padding: 12px; font-size: 0.85em; color: var(--text-dim);">
                                    ${new Date(log.timestamp).toLocaleString()}
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <span style="color: #f43f5e; font-weight: 700;">${log.bias_from}</span>
                                    <i class="fas fa-arrow-right" style="margin: 0 8px; color: var(--accent-primary);"></i>
                                    <span style="color: #10b981; font-weight: 700;">${log.bias_to}</span>
                                </td>
                                <td style="padding: 12px; font-family: monospace; font-size: 0.9em;">
                                    ${log.recommended_strategy}
                                </td>
                                <td style="padding: 12px; color: #fbbf24; font-weight: 600;">
                                    ${log.recommended_product}
                                </td>
                                <td style="padding: 12px; text-align: center;">
                                    <span style="background: ${actionColor}; color: white; padding: 4px 12px; border-radius: 8px; font-size: 0.85em; font-weight: 600;">
                                        ${log.action.toUpperCase().replace('_', ' ')}
                                    </span>
                                </td>
                            </tr>
                        `;
                    });
                }

                html += `
                            </tbody>
                        </table>
                        <div style="margin-top: 20px; text-align: center;">
                            <button onclick="this.parentElement.parentElement.remove()" 
                                style="background: var(--accent-primary); color: white; padding: 10px 30px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                                Close
                            </button>
                        </div>
                    </div>
                `;

                // Create overlay
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); z-index: 10001; overflow-y: auto; padding: 20px;';
                overlay.innerHTML = html;
                overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
                document.body.appendChild(overlay);

            } catch (err) {
                console.error('[NOTIFICATION-LOG-ERROR]', err);
                alert('Failed to load notification log');
            }
        }

        // [V20260209_1335] View Bias History
        async function viewBiasHistory() {
            try {
                const mode = document.getElementById('runMode').value;
                const resp = await fetch(`/api/bias_history?mode=${mode}&limit=100`);
                const data = await resp.json();

                if (!data.success) {
                    alert('Failed to load bias history');
                    return;
                }

                // Build HTML table
                let html = `
                    <div style="background: var(--bg-accent); padding: 30px; border-radius: 16px; max-width: 1400px; margin: 20px auto;">
                        <h2 style="margin-bottom: 20px; color: var(--accent-primary);">
                            <i class="fas fa-history"></i> Bias History (Last 100 entries)
                        </h2>
                        <p style="color: var(--text-dim); margin-bottom: 20px;">
                            Market bias logged every 5 minutes. Total entries: ${data.history.length}
                        </p>
                        <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                            <thead>
                                <tr style="background: rgba(99, 102, 241, 0.1); border-bottom: 2px solid var(--accent-primary);">
                                    <th style="padding: 12px; text-align: left;">Timestamp</th>
                                    <th style="padding: 12px; text-align: center;">Bias</th>
                                    <th style="padding: 12px; text-align: center;">Market</th>
                                    <th style="padding: 12px; text-align: center;">Status</th>
                                    <th style="padding: 12px; text-align: right;">Buy P&L</th>
                                    <th style="padding: 12px; text-align: right;">Sell P&L</th>
                                    <th style="padding: 12px; text-align: center;">Buy Trades</th>
                                    <th style="padding: 12px; text-align: center;">Sell Trades</th>
                                </tr>
                            </thead>
                            <tbody>
                `;

                if (data.history.length === 0) {
                    html += `<tr><td colspan="8" style="padding: 20px; text-align: center; color: var(--text-dim);">No history yet. History is logged every 5 minutes.</td></tr>`;
                } else {
                    data.history.forEach((entry, idx) => {
                        const biasColor = entry.bias === 'BUY' ? '#10b981' : '#f43f5e';
                        const buyPnl = parseFloat(entry.recent_buy_pnl || 0);
                        const sellPnl = parseFloat(entry.recent_sell_pnl || 0);
                        const buyColor = buyPnl >= 0 ? '#10b981' : '#f43f5e';
                        const sellColor = sellPnl >= 0 ? '#10b981' : '#f43f5e';

                        html += `
                            <tr style="border-bottom: 1px solid rgba(255, 255, 255, 0.05); ${idx === 0 ? 'background: rgba(99, 102, 241, 0.05);' : ''}">
                                <td style="padding: 10px; font-size: 0.85em; color: var(--text-dim);">
                                    ${new Date(entry.timestamp).toLocaleString()}
                                </td>
                                <td style="padding: 10px; text-align: center;">
                                    <span style="background: ${biasColor}; color: white; padding: 4px 12px; border-radius: 6px; font-weight: 700; font-size: 0.85em;">
                                        ${entry.bias}
                                    </span>
                                </td>
                                <td style="padding: 10px; text-align: center; color: var(--text-main); font-weight: 600;">
                                    ${entry.market_condition}
                                </td>
                                <td style="padding: 10px; text-align: center; color: #fbbf24; font-weight: 600;">
                                    ${entry.status}
                                </td>
                                <td style="padding: 10px; text-align: right; color: ${buyColor}; font-weight: 600;">
                                    $${buyPnl.toFixed(2)}
                                </td>
                                <td style="padding: 10px; text-align: right; color: ${sellColor}; font-weight: 600;">
                                    $${sellPnl.toFixed(2)}
                                </td>
                                <td style="padding: 10px; text-align: center; color: var(--text-dim);">
                                    ${entry.recent_buy_count || 0}
                                </td>
                                <td style="padding: 10px; text-align: center; color: var(--text-dim);">
                                    ${entry.recent_sell_count || 0}
                                </td>
                            </tr>
                        `;
                    });
                }

                html += `
                            </tbody>
                        </table>
                        <div style="margin-top: 20px; text-align: center;">
                            <button onclick="this.parentElement.parentElement.remove()" 
                                style="background: var(--accent-primary); color: white; padding: 10px 30px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                                Close
                            </button>
                        </div>
                    </div>
                `;

                // Create overlay
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.9); z-index: 10001; overflow-y: auto; padding: 20px;';
                overlay.innerHTML = html;
                overlay.onclick = (e) => { if (e.target === overlay) overlay.remove(); };
                document.body.appendChild(overlay);

            } catch (err) {
                console.error('[BIAS-HISTORY-ERROR]', err);
                alert('Failed to load bias history');
            }
        }

        // Start bias checking on page load
        function startBiasMonitoring() {
            // Check immediately
            checkBiasFlip();

            // Then check every 5 seconds
            if (biasCheckInterval) clearInterval(biasCheckInterval);
            biasCheckInterval = setInterval(checkBiasFlip, 5000);

            console.log('[BIAS-MONITOR] Started checking for bias flips every 5 seconds');
        }

        window.onload = function () {
            init();
            startBiasMonitoring(); // [V20260209_1010] Start bias-flip monitoring
        };

        // ========== PERFORMANCE SUMMARY BREAKDOWN [V20260210_0245] ==========
        async function openPerformanceSummary() {
            document.getElementById('summaryModal').style.display = 'block';
            const modalBody = document.getElementById('summaryGridV2');
            modalBody.innerHTML = '<div class="loading">📊 Fetching Global Totals for Summary...</div>';

            const mode = document.getElementById('runMode').value;
            const date = document.getElementById('statsDate').value;

            try {
                // [V20260210_0255] Fetch WITHOUT limit to ensure summary figures match the global dashboard
                const response = await fetch(`/api/stats_summary?mode=${mode}&date=${date}`);
                const data = await response.json();

                if (data.success) {
                    globalTimeDist = data.global_time_dist || null; // [V20260210_1415]
                    summaryMasterData = data.data; // [V20260210_1420]

                    // Initialize Modal Timebar
                    if (snapshotData) {
                        const slider = document.getElementById('summaryTimeSlider');
                        const times = [];
                        Object.values(snapshotData).forEach(m => Object.values(m).forEach(s => s.forEach(pt => times.push(new Date(pt.t).getTime()))));
                        if (times.length > 0) {
                            const min = Math.min(...times);
                            const max = Math.max(...times);
                            slider.min = min;
                            slider.max = max;
                            slider.value = max;
                            summaryFilterTime = max;
                            document.getElementById('summaryStartTimeLabel').textContent = formatTime(new Date(min));
                            document.getElementById('summaryEndTimeLabel').textContent = formatTime(new Date(max));
                            document.getElementById('summaryPlaybackTime').textContent = formatTime(new Date(max));
                            document.getElementById('summaryPlaybackPanel').style.display = 'block';
                        } else {
                            document.getElementById('summaryPlaybackPanel').style.display = 'none';
                        }
                    } else {
                        document.getElementById('summaryPlaybackPanel').style.display = 'none';
                    }

                    renderSummaryGrid(data.data);
                } else {
                    modalBody.innerHTML = `<div class="loading" style="color:red">Error: ${data.message}</div>`;
                }
            } catch (err) {
                console.error('[SUMMARY-FETCH-ERROR]', err);
                modalBody.innerHTML = `<div class="loading" style="color:red">Fetch Failed: ${err.message}</div>`;
            }
        }

        // Global state for summary sorting
        let summaryMasterData = []; // [V20260210_1420] Original full day data
        let summaryRawData = [];
        let summarySortKey = 'total_net'; // 'name', 'buy_net', 'sell_net', 'total_net'
        let summarySortAsc = false;
        // [V20260210_0545] State Persistence for Hierarchy
        let expandedRowsState = new Set();
        let isFirstRender = true;
        let leaderboardMetric = 'total'; // [V20260210_1135] Leaderboard metric state
        let globalTimeDist = null; // [V20260210_1415] Global session lifecycle distribution
        let summaryFilterTime = 0; // [V20260210_1420] Playback time for modal
        let isSummaryPlaying = false; // [V20260210_1435]
        let summaryPlaybackInterval = null;
        let summaryPlaybackSpeedIdx = 0;
        const summarySpeeds = [1, 10, 60, 300, 1800, 3600];
        let summaryLastLastTick = null;

        function sortSummary(key) {
            if (summarySortKey === key) {
                summarySortAsc = !summarySortAsc;
            } else {
                summarySortKey = key;
                summarySortAsc = false; // Default desc for metrics, asc for name? handling in sort logic
                if (key === 'name') summarySortAsc = true;
            }
            renderSummaryGrid(summaryRawData);
        }

        function renderSummaryGrid(data) {
            const grid = document.getElementById('summaryGridV2');
            if (!grid) return;

            // Store data for re-sorting
            if (data) summaryRawData = data;

            // Helper for color classes
            const getValClass = (val) => val > 0 ? 'val-positive' : (val < 0 ? 'val-negative' : 'val-neutral');
            const esc = (s) => String(s || '').replace(/'/g, "\\'"); // Escape single quotes for onclick
            const getSortIcon = (key) => {
                if (summarySortKey !== key) return '<i class="fas fa-sort" style="opacity:0.3"></i>';
                return summarySortAsc ? '<i class="fas fa-sort-up"></i>' : '<i class="fas fa-sort-down"></i>';
            };

            // [V20260210_1430] Local global time dist aggregation (respects playback/master)
            const currentGlobalDist = {};
            for (let i = 0; i < 24; i++) currentGlobalDist[String(i).padStart(2, '0')] = 0;
            summaryRawData.forEach(d => {
                Object.entries(d.time_dist || {}).forEach(([h, c]) => {
                    currentGlobalDist[h] = (currentGlobalDist[h] || 0) + c;
                });
            });

            // [V20260210_0500] Switch to Split View Layout
            grid.className = 'split-view-container';
            grid.innerHTML = `
                <div class="hier-panel">
                    <div class="box-header" style="display:flex; justify-content:space-between; align-items:center; border-bottom:none; margin-bottom:5px;">
                        <span><i class="fas fa-sitemap"></i> Performance Hierarchy</span> 
                        <div style="display:flex; gap:5px">
                            <button onclick="window.expandAllHier()" style="padding:4px 8px; font-size:0.75em; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#94a3b8; border-radius:4px; cursor:pointer;" title="Expand All"><i class="fas fa-plus"></i></button>
                            <button onclick="window.collapseAllHier()" style="padding:4px 8px; font-size:0.75em; background:rgba(255,255,255,0.1); border:1px solid rgba(255,255,255,0.2); color:#94a3b8; border-radius:4px; cursor:pointer;" title="Collapse All"><i class="fas fa-minus"></i></button>
                        </div>
                    </div>
                    
                    <!-- [V20260210_1415] Global Session Lifecycle Timebar -->
                    <div style="margin-bottom: 15px; padding: 0 5px;">
                        <div style="font-size: 0.65em; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 2px; font-weight: 700;">Global Session Lifecycle (00:00 - 23:59)</div>
                        ${renderTimeBar(currentGlobalDist)}
                    </div>

                    <table class="hier-table">
                        <thead>
                            <tr style="border-bottom: 2px solid rgba(255,255,255,0.1); font-size: 0.75em; text-transform: uppercase; color: #94a3b8;">
                                <th onclick="sortSummary('name')" style="padding: 10px; cursor: pointer;">Hierarchy ${getSortIcon('name')}</th>
                                <th onclick="sortSummary('buy_net')" style="padding: 10px; text-align: right; cursor: pointer;">Buy Net ${getSortIcon('buy_net')}</th>
                                <th onclick="sortSummary('sell_net')" style="padding: 10px; text-align: right; cursor: pointer;">Sell Net ${getSortIcon('sell_net')}</th>
                                <th onclick="sortSummary('total_net')" style="padding: 10px; text-align: right; cursor: pointer;">Total Net ${getSortIcon('total_net')}</th>
                                <th style="padding: 10px; text-align: center; width: 60px;"><i class="fas fa-th"></i></th>
                            </tr>
                        </thead>
                        <tbody id="hierTreeBody"></tbody>
                    </table>
                </div>
                <div class="leader-panel">
                    <div class="box-header" style="display:flex; justify-content:space-between; align-items:center">
                        <span><i class="fas fa-trophy"></i> Best Parameters</span>
                        <div style="display:flex; gap:2px; background:rgba(0,0,0,0.2); padding:2px; border-radius:6px;">
                            <button onclick="setLeaderboardMetric('total')" class="lb-toggle ${leaderboardMetric === 'total' ? 'active' : ''}" style="padding:4px 8px; font-size:0.7em; background:${leaderboardMetric === 'total' ? 'rgba(99, 102, 241, 0.3)' : 'transparent'}; border:none; color:${leaderboardMetric === 'total' ? '#fff' : '#64748b'}; border-radius:4px; cursor:pointer">Total</button>
                            <button onclick="setLeaderboardMetric('buy')" class="lb-toggle ${leaderboardMetric === 'buy' ? 'active' : ''}" style="padding:4px 8px; font-size:0.7em; background:${leaderboardMetric === 'buy' ? 'rgba(16, 185, 129, 0.3)' : 'transparent'}; border:none; color:${leaderboardMetric === 'buy' ? '#fff' : '#64748b'}; border-radius:4px; cursor:pointer">Buy</button>
                            <button onclick="setLeaderboardMetric('sell')" class="lb-toggle ${leaderboardMetric === 'sell' ? 'active' : ''}" style="padding:4px 8px; font-size:0.7em; background:${leaderboardMetric === 'sell' ? 'rgba(244, 63, 94, 0.3)' : 'transparent'}; border:none; color:${leaderboardMetric === 'sell' ? '#fff' : '#64748b'}; border-radius:4px; cursor:pointer">Sell</button>
                        </div>
                    </div>
                    <div id="paramLeaderboard"></div>
                </div>
            `;

            // [V20260210_1135] Metric Setter
            window.setLeaderboardMetric = function (m) {
                leaderboardMetric = m;
                renderSummaryGrid(summaryRawData);
            };

            // Define Collapse/Expand handlers
            window.expandAllHier = function () {
                const rows = document.querySelectorAll('.hier-row');
                rows.forEach(r => {
                    r.classList.remove('hidden-row');
                    if (r.classList.contains('level-1') || r.classList.contains('level-2')) {
                        r.classList.add('expanded');
                    }
                });
            };

            window.collapseAllHier = function () {
                const rows = document.querySelectorAll('.hier-row');
                rows.forEach(r => {
                    if (r.classList.contains('level-1')) {
                        r.classList.remove('expanded');
                    } else {
                        r.classList.add('hidden-row');
                        r.classList.remove('expanded');
                    }
                });
            };

            // --- 1. Aggregation Logic ---
            const tree = {}; // Cat -> Win -> Ratio -> Product -> Stats
            const paramMap = {}; // Ratio -> Stats (Cross-strategy aggregation)

            summaryRawData.forEach(d => {
                const s = (d.strategy || '').toLowerCase();
                const p = (d.parm_raw || d.params || '').toLowerCase();
                const prod = (d.product || 'Unknown').toUpperCase();

                // Categorization
                let cat = 'Other';
                if (s.startsWith('breakout_r_rev')) cat = 'Breakout R_Rev';
                else if (s.startsWith('breakout_rev')) cat = 'Breakout Rev';
                else if (s.startsWith('breakout_r')) cat = 'Breakout R';
                else if (s.startsWith('breakout')) cat = 'Breakout Standard';

                // Window Size
                let winNum = null;
                const winInStrat = s.match(/_([234])(_|tp|sl|$)/);
                const winInParam = p.match(/^([234])(_|tp|sl|$)/) || p.match(/win([234])/) || p.match(/_([234])(_|tp|sl|$)/);
                if (winInStrat) winNum = winInStrat[1];
                else if (winInParam) winNum = winInParam[1];
                const winSize = winNum ? `Window ${winNum}` : 'Unknown Window';

                // Ratio / Parameter
                const tpMatch = p.match(/tp([\d.]+)/) || s.match(/tp([\d.]+)/);
                const slMatch = p.match(/sl([\d.]+)/) || s.match(/sl([\d.]+)/);
                const ratio = (tpMatch && slMatch) ? `TP ${parseFloat(tpMatch[1]).toFixed(1)} / SL ${parseFloat(slMatch[1]).toFixed(1)}` : (p || 'Base');

                // Initialize Tree Path
                const initStats = () => ({ n: 0, bn: 0, sn: 0, c: 0, bc: 0, sc: 0 });
                if (!tree[cat]) tree[cat] = { stats: initStats(), children: {} };
                if (!tree[cat].children[winSize]) tree[cat].children[winSize] = { stats: initStats(), children: {} };
                // Level 3 (Ratio) now needs children for Level 4 (Product)
                if (!tree[cat].children[winSize].children[ratio]) tree[cat].children[winSize].children[ratio] = { stats: initStats(), children: {} };
                // Level 4 (Product)
                if (!tree[cat].children[winSize].children[ratio].children[prod]) {
                    tree[cat].children[winSize].children[ratio].children[prod] = {
                        stats: initStats(),
                        meta: { strategy: d.strategy, parm_raw: d.parm_raw || d.params },
                        time_dist: d.time_dist // [V20260210_1415]
                    };
                }

                const net = d.total_net || 0;
                const buyNet = d.buy_net || 0;
                const sellNet = d.sell_net || 0;
                const buyCount = d.buy_count || 0;
                const sellCount = d.sell_count || 0;
                const count = buyCount + sellCount;

                // Update Tree Stats Helper
                const updateStats = (node) => {
                    node.stats.n += net;
                    node.stats.bn += buyNet;
                    node.stats.sn += sellNet;
                    node.stats.c += count;
                    node.stats.bc += buyCount;
                    node.stats.sc += sellCount;
                };

                updateStats(tree[cat]);
                updateStats(tree[cat].children[winSize]);
                updateStats(tree[cat].children[winSize].children[ratio]);
                updateStats(tree[cat].children[winSize].children[ratio].children[prod]);

                // Update Parameter Leaderboard Map
                if (!paramMap[ratio]) paramMap[ratio] = {
                    net: 0, count: 0,
                    buy_net: 0, buy_count: 0,
                    sell_net: 0, sell_count: 0,
                    strategies: new Set(),
                    best_model: null,
                    best_product: null,
                    max_net: -Infinity,
                    raw: d.parm_raw || d.params || '' // [V20260210_1145] Capture raw for drill-down
                };
                paramMap[ratio].net += net;
                paramMap[ratio].count += count;
                paramMap[ratio].buy_net += buyNet;
                paramMap[ratio].buy_count += buyCount;
                paramMap[ratio].sell_net += sellNet;
                paramMap[ratio].sell_count += sellCount;
                paramMap[ratio].strategies.add(cat);

                // Track Best Single Match for direct promotion
                if (net > paramMap[ratio].max_net) {
                    paramMap[ratio].max_net = net;
                    paramMap[ratio].best_model = d.strategy;
                    paramMap[ratio].best_product = d.product;
                }
            });

            // Sorting Helper
            const sortNodes = (keys, obj) => {
                return keys.sort((a, b) => {
                    let valA, valB;
                    // Sort by Metric
                    if (summarySortKey === 'buy_net') { valA = obj[a].stats.bn; valB = obj[b].stats.bn; }
                    else if (summarySortKey === 'sell_net') { valA = obj[a].stats.sn; valB = obj[b].stats.sn; }
                    else if (summarySortKey === 'total_net') { valA = obj[a].stats.n; valB = obj[b].stats.n; }
                    else {
                        // Name sort
                        valA = a; valB = b;
                        // Special handling for Other/Windows to match logical order if name sort
                        if (summarySortKey === 'name') {
                            if (a === 'Other') return 1; if (b === 'Other') return -1;
                        }
                    }

                    if (summarySortKey === 'name') return summarySortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
                    return summarySortAsc ? valA - valB : valB - valA;
                });
            };

            // --- 2. Render Hierarchy (Left Panel) ---
            const tbody = document.getElementById('hierTreeBody');
            let rowIdCounter = 0;
            let hierHTML = '';

            const cats = sortNodes(Object.keys(tree), tree);

            // Pre-populate default expansions on first load if state is empty
            if (isFirstRender) {
                cats.forEach(c => {
                    expandedRowsState.add(c); // Level 1
                    Object.keys(tree[c].children).forEach(w => expandedRowsState.add(`${c}|${w}`)); // Level 2
                });
                isFirstRender = false;
            }

            cats.forEach(catKey => {
                const catNode = tree[catKey];
                const catId = `r-${rowIdCounter++}`;

                const catStableId = catKey;
                const isCatExpanded = expandedRowsState.has(catStableId);

                // Level 1: Category
                hierHTML += `
                    <tr class="hier-row level-1 ${isCatExpanded ? 'expanded' : ''}" data-level="1" data-id="${catId}" data-stable-id="${catStableId}" onclick="window.toggleHierRow(this)">
                        <td class="hier-cell">
                            <span class="toggle-icon">▶</span>${catKey}
                        </td>
                        <td class="hier-cell ${getValClass(catNode.stats.bn)}">$${catNode.stats.bn.toFixed(2)}</td>
                        <td class="hier-cell ${getValClass(catNode.stats.sn)}">$${catNode.stats.sn.toFixed(2)}</td>
                        <td class="hier-cell ${getValClass(catNode.stats.n)}">$${catNode.stats.n.toFixed(2)} <span style="opacity:0.5; font-size:0.75em">(${catNode.stats.c})</span></td>
                        <td class="hier-cell"></td>
                    </tr>
                `;

                const wins = sortNodes(Object.keys(catNode.children), catNode.children);
                wins.forEach(winKey => {
                    const winNode = catNode.children[winKey];
                    const winId = `r-${rowIdCounter++}`;

                    const winStableId = `${catKey}|${winKey}`;
                    const isWinExpanded = expandedRowsState.has(winStableId);
                    const winHiddenClass = isCatExpanded ? '' : 'hidden-row';

                    // Level 2: Window
                    hierHTML += `
                        <tr class="hier-row level-2 ${isWinExpanded ? 'expanded' : ''} ${winHiddenClass}" 
                            data-level="2" data-id="${winId}" data-parent="${catId}" data-stable-id="${winStableId}" onclick="window.toggleHierRow(this)">
                            <td class="hier-cell" style="padding-left: 30px">
                                <span class="toggle-icon">▶</span>${winKey}
                            </td>
                            <td class="hier-cell ${getValClass(winNode.stats.bn)}">$${winNode.stats.bn.toFixed(2)}</td>
                            <td class="hier-cell ${getValClass(winNode.stats.sn)}">$${winNode.stats.sn.toFixed(2)}</td>
                            <td class="hier-cell ${getValClass(winNode.stats.n)}">$${winNode.stats.n.toFixed(2)} <span style="opacity:0.5; font-size:0.75em">(${winNode.stats.c})</span></td>
                            <td class="hier-cell"></td>
                        </tr>
                    `;

                    // Level 3: Ratio
                    const ratios = sortNodes(Object.keys(winNode.children), winNode.children);
                    ratios.forEach(ratioKey => {
                        const ratioNode = winNode.children[ratioKey];
                        const ratioId = `r-${rowIdCounter++}`;

                        const ratioStableId = `${catKey}|${winKey}|${ratioKey}`;
                        const isRatioExpanded = expandedRowsState.has(ratioStableId);
                        const ratioHiddenClass = (isCatExpanded && isWinExpanded) ? '' : 'hidden-row';

                        hierHTML += `
                            <tr class="hier-row level-3 ${isRatioExpanded ? 'expanded' : ''} ${ratioHiddenClass}" 
                                data-level="3" data-id="${ratioId}" data-parent="${winId}" data-stable-id="${ratioStableId}" onclick="window.toggleHierRow(this)">
                                <td class="hier-cell" style="padding-left: 45px">
                                    <span class="toggle-icon">▶</span>${ratioKey}
                                </td>
                                <td class="hier-cell ${getValClass(ratioNode.stats.bn)}">$${ratioNode.stats.bn.toFixed(2)}</td>
                                <td class="hier-cell ${getValClass(ratioNode.stats.sn)}">$${ratioNode.stats.sn.toFixed(2)}</td>
                                <td class="hier-cell ${getValClass(ratioNode.stats.n)}">$${ratioNode.stats.n.toFixed(2)} <span style="opacity:0.5; font-size:0.75em">(${ratioNode.stats.c})</span></td>
                                <td class="hier-cell"></td>
                            </tr>
                        `;

                        // Level 4: Product (Drill Down)
                        const prods = sortNodes(Object.keys(ratioNode.children), ratioNode.children);
                        prods.forEach(prodKey => {
                            const prodNode = ratioNode.children[prodKey];
                            const prodHiddenClass = (isCatExpanded && isWinExpanded && isRatioExpanded) ? '' : 'hidden-row';

                            // [V20260210_1130] Escaped onclick calls
                            hierHTML += `
                                <tr class="hier-row level-4 ${prodHiddenClass}" data-level="4" data-parent="${ratioId}">
                                    <td class="hier-cell clickable" style="padding-left: 60px; color:#94a3b8; padding-bottom: 12px; vertical-align:top;" 
                                        onclick="showDrillDown('${esc(prodKey)}', '${esc(prodNode.meta.strategy)}', '${esc(prodNode.meta.parm_raw)}', 'all'); event.stopPropagation();">
                                        <div style="display:flex; align-items:center; gap:5px;">
                                            <i class="fas fa-chart-line" style="font-size:0.8em"></i>${prodKey}
                                        </div>
                                        ${renderTimeBar(prodNode.time_dist, true)}
                                    </td>
                                    <td class="hier-cell ${getValClass(prodNode.stats.bn)} clickable" onclick="showDrillDown('${esc(prodKey)}', '${esc(prodNode.meta.strategy)}', '${esc(prodNode.meta.parm_raw)}', 'buy'); event.stopPropagation();">$${prodNode.stats.bn.toFixed(2)}</td>
                                    <td class="hier-cell ${getValClass(prodNode.stats.sn)} clickable" onclick="showDrillDown('${esc(prodKey)}', '${esc(prodNode.meta.strategy)}', '${esc(prodNode.meta.parm_raw)}', 'sell'); event.stopPropagation();">$${prodNode.stats.sn.toFixed(2)}</td>
                                    <td class="hier-cell ${getValClass(prodNode.stats.n)} clickable" onclick="showDrillDown('${esc(prodKey)}', '${esc(prodNode.meta.strategy)}', '${esc(prodNode.meta.parm_raw)}', 'all'); event.stopPropagation();">$${prodNode.stats.n.toFixed(2)} <span style="opacity:0.5; font-size:0.75em">(${prodNode.stats.c})</span></td>
                                    <td class="hier-cell" style="text-align:center; padding: 2px;">
                                        <div style="display:flex; gap:2px; justify-content:center">
                                            <button class="push-btn" onclick="pushToGrid('${esc(prodNode.meta.strategy)}', '${esc(prodKey)}', 'buy_net', '${esc(ratioStableId)}'); event.stopPropagation();" 
                                                style="padding: 2px 5px; font-size: 0.7em; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #4ade80;" title="Push Buy">B</button>
                                            <button class="push-btn" onclick="pushToGrid('${esc(prodNode.meta.strategy)}', '${esc(prodKey)}', 'sell_net', '${esc(ratioStableId)}'); event.stopPropagation();" 
                                                style="padding: 2px 5px; font-size: 0.7em; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171;" title="Push Sell">S</button>
                                        </div>
                                    </td>
                                </tr>
                            `;
                        });
                    });
                });
            });
            tbody.innerHTML = hierHTML;

            // --- 3. Render Leaderboard (Right Panel) ---
            const lbContainer = document.getElementById('paramLeaderboard');
            let lbHTML = '';

            // Determine sort field based on metric
            const getMetricVal = (item) => {
                if (leaderboardMetric === 'buy') return item.buy_net;
                if (leaderboardMetric === 'sell') return item.sell_net;
                return item.net;
            };
            const getMetricCount = (item) => {
                if (leaderboardMetric === 'buy') return item.buy_count;
                if (leaderboardMetric === 'sell') return item.sell_count;
                return item.count;
            };

            const sortedParams = Object.keys(paramMap)
                .map(k => ({ key: k, ...paramMap[k] }))
                .filter(i => i.key !== 'Other' && i.key !== 'Base')
                .sort((a, b) => getMetricVal(b) - getMetricVal(a)) // Sort by selected metric
                .slice(0, 15); // Top 15

            sortedParams.forEach((item, idx) => {
                const val = getMetricVal(item);
                const count = getMetricCount(item);

                // [V20260210_1145] Clickable Leaderboard Item
                // Passing 'all' for product and appName, but specific raw param
                const drillDir = (leaderboardMetric === 'buy' || leaderboardMetric === 'sell') ? leaderboardMetric : 'all';

                lbHTML += `
                    <div class="leader-item" style="cursor: pointer; display:flex; align-items:center" onclick="showDrillDown('all', 'all', '${esc(item.raw)}', '${drillDir}'); event.stopPropagation();" title="Click to view all trades for this parameter">
                        <div class="leader-rank">#${idx + 1}</div>
                        <div class="leader-param" style="flex:1">
                            ${item.key}
                            <div style="font-size:0.7em; color:#64748b; font-weight:400">
                                Best: ${item.best_product} | ${Array.from(item.strategies).length} types
                            </div>
                        </div>
                        <div style="text-align:right; margin-right:10px">
                            <div class="leader-val ${getValClass(val)}">$${val.toFixed(2)}</div>
                            <div class="leader-count" style="font-size:0.7em">${count} trades</div>
                        </div>
                        <div style="display:flex; flex-direction:column; gap:2px">
                             <button class="push-btn" onclick="pushToGrid('${esc(item.best_model)}', '${esc(item.best_product)}', 'buy_net', 'Leaderboard|${esc(item.key)}'); event.stopPropagation();" 
                                 style="padding: 2px 6px; font-size: 0.7em; background: rgba(16, 185, 129, 0.2); border: 1px solid rgba(16, 185, 129, 0.4); color: #4ade80;" title="Promote Best Buy">B</button>
                             <button class="push-btn" onclick="pushToGrid('${esc(item.best_model)}', '${esc(item.best_product)}', 'sell_net', 'Leaderboard|${esc(item.key)}'); event.stopPropagation();" 
                                 style="padding: 2px 6px; font-size: 0.7em; background: rgba(239, 68, 68, 0.2); border: 1px solid rgba(239, 68, 68, 0.4); color: #f87171;" title="Promote Best Sell">S</button>
                        </div>
                    </div>
                `;
            });
            lbContainer.innerHTML = lbHTML;

            // --- 4. Define Toggle Logic (PERSISTENT & RECURSIVE RESPECTING) ---
            if (!window.toggleHierRow) {
                window.toggleHierRow = function (el) {
                    const stableId = el.dataset.stableId; // [V20260210_1155] Restored missing var

                    // Toggle expansion state
                    if (el.classList.contains('expanded')) {
                        el.classList.remove('expanded');
                        if (stableId) expandedRowsState.delete(stableId);
                    } else {
                        el.classList.add('expanded');
                        if (stableId) expandedRowsState.add(stableId);
                    }

                    const isExpanded = el.classList.contains('expanded');
                    const myLevel = parseInt(el.dataset.level);

                    // Stack to track visibility state of parents as we descend siblings
                    // Initial state: current row's expansion determines if next level is shown
                    const visStack = {};
                    visStack[myLevel] = isExpanded;

                    let next = el.nextElementSibling;
                    while (next) {
                        const nextLevel = parseInt(next.dataset.level);
                        if (nextLevel <= myLevel) break; // Finished siblings subtree

                        // Parent of 'next' is at 'nextLevel - 1'
                        // Check if that parent is expanded (visible in stack)
                        const parentExpanded = visStack[nextLevel - 1];

                        if (parentExpanded) {
                            next.classList.remove('hidden-row');
                            // Now set stack for *this* row's children based on its own expansion
                            const amIExpanded = next.classList.contains('expanded');
                            visStack[nextLevel] = amIExpanded;
                        } else {
                            next.classList.add('hidden-row');
                            // If I am hidden, my children are hidden too
                            visStack[nextLevel] = false;
                        }

                        next = next.nextElementSibling;
                    }
                };
            }


            const refreshTimeEl = document.getElementById('summaryRefreshTime');
            if (refreshTimeEl) refreshTimeEl.textContent = `Sync: ${new Date().toLocaleTimeString()}`;
        }

        // [V20260210_1415] Time Distribution Bar Renderer
        function renderTimeBar(dist, isMini = false) {
            if (!dist) return '<div style="font-size:0.6em; color:#475569">No time data</div>';
            const hours = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'));
            const max = Math.max(...Object.values(dist), 1);

            let html = `<div class="timebar-container ${isMini ? 'mini-timebar' : ''}">`;
            hours.forEach(h => {
                const count = dist[h] || 0;
                let opacity = 0.05;
                let color = 'rgba(255,255,255,0.05)';
                if (count > 0) {
                    opacity = 0.2 + (count / max) * 0.8;
                    color = '#fbbf24';
                }
                html += `<div class="timebar-segment" style="background:${color}; opacity:${opacity}" title="${h}:00 - ${count} trades"></div>`;
            });
            html += `</div>`;
            return html;
        }



        // [V20260210_1420] Summary Playback Logic
        function onSummarySliderInput() {
            const val = parseInt(document.getElementById('summaryTimeSlider').value);
            summaryFilterTime = val;
            document.getElementById('summaryPlaybackTime').textContent = formatTime(new Date(val));
            updateSummaryPlayback();
        }

        function onSummarySliderChange() {
            updateSummaryPlayback();
        }

        function updateSummaryPlayback() {
            if (!snapshotData || !summaryMasterData || summaryMasterData.length === 0) return;

            const targetMs = summaryFilterTime;
            const projected = summaryMasterData.map(d => {
                const prod = d.product;
                const appName = d.strategy;
                const params = d.parm_raw || d.params || '';

                // Robust mapping from snapshotData
                let points = (snapshotData[appName] && snapshotData[appName][prod]) ? snapshotData[appName][prod] : null;
                if (!points && params) {
                    const combinedKey = `${appName}_${params}`;
                    points = (snapshotData[combinedKey] && snapshotData[combinedKey][prod]) ? snapshotData[combinedKey][prod] : null;
                }
                if (!points || points.length === 0) return d;

                let bestPoint = null;
                for (let i = 0; i < points.length; i++) {
                    const ptTime = new Date(points[i].t).getTime();
                    if (ptTime <= targetMs) bestPoint = points[i];
                    else break;
                }

                if (!bestPoint) {
                    return { ...d, total_net: 0, buy_net: 0, sell_net: 0, trade_count: 0, buy_count: 0, sell_count: 0, net: 0, bn: 0, sn: 0, c: 0, bc: 0, sc: 0, time_dist: {} };
                }

                // [V20260210_1430] Project local time dist (mask future hours)
                const projectedDist = {};
                const targetHour = new Date(targetMs).getHours();
                Object.entries(d.time_dist || {}).forEach(([h, c]) => {
                    if (parseInt(h) <= targetHour) projectedDist[h] = c;
                });

                // Map back to tree-expected fields
                return {
                    ...d,
                    total_net: bestPoint.net || 0,
                    buy_net: bestPoint.buy_net || 0,
                    sell_net: bestPoint.sell_net || 0,
                    trade_count: (bestPoint.b_c || 0) + (bestPoint.s_c || 0),
                    buy_count: bestPoint.b_c || 0,
                    sell_count: bestPoint.s_c || 0,
                    // Tree aggregation keys
                    n: bestPoint.net || 0,
                    bn: bestPoint.buy_net || 0,
                    sn: bestPoint.sell_net || 0,
                    c: (bestPoint.b_c || 0) + (bestPoint.s_c || 0),
                    bc: bestPoint.b_c || 0,
                    sc: bestPoint.s_c || 0,
                    time_dist: projectedDist
                };
            });

            renderSummaryGrid(projected);
        }

        // [V20260210_1435] Summary Playback Engine
        function toggleSummaryPlayback() {
            isSummaryPlaying = !isSummaryPlaying;
            const btn = document.getElementById('summaryPlaybackPlay');
            if (isSummaryPlaying) {
                btn.innerHTML = '<i class="fas fa-pause"></i> <span>Pause</span>';
                btn.classList.add('active');
                summaryLastLastTick = Date.now();
                summaryPlaybackInterval = setInterval(tickSummaryPlayback, 50);
            } else {
                btn.innerHTML = '<i class="fas fa-play"></i> <span>Play</span>';
                btn.classList.remove('active');
                if (summaryPlaybackInterval) clearInterval(summaryPlaybackInterval);
            }
        }

        function tickSummaryPlayback() {
            if (!isSummaryPlaying) return;
            const now = Date.now();
            const delta = now - summaryLastLastTick;
            summaryLastLastTick = now;

            const slider = document.getElementById('summaryTimeSlider');
            const min = parseInt(slider.min);
            const max = parseInt(slider.max);
            let current = summaryFilterTime;

            const speed = summarySpeeds[summaryPlaybackSpeedIdx];
            current += (delta * speed);

            if (current >= max) {
                current = max;
                toggleSummaryPlayback();
            }

            slider.value = current;
            onSummarySliderInput();
        }

        function resetSummaryPlayback() {
            const slider = document.getElementById('summaryTimeSlider');
            slider.value = slider.min;
            onSummarySliderInput();
        }

        function endSummaryPlayback() {
            const slider = document.getElementById('summaryTimeSlider');
            slider.value = slider.max;
            onSummarySliderInput();
        }

        function slowerSummaryPlayback() {
            if (summaryPlaybackSpeedIdx > 0) {
                summaryPlaybackSpeedIdx--;
                updateSummarySpeedLabel();
            }
        }

        function fasterSummaryPlayback() {
            if (summaryPlaybackSpeedIdx < summarySpeeds.length - 1) {
                summaryPlaybackSpeedIdx++;
                updateSummarySpeedLabel();
            }
        }

        function updateSummarySpeedLabel() {
            const label = document.getElementById('summaryPlaybackSpeedLabel');
            if (label) label.textContent = `${summarySpeeds[summaryPlaybackSpeedIdx]}x SPEED`;
        }

        function closeSummaryModal() {
            if (isSummaryPlaying) toggleSummaryPlayback();
            document.getElementById('summaryModal').style.display = 'none';
        }
    