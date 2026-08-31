const {test}=require('node:test');
const assert=require('node:assert/strict');
const {buildBoothGroups,normalizeBoothCount,diffBoothActivity,uniformGrid}=require('../directory-groups.js');

const rows=[
 {strategy_id:'DNA_A',product_name:'GBP',market:'FX',win_rate:.8,total_net_return:120,total_trades:20,descriptive_name:'ALPHA'},
 {strategy_id:'DNA_B',product_name:'EUR',market:'FX',win_rate:.4,total_net_return:-30,total_trades:8,descriptive_name:'BETA'},
 {strategy_id:'DNA_C',product_name:'GBP',market:'FX',win_rate:.6,total_net_return:50,total_trades:14,descriptive_name:'GAMMA'},
];

test('booth count is even and bounded with 24 as default',()=>{
 assert.equal(normalizeBoothCount(),24);
 assert.equal(normalizeBoothCount(25),24);
 assert.equal(normalizeBoothCount(3),4);
 assert.equal(normalizeBoothCount(50),48);
});
test('product grouping aggregates strategies and ranks tower height by net return',()=>{
 const groups=buildBoothGroups(rows,{mode:'product',boothCount:24});
 assert.equal(groups.length,2);
 assert.equal(groups[0].label,'GBP');
 assert.equal(groups[0].strategyCount,2);
 assert.equal(groups[0].totalTrades,34);
 assert.ok(groups[0].towerHeight>groups[1].towerHeight);
});
test('groups retain closed and open net-return components while tower ranking uses their total',()=>{
 const groups=buildBoothGroups([{strategy_id:'CLOSED_OPEN',product_name:'GBP',market:'FX',total_trades:12,closed_net_return:80,open_net_return:20,win_rate:.6},{strategy_id:'LOSS',product_name:'EUR',market:'FX',total_trades:12,closed_net_return:20,open_net_return:-5,win_rate:.6}],{mode:'product'});
 assert.equal(groups[0].closedNetReturn,80);
 assert.equal(groups[0].openNetReturn,20);
 assert.equal(groups[0].totalNetReturn,100);
 assert.ok(groups[0].towerHeight>groups[1].towerHeight);
});
test('dynamic net-return bands start at zero and round the ceiling to an even grid capacity',()=>{
 const groups=buildBoothGroups([{strategy_id:'TOP',product_name:'GBP',market:'FX',total_trades:1,closed_net_return:575,open_net_return:0},{strategy_id:'LOW',product_name:'GBP',market:'FX',total_trades:1,closed_net_return:48,open_net_return:0}],{mode:'net_return',boothCount:12});
 assert.equal(groups.length,12);
 assert.equal(groups[0].label,'Net return 0–48');
 assert.equal(groups.at(-1).label,'Net return 528–576');
 assert.equal(groups[1].strategyCount,1);
 assert.equal(groups.at(-1).strategyCount,1);
});
test('win-rate bands divide the 0–100 scale and close at 100 percent',()=>{
 const groups=buildBoothGroups(rows,{mode:'win_rate',boothCount:12});
 assert.equal(groups[0].label,'Win rate 0–8%');
 assert.equal(groups[0].flagLabel,'0–8%');
 assert.equal(groups.at(-1).label,'Win rate 88–100%');
});
test('target bands use published target maxima but remain unavailable without source attributes',()=>{
 const missing=buildBoothGroups(rows,{mode:'target_profit',boothCount:4});
 assert.equal(missing[0].availability,'unavailable');
 const groups=buildBoothGroups([{strategy_id:'A',product_name:'GBP',market:'FX',total_trades:1,target_profit:55,target_loss:12},{strategy_id:'B',product_name:'EUR',market:'FX',total_trades:1,target_profit:10,target_loss:4}],{mode:'target_profit',boothCount:12});
 assert.equal(groups.at(-1).label,'Target profit 55–60');
 assert.equal(groups.at(-1).strategyCount,1);
 const loss=buildBoothGroups([{strategy_id:'L1',product_name:'GBP',market:'FX',total_trades:1,target_loss:-12},{strategy_id:'L2',product_name:'EUR',market:'FX',total_trades:1,target_loss:-4}],{mode:'target_loss',boothCount:4});
 assert.equal(loss.at(-1).label,'Target loss 9–12');
 assert.equal(loss.at(-1).strategyCount,1);
});
test('activity diff marks new trades and closed profit/loss pulses',()=>{
 const before=[{id:'GBP',totalTrades:10,totalNetReturn:5},{id:'EUR',totalTrades:8,totalNetReturn:2}];
 const after=[{id:'GBP',totalTrades:12,totalNetReturn:9},{id:'EUR',totalTrades:9,totalNetReturn:-1}];
 const result=diffBoothActivity(before,after);
 assert.deepEqual(result.GBP,{kind:'profit',trades:2});
 assert.deepEqual(result.EUR,{kind:'loss',trades:1});
});
test('uniform grids never leave a partial final row',()=>{
 assert.deepEqual(uniformGrid(12),{columns:4,rows:3,capacity:12});
 assert.deepEqual(uniformGrid(24),{columns:6,rows:4,capacity:24});
 assert.deepEqual(uniformGrid(10),{columns:5,rows:2,capacity:10});
});
