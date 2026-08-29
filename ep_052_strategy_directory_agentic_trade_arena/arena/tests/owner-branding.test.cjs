const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'owner.html'), 'utf8');
const css = fs.readFileSync(path.join(root, 'owner.css'), 'utf8');

const arenaHtml = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const arenaCss = fs.readFileSync(path.join(root, 'styles.css'), 'utf8');

test('Arena floor and Owner View use the real local TTP icon in their product shells', () => {
  for (const page of [html, arenaHtml]) {
    assert.match(page, /assets\/thetechprinciple-icon-180\.png/);
    assert.match(page, /https:\/\/thetechprinciple\.com\//);
  }
  assert.match(html, /class="brand-logo"[^>]+width="30"[^>]+height="30"/);
  assert.match(arenaHtml, /class="brand-logo"[^>]+width="30"[^>]+height="30"/);
  assert.ok(fs.existsSync(path.join(root, 'assets', 'thetechprinciple-icon-180.png')));
  assert.match(css, /\.brand-logo/);
  assert.match(css, /\.ttp-product-footer/);
  assert.match(arenaCss, /\.brand-logo/);
  assert.match(arenaCss, /\.ttp-product-footer/);
});
