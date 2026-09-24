# Lab 07: PKCE Flow — SPA Login Without a Secret

## The Problem

```
Lab 05: Web app with a backend → has a client_secret (stored on server)
This lab: SPA running in browser → code is visible → CAN'T store a secret

How does a browser-only app authenticate securely?
Answer: PKCE (Proof Key for Code Exchange)
```

---

## Architecture

```
BROWSER (SPA :5500)             KEYCLOAK (:8180)        RESOURCE SERVER (:8080)
   │                                  │                        │
   │── Generate random code_verifier  │                        │
   │── code_challenge = SHA256(verifier)                       │
   │                                  │                        │
   │── Redirect + code_challenge ────>│                        │
   │── Enter credentials ────────────>│                        │
   │<── 302 + authorization code ─────│                        │
   │                                  │                        │
   │── POST /token ──────────────────>│                        │
   │   code + code_verifier           │                        │
   │   (NO client_secret!)            │── SHA256(verifier)     │
   │                                  │   == challenge? ✓      │
   │<── tokens ───────────────────────│                        │
   │                                  │                        │
   │── GET /orders (Bearer token) ────────────────────────────>│
   │<── data ─────────────────────────────────────────────────│
```

---

## Step 1: Serve the SPA

```bash
cd ~/oauth-labs/lab-07-pkce-flow/client
python3 -m http.server 5500
```

Open http://localhost:5500

---

## Step 2: Click "Login with Keycloak (PKCE)"

Watch the **log panel** at the bottom of the page:

```
STEP 1: PKCE LOGIN
  code_verifier:  aB3dE5fG7hI9jK1lM...
  code_challenge: xY2zA4bC6dE8fG0hI...
  method:         S256 (SHA-256)
  NO client_secret! PKCE replaces it.

STEP 2: CALLBACK
  code:          8f3a7b2c...
  state matches: true

STEP 3: TOKEN EXCHANGE
  Sending code + code_verifier (NOT client_secret!)

STEP 4: DECODED
  User: rahul
  Roles: ["customer"]
```

---

## Step 3: Compare Auth Code vs PKCE

```
Auth Code (Lab 05):               PKCE (This lab):
  Confidential client               Public client
  Has client_secret                  NO client_secret
  Token exchange on backend          Token exchange in browser
  client_secret proves identity      code_verifier proves identity
  For: server-side web apps          For: SPAs, mobile apps
```

---

## Step 4: Call Resource Server

Click the API buttons. Same Resource Server, same validation — doesn't matter if token came from Auth Code or PKCE.

---

## Step 5: Why PKCE is secure

```
Without PKCE (old Implicit flow):
  Token returned directly in URL fragment
  → Visible in browser history, logs, referrer headers

With PKCE:
  1. SPA generates random code_verifier (secret, in memory only)
  2. Sends SHA256(verifier) as code_challenge to Keycloak
  3. Gets auth code back
  4. Exchanges code + code_verifier for tokens
  5. Keycloak checks: SHA256(verifier) == stored challenge?
  6. Attacker who intercepts the code can't use it
     without the code_verifier (which never left the browser's memory)
```

---

**Next:** [Lab 08 — OIDC](../lab-08-oidc/LAB.md)
