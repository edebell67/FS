import { chromium } from 'playwright';

const SCREENSHOTS_DIR = './demo_screenshots';
const BASE_URL = 'http://localhost:3002';

async function demo() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
  const page = await context.newPage();

  console.log('1. Opening landing page...');
  await page.goto(BASE_URL);
  await page.waitForTimeout(2000);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/01_landing_dashboard.png`, fullPage: true });
  console.log('   Saved: 01_landing_dashboard.png');

  console.log('2. Scrolling to strategies table...');
  await page.evaluate(() => document.querySelector('#strategies')?.scrollIntoView());
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/02_strategies_table.png` });
  console.log('   Saved: 02_strategies_table.png');

  console.log('3. Using search filter...');
  await page.fill('input[placeholder="Search strategies..."]', 'breakout_2');
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/03_filtered_search.png` });
  console.log('   Saved: 03_filtered_search.png');

  console.log('4. Clearing filter and clicking a strategy row...');
  await page.fill('input[placeholder="Search strategies..."]', '');
  await page.waitForTimeout(300);
  const firstRow = page.locator('tbody tr').first();
  await firstRow.click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/04_strategy_detail_gated.png`, fullPage: true });
  console.log('   Saved: 04_strategy_detail_gated.png');

  console.log('5. Closing detail and clicking Get Started...');
  await page.click('button:has-text("Get Started")');
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/05_signup_modal.png` });
  console.log('   Saved: 05_signup_modal.png');

  console.log('6. Filling signup form...');
  await page.fill('input#name', 'Marcus Chen');
  await page.fill('input#email', 'marcus@example.com');
  await page.fill('input#password', 'password123');
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/06_signup_filled.png` });
  console.log('   Saved: 06_signup_filled.png');

  console.log('7. Submitting signup...');
  await page.click('button[type="submit"]');
  await page.waitForTimeout(1500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/07_authenticated_dashboard.png`, fullPage: true });
  console.log('   Saved: 07_authenticated_dashboard.png');

  console.log('8. Clicking strategy to see unlocked chart...');
  await page.evaluate(() => document.querySelector('#strategies')?.scrollIntoView());
  await page.waitForTimeout(300);
  const strategyRow = page.locator('tbody tr').first();
  await strategyRow.click();
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/08_strategy_detail_unlocked.png`, fullPage: true });
  console.log('   Saved: 08_strategy_detail_unlocked.png');

  console.log('9. Mobile view...');
  await page.setViewportSize({ width: 375, height: 812 });
  await page.goto(BASE_URL);
  await page.waitForTimeout(1000);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/09_mobile_landing.png`, fullPage: true });
  console.log('   Saved: 09_mobile_landing.png');

  console.log('10. Mobile menu...');
  await page.click('button[aria-label="Toggle menu"]');
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${SCREENSHOTS_DIR}/10_mobile_menu.png` });
  console.log('   Saved: 10_mobile_menu.png');

  await browser.close();
  console.log('\nDemo complete! Screenshots saved to demo_screenshots/');
}

demo().catch(console.error);
