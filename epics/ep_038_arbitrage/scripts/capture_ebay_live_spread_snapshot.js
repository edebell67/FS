const http = require('http');
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'data', 'ebay_live_snapshot.json');

const SEARCH_URL = 'https://www.ebay.co.uk/sch/i.html?_nkw=nintendo+switch+oled+console&_sacat=0&_from=R40&rt=nc&LH_Auction=1';
const ITEM_ID = '800223554019';
const SALE_GUIDE_TOTAL = 123.06;
const SOLD_GUIDE = 'Comparable eBay sold guide: Nintendo Switch OLED 64GB White Console Complete Set with Box - Excellent, sold 28 Jun 2026, £117.18 + £5.88 delivery = £123.06';

function get(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => resolve(d));
    }).on('error', reject);
  });
}

async function connectCDP() {
  const pages = JSON.parse(await get('http://127.0.0.1:9222/json/list'));
  const page = pages.find(p => p.type === 'page') || pages[0];
  if (!page) throw new Error('No Chrome page found on CDP port 9222. Launch headed Chrome first.');
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map();
  ws.onmessage = ev => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      pending.get(msg.id)(msg);
      pending.delete(msg.id);
    }
  };
  await new Promise((resolve, reject) => { ws.onopen = resolve; ws.onerror = reject; });
  const send = (method, params = {}) => new Promise(resolve => {
    const i = ++id;
    pending.set(i, resolve);
    ws.send(JSON.stringify({ id: i, method, params }));
  });
  await send('Runtime.enable');
  await send('Page.enable');
  return { send, close: () => ws.close() };
}

function parseMoney(s) {
  const m = String(s || '').match(/£\s*([0-9]+(?:\.[0-9]{1,2})?)/);
  return m ? Number(m[1]) : null;
}

function parseHours(timeText) {
  const s = String(timeText || '');
  let h = 0;
  const d = s.match(/(\d+)d/);
  const hm = s.match(/(\d+)h/);
  const mm = s.match(/(\d+)m/);
  if (d) h += Number(d[1]) * 24;
  if (hm) h += Number(hm[1]);
  if (mm) h += Number(mm[1]) / 60;
  return Math.round(h * 100) / 100;
}

async function main() {
  const { send, close } = await connectCDP();
  try {
    await send('Page.navigate', { url: SEARCH_URL });
    await new Promise(r => setTimeout(r, 7000));
    const expression = `(() => {
      const lines = document.body.innerText.split('\\n').map(x => x.trim()).filter(Boolean);
      const links = [...document.querySelectorAll('a')].map(a => ({
        text: a.innerText.trim().replace(/\\s+/g, ' '),
        href: a.href
      }));
      const link = links.find(x => x.href.includes('${ITEM_ID}'));
      if (!link) return { ok:false, error:'item link not found', title:document.title, url:location.href, sample:lines.slice(190,260) };
      const titleLine = link.text.replace(' Opens in a new window or tab','');
      const idx = lines.findIndex(l => titleLine.startsWith(l.replace('NEW LISTING','')) || l.includes('Dockable Console Red/Blue'));
      const block = lines.slice(Math.max(0, idx), Math.min(lines.length, idx + 12));
      return { ok:true, title:document.title, url:location.href, itemUrl:link.href, titleLine, idx, block };
    })()`;
    const r = await send('Runtime.evaluate', { expression, returnByValue: true });
    const value = r.result.result.value;
    if (!value.ok) throw new Error(JSON.stringify(value));
    const block = value.block;
    const priceLine = block.find(x => /^£/.test(x)) || '';
    const deliveryLine = block.find(x => /delivery/i.test(x)) || '';
    const bidsLine = block.find(x => /bid/i.test(x)) || '';
    const timeLabelIdx = block.findIndex(x => /^Time left$/i.test(x));
    const timeLine = timeLabelIdx >= 0 ? (block[timeLabelIdx + 1] || '') : (block.find(x => /\d+[dhm].*left/i.test(x)) || '');
    const sourceBid = parseMoney(priceLine);
    const delivery = parseMoney(deliveryLine) || 0;
    const sourceTotal = sourceBid == null ? null : Math.round((sourceBid + delivery) * 100) / 100;
    const grossSpread = sourceTotal == null ? null : Math.round((SALE_GUIDE_TOTAL - sourceTotal) * 100) / 100;
    const grossPct = sourceTotal == null ? null : Math.round((grossSpread / sourceTotal) * 1000) / 10;
    const snapshot = {
      captured_at: new Date().toISOString(),
      spread_id: 'SPRD-EBAY-001',
      item_id: ITEM_ID,
      item_name: 'Nintendo Switch OLED Model Dockable Console Red/Blue Joy-Con Dock USB-C Box',
      item_url: value.itemUrl,
      search_url: SEARCH_URL,
      source_bid_gbp: sourceBid,
      delivery_gbp: delivery,
      source_total_gbp: sourceTotal,
      sale_guide_total_gbp: SALE_GUIDE_TOTAL,
      gross_spread_gbp: grossSpread,
      gross_spread_pct: grossPct,
      bids_text: bidsLine,
      time_left_text: timeLine,
      hours_to_expiry: parseHours(timeLine),
      sale_guide_note: SOLD_GUIDE,
      extraction_block: block,
      guardrail: 'Gross spread only; current auction price can rise. No bid/buy/list/contact action performed.'
    };
    fs.writeFileSync(OUT, JSON.stringify(snapshot, null, 2));
    console.log(JSON.stringify(snapshot, null, 2));
  } finally {
    close();
  }
}

main().catch(e => { console.error(e); process.exit(1); });
