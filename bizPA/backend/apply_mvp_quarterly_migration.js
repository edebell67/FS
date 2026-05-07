const fs = require('fs');
const path = require('path');
const db = require('./src/config/db');

async function run() {
  const sqlPath = path.join(__dirname, 'src', 'models', 'mvp_quarterly_export_migration.sql');
  const sql = fs.readFileSync(sqlPath, 'utf8');
  console.log(`[MIGRATION] Applying ${sqlPath}`);
  await db.query(sql);
  console.log('[MIGRATION] MVP quarterly export migration applied successfully.');
}

run()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('[MIGRATION] Failed:', err.message);
    process.exit(1);
  });
