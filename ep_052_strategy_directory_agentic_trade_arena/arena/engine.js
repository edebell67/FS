/* Deterministic, framework-free demo ledger. All amounts are normalised USD.
 * VERSION HISTORY
 * v1.1.0 · 2026-08-29 · Adds governed owner messages and participation/safety commands.
 * v1.0.0 · 2026-08-28 · Initial Arena simulation and accounting ledger.
 */
(function(root){
 'use strict';
 const FEE=.0001, DAY=24, YEAR=365;
 const catalog=[['VECTOR','Momentum','VX',.0018],['AEGIS','Defensive','AG',-.0004],['PULSE','Mean reversion','PL',.0003],['ORBIT','Macro rotation','OR',.0008],['PRISM','Statistical arb','PR',.0001],['DRIFT','Trend following','DF',.0012],['HELIX','Volatility','HX',-.0006],['NEXUS','Multi-factor','NX',.0006]];
 const names=['AX-427','NOVA-8','AEGIS-4','KITE-09','ATLAS-7','SABLE-3','ION-112','LYRA-6','ROOK-21','ECHO-88','TESS-4','ONYX-9','VEGA-12','FLUX-31','ARC-17','CIPHER-2','MICA-4','DELTA-5','QUILL-7','SOL-19','FEN-22','MOTH-6','ZEN-43','IRIS-24','WREN-11','LUX-29','TIDE-32','AERO-6','EDGE-12','CORAL-9','NIMBUS-3','MARS-11','ZERO-4','RIFT-29','DUSK-8','EMBER-6'];
 class ArenaEngine {
  constructor(seed=52028,bootstrap=true){
   this.seed=seed;this.hour=0;this.regime='balanced';this.agents=[];this.events=[];this.stories=[];this.eventId=0;this.decisions=0;this.totalQueries=0;this.nextAgent=1;
   this.strategies=catalog.map((s,i)=>({id:i,name:s[0],family:s[1],code:s[2],bias:s[3],history:[1],index:1}));
   this.instruments=[...this.strategies.map(s=>this.instrument(s,false)),...[0,3,5,6].map(i=>this.instrument(this.strategies[i],true))];
   if(bootstrap){for(let i=0;i<36;i++)this.join(i<2);for(let i=0;i<112;i++)this.step(3,false);this.exit(this.agents[18]);this.join();this.events=this.events.slice(0,90);this.story('The floor is open.',`${this.activeAgents().length} autonomous agents. ${this.instruments.length} booths. One common $1 starting line.`,'ARENA OPEN');}
  }
  random(){this.seed=(Math.imul(1664525,this.seed)+1013904223)>>>0;return this.seed/4294967296;}
  pick(xs){return xs[Math.floor(this.random()*xs.length)];}
  instrument(s,flip){return{id:s.code+(flip?'-F':'-L'),strategy:s.id,name:s.name+(flip?' FLIP':''),flip,price:.01,supply:160+(s.id%4)*60,available:160+(s.id%4)*60,history:[.01],trades:0};}
  nav(a){return a.cash+Object.entries(a.holdings).reduce((v,[id,q])=>v+q*this.instruments.find(x=>x.id===id).price,0);}
  ret(a){return(this.nav(a)-1)*100;}
  activeAgents(){return this.agents.filter(a=>a.status==='active');}
  record(type,a,instrument,text,extra={}){const e={id:++this.eventId,hour:this.hour,type,agent:a?.id||null,name:a?.name||'ARENA',instrument:instrument?.id||null,text,...extra};this.events.unshift(e);if(this.events.length>240)this.events.pop();return e;}
  story(title,body,kind='FLOOR SIGNAL',event=null){this.stories.unshift({id:this.eventId+'-'+this.hour+'-'+this.stories.length,title,body,kind,hour:this.hour,event,regime:this.regime});this.stories=this.stories.slice(0,24);}
  join(owned=false){if(owned&&this.agents.filter(a=>a.owned).length>=10)return null;const n=this.nextAgent++;const a={id:'agent-'+n,name:names[n-1]||'AGENT-'+String(n+400).padStart(3,'0'),owned,status:'active',mode:'full',cash:1,lots:[{amount:1,since:this.hour}],holdings:{},fees:0,queryFees:0,interest:0,queries:0,decisions:0,created:this.hour,history:[1],peak:1,drawdown:0,positive:0,samples:0,personality:this.pick(['Adaptive','Defensive','Momentum','Contrarian','Low turnover']),last:'Entered with $1.0000',lastInstrument:null,ownerMessages:[],ownerCommands:[]};this.agents.push(a);this.record('join',a,null,'joined the Arena with $1.0000');return a;}
  spend(a,amount){if(amount>a.cash+1e-10)return false;a.cash-=amount;let left=amount;for(const l of a.lots){const take=Math.min(l.amount,left);l.amount-=take;left-=take;if(left<1e-12)break;}a.lots=a.lots.filter(l=>l.amount>1e-12);return true;}
  credit(a,amount,eligible=true){a.cash+=amount;if(eligible)a.lots.push({amount,since:this.hour});}
  buy(a,id,budget){const x=this.instruments.find(x=>x.id===id);if(!x||a.status!=='active'||a.cash<=FEE||x.available<1e-7)return false;const heldFamilies=new Set(Object.keys(a.holdings).map(k=>this.instruments.find(i=>i.id===k).strategy));if(!heldFamilies.has(x.strategy)&&heldFamilies.size>=10)return false;const value=Math.min(budget,a.cash-FEE,x.available*x.price);if(value<.00001)return false;const q=value/x.price;if(!this.spend(a,value+FEE))return false;a.holdings[id]=(a.holdings[id]||0)+q;x.available=Math.max(0,x.available-q);a.fees+=FEE;a.decisions++;this.decisions++;x.trades++;a.last=`Bought ${q.toFixed(2)} ${x.name} units`;a.lastInstrument=id;const e=this.record(x.flip?'buy-flip':'buy',a,x,`bought ${q.toFixed(2)} ${x.name} units`,{units:q,value,fee:FEE,price:x.price});if(x.available<1e-7){this.record('sold-out',a,x,`${x.name} is fully allocated`);this.story(`${x.name} is sold out.`,`All ${x.supply} units are held by agents. New allocations are closed until units return. Unit value: $${x.price.toFixed(5)}.`,'CAPACITY ALERT',e.id);}return true;}
  sell(a,id,fraction=1){const x=this.instruments.find(x=>x.id===id),q=(a.holdings[id]||0)*fraction;if(!x||q<=0||a.status==='exited')return false;const gross=q*x.price;if(a.cash+gross<FEE)return false;a.holdings[id]-=q;if(a.holdings[id]<1e-8)delete a.holdings[id];x.available=Math.min(x.supply,x.available+q);this.credit(a,gross);this.spend(a,FEE);a.fees+=FEE;a.decisions++;this.decisions++;x.trades++;a.last=`Sold ${q.toFixed(2)} ${x.name} units`;a.lastInstrument=id;const e=this.record(x.flip?'sell-flip':'sell',a,x,`sold ${q.toFixed(2)} ${x.name} units`,{units:q,value:gross,fee:FEE,price:x.price});if(q>4&&this.random()<.16)this.story(`${a.name} changes exposure.`,`${a.name} sold ${q.toFixed(2)} ${x.name} units at $${x.price.toFixed(5)}. Agent return at this event: ${this.ret(a).toFixed(2)}%, after fees.`,'AGENT MOVE',e.id);return true;}
  query(a){if(a.status!=='active'||a.cash<FEE)return false;this.spend(a,FEE);a.queryFees+=FEE;a.queries++;this.totalQueries++;const scope=this.random()<.5?'Arena allocation flows':'strategy intelligence';a.last=`Queried ${scope}`;this.record('query',a,null,`queried ${scope} · $0.0001`,{fee:FEE});return true;}
  exit(a){if(a.status!=='active')return false;for(const id of Object.keys(a.holdings))if(!this.sell(a,id))return false;a.status='exited';a.exited=this.hour;a.last='Exited · record retained';this.record('exit',a,null,'left the floor · record retained');this.story(`${a.name} leaves the floor.`,`Final simulated return: ${this.ret(a).toFixed(2)}%. Its history remains visible. An exit never resets an agent.`,'AGENT EXIT');return true;}
  ownerCommand(a,type,payload={}){
   if(!a||!a.owned)return{ok:false,message:'Only the participant owner can send this command.'};
   a.mode=a.mode||'full';a.ownerMessages=a.ownerMessages||[];a.ownerCommands=a.ownerCommands||[];
   let detail='';
   if(type==='read_only'){
    if(a.status!=='active')return{ok:false,message:'An exited agent cannot change participation mode.'};
    a.mode='read-only';detail='entered read-only mode; valuation and cash interest continue, but no new autonomous decisions execute';
   }else if(type==='participate'){
    if(a.status!=='active')return{ok:false,message:'An exited agent cannot rejoin. Its record is permanent.'};
    a.mode='full';detail='resumed full autonomous participation';
   }else if(type==='exit_strategy'){
    if(a.status!=='active')return{ok:false,message:'The agent is no longer active.'};
    const id=String(payload.instrument||''),x=this.instruments.find(x=>x.id===id);
    if(!x||!(a.holdings[id]>0))return{ok:false,message:'The selected strategy is not held by this agent.'};
    const units=a.holdings[id];if(!this.sell(a,id))return{ok:false,message:'The exit could not be executed.'};detail=`exited ${units.toFixed(2)} units of ${x.name} under the owner safety mandate`;
   }else if(type==='exit_all'){
    if(a.status!=='active')return{ok:false,message:'The agent is no longer active.'};
    const count=Object.keys(a.holdings).length;for(const id of [...Object.keys(a.holdings)])if(!this.sell(a,id))return{ok:false,message:'The exit-all mandate could not be completed.'};detail=`exited all positions across ${count} strategies and moved to cash`;
   }else if(type==='leave'){
    if(!this.exit(a))return{ok:false,message:'The agent has already left the Arena.'};detail='left the Arena; its verified record remains';
   }else if(type==='message'){
    const text=String(payload.text||'').trim().slice(0,280);if(!text)return{ok:false,message:'Write a message before sending.'};
    const message={id:`msg-${this.eventId+1}`,hour:this.hour,text};a.ownerMessages.unshift(message);a.ownerMessages=a.ownerMessages.slice(0,40);detail=`received owner context: “${text}”`;
   }else return{ok:false,message:'Unknown owner command.'};
   const command={id:`cmd-${this.eventId+1}`,hour:this.hour,type,detail};a.ownerCommands.unshift(command);a.ownerCommands=a.ownerCommands.slice(0,60);a.last=detail;this.record('owner-command',a,null,detail,{command:type});return{ok:true,message:detail};
  }
  step(hours=3,allowJoin=true){
   this.hour+=hours;
   const direction={balanced:0,bull:.003,bear:-.0035,volatile:0}[this.regime]||0;
   const vol=this.regime==='volatile'?.015:.006;
   const market=(this.random()-.48)*vol+direction;
   const changes=this.strategies.map(s=>{const r=Math.max(-.06,Math.min(.06,market*(s.id===1?-.3:1)+(this.random()-.5)*vol+s.bias));s.index=Math.max(.05,Math.min(5,s.index*(1+r)));s.history.push(s.index);if(s.history.length>120)s.history.shift();return r;});
   for(const x of this.instruments){x.price=Math.max(.0002,Math.min(.05,x.price*(1+(x.flip?-1:1)*changes[x.strategy])));x.history.push(x.price);if(x.history.length>120)x.history.shift();}
   for(const a of this.activeAgents()){
    for(const lot of a.lots){const days=Math.floor((this.hour-lot.since)/DAY);if(days>0){const interest=lot.amount*.03*days/YEAR;a.cash+=interest;a.interest+=interest;lot.since+=days*DAY;}}
    const held=Object.keys(a.holdings);const defensive=a.personality==='Defensive'&&this.regime==='bear';
    if((a.mode||'full')==='full'){
     if(this.random()<.09)this.query(a);
     if(held.length&&this.random()<(defensive?.27:.12))this.sell(a,this.pick(held),this.random()<.6?1:.5);
     else if(this.random()<(a.personality==='Low turnover'?.055:.24)&&a.cash>.01){let choices=this.instruments.filter(x=>x.available>1e-5);if(this.regime==='bear'&&a.personality!=='Momentum')choices=choices.filter(x=>x.flip||x.strategy===1);if(this.regime==='bull'&&a.personality!=='Contrarian')choices=choices.filter(x=>!x.flip);if(choices.length)this.buy(a,this.pick(choices).id,.035+this.random()*.14);}
    }
    const n=this.nav(a);const prior=a.history[a.history.length-1];a.positive+=n>=prior?1:0;a.samples++;a.history.push(n);if(a.history.length>120)a.history.shift();a.peak=Math.max(a.peak,n);a.drawdown=Math.max(a.drawdown,(a.peak-n)/a.peak);
   }
   if(allowJoin&&this.activeAgents().length<65&&this.random()<.08)this.join();
   if(allowJoin&&this.activeAgents().length>30&&this.random()<.025){const candidates=this.activeAgents().filter(a=>!a.owned);this.exit(this.pick(candidates));}
   if(allowJoin&&this.random()<.12){const top=[...this.agents].sort((a,b)=>this.ret(b)-this.ret(a))[0];this.story(`${top.name} leads the Arena.`,`A ${this.ret(top).toFixed(2)}% simulated return from $1. ${top.decisions} allocation decisions; $${(top.fees+top.queryFees).toFixed(4)} in total fees. Performance is not proof of skill.`,'LEADER WATCH');}
  }
  consistency(a){return a.samples?100*a.positive/a.samples:0;}
  snapshot(){return JSON.stringify({version:1,...this});}
  static restore(json){const data=JSON.parse(json);if(data.version!==1||!Array.isArray(data.agents)||!Array.isArray(data.instruments))throw Error('Invalid demo state');const e=new ArenaEngine(1,false);Object.assign(e,data);for(const a of e.agents){a.mode=a.mode||'full';a.ownerMessages=a.ownerMessages||[];a.ownerCommands=a.ownerCommands||[];}return e;}
 }
 if(typeof module!=='undefined'&&module.exports)module.exports={ArenaEngine,FEE};else root.ArenaEngine=ArenaEngine;
})(typeof window==='undefined'?{}:window);
