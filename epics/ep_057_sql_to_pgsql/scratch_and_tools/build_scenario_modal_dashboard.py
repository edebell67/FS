import json

html_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\dashboards_and_uis\top10_5min_equity_curves.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

json_path = r"C:\Users\edebe\eds\epics\ep_057_sql_to_pgsql\scratch_and_tools\scenario_catalogue_data.json"
with open(json_path, "r", encoding="utf-8") as f:
    sc_json = json.load(f)

sc_meta_str = json.dumps(sc_json["meta"])
sc_data_str = json.dumps(sc_json["data"])

# 1. Update Title and Header comments
v_head = """ * top10_5min_equity_curves.html — Universal Strategy Scenario Engine: Scenario / Criteria Selection Modal, 5-Min Directional Split, Replay from Baseline & Delta Hiding
 *
 * VERSION HISTORY
 * v1.7.0 · 2026-09-20 · [V20260920_2020] Appends Scenario / Criteria Selection Modal; provides complete Strategy Directory catalogue (Top 10 Net, Top 10 Win Rate, Strongest Three, Strengthening Cluster, Relative Value, Market Move, Opposite Cluster, Weakening Selection, Repair Negative); every scenario feeds into the exact same universal functional engine (Replay Mode, Baseline Re-centering, Directional Splits, Delta line hiding, Scrubber, Model visibility toggles, Win rate filter, and Multi-date navigation) with complete feature preservation.
 * v1.6.0 · 2026-09-20 · [V20260920_1650] Adds selectable Ranking Criteria: Top 10 by Net Return vs Top 10 by Win Rate."""

content = content.replace(" * top10_5min_equity_curves.html — Top 10 Strategy Models: Dual Ranking Criteria Selection (Net Return & Win Rate), 5-Min Directional Split, Replay from Baseline, Baseline Initializer & Delta Hiding\n *\n * VERSION HISTORY\n * v1.6.0 · 2026-09-20 · [V20260920_1650] Adds selectable Ranking Criteria: Top 10 by Net Return vs Top 10 by Win Rate", v_head)

# 2. Update page title and h1
content = content.replace(
    "<title>Top 10 Strategy Models - Selectable Criteria (Net Return / Win Rate), Replay from Baseline & Directional Split</title>",
    "<title>Strategy Scenarios Engine - Universal Replay & Directional Split</title>"
)

content = content.replace(
    "Top 10 Models: Dual Ranking Criteria & Directional Split",
    "Strategy Directory: Scenario & Criteria Universal Engine"
)

content = content.replace(
    "Select <b class=\"text-sky-300\">Top 10 Net Return</b> or <b class=\"text-emerald-300\">Top 10 Win Rate</b> &bull; Replay from selected baseline &bull; Inspect Total Net, <span class=\"text-sky-400 font-semibold\">Buy Net</span> & <span class=\"text-amber-400 font-semibold\">Sell Net</span> &bull; Toggle delta lines &bull; Re-center baseline",
    "Click <b class=\"text-sky-300\">Criteria / Scenario</b> to choose an investigation workflow &bull; Replay from selected baseline &bull; Inspect Total Net, <span class=\"text-sky-400 font-semibold\">Buy Net</span> & <span class=\"text-amber-400 font-semibold\">Sell Net</span> &bull; Toggle delta lines &bull; Re-center baseline"
)

# 3. Replace the Criteria buttons with the Criteria / Scenario Modal trigger button
old_criteria_markup = """        <!-- Ranking Criteria Selector -->
        <div class="flex items-center gap-1 bg-slate-950 p-1 rounded-lg border border-sky-500/40 font-mono text-xs shadow-inner">
          <span class="text-[10px] uppercase font-bold text-slate-400 px-1.5 hidden sm:inline">Criteria:</span>
          <button id="criteriaNetBtn" class="criteria-btn px-2.5 py-1 font-bold rounded bg-sky-600 text-white transition flex items-center gap-1">
            <span>★</span>
            <span>Top 10 Net Return</span>
          </button>
          <button id="criteriaWinBtn" class="criteria-btn px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1">
            <span>🎯</span>
            <span>Top 10 Win Rate</span>
          </button>
        </div>"""

new_criteria_markup = """        <!-- Criteria / Scenario Modal Trigger Button -->
        <div class="flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-sky-500/50 font-mono text-xs shadow-inner">
          <span class="text-[10px] uppercase font-bold text-slate-400 px-1.5 hidden sm:inline">Scenario:</span>
          <button id="openScenarioModalBtn" class="px-3 py-1 font-bold rounded bg-sky-600 hover:bg-sky-500 text-white transition flex items-center gap-1.5 shadow active:scale-95">
            <span id="activeScenarioIcon">★</span>
            <span id="activeScenarioName">Top 10 Net Return</span>
            <span class="text-[10px] bg-sky-700/80 px-1.5 py-0.2 rounded text-sky-200 ml-1">Change ▾</span>
          </button>
        </div>"""

content = content.replace(old_criteria_markup, new_criteria_markup)

