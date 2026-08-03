// EP047 — transaction-scoped verification for the business-level visibility override resolver.
// Uses a single raw pg.Client (not the drizzle pool) so setup/assert/rollback share one
// connection/transaction — matches the pattern in verify-public-news-fixtures.ts. The
// predicate below is a literal copy of publicScopeWhere() in ep047_visibility_news/lib/public-scope.ts;
// keep the two in sync if that resolver changes.
import pg from "pg";

async function main() {
  const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  await client.query("BEGIN");
  try {
    // Force a known scope: selected-only town/category mode, with the fixture town/category disabled.
    await client.query(
      `INSERT INTO public_directory_settings (id, town_mode, category_mode) VALUES ('default','selected','selected')
       ON CONFLICT (id) DO UPDATE SET town_mode='selected', category_mode='selected'`
    );
    const townKey = "fixture-hidden-town";
    const categoryKey = "fixture-hidden-category";
    await client.query(
      `INSERT INTO public_town_visibility (town_key, town_label, is_enabled) VALUES ($1,$1,false)
       ON CONFLICT (town_key) DO UPDATE SET is_enabled=false`,
      [townKey]
    );
    await client.query(
      `INSERT INTO public_category_visibility (category_key, category_label, is_enabled) VALUES ($1,$1,false)
       ON CONFLICT (category_key) DO UPDATE SET is_enabled=false`,
      [categoryKey]
    );

    async function fixtureBusiness(suffix: string) {
      const ref = `fixture-override-${suffix}-${Date.now()}`;
      const inserted = await client.query(
        `INSERT INTO businesses (business_ref, slug, business_name, category, town, imported_source)
         VALUES ($1,$1,$2,$3,$4,'fixture') RETURNING id`,
        [ref, `Fixture Override Business ${suffix}`, categoryKey, townKey]
      );
      return inserted.rows[0].id as string;
    }

    const isPublic = async (businessId: string) => {
      const result = await client.query(
        `SELECT (
          COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') = 'show'
          OR (
            COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') <> 'hide'
            AND EXISTS (SELECT 1 FROM public_directory_settings s WHERE s.id = 'default'
              AND (s.town_mode = 'all' OR NOT EXISTS (SELECT 1 FROM public_town_visibility t
                WHERE t.town_key = lower(trim(b.town)) AND t.is_enabled = false)))
            AND EXISTS (SELECT 1 FROM public_directory_settings s WHERE s.id = 'default'
              AND (s.category_mode = 'all' OR NOT EXISTS (SELECT 1 FROM public_category_visibility c
                WHERE c.category_key = lower(trim(b.category)) AND c.is_enabled = false)))
          )
        ) AS is_public FROM businesses b WHERE b.id = $1`,
        [businessId]
      );
      return result.rows[0].is_public as boolean;
    };

    // Case 1: inherit (no override row) in a hidden town/category -> must be excluded.
    const inheritId = await fixtureBusiness("inherit");
    if (await isPublic(inheritId)) throw new Error("inherit case: expected excluded, was public");

    // Case 2: explicit 'show' override in a hidden town/category -> must be included (this is the bug being fixed).
    const showId = await fixtureBusiness("show");
    await client.query(
      `INSERT INTO public_business_visibility (business_id, decision, reason) VALUES ($1,'show','Fixture: force-show despite hidden scope')`,
      [showId]
    );
    if (!(await isPublic(showId))) throw new Error("show override: expected included, was excluded");

    // Case 3: explicit 'hide' override, even if town/category mode were 'all' -> must be excluded.
    await client.query(`UPDATE public_directory_settings SET town_mode='all', category_mode='all' WHERE id='default'`);
    const hideId = await fixtureBusiness("hide");
    await client.query(
      `INSERT INTO public_business_visibility (business_id, decision, reason) VALUES ($1,'hide','Fixture: force-hide despite all-mode scope')`,
      [hideId]
    );
    if (await isPublic(hideId)) throw new Error("hide override: expected excluded even under all-mode, was public");

    // Case 4: the admin upsert-with-audit statement (mirrors saveBusinessOverride) round-trips
    // through an initial set and a later change, and records one audit row per change.
    const auditId = await fixtureBusiness("audit-roundtrip");
    async function setOverride(decision: string, reason: string) {
      await client.query(
        `INSERT INTO public_business_visibility (business_id, decision, reason) VALUES ($1,$2,$3)
         ON CONFLICT (business_id) DO UPDATE SET decision=$2, reason=$3, updated_at=now()`,
        [auditId, decision, reason]
      );
      await client.query(
        `INSERT INTO public_visibility_audit (entity_type, entity_key, action, reason) VALUES ('business',$1,$2,$3)`,
        [auditId, "override_" + decision, reason]
      );
    }
    await setOverride("hide", "Fixture: initial hide");
    await setOverride("inherit", "Fixture: reverted to inherit");
    const finalDecision = await client.query(`SELECT decision, reason FROM public_business_visibility WHERE business_id=$1`, [auditId]);
    if (finalDecision.rows[0]?.decision !== "inherit") throw new Error("upsert roundtrip: expected final decision inherit");
    const auditRows = await client.query(`SELECT action FROM public_visibility_audit WHERE entity_key=$1 ORDER BY created_at`, [auditId]);
    if (auditRows.rows.length !== 2 || auditRows.rows[0].action !== "override_hide" || auditRows.rows[1].action !== "override_inherit") {
      throw new Error(`upsert roundtrip: expected 2 audit rows (override_hide, override_inherit), got ${JSON.stringify(auditRows.rows)}`);
    }

    console.log(JSON.stringify({ checks: ["inherit-excluded-in-selected-mode", "show-overrides-hidden-scope", "hide-overrides-all-mode", "upsert-and-audit-roundtrip"], result: "pass" }));
    await client.query("ROLLBACK");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    await client.end();
  }
}

main().catch((error) => { console.error(error); process.exit(1); });
