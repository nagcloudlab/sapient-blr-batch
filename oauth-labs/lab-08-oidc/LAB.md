# Lab 08: OpenID Connect — Identity on Top of OAuth

## The Problem

```
OAuth 2.0 answers: "What can this token ACCESS?"
But NOT:           "WHO is the user?"

You have an access_token. You can call APIs.
But the access_token is for the RESOURCE SERVER, not for your app.

How does YOUR APP know the user's name, email, picture?
Answer: OpenID Connect (OIDC) — adds an identity layer to OAuth.
```

---

## OIDC = OAuth + Identity

```
OAuth alone:    access_token           → "What can I do?"
OIDC adds:      access_token           → "What can I do?"
                + id_token             → "Who am I?"
                + /userinfo endpoint   → "Tell me more about the user"
```

---

## Step 1: With vs Without scope=openid

Paste the decode helper:
```bash
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

```bash
# WITHOUT openid scope (pure OAuth)
echo "=== WITHOUT openid ==="
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" | jq 'keys'
# No id_token!

# WITH openid scope (OIDC)
echo "=== WITH openid ==="
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email" | jq 'keys'
# Has id_token!
```

---

## Step 2: Decode the ID Token

```bash
RESPONSE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email")

# Access token — for APIs
echo "=== ACCESS TOKEN ==="
decode "$(echo $RESPONSE | jq -r '.access_token')" '{preferred_username, email, scope, realm_access}'

# ID token — for the CLIENT APP
echo "=== ID TOKEN ==="
decode "$(echo $RESPONSE | jq -r '.id_token')" '{preferred_username, name, email, email_verified, typ, aud}'
```

```
ACCESS TOKEN:                    ID TOKEN:
  aud: "account"                   aud: "foodexpress-web"
  typ: "Bearer"                    typ: "ID"
  For: Resource Server             For: Client app
  Purpose: API access              Purpose: User identity
```

---

## Step 3: UserInfo Endpoint

```bash
TOKEN=$(echo $RESPONSE | jq -r '.access_token')

curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer $TOKEN" | jq .
```

> **UserInfo** returns the same data as the id_token, but via an API call.
> Use id_token when login-time data is enough. Use UserInfo for fresh data.

---

## Step 4: Scopes Control Claims

```bash
# Only openid — minimal
echo "=== openid only ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid" \
  | jq -r '.id_token')
decode "$TOKEN" '{name, email, preferred_username}'

# openid + profile
echo "=== openid profile ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid profile" \
  | jq -r '.id_token')
decode "$TOKEN" '{name, email, preferred_username}'

# openid + profile + email
echo "=== openid profile email ==="
TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123&scope=openid profile email" \
  | jq -r '.id_token')
decode "$TOKEN" '{name, email, preferred_username}'
```

```
openid          → preferred_username only
openid profile  → + name, given_name, family_name
openid email    → + email, email_verified
```

> **Principle:** Request minimum scope. Don't ask for email if you don't need it.

---

**Next:** [Lab 09 — Secure Microservices](../lab-09-secure-microservices/LAB.md)
