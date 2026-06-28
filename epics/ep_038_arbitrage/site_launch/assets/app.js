const fmtGBP = v => Number(v||0).toLocaleString('en-GB',{style:'currency',currency:'GBP',maximumFractionDigits:0});
const fmtUSD = v => Number(v||0).toLocaleString('en-US',{style:'currency',currency:'USD',maximumFractionDigits:0});
document.getElementById('menuBtn')?.addEventListener('click',()=>document.getElementById('nav')?.classList.toggle('open'));
async function loadData(){ const r=await fetch('data/spreads.json'); return await r.json(); }
function card(s){
  const demo = s.source_kind !== 'live' || s.qualified_spread !== 'yes';
  return `<article class="spread-card ${demo?'demo-card':''}"><div class="top"><span class="badge">${demo?'DEMO / NOT LIVE':s.state}</span><span>${s.category}</span></div><h3>${s.item_name}</h3><p class="risk">${s.variant||''}</p><div class="prices"><div><small>Marketplace / sale guide</small><b>${s.marketplace_price} ${s.currency}</b></div><div><small>Source</small><b>${s.source_price} ${s.currency}</b></div><div><small>Spread</small><b>${s.gross_spread_pct||'TBD'}%</b></div></div><p>${s.public_card_summary}</p><div class="urgency"><b>Time pressure:</b> ${s.urgency_level||'low'} · ${s.expiry_type||'not time-sensitive'} · ${s.hours_to_expiry||'no countdown'}h</div><p class="risk"><b>Risk:</b> ${s.risk_notes}</p></article>`
}
async function initBoard(){
  const grid=document.getElementById('spreadGrid'); if(!grid)return;
  const data=await loadData();
  const spreads=data.spreads||[];
  const qualified=spreads.filter(s=>s.source_kind==='live' && s.qualified_spread==='yes');
  const demo=spreads.filter(s=>!(s.source_kind==='live' && s.qualified_spread==='yes'));
  const states=[...new Set(spreads.map(s=>s.state))].sort();
  const cats=[...new Set(spreads.map(s=>s.category))].sort();
  stateFilter.innerHTML+=[...states].map(x=>`<option>${x}</option>`).join('');
  categoryFilter.innerHTML+=[...cats].map(x=>`<option>${x}</option>`).join('');
  boardMetrics.innerHTML=`<div><small>Qualified live spread value</small><strong>${fmtGBP(data.metrics.qualified_live_gross_spread_value||0)}</strong></div><div><small>Qualified live spreads</small><strong>${data.metrics.qualified_live_spread_count||0}</strong></div><div><small>Auction watch candidates</small><strong>${data.metrics.auction_watch_count||0}</strong></div><div><small>Demo examples</small><strong>${data.metrics.demo_example_count||0}</strong></div>`;
  const notice=document.createElement('section');
  notice.className='notice';
  notice.innerHTML='<b>Current live status:</b> No qualified live spreads are currently displayed. The records below are labelled demo examples until real source price + sale/reference/guide price are confirmed.';
  grid.parentNode.insertBefore(notice, grid);
  function matches(s){const q=search.value.toLowerCase(); const st=stateFilter.value; const cat=categoryFilter.value; const t=timeOnly.checked; return (!q||(s.item_name+s.category+s.variant).toLowerCase().includes(q))&&(!st||s.state===st)&&(!cat||s.category===cat)&&(!t||s.time_sensitive==='yes');}
  function render(){
    const qrows=qualified.filter(matches);
    const drows=demo.filter(matches);
    const liveHtml = qrows.length ? `<h2>Qualified live spreads</h2><div class="grid cards">${qrows.map(card).join('')}</div>` : '<h2>Qualified live spreads</h2><p class="notice">0 qualified live spreads. We only publish a spread when source price and sale/reference/guide price are both known.</p>';
    const demoHtml = `<h2>Demo examples — not live data</h2><p class="risk">These are format examples only and are excluded from live spread value/count metrics.</p><div class="grid cards">${drows.map(card).join('')}</div>`;
    grid.innerHTML=liveHtml+demoHtml;
  }
  [search,stateFilter,categoryFilter,timeOnly].forEach(el=>el.addEventListener('input',render)); render();
}
async function initPrefs(){const form=document.getElementById('prefForm'); if(!form)return; const data=await loadData(); alertList.innerHTML=(data.alerts||[]).map(a=>`<article class="spread-card demo-card"><div class="top"><span class="badge">DEMO ALERT</span><span>${a.delivery_status}</span></div><h3>${a.subscriber_id}</h3><p>${a.message_summary}</p><p class="risk">No real notification sent in MVP.</p></article>`).join(''); form.addEventListener('submit',e=>{e.preventDefault(); const pref=Object.fromEntries(new FormData(form).entries()); pref.timeOnly=form.timeOnly.checked; pref.savedAt=new Date().toISOString(); localStorage.setItem('ep038Preference',JSON.stringify(pref)); prefResult.classList.remove('hidden'); prefResult.innerHTML='<b>Preference saved locally.</b> Production launch will connect this to a user-owned notification provider.';});}
initBoard(); initPrefs();
