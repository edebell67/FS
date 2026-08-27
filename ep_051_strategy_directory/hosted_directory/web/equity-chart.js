/* Version history: 1.1.0 (2026-08-27) real responsive coordinates and touch inspection; 1.0.0 premium SVG equity curve. */
(function(){
  const money=n=>Number(n).toLocaleString(undefined,{minimumFractionDigits:0,maximumFractionDigits:0,signDisplay:'always'});
  function render(host,payload){
    const points=payload.points||[];if(!points.length){host.innerHTML='<div class="chart-empty">No closed trades in this evidence window.</div>';return}
    const W=Math.max(280,Math.min(1200,host.clientWidth)),H=W<600?320:430,pad={l:55,r:20,t:35,b:52},values=points.map(p=>p.equity),min=Math.min(0,...values),max=Math.max(0,...values),span=max-min||1;
    const x=i=>pad.l+i*(W-pad.l-pad.r)/Math.max(1,points.length-1),y=v=>pad.t+(max-v)*(H-pad.t-pad.b)/span;
    const line=points.map((p,i)=>`${i?'L':'M'}${x(i).toFixed(1)},${y(p.equity).toFixed(1)}`).join(' '),zero=y(0),area=`${line} L${x(points.length-1)},${zero} L${x(0)},${zero} Z`;
    const ticks=[0,.25,.5,.75,1].map(t=>{const v=max-span*t,yy=pad.t+(H-pad.t-pad.b)*t;return `<g><line x1="${pad.l}" x2="${W-pad.r}" y1="${yy}" y2="${yy}" class="chart-grid"/><text x="${pad.l-12}" y="${yy+4}" text-anchor="end">${money(v)}</text></g>`}).join('');
    const first=points[0],last=points.at(-1),peak=Math.max(...values),maxDd=Math.min(...points.map(p=>p.drawdown));
    host.innerHTML=`<div class="chart-kpis"><div><span>Period return</span><b>${money(last.equity)}</b></div><div><span>Peak equity</span><b>${money(peak)}</b></div><div><span>Maximum drawdown</span><b>${money(maxDd)}</b></div><div><span>Closed trades</span><b>${points.length.toLocaleString()}</b></div></div><div class="chart-stage"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Cumulative net return equity curve"><defs><linearGradient id="eq-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9ef69" stop-opacity=".42"/><stop offset="1" stop-color="#c9ef69" stop-opacity="0"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>${ticks}<path d="${area}" fill="url(#eq-fill)"/><line x1="${pad.l}" x2="${W-pad.r}" y1="${zero}" y2="${zero}" class="zero-line"/><path d="${line}" class="equity-line" filter="url(#glow)"/><line id="chartCross" y1="${pad.t}" y2="${H-pad.b}" class="chart-cross"/><circle id="chartDot" r="6" class="chart-dot"/><rect id="chartHit" x="${pad.l}" y="${pad.t}" width="${W-pad.l-pad.r}" height="${H-pad.t-pad.b}" fill="transparent"/><text x="${pad.l}" y="${H-18}" class="axis-date">${new Date(first.closed_at).toLocaleDateString()}</text><text x="${W-pad.r}" y="${H-18}" text-anchor="end" class="axis-date">${new Date(last.closed_at).toLocaleDateString()}</text></svg><div id="chartTip" class="chart-tip"></div></div><p class="chart-basis">Cumulative net return · costs and commission included · hover to inspect each closed trade</p>`;
    const svg=host.querySelector('svg'),hit=host.querySelector('#chartHit'),cross=host.querySelector('#chartCross'),dot=host.querySelector('#chartDot'),tip=host.querySelector('#chartTip');
    hit.addEventListener('pointermove',e=>{const r=svg.getBoundingClientRect(),px=(e.clientX-r.left)/r.width*W,i=Math.max(0,Math.min(points.length-1,Math.round((px-pad.l)/(W-pad.l-pad.r)*(points.length-1)))),p=points[i],xx=x(i),yy=y(p.equity);cross.setAttribute('x1',xx);cross.setAttribute('x2',xx);dot.setAttribute('cx',xx);dot.setAttribute('cy',yy);cross.style.opacity=dot.style.opacity=1;tip.style.opacity=1;tip.style.left=`${Math.min(82,Math.max(8,e.offsetX/r.width*100))}%`;tip.innerHTML=`<span>Trade ${p.trade_number} · ${new Date(p.closed_at).toLocaleString()}</span><b>${money(p.equity)}</b><em>${money(p.net_return)} trade · ${money(p.drawdown)} drawdown</em>`});
    hit.addEventListener('pointerdown',e=>hit.dispatchEvent(new PointerEvent('pointermove',{clientX:e.clientX,clientY:e.clientY,bubbles:true})));
    hit.addEventListener('pointerleave',()=>{cross.style.opacity=tip.style.opacity=0;dot.style.opacity=points.length===1?1:0});
    if(points.length===1){dot.setAttribute('cx',x(0));dot.setAttribute('cy',y(points[0].equity));dot.style.opacity=1}
    host.querySelector('.chart-basis').textContent='Cumulative net return · costs and commission included · tap or hover to inspect each closed trade';
    if(host._equityObserver)host._equityObserver.disconnect();
    let previousWidth=host.clientWidth;
    host._equityObserver=new ResizeObserver(()=>{if(Math.abs(host.clientWidth-previousWidth)>1){host._equityObserver.disconnect();render(host,payload)}});
    host._equityObserver.observe(host);
  }
  globalThis.DnaEquityChart={render};
})();
