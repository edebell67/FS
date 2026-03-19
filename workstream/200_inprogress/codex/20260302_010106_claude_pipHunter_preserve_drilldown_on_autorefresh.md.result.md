OpenAI Codex v0.115.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d06f1-8c3e-7c40-b41b-fc43e217ac11
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m loading the workstream lifecycle skill and the assigned task file first, then I’ll inspect the relevant code paths and carry the task through implementation, validation, and lifecycle updates.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md'" in C:\Users\edebe\eds succeeded in 1.54s:
---
name: workstream-task-lifecycle
description: Create and maintain timestamped task documentation files in the workstream lifecycle folders (`workstream/000_epic`, `workstream/100_backlog`, `workstream/200_inprogress`, `workstream/300_complete`). Use when a user asks to document changes, track progress for a distinct task, or enforce file movement across backlog/in-progress/complete states.
---

# Workstream Task Lifecycle

Execute this workflow whenever a distinct task needs a documented trail.

## Folder Structure
```
workstream/
├── 000_epic/        ← High-level specs, PRDs, strategic documents
│                      Source material for task decomposition
│                      Items remain here permanently as reference
│
├── 100_backlog/     ← Atomic tasks decomposed from epics
│                      Ready to be picked up
│
├── 200_inprogress/  ← Currently active work
 succeeded in 1.74s:
# Preserve Drilldown State on Auto-Refresh

**Source**: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- **Auto-refresh interval**: 30 seconds (line 1173)

## Problem Description
1. User expands a strategy to view trade drilldown
2. Auto-refresh triggers after 30 seconds
3. Drilldown collapses/closes
4. User must re-click to expand again
5. Poor UX - interrupts analysis workflow

## Root Cause (Likely)
codex
I have the lifecycle rules and the current task file. Next I’m inspecting the dashboard component and the worktree so I can implement the refresh-state fix without trampling any unrelated edits, then I’ll normalize the task file to the required lifecycle format as evidence accumulates.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx' | Select-Object -First 1400" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"selectedId|strategyTrades|loadData|setSelectedId|setStrategyTrades|setInterval|selectedDate|handle.*Trade|fetch.*trade|strategy.*trades\" 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx'" in C:\Users\edebe\eds succeeded in 4.78s:
M  DataInsights/src/Constants.py
 M TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
R  workstream/000_backlog/.keep -> workstream/000_epic/.keep
RD "workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md" -> "workstream/000_epic/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md"
RD workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md -> workstream/000_epic/20260225_104010_live_market_data_pipeline_prompt.md
RD workstream/000_backlog/20260227_022357_sFX_Technical_Design_Brief_v2.md -> workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
AD workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
AD workstream/000_epic/20260313_165611_bizPA_epic.md
AD "workstream/000_epic/20260313_165611_unassigned_Autonomous Trading Signal Platform.md"
AD workstream/000_epic/20260313_165611_unassigned_bizPA.md
A  workstream/000_epic/bizPA_disccussion.txt
R  workstream/000_backlog/claude/.keep -> workstream/000_epic/claude/.keep
A  workstream/000_epic/claude/20260305_100142_claude_etrmui_etrui_processed.md
R  workstream/000_backlog/codex/.keep -> workstream/000_epic/codex/.keep
R  workstream/000_backlog/codex/20260303_152309_codex_afrix_build_prompt_processed.md -> workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_processed.md
A  workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_review.md
R  workstream/000_backlog/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md -> workstream/000_epic/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
R  workstream/000_backlog/codex/20260304_142350_codex_linkage_verification_processed.md -> workstream/000_epic/codex/20260304_142350_codex_linkage_verification_processed.md
 succeeded in 5.83s:
import { useState, useEffect, useCallback, useRef } from "react";
import { fetchTop20, fetchMarketBias, fetchLiveTrades, fetchSummaryNet } from "./src/api/dataService.js";

// Inline fetchStrategyTrades to avoid import issue
const fetchStrategyTrades = async (strategy, product = null, date = null) => {
  const useDate = date || new Date().toISOString().split('T')[0];
  const baseUrl = 'http://192.168.1.110:5050/api';
  let endpoint = `${baseUrl}/strategy-trades?strategy=${encodeURIComponent(strategy)}&date=${useDate}&mode=live`;
  if (product) endpoint += `&product=${encodeURIComponent(product)}`;
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000);
    const response = await fetch(endpoint, { signal: controller.signal });
    clearTimeout(timeoutId);
    if (!response.ok) return null;
    const data = await response.json();
    return {
      trades: data.trades.map(t => ({
        tradeId: t.trade_id, product: t.product, direction: t.direction, strategy: t.strategy,
        entryTime: t.entry_time, exitTime: t.exit_time, pnlPips: t.pnl_pips, netReturn: t.net_return,
 succeeded in 8.02s:
8:  let endpoint = `${baseUrl}/strategy-trades?strategy=${encodeURIComponent(strategy)}&date=${useDate}&mode=live`;
197:    if(openCount > 8) alerts.push({id:`op-${s.id}`,level:"warning",strategy:s.name,msg:`${openCount} open trades — high concurrent exposure`,stratId:s.id});
1092:  const [selectedId,setSelectedId]=useState(null);
1097:  const [strategyTrades, setStrategyTrades] = useState([]);  // All trades (open + closed) for selected strategy
1100:  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
1132:    const loadData = async () => {
1135:        setSelectedId(null); // Reset selection when date changes
1136:        setStrategyTrades([]);
1139:            fetchTop20(selectedDate),
1140:            fetchMarketBias(selectedDate),
1141:            fetchLiveTrades(selectedDate),
1142:            fetchSummaryNet(selectedDate)
1170:    loadData();
1173:    const refreshInterval = setInterval(loadData, 30000);
1175:  }, [selectedDate]);
1177:  useEffect(()=>{const iv=setInterval(()=>setTick(new Date()),8000);return()=>clearInterval(iv);},[]);
1185:      if (!selectedId || DATA_MODE !== 'live') {
1186:        setStrategyTrades([]);
1190:      const sel = activeStrategies.find(s => s.id === selectedId);
1192:        setStrategyTrades([]);
codex
I’ve confirmed the current behavior: `loadData` clears `selectedId` and `strategyTrades` on every 30-second poll, and the drilldown fetch only reruns when selection/date change, not when the main refresh completes. I’m patching the component to separate date-change resets from interval refreshes, add a refresh signal for selected strategy trades, and guard the case where the selected strategy disappears after refresh.
Plan update
Implement the dashboard refresh fix first, then run technical validation, then update the lifecycle file with ordered checklist evidence and current completion state.
  → Patch the dashboard component so auto-refresh preserves the selected drilldown while date changes still reset it.
  • Run validation commands against the modified dashboard code and inspect the diff/output.
  • Update the lifecycle task file with required plan/evidence/validation entries and current status.
file update
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx
@@ -1101,2 +1101,5 @@
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
@@ -1129,2 +1132,6 @@
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
@@ -1134,4 +1141,9 @@
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
@@ -1149,2 +1161,7 @@
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
@@ -1162,2 +1179,4 @@
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
@@ -1227,4 +1246,3 @@
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
apply_patch(auto_approved=true) exited 0 in 584ms:
Success. Updated the following files:
M C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\forex-dashboard_1.jsx
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The component patch is in. I’m validating the updated file next so I can capture concrete proof for the lifecycle record, then I’ll bring the task document up to the required checklist/evidence format with the actual command outputs.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx' | Select-String -Pattern 'previousSelectedDateRef|selectedIdRef|strategyTradesRefreshKey|dateChanged|transformed.some|loadStrategyTrades' -Context 2,3" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'TradeApps/breakout/piphunter/landing_page'" in C:\Users\edebe\eds succeeded in 1.85s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          27/02/2026    22:25                [44;1m.venv[0m
d----          01/03/2026    22:22                [44;1mnode_modules[0m
d----          04/03/2026    17:10                [44;1msocial[0m
d----          27/02/2026    22:18                [44;1msrc[0m
d----          04/03/2026    17:02                [44;1mvenv[0m
-a---          27/02/2026    20:27             40 .gitignore
-a---          19/03/2026    16:34          92514 forex-dashboard_1.jsx
-a---          27/02/2026    16:52          71797 forex-dashboard.jsx
-a---          27/02/2026    20:27            945 index.html
-a---          27/02/2026    20:27            257 main.jsx
-a---          01/03/2026    22:22          54975 package-lock.json
-a---          27/02/2026    20:27            425 package.json
-a---          04/03/2026    17:08           5793 [32;1mrun_social.py[0m
-a---          02/03/2026    03:37          16139 [32;1mserver.py[0m
-a---          01/03/2026    20:48            376 [32;1mvite.config.js[0m
 succeeded in 1.96s:

    const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
    const drillRef=useRef(null);
>   const [7mpreviousSelectedDateRef[0m = useRef(selectedDate);[0m
>   const [7mselectedIdRef[0m = useRef(selectedId);
>   const [[7mstrategyTradesRefreshKey[0m, setStrategyTradesRefreshKey] = useState(0);[0m
[7m[0m  [0m
[7m[0m    // Theme colors[0m
[7m[0m    const themes = {[0m
  
    useEffect(() => {
>     [7mselectedIdRef[0m.current = selectedId;[0m
[7m[0m    }, [selectedId]);[0m
[7m[0m  [0m
[7m[0m    // Fetch live data on mount and when date changes[0m
        if (DATA_MODE === 'live') {
          setIsLoading(true);
>         const [7mdateChanged[0m = previousSelectedDateRef.current !== selectedDate;[0m
>         [7mpreviousSelectedDateRef[0m.current = selectedDate;[0m
[7m[0m  [0m
 succeeded in 2.07s:

file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'TradeApps/breakout/piphunter/landing_page/package.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'TradeApps/breakout/piphunter/landing_page/node_modules/.bin'" in C:\Users\edebe\eds succeeded in 1.26s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\.bin

[32;1mMode   [0m[32;1m              LastWriteTime[0m[32;1m         Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
la---          27/02/2026    20:39              0 [36;1mbaseline-browser-mapping[0m -> 
la---          27/02/2026    20:39              0 [36;1mbrowserslist[0m -> 
la---          27/02/2026    20:39              0 [36;1mesbuild[0m -> 
la---          27/02/2026    20:39              0 [36;1mjsesc[0m -> 
la---          27/02/2026    20:39              0 [36;1mjson5[0m -> 
la---          27/02/2026    20:39              0 [36;1mloose-envify[0m -> 
la---          27/02/2026    20:39              0 [36;1mnanoid[0m -> 
la---          27/02/2026    20:39              0 [36;1mparser[0m -> 
la---          27/02/2026    20:39              0 [36;1mrollup[0m -> 
la---          27/02/2026    20:39              0 [36;1msemver[0m -> 
la---          27/02/2026    20:39              0 [36;1mupdate-browserslist-db[0m -> 
la---          27/02/2026    20:39              0 [36;1mvite[0m -> 

 succeeded in 1.25s:
{
  "name": "piphunter-landing",
  "version": "1.0.0",
  "description": "Landing page for PipHunter/Breakout FS trading app",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.1.0"
  }
}
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The package has a local Vite build available, so I’m using that as the technical gate for this change. After that I’ll rewrite the task file into the required lifecycle structure and capture the exact evidence from the diff and build output.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff --stat -- 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'npm run build' in C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page succeeded in 1.97s:

 exited 1 in 4.09s:

> piphunter-landing@1.0.0 build
> vite build

'vite' is not recognized as an internal or external command,
operable program or batch file.
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The first validation attempt failed because the local `vite` shim isn’t executable in this environment even though dependencies are present. I’m switching to the direct Node entrypoint so we still get a real build signal and can record the environment-specific failure plus the successful fallback in the task file.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "node .\\node_modules\\vite\\bin\\vite.js build" in C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_pageexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\landing_page\\node_modules\\vite\\bin'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx' | Select-Object -First 220" in C:\Users\edebe\eds succeeded in 3.07s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\vite\bin

[32;1mMode   [0m[32;1m              LastWriteTime[0m[32;1m         Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
-a---          27/02/2026    20:38           2691 openChrome.applescript
-a---          27/02/2026    20:39           1670 [32;1mvite.js[0m

 exited 1 in 4.03s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\rollup\dist\native.js:115
		throw new Error(
		      ^

Error: Cannot find module @rollup/rollup-win32-x64-msvc. npm has a bug related to optional dependencies (https://github.com/npm/cli/issues/4828). Please try `npm i` again after removing both package-lock.json and node_modules directory.
    at requireWithFriendlyError (C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\rollup\dist\native.js:115:9)
    at Object.<anonymous> (C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\rollup\dist\native.js:124:76)
    at Module._compile (node:internal/modules/cjs/loader:1554:14)
    at Object..js (node:internal/modules/cjs/loader:1706:10)
    at Module.load (node:internal/modules/cjs/loader:1289:32)
    at Function._load (node:internal/modules/cjs/loader:1108:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:220:24)
    at cjsLoader (node:internal/modules/esm/translators:262:5)
    at ModuleWrap.<anonymous> (node:internal/modules/esm/translators:196:7) {
  [cause]: Error: Cannot find module '@rollup/rollup-win32-x64-msvc'
  Require stack:
  - C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\rollup\dist\native.js
      at Function._resolveFilename (node:internal/modules/cjs/loader:1225:15)
      at Function._load (node:internal/modules/cjs/loader:1055:27)
 succeeded in 4.00s:

file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The Rollup native optional package is missing from `node_modules`, so the normal Vite build path is blocked by the environment rather than by this patch. I’m adding a syntax-level fallback validation with the installed `esbuild` binary so we still have a concrete code check for the modified JSX file.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\landing_page\\node_modules\\esbuild' -Recurse -Depth 2" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "node .\\node_modules\\esbuild\\bin\\esbuild 'forex-dashboard_1.jsx' --bundle --format=esm --outfile='dist\\validation-forex-dashboard_1.js'" in C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page succeeded in 9.02s:

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\esbuild

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          27/02/2026    20:39                [44;1mbin[0m
d----          27/02/2026    20:38                [44;1mlib[0m
-a---          27/02/2026    20:38          10943 [32;1minstall.js[0m
-a---          27/02/2026    20:38           1069 LICENSE.md
-a---          27/02/2026    20:38           1340 package.json
-a---          27/02/2026    20:38            175 README.md

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\esbuild\bin

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
-a---          27/02/2026    20:39        9707520 esbuild

    Directory: C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\esbuild\lib

 exited 1 in 9.03s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\esbuild\bin\esbuild:1
ELF
^

SyntaxError: Invalid or unexpected token
    at wrapSafe (node:internal/modules/cjs/loader:1486:18)
    at Module._compile (node:internal/modules/cjs/loader:1528:20)
    at Object..js (node:internal/modules/cjs/loader:1706:10)
    at Module.load (node:internal/modules/cjs/loader:1289:32)
    at Function._load (node:internal/modules/cjs/loader:1108:12)
    at TracingChannel.traceSync (node:diagnostics_channel:322:14)
    at wrapModuleLoad (node:internal/modules/cjs/loader:220:24)
    at Function.executeUserEntryPoint [as runMain] (node:internal/modules/run_main:170:5)
    at node:internal/main/run_main_module:36:49

Node.js v22.14.0
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The packaged `esbuild` binary in this checkout is also the wrong platform build, so I’m falling back one more level to the JS API. If that can load, it gives us a parse/bundle check without depending on the broken native shims.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "@'
const esbuild = require('esbuild');
esbuild.build({
  entryPoints: ['forex-dashboard_1.jsx'],
  bundle: true,
  format: 'esm',
  outfile: 'dist/validation-forex-dashboard_1.js',
  logLevel: 'info'
}).catch((error) => {
  console.error(error);
  process.exit(1);
});
'@ | node -" in C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_pageexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Test-Path 'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\landing_page\\dist\\validation-forex-dashboard_1.js'" in C:\Users\edebe\eds exited 1 in 2.50s:
C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_page\node_modules\esbuild\lib\main.js:1736
          throw new Error(`
          ^

