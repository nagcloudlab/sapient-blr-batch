# Lab 02: Auth Server Endpoints — What Keycloak Exposes

## The Problem

```
You know Keycloak issues tokens. But HOW?

  - Where does the browser go to log in?
  - Where does the app send the authorization code?
  - Where do you check who a user is?
  - Where do you get the public keys to verify tokens?
  - Where do you send users to log out?

Every OAuth/OIDC server publishes these endpoints.
You don't guess them — you DISCOVER them.
```

**Pre-requisite:** Keycloak running from Lab 01. Paste the decode helper:

```bash
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

---

## Part 1: The Discovery Endpoint

Every OIDC server has a `.well-known` URL that lists ALL its endpoints:

```bash
curl -s http://localhost:8180/realms/foodexpress/.well-known/openid-configuration | jq .
```

The important ones:

```bash
curl -s http://localhost:8180/realms/foodexpress/.well-known/openid-configuration \
  | jq '{
    issuer,
    authorization_endpoint,
    token_endpoint,
    userinfo_endpoint,
    jwks_uri,
    end_session_endpoint,
    introspection_endpoint,
    grant_types_supported,
    scopes_supported
  }'
```

```
┌──────────────────────────┬────────────────────────────────────────────┐
│ Endpoint                 │ Purpose                                    │
├──────────────────────────┼────────────────────────────────────────────┤
│ authorization_endpoint   │ Where users LOG IN (browser redirect)      │
│ token_endpoint           │ Where apps EXCHANGE code for tokens        │
│ userinfo_endpoint        │ Where apps GET user details with a token   │
│ jwks_uri                 │ Where apps GET public keys to verify JWTs  │
│ end_session_endpoint     │ Where users LOG OUT                        │
│ introspection_endpoint   │ Where apps CHECK if a token is still valid │
└──────────────────────────┴────────────────────────────────────────────┘
```

> **Teaching point:** Your app should NEVER hardcode these URLs.
> Discover them from `.well-known` at startup.

---

## Part 2: Authorization Endpoint (/auth)

**Purpose:** Where the browser goes to show the login form.

### Build the URL manually:

```
http://localhost:8180/realms/foodexpress/protocol/openid-connect/auth?
  response_type=code
  &client_id=foodexpress-web
  &redirect_uri=http://localhost:3000/callback
  &scope=openid profile email
  &state=random123
```

### Open in browser — you'll see the Keycloak login page.

```
What each parameter means:
  response_type=code       "I want an authorization code"
  client_id=foodexpress-web "I am the web app"
  redirect_uri=...         "After login, send user here"
  scope=openid profile email "I want these claims in the token"
  state=random123          "CSRF protection — verify on callback"
```

Login as `rahul` / `password123`. Browser redirects to:
```
http://localhost:3000/callback?code=abc123...&state=random123
```
(Will fail — no server on :3000 yet. But look at the URL — it has the `code`.)

---

## Part 3: Token Endpoint (/token)

**Purpose:** THE most important endpoint. Where apps exchange credentials for tokens.

### Test 1: Password Grant (for testing)

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email" | jq .
```

**Response:**
```json
{
  "access_token": "eyJhbG...",      ← for calling APIs
  "refresh_token": "eyJhbG...",     ← for getting new access tokens
  "id_token": "eyJhbG...",          ← for knowing WHO logged in
  "token_type": "Bearer",           ← use in Authorization header
  "expires_in": 300,                ← access token lives 5 minutes
  "refresh_expires_in": 1800        ← refresh token lives 30 minutes
}
```

### Test 2: Client Credentials (machine-to-machine)

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=foodexpress-api" \
  -d "client_secret=api-secret-456" | jq .
```

**Notice the difference:**
```
Password grant:            Client Credentials:
  Has refresh_token ✓        Has refresh_token ✗
  Has id_token      ✓        Has id_token      ✗
  Has user info     ✓        Has NO user info
```

### Test 3: Wrong credentials

```bash
# Wrong password
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=WRONG" | jq .

# Wrong client secret
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=WRONG-SECRET" \
  -d "username=rahul" \
  -d "password=password123" | jq .
```

> **Teaching point:** Keycloak validates BOTH the client AND the user.

---

## Part 4: UserInfo Endpoint (/userinfo)

**Purpose:** Get user details using an access token.

```bash
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email" \
  | jq -r '.access_token')

curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer $TOKEN" | jq .
```

```bash
# Without token — fails
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo | jq .
```

---

## Part 5: JWKS Endpoint (/certs)

**Purpose:** Public keys to verify JWT signatures.

```bash
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/certs | jq .
```

### Verify the key matches the token:

```bash
# Get kid from token header
echo $TOKEN | cut -d'.' -f1 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq .kid

# Get kid from JWKS
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/certs \
  | jq '.keys[] | select(.use=="sig") | .kid'
```

> **They match!** This is how Resource Servers know which key to verify with.

---

## Part 6: Logout Endpoint (/logout)

**Purpose:** End the user's session.

```bash
# Get tokens
RESPONSE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid")
REFRESH=$(echo $RESPONSE | jq -r '.refresh_token')

# Logout
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/logout \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH"
echo "Logged out"

# Try refresh — should fail
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=refresh_token" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH" | jq .
```

> **Teaching point:** Logout revokes the refresh token. Access token may still work briefly (validated locally). That's why access tokens are SHORT-lived.

---

## Part 7: Introspection Endpoint (/introspect)

**Purpose:** Ask Keycloak "Is this token still valid?"

```bash
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  | jq -r '.access_token')

# Valid token
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token/introspect \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "token=$TOKEN" | jq '{active, username: .preferred_username, exp, scope}'

# Fake token
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token/introspect \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "token=fake.token.here" | jq .
```

> **Teaching point:** Introspection = real-time check with Keycloak. JWT validation = local check with public key. Use introspection for high-security (banking). Use JWT for performance (most apps).

---

## Part 8: Summary — All Endpoints

```
┌──────────────────────┬───────────────────────────────────────────────┐
│ ENDPOINT             │ PURPOSE                                       │
├──────────────────────┼───────────────────────────────────────────────┤
│ GET  /.well-known/.. │ Discover all endpoints                        │
│ GET  /auth?...       │ Show login page (browser)                     │
│ POST /token          │ Get tokens (code, password, client_creds)     │
│ GET  /userinfo       │ Get user details (with Bearer token)          │
│ GET  /certs          │ Get public keys (JWKS)                        │
│ POST /logout         │ End session (with refresh_token)              │
│ POST /token/introspect │ Check if token is valid                     │
└──────────────────────┴───────────────────────────────────────────────┘
```

---

**Next:** [Lab 03 — Grant Types](../lab-03-grant-types/LAB.md)
