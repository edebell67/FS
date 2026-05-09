// [V20260126_1430] Reusable Live Monitoring Logic
class LiveMonitor {
    constructor(apiEndpoint = 'http://127.0.0.1:5000/api/grid_live', mode = 'live') { // [V20260131_0310] Added mode
        this.apiEndpoint = apiEndpoint;
        this.mode = mode;
        this.currentLeaders = {}; // { groupName: 'leaderKey|metric' }
        this.modelActivations = {}; // [V20260130_1615] Store timestamps PER MODEL: { 'model|product': isoTimestamp }
        this.activeGroups = new Set();
        this.lastEvaluation = {}; // [V20260129_1055] Track timing for re-election (datetime: 2026-01-29 11:00)
        console.log("LiveMonitor initialized.");
    }

    setMode(mode) {
        this.mode = mode;
    }

    _getLocalISO() {
        // [V20260130_1620] Proper Local ISO string for cross-platform sync
        const tzoffset = (new Date()).getTimezoneOffset() * 60000;
        const localISOTime = (new Date(Date.now() - tzoffset)).toISOString().slice(0, -1);
        return localISOTime.split('.')[0];
    }

    /**
     * [V20260204_1650] Determines the source tag based on user requirements.
     * [V20260204_1941] Refined: If groupName is just the product or the strategy key, it's NOT a bucket source.
     */
    _calculateSource(leader, groupName) {
        if (!leader) return 'ui';

        const strategy = leader.model;
        const product = leader.product;
        const metric = leader.metric;
        const key = `${strategy} | ${product}`;
        const keyNoSpaces = key.replace(' | ', '|');

        // 1. Determine if this IS a named bucket or just a default UI card
        const isDefaultGroup = (
            groupName === key ||
            groupName === keyNoSpaces ||
            groupName === product ||
            groupName === product.toUpperCase() ||
            groupName === product.toLowerCase()
        );

        if (!isDefaultGroup) {
            return groupName; // "{trade bucket name}"
        }

        // 2. DNA vs Breakout
        if (strategy.startsWith('DNA_')) {
            const isAlt = metric && (metric.includes('alt') || metric === 'alt_net_return');
            return isAlt ? `frequency_dna_alt_${strategy}` : `frequency_dna_net_${strategy}`;
        } else {
            return `frequency_${strategy}`;
        }
    }

    /**
     * [V20260128_1428] Loads existing state from grid_live.json and restores activeGroups.
     * Should be called after page load and after overlays are rendered.
     * @param {object} groupMap - Map of groupName -> array of overlay configs
     */
    async loadState(groupMap) {
        try {
            const res = await fetch(`${this.apiEndpoint}?mode=${this.mode}`);
            const data = await res.json();
            if (!data.success) {
                console.log("[LiveMonitor] No existing grid_live state to restore.");
                return;
            }
            this.syncState(data.data || [], groupMap);
        } catch (e) {
            console.warn("[LiveMonitor] Failed to load state from grid_live.json:", e);
        }
    }

    /**
     * [V20260130_1635] Syncs internal memory (leaders + activations) from raw server data
     * to prevent redundant activation triggers that overwrite timestamps.
     */
    syncState(gridData, groupMap = null) {
        if (!Array.isArray(gridData)) return;

        const grouped = {};
        gridData.forEach(m => {
            if (!grouped[m.group]) grouped[m.group] = [];
            grouped[m.group].push(m);
        });

        for (const groupName in grouped) {
            // If groupMap provided, only sync if group is in map
            if (groupMap && !groupMap[groupName]) continue;

            this.activeGroups.add(groupName);

            // 1. Sync Leaders (to prevent re-triggering activation update)
            this.currentLeaders[groupName] = JSON.stringify(grouped[groupName].map(m => ({
                model: m.model,
                product: m.product,
                metric: m.metric
            })));

            // 2. Sync Model Activations (the memory of when it started)
            grouped[groupName].forEach(m => {
                const mKey = `${m.model}|${m.product}`;
                if (m.activated_at) this.modelActivations[mKey] = m.activated_at;
            });
            console.log(`[LiveMonitor] Synced state for group: ${groupName}`);
        }
    }

