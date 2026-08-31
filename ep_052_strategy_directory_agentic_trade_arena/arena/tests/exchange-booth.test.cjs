const {test}=require('node:test');
const assert=require('node:assert/strict');
const {exchangeBoothSpec}=require('../exchange-booth.js');

test('directory booth uses recognisable financial-exchange fixtures',()=>{
 const booth=exchangeBoothSpec({label:'GBP',towerHeight:4.2,strategyCount:42,totalTrades:880},3);
 assert.equal(booth.id,'GROUP 04');
 assert.ok(booth.parts.includes('raised trading counter'));
 assert.ok(booth.parts.includes('dual uprights'));
 assert.ok(booth.parts.includes('overhead market header'));
 assert.ok(booth.parts.includes('quote screen'));
 assert.ok(booth.parts.includes('front trade tape'));
 assert.equal(booth.footprint,'octagonal');
 assert.equal(booth.roofFlag.text,'GBP');
 assert.ok(booth.roofFlag.height>0);
 assert.equal(booth.roofFlag.width,2.13);
 assert.equal(booth.roofFlag.height,1.23);
 assert.ok(booth.performanceColumn.height>booth.counter.height);
});
