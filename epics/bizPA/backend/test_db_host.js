const { Client } = require('pg');
require('dotenv').config();

const client = new Client({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

async function test() {
  try {
    console.log('Connecting to:', process.env.DATABASE_URL.split('@')[1]);
    await client.connect();
    console.log('Connected!');
    const res = await client.query('SELECT NOW()');
    console.log('Success:', res.rows[0]);
    await client.end();
  } catch (err) {
    console.error('Connection failed:', err.stack);
    process.exit(1);
  }
}

test();