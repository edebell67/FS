const BASE = window.location.origin;
let STATE = { tenant: "", token: "", client: null, stream: null };

// Phase 2b: live push. EventSource can't set an Authorization header, so the
// token travels via query string for this one connection — the stream
// endpoint accepts that as a documented exception, not a general relaxation.
// Falls back to nothing worse than the pre-existing polled behaviour: the
// Refresh button and tab-switch reloads still work unmodified if the stream
// never connects or silently drops.
function openReportingStream(){
  closeReportingStream();
  const stream = new EventSource(`${BASE}/api/owner/reporting/stream?tenant=${encodeURIComponent(STATE.tenant)}&token=${encodeURIComponent(STATE.token)}`);
  stream.onmessage = (event) => {
    $('live-status').textContent = 'Live';
    $('live-status').classList.remove('stale');
    try {
      const payload = JSON.parse(event.data);
      renderOverview(payload);
      // Only push into Compare while the owner is on the default 7-day
      // window they'd get from a fresh Refresh — a custom day count is an
      // explicit choice the live push must not silently overwrite.
      if (payload.compare && (parseInt($('compare-days').value) || 7) === 7) renderCompare(payload.compare);
    } catch { /* ignore a malformed frame, keep the connection open */ }
  };
  stream.onerror = () => {
    // EventSource retries on its own; only tell the owner their data may be
    // stale, don't tear anything down — a transient network blip shouldn't
    // force a manual reconnect.
    $('live-status').textContent = 'Reconnecting…';
    $('live-status').classList.add('stale');
  };
  STATE.stream = stream;
}

function closeReportingStream(){
  STATE.stream?.close();
  STATE.stream = null;
}

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
    if(btn.dataset.view==='questions') loadQuestions();
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
    openReportingStream();
  } catch(e){
    $('login-error').textContent = e.message || 'Login failed. Check your site key and token.';
    $('login-error').hidden = false;
  }
}

function logout(){
  closeReportingStream();
  STATE = { tenant:'', token:'', client:null, stream:null };
  $('login-screen').hidden = false;
  $('dash-screen').hidden = true;
  $('login-error').hidden = true;
}

// Shared by the manual fetch (loadOverview) and the live SSE push
// (openReportingStream) — one rendering path, two ways to get data into it,
// per the workflow doc's explicit instruction not to duplicate this logic.
function renderOverview(data){
  STATE.client = data;
  const tracking = data.pageAnalytics;
  const isDisabled = tracking && tracking.status === 'tracking_disabled';
  $('tracking-status').textContent = isDisabled ? 'Web tracking is off' : 'Web tracking is on';
  $('tracking-toggle').checked = !isDisabled;

  $('overview-stats').innerHTML = `
    <div class="stat-card"><span>Unique visitors</span><strong>${tracking?.uniqueVisits||0}</strong></div>
    <div class="stat-card"><span>Page views</span><strong>${tracking?.pageViews||0}</strong></div>
    <div class="stat-card"><span>Conversations</span><strong>${data.summary?.conversations||0}</strong></div>
    <div class="stat-card"><span>Leads captured</span><strong>${data.summary?.leads||0}</strong></div>
  `;

  const reasons = Object.entries(data.leadsByReason || {}).sort((a,b)=>b[1]-a[1]);
  $('overview-reasons-card').hidden = reasons.length === 0;
  if(reasons.length){
    const total = reasons.reduce((sum,[,count])=>sum+count,0);
    $('overview-reasons').innerHTML = reasons.map(([reason,count])=>{
      const pct = total ? Math.round((count/total)*100) : 0;
      const label = reason.replace(/&/g,'&amp;').replace(/</g,'&lt;');
      return `<div class="service-row"><span class="svc-name">${label}</span><span class="svc-val">${count} lead${count===1?'':'s'}</span><span class="svc-change up">${pct}%</span></div>`;
    }).join('');
  }

  const records = Object.entries(data.summary || {}).filter(([k,v])=>v>0&&k!=='previewResponses').slice(0,8);
  $('overview-activity').innerHTML = records.length
    ? records.map(([k,v])=>`<div class="activity-item"><strong>${k}</strong> — ${v} records</div>`).join('')
    : '<div class="empty-state">No activity yet. Activity appears when visitors interact with your site.</div>';
  const selector = $('promo-services');
  const selected = new Set(Array.from(selector.selectedOptions).map((option) => option.value));
  selector.innerHTML = (tracking?.serviceViews || []).map(([service]) => `<option value="${service.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;')}"${selected.has(service) ? ' selected' : ''}>${service.replace(/&/g, '&amp;').replace(/</g, '&lt;')}</option>`).join('');
}

