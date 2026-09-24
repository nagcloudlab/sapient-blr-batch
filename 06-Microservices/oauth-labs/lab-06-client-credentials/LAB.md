# Lab 06: Client Credentials Flow — Service-to-Service

## The Problem

```
Lab 05 was about USERS logging in.
But what about machines talking to machines?

  - A cron job that syncs data every night
  - Order-service calling payment-service
  - A batch job processing reports

No user. No browser. No redirect. No login form.
Just two services authenticating with each other.
```

---

## Architecture

```
CLIENT SERVICE (:3001)         KEYCLOAK (:8180)       RESOURCE SERVER (:8080)
  Node.js                                               Spring Boot
       │                             │                        │
       │── POST /token ─────────────>│                        │
       │   grant_type=client_creds   │                        │
       │   client_id + client_secret │                        │
       │<── access_token ────────────│                        │
       │   (NO refresh, NO id_token) │                        │
       │                             │                        │
       │── GET /orders (Bearer token) ───────────────────────>│
       │<── order data ──────────────────────────────────────│
```

---

## Step 1: Start the Client Service

(Keycloak + Resource Server still running from Lab 05)

```bash
cd ~/oauth-labs/lab-06-client-credentials/client-service
npm install
node server.js
# Runs on http://localhost:3001
```

Open http://localhost:3001

---

## Step 2: Compare with Lab 05

| | Auth Code (Lab 05) | Client Credentials (This lab) |
|-|-------------------|-------------------------------|
| User involved? | YES (Rahul logs in) | NO |
| Browser redirect? | YES | NO |
| Token has username? | YES | NO |
| Token has email? | YES | NO |
| Has refresh_token? | YES | NO |
| Has id_token? | YES | NO |

---

## Step 3: Click "Fetch Orders"

Watch the terminal:

```
CLIENT CREDENTIALS: Requesting new token from Keycloak
  grant_type:     client_credentials
  client_id:      foodexpress-api
  client_secret:  api-secr...
  NO username, NO password — this is MACHINE-to-MACHINE

Token received:
  access_token:     eyJhbG...
  expires_in:       300 seconds
  has refresh_token? false
  has id_token?      false
```

---

## Step 4: Click "Show Machine Token"

The decoded token shows:
- `azp: "foodexpress-api"` — identifies the service
- NO `preferred_username`
- NO `email`
- This token represents the APP, not a person

---

## Step 5: Same demo with curl

```bash
# Get machine token
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=foodexpress-api" \
  -d "client_secret=api-secret-456" | jq .

# Call Resource Server with machine token
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials&client_id=foodexpress-api&client_secret=api-secret-456" \
  | jq -r '.access_token')

curl -s http://localhost:8080/orders -H "Authorization: Bearer $TOKEN" | jq .
```

---

## Step 6: Token Caching

Click "Fetch Orders" again. Terminal shows:

```
  Using CACHED token (expires in 280 seconds)
```

> **Teaching point:** Don't request a new token for every API call. Cache it and reuse until expiry.

---

**Next:** [Lab 07 — PKCE Flow](../lab-07-pkce-flow/LAB.md)