# 4. Insert Scenario Selection Modal dialog just before the script tag
modal_html = """    <!-- ========================================== -->
    <!-- SCENARIO / CRITERIA SELECTION MODAL          -->
    <!-- ========================================== -->
    <dialog id="scenarioModal" class="bg-slate-900 text-slate-100 border border-slate-700 rounded-2xl p-0 max-w-2xl w-full shadow-2xl backdrop:bg-black/75 backdrop:backdrop-blur-sm">
      <div class="p-4 sm:p-6 flex flex-col gap-4 font-mono">
        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b border-slate-800 pb-3">
          <div class="flex items-center gap-2.5">
            <div class="w-3 h-8 rounded-full bg-sky-500"></div>
            <div>
              <h2 class="text-lg font-black text-white tracking-tight">Select Strategy Scenario / Criteria</h2>
              <p class="text-xs text-slate-400">The chosen scenario provides qualifying strategies to the universal replay & split engine.</p>
            </div>
          </div>
          <button id="closeScenarioModalBtn" class="text-slate-400 hover:text-white p-1 rounded-lg text-lg leading-none transition">✕</button>
        </div>

        <!-- Search / Filter input -->
        <div class="relative">
          <input type="text" id="scenarioSearchInput" placeholder="Filter scenarios (e.g. win rate, momentum, cluster, repair)..." 
                 class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3.5 py-2 text-xs text-white focus:outline-none focus:border-sky-500 placeholder-slate-500">
        </div>

        <!-- Scenario Cards Grid -->
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 max-h-[420px] overflow-y-auto pr-1" id="modalScenarioCards"></div>

        <!-- Modal Footer -->
        <div class="flex items-center justify-between border-t border-slate-800 pt-3 text-xs text-slate-400">
          <span>All scenarios utilize the <b>identical</b> universal engine.</span>
          <button id="closeScenarioModalFooterBtn" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 transition font-bold">
            Close
          </button>
        </div>
      </div>
    </dialog>
"""

content = content.replace("  <script>", modal_html + "\n  <script>")

# 5. Replace data block in script
pos1 = content.find("// Dual Criteria Master Dataset")
pos2 = content.find("const ALL_DATE_DATA = ALL_CRITERIA_DATA[\"NET_RETURN\"];")
if pos1 != -1 and pos2 != -1:
    new_data_script = f"""// Unified Scenario Catalogue Meta & Strategy Datasets
    const SCENARIOS_CATALOGUE = {sc_meta_str};
    const ALL_CRITERIA_DATA = {sc_data_str};
    """
    content = content[:pos1] + new_data_script + content[pos2:]

# 6. Update state variables and DOM references
old_vars = """    let currentCriteria = 'NET_RETURN'; // 'NET_RETURN' or 'WIN_RATE'
    let currentDate = 'WEEK_OVERALL';"""

new_vars = """    let currentCriteria = 'top_net'; // Active Scenario ID ('top_net', 'top_win', 'strongest_three', etc.)
    // Default to most recent trading date (datetime stamp: 2026-09-20 21:36 - [V20260920_2136])
    let currentDate = '2026-09-18';"""

content = content.replace(old_vars, new_vars)

old_dom = """    // DOM Elements
    const criteriaNetBtn = document.getElementById('criteriaNetBtn');
    const criteriaWinBtn = document.getElementById('criteriaWinBtn');
    const activeCriteriaLabel = document.getElementById('activeCriteriaLabel');"""

new_dom = """    // DOM Elements
    const openScenarioModalBtn = document.getElementById('openScenarioModalBtn');
    const closeScenarioModalBtn = document.getElementById('closeScenarioModalBtn');
    const closeScenarioModalFooterBtn = document.getElementById('closeScenarioModalFooterBtn');
    const scenarioModal = document.getElementById('scenarioModal');
    const modalScenarioCards = document.getElementById('modalScenarioCards');
    const scenarioSearchInput = document.getElementById('scenarioSearchInput');
    const activeScenarioIcon = document.getElementById('activeScenarioIcon');
    const activeScenarioName = document.getElementById('activeScenarioName');
    const activeCriteriaLabel = document.getElementById('activeCriteriaLabel');"""

content = content.replace(old_dom, new_dom)

# 7. Update updateCriteriaButtonsUI to updateScenarioUI and hook modal
old_criteria_fn = """    function updateCriteriaButtonsUI() {
      if (currentCriteria === 'NET_RETURN') {
        criteriaNetBtn.className = 'criteria-btn px-2.5 py-1 font-bold rounded bg-sky-600 text-white transition flex items-center gap-1 shadow';
        criteriaWinBtn.className = 'criteria-btn px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1';
        activeCriteriaLabel.textContent = 'Top 10 Net Return';
        activeCriteriaLabel.className = 'text-sky-300';
      } else {
        criteriaNetBtn.className = 'criteria-btn px-2.5 py-1 font-bold rounded text-slate-400 hover:text-white transition flex items-center gap-1';
        criteriaWinBtn.className = 'criteria-btn px-2.5 py-1 font-bold rounded bg-emerald-600 text-white transition flex items-center gap-1 shadow';
        activeCriteriaLabel.textContent = 'Top 10 Win Rate';
        activeCriteriaLabel.className = 'text-emerald-300';
      }
    }"""

