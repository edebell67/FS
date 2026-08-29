(() => {
  'use strict';
  const ARENA_OWNER = 'https://www.thetechprinciple.com/epic/ep052/owner/';
  const PREVIEW_BOUNDARY = 'Preview only: no real agent, skill assignment, Arena join or trading action has been executed.';
  const state = { phase: 'FINDER_IDLE', selectedStrategy: null, agent: null, query: '' };
  const strategies = [
    { strategy_id: 'DNA_108742', name: 'Defensive Mean Reversion', match: 94, return: '+12.4%', win: '64%', drawdown: '5.8%', trades: '3,821', market: 'FX', regime: 'Sideways', why: 'Controlled drawdown with strong sideways-regime evidence.' },
    { strategy_id: 'DNA_204901', name: 'EUR/USD Range Capture', match: 88, return: '+10.7%', win: '61%', drawdown: '7.1%', trades: '2,195', market: 'FX', regime: 'Range-bound', why: 'Frequent EUR/USD range opportunities with a measured risk profile.' },
    { strategy_id: 'DNA_337515', name: 'Steady FX Carry Filter', match: 82, return: '+8.9%', win: '58%', drawdown: '6.6%', trades: '1,440', market: 'FX', regime: 'Balanced', why: 'Lower-turnover candidate with a defensive cash-aware profile.' }
  ];
  const agents = [
    { id: 'AX-427', name: 'Atlas 427', nav: '$1.0837', rank: '#137' },
    { id: 'NV-012', name: 'Nova 12', nav: '$1.0211', rank: '#814' },
    { id: 'QM-008', name: 'Quantum 8', nav: '$1.1402', rank: '#41' }
  ];
  const $ = (s) => document.querySelector(s);
  const open = (id) => $(id).showModal();
  const closeAll = () => document.querySelectorAll('dialog[open]').forEach((d) => d.close());
  const phase = (next) => { state.phase = next; document.body.dataset.finderState = next; };
  const selectedMarkup = (s) => `<span class="result-id">${s.strategy_id} · STRATEGY DIRECTORY SKILL</span><h3>${s.name}</h3><p>${s.why}</p><div class="metrics"><span>Match<b>${s.match}%</b></span><span>Max drawdown<b>${s.drawdown}</b></span><span>Market<b>${s.market}</b></span><span>Strongest regime<b>${s.regime}</b></span></div>`;
  function displayResults(showResults = true) {
    $('#interpretation').innerHTML = '<b>Hard: FX</b><b>Hard: max drawdown ≤ 8%</b><b>Preference: sideways regime</b><b>Objective: defensive / steady</b>';
    $('#resultList').innerHTML = showResults ? strategies.map((s, index) => `<article class="result"><div class="result-head"><span class="result-id">${s.strategy_id}</span><span class="match">${s.match}% match</span></div><h3>${s.name}</h3><p>${s.why}</p><div class="metrics"><span>Return<b>${s.return}</b></span><span>Win rate<b>${s.win}</b></span><span>Max DD<b>${s.drawdown}</b></span><span>Trades<b>${s.trades}</b></span><span>Market<b>${s.market}</b></span><span>Regime<b>${s.regime}</b></span></div><button data-select="${index}">Select strategy →</button></article>`).join('') : '';
    $('#noResults').hidden = showResults;
    $('#resultsSection').hidden = false;
    phase(showResults ? 'RESULTS' : 'FINDER_NO_RESULTS');
    $('#resultsSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function renderResults() {
    state.query = $('#strategyQuery').value.trim();
    const noMatch = /no match|impossible|70%|crypto/i.test(state.query);
    displayResults(!noMatch);
  }
  function showClosestMatches() { displayResults(true); }
  function chooseStrategy(index) {
    state.selectedStrategy = strategies[index]; phase('STRATEGY_SELECTED');
    $('#selectedStrategy').innerHTML = selectedMarkup(state.selectedStrategy);
    $('#selectionSection').hidden = false;
    $('#selectionSection').scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  function skillPayload() { return { skill_type: 'strategy_directory_strategy', strategy_id: state.selectedStrategy.strategy_id, strategy_version: 'current', source: 'strategy_directory' }; }
  function resetHandoff() {
    $('#handoffSteps').querySelectorAll('li').forEach((li) => li.className = '');
    $('#successSummary').hidden = true; $('#watchAgent').hidden = true; $('#findAnother').hidden = true;
  }
  function simulateArenaHandoff(agent) {
    state.agent = agent; closeAll(); resetHandoff(); open('#successDialog');
    const payload = skillPayload(); const steps = [...$('#handoffSteps').querySelectorAll('li')];
    const phases = ['ASSIGN_SKILL', 'ASSIGN_SKILL', 'JOIN_ARENA', 'ARENA_ACTIVE'];
    steps.forEach((step, index) => setTimeout(() => {
      phase(phases[index]); step.className = 'complete'; step.textContent = `✓ ${step.textContent}`;
      if (index === steps.length - 1) {
        $('#successTitle').textContent = `${agent.name} is simulated in the Arena.`;
        $('#successSummary').hidden = false;
        $('#successSummary').innerHTML = `<b>Local demo record</b><br><br><b>Agent:</b> ${agent.name}<br><b>Skill:</b> ${payload.strategy_id} — ${state.selectedStrategy.name}<br><b>Starting Arena capital:</b> $1.00<br><b>Preview status:</b> Simulated trading active`;
        $('#watchAgent').hidden = false; $('#findAnother').hidden = false;
      }
    }, 500 * (index + 1)));
  }
  $('#searchButton').addEventListener('click', renderResults);
  $('#strategyQuery').addEventListener('keydown', (e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') renderResults(); });
  document.querySelectorAll('.prompt').forEach((b) => b.addEventListener('click', () => { $('#strategyQuery').value = b.dataset.query; renderResults(); }));
  $('#resultList').addEventListener('click', (e) => { const index = e.target.dataset.select; if (index !== undefined) chooseStrategy(Number(index)); });
  $('#showClosest').addEventListener('click', showClosestMatches);
  $('#changeRequirements').addEventListener('click', () => { $('#strategyQuery').focus(); $('#strategyQuery').scrollIntoView({ behavior: 'smooth', block: 'center' }); });
  $('#giveButton').addEventListener('click', () => { if (state.selectedStrategy) { phase('AGENT_DESTINATION'); open('#agentDialog'); } });
  document.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', closeAll));
  document.querySelectorAll('[data-destination]').forEach((b) => b.addEventListener('click', () => {
    closeAll();
    if (b.dataset.destination === 'existing') {
      phase('EXISTING_AGENT');
      $('#agentList').innerHTML = agents.map((a, i) => `<button class="agent-choice" data-agent="${i}"><b>${a.name}</b><span>NAV ${a.nav} · Arena rank ${a.rank}</span></button>`).join('');
      open('#existingDialog');
    } else {
      phase('CREATE_AGENT'); $('#newSkill').textContent = `${state.selectedStrategy.strategy_id} — ${state.selectedStrategy.name}`; open('#newDialog');
    }
  }));
  $('#agentList').addEventListener('click', (e) => { const button = e.target.closest('[data-agent]'); if (button) simulateArenaHandoff(agents[Number(button.dataset.agent)]); });
  $('#createButton').addEventListener('click', () => {
    const name = $('#agentName').value.trim() || 'Atlas';
    simulateArenaHandoff({ id: `SIM-${Date.now()}`, name, nav: '$1.0000', rank: 'Simulated new entrant' });
  });
  $('#findAnother').addEventListener('click', () => { closeAll(); phase('FINDER_IDLE'); $('#strategyQuery').focus(); window.scrollTo({ top: 0, behavior: 'smooth' }); });
  window.finderIntegration = { ownerView: ARENA_OWNER, skillPayload, state, simulateArenaHandoff, showClosestMatches };
})();
