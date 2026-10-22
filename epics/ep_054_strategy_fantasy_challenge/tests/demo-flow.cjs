const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 375, height: 812 } });
  await page.goto('http://127.0.0.1:8055/', { waitUntil: 'networkidle' });
  await page.locator('#savePortfolio').click();
  await page.locator('#enterGlobal').click();
  await page.locator('#advanceRound').click();
  await page.locator('#createChallenge').click();
  await page.locator('#inviteRecipient').fill('friend@example.test');
  await page.locator('#inviteFriend').click();
  await page.locator('#sendToAgent').click();
  await page.locator('#newAgent').click();
  const result = await page.evaluate(() => ({
    portfolioId: document.querySelector('#portfolioId').textContent,
    status: document.querySelector('#portfolioStatus').textContent,
    events: document.querySelector('#destinationEvents').innerText,
    handoff: document.querySelector('#agentHandoff').innerText,
    ownerVisible: !document.querySelector('#ownerLink').hidden,
    hasEntry: document.querySelector('#leaderboardRows').innerText.includes('YOUR LOCKED ENTRY SNAPSHOT'),
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
  }));
  for (const [key, value] of Object.entries(result)) console.log(`${key}=${String(value).replace(/\n/g, ' | ')}`);
  if (!/^PF_\d+$/.test(result.portfolioId) || !result.status.includes('SUBMITTED') || !result.events.includes('INVITE_CREATED') || !result.handoff.includes('ARENA_JOINED') || !result.ownerVisible || !result.hasEntry || result.overflow) process.exitCode = 1;
  await browser.close();
})();
