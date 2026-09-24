const express = require('express');
const session = require('express-session');
const { Issuer, generators } = require('openid-client');

const app = express();
app.use(session({ secret: 'oauth-lab', resave: false, saveUninitialized: false }));

// ─── Configuration ───
// Option 1: Keycloak (local)
const ISSUER_URL = 'http://localhost:8180/realms/foodexpress';
const CLIENT_ID = 'foodexpress-web';
const CLIENT_SECRET = 'web-secret-123';

// Option 2: Google (cloud) — uncomment to switch
// const ISSUER_URL = 'https://accounts.google.com';
// const CLIENT_ID = 'your-google-client-id.apps.googleusercontent.com';
// const CLIENT_SECRET = 'your-google-client-secret';

const REDIRECT_URI = 'http://localhost:3000/callback';
const RESOURCE_SERVER = 'http://localhost:8080';

let client;

async function init() {
  const issuer = await Issuer.discover(ISSUER_URL);
  console.log('Discovered issuer:', issuer.metadata.issuer);

  client = new issuer.Client({
    client_id: CLIENT_ID,
    client_secret: CLIENT_SECRET,
    redirect_uris: [REDIRECT_URI],
    response_types: ['code'],
  });
}

// ─── HOME PAGE ───
app.get('/', (req, res) => {
  const user = req.session.user;
  res.send(`
    <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto; padding:0 20px;">
    <h1>FoodExpress (Client App - Node.js)</h1>
    ${user ? `
      <div style="background:#e8f5e9; padding:20px; border-radius:8px;">
        <h2>Welcome, ${user.name}!</h2>
        <p><b>Email:</b> ${user.email}</p>
        <p><b>Roles:</b> ${JSON.stringify(user.roles)}</p>
      </div>

      <h3>Call Resource Server (Spring Boot :8080)</h3>
      <p>These calls send the access token as <code>Authorization: Bearer &lt;token&gt;</code></p>
      <a href="/api/profile">GET /profile</a> |
      <a href="/api/orders">GET /orders</a> |
      <a href="/api/admin/users">GET /admin/users</a> |
      <a href="/api/restaurant/dashboard">GET /restaurant/dashboard</a> |
      <a href="/api/debug/token">GET /debug/token</a> |
      <a href="/api/public/menu">GET /public/menu (no auth)</a>

      <hr>
      <details><summary><b>Access Token</b> (click to expand)</summary>
        <pre style="word-break:break-all;font-size:11px;background:#f5f5f5;padding:10px">${req.session.accessToken}</pre>
      </details>
      <details><summary><b>ID Token Claims</b></summary>
        <pre style="background:#f5f5f5;padding:10px">${JSON.stringify(req.session.claims, null, 2)}</pre>
      </details>
      <details><summary><b>Refresh Token</b></summary>
        <pre style="word-break:break-all;font-size:11px;background:#f5f5f5;padding:10px">${req.session.refreshToken}</pre>
      </details>
      <hr>
      <a href="/logout" style="color:red">Logout</a>
    ` : `
      <p>You are not logged in.</p>
      <a href="/login" style="display:inline-block;padding:12px 24px;background:#1976d2;color:white;text-decoration:none;border-radius:4px;font-size:16px">
        Login with Keycloak
      </a>
    `}
    </body></html>
  `);
});

// ─── STEP 1: Redirect to Keycloak ───
app.get('/login', (req, res) => {
  const state = generators.state();
  const nonce = generators.nonce();
  req.session.state = state;
  req.session.nonce = nonce;

  const url = client.authorizationUrl({
    scope: 'openid profile email',
    state,
    nonce,
  });

  console.log('\n' + '='.repeat(60));
  console.log('STEP 1: REDIRECT TO AUTHORIZATION SERVER');
  console.log('='.repeat(60));
  console.log('Auth URL:', url);
  console.log('Parameters:');
  console.log('  response_type: code');
  console.log('  client_id:     ', CLIENT_ID);
  console.log('  redirect_uri:  ', REDIRECT_URI);
  console.log('  scope:          openid profile email');
  console.log('  state:         ', state.substring(0, 20) + '...');

  res.redirect(url);
});

