# Lab 01: Keycloak Setup — Understanding the Authorization Server

## The Problem

```
Your app needs to:
  - Let users log in
  - Know WHO the user is
  - Know WHAT the user is allowed to do
  - Let services talk to each other securely

You could build all this yourself:
  - User database, password hashing, session management
  - Token generation, token validation, role management
  - Login pages, forgot password flows

Or... use an Authorization Server that does ALL of this.
That's Keycloak.
```

---

## Setup: JWT Decode Helper

JWT payloads are base64url-encoded. This one-liner decodes them:

```bash
# Paste this once per terminal session
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

Usage: `decode "$TOKEN"` or `decode "$TOKEN" '{.name, .email}'`

---

## Part 1: Start Keycloak

```bash
cd ~/oauth-labs/keycloak
docker compose up -d
```

Wait 30-60 seconds, then open: **http://localhost:8180**

Login: `admin` / `admin`

```
Keycloak Admin Console
├── Realms        (isolated tenants — like separate databases)
├── Users         (people who log in)
├── Roles         (permissions — customer, admin, etc.)
├── Clients       (apps that request tokens)
├── Client Scopes (what data goes into tokens)
└── Sessions      (who's currently logged in)
```

---

## Part 2: Create a Realm

A **Realm** is an isolated security domain. Think of it as a separate tenant.

```
Keycloak Server
├── master realm     (admin-only, don't use for apps)
├── foodexpress      (our app's realm) ← we'll create this
└── ...
```

### Steps:

1. Hover over **"master"** dropdown (top-left)
2. Click **"Create realm"**
3. Realm name: `foodexpress`, Enabled: ON
4. Click **Create**

### Verify:

```bash
curl -s http://localhost:8180/realms/foodexpress | jq .
```

---

## Part 3: Create Roles

Roles define WHAT a user can do.

### Steps:

1. Go to **Realm roles** (left sidebar)
2. Click **"Create role"**
3. Create 4 roles:

| Role Name | Description |
|-----------|-------------|
| `customer` | Regular customer |
| `restaurant-owner` | Restaurant owner |
| `delivery-partner` | Delivery partner |
| `admin` | Platform admin |

### Verify:

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8180/realms/master/protocol/openid-connect/token \
  -d "grant_type=password&client_id=admin-cli&username=admin&password=admin" \
  | jq -r '.access_token')

curl -s http://localhost:8180/admin/realms/foodexpress/roles \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.[].name'
```

> **Note:** The admin token expires in 60 seconds. Re-run the first command if you get errors.

---

## Part 4: Create Users

### Steps:

1. Go to **Users** → **Create new user**

**User 1: Rahul (Customer)**
```
Username:       rahul
Email:          rahul@foodexpress.com
First name:     Rahul
Last name:      Sharma
Email verified: ON
→ Save
→ Credentials tab → Set password: password123 → Temporary: OFF
→ Role mapping tab → Assign role → Select "customer"
```

**User 2: Priya (Restaurant Owner)**
```
Username:       priya
Email:          priya@foodexpress.com
First name:     Priya
Last name:      Patel
Password:       password123
Role:           restaurant-owner
```

**User 3: Admin**
```
Username:       admin-user
Email:          admin@foodexpress.com
First name:     Admin
Last name:      User
Password:       admin123
Role:           admin
```

### Verify:

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8180/realms/master/protocol/openid-connect/token \
  -d "grant_type=password&client_id=admin-cli&username=admin&password=admin" \
  | jq -r '.access_token')

curl -s http://localhost:8180/admin/realms/foodexpress/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" | jq '.[].username'
```

### Test authentication:

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=admin-cli" \
  -d "username=rahul" \
  -d "password=password123" | jq '{has_token: (.access_token != null), error}'
```

> **Teaching point:** We authenticated WITHOUT creating a Client yet.
> `admin-cli` is built-in. In production, you create your OWN clients.

---

## Part 5: Create Clients

A **Client** is any application that requests tokens from Keycloak.

```
Client = your app's identity in Keycloak:
  Client ID     = your app's username
  Client Secret = your app's password (confidential clients only)
  Redirect URI  = where Keycloak sends users after login
  Grant Type    = HOW your app gets tokens
```

### Client Types

```
┌─────────────────────┬──────────────────────────────────────┐
│ CONFIDENTIAL        │ PUBLIC                                │
│ (has a secret)      │ (no secret)                           │
├─────────────────────┼──────────────────────────────────────┤
│ Backend web apps    │ SPAs (browser JavaScript)             │
│ Server-side APIs    │ Mobile apps                           │
│ Microservices       │ Desktop apps                          │
│                     │                                       │
│ Secret stored       │ Code is visible to user               │
│ safely on server    │ Can't hide a secret                   │
└─────────────────────┴──────────────────────────────────────┘
```

### Create Client 1: foodexpress-web (Web App — Confidential)

1. Go to **Clients** → **Create client**

```
General:
  Client ID:        foodexpress-web
  Name:             FoodExpress Web App
  Client type:      OpenID Connect
  → Next

Capability:
  Client authentication:      ON  (confidential)
  Authentication flow:
    ✅ Standard flow           (Authorization Code)
    ✅ Direct access grants    (Password grant — for testing)
    ☐ Implicit flow
    ☐ Service accounts
  → Next

Login settings:
  Valid redirect URIs:    http://localhost:3000/*
  Web origins:            http://localhost:3000
  → Save
```

Go to **Credentials** tab → Copy the **Client secret** (should be `web-secret-123` if imported, or a generated value if created manually).

### Create Client 2: foodexpress-spa (SPA — Public, PKCE)

```
General:
  Client ID:        foodexpress-spa
  Client type:      OpenID Connect
  → Next

Capability:
  Client authentication:      OFF (public — no secret)
  Authentication flow:
    ✅ Standard flow
    ☐ Direct access grants
  → Next

Login settings:
  Valid redirect URIs:    http://localhost:5500/*
  Web origins:            http://localhost:5500
  → Save

Advanced tab → Proof Key for Code Exchange:
  Code Challenge Method:  S256
```

### Create Client 3: foodexpress-api (Service-to-Service — Confidential)

```
General:
  Client ID:        foodexpress-api
  Client type:      OpenID Connect
  → Next

Capability:
  Client authentication:      ON
  Authentication flow:
    ☐ Standard flow
    ☐ Direct access grants
    ✅ Service accounts         (Client Credentials!)
  → Next

Login settings:
  (leave empty — no redirect URIs for machine-to-machine)
  → Save
```

### Verify all clients:

```bash
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8180/realms/master/protocol/openid-connect/token \
  -d "grant_type=password&client_id=admin-cli&username=admin&password=admin" \
  | jq -r '.access_token')

curl -s http://localhost:8180/admin/realms/foodexpress/clients \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  | jq '.[] | select(.clientId | startswith("foodexpress")) | {clientId, publicClient, serviceAccountsEnabled, directAccessGrantsEnabled}'
```

### Test with your new client:

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email" | jq '{token_type, expires_in, scope}'
```

---

## Part 6: Understand Client Scopes

Scopes control **what data goes into the token**.

```
scope=openid          → sub (user ID), iss, aud, exp
scope=openid profile  → + name, preferred_username
scope=openid email    → + email, email_verified
scope=openid roles    → + realm_access.roles

More scope = more data in token = larger token
Always request MINIMUM necessary.
```

### Test scope differences:

```bash
echo "=== scope=openid ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid" \
  | jq -r '.access_token')
decode "$TOKEN" '{preferred_username, email, name, scope}'

echo "=== scope=openid profile ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid profile" \
  | jq -r '.access_token')
decode "$TOKEN" '{preferred_username, email, name, scope}'

echo "=== scope=openid profile email ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid profile email" \
  | jq -r '.access_token')
decode "$TOKEN" '{preferred_username, email, name, scope}'
```

> **Watch:** Each scope ADDS data. `openid` = minimal. `profile` adds name. `email` adds email.

---

## Part 7: Summary

```
KEYCLOAK (:8180)
├── Realm: foodexpress
│
├── Roles:
│   ├── customer
│   ├── restaurant-owner
│   ├── delivery-partner
│   └── admin
│
├── Users:
│   ├── rahul      (password123)  → customer
│   ├── priya      (password123)  → restaurant-owner
│   └── admin-user (admin123)     → admin
│
└── Clients:
    ├── foodexpress-web   (confidential, auth code + password grant)
    ├── foodexpress-spa   (public, PKCE)
    └── foodexpress-api   (confidential, client credentials)
```

---

**Next:** [Lab 02 — Auth Server Endpoints](../lab-02-endpoints/LAB.md)
