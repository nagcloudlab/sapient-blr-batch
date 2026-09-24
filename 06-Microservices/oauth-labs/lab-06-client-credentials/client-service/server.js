const express = require('express');
const app = express();

const KEYCLOAK_TOKEN_URL = 'http://localhost:8180/realms/foodexpress/protocol/openid-connect/token';
const CLIENT_ID = 'foodexpress-api';
const CLIENT_SECRET = 'api-secret-456';
const RESOURCE_SERVER = 'http://localhost:8080';

let cachedToken = null;
let tokenExpiry = 0;

// Get token using Client Credentials — no user involved!
async function getServiceToken() {
  if (cachedToken && Date.now() < tokenExpiry) {
    console.log('  Using CACHED token (expires in', Math.round((tokenExpiry - Date.now()) / 1000), 'seconds)');
    return cachedToken;
  }

  console.log('\n' + '='.repeat(60));
  console.log('CLIENT CREDENTIALS: Requesting new token from Keycloak');
  console.log('='.repeat(60));
  console.log('POST', KEYCLOAK_TOKEN_URL);
  console.log('  grant_type:    client_credentials');
  console.log('  client_id:     ', CLIENT_ID);
  console.log('  client_secret: ', CLIENT_SECRET.substring(0, 8) + '...');
  console.log('  NO username, NO password — this is MACHINE-to-MACHINE');

  const res = await fetch(KEYCLOAK_TOKEN_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }).toString(),
  });

  const data = await res.json();

  if (data.error) {
    console.error('Token error:', data.error, data.error_description);
    throw new Error(data.error_description || data.error);
  }

  console.log('\nToken received:');
  console.log('  access_token:    ', data.access_token?.substring(0, 50) + '...');
  console.log('  token_type:      ', data.token_type);
  console.log('  expires_in:      ', data.expires_in, 'seconds');
  console.log('  has refresh_token?', !!data.refresh_token, '(should be NO)');
  console.log('  has id_token?    ', !!data.id_token, '(should be NO)');

  cachedToken = data.access_token;
  tokenExpiry = Date.now() + (data.expires_in - 10) * 1000;

  return cachedToken;
}

// Decode JWT payload (for display)
function decodeJwt(token) {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(Buffer.from(payload, 'base64').toString());
  } catch { return null; }
}

// ─── ENDPOINTS ───

app.get('/', (req, res) => {
  res.send(`
    <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto;">
    <h1>FoodExpress Internal Service</h1>
    <p>This service authenticates as a <b>MACHINE</b>, not a user.<br>
    Grant type: <code>client_credentials</code></p>
    <h3>Service-to-Service Calls</h3>
    <a href="/fetch-orders">Fetch Orders from Resource Server</a><br>
    <a href="/fetch-menu">Fetch Menu (public, no token)</a><br>
    <a href="/show-token">Show Machine Token (decoded)</a>
    </body></html>
  `);
});

app.get('/fetch-orders', async (req, res) => {
  try {
    const token = await getServiceToken();

    console.log('\n' + '='.repeat(60));
    console.log('CALLING RESOURCE SERVER (service-to-service)');
    console.log('='.repeat(60));
    console.log('GET', RESOURCE_SERVER + '/orders');
    console.log('Authorization: Bearer', token.substring(0, 40) + '...');

    const apiRes = await fetch(`${RESOURCE_SERVER}/orders`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    const data = await apiRes.json();
    console.log('Response:', apiRes.status);

    res.send(`
      <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto;">
      <h2>Service-to-Service Call Result</h2>
      <p>Status: ${apiRes.status}</p>
      <pre style="background:#f5f5f5; padding:15px;">${JSON.stringify(data, null, 2)}</pre>
      <a href="/">Back</a>
      </body></html>
    `);
  } catch (err) {
    res.status(500).send(`<h1>Error</h1><pre>${err.message}</pre><a href="/">Back</a>`);
  }
});

app.get('/fetch-menu', async (req, res) => {
  console.log('\nCalling PUBLIC endpoint (no token needed)');
  const apiRes = await fetch(`${RESOURCE_SERVER}/public/menu`);
  const data = await apiRes.json();
  res.send(`
    <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto;">
    <h2>Public Endpoint (no auth)</h2>
    <pre style="background:#f5f5f5; padding:15px;">${JSON.stringify(data, null, 2)}</pre>
    <a href="/">Back</a>
    </body></html>
  `);
});

app.get('/show-token', async (req, res) => {
  const token = await getServiceToken();
  const decoded = decodeJwt(token);
  res.send(`
    <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto;">
    <h2>Machine Token (decoded)</h2>
    <p>Notice: <b>NO preferred_username</b>, <b>NO email</b> — this is a machine identity.</p>
    <pre style="background:#f5f5f5; padding:15px;">${JSON.stringify(decoded, null, 2)}</pre>
    <a href="/">Back</a>
    </body></html>
  `);
});

app.listen(3001, () => {
  console.log('\n' + '='.repeat(60));
  console.log('CLIENT CREDENTIALS FLOW - Lab 06');
  console.log('='.repeat(60));
  console.log('CLIENT SERVICE (this app): http://localhost:3001');
  console.log('AUTHORIZATION SERVER:      http://localhost:8180');
  console.log('RESOURCE SERVER:           http://localhost:8080');
  console.log('');
  console.log('This service authenticates as a MACHINE, not a user.');
  console.log('Open http://localhost:3001');
  console.log('='.repeat(60) + '\n');
});
