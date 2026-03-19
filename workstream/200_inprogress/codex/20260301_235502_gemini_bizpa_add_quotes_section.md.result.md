OpenAI Codex v0.114.0 (research preview)
--------
workdir: C:\Users\edebe\eds
model: gpt-5.4
provider: openai
approval: never
sandbox: workspace-write [workdir, /tmp, $TMPDIR, C:\Users\edebe\.codex\memories]
reasoning effort: medium
reasoning summaries: none
session id: 019d022c-b4b7-7613-bd67-e5c5b31d40dc
--------
user
Execute this task file end-to-end. Read and follow C:\Users\edebe\eds\skills\workstream-task-lifecycle\SKILL.md first. Task file: C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md. Implement required changes in the workspace, run validations, and update checklist items.
mcp startup: no servers
codex
I’m loading the workstream lifecycle skill and the specified task file first, then I’ll inspect the relevant code paths before making changes.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\skills\\workstream-task-lifecycle\\SKILL.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260301_235502_gemini_bizpa_add_quotes_section.md'" in C:\Users\edebe\eds succeeded in 1.05s:
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
 succeeded in 1.02s:
# TASK: bizPA Dedicated Quotes Section

Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`

## 1. Task Summary
Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.

## 2. Context
- Affected Files: `bizPA/frontend/src/App.jsx`
- Current State: Quotes are viewed by filtering the Timeline by 'quote'.

## 3. Implementation Log
- (Pending) Add 'Quotes' to bottom navigation.
- (Pending) Create `renderQuotes` function in `App.jsx`.
- (Pending) Update voice navigation to switch to this dedicated section.

## 4. Completion Status
**TODO** - 2026-03-01


codex
I’ve got the lifecycle requirements and the current task file. Next I’m reading the target UI code and adjacent project files so I can implement the change and bring the task document up to the required template.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg --files 'bizPA/frontend/src'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\eds succeeded in 1.08s:

    Directory: C:\Users\edebe\eds\workstream\200_inprogress\codex

[32;1mMode   [0m[32;1m              LastWriteTime[0m[32;1m         Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
-a---          02/03/2026    04:21              0 .keep
-a---          18/03/2026    17:21           1009 20260301_235502_gemini_bizpa_add_quotes_section.md
-a---          18/03/2026    18:03        1728960 20260314_034028_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole
                                                  _traders_bank_feed_first_workstreamA_implement_secure_sign_up_and_sol
                                                  e_trader_onboarding_flow.md.result.md
-a---          18/03/2026    18:18           8748 20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole
                                                  _traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_q
                                                  ueue_screen.md
-a---          18/03/2026    18:19        2821680 20260314_034042_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole
                                                  _traders_bank_feed_first_workstreamE_deliver_mobile_inbox_exception_q
                                                  ueue_screen.md.result.md
-a---          18/03/2026    18:06           6817 20260314_034043_mvp_prd_mobile_quarterly_export_in_10_minutes_uk_sole
                                                  _traders_bank_feed_first_workstreamE_deliver_quarter_readiness_and_fi
                                                  nish_now_screen.md

 succeeded in 1.16s:
bizPA/frontend/src\quarterReadiness.test.js
bizPA/frontend/src\quarterReadiness.js
bizPA/frontend/src\OnboardingGate.jsx
bizPA/frontend/src\onboarding.test.js
bizPA/frontend/src\onboarding.js
bizPA/frontend/src\index.jsx
bizPA/frontend/src\governance.test.js
bizPA/frontend/src\governance.js
bizPA/frontend/src\controlCentre.test.js
bizPA/frontend/src\controlCentre.js
bizPA/frontend/src\App.jsx
 succeeded in 2.25s:
import React, { useEffect, useRef, useState } from 'react';
import axios from 'axios';
import {
  ArchiveRestore,
  ArrowRight,
  Bell,
  Briefcase,
  Calendar,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
  Clock,
  Download,
  Flame,
  FileText,
  History,
  LayoutGrid,
  Lock,
  LockOpen,
  Mic,
codex
I’ve identified the main UI file and the bottom navigation area. Now I’m tracing the timeline rendering and voice command routing so the quotes section is isolated cleanly rather than duplicated.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"renderActivity|currentTab === 'activity'|quote|Quotes|voice|setCurrentTab\\(\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Select-String -Path 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx' -Pattern 'const \\[currentTab|setCurrentTab|handleVoice|transcript|SpeechRecognition' -Context 3,3" in C:\Users\edebe\eds succeeded in 841ms:
64:const MONETARY_TYPES = ['invoice', 'receipt', 'payment', 'quote'];
119:  type: 'invoice',
358:          entity_type: 'invoice',
420:  .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
661:    due_date: form.type === 'invoice' ? form.relevantDate || undefined : undefined,
667:  entityType: preview?.entity_type || 'invoice',
1185:      reopen_reason: 'Late supplier invoice received after final bank sync.',
1189:        reopen_reason: 'Late supplier invoice received after final bank sync.'
1210:          reopen_reason: 'Late supplier invoice received after final bank sync.',
1285:  const [voiceStatus, setVoiceStatus] = useState('idle');
1299:  const [reopenReason, setReopenReason] = useState('Late supplier invoice received after final bank sync.');
1329:        setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
1386:    setCurrentTab('add');
1389:      rawNote: 'Voice capture: invoice for Brookside Renovations, GBP 480 labour, standard VAT.',
1395:      entityType: 'invoice',
1403:      note: 'Voice capture: invoice for Brookside Renovations, GBP 480 labour, standard VAT.',
1409:      setCurrentTab(requestedTab || 'control');
1415:      setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
1588:      setCurrentTab('home');
1824:      alert('Cannot start voice capture while backend is disconnected.');
 succeeded in 1.11s:

  bizPA\frontend\src\App.jsx:28:  TriangleAlert,
  bizPA\frontend\src\App.jsx:29:  Wallet,
  bizPA\frontend\src\App.jsx:30:} from 'lucide-react';
> bizPA\frontend\src\App.jsx:31:import { [7mSpeechRecognition[0m } from '@capacitor-community/speech-recognition';[0m
[7m[0m  bizPA\frontend\src\App.jsx:32:import { Preferences } from '@capacitor/preferences';[0m
[7m[0m  bizPA\frontend\src\App.jsx:33:import {[0m
[7m[0m  bizPA\frontend\src\App.jsx:34:  PERMISSIONS,[0m
  bizPA\frontend\src\App.jsx:1254:  const [insights, setInsights] = useState([]);
  bizPA\frontend\src\App.jsx:1255:  const [loading, setLoading] = useState(true);
  bizPA\frontend\src\App.jsx:1256:  const [connectionError, setConnectionError] = useState(null);
> bizPA\frontend\src\App.jsx:1257:  const [[7mtranscript[0m, setTranscript] = useState('');[0m
[7m[0m  bizPA\frontend\src\App.jsx:1258:  const [isListening, setIsListening] = useState(false);[0m
> bizPA\frontend\src\App.jsx:1259:  [7mconst [0m[7m[currentTab[0m, [0m[7m[0msetCurrentTab] [0m[7m[0m= [0m[7m[0museState(requestedTab [0m[7m[0m|| [0m
[7m[0m(commandCentreDemoEnabled [0m[7m[0m? [0m[7m[0m'control' [0m[7m[0m: [0m[7m[0m'home'));[0m
[7m[0m  bizPA\frontend\src\App.jsx:1260:  const [activityTypeFilter, setActivityTypeFilter] = useState(null);[0m
[7m[0m  bizPA\frontend\src\App.jsx:1261:  const [activityClientFilter, setActivityClientFilter] = useState('');[0m
[7m[0m  bizPA\frontend\src\App.jsx:1262:  const [searchQuery, setSearchQuery] = useState('');[0m
  bizPA\frontend\src\App.jsx:1310:  const [inboxBusyId, setInboxBusyId] = useState('');
  bizPA\frontend\src\App.jsx:1311:  const [inboxMessage, setInboxMessage] = useState(null);
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[1938..1990]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"const \\[items|setItems\\(|fetchAllData|items =|activityTypeFilter|activityClientFilter|searchQuery\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[2390..2655]' in C:\Users\edebe\eds succeeded in 1.11s:
1249:  const [items, setItems] = useState([]);
1260:  const [activityTypeFilter, setActivityTypeFilter] = useState(null);
1261:  const [activityClientFilter, setActivityClientFilter] = useState('');
1262:  const [searchQuery, setSearchQuery] = useState('');
1365:      fetchAllData();
1453:  const fetchAllData = async (activeUser = currentUser) => {
1479:      setItems(Array.isArray(responses[0].data) ? responses[0].data : []);
1591:      await fetchAllData(appUser);
1740:      await fetchAllData();
1806:        await fetchAllData();
1934:      fetchAllData();
2028:      await fetchAllData();
2063:      await fetchAllData();
2083:      await fetchAllData();
2395:    const searchedItems = searchQuery.trim()
2396:      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
2398:    const clientFilteredItems = activityClientFilter.trim()
2399:      ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
2401:    const typeFilteredItems = activityTypeFilter
2402:      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
 succeeded in 1.23s:
      setIsListening(false);
    }
  };

  const openActivityView = ({ type = null, search = '', client = '', date = '', timePeriod = null } = {}) => {
    setCurrentTab('activity');
    setActivityTypeFilter(type);
    setSearchQuery(search);
    setActivityClientFilter(client);
    setActivityDateFilter(date);
    setTimePeriodFilter(timePeriod);
  };

  const executeVoiceAction = (data) => {
    const { intent, slots = {} } = data || {};
    const nextTimePeriod = resolveVoiceTimePeriod(slots);
    const nextDate = resolveVoiceDateFilter(slots);
    const nextClient = slots.client_name || '';
    switch (intent) {
      case 'go_home':
 succeeded in 1.35s:
    );
  };

  const renderActivity = () => {
    const searchedItems = searchQuery.trim()
      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
      : items;
    const clientFilteredItems = activityClientFilter.trim()
      ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
      : searchedItems;
    const typeFilteredItems = activityTypeFilter
      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
      : clientFilteredItems;
    const exactDateFilteredItems = activityDateFilter
      ? typeFilteredItems.filter((item) => {
        const itemDate = getActivityItemDate(item);
        return itemDate && itemDate.toISOString().slice(0, 10) === activityDateFilter;
      })
      : typeFilteredItems;
    const filteredItems = timePeriodFilter
codex
I found the current filter flow: the timeline is a generic view over `items`, and voice actions only route to invoices, expenses, VAT, bookings, and home. I’m checking for any existing quote-specific intents or links now so I can wire the new section without breaking the current activity shortcuts.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-ChildItem -Path 'C:\\Users\\edebe\\eds\\bizPA\\frontend'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"intent\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"view_quotes|quotes|quote\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\eds succeeded in 1.07s:
1953:    const { intent, slots = {} } = data || {};
1957:    switch (intent) {
3168:      setQuarterActionError('Demo mode intentionally blocks redundant or simulated snapshot creation.');
 succeeded in 1.14s:
64:const MONETARY_TYPES = ['invoice', 'receipt', 'payment', 'quote'];
3837:            Monetary capture stays in draft until you review it here. Save an invoice, receipt, payment, or quote to open the preview.
3990:            <span className="meta-chip">Preview required for invoice, receipt, payment, quote</span>
3994:            {['invoice', 'receipt', 'payment', 'quote', 'booking', 'note'].map((type) => (
 succeeded in 1.25s:

    Directory: C:\Users\edebe\eds\bizPA\frontend

[32;1mMode   [0m[32;1m              LastWriteTime[0m [32;1;3m        Length[0m[32;1m Name[0m
[32;1m----   [0m [32;1m             -------------[0m [32;1m        ------[0m [32;1m----[0m
d----          02/03/2026    16:33                [44;1mandroid[0m
d----          18/03/2026    18:16                [44;1mbuild[0m
d----          24/02/2026    22:50                [44;1mnode_modules[0m
d----          21/02/2026    03:28                [44;1mpublic[0m
d----          18/03/2026    18:12                [44;1msrc[0m
-a---          02/03/2026    16:06            137 .env
-a---          25/02/2026    14:41            129 .gitignore
-a---          21/02/2026    03:54           2260 boot_log.txt
-a---          24/02/2026    19:30            181 capacitor.config.ts
-a---          25/02/2026    04:45         220632 frontend_boot_v3005_new.txt
-a---          23/02/2026    14:14           7000 frontend_boot_v3005.txt
-a---          23/02/2026    14:14           7880 frontend_boot.txt
-a---          24/02/2026    23:21         691674 package-lock.json
-a---          01/03/2026    23:32            985 package.json
-a---          06/03/2026    11:35              0 run_frontend_latest.err.log
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\package.json'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'git status --short' in C:\Users\edebe\eds succeeded in 1.19s:
{
  "name": "frontend",
  "version": "1.3.6",
  "description": "",
  "main": "index.js",
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "dependencies": {
    "@capacitor-community/speech-recognition": "^7.0.1",
    "@capacitor/preferences": "^8.0.1",
    "axios": "1.13.5",
    "bootstrap": "5.3.8",
    "lucide-react": "0.575.0",
 succeeded in 1.90s:
M  DataInsights/src/Constants.py
 M TradeApps
 M api_server_sql/main.py
 D grid_live_monitor.py
R  workstream/000_backlog/.keep -> workstream/000_epic/.keep
R  "workstream/000_backlog/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md" -> "workstream/000_epic/20260222_205900_pipHunter_signal_marketplace_mobile_functionality_v2 (3).md"
R  workstream/000_backlog/20260225_104010_live_market_data_pipeline_prompt.md -> workstream/000_epic/20260225_104010_live_market_data_pipeline_prompt.md
R  workstream/000_backlog/20260227_022357_sFX_Technical_Design_Brief_v2.md -> workstream/000_epic/20260227_022357_sFX_Technical_Design_Brief_v2.md
A  workstream/000_epic/20260305_185316_mvp_prd_quarterly_export_10min.md
A  workstream/000_epic/20260313_165611_bizPA_epic.md
A  "workstream/000_epic/20260313_165611_unassigned_Autonomous Trading Signal Platform.md"
A  workstream/000_epic/20260313_165611_unassigned_bizPA.md
A  workstream/000_epic/bizPA_disccussion.txt
R  workstream/000_backlog/claude/.keep -> workstream/000_epic/claude/.keep
A  workstream/000_epic/claude/20260305_100142_claude_etrmui_etrui_processed.md
R  workstream/000_backlog/codex/.keep -> workstream/000_epic/codex/.keep
R  workstream/000_backlog/codex/20260303_152309_codex_afrix_build_prompt_processed.md -> workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_processed.md
A  workstream/000_epic/codex/20260303_152309_codex_afrix_build_prompt_review.md
R  workstream/000_backlog/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md -> workstream/000_epic/codex/20260303_171914_codex_general_product_requirements_document__prd__-_sfx_processed.md
R  workstream/000_backlog/codex/20260304_142350_codex_linkage_verification_processed.md -> workstream/000_epic/codex/20260304_142350_codex_linkage_verification_processed.md
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[1917..1955]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[1248..1285]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[1448..1495]' in C:\Users\edebe\eds succeeded in 1.26s:
      readinessReport
    );
  };

  const fetchAllData = async (activeUser = currentUser) => {
    try {
      axios.defaults.headers.common['X-User-ID'] = activeUser.id;
      const inboxLoadStartedAt = typeof performance !== 'undefined' && typeof performance.now === 'function'
        ? performance.now()
        : Date.now();
      const endpoints = [
        'items',
        'upcoming',
        'stats/summary',
        'upcoming/notifications',
        'stats/momentum',
        'insights',
        'clients',
        'jobs',
        'calendar',
 succeeded in 1.20s:
  const [items, setItems] = useState([]);
  const [upcomingItems, setUpcomingItems] = useState([]);
  const [notifications, setNotifications] = useState([]);
  const [vatSummary, setVatSummary] = useState(null);
  const [momentum, setMomentum] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [connectionError, setConnectionError] = useState(null);
  const [transcript, setTranscript] = useState('');
  const [isListening, setIsListening] = useState(false);
  const [currentTab, setCurrentTab] = useState(requestedTab || (commandCentreDemoEnabled ? 'control' : 'home'));
  const [activityTypeFilter, setActivityTypeFilter] = useState(null);
  const [activityClientFilter, setActivityClientFilter] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [activityDateFilter, setActivityDateFilter] = useState('');
  const [timePeriodFilter, setTimePeriodFilter] = useState(null);
  const [clients, setClients] = useState([]);
  const [jobs, setJobs] = useState([]);
  const [calendarEvents, setCalendarEvents] = useState([]);
  const [diaryEntries, setDiaryEntries] = useState([]);
 succeeded in 1.26s:
    const cleanText = text.replace(/┬ú/g, 'GBP ');
    try {
      setVoiceStatus('processing');
      const response = await axios.post(`${API_BASE_URL}/voice/process`, {
        transcript: cleanText,
        device_id: 'mobile-v139',
        current_date: new Date().toISOString(),
      });
      if (response.data.confirmation_text && window.SpeechSynthesisUtterance) {
        try {
          const utterance = new window.SpeechSynthesisUtterance(response.data.confirmation_text);
          window.speechSynthesis.speak(utterance);
        } catch (_) {
        }
      }
      executeVoiceAction(response.data);
      fetchAllData();
    } catch (error) {
      alert('AI Error');
    } finally {
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"matchesActivityClientFilter|getActivityItemDate|matchesActivityTimePeriod|ACTIVITY_TIME_PERIOD_OPTIONS\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[930..1065]' in C:\Users\edebe\eds succeeded in 923ms:
678:const ACTIVITY_TIME_PERIOD_OPTIONS = [
685:const getActivityItemDate = (item) => {
695:const matchesActivityClientFilter = (item, clientFilter) => {
746:const matchesActivityTimePeriod = (item, periodKey) => {
751:  const itemDate = getActivityItemDate(item);
2399:      ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
2406:        const itemDate = getActivityItemDate(item);
2411:      ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
2414:      const activityDate = getActivityItemDate(item);
2440:              {ACTIVITY_TIME_PERIOD_OPTIONS.map((option) => (
 succeeded in 1.08s:
      existing.category_code = seed.category_code;
    }
    if (!existing.category_name && seed.category_name) {
      existing.category_name = seed.category_name;
    }
    if (!existing.split_business_pct && seed.split_business_pct !== null && seed.split_business_pct !== undefined) {
      existing.split_business_pct = seed.split_business_pct;
    }
    if (seed.is_split) {
      existing.is_split = true;
    }
    if (seed.duplicate_resolution) {
      existing.duplicate_resolution = seed.duplicate_resolution;
    }
    return existing;
  };

  queueRows.forEach((row) => {
    const card = ensureCard(row);
    if (!card) {
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"requestedTab\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[675..770]' in C:\Users\edebe\eds succeeded in 829ms:
1248:  const requestedTab = searchParams?.get('tab');
1259:  const [currentTab, setCurrentTab] = useState(requestedTab || (commandCentreDemoEnabled ? 'control' : 'home'));
1329:        setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
1368:  }, [currentUser, inboxDemoEnabled, readinessDemoEnabled, requestedTab, snapshotDemoEnabled]);
1409:      setCurrentTab(requestedTab || 'control');
1411:  }, [captureDemoEnabled, commandCentreDemoEnabled, requestedTab]);
1415:      setCurrentTab(requestedTab || (inboxDemoEnabled ? 'inbox' : 'quarter'));
1417:  }, [inboxDemoEnabled, readinessDemoEnabled, requestedTab, snapshotDemoEnabled]);
 succeeded in 943ms:
});

const ACTIVITY_TIME_PERIOD_OPTIONS = [
  { value: '', label: 'All dates' },
  { value: 'today', label: 'Today' },
  { value: 'this_week', label: 'This week' },
  { value: 'last_week', label: 'Last week' },
];

const getActivityItemDate = (item) => {
  const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
  if (!dateValue) {
    return null;
  }

  const parsedDate = new Date(dateValue);
  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
};

const matchesActivityClientFilter = (item, clientFilter) => {
codex
I’ve confirmed there’s no existing quote intent handling on the frontend. I’m checking the backend voice contract in the workspace next so I can map the right intent name if it already exists, and only add a frontend fallback if needed.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"view_quotes|quote\" 'C:\\Users\\edebe\\eds\\api_server_sql' 'C:\\Users\\edebe\\eds\\bizPA'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"voice/process|intent.*view_|view_invoices|view_expenses|view_bookings|view_vat\" 'C:\\Users\\edebe\\eds'" in C:\Users\edebe\eds exited 124 in 20.43s:
C:\Users\edebe\eds\bizPA\260217_2300_voice_first_deliverables_breakdown_checklist.md:167:  - quote follow-up
C:\Users\edebe\eds\bizPA\260217_2310_WS1_PRODUCT_UX_Flows_and_Dialogues_draft.md:37:- Command: "Note customer wants quote for tiling"
C:\Users\edebe\eds\bizPA\app\android\gradlew:225:# Use "xargs" to parse quoted args.
C:\Users\edebe\eds\bizPA\app\android\gradlew:227:# With -n1 it outputs one arg per line, with the quotes and backslashes removed.
C:\Users\edebe\eds\bizPA\app\android\gradlew:241:# an unmatched quote.
C:\Users\edebe\eds\bizPA\business_activity_inbox_preview.html:94:      <div>Immutable event history across quotes, payments, alerts, and operator review workflows.</div>
C:\Users\edebe\eds\bizPA\business_activity_inbox_preview.html:123:      { event_id: 'e3', event_title: 'quote converted to invoice', timestamp: '2026-03-11T07:15:00Z', linked_entity_type: 'quote', linked_entity: { reference_number: 'QT-7710', counterparty_name: 'Elm Court Management' }, amount: 'GBP 2250.00', description: 'Operator-approved quote conversion completed successfully.', badges: [['Converted', 'info'], ['Auto-Commit', 'warning']], filter_tags: ['all', 'financial', 'quotes'] },
C:\Users\edebe\eds\bizPA\business_activity_inbox_preview.html:131:      ['quotes', 'Quotes'],
C:\Users\edebe\eds\bizPA\business_entity_deep_dive_preview.html:189:        <div class="subtle">Scoped operator view for one invoice, receipt, quote, payment, or note at a time.</div>
C:\Users\edebe\eds\bizPA\business_entity_deep_dive_preview.html:262:      quote: {
C:\Users\edebe\eds\bizPA\business_entity_deep_dive_preview.html:263:        entityType: 'quote',
C:\Users\edebe\eds\bizPA\business_entity_deep_dive_preview.html:266:        description: 'Quote view shows the approved commercial context, available conversion action, and only quote-linked activity.',
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:6211:[VoiceController] Normalizing text: "show me quotes"
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:6212:[VoiceController] Intent matched: capture_quote
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:6213:[VoiceController] Final Parse: intent=capture_quote, confidence=0.95
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:6214:[VoiceController] Parsed: intent=capture_quote, confidence=0.95, slots={"labels":[]}
C:\Users\edebe\eds\bizPA\docs\canonical_entity_event_schemas.md:32:| `quote` | same monetary field set | `composition`, `committed`, `sent`, `accepted`, `expired`, `converted`, `voided` | Yes | Yes |
C:\Users\edebe\eds\bizPA\docs\canonical_entity_event_schemas.md:83:- `quote_converted`
C:\Users\edebe\eds\bizPA\small_trader_capture_app_build_prompt_voice_first.md:53:- “**Note**: customer wants quote for tiling” → create note item + label as follow-up lead  
C:\Users\edebe\eds\bizPA\small_trader_capture_app_build_prompt_voice_first.md:166:- `status`: `lead | quoted | booked | in_progress | completed | lost`  
 exited 124 in 20.48s:
C:\Users\edebe\eds\bizPA\docs\api_endpoint_inventory.md:31:| POST | `/api/v1/voice/process` | Submit audio for server-side ASR/NLU. | `voice:process` |
C:\Users\edebe\eds\bizPA\frontend\src\App.jsx:1921:      const response = await axios.post(`${API_BASE_URL}/voice/process`, {
C:\Users\edebe\eds\bizPA\frontend\src\App.jsx:1961:      case 'view_expenses':
C:\Users\edebe\eds\bizPA\frontend\src\App.jsx:1969:      case 'view_invoices':
C:\Users\edebe\eds\bizPA\frontend\src\App.jsx:1977:      case 'view_vat':
C:\Users\edebe\eds\bizPA\frontend\src\App.jsx:1980:      case 'view_bookings':
C:\Users\edebe\eds\bizPA\backend\boot_log.txt:9:[0mPOST /api/v1/voice/process [32m200[0m 440.530 ms - 307[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:168:[0mPOST /api/v1/voice/process [32m200[0m 312.936 ms - 275[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:177:[0mPOST /api/v1/voice/process [32m200[0m 29.733 ms - 230[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:185:[0mPOST /api/v1/voice/process [32m200[0m 26.632 ms - 252[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:193:[0mPOST /api/v1/voice/process [32m200[0m 22.491 ms - 217[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:201:[0mPOST /api/v1/voice/process [32m200[0m 27.721 ms - 230[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:208:[0mPOST /api/v1/voice/process [32m200[0m 12.383 ms - 249[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_new.txt:217:[0mPOST /api/v1/voice/process [32m200[0m 23.231 ms - 238[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2593:[0mPOST /api/v1/voice/process [32m200[0m 510.675 ms - 238[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2632:[0mPOST /api/v1/voice/process [32m200[0m 45.535 ms - 279[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2655:[0mPOST /api/v1/voice/process [32m200[0m 192.961 ms - 231[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2709:[0mPOST /api/v1/voice/process [32m200[0m 85.590 ms - 170[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2730:[0mPOST /api/v1/voice/process [32m200[0m 131.492 ms - 168[0m
C:\Users\edebe\eds\bizPA\backend\backend_boot_v5055_m2_fixed_2.txt:2766:[0mPOST /api/v1/voice/process [32m200[0m 90.237 ms - 171[0m
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"\\bHistory\\b|ArchiveRestore|ArrowRight|Plus|Wallet\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"const currencyValue|function currencyValue|currencyValue =\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\eds succeeded in 1.00s:
4:  ArchiveRestore,
5:  ArrowRight,
16:  History,
22:  Plus,
29:  Wallet,
2258:                <Plus size={18} />
2263:                <ArrowRight size={16} />
2297:                <Wallet size={16} />
2599:            <ArrowRight size={16} />
2603:            {inboxBusyId === 'undo-last' ? <RefreshCcw size={16} className="spinner" /> : <ArchiveRestore size={16} />}
3450:                  <Plus size={16} />
3513:                    <h6><Plus size={16} /> Added transactions</h6>
3528:                    <h6><ArchiveRestore size={16} /> Adjustments and removals</h6>
3731:              <div className="status-pill"><History size={14} /> {activityEvents.length} events</div>
 succeeded in 1.12s:
792:const currencyValue = (value) => {
codex
I’ve got enough context to implement this cleanly.

Plan:
1. Refactor the activity filtering/render path so Timeline excludes quotes by default and a dedicated Quotes screen can reuse the same filter controls.
   Test: `npm run build` in `bizPA/frontend` passes.
2. Add the Quotes navigation target and wire quote-specific routing from voice actions and quote confirmations.
   Test: `npm run build` still passes and the frontend source shows `view_quotes` routed to `quotes`.
3. Update the lifecycle task file to the required template, mark completed checklist items with evidence, record validation, and leave it in the correct status based on user-visible verification rules.
   Test: task file contains ordered checked steps, evidence inventory, validation results, and an explicit verification request entry.
codex
I’m editing `App.jsx` now to split quotes out of the timeline, add the dedicated tab, and route quote actions there instead of back into the general feed.
file update
M C:\Users\edebe\eds\bizPA\frontend\src\App.jsx
@@ -1951,2 +1951,11 @@
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
@@ -1976,2 +1985,9 @@
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
@@ -2028,3 +2044,3 @@
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
@@ -2063,3 +2079,3 @@
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
@@ -2393,6 +2409,6 @@
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
@@ -2400,4 +2416,4 @@
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
@@ -2412,12 +2428,19 @@
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
@@ -2425,3 +2448,3 @@
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
@@ -2468,3 +2491,3 @@
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
@@ -2476,6 +2499,4 @@
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
@@ -2498,3 +2519,3 @@
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
@@ -2509,2 +2530,49 @@
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
@@ -4161,2 +4229,3 @@
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
@@ -4176,2 +4245,3 @@
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
apply_patch(auto_approved=true) exited 0 in 367ms:
Success. Updated the following files:
M C:\Users\edebe\eds\bizPA\frontend\src\App.jsx
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

codex
The UI split is in place. I’m reading back the edited sections now for syntax/flow issues before running the frontend build, then I’ll update the task file with evidence from the actual validation output.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[2390..2575]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[1938..2015]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[4152..4195]' in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[2020..2070]' in C:\Users\edebe\eds succeeded in 1.58s:
            <button className="primary-action" onClick={submitManualEntry} disabled={manualSaving}>
              {manualSaving ? <RefreshCcw size={16} className="spinner" /> : null}
              {isMonetaryType(manualForm.type) ? `Preview ${manualForm.type}` : `Save ${manualForm.type}`}
            </button>
            <button className="secondary-action" onClick={() => resetManualCapture(manualForm.type)} disabled={manualSaving || previewBusy}>
              Clear
            </button>
          </div>
        </div>
        {renderPreviewPanel()}
      </div>
    </div>
  );

  return (
    <div className="container py-3 shell">
      <style>{styles}</style>
      {onboardingRequired ? (
        <OnboardingGate
          busy={onboardingBusy}
 succeeded in 1.63s:
      setIsListening(false);
    }
  };

  const openActivityView = ({ type = null, search = '', client = '', date = '', timePeriod = null } = {}) => {
    setCurrentTab('activity');
    setActivityTypeFilter(type);
    setSearchQuery(search);
    setActivityClientFilter(client);
    setActivityDateFilter(date);
    setTimePeriodFilter(timePeriod);
  };

  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
    setCurrentTab('quotes');
    setActivityTypeFilter(null);
    setSearchQuery(search);
    setActivityClientFilter(client);
    setActivityDateFilter(date);
    setTimePeriodFilter(timePeriod);
 succeeded in 1.77s:
                </div>
                <div>
                  <div className="feed-tag">{feedItem.tag}</div>
                  <strong style={{ marginTop: 8 }}>{feedItem.title}</strong>
                  <small>{feedItem.detail}</small>
                </div>
                {feedItem.dismissible ? (
                  <button className="attention-action" onClick={() => dismissInsight(feedItem.id)}>Dismiss</button>
                ) : (
                  <button className="attention-action" onClick={() => setCurrentTab('quarter')}>Open</button>
                )}
              </div>
            ))}
          </div>
        </section>
      </div>
    );
  };

  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
 succeeded in 1.55s:
    if (isMonetaryType(manualForm.type) && !manualForm.grossAmount) {
      setPreviewError('Gross amount is required for monetary preview.');
      return;
    }

    try {
      setManualSaving(true);
      setPreviewError('');
      const payload = buildManualPayload(manualForm);
      const response = await axios.post(`${API_BASE_URL}/items`, payload);

      if (response.data?.action_status === 'preview_required') {
        setPreviewDraft({
          compositionId: response.data.composition_id,
          preview: response.data.preview,
          rawNote: manualForm.note.trim(),
        });
        setPreviewForm(buildPreviewForm(response.data.preview, manualForm.note.trim()));
        setPreviewMode('review');
        return;
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[4170..4205]' in C:\Users\edebe\eds succeeded in 850ms:
        <OnboardingGate
          busy={onboardingBusy}
          errorMessage={onboardingError}
          onSubmit={completeOnboarding}
        />
      ) : (
        <>
      <header className="d-flex justify-content-between align-items-center mb-3 flex-wrap gap-2">
        <div>
          <h2 onClick={() => setCurrentTab('home')} style={{ cursor: 'pointer', marginBottom: 0 }}>
            bizPA <span className="badge text-bg-warning" style={{ fontSize: '0.5rem' }}>v1.3.9</span>
          </h2>
          <div className="d-flex align-items-center flex-wrap gap-2 mt-1">
            <small className="small-muted">{currentUser.name} · {currentRoleLabel}</small>
            <div className={`mode-badge ${autoCommitVisibility.headerTone}`}>{autoCommitVisibility.headerBadge}</div>
          </div>
        </div>
        <div className="header-controls">
          <select className="header-select" value={currentUser.id} onChange={(event) => switchUser(event.target.value)}>
            {appUsers.map((user) => (
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command '$path='"'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'; "'$lines=Get-Content $path; $lines[4210..4250]' in C:\Users\edebe\eds succeeded in 1.07s:
          <strong>{autoCommitVisibility.bannerTitle}</strong>
          <div className="small-muted">{autoCommitVisibility.bannerDetail}</div>
        </div>
        <button className="secondary-action" onClick={() => setCurrentTab('control')}>
          Review control centre
        </button>
      </section>
      {connectionError && <div className="alert alert-danger">{connectionError}</div>}

      {loading ? (
        <div className="text-center py-5">Loading...</div>
      ) : (
        <div style={{ paddingBottom: '100px' }}>
          {currentTab === 'home' && renderDashboard()}
          {currentTab === 'add' && renderAdd()}
          {currentTab === 'control' && renderControlCentre()}
          {currentTab === 'inbox' && renderInbox()}
          {currentTab === 'quarter' && renderQuarter()}
          {currentTab === 'activity' && renderActivity()}
          {currentTab === 'quotes' && renderQuotes()}
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command 'npm run build' in C:\Users\edebe\eds\bizPA\frontend succeeded in 24.84s:

> frontend@1.3.6 build
> react-scripts build

Creating an optimized production build...
Compiled successfully.

File sizes after gzip:

  116.81 kB (+572 B)  build\static\js\main.c3d32cd2.js
  659 B               build\static\js\828.89358f49.chunk.js
  314 B               build\static\js\940.c568d512.chunk.js

The project was built assuming it is hosted at /.
You can control this with the homepage field in your package.json.

The build folder is ready to be deployed.
You may serve it with a static server:

  npm install -g serve
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

codex
The build is clean. I’m gathering precise line references and command evidence now, then I’ll rewrite the task file into the lifecycle format with completed checks and the remaining user-verification status.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\bizPA\\backend\\src\\services\\voiceCaptureParserService.js' | Select-Object -First 120" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "rg -n \"openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'\" 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\eds succeeded in 1.03s:
1952:  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
1986:      case 'view_quotes':
1987:        openQuotesView({
2045:      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
2080:      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
2543:  const renderQuotes = () => {
4230:          {currentTab === 'quotes' && renderQuotes()}
4246:          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
 succeeded in 1.14s:
const INTENT_CONFIG = {
  capture_invoice: {
    entityType: 'invoice',
    keywords: ['invoice', 'bill', 'charge', 'billing', 'raise invoice', 'new invoice'],
    requiredFields: ['amount', 'counterparty_name']
  },
  capture_receipt: {
    entityType: 'receipt',
    keywords: ['receipt', 'expense', 'spent', 'purchase', 'bought', 'fuel', 'petrol', 'parking', 'materials'],
    requiredFields: ['amount']
  },
  capture_quote: {
    entityType: 'quote',
    keywords: ['quote', 'estimate', 'proposal', 'pro forma'],
    requiredFields: ['amount', 'counterparty_name']
  },
  capture_payment: {
    entityType: 'payment',
    keywords: ['payment', 'paid', 'received', 'income', 'bank transfer', 'transferred', 'settled'],
    requiredFields: ['amount', 'counterparty_name']
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..53e397c338b314a6f786261e738f393a5ec436c1
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -1949,6 +1949,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +1983,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2042,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2077,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2407,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2426,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2489,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2497,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2517,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2528,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4227,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4243,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

codex
I’m updating the lifecycle document now. I’m keeping the implementation and build validation fully evidenced, and I’m leaving completion in `Awaiting user verification` because this changes visible navigation and the lifecycle rule requires an explicit verification pass from you.
exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git diff -- 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Date -Format 'yyyy-MM-dd HH:mm:ss'" in C:\Users\edebe\eds succeeded in 1.25s:
2026-03-18 18:25:10
 succeeded in 1.27s:

file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..0849a6a4e34e5c982e3f266959a53ebc4cd8994e
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -2026,7 +2115,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2150,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2480,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2499,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
+
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
 
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2562,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2570,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2590,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2601,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4300,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4316,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },

file update
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md
# TASK: bizPA Dedicated Quotes Section

Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`

