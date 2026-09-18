# OAuth 2.0 + OIDC — Practical Labs

> **Style:** Trainer-led, incremental, problem-solution
> **Stack:** Keycloak (Authorization Server) + Node.js (Client) + Spring Boot (Resource Server)

---

## Architecture

```
┌──────────────┐       ┌──────────────────┐       ┌──────────────────┐
│   CLIENT     │ ────> │  AUTHORIZATION   │ ────> │  RESOURCE        │
│   (Node.js)  │       │  SERVER          │       │  SERVER          │
│              │       │  (Keycloak)      │       │  (Spring Boot)   │
│ Requests     │       │  :8180           │       │  :8080           │
│ tokens       │       │  Issues tokens   │       │  Validates tokens│
└──────────────┘       └──────────────────┘       └──────────────────┘
```

---

## Phase 1: UNDERSTAND (curl + Keycloak Admin — no code)

| # | Lab | What You'll Learn |
|---|-----|-------------------|
| 01 | [Keycloak Setup](lab-01-keycloak-setup/LAB.md) | Create realm, users, roles, clients. Understand every config. |
| 02 | [Auth Server Endpoints](lab-02-endpoints/LAB.md) | Discover .well-known, explore /auth, /token, /userinfo, /certs, /logout, /introspect |
| 03 | [Grant Types](lab-03-grant-types/LAB.md) | All 4 flows with curl. Decision tree. When to use which. |
| 04 | [Tokens Deep Dive](lab-04-tokens-deep-dive/LAB.md) | Access vs Refresh vs ID token. Decode, expiry, refresh cycle, signature, tampering. |

## Phase 2: BUILD (Node.js Client + Spring Boot Resource Server)

| # | Lab | What You'll Build |
|---|-----|-------------------|
| 05 | [Auth Code Flow](lab-05-auth-code-flow/LAB.md) | Node.js client + Spring Boot resource server, browser login |
| 06 | [Client Credentials](lab-06-client-credentials/LAB.md) | Machine-to-machine, no user, service token |
| 07 | [PKCE Flow](lab-07-pkce-flow/LAB.md) | SPA (browser-only), no client secret, code_verifier |
| 08 | [OIDC](lab-08-oidc/LAB.md) | ID token vs access token, userinfo, scopes |
| 09 | [Secure Microservices](lab-09-secure-microservices/LAB.md) | Role-based access matrix, 3 users, curl tests |
| 10 | [Token Security](lab-10-token-security/LAB.md) | XSS, alg=none forgery, replay, refresh theft |

---

## Quick Start

```bash
cd ~/oauth-labs/keycloak
docker compose up -d
# Wait 30-60 sec
# Admin: http://localhost:8180 (admin/admin)
```

Then follow Lab 01.

---

## Pre-configured Users (after Lab 01 setup)

| Username | Password | Role |
|----------|----------|------|
| rahul | password123 | customer |
| priya | password123 | restaurant-owner |
| admin-user | admin123 | admin |

## Pre-configured Clients (after Lab 01 setup)

| Client ID | Type | Flow | Secret |
|-----------|------|------|--------|
| foodexpress-web | Confidential | Auth Code + Password | (from Keycloak) |
| foodexpress-spa | Public | PKCE | (none) |
| foodexpress-api | Confidential | Client Credentials | (from Keycloak) |

## Key Endpoints

```
Discovery:     http://localhost:8180/realms/foodexpress/.well-known/openid-configuration
Authorization: http://localhost:8180/realms/foodexpress/protocol/openid-connect/auth
Token:         http://localhost:8180/realms/foodexpress/protocol/openid-connect/token
UserInfo:      http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo
JWKS:          http://localhost:8180/realms/foodexpress/protocol/openid-connect/certs
Logout:        http://localhost:8180/realms/foodexpress/protocol/openid-connect/logout
Introspect:    http://localhost:8180/realms/foodexpress/protocol/openid-connect/token/introspect
```
