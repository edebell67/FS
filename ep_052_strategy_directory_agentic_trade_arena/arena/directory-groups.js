(function(root,factory){
 const api=factory();
 if(typeof module==='object'&&module.exports)module.exports=api;
 root.DirectoryGroups=api;
})(typeof window!=='undefined'?window:globalThis,function(){
 'use strict';
 const MIN=4,MAX=48;
 function normalizeBoothCount(value=24){let n=Number.isFinite(+value)?Math.round(+value):24;n=Math.max(MIN,Math.min(MAX,n));return n%2?n-1:n;}
 function uniformGrid(count){const capacity=normalizeBoothCount(count),pairs=[];for(let rows=2;rows<=Math.sqrt(capacity);rows++){if(capacity%rows===0)pairs.push({columns:capacity/rows,rows,capacity});}return pairs.sort((a,b)=>(a.columns-a.rows)-(b.columns-b.rows))[0]||{columns:capacity/2,rows:2,capacity};}
 function firstNumber(row,names){for(const name of names){if(row[name]!=null&&Number.isFinite(Number(row[name])))return Number(row[name]);}return null;}
 function returnParts(row){const closed=firstNumber(row,['closed_net_return','closedNetReturn']);const open=firstNumber(row,['open_net_return','openNetReturn'])||0;const legacy=firstNumber(row,['total_net_return','totalNetReturn'])||0;return{closed:closed==null?legacy:closed,open,total:(closed==null?legacy:closed)+open};}
 function targetValue(row,mode){const value=mode==='target_profit'?firstNumber(row,['target_profit','targetProfit','profit_target','profitTarget']):firstNumber(row,['target_loss','targetLoss','loss_target','lossTarget']);return value==null?null:(mode==='target_loss'?Math.abs(value):value);}
 function metric(row,mode){if(mode==='win_rate')return (Number(row.win_rate??row.winRate)||0)*100;if(mode==='net_return')return returnParts(row).total;if(mode==='target_profit'||mode==='target_loss')return targetValue(row,mode);return Number(row.total_trades??row.totalTrades)||0;}
 function fixedKey(row,mode){if(mode==='product')return String(row.product_name||row.productName||'Unclassified').toUpperCase();if(mode==='product_type')return String(row.market||'Unclassified').toUpperCase();return null;}
 function empty(label,id,availability='available'){return{id,label,availability,strategies:[],strategyCount:0,totalTrades:0,closedNetReturn:0,openNetReturn:0,totalNetReturn:0,winRate:0,towerHeight:1,activeRank:0};}
 function fmt(value){return Number.isInteger(value)?String(value):Number(value.toFixed(2)).toString();}
 function rangeConfig(rows,mode,count){
  if(mode==='win_rate'){const step=Math.floor(100/count)||1;return{step,ceiling:100,label:(i)=>`Win rate ${i*step}–${i===count-1?100:(i+1)*step}%`,flagLabel:(i)=>`${i*step}–${i===count-1?100:(i+1)*step}%`};}
  const values=rows.map(r=>metric(r,mode)).filter(v=>v!=null&&Number.isFinite(v));
  if(!values.length)return null;
  const max=Math.max(0,...values),ceiling=Math.ceil(max/count)*count,step=ceiling/count||1;
  const prefix=mode==='net_return'?'Net return':mode==='target_profit'?'Target profit':mode==='target_loss'?'Target loss':'Trade count';
  return{step,ceiling,label:(i)=>`${prefix} ${fmt(i*step)}–${fmt(i===count-1?ceiling:(i+1)*step)}`};
 }
 function aggregate(groups){
  for(const g of groups){g.strategyCount=g.strategies.length;g.totalTrades=g.strategies.reduce((s,x)=>s+(Number(x.total_trades??x.totalTrades)||0),0);g.closedNetReturn=g.strategies.reduce((s,x)=>s+returnParts(x).closed,0);g.openNetReturn=g.strategies.reduce((s,x)=>s+returnParts(x).open,0);g.totalNetReturn=g.closedNetReturn+g.openNetReturn;g.winRate=g.totalTrades?g.strategies.reduce((s,x)=>s+(Number(x.win_rate??x.winRate)||0)*(Number(x.total_trades??x.totalTrades)||0),0)/g.totalTrades:0;}
  const ranked=[...groups].sort((a,b)=>b.totalNetReturn-a.totalNetReturn);ranked.forEach((g,i)=>g.towerHeight=1.1+(ranked.length-i-1)/Math.max(1,ranked.length-1)*3.2);[...groups].sort((a,b)=>b.totalTrades-a.totalTrades).slice(0,3).forEach((g,i)=>g.activeRank=i+1);
 }
 function buildBoothGroups(rows=[],{mode='product',boothCount=24}={}){
  const count=normalizeBoothCount(boothCount),groups=[];
  if(mode==='product'||mode==='product_type'){const map=new Map();for(const row of rows){const key=fixedKey(row,mode);if(!map.has(key))map.set(key,empty(key,key));map.get(key).strategies.push(row);}groups.push(...map.values());}
  else{
   const config=rangeConfig(rows,mode,count);
   if(!config){const label=mode==='target_profit'?'Profit target unavailable':mode==='target_loss'?'Loss target unavailable':'No published data';return Array.from({length:count},(_,i)=>empty(label,`${mode}-${i+1}`,'unavailable'));}
   for(let i=0;i<count;i++){const group=empty(config.label(i),`${mode}-${i+1}`);group.flagLabel=config.flagLabel?.(i)||group.label;groups.push(group);}
   for(const row of rows){const value=metric(row,mode);if(value==null||!Number.isFinite(value))continue;const index=Math.min(count-1,Math.max(0,Math.floor(value/config.step)));groups[index].strategies.push(row);}
  }
  aggregate(groups);return groups;
 }
 function diffBoothActivity(before=[],after=[]){const old=new Map(before.map(x=>[x.id,x])),result={};for(const item of after){const prior=old.get(item.id);if(!prior)continue;const trades=Math.max(0,item.totalTrades-prior.totalTrades);if(!trades)continue;const delta=item.totalNetReturn-prior.totalNetReturn;result[item.id]={kind:delta>=0?'profit':'loss',trades};}return result;}
 return{normalizeBoothCount,uniformGrid,buildBoothGroups,diffBoothActivity};
});
