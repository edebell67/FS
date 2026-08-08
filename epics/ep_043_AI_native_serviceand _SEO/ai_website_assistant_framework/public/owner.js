const BASE = window.location.origin;
let STATE = { tenant: "", token: "", client: null };

function $(id){return document.getElementById(id)}
function qs(sel){return document.querySelector(sel)}

$('login-btn').addEventListener('click', login);
$('logout-btn').addEventListener('click', logout);
$('tracking-toggle').addEventListener('change', toggleTracking);
$('compare-btn').addEventListener('click', loadCompare);
$('new-promo-btn').addEventListener('click', ()=>$('promo-form').hidden=false);
$('promo-cancel').addEventListener('click', ()=>$('promo-form').hidden=true);
$('promo-submit').addEventListener('click', createPromotion);

document.querySelectorAll('.dash-nav button[data-view]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.dash-nav button').forEach(b=>b.classList.remove('nav-on'));
    btn.classList.add('nav-on');
    document.querySelectorAll('.dash-view').forEach(v=>v.hidden=true);
    const view = $('view-'+btn.dataset.view);
    if(view) view.hidden=false;
    if(btn.dataset.view==='overview') loadOverview();
    if(btn.dataset.view==='compare') loadCompare();
    if(btn.dataset.view==='promotions') loadPromotions();
  });
});

