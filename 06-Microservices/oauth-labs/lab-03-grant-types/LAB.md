# Lab 03: Grant Types — How Clients Get Tokens

## The Problem

```
4 different apps need tokens from Keycloak:

  1. A web app (Node.js backend) — users log in via browser
  2. A cron job (no user) — runs every night to sync data
  3. A mobile app (no backend secret) — user logs in on phone
  4. A testing script — you just need a quick token for curl

Each needs a DIFFERENT way to get a token.
That's what Grant Types are.
```

**Pre-requisite:** Keycloak running from Lab 01. Paste the decode helper:

```bash
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

## The Decision Tree

```
START
  │
  ├── Is there a USER logging in?
  │     │
  │     ├── YES — Can you store a CLIENT SECRET safely?
  │     │     │
  │     │     ├── YES (backend server) → AUTHORIZATION CODE FLOW
  │     │     └── NO (SPA, mobile)     → AUTHORIZATION CODE + PKCE
  │     │
  │     └── Just testing?              → RESOURCE OWNER PASSWORD
  │
  └── NO (machine-to-machine)          → CLIENT CREDENTIALS
```

---

## Grant Type 1: Authorization Code Flow

**When:** Web app with a backend server. Users log in via browser.

```
BROWSER              YOUR SERVER           KEYCLOAK
   │                      │                    │
   │── Click Login ──────>│                    │
   │                      │── Redirect ──────> │
   │<──── Login Page ─────│<───────────────────│
   │── Enter creds ──────>│───────────────────>│
   │                      │<── code ────────── │
   │                      │── POST /token ───> │
   │                      │   code + secret    │
   │                      │<── tokens ──────── │
   │<── Welcome! ─────────│                    │
```

### Demo — open this URL in your browser:

```
http://localhost:8180/realms/foodexpress/protocol/openid-connect/auth?response_type=code&client_id=foodexpress-web&redirect_uri=http://localhost:3000/callback&scope=openid profile email&state=random123
```

Login as `rahul` / `password123`. Look at the redirect URL — it contains `?code=...&state=...`

> **Key point:** The code is short-lived (60 sec), single-use. Token exchange happens server-to-server.

---

## Grant Type 2: Client Credentials

**When:** Machine-to-machine. No user. Service A calls Service B.

```
YOUR SERVICE              KEYCLOAK
     │                        │
     │── POST /token ────────>│
     │   client_id             │
     │   client_secret         │
     │   grant_type=           │
     │   client_credentials    │
     │<── access_token ───────│
     │   (no refresh, no id)   │
```

### Demo:

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=foodexpress-api" \
  -d "client_secret=api-secret-456" | jq .
```

**Notice:** No `refresh_token`, no `id_token`. This is a machine identity.

### Decode the machine token:

```bash
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=foodexpress-api" \
  -d "client_secret=api-secret-456" \
  | jq -r '.access_token')

decode "$TOKEN" '{sub, azp, scope, preferred_username, email}'
```

> **Notice:** `preferred_username` and `email` are null — no user, just a machine.

---

## Grant Type 3: Authorization Code + PKCE

**When:** SPA or mobile app. User logs in but NO client secret possible.

```
BROWSER (SPA)               KEYCLOAK
     │                          │
     │── Generate:              │
     │   code_verifier (random) │
     │   code_challenge =       │
     │     SHA256(verifier)     │
     │                          │
     │── Redirect + challenge ─>│
     │── Enter creds ──────────>│
     │<── code ─────────────────│
     │                          │
     │── POST /token ──────────>│
     │   code + code_verifier   │
     │   (NO client_secret!)    │
     │                          │
     │<── tokens ───────────────│
```

### Demo — generate PKCE values:

```bash
CODE_VERIFIER=$(openssl rand -base64 32 | tr -d '=/+' | cut -c1-43)
CODE_CHALLENGE=$(echo -n "$CODE_VERIFIER" | openssl dgst -sha256 -binary | base64 | tr -d '=' | tr '/+' '_-')

echo "code_verifier:  $CODE_VERIFIER"
echo "code_challenge: $CODE_CHALLENGE"

echo ""
echo "Open this URL in browser:"
echo "http://localhost:8180/realms/foodexpress/protocol/openid-connect/auth?response_type=code&client_id=foodexpress-spa&redirect_uri=http://localhost:5500/&scope=openid profile email&state=xyz&code_challenge=$CODE_CHALLENGE&code_challenge_method=S256"
```

> **Key point:** `code_verifier` replaces the client_secret. Attacker who intercepts the code can't use it without the verifier.

---

## Grant Type 4: Resource Owner Password (ROPC)

**When:** TESTING ONLY. Never in production.

```
YOUR SCRIPT               KEYCLOAK
     │                        │
     │── POST /token ────────>│
     │   username + password   │
     │   client_id + secret    │
     │<── tokens ─────────────│
```

### Demo:

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email" | jq '{token_type, expires_in, scope}'
```

> **Warning:** User's password goes through YOUR app. Anti-pattern. Use Auth Code in production.

---

## Grant Type 5: Implicit Flow (DEPRECATED)

```
DON'T USE. Token appears in URL:
  redirect_uri#access_token=eyJhbG...

Problems:
  ✗ Token in browser history
  ✗ Token in server logs
  ✗ Token leaked via Referrer header
  ✗ No refresh token support

Replaced by PKCE.
```

---

## Comparison

```
┌───────────────────┬──────────┬───────────┬──────────┬────────────┐
│                   │ Auth     │ Client    │ PKCE     │ Password   │
│                   │ Code     │ Creds     │          │ (ROPC)     │
├───────────────────┼──────────┼───────────┼──────────┼────────────┤
│ User involved?    │ YES      │ NO        │ YES      │ YES        │
│ Browser needed?   │ YES      │ NO        │ YES      │ NO         │
│ Client secret?    │ YES      │ YES       │ NO       │ YES        │
│ Has refresh_token?│ YES      │ NO        │ YES      │ YES        │
│ Has id_token?     │ YES      │ NO        │ YES      │ YES        │
│ Use in production?│ YES      │ YES       │ YES      │ NO         │
├───────────────────┼──────────┼───────────┼──────────┼────────────┤
│ Use for:          │ Web apps │ Cron jobs │ SPAs     │ Testing    │
│                   │ Backend  │ Services  │ Mobile   │ only       │
└───────────────────┴──────────┴───────────┴──────────┴────────────┘
```

---

**Next:** [Lab 04 — Tokens Deep Dive](../lab-04-tokens-deep-dive/LAB.md)