    /**
     * Activates a group with a specific sticky leader.
     * [V20260129_1055] Updated to support periodic re-election (datetime: 2026-01-29 11:00)
     */
    activateGroup(groupName, leader) {
        if (!leader) {
            this.deactivateGroup(groupName);
            return;
        }

        this.activeGroups.add(groupName);
        const signature = JSON.stringify([leader]);

        if (this.currentLeaders[groupName] !== signature) {
            console.log(`[LiveMonitor] Activating sticky leader for '${groupName}':`, leader);

            // [V20260130_1615] Preserve or Create activation timestamp FOR THIS MODEL
            const mKey = `${leader.model}|${leader.product}`;
            const nowIso = this._getLocalISO();
            const actTime = this.modelActivations[mKey] || nowIso;
            this.modelActivations[mKey] = actTime;

            leader.activated_at = actTime; // Attach to payload
            const source = this._calculateSource(leader, groupName);
            this._setLiveMonitoring({ group: groupName, models: [leader], source: source });
            this.currentLeaders[groupName] = signature;
        }
    }

    deactivateGroup(groupName) {
        this.activeGroups.delete(groupName);
        delete this.currentLeaders[groupName];
        // Note: we keep modelActivations in memory in case the model is toggled back on later
        console.log(`[LiveMonitor] Deactivating group '${groupName}'.`);
        this._setLiveMonitoring({ group: groupName, models: [] });
    }

    /**
     * Checks if a group is currently being monitored.
     * @param {string} groupName 
     * @returns {boolean}
     */
    isGroupActive(groupName) {
        return this.activeGroups.has(groupName);
    }

    /**
     * The main update function, called on every data refresh.
     * [V20260129_1055] Periodic Leader Election.
     */
    update(processedSeries, groupMap, globalMetric, startMs, evalMs) {
        if (this.activeGroups.size === 0) return;

        const now = Date.now();
        const throttleInterval = 60000; // 1 minute re-evaluation

        this.activeGroups.forEach(groupName => {
            // Check if it's time to re-evaluate leader
            const lastEval = this.lastEvaluation[groupName] || 0;
            if (now - lastEval < throttleInterval && this.currentLeaders[groupName]) {
                return; // Not time yet
            }

            const overlays = groupMap[groupName];
            if (!overlays || overlays.length === 0) {
                this.deactivateGroup(groupName);
                return;
            }

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
                const signature = JSON.stringify([bestLeader]);
                if (this.currentLeaders[groupName] !== signature) {
                    console.log(`[LiveMonitor] Leader changed for '${groupName}':`, bestLeader);

                    // [V20260130_1615] Preserve original timestamp FOR THIS MODEL
                    const mKey = `${bestLeader.model}|${bestLeader.product}`;
                    const actTime = this.modelActivations[mKey] || this._getLocalISO();
                    this.modelActivations[mKey] = actTime;
                    bestLeader.activated_at = actTime;

                    const source = this._calculateSource(bestLeader, groupName);
                    this._setLiveMonitoring({ group: groupName, models: [bestLeader], source: source });
                    this.currentLeaders[groupName] = signature;
                }
                this.lastEvaluation[groupName] = now;
            }
        });
    }

    /**
     * Sends the API request to the backend to update grid_live.json.
     * @private
     */
    async _setLiveMonitoring(payload) { // [V20260126_1530] New payload-based method
        payload.mode = this.mode; // [V20260131_0310] Inject mode
        if (!payload.source) payload.source = 'ui'; // [V20260204_1650] Use provided source or default 'ui'
        try {
            await fetch(this.apiEndpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            console.log(`[LiveMonitor] Successfully sent update for group: ${payload.group}`);
        } catch (e) {
            console.error(`[LiveMonitor] API call failed for group ${payload.group}:`, e);
        }
    }

    _getFieldNameForMetric(metric) {
        switch (metric) {
            case 'buy_net':
            case 'buy_trades':
                return 'buy_net';
            case 'sell_net':
            case 'sell_trades':
                return 'sell_net';
            case 'net':
            default:
                return 'net';
        }
    }
}

// [V20260126_1430] Export for Node.js testing
module.exports = LiveMonitor;