## 1. Task Summary
Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.

## 2. Context
- Affected Files: `bizPA/frontend/src/App.jsx`
- Current State: Quotes are viewed by filtering the Timeline by 'quote'.

## 3. Implementation Log
- (Pending) Add 'Quotes' to bottom navigation.
- (Pending) Create `renderQuotes` function in `App.jsx`.
- (Pending) Update voice navigation to switch to this dedicated section.

## 4. Completion Status
**TODO** - 2026-03-01



## Execution Evidence
- Agent lane: gemini
- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
- Return code: 0
- Stdout:
```text
gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
```


## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 345ms:
Success. Updated the following files:
D C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
deleted file mode 100644
index cedd6df7cb4aa91a34527114812235198441b01f..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ /dev/null
@@ -1,34 +0,0 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
deleted file mode 100644
index cedd6df7cb4aa91a34527114812235198441b01f..0000000000000000000000000000000000000000
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ /dev/null
@@ -1,34 +0,0 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29

file update
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md
Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`

## Task Summary
Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.

## Context
- Affected Files: `bizPA/frontend/src/App.jsx`
- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.

## Dependency
Dependency: None

## Plan
- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
- [ ] 3. Request user verification for the visible navigation and feed behavior change.
  - [ ] Test: Ask the user to verify that the bottom navigation exposes Quotes, the Timeline no longer shows quote records by default, and the quote-specific navigation flow behaves as expected.
  - Evidence: Pending user pass/fail feedback in the conversation.

## Evidence
Objective-Delivery-Coverage: 85%
Auto-Acceptance: false
- Evidence-Type: test_output
  - Artifact: `npm run build` in `bizPA/frontend` on 2026-03-18 18:25:10; result included `Compiled successfully.` and emitted `build\\static\\js\\main.c3d32cd2.js`.
  - Objective-Proved: The modified React app compiles successfully after the dedicated Quotes view and routing changes.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `bizPA/frontend/src/App.jsx` line references 1952, 1986, 2045, 2080, 2543, 4230, 4246.
  - Objective-Proved: The frontend contains a dedicated Quotes screen, navigation target, quote-specific routing, and quote save redirection.
  - Status: captured
- Evidence-Type: file_output
  - Artifact: `bizPA/backend/src/services/voiceCaptureParserService.js` includes `intent: 'view_quotes'`.
  - Objective-Proved: The existing backend voice contract already exposes a quote-navigation intent that the frontend now consumes.
  - Status: captured
- Evidence-Type: manual_verification
  - Artifact: User verification request to confirm Quotes navigation, Timeline exclusion of quotes, and quote voice navigation behavior.
  - Objective-Proved: Final user-visible behavior matches the requested UX change in a real session.
  - Status: planned

## Implementation Log
- 2026-03-01: Initial task created with pending notes to add Quotes navigation, create a dedicated render function, and update voice navigation.
- 2026-03-18 17:21:29: Retry scheduled for the task.
- 2026-03-18 18:03-18:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the in-progress task file, and inspected `bizPA/frontend/src/App.jsx` plus the backend voice parser contract.
- 2026-03-18 18:20-18:24: Refactored activity rendering into shared filtering helpers, introduced `renderQuotes`, excluded `quote` items from the general Timeline source list, and added a Quotes bottom-nav target.
- 2026-03-18 18:24-18:25: Wired `view_quotes` to `openQuotesView`, and redirected manual quote save plus quote preview confirmation flows into the dedicated Quotes section.
- 2026-03-18 18:25:10: Ran `npm run build` in `bizPA/frontend`; build completed successfully.
- 2026-03-18 18:25:10: Updated this lifecycle file with ordered checklist evidence and marked the task as awaiting user verification because the change is user-visible.

## Changes Made
- `bizPA/frontend/src/App.jsx`
  - Added `openQuotesView` to route quote-specific navigation without leaving Timeline filters stuck on `quote`.
  - Added `view_quotes` handling in `executeVoiceAction`.
  - Redirected manual quote save and confirmed quote preview flows to `currentTab = 'quotes'`.
  - Extracted shared activity filtering/render helpers for reuse across Timeline and Quotes views.
  - Updated `renderActivity` to exclude `quote` items from the general Timeline source list.
  - Added `renderQuotes` with a dedicated summary header and quote-only list rendering.
  - Added `quotes` to the bottom navigation and conditional render block.
- `bizPA/backend/src/services/voiceCaptureParserService.js`
  - No code change required; verified existing `view_quotes` intent support as the frontend integration target.

## Validation
- 2026-03-18 18:25:10: Ran `npm run build` from `C:\Users\edebe\eds\bizPA\frontend`.
  - Result: Pass.
  - Summary:
    - `Creating an optimized production build...`
    - `Compiled successfully.`
    - Output bundle emitted under `build\static\js\`.
- 2026-03-18 18:25:10: Verified source integration points with `rg -n "openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'" bizPA/frontend/src/App.jsx`.
  - Result: Pass.
  - Summary: Located quote routing and rendering references at lines 1952, 1986, 2045, 2080, 2543, 4230, and 4246.
- 2026-03-18 18:25:10: Verified backend intent contract with `Get-Content bizPA/backend/src/services/voiceCaptureParserService.js | Select-Object -First 120`.
  - Result: Pass.
  - Summary: Confirmed `QUERY_INTENTS` includes `intent: 'view_quotes'`.
- 2026-03-18 18:25:10: User verification request prepared for final response.
  - Result: Pending.
  - Summary: Awaiting explicit user pass/fail on visible UI behavior.

## Risks/Notes
- No browser-driven manual UI session was run in this task; validation is compile-time plus source-contract verification.
- The bottom navigation now includes both Capture and Quotes using `FileText` icons; behavior is correct, but icon differentiation may be worth a later UX pass if visual distinction matters.
- Task remains in `workstream/200_inprogress` until user verification is provided per lifecycle rules for visible UI changes.

## Completion Status
**Awaiting user verification** - 2026-03-18 18:25:10

## Legacy Execution Evidence
- Agent lane: gemini
- Command: `cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md`
- Return code: `0`
- Stdout:
```text
gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
```

## Retry History
Retry-Count: 1
- Retry scheduled at 2026-03-18 17:21:29
apply_patch(auto_approved=true) exited 0 in 840ms:
Success. Updated the following files:
A C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
index cedd6df7cb4aa91a34527114812235198441b01f..311e73b29f04474a43fe648d79d268090dc68fd9
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
@@ -1,34 +1,102 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`
+
+## Task Summary
+Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.
+
+## Context
+- Affected Files: `bizPA/frontend/src/App.jsx`
+- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
+- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.
+
+## Dependency
+Dependency: None
+
+## Plan
+- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
+  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
+- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
+  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
+- [ ] 3. Request user verification for the visible navigation and feed behavior change.
+  - [ ] Test: Ask the user to verify that the bottom navigation exposes Quotes, the Timeline no longer shows quote records by default, and the quote-specific navigation flow behaves as expected.
+  - Evidence: Pending user pass/fail feedback in the conversation.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: test_output
+  - Artifact: `npm run build` in `bizPA/frontend` on 2026-03-18 18:25:10; result included `Compiled successfully.` and emitted `build\\static\\js\\main.c3d32cd2.js`.
+  - Objective-Proved: The modified React app compiles successfully after the dedicated Quotes view and routing changes.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/frontend/src/App.jsx` line references 1952, 1986, 2045, 2080, 2543, 4230, 4246.
+  - Objective-Proved: The frontend contains a dedicated Quotes screen, navigation target, quote-specific routing, and quote save redirection.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/backend/src/services/voiceCaptureParserService.js` includes `intent: 'view_quotes'`.
+  - Objective-Proved: The existing backend voice contract already exposes a quote-navigation intent that the frontend now consumes.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request to confirm Quotes navigation, Timeline exclusion of quotes, and quote voice navigation behavior.
+  - Objective-Proved: Final user-visible behavior matches the requested UX change in a real session.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-01: Initial task created with pending notes to add Quotes navigation, create a dedicated render function, and update voice navigation.
+- 2026-03-18 17:21:29: Retry scheduled for the task.
+- 2026-03-18 18:03-18:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the in-progress task file, and inspected `bizPA/frontend/src/App.jsx` plus the backend voice parser contract.
+- 2026-03-18 18:20-18:24: Refactored activity rendering into shared filtering helpers, introduced `renderQuotes`, excluded `quote` items from the general Timeline source list, and added a Quotes bottom-nav target.
+- 2026-03-18 18:24-18:25: Wired `view_quotes` to `openQuotesView`, and redirected manual quote save plus quote preview confirmation flows into the dedicated Quotes section.
+- 2026-03-18 18:25:10: Ran `npm run build` in `bizPA/frontend`; build completed successfully.
+- 2026-03-18 18:25:10: Updated this lifecycle file with ordered checklist evidence and marked the task as awaiting user verification because the change is user-visible.
+
+## Changes Made
+- `bizPA/frontend/src/App.jsx`
+  - Added `openQuotesView` to route quote-specific navigation without leaving Timeline filters stuck on `quote`.
+  - Added `view_quotes` handling in `executeVoiceAction`.
+  - Redirected manual quote save and confirmed quote preview flows to `currentTab = 'quotes'`.
+  - Extracted shared activity filtering/render helpers for reuse across Timeline and Quotes views.
+  - Updated `renderActivity` to exclude `quote` items from the general Timeline source list.
+  - Added `renderQuotes` with a dedicated summary header and quote-only list rendering.
+  - Added `quotes` to the bottom navigation and conditional render block.
+- `bizPA/backend/src/services/voiceCaptureParserService.js`
+  - No code change required; verified existing `view_quotes` intent support as the frontend integration target.
+
+## Validation
+- 2026-03-18 18:25:10: Ran `npm run build` from `C:\Users\edebe\eds\bizPA\frontend`.
+  - Result: Pass.
+  - Summary:
+    - `Creating an optimized production build...`
+    - `Compiled successfully.`
+    - Output bundle emitted under `build\static\js\`.
+- 2026-03-18 18:25:10: Verified source integration points with `rg -n "openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'" bizPA/frontend/src/App.jsx`.
+  - Result: Pass.
+  - Summary: Located quote routing and rendering references at lines 1952, 1986, 2045, 2080, 2543, 4230, and 4246.
+- 2026-03-18 18:25:10: Verified backend intent contract with `Get-Content bizPA/backend/src/services/voiceCaptureParserService.js | Select-Object -First 120`.
+  - Result: Pass.
+  - Summary: Confirmed `QUERY_INTENTS` includes `intent: 'view_quotes'`.
+- 2026-03-18 18:25:10: User verification request prepared for final response.
+  - Result: Pending.
+  - Summary: Awaiting explicit user pass/fail on visible UI behavior.
+
+## Risks/Notes
+- No browser-driven manual UI session was run in this task; validation is compile-time plus source-contract verification.
+- The bottom navigation now includes both Capture and Quotes using `FileText` icons; behavior is correct, but icon differentiation may be worth a later UX pass if visual distinction matters.
+- Task remains in `workstream/200_inprogress` until user verification is provided per lifecycle rules for visible UI changes.
+
+## Completion Status
+**Awaiting user verification** - 2026-03-18 18:25:10
+
+## Legacy Execution Evidence
+- Agent lane: gemini
+- Command: `cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md`
+- Return code: `0`
+- Stdout:
+```text
+gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
index cedd6df7cb4aa91a34527114812235198441b01f..311e73b29f04474a43fe648d79d268090dc68fd9
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
@@ -1,34 +1,102 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`
+
+## Task Summary
+Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.
+
+## Context
+- Affected Files: `bizPA/frontend/src/App.jsx`
+- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
+- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.
+
+## Dependency
+Dependency: None
+
+## Plan
+- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
+  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
+- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
+  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
+- [ ] 3. Request user verification for the visible navigation and feed behavior change.
+  - [ ] Test: Ask the user to verify that the bottom navigation exposes Quotes, the Timeline no longer shows quote records by default, and the quote-specific navigation flow behaves as expected.
+  - Evidence: Pending user pass/fail feedback in the conversation.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: test_output
+  - Artifact: `npm run build` in `bizPA/frontend` on 2026-03-18 18:25:10; result included `Compiled successfully.` and emitted `build\\static\\js\\main.c3d32cd2.js`.
+  - Objective-Proved: The modified React app compiles successfully after the dedicated Quotes view and routing changes.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/frontend/src/App.jsx` line references 1952, 1986, 2045, 2080, 2543, 4230, 4246.
+  - Objective-Proved: The frontend contains a dedicated Quotes screen, navigation target, quote-specific routing, and quote save redirection.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/backend/src/services/voiceCaptureParserService.js` includes `intent: 'view_quotes'`.
+  - Objective-Proved: The existing backend voice contract already exposes a quote-navigation intent that the frontend now consumes.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request to confirm Quotes navigation, Timeline exclusion of quotes, and quote voice navigation behavior.
+  - Objective-Proved: Final user-visible behavior matches the requested UX change in a real session.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-01: Initial task created with pending notes to add Quotes navigation, create a dedicated render function, and update voice navigation.
+- 2026-03-18 17:21:29: Retry scheduled for the task.
+- 2026-03-18 18:03-18:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the in-progress task file, and inspected `bizPA/frontend/src/App.jsx` plus the backend voice parser contract.
+- 2026-03-18 18:20-18:24: Refactored activity rendering into shared filtering helpers, introduced `renderQuotes`, excluded `quote` items from the general Timeline source list, and added a Quotes bottom-nav target.
+- 2026-03-18 18:24-18:25: Wired `view_quotes` to `openQuotesView`, and redirected manual quote save plus quote preview confirmation flows into the dedicated Quotes section.
+- 2026-03-18 18:25:10: Ran `npm run build` in `bizPA/frontend`; build completed successfully.
+- 2026-03-18 18:25:10: Updated this lifecycle file with ordered checklist evidence and marked the task as awaiting user verification because the change is user-visible.
+
+## Changes Made
+- `bizPA/frontend/src/App.jsx`
+  - Added `openQuotesView` to route quote-specific navigation without leaving Timeline filters stuck on `quote`.
+  - Added `view_quotes` handling in `executeVoiceAction`.
+  - Redirected manual quote save and confirmed quote preview flows to `currentTab = 'quotes'`.
+  - Extracted shared activity filtering/render helpers for reuse across Timeline and Quotes views.
+  - Updated `renderActivity` to exclude `quote` items from the general Timeline source list.
+  - Added `renderQuotes` with a dedicated summary header and quote-only list rendering.
+  - Added `quotes` to the bottom navigation and conditional render block.
+- `bizPA/backend/src/services/voiceCaptureParserService.js`
+  - No code change required; verified existing `view_quotes` intent support as the frontend integration target.
+
+## Validation
+- 2026-03-18 18:25:10: Ran `npm run build` from `C:\Users\edebe\eds\bizPA\frontend`.
+  - Result: Pass.
+  - Summary:
+    - `Creating an optimized production build...`
+    - `Compiled successfully.`
+    - Output bundle emitted under `build\static\js\`.
+- 2026-03-18 18:25:10: Verified source integration points with `rg -n "openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'" bizPA/frontend/src/App.jsx`.
+  - Result: Pass.
+  - Summary: Located quote routing and rendering references at lines 1952, 1986, 2045, 2080, 2543, 4230, and 4246.
+- 2026-03-18 18:25:10: Verified backend intent contract with `Get-Content bizPA/backend/src/services/voiceCaptureParserService.js | Select-Object -First 120`.
+  - Result: Pass.
+  - Summary: Confirmed `QUERY_INTENTS` includes `intent: 'view_quotes'`.
+- 2026-03-18 18:25:10: User verification request prepared for final response.
+  - Result: Pending.
+  - Summary: Awaiting explicit user pass/fail on visible UI behavior.
+
+## Risks/Notes
+- No browser-driven manual UI session was run in this task; validation is compile-time plus source-contract verification.
+- The bottom navigation now includes both Capture and Quotes using `FileText` icons; behavior is correct, but icon differentiation may be worth a later UX pass if visual distinction matters.
+- Task remains in `workstream/200_inprogress` until user verification is provided per lifecycle rules for visible UI changes.
+
+## Completion Status
+**Awaiting user verification** - 2026-03-18 18:25:10
+
+## Legacy Execution Evidence
+- Agent lane: gemini
+- Command: `cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md`
+- Return code: `0`
+- Stdout:
+```text
+gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