async function loadOverview(){
  try {
    renderOverview(await api(`/api/owner/reporting?tenant=${encodeURIComponent(STATE.tenant)}`));
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

// Phase 2b: shared by the polled Refresh button and the live SSE push, so
// both paths render identically — see openReportingStream() below, which
// calls this with the compare frame that now rides alongside every
// Overview push (default 7-day window only; a non-default day count still
// needs a manual Refresh, matching the days param the owner last chose).
function renderCompare(data){
  const c = data.comparison || {};
  const pc = (v)=>`<span class="change ${v.change.startsWith('+')?'up':'down'}">${v.change}</span>`;
  $('compare-stats').innerHTML = `
    <div class="stat-card"><span>Visitors</span><strong>${c.visitors?.today||0}</strong>${pc(c.visitors||{})}</div>
    <div class="stat-card"><span>Page views</span><strong>${c.pageViews?.today||0}</strong>${pc(c.pageViews||{})}</div>
    <div class="stat-card"><span>Engaged</span><strong>${c.engagedPct?.today||0}%</strong><span class="change">avg ${c.engagedPct?.average||0}%</span></div>
    <div class="stat-card"><span>CTA clicks</span><strong>${c.ctaClicks?.today||0}</strong>${pc(c.ctaClicks||{})}</div>
  `;
  const services = c.perService || [];
  const signals = c.signals || [];
  $('compare-signals').innerHTML = signals.length
    ? signals.map((signal) => `<div class="service-row"><span class="svc-name">${signal.service}</span><span class="svc-val">${signal.viewsToday} views today · average ${signal.averageViews}</span><span class="svc-change up">Act</span></div>`).join('')
    : '<div class="empty-state">No actionable demand signal yet. The dashboard waits for sufficient above-baseline interest.</div>';
  $('compare-services').innerHTML = services.length
    ? services.map(s=>{
        const vc = s.views.change;
        const cc = s.clicks.change;
        return `<div class="service-row"><span class="svc-name">${s.service}</span><span class="svc-val">Views: ${s.views.today} <small>(avg ${s.views.average})</small></span><span class="svc-change ${vc>0?'up':'down'}">${vc>0?'+':''}${vc||0}%</span></div>`;
      }).join('')
    : '<div class="empty-state">No service data yet. Data appears after visitors interact with your services.</div>';
}

async function loadCompare(){
  const days = parseInt($('compare-days').value) || 7;
  try {
    renderCompare(await api(`/api/owner/reporting/compare?tenant=${encodeURIComponent(STATE.tenant)}&days=${days}`));
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

async function loadQuestions(){
  try {
    const data = await api(`/api/owner/question-followups?tenant=${encodeURIComponent(STATE.tenant)}`);
    const renderQuestions = (list) => list.map(q=>`<li>${q.text.replace(/&/g,'&amp;').replace(/</g,'&lt;')}</li>`).join('');
    const pending = data.pending || [];
    $('questions-pending').innerHTML = pending.length
      ? pending.map(r=>`<div class="promo-item">
          <div class="promo-top"><span class="promo-type">${r.email}</span><span class="promo-status active">pending</span></div>
          <ul class="promo-desc">${renderQuestions(r.questions)}</ul>
          <div class="promo-actions"><button class="primary" onclick="resolveQuestionFollowup('${r.id}')">Mark replied</button></div>
        </div>`).join('')
      : '<div class="empty-state">No unanswered questions right now.</div>';
    const resolved = data.resolved || [];
    $('questions-resolved').innerHTML = resolved.length
      ? resolved.map(r=>`<div class="promo-item">
          <div class="promo-top"><span class="promo-type">${r.email}</span><span class="promo-status paused">resolved</span></div>
          <ul class="promo-desc">${renderQuestions(r.questions)}</ul>
        </div>`).join('')
      : '<div class="empty-state">Nothing resolved yet.</div>';
  } catch(e){
    $('questions-pending').innerHTML = `<div class="empty-state">Error loading questions: ${e.message}</div>`;
  }
}

async function resolveQuestionFollowup(id){
  try {
    await api(`/api/owner/question-followups/${id}/resolve?tenant=${encodeURIComponent(STATE.tenant)}`, {method:'PUT'});
    loadQuestions();
  } catch(e){ alert('Failed: '+e.message); }
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
window.resolveQuestionFollowup = resolveQuestionFollowup;