Error: 
You installed esbuild for another platform than the one you're currently using.
This won't work because esbuild is written with native code and needs to
install a platform-specific binary executable.

Specifically the "@esbuild/linux-x64" package is present but this platform
needs the "@esbuild/win32-x64" package instead. People often get into this
situation by installing esbuild on Windows or macOS and copying "node_modules"
into a Docker image that runs Linux, or by copying "node_modules" between
Windows and WSL environments.

If you are installing with npm, you can try not copying the "node_modules"
directory when you copy the files over, and running "npm ci" or "npm install"
on the destination platform after the copy. Or you could consider using yarn
instead of npm which has built-in support for installing a package on multiple
platforms simultaneously.
 succeeded in 3.80s:
False
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The native bundlers are unusable because this `node_modules` tree was installed for Linux while the current machine is Windows. I’m switching to Babel parser validation now; that won’t prove a full production build, but it will prove the edited JSX still parses in this environment and lets us document the real blocker accurately.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "@'
const fs = require('fs');
const parser = require('@babel/parser');
const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8');
parser.parse(source, {
  sourceType: 'module',
  plugins: ['jsx']
});
console.log('Babel parse OK');
'@ | node -" in C:\Users\edebe\eds\TradeApps\breakout\piphunter\landing_pageexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx' | Select-Object -Index (1090..1235)" in C:\Users\edebe\eds succeeded in 2.64s:
Babel parse OK
 succeeded in 3.02s:
  const [activeTab,setActiveTab]=useState("leaderboard");
  const [selectedId,setSelectedId]=useState(null);
  const [tradeFilter,setTradeFilter]=useState("ALL");
  const [typeFilter,setTypeFilter]=useState("ALL");
  const [pairFilter,setPairFilter]=useState("ALL");
  const [tick,setTick]=useState(new Date());
  const [strategyTrades, setStrategyTrades] = useState([]);  // All trades (open + closed) for selected strategy
  const [tradesLoading, setTradesLoading] = useState(false);
  const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
  const drillRef=useRef(null);
  const previousSelectedDateRef = useRef(selectedDate);
  const selectedIdRef = useRef(selectedId);
  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);

  // Theme colors
  const themes = {
    dark: {
      bg: '#050b11',
      bgSecondary: 'rgba(255,255,255,0.015)',
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
The code change is validated as far as this environment allows: Babel parsed the JSX successfully, while both Vite and esbuild are blocked by cross-platform `node_modules`. I’m updating the lifecycle document now with checked plan items, normalized evidence, the validation trail, and an explicit user-verification request so the task state is accurate.
Plan update
Implementation and available technical validation are complete. Final step is updating the lifecycle file with normalized evidence and awaiting-user-verification status.
  ✓ Patch the dashboard component so auto-refresh preserves the selected drilldown while date changes still reset it.
  ✓ Run validation commands against the modified dashboard code and inspect the diff/output.
  → Update the lifecycle task file with required plan/evidence/validation entries and current status.
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git -C 'TradeApps' diff -- 'breakout/piphunter/landing_page/forex-dashboard_1.jsx' | Select-Object -First 220" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git -C 'TradeApps' status --short -- 'breakout/piphunter/landing_page/forex-dashboard_1.jsx'" in C:\Users\edebe\eds succeeded in 1.50s:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb6..d0e8eb8b60 100644
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@ export default function App(){
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@ export default function App(){
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
 succeeded in 2.33s:
 M breakout/piphunter/landing_page/forex-dashboard_1.jsx
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss zzz'" in C:\Users\edebe\eds succeeded in 1.06s:
2026-03-19 16:36:51 +00:00
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$i=1; Get-Content '"'C:\\Users\\edebe\\eds\\TradeApps\\breakout\\piphunter\\landing_page\\forex-dashboard_1.jsx' | ForEach-Object { '{0,6}: {1}' -f "'$i, $_; $i++ } | Select-String -Pattern '"'previousSelectedDateRef|selectedIdRef|strategyTradesRefreshKey|dateChanged|transformed.some|loadStrategyTrades\\(|\\}, \\[selectedId, selectedDate, strategyTradesRefreshKey, strategies\\]\\);' -Context 0,2" in C:\Users\edebe\eds succeeded in 1.47s:

>   1102:   const [7mpreviousSelectedDateRef[0m = useRef(selectedDate);
>   1103:   const [7mselectedIdRef[0m = useRef(selectedId);
>   1104:   const [[7mstrategyTradesRefreshKey[0m, setStrategyTradesRefreshKey] = useState(0);[0m
[7m[0m    1105: [0m
[7m[0m    1106:   // Theme colors[0m
>   1134:     [7mselectedIdRef[0m.current = selectedId;[0m
[7m[0m    1135:   }, [selectedId]);[0m
[7m[0m    1136: [0m
>   1142:         const [7mdateChanged[0m = previousSelectedDateRef.current !== selectedDate;
>   1143:         [7mpreviousSelectedDateRef[0m.current = selectedDate;[0m
[7m[0m    1144: [0m
>   1145:         if ([7mdateChanged[0m) {[0m
[7m[0m    1146:           setSelectedId(null);[0m
[7m[0m    1147:           setStrategyTrades([]);[0m
>   1163:             if ([7mselectedIdRef[0m.current && !transformed.some(s => s.id === selectedIdRef.current)) {[0m
[7m[0m    1164:               setSelectedId(null);[0m
[7m[0m    1165:               setStrategyTrades([]);[0m
>   1181:           set[7mStrategyTradesRefreshKey[0m(prev => prev + 1);[0m
[7m[0m    1182:         } catch (err) {[0m
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];

codex
I have the code references and validation outputs I need. I’m replacing the ad hoc task note with a compliant lifecycle record now, preserving the original intake details and appending the actual implementation, evidence, and current `Awaiting user verification` state.
file update
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
# Preserve Drilldown State on Auto-Refresh

**Source**: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.

## Context
- **Dashboard URL**: `http://172.22.108.121:3001/`
- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- **Auto-refresh interval**: 30 seconds (line 1173)

## Problem Description
1. User expands a strategy to view trade drilldown
2. Auto-refresh triggers after 30 seconds
3. Drilldown collapses/closes
4. User must re-click to expand again
5. Poor UX - interrupts analysis workflow

## Root Cause (Likely)
The `loadData` function in useEffect (line 1131-1175) resets state:
- `setSelectedId(null)` on line 1135 clears the selected strategy
- `setStrategyTrades([])` on line 1136 clears trade data

This happens on every refresh, not just date changes.

## Implementation Steps
- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
- [ ] Preserve expanded strategy state across refreshes
- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
- [ ] Consider using `useRef` to track if this is initial load vs refresh

## Proposed Fix
```javascript
// Track if date changed vs just refresh
const prevDateRef = useRef(selectedDate);

useEffect(() => {
  const loadData = async () => {
    const dateChanged = prevDateRef.current !== selectedDate;
    prevDateRef.current = selectedDate;

    if (dateChanged) {
      setSelectedId(null);  // Only reset on date change
      setStrategyTrades([]);
    }
    // ... rest of fetch logic
  };
}, [selectedDate]);
```

## Validation
- Expand a strategy drilldown
- Wait for auto-refresh (30s)
- Drilldown should remain open with updated data
- Changing date should still reset the view

## Risks/Notes
- Need to handle case where selected strategy no longer exists after refresh
- May need to re-fetch strategy trades after main refresh

## Completion Status
**Pending**


## Execution Evidence
- Agent lane: claude
- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
- Return code: 0
- Stdout:
```text
claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 2.50s:
Success. Updated the following files:
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
deleted file mode 100644
index 929e3eac76297c61ad5307d7b040b60e19eefc49..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ /dev/null
@@ -1,78 +0,0 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
deleted file mode 100644
index 929e3eac76297c61ad5307d7b040b60e19eefc49..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ /dev/null
@@ -1,78 +0,0 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
# Preserve Drilldown State on Auto-Refresh

Source: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.

## Context
- Dashboard URL: `http://172.22.108.121:3001/`
- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- Auto-refresh interval: `30000` ms

## Dependency
Dependency: None

## Original Task Intake
- User expands a strategy to view trade drilldown.
- Auto-refresh triggers after 30 seconds.
- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
- Expected behavior: preserve drilldown on refresh, but still reset on date change.

## Plan
- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.

## Evidence
Objective-Delivery-Coverage: 85%
Auto-Acceptance: false
- Evidence-Type: diff
  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
  - Status: captured
- Evidence-Type: test_output
  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
  - Objective-Proved: The modified JSX parses successfully in the current environment.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: `http://172.22.108.121:3001/`
  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
  - Status: planned

## Implementation Log
- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.

## Changes Made
- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.

## Validation
- `npm run build`
  - Result: failed
  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
- `node .\node_modules\vite\bin\vite.js build`
  - Result: failed
  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
  - Result: passed
  - Summary: `Babel parse OK`
- User verification requested on 2026-03-19 16:36 UTC:
  - Expand a strategy drilldown on the dashboard.
  - Wait for the 30-second auto-refresh.
  - Confirm the same drilldown remains open and its trade data refreshes.
  - Change the selected date and confirm the drilldown resets.

## Risks/Notes
- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.

## Completion Status
Awaiting user verification - 2026-03-19 16:36:51 +00:00

## Historical Execution Evidence
- Agent lane: claude
- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
- Return code: `0`
- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`

## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 2.33s:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
index 929e3eac76297c61ad5307d7b040b60e19eefc49..f82a180044a1f119a76fc81a8cd8c557bc3328eb
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
@@ -1,78 +1,96 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# Preserve Drilldown State on Auto-Refresh
+
+Source: PipHunter Dashboard - FXPilot Landing Page
+
+## Task Summary
+Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.
+
+## Context
+- Dashboard URL: `http://172.22.108.121:3001/`
+- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+- Auto-refresh interval: `30000` ms
+
+## Dependency
+Dependency: None
+
+## Original Task Intake
+- User expands a strategy to view trade drilldown.
+- Auto-refresh triggers after 30 seconds.
+- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
+- Expected behavior: preserve drilldown on refresh, but still reset on date change.
+
+## Plan
+- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
+  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
+  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
+- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
+  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
+  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
+- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
+  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
+  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Objective-Proved: The modified JSX parses successfully in the current environment.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: `http://172.22.108.121:3001/`
+  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
+- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
+- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
+- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
+- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
+- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
+- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.
+
+## Changes Made
+- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
+- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
+- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
+- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.
+
+## Validation
+- `npm run build`
+  - Result: failed
+  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
+- `node .\node_modules\vite\bin\vite.js build`
+  - Result: failed
+  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
+- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Result: passed
+  - Summary: `Babel parse OK`
+- User verification requested on 2026-03-19 16:36 UTC:
+  - Expand a strategy drilldown on the dashboard.
+  - Wait for the 30-second auto-refresh.
+  - Confirm the same drilldown remains open and its trade data refreshes.
+  - Change the selected date and confirm the drilldown resets.
+
+## Risks/Notes
+- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
+- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
+- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.
+
+## Completion Status
+Awaiting user verification - 2026-03-19 16:36:51 +00:00
+
+## Historical Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+- Return code: `0`
+- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
index 929e3eac76297c61ad5307d7b040b60e19eefc49..f82a180044a1f119a76fc81a8cd8c557bc3328eb
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
@@ -1,78 +1,96 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# Preserve Drilldown State on Auto-Refresh
+
+Source: PipHunter Dashboard - FXPilot Landing Page
+
+## Task Summary
+Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.
+
+## Context
+- Dashboard URL: `http://172.22.108.121:3001/`
+- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+- Auto-refresh interval: `30000` ms
+
+## Dependency
+Dependency: None
+
+## Original Task Intake
+- User expands a strategy to view trade drilldown.
+- Auto-refresh triggers after 30 seconds.
+- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
+- Expected behavior: preserve drilldown on refresh, but still reset on date change.
+
+## Plan
+- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
+  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
+  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
+- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
+  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
+  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
+- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
+  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
+  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Objective-Proved: The modified JSX parses successfully in the current environment.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: `http://172.22.108.121:3001/`
+  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
+- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
+- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
+- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
+- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
+- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
+- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.
+
+## Changes Made
+- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
+- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
+- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
+- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.
+
+## Validation
+- `npm run build`
+  - Result: failed
+  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
+- `node .\node_modules\vite\bin\vite.js build`
+  - Result: failed
+  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
+- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Result: passed
+  - Summary: `Babel parse OK`
+- User verification requested on 2026-03-19 16:36 UTC:
+  - Expand a strategy drilldown on the dashboard.
+  - Wait for the 30-second auto-refresh.
+  - Confirm the same drilldown remains open and its trade data refreshes.
+  - Change the selected date and confirm the drilldown resets.
+
+## Risks/Notes
+- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
+- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
+- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.
+
+## Completion Status
+Awaiting user verification - 2026-03-19 16:36:51 +00:00
+
+## Historical Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+- Return code: `0`
+- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git -C 'TradeApps' diff --stat -- 'breakout/piphunter/landing_page/forex-dashboard_1.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md'" in C:\Users\edebe\eds succeeded in 1.33s:
# Preserve Drilldown State on Auto-Refresh

Source: PipHunter Dashboard - FXPilot Landing Page

## Task Summary
Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.

## Context
- Dashboard URL: `http://172.22.108.121:3001/`
- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
- Auto-refresh interval: `30000` ms

## Dependency
Dependency: None

## Original Task Intake
- User expands a strategy to view trade drilldown.
- Auto-refresh triggers after 30 seconds.
- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
- Expected behavior: preserve drilldown on refresh, but still reset on date change.
 succeeded in 1.50s:
 .../piphunter/landing_page/forex-dashboard_1.jsx   | 26 ++++++++++++++++++----
 1 file changed, 22 insertions(+), 4 deletions(-)
warning: in the working copy of 'breakout/piphunter/landing_page/forex-dashboard_1.jsx', LF will be replaced by CRLF the next time Git touches it
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
index 929e3eac76297c61ad5307d7b040b60e19eefc49..f82a180044a1f119a76fc81a8cd8c557bc3328eb
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
@@ -1,78 +1,96 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# Preserve Drilldown State on Auto-Refresh
+
+Source: PipHunter Dashboard - FXPilot Landing Page
+
+## Task Summary
+Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.
+
+## Context
+- Dashboard URL: `http://172.22.108.121:3001/`
+- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+- Auto-refresh interval: `30000` ms
+
+## Dependency
+Dependency: None
+
+## Original Task Intake
+- User expands a strategy to view trade drilldown.
+- Auto-refresh triggers after 30 seconds.
+- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
+- Expected behavior: preserve drilldown on refresh, but still reset on date change.
+
+## Plan
+- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
+  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
+  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
+- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
+  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
+  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
+- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
+  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
+  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Objective-Proved: The modified JSX parses successfully in the current environment.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: `http://172.22.108.121:3001/`
+  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
+- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
+- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
+- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
+- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
+- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
+- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.
+
+## Changes Made
+- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
+- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
+- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
+- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.
+
+## Validation
+- `npm run build`
+  - Result: failed
+  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
+- `node .\node_modules\vite\bin\vite.js build`
+  - Result: failed
+  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
+- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Result: passed
+  - Summary: `Babel parse OK`
+- User verification requested on 2026-03-19 16:36 UTC:
+  - Expand a strategy drilldown on the dashboard.
+  - Wait for the 30-second auto-refresh.
+  - Confirm the same drilldown remains open and its trade data refreshes.
+  - Change the selected date and confirm the drilldown resets.
+
+## Risks/Notes
+- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
+- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
+- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.
+
+## Completion Status
+Awaiting user verification - 2026-03-19 16:36:51 +00:00
+
+## Historical Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+- Return code: `0`
+- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

Plan update
Lifecycle record has been updated with checked steps, evidence, validation results, and awaiting-user-verification status.
  ✓ Patch the dashboard component so auto-refresh preserves the selected drilldown while date changes still reset it.
  ✓ Run validation commands against the modified dashboard code and inspect the diff/output.
  ✓ Update the lifecycle task file with required plan/evidence/validation entries and current status.
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
index 929e3eac76297c61ad5307d7b040b60e19eefc49..f82a180044a1f119a76fc81a8cd8c557bc3328eb
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
@@ -1,78 +1,96 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# Preserve Drilldown State on Auto-Refresh
+
+Source: PipHunter Dashboard - FXPilot Landing Page
+
+## Task Summary
+Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.
+
+## Context
+- Dashboard URL: `http://172.22.108.121:3001/`
+- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+- Auto-refresh interval: `30000` ms
+
+## Dependency
+Dependency: None
+
+## Original Task Intake
+- User expands a strategy to view trade drilldown.
+- Auto-refresh triggers after 30 seconds.
+- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
+- Expected behavior: preserve drilldown on refresh, but still reset on date change.
+
+## Plan
+- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
+  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
+  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
+- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
+  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
+  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
+- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
+  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
+  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Objective-Proved: The modified JSX parses successfully in the current environment.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: `http://172.22.108.121:3001/`
+  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
+- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
+- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
+- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
+- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
+- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
+- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.
+
+## Changes Made
+- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
+- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
+- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
+- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.
+
+## Validation
+- `npm run build`
+  - Result: failed
+  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
+- `node .\node_modules\vite\bin\vite.js build`
+  - Result: failed
+  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
+- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Result: passed
+  - Summary: `Babel parse OK`
+- User verification requested on 2026-03-19 16:36 UTC:
+  - Expand a strategy drilldown on the dashboard.
+  - Wait for the 30-second auto-refresh.
+  - Confirm the same drilldown remains open and its trade data refreshes.
+  - Change the selected date and confirm the drilldown resets.
+
+## Risks/Notes
+- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
+- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
+- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.
+
+## Completion Status
+Awaiting user verification - 2026-03-19 16:36:51 +00:00
+
+## Historical Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+- Return code: `0`
+- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

codex
Implemented the drilldown preservation fix in [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1102). The refresh loop now tracks date changes separately, preserves `selectedId` during the 30-second poll, clears the drilldown only when the date changes or the selected strategy disappears from refreshed results, and re-fetches selected strategy trades after each successful main refresh via the new refresh key at [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1142) and [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1246).

I updated the lifecycle file at [20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md](/Users/edebe/eds/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md) with checked plan items, normalized evidence, validation results, and `Awaiting user verification` status. Validation: Babel JSX parse passed; `npm run build` and direct Vite build are blocked by the current cross-platform `node_modules` state (`vite` shim unavailable, Rollup Windows native package missing).

Please verify on `http://172.22.108.121:3001/`:
1. Expand a strategy drilldown and wait for the 30-second auto-refresh.
2. Confirm the drilldown stays open and trade data refreshes.
3. Change the date and confirm the drilldown resets.

Send pass/fail for those three checks and I’ll update the task to complete.
file update:
diff --git a/breakout/piphunter/landing_page/forex-dashboard_1.jsx b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
index b79769deb68df972f858b6b2aec1b5a31ba6da7d..d0e8eb8b6017694a3c0ef418328b5d2328e87374
--- a/breakout/piphunter/landing_page/forex-dashboard_1.jsx
+++ b/breakout/piphunter/landing_page/forex-dashboard_1.jsx
@@ -1099,6 +1099,9 @@
   const [theme, setTheme] = useState('dark');  // 'dark' | 'light'
   const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);  // Date selector
   const drillRef=useRef(null);
+  const previousSelectedDateRef = useRef(selectedDate);
+  const selectedIdRef = useRef(selectedId);
+  const [strategyTradesRefreshKey, setStrategyTradesRefreshKey] = useState(0);
 
   // Theme colors
   const themes = {
@@ -1127,13 +1130,22 @@
   };
   const t = themes[theme];
 
+  useEffect(() => {
+    selectedIdRef.current = selectedId;
+  }, [selectedId]);
+
   // Fetch live data on mount and when date changes
   useEffect(() => {
     const loadData = async () => {
       if (DATA_MODE === 'live') {
         setIsLoading(true);
-        setSelectedId(null); // Reset selection when date changes
-        setStrategyTrades([]);
+        const dateChanged = previousSelectedDateRef.current !== selectedDate;
+        previousSelectedDateRef.current = selectedDate;
+
+        if (dateChanged) {
+          setSelectedId(null);
+          setStrategyTrades([]);
+        }
         try {
           const [top20Data, biasData, tradesData, summaryData] = await Promise.all([
             fetchTop20(selectedDate),
@@ -1147,6 +1159,11 @@
             setStrategies(transformed);
             STRATEGIES = transformed; // Update global for compatibility
             setLastUpdate(top20Data.lastUpdate);
+
+            if (selectedIdRef.current && !transformed.some(s => s.id === selectedIdRef.current)) {
+              setSelectedId(null);
+              setStrategyTrades([]);
+            }
           }
 
           if (biasData) {
@@ -1160,6 +1177,8 @@
           if (summaryData && summaryData.curves) {
             setEquityCurves(summaryData.curves);
           }
+
+          setStrategyTradesRefreshKey(prev => prev + 1);
         } catch (err) {
           console.error('Failed to fetch live data:', err);
         }
@@ -1225,8 +1244,7 @@
     };
 
     loadStrategyTrades();
-  // eslint-disable-next-line react-hooks/exhaustive-deps
-  }, [selectedId, strategies.length, selectedDate]);
+  }, [selectedId, selectedDate, strategyTradesRefreshKey, strategies]);
 
   // Dynamic types & pairs — derived from data (live: from GET /v1/strategy-types)
   const allTypes=["ALL",...[...new Set(activeStrategies.map(s=>s.type))].sort()];
diff --git a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
index 929e3eac76297c61ad5307d7b040b60e19eefc49..f82a180044a1f119a76fc81a8cd8c557bc3328eb
--- a/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
+++ b/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
@@ -1,78 +1,96 @@
-# Preserve Drilldown State on Auto-Refresh
-
-**Source**: PipHunter Dashboard - FXPilot Landing Page
-
-## Task Summary
-When viewing trade drilldown for a strategy, the auto-refresh (every 30 seconds) causes the drilldown to close, forcing user to re-expand. The drilldown state should be preserved across data refreshes.
-
-## Context
-- **Dashboard URL**: `http://172.22.108.121:3001/`
-- **Source File**: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
-- **Auto-refresh interval**: 30 seconds (line 1173)
-
-## Problem Description
-1. User expands a strategy to view trade drilldown
-2. Auto-refresh triggers after 30 seconds
-3. Drilldown collapses/closes
-4. User must re-click to expand again
-5. Poor UX - interrupts analysis workflow
-
-## Root Cause (Likely)
-The `loadData` function in useEffect (line 1131-1175) resets state:
-- `setSelectedId(null)` on line 1135 clears the selected strategy
-- `setStrategyTrades([])` on line 1136 clears trade data
-
-This happens on every refresh, not just date changes.
-
-## Implementation Steps
-- [ ] Only reset `selectedId` when date actually changes, not on interval refresh
-- [ ] Preserve expanded strategy state across refreshes
-- [ ] Re-fetch strategy trades after main data refresh if a strategy is selected
-- [ ] Consider using `useRef` to track if this is initial load vs refresh
-
-## Proposed Fix
-```javascript
-// Track if date changed vs just refresh
-const prevDateRef = useRef(selectedDate);
-
-useEffect(() => {
-  const loadData = async () => {
-    const dateChanged = prevDateRef.current !== selectedDate;
-    prevDateRef.current = selectedDate;
-
-    if (dateChanged) {
-      setSelectedId(null);  // Only reset on date change
-      setStrategyTrades([]);
-    }
-    // ... rest of fetch logic
-  };
-}, [selectedDate]);
-```
-
-## Validation
-- Expand a strategy drilldown
-- Wait for auto-refresh (30s)
-- Drilldown should remain open with updated data
-- Changing date should still reset the view
-
-## Risks/Notes
-- Need to handle case where selected strategy no longer exists after refresh
-- May need to re-fetch strategy trades after main refresh
-
-## Completion Status
-**Pending**
-
-
-## Execution Evidence
-- Agent lane: claude
-- Command: cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-- Return code: 0
-- Stdout:
-```text
-claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+# Preserve Drilldown State on Auto-Refresh
+
+Source: PipHunter Dashboard - FXPilot Landing Page
+
+## Task Summary
+Preserve the selected strategy drilldown during the 30-second dashboard auto-refresh so users do not have to reopen the drilldown during analysis. Date changes must still reset the drilldown.
+
+## Context
+- Dashboard URL: `http://172.22.108.121:3001/`
+- Source file: `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+- Auto-refresh interval: `30000` ms
+
+## Dependency
+Dependency: None
+
+## Original Task Intake
+- User expands a strategy to view trade drilldown.
+- Auto-refresh triggers after 30 seconds.
+- Drilldown collapses because `selectedId` and `strategyTrades` were reset inside `loadData`.
+- Expected behavior: preserve drilldown on refresh, but still reset on date change.
+
+## Plan
+- [x] 1. Separate date-change resets from interval refreshes inside the dashboard data loader.
+  - [x] Test: Inspect the updated `loadData` flow in `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` and confirm `setSelectedId(null)` only runs when the selected date changes or the selected strategy disappears from refreshed results.
+  - [x] Evidence: `previousSelectedDateRef` and `selectedIdRef` were added, `dateChanged` now gates the reset path, and missing selected strategies are cleared in the refreshed strategy list diff.
+- [x] 2. Re-trigger selected strategy trade loading after each successful main refresh without collapsing the drilldown.
+  - [x] Test: Inspect the updated drilldown fetch effect and confirm it depends on a refresh signal produced by the main data load rather than on clearing selection state.
+  - [x] Evidence: `strategyTradesRefreshKey` increments after successful main refresh and the strategy-trade effect now depends on `[selectedId, selectedDate, strategyTradesRefreshKey, strategies]`.
+- [x] 3. Run technical validation available in the current environment and record the user verification request required for this UI change.
+  - [x] Test: Run `@'...@ | node -` with `@babel/parser` against `forex-dashboard_1.jsx` and confirm parse success; run `npm run build` and `node .\node_modules\vite\bin\vite.js build` to capture the current environment limitation.
+  - [x] Evidence: Babel parser returned `Babel parse OK`; Vite and Rollup validation are blocked because the checked-in `node_modules` tree contains Linux-native packages on this Windows host.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: diff
+  - Artifact: `git -C TradeApps diff -- breakout/piphunter/landing_page/forex-dashboard_1.jsx`
+  - Objective-Proved: The dashboard now preserves drilldown state across auto-refresh, only resets on date change, and refreshes selected strategy trades after the main data load.
+  - Status: captured
+- Evidence-Type: test_output
+  - Artifact: `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Objective-Proved: The modified JSX parses successfully in the current environment.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: `http://172.22.108.121:3001/`
+  - Objective-Proved: User can verify that expanded drilldown stays open after the next 30-second refresh and still resets after changing the date.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-19 16:31: Loaded `skills/workstream-task-lifecycle/SKILL.md` and this task file, then reviewed the dashboard component and current worktree state.
+- 2026-03-19 16:34: Updated `TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx` to stop clearing selection on every refresh, track the selected strategy in a ref, and create a refresh key for selected strategy trade reloads.
+- 2026-03-19 16:35: Added a guard to clear the drilldown only if the selected strategy disappears from refreshed strategy data.
+- 2026-03-19 16:35: Attempted `npm run build`; this failed because the local `vite` command is not executable in the current environment.
+- 2026-03-19 16:35: Attempted `node .\node_modules\vite\bin\vite.js build`; this failed because Rollup's Windows native optional dependency is missing from the current `node_modules`.
+- 2026-03-19 16:36: Ran Babel parser validation for `forex-dashboard_1.jsx`; parsing succeeded with `Babel parse OK`.
+- 2026-03-19 16:36: Recorded a required user verification request for the UI behavior change and left the task in progress pending that confirmation.
+
+## Changes Made
+- Added `previousSelectedDateRef` in `forex-dashboard_1.jsx` so the dashboard only resets `selectedId` and `strategyTrades` when `selectedDate` changes.
+- Added `selectedIdRef` so the refresh cycle can preserve or clear the current drilldown based on refreshed strategy availability without relying on stale interval-closure state.
+- Added `strategyTradesRefreshKey` so the selected strategy's trade drilldown re-fetches after each successful main dashboard refresh while keeping the drilldown open.
+- Updated the selected strategy trade effect dependencies to include the refresh key and live strategy data.
+
+## Validation
+- `npm run build`
+  - Result: failed
+  - Summary: `'vite' is not recognized as an internal or external command, operable program or batch file.`
+- `node .\node_modules\vite\bin\vite.js build`
+  - Result: failed
+  - Summary: `Cannot find module @rollup/rollup-win32-x64-msvc`; the current `node_modules` tree contains incompatible optional native packages for this Windows environment.
+- `@' const fs = require('fs'); const parser = require('@babel/parser'); const source = fs.readFileSync('forex-dashboard_1.jsx', 'utf8'); parser.parse(source, { sourceType: 'module', plugins: ['jsx'] }); console.log('Babel parse OK'); '@ | node -`
+  - Result: passed
+  - Summary: `Babel parse OK`
+- User verification requested on 2026-03-19 16:36 UTC:
+  - Expand a strategy drilldown on the dashboard.
+  - Wait for the 30-second auto-refresh.
+  - Confirm the same drilldown remains open and its trade data refreshes.
+  - Change the selected date and confirm the drilldown resets.
+
+## Risks/Notes
+- Full production build validation is currently blocked by cross-platform dependency drift in `TradeApps/breakout/piphunter/landing_page/node_modules`.
+- This task changes user-visible behavior, so completion requires user verification per the lifecycle gate.
+- If the refreshed strategy list no longer contains the selected strategy, the drilldown still closes intentionally.
+
+## Completion Status
+Awaiting user verification - 2026-03-19 16:36:51 +00:00
+
+## Historical Execution Evidence
+- Agent lane: claude
+- Command: `cmd /c echo claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+- Return code: `0`
+- Stdout: `claude processing 20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md`
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

tokens used
90,403
Implemented the drilldown preservation fix in [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1102). The refresh loop now tracks date changes separately, preserves `selectedId` during the 30-second poll, clears the drilldown only when the date changes or the selected strategy disappears from refreshed results, and re-fetches selected strategy trades after each successful main refresh via the new refresh key at [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1142) and [forex-dashboard_1.jsx](/Users/edebe/eds/TradeApps/breakout/piphunter/landing_page/forex-dashboard_1.jsx#L1246).

I updated the lifecycle file at [20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md](/Users/edebe/eds/workstream/200_inprogress/codex/20260302_010106_claude_pipHunter_preserve_drilldown_on_autorefresh.md) with checked plan items, normalized evidence, validation results, and `Awaiting user verification` status. Validation: Babel JSX parse passed; `npm run build` and direct Vite build are blocked by the current cross-platform `node_modules` state (`vite` shim unavailable, Rollup Windows native package missing).

Please verify on `http://172.22.108.121:3001/`:
1. Expand a strategy drilldown and wait for the 30-second auto-refresh.
2. Confirm the drilldown stays open and trade data refreshes.
3. Change the date and confirm the drilldown resets.

Send pass/fail for those three checks and I’ll update the task to complete.