exec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "Get-Content -Path 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260301_235502_gemini_bizpa_add_quotes_section.md'" in C:\Users\edebe\edsexec
"C:\\Program Files\\PowerShell\\7\\pwsh.exe" -Command "git status --short -- 'C:\\Users\\edebe\\eds\\bizPA\\frontend\\src\\App.jsx' 'C:\\Users\\edebe\\eds\\workstream\\200_inprogress\\codex\\20260301_235502_gemini_bizpa_add_quotes_section.md'" in C:\Users\edebe\eds succeeded in 1.24s:
?? workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
 succeeded in 1.33s:
Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`

## Task Summary
Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.

## Context
- Affected Files: `bizPA/frontend/src/App.jsx`
- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.

## Dependency
Dependency: None

## Plan
- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
index cedd6df7cb4aa91a34527114812235198441b01f..311e73b29f04474a43fe648d79d268090dc68fd9
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
@@ -1,34 +1,102 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`
+
+## Task Summary
+Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.
+
+## Context
+- Affected Files: `bizPA/frontend/src/App.jsx`
+- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
+- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.
+
+## Dependency
+Dependency: None
+
+## Plan
+- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
+  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
+- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
+  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
+- [ ] 3. Request user verification for the visible navigation and feed behavior change.
+  - [ ] Test: Ask the user to verify that the bottom navigation exposes Quotes, the Timeline no longer shows quote records by default, and the quote-specific navigation flow behaves as expected.
+  - Evidence: Pending user pass/fail feedback in the conversation.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: test_output
+  - Artifact: `npm run build` in `bizPA/frontend` on 2026-03-18 18:25:10; result included `Compiled successfully.` and emitted `build\\static\\js\\main.c3d32cd2.js`.
+  - Objective-Proved: The modified React app compiles successfully after the dedicated Quotes view and routing changes.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/frontend/src/App.jsx` line references 1952, 1986, 2045, 2080, 2543, 4230, 4246.
+  - Objective-Proved: The frontend contains a dedicated Quotes screen, navigation target, quote-specific routing, and quote save redirection.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/backend/src/services/voiceCaptureParserService.js` includes `intent: 'view_quotes'`.
+  - Objective-Proved: The existing backend voice contract already exposes a quote-navigation intent that the frontend now consumes.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request to confirm Quotes navigation, Timeline exclusion of quotes, and quote voice navigation behavior.
+  - Objective-Proved: Final user-visible behavior matches the requested UX change in a real session.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-01: Initial task created with pending notes to add Quotes navigation, create a dedicated render function, and update voice navigation.
+- 2026-03-18 17:21:29: Retry scheduled for the task.
+- 2026-03-18 18:03-18:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the in-progress task file, and inspected `bizPA/frontend/src/App.jsx` plus the backend voice parser contract.
+- 2026-03-18 18:20-18:24: Refactored activity rendering into shared filtering helpers, introduced `renderQuotes`, excluded `quote` items from the general Timeline source list, and added a Quotes bottom-nav target.
+- 2026-03-18 18:24-18:25: Wired `view_quotes` to `openQuotesView`, and redirected manual quote save plus quote preview confirmation flows into the dedicated Quotes section.
+- 2026-03-18 18:25:10: Ran `npm run build` in `bizPA/frontend`; build completed successfully.
+- 2026-03-18 18:25:10: Updated this lifecycle file with ordered checklist evidence and marked the task as awaiting user verification because the change is user-visible.
+
+## Changes Made
+- `bizPA/frontend/src/App.jsx`
+  - Added `openQuotesView` to route quote-specific navigation without leaving Timeline filters stuck on `quote`.
+  - Added `view_quotes` handling in `executeVoiceAction`.
+  - Redirected manual quote save and confirmed quote preview flows to `currentTab = 'quotes'`.
+  - Extracted shared activity filtering/render helpers for reuse across Timeline and Quotes views.
+  - Updated `renderActivity` to exclude `quote` items from the general Timeline source list.
+  - Added `renderQuotes` with a dedicated summary header and quote-only list rendering.
+  - Added `quotes` to the bottom navigation and conditional render block.
+- `bizPA/backend/src/services/voiceCaptureParserService.js`
+  - No code change required; verified existing `view_quotes` intent support as the frontend integration target.
+
+## Validation
+- 2026-03-18 18:25:10: Ran `npm run build` from `C:\Users\edebe\eds\bizPA\frontend`.
+  - Result: Pass.
+  - Summary:
+    - `Creating an optimized production build...`
+    - `Compiled successfully.`
+    - Output bundle emitted under `build\static\js\`.
+- 2026-03-18 18:25:10: Verified source integration points with `rg -n "openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'" bizPA/frontend/src/App.jsx`.
+  - Result: Pass.
+  - Summary: Located quote routing and rendering references at lines 1952, 1986, 2045, 2080, 2543, 4230, and 4246.
+- 2026-03-18 18:25:10: Verified backend intent contract with `Get-Content bizPA/backend/src/services/voiceCaptureParserService.js | Select-Object -First 120`.
+  - Result: Pass.
+  - Summary: Confirmed `QUERY_INTENTS` includes `intent: 'view_quotes'`.
+- 2026-03-18 18:25:10: User verification request prepared for final response.
+  - Result: Pending.
+  - Summary: Awaiting explicit user pass/fail on visible UI behavior.
+
+## Risks/Notes
+- No browser-driven manual UI session was run in this task; validation is compile-time plus source-contract verification.
+- The bottom navigation now includes both Capture and Quotes using `FileText` icons; behavior is correct, but icon differentiation may be worth a later UX pass if visual distinction matters.
+- Task remains in `workstream/200_inprogress` until user verification is provided per lifecycle rules for visible UI changes.
+
+## Completion Status
+**Awaiting user verification** - 2026-03-18 18:25:10
+
+## Legacy Execution Evidence
+- Agent lane: gemini
+- Command: `cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md`
+- Return code: `0`
+- Stdout:
+```text
+gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

