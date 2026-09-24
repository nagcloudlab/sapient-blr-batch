# Lab 05: Authorization Code Flow — Build It

## The Problem

```
In Lab 02, you called /token with curl using grant_type=password.
That's fine for testing, but in production:
  - User's password should NEVER touch your app
  - User should type credentials ONLY in Keycloak's login page
  - Your app should get a CODE, then exchange it for tokens

This is the Authorization Code Flow.
```

---

## Architecture

```
BROWSER              CLIENT (:3000)         KEYCLOAK (:8180)     RESOURCE SERVER (:8080)
   │                    Node.js                                    Spring Boot
   │                      │                       │                      │
   │── GET / ────────────>│                       │                      │
   │<── "Login" button ───│                       │                      │
   │                      │                       │                      │
   │── Click Login ──────>│                       │                      │
   │                      │── Build auth URL ────>│                      │
   │<── 302 Redirect ─────│                       │                      │
   │── Follow redirect ──────────────────────────>│                      │
   │                      │                       │── Login form         │
   │── Enter user/pass ──────────────────────────>│                      │
   │                      │                       │── Validate           │
   │<── 302 + code ───────────────────────────────│                      │
   │                      │                       │                      │
   │── GET /callback?code=abc ──>│                │                      │
   │                      │── POST /token ───────>│                      │
   │                      │   code + client_secret│                      │
   │                      │<── access_token ──────│                      │
   │                      │                       │                      │
   │                      │── GET /orders ─────────────────────────────>│
   │                      │   Authorization: Bearer <token>              │
   │                      │<── order data ──────────────────────────────│
   │<── "Welcome Rahul!" ─│                       │                      │
```

---

## Step 1: Start all 3 components

### Terminal 1: Authorization Server (Keycloak)
```bash
cd ~/oauth-labs/keycloak
docker compose up -d
# Already running from Lab 01
```

### Terminal 2: Resource Server (Spring Boot)
```bash
cd ~/oauth-labs/resource-server
mvn spring-boot:run
# Runs on http://localhost:8080
```

### Terminal 3: Client (Node.js)
```bash
cd ~/oauth-labs/lab-05-auth-code-flow/client
npm install
node server.js
# Runs on http://localhost:3000
```

---

## Step 2: Test the Resource Server alone

```bash
# Public endpoint — works without token
curl -s http://localhost:8080/public/menu | jq .

# Protected endpoint — FAILS without token
curl -s http://localhost:8080/orders
# 401 Unauthorized
```

> **This is the Resource Server's job:** reject requests without a valid token.

---

## Step 3: Login via Browser

Open **http://localhost:3000** → Click **"Login with Keycloak"**

### What to show students:

**In the browser address bar:**
```
localhost:8180/realms/foodexpress/protocol/openid-connect/auth?
  response_type=code        ← "I want a code"
  &client_id=foodexpress-web ← "I am the web app"
  &redirect_uri=...         ← "Send me back here"
  &scope=openid profile email
  &state=...                ← CSRF protection
```

**Explain:** "Our app doesn't show a login form. It REDIRECTS to Keycloak."

---

## Step 4: Enter Credentials

Login as **rahul** / **password123**

### What to show students:

1. Keycloak validates the credentials (not our app!)
2. Browser redirects back to `localhost:3000/callback?code=abc...&state=xyz...`
3. The `code` is visible in the URL briefly

---

## Step 5: Watch the Terminal

The Node.js terminal shows every step:

```
STEP 1: REDIRECT TO AUTHORIZATION SERVER
  response_type: code
  client_id:      foodexpress-web
  redirect_uri:   http://localhost:3000/callback
  scope:          openid profile email

STEP 2: CALLBACK FROM AUTHORIZATION SERVER
  Authorization Code: 8f3a7b2c...
  State matches?      true

STEP 3: TOKEN EXCHANGE (code --> tokens)
  This happens SERVER-TO-SERVER. Browser never sees client_secret.
  Access Token:   eyJhbG...
  Expires In:     300 seconds
  Refresh Token?  true
  ID Token?       true

STEP 4: USERINFO RESPONSE
  { "name": "Rahul Sharma", "email": "rahul@foodexpress.com", ... }
```

