
        let currentProductType = 'forex';
        let currentTargetDate = new Date().toISOString().split('T')[0];
        let currentData = null;
        let lastUpdatedTime = null;
        let sortState = { key: 'rank', direction: 'asc' };
        let activations = {};
        let activationsLoaded = false;
        let scalperRatio = 5;
        let revScalperRatio = 2;
        let autoSelectModes = {}; // [2026-04-07 19:40] V20260407_1940 - Scoped by product type
        let autoSelectPermittedTypes = [];
        let vtradePersistenceSeconds = 60;
        let pendingAutoWinner = null;
        let leadershipChangeDetectedAt = null;
        let productTypeByProduct = {};
        let weeklyStateLoaded = false;
        let weeklyDataRequestId = 0;
        const weeklyDataCache = new Map();
        const WEEKLY_STATE_STORAGE_KEY = 'breakout_weekly_performance_state_v1';
        const supportedProductTypes = [
            { key: 'forex', label: 'Forex', icon: 'fas fa-euro-sign' },
            { key: 'indices', label: 'Indices', icon: 'fas fa-chart-line' },
            { key: 'metals', label: 'Metals', icon: 'fas fa-gem' },
            { key: 'crypto', label: 'Crypto', icon: 'fab fa-bitcoin' },
            { key: 'energy', label: 'Energy', icon: 'fas fa-fire' }
        ];

        function formatWeekDisplay(startDate, endDate) {
            return `${startDate} to ${endDate}`;
        }

        function updateAgeDisplay() {
            if (!lastUpdatedTime) return;
            const now = new Date();
            const diffSeconds = Math.floor((now - lastUpdatedTime) / 1000);
            let ageText = diffSeconds < 60 ? `${diffSeconds}s ago` : diffSeconds < 3600 ? `${Math.floor(diffSeconds / 60)}m ${diffSeconds % 60}s ago` : `${Math.floor(diffSeconds / 3600)}h ${Math.floor((diffSeconds % 3600) / 60)}m ago`;
            const ageEl = document.getElementById('last-update-age');
            if (ageEl) ageEl.innerText = `(${ageText})`;
        }

        async function loadActivations() {
            if (activationsLoaded) return activations;
            try {
                const response = await fetch(`/api/activations?mode=live`);
                const data = await response.json();
                if (data.success) {
                    activations = data.activations || {};
                    activationsLoaded = true;
                }
            } catch (error) { console.error('Error loading activations:', error); }
            return activations;
        }

        async function toggleGenStrategy(product, strategy, isChecked, isManual = true) {
            const buyKey = `breakout_${strategy}_buy_net`;
            const sellKey = `breakout_${strategy}_sell_net`;
            const payload = {
                mode: 'live',
                activations: {
                    [buyKey]: { active: isChecked, manual: isManual, auto_promote: isChecked, products: [product] },
                    [sellKey]: { active: isChecked, manual: isManual, auto_promote: isChecked, products: [product] }
                }
            };
            try {
                const response = await fetch('/api/activations', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (result.success) {
                    activations = result.activations || {};
                    activationsLoaded = true;
                    updateAutoSelectStatus();
                    if (currentData) renderTable();
                } else if (isManual) { alert('Failed: ' + result.message); fetchData(); }
            } catch (error) { if (isManual) alert('Error. Check console.'); fetchData(); }
        }

        function isStrategyActive(product, strategy) {
            const b = activations[`breakout_${strategy}_buy_net`];
            const s = activations[`breakout_${strategy}_sell_net`];
            return (b && b.active && (b.products || []).includes(product.toUpperCase())) || (s && s.active && (s.products || []).includes(product.toUpperCase()));
        }

        function getStoredWeeklyState() {
            try {
                const raw = localStorage.getItem(WEEKLY_STATE_STORAGE_KEY);
                if (!raw) return null;
                return JSON.parse(raw);
            } catch (e) {
                return null;
            }
        }

        function storeWeeklyState() {
            try {
                localStorage.setItem(WEEKLY_STATE_STORAGE_KEY, JSON.stringify({
                    auto_select_modes: autoSelectModes,
                    auto_select_permitted_types: autoSelectPermittedTypes
                }));
            } catch (e) { }
        }

        function applyWeeklyStateToUi() {
            const mode = autoSelectModes[currentProductType] || 'None';
            document.getElementById('autoSelectMode').value = mode;
            renderPermittedTypeSelector();
            updateAutoSelectStatus();
        }

        function hydrateWeeklyState(state) {
            if (!state || typeof state !== 'object') return;
            if (state.scalper_ratio) scalperRatio = parseFloat(state.scalper_ratio);
            if (state.rev_scalper_ratio) revScalperRatio = parseFloat(state.rev_scalper_ratio);
            vtradePersistenceSeconds = parseInt(state.vtrade_persistence_seconds || 60);
            autoSelectModes = state.auto_select_modes || {};
            autoSelectPermittedTypes = normalizePermittedTypes(state.auto_select_permitted_types || []);
            productTypeByProduct = normalizeProductTypeMap(state.product_type_by_product || productTypeByProduct || {});
            storeWeeklyState();
            applyWeeklyStateToUi();
        }

        async function loadConfig(force = false) {
            if (!force && weeklyStateLoaded) {
                applyWeeklyStateToUi();
                return;
            }

            if (!force) {
                const stored = getStoredWeeklyState();
                if (stored) {
                    hydrateWeeklyState(stored);
                }
            }

            try {
                const response = await fetch('/api/weekly_performance_state');
                const data = await response.json();
                if (data && data.state) {
                    hydrateWeeklyState(data.state);
                    weeklyStateLoaded = true;
                }
            } catch (e) { }
        }

        async function persistWeeklyState(payload) {
            storeWeeklyState();
            try {
                const response = await fetch('/api/weekly_performance_state', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });
                const result = await response.json();
                if (result && result.state) {
                    hydrateWeeklyState(result.state);
                    weeklyStateLoaded = true;
                }
            } catch (e) { }
        }

        async function handleAutoSelectChange(val) {
            autoSelectModes[currentProductType] = val;
            clearPendingAutoLeader();
            storeWeeklyState();
            applyWeeklyStateToUi();
            await persistWeeklyState({ auto_select_modes: autoSelectModes });
            await evaluateAutoSelect();
        }

        function normalizePermittedTypes(rawTypes) {
            if (!Array.isArray(rawTypes)) return [];
            const normalized = [];
            for (const rawType of rawTypes) {
                const type = String(rawType || '').trim().toLowerCase();
                if (!type || normalized.includes(type)) continue;
                normalized.push(type);
            }
            return normalized;
        }

        function normalizeProductTypeMap(rawMapping) {
            const normalized = {};
            if (!rawMapping || typeof rawMapping !== 'object') return normalized;
            for (const [rawProduct, rawType] of Object.entries(rawMapping)) {
                const product = String(rawProduct || '').trim().toUpperCase();
                const productType = String(rawType || '').trim().toLowerCase();
                if (!product || !productType) continue;
                normalized[product] = productType;
            }
            return normalized;
        }

        function isCurrentProductTypePermitted() {
            return autoSelectPermittedTypes.includes(currentProductType);
        }

        function syncProductTypeMapFromCurrentData() {
            if (!Array.isArray(currentData?.top_strategies)) return;
            for (const item of currentData.top_strategies) {
                const product = String(item.product || '').trim().toUpperCase();
                const productType = String(item.product_type || currentProductType || '').trim().toLowerCase();
                if (!product || !productType) continue;
                productTypeByProduct[product] = productType;
            }
        }

        function resolveProductTypeForProduct(product, fallbackProductType = null) {
            const productKey = String(product || '').trim().toUpperCase();
            if (productTypeByProduct[productKey]) return productTypeByProduct[productKey];
            const fallback = String(fallbackProductType || '').trim().toLowerCase();
            return fallback || null;
        }

        function renderPermittedTypeSelector() {
            const container = document.getElementById('autoSelectPermittedTypes');
            if (!container) return;
            container.innerHTML = '';
            for (const type of supportedProductTypes) {
                const label = document.createElement('label');
                label.className = `permit-chip${autoSelectPermittedTypes.includes(type.key) ? ' active' : ''}`;
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.checked = autoSelectPermittedTypes.includes(type.key);
                input.addEventListener('change', () => handlePermittedTypeToggle(type.key, input.checked));
                const icon = document.createElement('i');
                icon.className = type.icon;
                const text = document.createElement('span');
                text.textContent = type.label;
                label.appendChild(input);
                label.appendChild(icon);
                label.appendChild(text);
                container.appendChild(label);
            }
        }

        async function handlePermittedTypeToggle(productType, isChecked) {
            const next = new Set(autoSelectPermittedTypes);
            if (isChecked) next.add(productType);
            else next.delete(productType);
            autoSelectPermittedTypes = Array.from(next);
            clearPendingAutoLeader();
            storeWeeklyState();
            applyWeeklyStateToUi();
            await persistWeeklyState({ auto_select_permitted_types: autoSelectPermittedTypes });
            await evaluateAutoSelect();
        }

        function normalizeLeaderCandidate(item) {
            if (!item || !item.product || !item.strategy_name_parm) return null;
            return {
                product: String(item.product).toUpperCase(),
                strategy: item.strategy_name_parm,
                genStrategyName: item.gen_strategy_name || '',
                totalNet: Number(item.total_net || 0),
                productType: item.product_type || currentProductType
            };
        }

        function sameLeader(a, b) {
            if (!a || !b) return false;
            return String(a.product || '').toUpperCase() === String(b.product || '').toUpperCase()
                && String(a.strategy || '') === String(b.strategy || '');
        }

        function getCurrentAutoLeadersForScope(productType) {
            const leaders = [];
            const seen = new Set();
            for (const [key, entry] of Object.entries(activations)) {
                if (entry.active && entry.manual === false && entry.auto_promote === true) {
                    const prod = String((entry.products || [])[0] || '').toUpperCase();
                    const resolvedProductType = resolveProductTypeForProduct(prod, currentProductType);
                    if (resolvedProductType !== productType) continue;

                    const stratMatch = key.match(/^breakout_(.*)_(buy|sell)_net$/);
                    if (!stratMatch || !prod) continue;
                    const dedupeKey = `${prod}|${stratMatch[1]}`;
                    if (seen.has(dedupeKey)) continue;
                    seen.add(dedupeKey);
                    leaders.push({ product: prod, strategy: stratMatch[1], productType: resolvedProductType });
                }
            }
            return leaders;
        }

        function formatLeaderLabel(leader) {
            if (!leader) return 'No active leader';
            return `${leader.product} | ${leader.strategy}`;
        }

        function clearPendingAutoLeader() {
            pendingAutoWinner = null;
            leadershipChangeDetectedAt = null;
        }

        function logAutoSelectEvent(message, details = null) {
            const scope = `[auto-select:${currentProductType}]`;
            if (details) { console.log(`${scope} ${message}`, details); return; }
            console.log(`${scope} ${message}`);
        }

        function getPendingAutoLeaderRemainingSeconds() {
            if (!pendingAutoWinner || leadershipChangeDetectedAt === null) return 0;
            const elapsedMs = Date.now() - leadershipChangeDetectedAt;
            const remainingMs = Math.max(0, (vtradePersistenceSeconds * 1000) - elapsedMs);
            return Math.ceil(remainingMs / 1000);
        }

        function updateAutoSelectStatus() {
            const statusEl = document.getElementById('autoSelectStatus');
            if (!statusEl) return;
            const mode = autoSelectModes[currentProductType] || 'None';
            if (mode === 'None') {
                statusEl.dataset.state = 'idle';
                statusEl.innerText = `Auto-select disabled for ${currentProductType}.`;
                return;
            }

            if (!isCurrentProductTypePermitted()) {
                statusEl.dataset.state = 'idle';
                statusEl.innerText = `Auto-select blocked for ${currentProductType}. Select this product type in Permitted Product Types.`;
                return;
            }

            if (pendingAutoWinner && leadershipChangeDetectedAt !== null) {
                const remaining = getPendingAutoLeaderRemainingSeconds();
                statusEl.dataset.state = 'pending';
                statusEl.innerText = `Pending leader ${formatLeaderLabel(pendingAutoWinner)}. Switching in ${remaining}s...`;      
                return;
            }

            const activeLeader = getCurrentAutoLeadersForScope(currentProductType)[0];
            if (activeLeader) {
                statusEl.dataset.state = 'active';
                statusEl.innerText = `Active leader ${formatLeaderLabel(activeLeader)}. Delay ${vtradePersistenceSeconds}s.`;
                return;
            }

            statusEl.dataset.state = 'idle';
            statusEl.innerText = `Waiting for a positive ${currentProductType} leader.`;
        }

        async function applyAutoLeaderSelection(topCandidate, scopedAutoLeaders) {
            // Only deactivate auto-leaders in the CURRENT scope
            for (const old of scopedAutoLeaders) {
                if (!topCandidate || !sameLeader(old, topCandidate)) {
                    await toggleGenStrategy(old.product, old.strategy, false, false);
                }
            }

            if (topCandidate && !scopedAutoLeaders.some(old => sameLeader(old, topCandidate))) {
                await toggleGenStrategy(topCandidate.product, topCandidate.strategy, true, false);
            }

            clearPendingAutoLeader();
            logAutoSelectEvent('applied leader selection', {
                activeLeader: topCandidate ? formatLeaderLabel(topCandidate) : 'none',
                deactivatedLeaders: scopedAutoLeaders
                    .filter(old => !topCandidate || !sameLeader(old, topCandidate))
                    .map(formatLeaderLabel)
            });
            updateAutoSelectStatus();
            if (currentData) renderTable();
        }

        async function evaluateAutoSelect() {
            const mode = autoSelectModes[currentProductType] || 'None';
            if (!currentData || !currentData.top_strategies) {
                clearPendingAutoLeader();
                updateAutoSelectStatus();
                return;
            }

            syncProductTypeMapFromCurrentData();
            const scopedAutoLeaders = getCurrentAutoLeadersForScope(currentProductType);
            if (mode === 'None') {
                clearPendingAutoLeader();
                if (scopedAutoLeaders.length > 0) {
                    logAutoSelectEvent('mode disabled for scope, clearing scoped auto-leaders');
                    await applyAutoLeaderSelection(null, scopedAutoLeaders);
                    return;
                }
                updateAutoSelectStatus();
                return;
            }
            if (!isCurrentProductTypePermitted()) {
                clearPendingAutoLeader();
                if (scopedAutoLeaders.length > 0) {
                    logAutoSelectEvent('current product type is not permitted, clearing scoped auto-leaders');
                    await applyAutoLeaderSelection(null, scopedAutoLeaders);
                    return;
                }
                updateAutoSelectStatus();
                return;
            }
            const currentAutoLeader = scopedAutoLeaders[0] || null;
            let topCandidate = null;
            for (const item of currentData.top_strategies) {
                if (Number(item.total_net) <= 0) continue;
                if (resolveProductTypeForProduct(item.product, item.product_type || currentProductType) !== currentProductType) continue;
                
                // [2026-04-07 19:30] V20260407_1930 - Respect Manual Rejection
                const bKey = `breakout_${item.strategy_name_parm}_buy_net`;
                const sKey = `breakout_${item.strategy_name_parm}_sell_net`;
                const bE = activations[bKey], sE = activations[sKey];
                if ((bE && bE.manual && !bE.active) || (sE && sE.manual && !sE.active)) continue;

                const style = classifyStrategyStyle(item.strategy_name_parm);
                const match = mode === 'All'
                    || (mode === 'Scalper' && style.isScalper)
                    || (mode === 'Rev_scalper' && style.isRevScalper);
                if (match) {
                    topCandidate = normalizeLeaderCandidate(item);
                    break;
                }
            }

            if (!topCandidate) {
                if (scopedAutoLeaders.length > 0) {
                    logAutoSelectEvent('no candidate remains in scope, clearing auto-pilot');
                    await applyAutoLeaderSelection(null, scopedAutoLeaders);
                }
                return;
            }

            if (!currentAutoLeader) {
                logAutoSelectEvent('activating first auto-leader immediately', { leader: formatLeaderLabel(topCandidate) });
                await applyAutoLeaderSelection(topCandidate, scopedAutoLeaders);
                return;
            }

            if (sameLeader(currentAutoLeader, topCandidate)) {
                clearPendingAutoLeader();
                if (scopedAutoLeaders.length > 1) {
                    await applyAutoLeaderSelection(topCandidate, scopedAutoLeaders);
                } else {
                    updateAutoSelectStatus();
                }
                return;
            }

            if (!sameLeader(pendingAutoWinner, topCandidate)) {
                pendingAutoWinner = topCandidate;
                leadershipChangeDetectedAt = Date.now();
                updateAutoSelectStatus();
                return;
            }

            if (getPendingAutoLeaderRemainingSeconds() > 0) {
                updateAutoSelectStatus();
                return;
            }

            logAutoSelectEvent('switching active leader after delay');
            await applyAutoLeaderSelection(topCandidate, scopedAutoLeaders);
        }

        function classifyStrategyStyle(rawStrategy) {
            const raw = String(rawStrategy || '').toLowerCase();
            const tpMatch = raw.match(/tp([\d.]+)/), slMatch = raw.match(/sl([\d.]+)/);
            if (!tpMatch || !slMatch) return { cellClass: '', isScalper: false, isRevScalper: false };
            const tp = parseFloat(tpMatch[1]), sl = parseFloat(slMatch[1]);
            const isS = tp > 0 && sl >= tp * scalperRatio, isR = sl > 0 && tp >= sl * revScalperRatio;
            return { cellClass: isS ? 'scalper' : isR ? 'rev-scalper' : '', isScalper: isS, isRevScalper: isR };
        }

        function escapeHtml(value) {
            return String(value ?? '')
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#39;');
        }

        function formatNetValue(value) {
            const numeric = Number(value || 0);
            const cssClass = numeric > 0 ? 'pos' : numeric < 0 ? 'neg' : 'neutral';
            return `<span class="net-val ${cssClass}">${numeric.toFixed(2)}</span>`;
        }

        function compareValues(left, right, numeric = false) {
            if (numeric) {
                return Number(left || 0) - Number(right || 0);
            }
            return String(left ?? '').localeCompare(String(right ?? ''), undefined, { sensitivity: 'base' });
        }

        function setSort(key) {
            if (sortState.key === key) {
                sortState.direction = sortState.direction === 'asc' ? 'desc' : 'asc';
            } else {
                sortState.key = key;
                sortState.direction = key === 'rank' ? 'asc' : 'desc';
            }
            if (currentData) renderTable();
        }

        function createHeaderCell(label, key, numeric = false) {
            const th = document.createElement('th');
            const button = document.createElement('button');
            button.className = `sort-btn${sortState.key === key ? ' active' : ''}`;
            button.type = 'button';
            button.addEventListener('click', () => setSort(key));

            const labelSpan = document.createElement('span');
            labelSpan.className = 'sort-label';
            labelSpan.textContent = label;
            button.appendChild(labelSpan);

            const indicator = document.createElement('span');
            indicator.className = 'sort-indicator';
            indicator.textContent = sortState.key === key ? (sortState.direction === 'asc' ? '▲' : '▼') : '';
            button.appendChild(indicator);

            if (numeric) {
                button.style.justifyContent = 'flex-end';
            }

            th.appendChild(button);
            return th;
        }

        function createStaticHeaderCell(label, className = '') {
            const th = document.createElement('th');
            if (className) th.className = className;
            th.textContent = label;
            if (className.includes('col-live-trade') || className.includes('col-chart')) {
                th.style.textAlign = 'center';
            }
            return th;
        }

        function getSortedStrategies() {
            const rows = Array.isArray(currentData?.top_strategies) ? [...currentData.top_strategies] : [];
            const dateLabels = currentData?.date_labels
                ? Object.keys(currentData.date_labels)
                : rows[0]?.daily
                    ? Object.keys(rows[0].daily)
                    : (currentData?.date_range || []);
            const keyedRows = rows.map((row, index) => ({ ...row, __rank: index + 1 }));

            keyedRows.sort((a, b) => {
                let comparison = 0;
                const key = sortState.key;

                if (key === 'rank') {
                    comparison = compareValues(a.__rank, b.__rank, true);
                } else if (key === 'strategy_label') {
                    comparison = compareValues(a.strategy_label, b.strategy_label);
                } else if (key === 'gen_strategy_name') {
                    comparison = compareValues(a.gen_strategy_name, b.gen_strategy_name);
                } else if (key === 'total') {
                    comparison = compareValues(a.total_net, b.total_net, true);
                } else if (key === 'trades') {
                    comparison = compareValues(a.total_trades, b.total_trades, true);
                } else if (key.startsWith('date:')) {
                    const dateKey = key.slice(5);
                    comparison = compareValues(a.daily?.[dateKey], b.daily?.[dateKey], true);
                }

                if (comparison === 0) {
                    comparison = compareValues(a.__rank, b.__rank, true);
                }
                return sortState.direction === 'asc' ? comparison : -comparison;
            });

            return { rows: keyedRows, dateLabels };
        }

        function renderTable() {
            const headerRow = document.getElementById('table-header');
            const body = document.getElementById('performance-body');
            if (!headerRow || !body) return;
            const dateLabels = currentData?.date_labels || {};

            headerRow.innerHTML = '';
            headerRow.appendChild(Object.assign(createHeaderCell('#', 'rank'), { className: 'col-rank' }));
            headerRow.appendChild(Object.assign(createHeaderCell('Product | Strategy', 'strategy_label'), { className: 'col-strategy' }));
            headerRow.appendChild(createStaticHeaderCell('Live Trade', 'col-live-trade'));
            headerRow.appendChild(createStaticHeaderCell('Chart', 'col-chart'));

            const { rows, dateLabels: dateKeys } = getSortedStrategies();
            dateKeys.forEach(d => {
                headerRow.appendChild(Object.assign(createHeaderCell(dateLabels[d] || d.substring(5), `date:${d}`, true), { className: 'col-day' }));
            });
            headerRow.appendChild(Object.assign(createHeaderCell('Total', 'total', true), { className: 'col-total' }));
            headerRow.appendChild(Object.assign(createHeaderCell('Trades', 'trades', true), { className: 'col-trades' }));

            body.innerHTML = '';
            rows.forEach((item, index) => {
                const tr = document.createElement('tr');
                const style = classifyStrategyStyle(item.strategy_name_parm);
                const isActive = isStrategyActive(item.product, item.strategy_name_parm);
                const safeStrategyLabel = escapeHtml(item.strategy_label);
                const product = String(item.product || '');
                const strategyParm = String(item.strategy_name_parm || '');

                tr.innerHTML = `
                    <td class="col-rank">${index + 1}</td>
                    <td class="strategy-cell col-strategy ${style.cellClass}">${safeStrategyLabel}</td>
                `;

                const toggleCell = document.createElement('td');
                toggleCell.className = 'gen-strategy-cell col-live-trade';
                const toggleContainer = document.createElement('div');
                toggleContainer.className = 'gen-strategy-container';
                const toggleLabel = document.createElement('label');
                toggleLabel.className = 'switch';
                toggleLabel.title = `Toggle auto-promotion for ${product} | ${strategyParm}`;
                const toggleInput = document.createElement('input');
                toggleInput.type = 'checkbox';
                toggleInput.checked = isActive;
                toggleInput.addEventListener('change', () => toggleGenStrategy(product, strategyParm, toggleInput.checked, true));
                const slider = document.createElement('span');
                slider.className = 'slider';
                toggleLabel.appendChild(toggleInput);
                toggleLabel.appendChild(slider);
                toggleContainer.appendChild(toggleLabel);
                toggleCell.appendChild(toggleContainer);
                tr.appendChild(toggleCell);

                const chartCell = document.createElement('td');
                chartCell.className = 'col-chart chart-action-cell';
                const chartButton = document.createElement('button');
                chartButton.className = 'pag-btn';
                chartButton.type = 'button';
                chartButton.title = 'Open chart';
                chartButton.innerHTML = '<i class="fas fa-chart-area"></i>';
                chartButton.addEventListener('click', () => sendSingleRowToMultiChart(strategyParm, product));
                chartCell.appendChild(chartButton);
                tr.appendChild(chartCell);

                dateKeys.forEach(d => {
                    const td = document.createElement('td');
                    td.className = 'col-day';
                    td.innerHTML = formatNetValue(item.daily?.[d] || 0);
                    tr.appendChild(td);
                });

                const totalCell = document.createElement('td');
                totalCell.className = 'col-total';
                totalCell.innerHTML = formatNetValue(item.total_net || 0);
                tr.appendChild(totalCell);

                const tradesCell = document.createElement('td');
                tradesCell.className = 'col-trades';
                tradesCell.innerHTML = `<span class="trades-badge">${Number(item.total_trades || 0)}</span>`;
                tr.appendChild(tradesCell);

                body.appendChild(tr);
            });
        }

        function getWeeklyCacheKey() {
            return `${currentProductType}|${currentTargetDate}`;
        }

        async function fetchData(options = {}) {
            const {
                refreshState = false,
                refreshActivations = false,
                useCache = true
            } = options;
            const requestId = ++weeklyDataRequestId;
            const cacheKey = getWeeklyCacheKey();
            showLoading(true);
            try {
                if (refreshActivations || !activationsLoaded) {
                    await loadActivations();
                }
                await loadConfig(refreshState);

                let data = null;
                if (useCache && weeklyDataCache.has(cacheKey)) {
                    data = weeklyDataCache.get(cacheKey);
                } else {
                    const response = await fetch(`/api/weekly_performance?product_type=${currentProductType}&target_date=${currentTargetDate}`);
                    data = await response.json();
                    if (!data.error) {
                        weeklyDataCache.set(cacheKey, data);
                    }
                }

                if (requestId !== weeklyDataRequestId) return;
                if (data.error) { alert(data.error); return; }
                currentData = data;
                currentTargetDate = data.week_start || currentTargetDate;
                lastUpdatedTime = new Date();
                syncProductTypeMapFromCurrentData();
                const timeEl = document.getElementById('last-update-time');
                if (timeEl) timeEl.innerText = lastUpdatedTime.toLocaleTimeString();
                updateAgeDisplay();

                await evaluateAutoSelect(); 
                renderTable();
                updateDisplay();
            } catch (err) { console.error("Fetch error:", err); }
            finally { showLoading(false); }
        }

        function updateDisplay() {
            const range = currentData.date_range;
            document.getElementById('week-display').innerText = formatWeekDisplay(range[0], range[1]);
            document.querySelectorAll('.filter-btn').forEach(btn => {
                const id = btn.id.replace('btn-', '');
                if (id === currentProductType) btn.classList.add('active');
                else btn.classList.remove('active');
            });
        }

        function setProductType(type) { 
            currentProductType = type; 
            clearPendingAutoLeader();
            applyWeeklyStateToUi();
            fetchData(); 
        }

        function changeWeek(dir) {
            const d = new Date(currentData?.week_start || currentTargetDate);
            d.setDate(d.getDate() + (dir * 7));
            currentTargetDate = d.toISOString().split('T')[0];
            fetchData();
        }
        function showLoading(s) { document.getElementById('loading').style.display = s ? 'flex' : 'none'; }
        function buildModelName(b, p) { return p ? `${b}_${p}` : b; }
        function sendSingleRowToMultiChart(s, p) { sendSummarySelectionToMultiChart([{ strategy: s, product: p }], `${s} | ${p}`); }

        function sendSummarySelectionToMultiChart(items, label = "Summary", preferredMetric = "net") {
            const dedup = []; const seen = new Set();
            for (const it of items) {
                const bS = String(it.strategy || "").trim(), p = String(it.product || "").trim(), pR = String(it.params || "").trim();
                if (!bS || !p) continue;
                const strategy = (pR && !bS.includes("_tp") && !bS.endsWith(`_${pR}`)) ? buildModelName(bS, pR) : bS;
                const key = `${strategy}|${p}`;
                if (seen.has(key)) continue; seen.add(key);
                dedup.push({ strategy, product: p, group: `${strategy} | ${p}`, parm_raw: pR });
            }
            if (!dedup.length) { alert("No valid items."); return; }
            localStorage.setItem("multi_chart_import_payload", JSON.stringify({
                created_at: new Date().toISOString(), mode: "live", date: currentTargetDate, source: "weekly_performance", label, preferred_metric: preferredMetric, append: true, items: dedup
            }));
            const bc = new BroadcastChannel("multi_chart_channel");
            let resp = false;
            bc.onmessage = (e) => { if (e.data === "PONG") { resp = true; bc.postMessage("IMPORT"); } };
            bc.postMessage("PING");
            setTimeout(() => { if (!resp) window.open("multi_chart.html?import=1", "_blank"); }, 300);
        }

        window.addEventListener('DOMContentLoaded', () => {
            fetchData();
            setInterval(() => {
                updateAgeDisplay();
                updateAutoSelectStatus();
                if (pendingAutoWinner && currentData && autoSelectModes[currentProductType] !== 'None' && getPendingAutoLeaderRemainingSeconds() <= 0) {
                    evaluateAutoSelect();
                }
            }, 1000);
        });
    