async function api(path, opts={}){
  const headers = {'Authorization': `Bearer ${STATE.token}`, ...opts.headers};
  if(opts.body && !(opts.body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const res = await fetch(BASE+path, {...opts, headers});
  const data = await res.json().catch(()=>({error:'Parse error'}));
  if(!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

async function login(){
  const tenant = $('login-tenant').value.trim();
  const token = $('login-token').value.trim();
  if(!tenant || !token){ $('login-error').textContent='Please enter both site key and token.';$('login-error').hidden=false;return}
  STATE = { tenant, token };
  try {
    const data = await api(`/api/owner/reporting?tenant=${encodeURIComponent(tenant)}`);
    STATE.client = data;
    $('dash-title').textContent = data.businessName || 'Owner Dashboard';
    $('login-screen').hidden = true;
    $('dash-screen').hidden = false;
    loadOverview();
  } catch(e){
    $('login-error').textContent = e.message || 'Login failed. Check your site key and token.';
    $('login-error').hidden = false;
  }
}

function logout(){
  STATE = { tenant:'', token:'', client:null };
  $('login-screen').hidden = false;
  $('dash-screen').hidden = true;
  $('login-error').hidden = true;
}

async function loadOverview(){
  try {
    const data = await api(`/api/owner/reporting?tenant=${encodeURIComponent(STATE.tenant)}`);
    STATE.client = data;
    const tracking = data.pageAnalytics;
    const isDisabled = tracking && tracking.status === 'tracking_disabled';
    $('tracking-status').textContent = isDisabled ? 'Web tracking is off' : 'Web tracking is on';
    $('tracking-toggle').checked = !isDisabled;

    const perf = data.performance || {};
    const totalRecords = data.summary ? Object.values(data.summary).reduce((a,b)=>a+b,0) : 0;
    $('overview-stats').innerHTML = `
      <div class="stat-card"><span>Unique visitors</span><strong>${perf.uniqueVisits||0}</strong></div>
      <div class="stat-card"><span>Page views</span><strong>${perf.pageViews||0}</strong></div>
      <div class="stat-card"><span>Conversations</span><strong>${data.summary?.conversations||0}</strong></div>
      <div class="stat-card"><span>Leads captured</span><strong>${data.summary?.leads||0}</strong></div>
    `;

    const records = Object.entries(data.summary || {}).filter(([k,v])=>v>0&&k!=='previewResponses').slice(0,8);
    $('overview-activity').innerHTML = records.length
      ? records.map(([k,v])=>`<div class="activity-item"><strong>${k}</strong> — ${v} records</div>`).join('')
      : '<div class="empty-state">No activity yet. Activity appears when visitors interact with your site.</div>';
  } catch(e){
    $('overview-stats').innerHTML = `<div class="stat-card"><span>Error</span><strong>${e.message}</strong></div>`;
  }
}

async function toggleTracking(){
  const enabled = $('tracking-toggle').checked;
  try {
    const data = await api(`/api/owner/reporting/tracking?tenant=${encodeURIComponent(STATE.tenant)}`, {
      method: 'PUT', body: JSON.stringify({analyticsEnabled: enabled})
    });
    $('tracking-status').textContent = enabled ? 'Web tracking is on' : 'Web tracking is off';
  } catch(e){
    $('tracking-toggle').checked = !enabled;
    alert('Failed to toggle tracking: '+e.message);
  }
}

async function loadCompare(){
  const days = parseInt($('compare-days').value) || 7;
  try {
    const data = await api(`/api/owner/reporting/compare?tenant=${encodeURIComponent(STATE.tenant)}&days=${days}`);
    const c = data.comparison || {};
    const pc = (v)=>`<span class="change ${v.change.startsWith('+')?'up':'down'}">${v.change}</span>`;
    $('compare-stats').innerHTML = `
      <div class="stat-card"><span>Visitors</span><strong>${c.visitors?.today||0}</strong>${pc(c.visitors||{})}</div>
      <div class="stat-card"><span>Page views</span><strong>${c.pageViews?.today||0}</strong>${pc(c.pageViews||{})}</div>
      <div class="stat-card"><span>Engaged</span><strong>${c.engagedPct?.today||0}%</strong><span class="change">avg ${c.engagedPct?.average||0}%</span></div>
      <div class="stat-card"><span>CTA clicks</span><strong>${c.ctaClicks?.today||0}</strong>${pc(c.ctaClicks||{})}</div>
    `;
    const services = c.perService || [];
    $('compare-services').innerHTML = services.length
      ? services.map(s=>{
          const vc = s.views.change;
          const cc = s.clicks.change;
          return `<div class="service-row"><span class="svc-name">${s.service}</span><span class="svc-val">Views: ${s.views.today} <small>(avg ${s.views.average})</small></span><span class="svc-change ${vc>0?'up':'down'}">${vc>0?'+':''}${vc||0}%</span></div>`;
        }).join('')
      : '<div class="empty-state">No service data yet. Data appears after visitors interact with your services.</div>';
  } catch(e){
    $('compare-stats').innerHTML = `<div class="stat-card"><span>Error</span><strong>${e.message}</strong></div>`;
  }
}

async function loadPromotions(){
  try {
    const data = await api(`/api/owner/promotions?tenant=${encodeURIComponent(STATE.tenant)}`);
    const promos = data.promotions || [];
    $('promo-list').innerHTML = promos.length
      ? promos.map(p=>{
          const status = p.status || (p.active ? 'active' : 'paused');
          const fmt = (n)=>n==null?'—':n;
          return `<div class="promo-item">
            <div class="promo-top"><span class="promo-type">${p.type}</span><span class="promo-status ${status}">${status}</span></div>
            <div class="promo-desc">${p.description||'No description'}</div>
            <div class="promo-stats">
              <span>Impressions: ${fmt(p.stats?.impressions)}</span>
              <span>Clicks: ${fmt(p.stats?.clicks)}</span>
              <span>CTR: ${p.stats?.clickThroughRate ? (p.stats.clickThroughRate*100).toFixed(1)+'%' : '—'}</span>
              <span>Conversions: ${fmt(p.stats?.conversions)}</span>
            </div>
            <div class="promo-actions">
              ${p.active
                ? `<button onclick="deactivatePromo('${p.promotionId}')">Deactivate</button>`
                : `<button class="primary" onclick="activatePromo('${p.promotionId}')">Activate</button>`
              }
              <button onclick="viewEffectiveness('${p.promotionId}')">Effectiveness</button>
            </div>
          </div>`;
        }).join('')
      : '<div class="empty-state">No promotions yet. Create one when a service shows above-average traffic.</div>';
  } catch(e){
    $('promo-list').innerHTML = `<div class="empty-state">Error loading promotions: ${e.message}</div>`;
  }
}

async function createPromotion(){
  const services = Array.from($('promo-services').selectedOptions).map(o=>o.value);
  const displayOn = [];
  if($('promo-display-web').checked) displayOn.push('website');
  if($('promo-display-chat').checked) displayOn.push('chat_widget');
  const payload = {
    type: $('promo-type').value,
    value: parseInt($('promo-value').value) || 10,
    description: $('promo-desc').value.trim(),
    voucherCode: $('promo-code').value.trim(),
    services,
    applyTo: services.length > 1 ? 'multiple' : (services.length === 1 ? 'single' : 'any'),
    displayOn,
    durationDays: parseInt($('promo-duration').value) || 7
  };
  try {
    await api(`/api/owner/promotions?tenant=${encodeURIComponent(STATE.tenant)}`, {
      method: 'POST', body: JSON.stringify(payload)
    });
    $('promo-form').hidden = true;
    // Reset form
    $('promo-desc').value = '';
    $('promo-code').value = '';
    $('promo-services').selectedIndex = -1;
    loadPromotions();
  } catch(e){
    $('promo-error').textContent = 'Failed to create: '+e.message;
    $('promo-error').hidden = false;
  }
}

async function activatePromo(id){
  try {
    await api(`/api/owner/promotions/${id}/activate?tenant=${encodeURIComponent(STATE.tenant)}`, {method:'PUT'});
    loadPromotions();
  } catch(e){ alert('Failed: '+e.message); }
}

async function deactivatePromo(id){
  try {
    await api(`/api/owner/promotions/${id}/deactivate?tenant=${encodeURIComponent(STATE.tenant)}`, {method:'PUT'});
    loadPromotions();
  } catch(e){ alert('Failed: '+e.message); }
}

async function viewEffectiveness(id){
  try {
    const data = await api(`/api/owner/reporting/promotion/${id}?tenant=${encodeURIComponent(STATE.tenant)}`);
    const p = data.promotion || {};
    const b = data.baseline || {};
    const d = data.duringPromotion || {};
    const po = data.postPromotion || {};
    alert(
      `[${p.type}] ${p.description||'No description'}\n\n`+
      `BASELINE (7 days before)\n`+
      `  Views/day: ${b.dailyViews}\n`+
      `  Conversions/day: ${b.dailyConversions}\n`+
      `  Rate: ${(b.conversionRate*100).toFixed(1)}%\n\n`+
      `DURING PROMOTION\n`+
      `  Views/day: ${d.dailyViews}\n`+
      `  Conversions/day: ${d.dailyConversions}\n`+
      `  Rate: ${(d.conversionRate*100).toFixed(1)}%\n`+
      `  Impressions: ${d.impressions}\n`+
      `  Clicks: ${d.clicks}\n`+
      `  CTR: ${d.clickThroughRate ? (d.clickThroughRate*100).toFixed(1)+'%' : '—'}\n`+
      (d.conversionUplift ? `  Uplift: ${d.conversionUplift}\n` : '')+
      `\nPOST-PROMOTION (7 days after)\n`+
      `  Views/day: ${po.dailyViews}\n`+
      `  Conversions/day: ${po.dailyConversions}\n`+
      `  Rate: ${(po.conversionRate*100).toFixed(1)}%\n`+
      (po.lastEffect ? `  Effect: ${po.lastEffect}\n` : '')+
      (data.revenueImpact ? `\nRevenue impact: £${data.revenueImpact}` : '')
    );
  } catch(e){ alert('Failed to load effectiveness: '+e.message); }
}

// Load clients for promo service selector on login
async function loadServices(){
  try {
    const data = await api(`/api/owner/reporting?tenant=${encodeURIComponent(STATE.tenant)}`);
    const client = data;
    const services = client.summary?.services || [];
    // No direct services list from reporting, so populate from known patterns or let user type
  } catch(e){}
}

document.addEventListener('DOMContentLoaded', () => {
  // Check if already authenticated (e.g. from deep link)
  $('login-token').addEventListener('keydown', e => { if(e.key==='Enter') login(); });
  $('login-tenant').addEventListener('keydown', e => { if(e.key==='Enter') $('login-token').focus(); });
});

// Expose functions for inline onclick
window.activatePromo = activatePromo;
window.deactivatePromo = deactivatePromo;
window.viewEffectiveness = viewEffectiveness;