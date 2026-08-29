(() => {
  'use strict';
  const state = {
    portfolio_id: 'PF_DRAFT', version: 1, status: 'draft', provenance: 'MANUAL',
    strategies: [
      { id: 'DNA_108742', name: 'Mean Reversion FX', source: 'Finder AI', version: 'v4' },
      { id: 'DNA_104921', name: 'Defensive Carry Filter', source: 'Directory', version: 'v2' },
      { id: 'DNA_112087', name: 'Sideways Range Capture', source: 'Finder AI', version: 'v3' }
    ],
    saved: [], entered: false, round: 0, sequence: 18427
  };
  const $ = (id) => document.getElementById(id);
  const candidates = [
    { id: 'DNA_107311', name: 'Volatility Guard Overlay', source: 'Finder AI', version: 'v1' },
    { id: 'DNA_103882', name: 'EUR/USD Intraday Reset', source: 'Agent import', version: 'v5' },
    { id: 'DNA_115904', name: 'Trend Exhaustion Monitor', source: 'Directory', version: 'v2' }
  ];
  const event = (kind, text) => {
    $('eventStatus').textContent = kind;
    const row = document.createElement('div'); row.className = 'event'; row.innerHTML = `<b>${kind}</b> · ${text}`;
    $('destinationEvents').prepend(row);
  };
  const compositionFingerprint = () => state.strategies.map(s => s.id).sort().join('|').split('').reduce((n,c) => ((n * 31 + c.charCodeAt(0)) >>> 0), 7).toString(16).toUpperCase().padStart(8,'0');
  const portfolioLabel = () => $('portfolioName').value.trim() || 'Untitled Portfolio';
  const renderStrategies = () => {
    $('portfolioStrategies').innerHTML = state.strategies.map((s,i) => `<article class="strategy"><div><small>${s.id} · ${s.version} · ${s.source}</small><b>${s.name}</b></div><button aria-label="Remove ${s.name}" data-remove="${i}">×</button></article>`).join('');
    document.querySelectorAll('[data-remove]').forEach(btn => btn.onclick = () => { state.strategies.splice(Number(btn.dataset.remove), 1); state.status='draft'; render(); event('STRATEGY_REMOVED', 'Membership changed; resave to validate destinations.'); });
  };
  const renderObject = () => {
    $('objectName').textContent = portfolioLabel(); $('portfolioId').textContent = state.portfolio_id;
    $('fingerprint').textContent = state.strategies.length ? compositionFingerprint() : 'EMPTY'; $('version').textContent = state.version; $('provenance').textContent = state.provenance;
    $('portfolioStatus').textContent = `${state.status.toUpperCase()} · ${state.strategies.length} ${state.strategies.length===1?'strategy':'strategies'}`;
  };
  const renderSaved = () => {
    $('savedPortfolios').innerHTML = state.saved.length ? state.saved.map(p => `<article class="saved"><div><b>${p.name}</b><small>${p.portfolio_id} · ${p.members} strategies · ${p.status}</small></div><button class="secondary" data-open="${p.portfolio_id}">Open</button></article>`).join('') : '<p class="help">Save a portfolio once, then reuse it across Global, Friends and Agent destinations.</p>';
    document.querySelectorAll('[data-open]').forEach(b => b.onclick = () => { event('PORTFOLIO_REOPENED', `${b.dataset.open} loaded as the active reusable object.`); document.getElementById('portfolio').scrollIntoView({behavior:'smooth'}); });
  };
  const renderBoard = () => {
    const score = 184 + state.round * 17;
    const rows = [{rank:1,name:'Maya · Momentum Select',points:248+state.round*8},{rank:2,name:'Jon · Macro Basket',points:221+state.round*10},{rank:state.entered?3:4,name:portfolioLabel(),points:score,me:true},{rank:state.entered?4:3,name:'Rae · Range Blend',points:162+state.round*5}].sort((a,b)=>b.points-a.points).map((r,i)=>({...r,rank:i+1}));
    $('leaderboardRows').innerHTML=rows.map(r=>`<article class="board-row ${r.me?'me':''}"><span class="rank">#${r.rank}</span><div><b>${r.name}</b><small>${r.me?'YOUR LOCKED ENTRY SNAPSHOT':'Global Weekly participant'}</small></div><span class="points">${r.points} pts</span></article>`).join('');
  };
  const render = () => { renderStrategies(); renderObject(); renderSaved(); renderBoard(); };
  const save = () => {
    if (state.strategies.length < 3) { event('VALIDATION_BLOCKED', 'Global Weekly needs at least 3 strategies. Add another first.'); return; }
    const hash=compositionFingerprint(); const existing=state.saved.find(p=>p.hash===hash);
    if(existing){ $('duplicateNotice').hidden=false; $('duplicateNotice').textContent=`Exact duplicate detected: ${existing.portfolio_id}. Use Existing Portfolio, open it, or modify this combination.`; event('PORTFOLIO_DUPLICATE_DETECTED', `${existing.portfolio_id} has the same canonical strategy membership.`); return; }
    state.portfolio_id=`PF_${state.sequence++}`; state.status='validated';
    state.saved.unshift({portfolio_id:state.portfolio_id,name:portfolioLabel(),members:state.strategies.length,status:'VALIDATED',hash});
    $('duplicateNotice').hidden=true; event('PORTFOLIO_SAVED', `${state.portfolio_id} saved once and can now be submitted anywhere.`); render();
  };
  $('addStrategy').onclick=()=>{const next=candidates.find(c=>!state.strategies.some(s=>s.id===c.id)); if(!next){event('STRATEGY_LIMIT_REACHED','All demo strategy fixtures are already present.'); return;} state.strategies.push(next);state.provenance=next.source==='Agent import'?'AGENT_IMPORT':'FINDER_AI';event('STRATEGY_ADDED',`${next.id} flowed into the editable portfolio.`);render();};
  $('openFinder').onclick=()=>{window.open('https://www.thetechprinciple.com/epic/ep053/','_blank','noopener'); const next=candidates[0];if(!state.strategies.some(s=>s.id===next.id)){state.strategies.push(next);state.provenance='FINDER_AI';render();}event('FINDER_OPENED_FROM_FANTASY','Simulated Finder match added; existing Finder AI opened in a new tab.');};
  $('importAgent').onclick=()=>{const next=candidates[1];if(!state.strategies.some(s=>s.id===next.id)){state.strategies.push(next);state.provenance='AGENT_IMPORT';render();}event('AGENT_PORTFOLIO_IMPORTED','Atlas-07 strategy set contributed a simulated strategy membership.');};
  $('savePortfolio').onclick=save;
  $('duplicatePortfolio').onclick=()=>{state.version+=1;$('portfolioName').value=`${portfolioLabel()} v${state.version}`;state.status='draft';event('PORTFOLIO_CLONED','Created a local editable variation; original portfolio stays reusable.');render();};
  $('archivePortfolio').onclick=()=>{state.status='archived';event('PORTFOLIO_ARCHIVED','Active local portfolio is archived; no remote state changed.');render();};
  $('enterGlobal').onclick=()=>{if(state.status!=='validated'){event('DESTINATION_VALIDATION','Save a valid portfolio before creating a competition snapshot.');return;}state.entered=true; state.status='submitted'; const p=state.saved.find(x=>x.portfolio_id===state.portfolio_id);if(p)p.status='GLOBAL WEEKLY · SNAPSHOT LOCKED';event('GLOBAL_COMPETITION_JOINED',`ENTRY_${state.portfolio_id.slice(3)} locks ${state.strategies.length} strategy IDs with rules v1 and scoring v1.`);render();$('leaderboard').scrollIntoView({behavior:'smooth'});};
  $('createChallenge').onclick=()=>$('challengeDialog').showModal();
  $('inviteFriend').onclick=()=>{const recipient=$('inviteRecipient').value||'friend';$('challengeDialog').close();event('INVITE_CREATED',`Private challenge created for ${recipient}; invite context retains ${state.portfolio_id}.`);};
  $('sendToAgent').onclick=()=>{if(state.status==='draft')event('AGENT_HANDOFF_NOTICE','You can demo the handoff now; in production, a validated portfolio would be required.');$('agentDialog').showModal();};
  const agentHandoff=(name,newAgent)=>{const skillPayload={skill_type:'strategy_portfolio',portfolio_id:state.portfolio_id,portfolio_version:state.version,source:'strategy_fantasy_challenge'}; const h=$('agentHandoff');h.hidden=false;h.innerHTML=[`PORTFOLIO_SKILL_CREATED · ${skillPayload.skill_type}`,`PORTFOLIO_REFERENCE · ${skillPayload.portfolio_id} v${skillPayload.portfolio_version}`,newAgent?`AGENT_CREATED · ${name} · $1.00 starting Arena capital`:`AGENT_SELECTED · ${name}`, 'AGENT_SKILL_ATTACHED · portfolio strategy set assigned','ARENA_JOINED · simulated participant activated'].map((x,i)=>`<div class="${i>1?'done':''}">${x}</div>`).join('');$('ownerLink').hidden=false;event('AGENT_SKILL_ATTACHED',`${state.portfolio_id} assigned as a reusable portfolio skill to ${name}.`);event('ARENA_JOINED','Simulated Arena activation complete. Owner View is available.');};
  $('existingAgent').onclick=()=>agentHandoff('Atlas-07',false); $('newAgent').onclick=()=>agentHandoff('Nova-PF',true);
  $('advanceRound').onclick=()=>{state.round+=1;event('LEADERBOARD_UPDATED',`Round ${state.round} deterministically recalculated all demo points and ranks.`);renderBoard();};
  $('resetDemo').onclick=()=>location.reload();
  document.querySelectorAll('[data-close]').forEach(b=>b.onclick=()=>b.closest('dialog').close());
  render();
})();
