const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.resolve(__dirname, '..');
const source = (name) => fs.readFileSync(path.join(root, name), 'utf8');

test('Fantasy Challenge exposes the complete human-first portfolio loop', () => {
  const html = source('index.html');
  for (const token of ['Build your fantasy portfolio', 'Save Portfolio', 'Enter Global', 'Challenge friends', 'Send to Agent', 'MY PORTFOLIOS', 'leaderboard']) {
    assert.match(html, new RegExp(token));
  }
  assert.match(html, /id="portfolioName"/);
  assert.match(html, /id="portfolioStrategies"/);
  assert.match(html, /id="savePortfolio"/);
});

test('Fantasy Challenge models reuse instead of copying portfolios', () => {
  const js = source('fantasy.js');
  for (const token of ['compositionFingerprint', 'duplicate', 'portfolio_id', 'strategy_portfolio', 'portfolio_version']) {
    assert.match(js, new RegExp(token));
  }
  assert.match(js, /GLOBAL_COMPETITION_JOINED/);
  assert.match(js, /private challenge/i);
});

test('Fantasy Challenge demonstrates Finder, agent import, invitation, Arena and Owner handoffs', () => {
  const html = source('index.html');
  const js = source('fantasy.js');
  assert.match(html, /id="openFinder"/);
  assert.match(html, /id="importAgent"/);
  assert.match(html, /id="inviteFriend"/);
  assert.match(html, /id="sendToAgent"/);
  assert.match(js, /https:\/\/www\.thetechprinciple\.com\/epic\/ep053\//);
  assert.doesNotMatch(js, /ep053-strategy-finder-ai\.onrender\.com/);
  assert.match(html, /https:\/\/www\.thetechprinciple\.com\/epic\/ep052\/owner\//);
  assert.doesNotMatch(html, /ep052-agentic-arena\.onrender\.com/);
  for (const token of ['INVITE_CREATED', 'AGENT_SKILL_ATTACHED', 'ARENA_JOINED', 'LEADERBOARD_UPDATED']) {
    assert.match(js, new RegExp(token));
  }
});

test('Fantasy Challenge visibly labels local data and simulated side effects', () => {
  const html = source('index.html');
  assert.match(html, /Preview-only demo/i);
  assert.match(html, /No live persistence, invitation delivery, scoring, account lookup, skill assignment, Arena join or trading is connected/i);
});

test('Fantasy Challenge includes the actual TTP icon and exact product footer', () => {
  const html = source('index.html');
  assert.match(html, /assets\/thetechprinciple-icon-180\.png/);
  assert.match(html, /thetechprinciple\.com product/);
  assert.ok(fs.existsSync(path.join(root, 'assets', 'thetechprinciple-icon-180.png')));
});

test('Fantasy Challenge is Uvicorn-served and mobile-first', () => {
  const html = source('index.html');
  const css = source('fantasy.css');
  const server = source('server.py');
  assert.match(html, /viewport-fit=cover/);
  assert.match(html, /mobile-nav/);
  assert.match(css, /@media\(min-width:768px\)/);
  assert.match(css, /min-height:44px/);
  assert.match(server, /FastAPI/);
  assert.match(server, /@app\.get\(['"]\/health/);
});
