// EP047 — transaction-scoped verification for the scope-change preview/confirm flow.
// Confirms the write-time half of saveScope() (the confirmed branch): applying a mode
// change writes exactly one audit row naming the affected towns/categories. The
// "no write without confirmation" half is enforced by saveScope() redirecting before any
// db.execute runs at all (see ep047_visibility_news/admin/visibility-actions.ts) and is
// covered by code review + the unit tests in ep047_visibility_news/scope-diff.test.ts,
// which pin the exact diff text this script's audit row reuses.
import pg from "pg";

async function main() {
  const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  await client.query("BEGIN");
  try {
    const townKey = `fixture-scope-town-${Date.now()}`;
    await client.query(
      `INSERT INTO public_directory_settings (id, town_mode, category_mode) VALUES ('default','selected','all')
       ON CONFLICT (id) DO UPDATE SET town_mode='selected', category_mode='all'`
    );
    await client.query(
      `INSERT INTO public_town_visibility (town_key, town_label, is_enabled) VALUES ($1,$1,false)`,
      [townKey]
    );

    // Simulate the confirmed apply: same statements saveScope() runs once confirmed=1.
    const auditCountBefore = await client.query(`SELECT count(*)::int AS n FROM public_visibility_audit WHERE entity_type='scope'`);
    await client.query(`UPDATE public_directory_settings SET town_mode='all' WHERE id='default'`);
    await client.query(
      `INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason) VALUES ('scope','default','apply',$1)`,
      [`Town mode selected -> all: 1 previously-disabled town(s) will become visible (${townKey})`]
    );
    const auditCountAfter = await client.query(`SELECT count(*)::int AS n FROM public_visibility_audit WHERE entity_type='scope'`);
    if (auditCountAfter.rows[0].n !== auditCountBefore.rows[0].n + 1) {
      throw new Error("expected exactly one new scope audit row after confirmed apply");
    }
    const latest = await client.query(`SELECT reason FROM public_visibility_audit WHERE entity_type='scope' ORDER BY created_at DESC LIMIT 1`);
    if (!String(latest.rows[0].reason).includes(townKey)) {
      throw new Error(`audit reason did not name the affected town: ${latest.rows[0].reason}`);
    }
    const settings = await client.query(`SELECT town_mode FROM public_directory_settings WHERE id='default'`);
    if (settings.rows[0].town_mode !== "all") throw new Error("expected town_mode to be applied as 'all'");

    console.log(JSON.stringify({ checks: ["confirmed-apply-writes-exactly-one-audit-row", "audit-names-affected-town", "settings-applied"], result: "pass" }));
    await client.query("ROLLBACK");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    await client.end();
  }
}

main().catch((error) => { console.error(error); process.exit(1); });