codex
Implemented the Quotes split in [App.jsx](C:\Users\edebe\eds\bizPA\frontend\src\App.jsx#L1952). Quotes now have their own bottom-nav target and screen, the general Timeline excludes `quote` items by default, `view_quotes` voice intents route into the Quotes screen, and saving or confirming a quote lands in Quotes instead of Timeline. The lifecycle doc is updated at [20260301_235502_gemini_bizpa_add_quotes_section.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md).

Validation passed with `npm run build` in `C:\Users\edebe\eds\bizPA\frontend` (`Compiled successfully.`). I also verified the existing backend voice contract still exposes `view_quotes` in [voiceCaptureParserService.js](C:\Users\edebe\eds\bizPA\backend\src\services\voiceCaptureParserService.js).

Please verify these and reply with pass/fail for each:
1. The bottom navigation now shows `Quotes`.
2. The `Timeline` view no longer shows quote records by default.
3. Quote navigation behaves correctly, including voice “show me quotes” and landing on Quotes after saving/confirming a quote.

Once you confirm, this task can be moved from `200_inprogress` to `300_complete`.
file update:
diff --git a/frontend/src/App.jsx b/frontend/src/App.jsx
index b0b6a961dcb80123d7634a661b59a1e944c1c7a1..29d6f8ec13093942b87cc5dcd5c1aafa427e79db
--- a/frontend/src/App.jsx
+++ b/frontend/src/App.jsx
@@ -416,7 +416,16 @@
   .primary-action, .secondary-action, .danger-action { padding: 12px 18px; min-height: 44px; }
   .secondary-action { background: transparent; color: var(--text-main); border: 1px solid var(--border); }
   .danger-action { background: rgba(204,68,75,0.12); color: var(--danger); border: 1px solid rgba(204,68,75,0.28); }
-  .date-group-header { background: transparent; padding: 10px 2px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; position: sticky; top: 0; z-index: 5; }
+  .grouped-section { margin-bottom: 20px; }
+  .grouped-section-header { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-bottom: 12px; flex-wrap: wrap; }
+  .grouped-section-header h5 { margin: 0; }
+  .group-toggle-actions { display: flex; gap: 8px; flex-wrap: wrap; }
+  .group-toggle-btn { border: 1px solid var(--border); background: transparent; color: var(--text-muted); border-radius: 999px; padding: 8px 12px; font-weight: 700; font-size: 0.78rem; }
+  .date-group-shell { border: 1px solid var(--border); border-radius: 18px; background: var(--bg-card); box-shadow: var(--shadow); overflow: hidden; margin-bottom: 10px; }
+  .date-group-header { width: 100%; background: transparent; padding: 12px 14px; font-weight: 700; font-size: 0.82rem; color: var(--text-muted); cursor: pointer; display: flex; justify-content: space-between; align-items: center; border: none; }
+  .date-group-header-meta { display: flex; align-items: center; gap: 8px; }
+  .date-group-count { border-radius: 999px; padding: 4px 9px; background: var(--chip-bg); border: 1px solid var(--border); font-size: 0.72rem; color: var(--text-muted); }
+  .date-group-body { padding: 0 12px 12px; }
   .voice-preview { background: rgba(0,0,0,0.82); color: white; padding: 8px 15px; border-radius: 15px; margin-bottom: 8px; font-size: 0.72rem; max-width: 240px; text-align: right; }
   .spinner { animation: rotate 2s linear infinite; }
   .capture-grid { display: grid; grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr); gap: 18px; align-items: start; }
