const express = require('express');
const { Pool } = require('pg');
require('dotenv').config();

const app = express();
const port = 5099;

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

app.get('/api/health', async (req, res) => {
  let dbStatus = 'unknown';
  try {
    const result = await pool.query('SELECT NOW()');
    dbStatus = 'connected';
  } catch (err) {
    dbStatus = 'error: ' + err.message;
  }

  res.json({
    status: 'UP',
    port: port,
    database: dbStatus,
    supabase_url: process.env.SUPABASE_URL ? 'set' : 'missing',
    env_loaded: process.env.DATABASE_URL ? 'yes' : 'no'
  });
});

app.listen(port, '0.0.0.0', () => {
  console.log(`Debug server running on port ${port}`);
});