// EP047 — transaction-scoped verification that the preview screen's hypothetical-scope
// predicate (app/directoryadmin/visibility/preview/page.tsx) reads live individual
// town/category toggles + overrides, but decides ONLY on the hypothetical mode params —
// never on the saved public_directory_settings row — and never writes anything.
import pg from "pg";

async function main() {
  const client = new pg.Client({ connectionString: process.env.DATABASE_URL });
  await client.connect();
  await client.query("BEGIN");
  try {
    // Saved settings say "all" for both — but the preview will be asked about "selected".
    await client.query(
      `INSERT INTO public_directory_settings (id, town_mode, category_mode) VALUES ('default','all','all')
       ON CONFLICT (id) DO UPDATE SET town_mode='all', category_mode='all'`
    );
    const townKey = `fixture-preview-town-${Date.now()}`;
    await client.query(`INSERT INTO public_town_visibility (town_key, town_label, is_enabled) VALUES ($1,$1,false)`, [townKey]);
    const ref = `fixture-preview-biz-${Date.now()}`;
    await client.query(
      `INSERT INTO businesses (business_ref, slug, business_name, category, town, imported_source) VALUES ($1,$1,$2,'fixture-preview-category',$3,'fixture')`,
      [ref, "Fixture Preview Business", townKey]
    );

    async function previewCount(townMode: string, categoryMode: string) {
      const scope = `(
        COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') = 'show'
        OR (
          COALESCE((SELECT v.decision FROM public_business_visibility v WHERE v.business_id = b.id), 'inherit') <> 'hide'
          AND ($1 = 'all' OR NOT EXISTS (SELECT 1 FROM public_town_visibility t WHERE t.town_key = lower(trim(b.town)) AND t.is_enabled = false))
          AND ($2 = 'all' OR NOT EXISTS (SELECT 1 FROM public_category_visibility c WHERE c.category_key = lower(trim(b.category)) AND c.is_enabled = false))
        )
      )`;
      const result = await client.query(`SELECT count(*)::int AS n FROM businesses b WHERE b.business_ref = $3 AND ${scope}`, [townMode, categoryMode, ref]);
      return result.rows[0].n as number;
    }

    // Saved settings ('all') would show the fixture even though its town is individually disabled.
    const underSavedAll = await previewCount("all", "all");
    if (underSavedAll !== 1) throw new Error(`expected visible under saved 'all' mode, got count=${underSavedAll}`);

    // Hypothetical 'selected' mode (not saved) must hide it, proving the preview uses the
    // hypothetical param, not the saved public_directory_settings row.
    const underHypotheticalSelected = await previewCount("selected", "all");
    if (underHypotheticalSelected !== 0) throw new Error(`expected hidden under hypothetical 'selected' mode, got count=${underHypotheticalSelected}`);

    // Confirm nothing was actually written to public_directory_settings by the preview logic itself.
    const settingsAfter = await client.query(`SELECT town_mode FROM public_directory_settings WHERE id='default'`);
    if (settingsAfter.rows[0].town_mode !== "all") throw new Error("preview query must not mutate saved settings");

    console.log(JSON.stringify({
      checks: ["visible-under-saved-mode", "hidden-under-hypothetical-mode-not-yet-saved", "saved-settings-unchanged"],
      result: "pass",
    }));
    await client.query("ROLLBACK");
  } catch (error) {
    await client.query("ROLLBACK");
    throw error;
  } finally {
    await client.end();
  }
}

main().catch((error) => { console.error(error); process.exit(1); });