> **Key point:** Step 3 happens server-to-server. The browser never sees the client_secret.

---

## Step 6: Explore the Home Page

After login, the home page shows:
- Welcome message with name, email, roles
- Links to call the Resource Server
- Expandable sections showing the actual tokens

### Click each link:

| Link | Expected | Why |
|------|----------|-----|
| GET /profile | 200 — user info | Valid token, any role |
| GET /orders | 200 — order list | Valid token, any role |
| GET /admin/users | 403 Forbidden | Rahul is `customer`, not `admin` |
| GET /restaurant/dashboard | 403 Forbidden | Rahul is `customer`, not `restaurant-owner` |
| GET /debug/token | 200 — full token | Shows what Resource Server sees |
| GET /public/menu | 200 — menu | No token needed |

---

## Step 7: Test Role-Based Access with curl

```bash
# Get Rahul's token (customer)
RAHUL_TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123" \
  | jq -r '.access_token')

# Customer can access orders
curl -s http://localhost:8080/orders -H "Authorization: Bearer $RAHUL_TOKEN" | jq .message

# Customer CANNOT access admin
curl -s http://localhost:8080/admin/users -H "Authorization: Bearer $RAHUL_TOKEN"
# 403 Forbidden!

# Get Admin's token
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=admin-user&password=admin123" \
  | jq -r '.access_token')

# Admin CAN access admin
curl -s http://localhost:8080/admin/users -H "Authorization: Bearer $ADMIN_TOKEN" | jq .message

# Get Priya's token (restaurant-owner)
PRIYA_TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=priya&password=password123" \
  | jq -r '.access_token')

# Restaurant owner can access dashboard
curl -s http://localhost:8080/restaurant/dashboard -H "Authorization: Bearer $PRIYA_TOKEN" | jq .message
```

```
ACCESS MATRIX:
                        /orders   /restaurant   /admin
                                  /dashboard    /users
Customer (rahul)          ✓           ✗            ✗
Restaurant (priya)        ✓           ✓            ✗
Admin (admin-user)        ✓           ✓            ✓
No token                  ✗           ✗            ✗
```

---

## Step 8: Logout

Click **Logout** on the home page.

- Browser redirects to Keycloak's logout endpoint
- Session cleared in both the client app AND Keycloak
- Check Keycloak Admin → Sessions → Rahul's session is gone

---

## Step 9: Read the Code

Open `client/server.js` and walk through:

| Route | What It Does | OAuth Step |
|-------|-------------|-----------|
| `GET /` | Shows home page / login button | — |
| `GET /login` | Builds auth URL, redirects to Keycloak | Step 1 |
| `GET /callback` | Receives code, exchanges for tokens | Steps 2-4 |
| `GET /api/*` | Forwards request to Resource Server with Bearer token | Step 5 |
| `GET /logout` | Redirects to Keycloak logout | Logout |

---

## Key Teaching Points

| Point | Where to Show | What to Say |
|-------|--------------|-------------|
| Password never touches our app | Browser URL during login | "User types credentials in Keycloak, not in our form" |
| Code is short-lived | Terminal: Step 2 | "60 seconds, single-use. Intercepting it is useless without the secret" |
| Token exchange is server-to-server | Terminal: Step 3 | "client_secret never leaves the server. Browser never sees it" |
| JWT is self-contained | /debug/token response | "Resource Server validates locally. No call to Keycloak per request" |
| Roles control access | 403 on /admin/users | "Same API, different access. Roles are in the token" |

---

**Next:** [Lab 06 — Client Credentials Flow](../lab-06-client-credentials/LAB.md)
