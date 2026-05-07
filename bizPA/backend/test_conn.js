const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

async function run() {
  console.log('Testing connection to:', process.env.DATABASE_URL.split('@')[1]);
  try {
    const res = await pool.query('SELECT NOW()');
    console.log('SUCCESS:', res.rows[0]);
  } catch (err) {
    console.error('FAILURE:', err.message);
  } finally {
    await pool.end();
  }
}

run();