// ─── STEP 2: Handle callback from Keycloak ───
app.get('/callback', async (req, res) => {
  console.log('\n' + '='.repeat(60));
  console.log('STEP 2: CALLBACK FROM AUTHORIZATION SERVER');
  console.log('='.repeat(60));
  console.log('Authorization Code:', req.query.code?.substring(0, 40) + '...');
  console.log('State received:    ', req.query.state?.substring(0, 20) + '...');
  console.log('State matches?     ', req.query.state === req.session.state);

  try {
    const params = client.callbackParams(req);
    const tokenSet = await client.callback(REDIRECT_URI, params, {
      state: req.session.state,
      nonce: req.session.nonce,
    });

    console.log('\n' + '='.repeat(60));
    console.log('STEP 3: TOKEN EXCHANGE (code --> tokens)');
    console.log('='.repeat(60));
    console.log('This happens SERVER-TO-SERVER. Browser never sees client_secret.');
    console.log('Access Token:  ', tokenSet.access_token?.substring(0, 50) + '...');
    console.log('Token Type:    ', tokenSet.token_type);
    console.log('Expires In:    ', tokenSet.expires_in, 'seconds');
    console.log('Refresh Token? ', !!tokenSet.refresh_token);
    console.log('ID Token?      ', !!tokenSet.id_token);
    console.log('Scope:         ', tokenSet.scope);

    // Get user info from Keycloak
    const userinfo = await client.userinfo(tokenSet.access_token);

    console.log('\n' + '='.repeat(60));
    console.log('STEP 4: USERINFO RESPONSE');
    console.log('='.repeat(60));
    console.log(JSON.stringify(userinfo, null, 2));

    // Store in session
    req.session.user = {
      name: userinfo.name || userinfo.preferred_username,
      email: userinfo.email,
      roles: tokenSet.claims()?.realm_access?.roles || [],
    };
    req.session.accessToken = tokenSet.access_token;
    req.session.refreshToken = tokenSet.refresh_token;
    req.session.idToken = tokenSet.id_token;
    req.session.claims = tokenSet.claims();

    res.redirect('/');
  } catch (err) {
    console.error('Callback error:', err.message);
    res.status(500).send(`<h1>Error</h1><pre>${err.message}</pre><a href="/">Home</a>`);
  }
});

// ─── STEP 5: Call Resource Server with Bearer token ───
app.get('/api/*', async (req, res) => {
  if (!req.session.accessToken) return res.redirect('/login');

  const endpoint = req.params[0];
  const url = `${RESOURCE_SERVER}/${endpoint}`;
  const useAuth = !endpoint.startsWith('public/');

  console.log('\n' + '='.repeat(60));
  console.log('STEP 5: CALLING RESOURCE SERVER');
  console.log('='.repeat(60));
  console.log('URL:          ', url);
  if (useAuth) {
    console.log('Authorization: Bearer', req.session.accessToken.substring(0, 40) + '...');
  } else {
    console.log('No auth header (public endpoint)');
  }

  try {
    const headers = useAuth ? { 'Authorization': `Bearer ${req.session.accessToken}` } : {};
    const response = await fetch(url, { headers });
    const body = await response.text();

    console.log('Status:       ', response.status);

    let formatted;
    try { formatted = JSON.stringify(JSON.parse(body), null, 2); } catch { formatted = body; }

    res.send(`
      <html><body style="font-family:sans-serif; max-width:800px; margin:40px auto;">
      <h2>Resource Server Response</h2>
      <p><b>URL:</b> <code>${url}</code></p>
      <p><b>Status:</b> ${response.status} ${response.status === 200 ? '(OK)' : response.status === 403 ? '(FORBIDDEN - wrong role)' : response.status === 401 ? '(UNAUTHORIZED - no/invalid token)' : ''}</p>
      <pre style="background:#f5f5f5; padding:15px; border-radius:4px;">${formatted}</pre>
      <a href="/">Back to Home</a>
      </body></html>
    `);
  } catch (err) {
    res.send(`<h1>Error</h1><pre>${err.message}</pre><a href="/">Home</a>`);
  }
});

// ─── LOGOUT ───
app.get('/logout', (req, res) => {
  const idToken = req.session.idToken;
  req.session.destroy(() => {
    const url = `${KEYCLOAK_URL}/protocol/openid-connect/logout?id_token_hint=${idToken}&post_logout_redirect_uri=http://localhost:3000`;
    console.log('\n' + '='.repeat(60));
    console.log('LOGOUT: Redirecting to Keycloak');
    console.log('='.repeat(60));
    res.redirect(url);
  });
});

// ─── START ───
init().then(() => {
  app.listen(3000, () => {
    console.log('\n' + '='.repeat(60));
    console.log('AUTHORIZATION CODE FLOW - Lab 05');
    console.log('='.repeat(60));
    console.log('CLIENT (this app):        http://localhost:3000');
    console.log('AUTHORIZATION SERVER:     http://localhost:8180');
    console.log('RESOURCE SERVER:          http://localhost:8080');
    console.log('');
    console.log('Open http://localhost:3000 and click "Login with Keycloak"');
    console.log('Watch this terminal for the OAuth flow steps.');
    console.log('='.repeat(60) + '\n');
  });
}).catch(err => {
  console.error('Failed to initialize:', err.message);
  console.error('Is Keycloak running on http://localhost:8180?');
});