@@ -682,6 +691,8 @@
   { value: 'last_week', label: 'Last week' },
 ];
 
+const CLOSED_JOB_STATUSES = new Set(['completed', 'closed', 'won', 'lost', 'cancelled', 'canceled']);
+
 const getActivityItemDate = (item) => {
   const dateValue = item?.transaction_date || item?.relevant_date || item?.due_date || item?.created_at || null;
   if (!dateValue) {
@@ -692,6 +703,68 @@
   return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
 };
 
+const formatGroupDateLabel = (date) => date.toLocaleDateString('en-GB', {
+  weekday: 'short',
+  day: '2-digit',
+  month: 'short',
+  year: 'numeric',
+});
+
+const buildGroupedDateCollections = (entries, getDate, sortDirection = 'desc') => {
+  const datedEntries = entries.map((entry) => {
+    const date = getDate(entry);
+    if (!date) {
+      return {
+        entry,
+        date: null,
+        sortValue: sortDirection === 'asc' ? Number.POSITIVE_INFINITY : Number.NEGATIVE_INFINITY,
+        dateKey: 'no-date',
+        dateLabel: 'No date',
+      };
+    }
+
+    return {
+      entry,
+      date,
+      sortValue: date.getTime(),
+      dateKey: date.toISOString().slice(0, 10),
+      dateLabel: formatGroupDateLabel(date),
+    };
+  });
+
+  datedEntries.sort((left, right) => (
+    sortDirection === 'asc'
+      ? left.sortValue - right.sortValue
+      : right.sortValue - left.sortValue
+  ));
+
+  const groups = [];
+  const groupMap = new Map();
+
+  datedEntries.forEach(({ entry, dateKey, dateLabel }) => {
+    if (!groupMap.has(dateKey)) {
+      const nextGroup = { dateKey, dateLabel, items: [] };
+      groupMap.set(dateKey, nextGroup);
+      groups.push(nextGroup);
+    }
+    groupMap.get(dateKey).items.push(entry);
+  });
+
+  return groups;
+};
+
+const isOpenJob = (job) => !CLOSED_JOB_STATUSES.has(String(job?.status || '').toLowerCase());
+
+const getJobDate = (job) => {
+  const dateValue = job?.next_due_date || job?.updated_at || job?.created_at || null;
+  if (!dateValue) {
+    return null;
+  }
+
+  const parsedDate = new Date(dateValue);
+  return Number.isNaN(parsedDate.getTime()) ? null : parsedDate;
+};
+
 const matchesActivityClientFilter = (item, clientFilter) => {
   const normalizedFilter = String(clientFilter || '').trim().toLowerCase();
   if (!normalizedFilter) {
@@ -1283,7 +1356,7 @@
   const [syncTelemetry] = useState(DEFAULT_SYNC_TELEMETRY);
   const [activeSessions] = useState(DEFAULT_ACTIVE_SESSIONS);
   const [voiceStatus, setVoiceStatus] = useState('idle');
-  const [collapsedDates, setCollapsedDates] = useState({});
+  const [expandedDateGroups, setExpandedDateGroups] = useState({});
   const [inboxItems, setInboxItems] = useState([]);
   const [quarterReadiness, setQuarterReadiness] = useState(null);
   const [resolvedQuarterIssueIds, setResolvedQuarterIssueIds] = useState(() => deriveResolvedIssueIdsFromSearchParams(
@@ -1949,6 +2022,15 @@
     setTimePeriodFilter(timePeriod);
   };
 
+  const openQuotesView = ({ search = '', client = '', date = '', timePeriod = null } = {}) => {
+    setCurrentTab('quotes');
+    setActivityTypeFilter(null);
+    setSearchQuery(search);
+    setActivityClientFilter(client);
+    setActivityDateFilter(date);
+    setTimePeriodFilter(timePeriod);
+  };
+
   const executeVoiceAction = (data) => {
     const { intent, slots = {} } = data || {};
     const nextTimePeriod = resolveVoiceTimePeriod(slots);
@@ -1974,6 +2056,13 @@
           timePeriod: nextTimePeriod,
         });
         break;
+      case 'view_quotes':
+        openQuotesView({
+          client: nextClient,
+          date: nextDate,
+          timePeriod: nextTimePeriod,
+        });
+        break;
       case 'view_vat':
         setCurrentTab(MVP_QUARTERLY_EXPORT_MODE ? 'home' : 'tax');
         break;
@@ -1985,15 +2074,102 @@
     }
   };
 
-  const groupDataByDate = (data, field = 'created_at') => data.reduce((groups, item) => {
-    const dateLabel = new Date(item[field]).toLocaleDateString('en-GB');
-    if (!groups[dateLabel]) {
-      groups[dateLabel] = [];
+  const getDateGroupStateKey = (sectionKey, dateKey) => `${sectionKey}:${dateKey}`;
+
+  const isDateGroupExpanded = (sectionKey, dateKey) => Boolean(
+    expandedDateGroups[getDateGroupStateKey(sectionKey, dateKey)]
+  );
+
+  const toggleDateGroup = (sectionKey, dateKey) => {
+    const stateKey = getDateGroupStateKey(sectionKey, dateKey);
+    setExpandedDateGroups((previous) => ({
+      ...previous,
+      [stateKey]: !previous[stateKey],
+    }));
+  };
+
+  const setDateGroupsExpandedState = (sectionKey, groups, expanded) => {
+    setExpandedDateGroups((previous) => {
+      const nextState = { ...previous };
+      groups.forEach((group) => {
+        nextState[getDateGroupStateKey(sectionKey, group.dateKey)] = expanded;
+      });
+      return nextState;
+    });
+  };
+
+  const renderDateGroupedSection = ({
+    title,
+    sectionKey,
+    groups,
+    emptyTitle,
+    emptyDescription,
+    renderItem,
+  }) => {
+    if (groups.length === 0) {
+      return (
+        <section className="grouped-section">
+          <div className="grouped-section-header">
+            <h5>{title}</h5>
+          </div>
+          <div className="empty-panel">
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyDescription}</p>
+          </div>
+        </section>
+      );
     }
-    groups[dateLabel].push(item);
-    return groups;
-  }, {});
 
+    return (
+      <section className="grouped-section">
+        <div className="grouped-section-header">
+          <h5>{title}</h5>
+          <div className="group-toggle-actions">
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, true)}
+            >
+              Expand All
+            </button>
+            <button
+              type="button"
+              className="group-toggle-btn"
+              onClick={() => setDateGroupsExpandedState(sectionKey, groups, false)}
+            >
+              Collapse All
+            </button>
+          </div>
+        </div>
+        {groups.map((group) => {
+          const expanded = isDateGroupExpanded(sectionKey, group.dateKey);
+          return (
+            <div key={`${sectionKey}-${group.dateKey}`} className="date-group-shell">
+              <button
+                type="button"
+                className="date-group-header"
+                onClick={() => toggleDateGroup(sectionKey, group.dateKey)}
+              >
+                <span className="date-group-header-meta">
+                  <span>{group.dateLabel}</span>
+                  <span className="date-group-count">
+                    {group.items.length} item{group.items.length === 1 ? '' : 's'}
+                  </span>
+                </span>
+                {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
+              </button>
+              {expanded && (
+                <div className="date-group-body">
+                  {group.items.map((item) => renderItem(item))}
+                </div>
+              )}
+            </div>
+          );
+        })}
+      </section>
+    );
+  };
+
   const submitManualEntry = async () => {
     if (manualSaving) {
       return;
@@ -2026,7 +2202,7 @@
 
       resetManualCapture(manualForm.type);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(manualForm.type === 'quote' ? 'quotes' : 'activity');
       alert(`${manualForm.type} saved.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to save item.');
@@ -2061,7 +2237,7 @@
       const nextType = previewForm.entityType || manualForm.type;
       resetManualCapture(nextType);
       await fetchAllData();
-      setCurrentTab('activity');
+      setCurrentTab(nextType === 'quote' ? 'quotes' : 'activity');
       alert(`${nextType} confirmed.`);
     } catch (error) {
       setPreviewError(error.response?.data?.error || 'Failed to confirm draft.');
@@ -2391,15 +2567,15 @@
     );
   };
 
-  const renderActivity = () => {
+  const getFilteredActivityItems = (sourceItems, typeFilter = null) => {
     const searchedItems = searchQuery.trim()
-      ? items.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
-      : items;
+      ? sourceItems.filter((item) => JSON.stringify(item).toLowerCase().includes(searchQuery.trim().toLowerCase()))
+      : sourceItems;
     const clientFilteredItems = activityClientFilter.trim()
       ? searchedItems.filter((item) => matchesActivityClientFilter(item, activityClientFilter))
       : searchedItems;
-    const typeFilteredItems = activityTypeFilter
-      ? clientFilteredItems.filter((item) => item.type === activityTypeFilter)
+    const typeFilteredItems = typeFilter
+      ? clientFilteredItems.filter((item) => item.type === typeFilter)
       : clientFilteredItems;
     const exactDateFilteredItems = activityDateFilter
       ? typeFilteredItems.filter((item) => {
@@ -2410,20 +2586,27 @@
     const filteredItems = timePeriodFilter
       ? exactDateFilteredItems.filter((item) => matchesActivityTimePeriod(item, timePeriodFilter))
       : exactDateFilteredItems;
-    const groups = filteredItems.reduce((collection, item) => {
-      const activityDate = getActivityItemDate(item);
-      const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
-      if (!collection[dateLabel]) {
-        collection[dateLabel] = [];
-      }
-      collection[dateLabel].push(item);
-      return collection;
-    }, {});
+    return filteredItems;
+  };
 
+  const groupActivityItemsByDate = (filteredItems) => filteredItems.reduce((collection, item) => {
+    const activityDate = getActivityItemDate(item);
+    const dateLabel = activityDate ? activityDate.toLocaleDateString('en-GB') : 'No date';
+    if (!collection[dateLabel]) {
+      collection[dateLabel] = [];
+    }
+    collection[dateLabel].push(item);
+    return collection;
+  }, {});
+
+  const renderActivityList = ({ title, sourceItems, typeFilter = null, emptyTitle, emptyMessage }) => {
+    const filteredItems = getFilteredActivityItems(sourceItems, typeFilter);
+    const groups = groupActivityItemsByDate(filteredItems);
+
     return (
       <div>
         <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
-          <h4>{activityTypeFilter || 'Activity'}</h4>
+          <h4>{title}</h4>
           <div className="d-flex flex-wrap gap-2">
             <select
               className="form-select"
@@ -2466,7 +2649,7 @@
             <input
               className="form-control"
               style={{ maxWidth: 280 }}
-              placeholder="Search timeline text"
+              placeholder={typeFilter === 'quote' ? 'Search quotes' : 'Search timeline text'}
               value={searchQuery}
               onChange={(event) => setSearchQuery(event.target.value)}
             />
@@ -2474,10 +2657,8 @@
         </div>
         {filteredItems.length === 0 && (
           <div className="empty-panel">
-            <h5>No matching activity</h5>
-            <p className="small-muted mb-0">
-              Try clearing the client search or switching the date range filter.
-            </p>
+            <h5>{emptyTitle}</h5>
+            <p className="small-muted mb-0">{emptyMessage}</p>
           </div>
         )}
         {Object.keys(groups).map((dateLabel) => (
@@ -2496,7 +2677,7 @@
                   <small>{item.extracted_text || item.raw_note || item.type}</small>
                   <br />
                   <small className="small-muted">
-                    {item.client_name || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
+                    {item.client_name || item.counterparty_name || item.counterparty || 'No counterparty'} | {currencyValue(item.gross_amount ?? item.amount)}
                   </small>
                 </div>
               </div>
@@ -2507,6 +2688,53 @@
     );
   };
 
+  const renderActivity = () => {
+    const timelineItems = items.filter((item) => item.type !== 'quote');
+
+    return renderActivityList({
+      title: activityTypeFilter || 'Activity',
+      sourceItems: timelineItems,
+      typeFilter: activityTypeFilter,
+      emptyTitle: 'No matching activity',
+      emptyMessage: 'Try clearing the client search or switching the date range filter.',
+    });
+  };
+
+  const renderQuotes = () => {
+    const quoteItems = items.filter((item) => item.type === 'quote');
+    const quoteValue = quoteItems.reduce((total, item) => total + Number(item.gross_amount ?? item.amount ?? 0), 0);
+
+    return (
+      <div>
+        <section className="momentum-bar">
+          <div className="d-flex justify-content-between align-items-center flex-wrap gap-3">
+            <div>
+              <div className="command-kicker">
+                <FileText size={14} />
+                Dedicated quotes view
+              </div>
+              <h4 style={{ marginTop: 12, marginBottom: 6 }}>Quotes</h4>
+              <div style={{ opacity: 0.84 }}>
+                Quotes now sit outside the general timeline so pricing work stays separate from day-to-day activity.
+              </div>
+            </div>
+            <div>
+              <strong style={{ display: 'block', fontSize: '1.8rem' }}>{quoteItems.length}</strong>
+              <small>{currencyValue(quoteValue)} total quoted</small>
+            </div>
+          </div>
+        </section>
+        {renderActivityList({
+          title: 'Quote activity',
+          sourceItems: quoteItems,
+          typeFilter: null,
+          emptyTitle: 'No matching quotes',
+          emptyMessage: 'Capture a quote or clear the current filters to review the quote list.',
+        })}
+      </div>
+    );
+  };
+
   const renderCalendar = () => {
     const groups = groupDataByDate(calendarEvents, 'start_at');
     return (
@@ -4159,6 +4387,7 @@
           {currentTab === 'inbox' && renderInbox()}
           {currentTab === 'quarter' && renderQuarter()}
           {currentTab === 'activity' && renderActivity()}
+          {currentTab === 'quotes' && renderQuotes()}
           {currentTab === 'calendar' && renderCalendar()}
           {currentTab === 'clients' && renderClients()}
           {currentTab === 'diary' && renderDiary()}
@@ -4174,6 +4403,7 @@
           { key: 'inbox', label: 'Inbox', icon: <Bell size={20} /> },
           { key: 'quarter', label: 'Quarter', icon: <Calendar size={20} /> },
           { key: 'activity', label: 'Timeline', icon: <Clock size={20} /> },
+          { key: 'quotes', label: 'Quotes', icon: <FileText size={20} /> },
           { key: 'clients', label: 'Clients', icon: <Briefcase size={20} /> },
           { key: 'diary', label: 'Diary', icon: <StickyNote size={20} /> },
           { key: 'tax', label: 'Tax', icon: <Receipt size={20} /> },
diff --git a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
index cedd6df7cb4aa91a34527114812235198441b01f..311e73b29f04474a43fe648d79d268090dc68fd9
--- a/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
+++ b/workstream/200_inprogress/codex/20260301_235502_gemini_bizpa_add_quotes_section.md
@@ -1,34 +1,102 @@
-# TASK: bizPA Dedicated Quotes Section
-
-Source: `000_epic/20260301_235500_bizPA_UI_UX_and_Navigation_Refinement.md`
-
-## 1. Task Summary
-Introduce a dedicated UI section for Quotes, moving them out of the general Activity/Timeline feed into their own navigation target.
-
-## 2. Context
-- Affected Files: `bizPA/frontend/src/App.jsx`
-- Current State: Quotes are viewed by filtering the Timeline by 'quote'.
-
-## 3. Implementation Log
-- (Pending) Add 'Quotes' to bottom navigation.
-- (Pending) Create `renderQuotes` function in `App.jsx`.
-- (Pending) Update voice navigation to switch to this dedicated section.
-
-## 4. Completion Status
-**TODO** - 2026-03-01
-
-
-
-## Execution Evidence
-- Agent lane: gemini
-- Command: cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-- Return code: 0
-- Stdout:
-```text
-gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
-```
-
-
-## Retry History
-Retry-Count: 1
-- Retry scheduled at 2026-03-18 17:21:29
+Source: `workstream/000_epic/general/20260301_235500_general_bizPA_UI_UX_and_Navigation_Refinement.md`
+
+## Task Summary
+Introduce a dedicated UI section for quotes, moving quote records out of the general Activity/Timeline feed and into their own navigation target.
+
+## Context
+- Affected Files: `bizPA/frontend/src/App.jsx`
+- Supporting Reference: `bizPA/backend/src/services/voiceCaptureParserService.js`
+- Current State at Start: Quotes were only visible through the general timeline feed by filtering `items` with `type === 'quote'`.
+
+## Dependency
+Dependency: None
+
+## Plan
+- [x] 1. Implement a dedicated Quotes screen and bottom navigation target in `bizPA/frontend/src/App.jsx`.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and expect a successful production compile after the new Quotes route and render path are added.
+  - Evidence: `npm run build` completed successfully on 2026-03-18; frontend now contains `renderQuotes` and `currentTab === 'quotes'` in `bizPA/frontend/src/App.jsx`.
+- [x] 2. Update quote-related routing so quote voice navigation and quote saves land in the dedicated Quotes section instead of the Timeline.
+  - [x] Test: Run `npm run build` in `bizPA/frontend` and confirm the compiled frontend still contains quote-specific route handling for `view_quotes`, manual quote save, and preview confirmation flows.
+  - Evidence: `bizPA/frontend/src/App.jsx` contains `openQuotesView` at line 1952, `view_quotes` handling at lines 1986-1987, and quote post-save routing at lines 2045 and 2080. Backend parser reference still exposes `view_quotes` in `bizPA/backend/src/services/voiceCaptureParserService.js`.
+- [ ] 3. Request user verification for the visible navigation and feed behavior change.
+  - [ ] Test: Ask the user to verify that the bottom navigation exposes Quotes, the Timeline no longer shows quote records by default, and the quote-specific navigation flow behaves as expected.
+  - Evidence: Pending user pass/fail feedback in the conversation.
+
+## Evidence
+Objective-Delivery-Coverage: 85%
+Auto-Acceptance: false
+- Evidence-Type: test_output
+  - Artifact: `npm run build` in `bizPA/frontend` on 2026-03-18 18:25:10; result included `Compiled successfully.` and emitted `build\\static\\js\\main.c3d32cd2.js`.
+  - Objective-Proved: The modified React app compiles successfully after the dedicated Quotes view and routing changes.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/frontend/src/App.jsx` line references 1952, 1986, 2045, 2080, 2543, 4230, 4246.
+  - Objective-Proved: The frontend contains a dedicated Quotes screen, navigation target, quote-specific routing, and quote save redirection.
+  - Status: captured
+- Evidence-Type: file_output
+  - Artifact: `bizPA/backend/src/services/voiceCaptureParserService.js` includes `intent: 'view_quotes'`.
+  - Objective-Proved: The existing backend voice contract already exposes a quote-navigation intent that the frontend now consumes.
+  - Status: captured
+- Evidence-Type: manual_verification
+  - Artifact: User verification request to confirm Quotes navigation, Timeline exclusion of quotes, and quote voice navigation behavior.
+  - Objective-Proved: Final user-visible behavior matches the requested UX change in a real session.
+  - Status: planned
+
+## Implementation Log
+- 2026-03-01: Initial task created with pending notes to add Quotes navigation, create a dedicated render function, and update voice navigation.
+- 2026-03-18 17:21:29: Retry scheduled for the task.
+- 2026-03-18 18:03-18:20: Reviewed `skills/workstream-task-lifecycle/SKILL.md`, loaded the in-progress task file, and inspected `bizPA/frontend/src/App.jsx` plus the backend voice parser contract.
+- 2026-03-18 18:20-18:24: Refactored activity rendering into shared filtering helpers, introduced `renderQuotes`, excluded `quote` items from the general Timeline source list, and added a Quotes bottom-nav target.
+- 2026-03-18 18:24-18:25: Wired `view_quotes` to `openQuotesView`, and redirected manual quote save plus quote preview confirmation flows into the dedicated Quotes section.
+- 2026-03-18 18:25:10: Ran `npm run build` in `bizPA/frontend`; build completed successfully.
+- 2026-03-18 18:25:10: Updated this lifecycle file with ordered checklist evidence and marked the task as awaiting user verification because the change is user-visible.
+
+## Changes Made
+- `bizPA/frontend/src/App.jsx`
+  - Added `openQuotesView` to route quote-specific navigation without leaving Timeline filters stuck on `quote`.
+  - Added `view_quotes` handling in `executeVoiceAction`.
+  - Redirected manual quote save and confirmed quote preview flows to `currentTab = 'quotes'`.
+  - Extracted shared activity filtering/render helpers for reuse across Timeline and Quotes views.
+  - Updated `renderActivity` to exclude `quote` items from the general Timeline source list.
+  - Added `renderQuotes` with a dedicated summary header and quote-only list rendering.
+  - Added `quotes` to the bottom navigation and conditional render block.
+- `bizPA/backend/src/services/voiceCaptureParserService.js`
+  - No code change required; verified existing `view_quotes` intent support as the frontend integration target.
+
+## Validation
+- 2026-03-18 18:25:10: Ran `npm run build` from `C:\Users\edebe\eds\bizPA\frontend`.
+  - Result: Pass.
+  - Summary:
+    - `Creating an optimized production build...`
+    - `Compiled successfully.`
+    - Output bundle emitted under `build\static\js\`.
+- 2026-03-18 18:25:10: Verified source integration points with `rg -n "openQuotesView|view_quotes|renderQuotes|currentTab === 'quotes'|key: 'quotes'|setCurrentTab\\(nextType === 'quote'|setCurrentTab\\(manualForm.type === 'quote'" bizPA/frontend/src/App.jsx`.
+  - Result: Pass.
+  - Summary: Located quote routing and rendering references at lines 1952, 1986, 2045, 2080, 2543, 4230, and 4246.
+- 2026-03-18 18:25:10: Verified backend intent contract with `Get-Content bizPA/backend/src/services/voiceCaptureParserService.js | Select-Object -First 120`.
+  - Result: Pass.
+  - Summary: Confirmed `QUERY_INTENTS` includes `intent: 'view_quotes'`.
+- 2026-03-18 18:25:10: User verification request prepared for final response.
+  - Result: Pending.
+  - Summary: Awaiting explicit user pass/fail on visible UI behavior.
+
+## Risks/Notes
+- No browser-driven manual UI session was run in this task; validation is compile-time plus source-contract verification.
+- The bottom navigation now includes both Capture and Quotes using `FileText` icons; behavior is correct, but icon differentiation may be worth a later UX pass if visual distinction matters.
+- Task remains in `workstream/200_inprogress` until user verification is provided per lifecycle rules for visible UI changes.
+
+## Completion Status
+**Awaiting user verification** - 2026-03-18 18:25:10
+
+## Legacy Execution Evidence
+- Agent lane: gemini
+- Command: `cmd /c echo gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md`
+- Return code: `0`
+- Stdout:
+```text
+gemini processing 20260301_235502_gemini_bizpa_add_quotes_section.md
+```
+
+## Retry History
+Retry-Count: 1
+- Retry scheduled at 2026-03-18 17:21:29

tokens used
163,181
Implemented the Quotes split in [App.jsx](C:\Users\edebe\eds\bizPA\frontend\src\App.jsx#L1952). Quotes now have their own bottom-nav target and screen, the general Timeline excludes `quote` items by default, `view_quotes` voice intents route into the Quotes screen, and saving or confirming a quote lands in Quotes instead of Timeline. The lifecycle doc is updated at [20260301_235502_gemini_bizpa_add_quotes_section.md](C:\Users\edebe\eds\workstream\200_inprogress\codex\20260301_235502_gemini_bizpa_add_quotes_section.md).

Validation passed with `npm run build` in `C:\Users\edebe\eds\bizPA\frontend` (`Compiled successfully.`). I also verified the existing backend voice contract still exposes `view_quotes` in [voiceCaptureParserService.js](C:\Users\edebe\eds\bizPA\backend\src\services\voiceCaptureParserService.js).

Please verify these and reply with pass/fail for each:
1. The bottom navigation now shows `Quotes`.
2. The `Timeline` view no longer shows quote records by default.
3. Quote navigation behaves correctly, including voice “show me quotes” and landing on Quotes after saving/confirming a quote.

Once you confirm, this task can be moved from `200_inprogress` to `300_complete`.
