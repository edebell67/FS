const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('C:/Users/edebe/eds/TradeApps/breakout/fs/trade_bucket.html', 'utf8');
const bucketJson = fs.readFileSync('C:/Users/edebe/eds/TradeApps/breakout/fs/json/live/2026-03-11/_trade_buckets.json', 'utf8');

const lastBuckets = JSON.parse(bucketJson).buckets;
const lastTradeRows = [];  // Empty trades just to test rendering crash

const dom = new JSDOM(html, { runScripts: "dangerously" });
const window = dom.window;

// Mock the DOM and inject our data
window.document.getElementById('bucketsContainer').innerHTML = ''; // Ensure container exists
window.lastBuckets = lastBuckets;
window.lastTradeRows = lastTradeRows;

// Mock console to catch errors
window.console.error = (msg, e) => { console.log("JSDOM ERROR:", msg, e); };
window.console.warn = (msg) => { console.log("JSDOM WARN:", msg); };

try {
    window.renderBuckets(lastBuckets, lastTradeRows);
    console.log("RENDER SUCCESS!");
} catch(e) {
    console.log("CAUGHT ERROR IN RENDER BUCKETS:", e);
}
