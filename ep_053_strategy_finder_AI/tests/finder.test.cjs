const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');

function source(name) {
  return fs.readFileSync(path.join(root, name), 'utf8');
}

test('Finder exposes the complete Find → Select → Give → Join → Watch loop', () => {
  const html = source('index.html');
  const js = source('finder.js');

  assert.match(html, /Strategy Finder AI/);
  assert.match(html, /id="strategyQuery"/);
  assert.match(html, /Give to Agent/);
  assert.match(html, /Use Existing Agent/);
  assert.match(html, /Create New Agent/);
  assert.match(html, /Watch Agent/);
  assert.match(html, /https:\/\/www\.thetechprinciple\.com\/epic\/ep052\/owner\//);
  assert.doesNotMatch(html, /ep052-agentic-arena\.onrender\.com/);
  assert.match(js, /FINDER_IDLE/);
  assert.match(js, /ASSIGN_SKILL/);
  assert.match(js, /JOIN_ARENA/);
});

test('Finder preserves the selected strategy while resolving an agent destination', () => {
  const js = source('finder.js');
  assert.match(js, /selectedStrategy/);
  assert.match(js, /strategy_id/);
  assert.match(js, /skill_type:\s*['"]strategy_directory_strategy['"]/);
});

test('Finder uses the actual local The Tech Principle icon in its brand header', () => {
  const html = source('index.html');
  assert.match(html, /src="assets\/thetechprinciple-icon-180\.png"/);
  assert.ok(fs.existsSync(path.join(root, 'assets', 'thetechprinciple-icon-180.png')));
});

test('Finder serves through a minimal Uvicorn-compatible application', () => {
  const server = source('server.py');
  assert.match(server, /FastAPI/);
  assert.match(server, /@app\.get\("\/health"/);
  assert.match(server, /FileResponse/);
});

test('Finder is explicitly mobile-first and has no horizontal UI shell', () => {
  const css = source('finder.css');
  const html = source('index.html');
  assert.match(html, /viewport-fit=cover/);
  assert.match(css, /min-height:\s*44px/);
  assert.match(css, /grid-template-columns:\s*1fr/);
  assert.match(css, /@media\s*\(min-width:\s*768px\)/);
  assert.match(css, /overflow-x:\s*hidden/);
});

test('Finder offers a complete no-results recovery path without losing the requirement', () => {
  const html = source('index.html');
  const js = source('finder.js');
  assert.match(html, /id="noResults"/);
  assert.match(html, /Show Closest Matches/);
  assert.match(html, /Change Requirements/);
  assert.match(js, /FINDER_NO_RESULTS/);
  assert.match(js, /showClosestMatches/);
});

test('Finder labels all mock assignment and Arena participation outcomes as preview-only', () => {
  const html = source('index.html');
  const js = source('finder.js');
  assert.match(html, /Preview only: no real agent/);
  assert.match(js, /Preview status/);
  assert.match(js, /no real agent/);
});