new_criteria_fn = """    function updateScenarioUI() {
      const sc = SCENARIOS_CATALOGUE.find(s => s.id === currentCriteria) || SCENARIOS_CATALOGUE[0];
      if (activeScenarioIcon) activeScenarioIcon.textContent = sc.icon;
      if (activeScenarioName) activeScenarioName.textContent = sc.name;
      if (activeCriteriaLabel) {
        activeCriteriaLabel.textContent = sc.name;
        activeCriteriaLabel.className = 'text-sky-300';
      }
      renderModalScenarioCards();
    }

    function renderModalScenarioCards(filterText = '') {
      if (!modalScenarioCards) return;
      modalScenarioCards.innerHTML = '';
      const q = filterText.toLowerCase().trim();

      SCENARIOS_CATALOGUE.forEach(sc => {
        if (q && !sc.name.toLowerCase().includes(q) && !sc.sub.toLowerCase().includes(q) && !sc.badge.toLowerCase().includes(q)) {
          return;
        }

        const isSelected = sc.id === currentCriteria;
        const card = document.createElement('div');
        card.className = `p-3 rounded-xl border cursor-pointer transition flex flex-col justify-between ${
          isSelected 
            ? 'border-sky-500 bg-sky-500/15 shadow-lg' 
            : 'border-slate-800 bg-slate-950/80 hover:border-slate-700 hover:bg-slate-950'
        }`;

        card.onclick = () => {
          setRankingCriteria(sc.id);
          scenarioModal.close();
        };

        card.innerHTML = `
          <div>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-1.5">
                <span class="text-base">${sc.icon}</span>
                <span class="font-bold text-xs ${isSelected ? 'text-sky-300' : 'text-white'}">${sc.name}</span>
              </div>
              <span class="text-[9px] px-1.5 py-0.5 rounded font-bold uppercase ${isSelected ? 'bg-sky-500/30 text-sky-200' : 'bg-slate-800 text-slate-400'}">
                ${sc.badge}
              </span>
            </div>
            <p class="text-[11px] text-slate-400 mt-1.5 leading-relaxed">${sc.sub}</p>
          </div>
          <div class="mt-2 pt-1.5 border-t border-slate-800/80 flex items-center justify-between text-[10px]">
            <span class="text-slate-500">Click to activate</span>
            ${isSelected ? '<span class="text-sky-400 font-bold flex items-center gap-1">● Active</span>' : '<span class="text-slate-400 font-bold hover:text-white">Select ➔</span>'}
          </div>
        `;
        modalScenarioCards.appendChild(card);
      });
    }"""

content = content.replace(old_criteria_fn, new_criteria_fn)

# 8. Update updateDateLabelAndTitle and ribbon logic
content = content.replace(
    "const critName = currentCriteria === 'NET_RETURN' ? 'Net Return' : 'Win Rate';",
    "const scObj = SCENARIOS_CATALOGUE.find(s => s.id === currentCriteria) || { name: currentCriteria }; const critName = scObj.name;"
)

content = content.replace(
    "const critLabel = currentCriteria === 'NET_RETURN' ? 'Top 10 Net' : 'Top 10 Win Rate';",
    "const scObj = SCENARIOS_CATALOGUE.find(s => s.id === currentCriteria) || { name: currentCriteria }; const critLabel = scObj.name;"
)

# 9. Update setupEventListeners to handle modal and search
old_events = """      // Criteria Buttons
      criteriaNetBtn.onclick = () => setRankingCriteria('NET_RETURN');
      criteriaWinBtn.onclick = () => setRankingCriteria('WIN_RATE');"""

new_events = """      // Scenario Modal Events
      if (openScenarioModalBtn) {
        openScenarioModalBtn.onclick = () => {
          renderModalScenarioCards();
          scenarioModal.showModal();
        };
      }
      if (closeScenarioModalBtn) closeScenarioModalBtn.onclick = () => scenarioModal.close();
      if (closeScenarioModalFooterBtn) closeScenarioModalFooterBtn.onclick = () => scenarioModal.close();
      if (scenarioSearchInput) {
        scenarioSearchInput.oninput = (e) => renderModalScenarioCards(e.target.value);
      }"""

content = content.replace(old_events, new_events)

# 10. Update init() call
content = content.replace("updateCriteriaButtonsUI();", "updateScenarioUI();")
content = content.replace("updateCriteriaButtonsUI()", "updateScenarioUI()")

# Write output file
with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

# Also copy to brain artifacts directory
brain_path = r"C:\Users\edebe\.gemini\antigravity\brain\6aed791c-b3c5-4ab4-a571-c23206db4462\top10_5min_equity_curves.html"
with open(brain_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Successfully assembled top10_5min_equity_curves.html with Scenario Selection Modal!")
