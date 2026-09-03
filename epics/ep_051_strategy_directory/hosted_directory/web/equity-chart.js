/* Version history: 1.2.0 (2026-09-02) split buy/sell cumulative lines on the same chart, toggle between single and split view. 1.1.0 (2026-08-27) real responsive coordinates and touch inspection; 1.0.0 premium SVG equity curve. */
(function(){
  const money=n=>Number(n).toLocaleString(undefined,{minimumFractionDigits:0,maximumFractionDigits:0,signDisplay:'always'});
  function splitSeries(points){
    let buyEq=0,sellEq=0,buyN=0,sellN=0;
    return points.map(p=>{
      const side=(p.signal||'').toUpperCase();
      if(side==='BUY'){buyEq+=p.net_return;buyN++}else if(side==='SELL'){sellEq+=p.net_return;sellN++}
      return {...p,buy_equity:buyEq,sell_equity:sellEq,buy_count:buyN,sell_count:sellN};
    });
  }
  function render(host,payload,mode){
    const points=payload.points||[];if(!points.length){host.innerHTML='<div class="chart-empty">No closed trades in this evidence window.</div>';return}
    const hasSides=points.some(p=>p.signal);
    mode=mode||host._equityMode||'single';
    if(mode==='split'&&!hasSides)mode='single';
    host._equityMode=mode;
    const split=hasSides?splitSeries(points):null;
    const W=Math.max(280,Math.min(1200,host.clientWidth)),H=W<600?320:430,pad={l:55,r:20,t:35,b:52};
    const values=mode==='split'?[0,...split.map(p=>p.buy_equity),...split.map(p=>p.sell_equity)]:points.map(p=>p.equity);
    const min=Math.min(0,...values),max=Math.max(0,...values),span=max-min||1;
    const x=i=>pad.l+i*(W-pad.l-pad.r)/Math.max(1,points.length-1),y=v=>pad.t+(max-v)*(H-pad.t-pad.b)/span;
    const zero=y(0);
    const lineFor=key=>points.map((p,i)=>`${i?'L':'M'}${x(i).toFixed(1)},${y((mode==='split'?split[i][key]:p.equity)).toFixed(1)}`).join(' ');
    const line=mode==='split'?null:lineFor('equity'),area=line?`${line} L${x(points.length-1)},${zero} L${x(0)},${zero} Z`:null;
    const buyLine=mode==='split'?lineFor('buy_equity'):null,sellLine=mode==='split'?lineFor('sell_equity'):null;
    const ticks=[0,.25,.5,.75,1].map(t=>{const v=max-span*t,yy=pad.t+(H-pad.t-pad.b)*t;return `<g><line x1="${pad.l}" x2="${W-pad.r}" y1="${yy}" y2="${yy}" class="chart-grid"/><text x="${pad.l-12}" y="${yy+4}" text-anchor="end">${money(v)}</text></g>`}).join('');
    const first=points[0],last=points.at(-1),peak=Math.max(...values),maxDd=Math.min(...points.map(p=>p.drawdown));
    const toggle=hasSides?`<div class="chart-mode-toggle"><button type="button" data-mode="single" class="${mode==='single'?'active':''}">Single</button><button type="button" data-mode="split" class="${mode==='split'?'active':''}">Split buy/sell</button></div>`:'';
    const legend=mode==='split'?`<div class="chart-legend"><span class="swatch buy"></span>Buy cumulative<span class="swatch sell"></span>Sell cumulative</div>`:'';
    host.innerHTML=`<div class="chart-kpis"><div><span>Period return</span><b>${money(last.equity)}</b></div><div><span>Peak equity</span><b>${money(peak)}</b></div><div><span>Maximum drawdown</span><b>${money(maxDd)}</b></div><div><span>Closed trades</span><b>${points.length.toLocaleString()}</b></div></div>${toggle}<div class="chart-stage"><svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Cumulative net return equity curve"><defs><linearGradient id="eq-fill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#c9ef69" stop-opacity=".42"/><stop offset="1" stop-color="#c9ef69" stop-opacity="0"/></linearGradient><filter id="glow"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>${ticks}${mode==='split'?'':`<path d="${area}" fill="url(#eq-fill)"/>`}<line x1="${pad.l}" x2="${W-pad.r}" y1="${zero}" y2="${zero}" class="zero-line"/>${mode==='split'?`<path d="${buyLine}" class="equity-line buy-line" filter="url(#glow)"/><path d="${sellLine}" class="equity-line sell-line" filter="url(#glow)"/>`:`<path d="${line}" class="equity-line" filter="url(#glow)"/>`}<line id="chartCross" y1="${pad.t}" y2="${H-pad.b}" class="chart-cross"/><circle id="chartDot" r="6" class="chart-dot"/><rect id="chartHit" x="${pad.l}" y="${pad.t}" width="${W-pad.l-pad.r}" height="${H-pad.t-pad.b}" fill="transparent"/><text x="${pad.l}" y="${H-18}" class="axis-date">${new Date(first.closed_at).toLocaleDateString()}</text><text x="${W-pad.r}" y="${H-18}" text-anchor="end" class="axis-date">${new Date(last.closed_at).toLocaleDateString()}</text></svg><div id="chartTip" class="chart-tip"></div></div>${legend}<p class="chart-basis">Cumulative net return · costs and commission included · ${mode==='split'?'buy and sell tracked independently, each flat between its own trades · ':''}hover to inspect each closed trade</p>`;
    const svg=host.querySelector('svg'),hit=host.querySelector('#chartHit'),cross=host.querySelector('#chartCross'),dot=host.querySelector('#chartDot'),tip=host.querySelector('#chartTip');
    hit.addEventListener('pointermove',e=>{
      const r=svg.getBoundingClientRect(),px=(e.clientX-r.left)/r.width*W,i=Math.max(0,Math.min(points.length-1,Math.round((px-pad.l)/(W-pad.l-pad.r)*(points.length-1)))),p=points[i],xx=x(i);
      const v=mode==='split'?split[i].buy_equity:p.equity,yy=y(v);
      cross.setAttribute('x1',xx);cross.setAttribute('x2',xx);dot.setAttribute('cx',xx);dot.setAttribute('cy',yy);cross.style.opacity=dot.style.opacity=1;tip.style.opacity=1;tip.style.left=`${Math.min(82,Math.max(8,e.offsetX/r.width*100))}%`;
      tip.innerHTML=mode==='split'
        ?`<span>Trade ${p.trade_number} · ${new Date(p.closed_at).toLocaleString()} · ${p.signal||'—'}</span><b>buy ${money(split[i].buy_equity)} · sell ${money(split[i].sell_equity)}</b><em>${money(p.net_return)} this trade</em>`
        :`<span>Trade ${p.trade_number} · ${new Date(p.closed_at).toLocaleString()}</span><b>${money(p.equity)}</b><em>${money(p.net_return)} trade · ${money(p.drawdown)} drawdown</em>`;
    });
    hit.addEventListener('pointerdown',e=>hit.dispatchEvent(new PointerEvent('pointermove',{clientX:e.clientX,clientY:e.clientY,bubbles:true})));
    hit.addEventListener('pointerleave',()=>{cross.style.opacity=tip.style.opacity=0;dot.style.opacity=points.length===1?1:0});
    if(points.length===1){dot.setAttribute('cx',x(0));dot.setAttribute('cy',y(mode==='split'?split[0].buy_equity:points[0].equity));dot.style.opacity=1}
    host.querySelectorAll('.chart-mode-toggle button').forEach(btn=>btn.addEventListener('click',()=>render(host,payload,btn.dataset.mode)));
    if(host._equityObserver)host._equityObserver.disconnect();
    let previousWidth=host.clientWidth;
    host._equityObserver=new ResizeObserver(()=>{if(Math.abs(host.clientWidth-previousWidth)>1){host._equityObserver.disconnect();render(host,payload,host._equityMode)}});
    host._equityObserver.observe(host);
  }
  globalThis.DnaEquityChart={render};
})();
