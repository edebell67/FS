/* Version history: 1.2.0 (2026-08-30) adds dayBack/dayForward buttons that
   shift the current From/To window by one day, preserving its width
   (a single day stays a single day, a week stays a week, etc); no-op on
   "All history" since there are no dates to shift. 1.1.0 (2026-08-26)
   initializes the directory to Current day; 1.0.0 shared day/week/month/
   custom evidence-period controller. */
(function(){
  const iso=d=>{const x=new Date(d.getTime()-d.getTimezoneOffset()*60000);return x.toISOString().slice(0,10)};
  const title=(from,to)=>from&&to?(from===to?new Date(from+'T00:00:00').toLocaleDateString(undefined,{dateStyle:'long'}):`${new Date(from+'T00:00:00').toLocaleDateString()} — ${new Date(to+'T00:00:00').toLocaleDateString()}`):'All available history';
  function setPreset(kind,notify=true){const now=new Date(),from=new Date(now),to=new Date(now);if(kind==='week'){const day=(now.getDay()+6)%7;from.setDate(now.getDate()-day);to.setDate(from.getDate()+6)}if(kind==='month'){from.setDate(1);to.setMonth(from.getMonth()+1,0)}if(kind==='all'){dateFrom.value='';dateTo.value=''}else{dateFrom.value=iso(from);dateTo.value=iso(to)}document.querySelectorAll('[data-period]').forEach(b=>b.classList.toggle('active',b.dataset.period===kind));periodLabel.textContent=title(dateFrom.value,dateTo.value);if(notify)document.dispatchEvent(new CustomEvent('periodchange'))}
  function apply(){if(dateFrom.value&&dateTo.value&&dateFrom.value>dateTo.value){dateTo.setCustomValidity('End date must be on or after start date');dateTo.reportValidity();return}dateTo.setCustomValidity('');document.querySelectorAll('[data-period]').forEach(b=>b.classList.remove('active'));periodLabel.textContent=title(dateFrom.value,dateTo.value);document.dispatchEvent(new CustomEvent('periodchange'))}
  function shiftDay(delta){if(!dateFrom.value&&!dateTo.value)return;if(dateFrom.value){const from=new Date(dateFrom.value+'T00:00:00');from.setDate(from.getDate()+delta);dateFrom.value=iso(from)}if(dateTo.value){const to=new Date(dateTo.value+'T00:00:00');to.setDate(to.getDate()+delta);dateTo.value=iso(to)}apply()}
  document.querySelectorAll('[data-period]').forEach(b=>b.addEventListener('click',()=>setPreset(b.dataset.period)));applyPeriod.addEventListener('click',apply);dayBack.addEventListener('click',()=>shiftDay(-1));dayForward.addEventListener('click',()=>shiftDay(1));setPreset('today',false);globalThis.DnaPeriod={params:()=>({date_from:dateFrom.value||'',date_to:dateTo.value||''}),setPreset};
})();
