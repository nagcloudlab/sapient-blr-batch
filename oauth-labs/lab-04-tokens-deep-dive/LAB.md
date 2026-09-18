# Lab 04: Tokens Deep Dive — Access, Refresh, and ID Tokens

## The Problem

```
Keycloak gave you 3 tokens:
  access_token   — eyJhbGciOiJSUz...
  refresh_token  — eyJhbGciOiJIUz...
  id_token       — eyJhbGciOiJSUz...

What IS each one? What's INSIDE? WHERE do you send each one?
WHEN do they expire? Can someone FORGE one?
```

**Pre-requisite:** Keycloak running from Lab 01. Paste the decode helper:

```bash
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

---

## Part 1: Get All 3 Tokens

```bash
RESPONSE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  -d "scope=openid profile email")

ACCESS=$(echo $RESPONSE | jq -r '.access_token')
REFRESH=$(echo $RESPONSE | jq -r '.refresh_token')
ID_TOKEN=$(echo $RESPONSE | jq -r '.id_token')

echo "Access Token length:  $(echo -n $ACCESS | wc -c | tr -d ' ') chars"
echo "Refresh Token length: $(echo -n $REFRESH | wc -c | tr -d ' ') chars"
echo "ID Token length:      $(echo -n $ID_TOKEN | wc -c | tr -d ' ') chars"
echo "Access expires in:    $(echo $RESPONSE | jq '.expires_in') seconds"
echo "Refresh expires in:   $(echo $RESPONSE | jq '.refresh_expires_in') seconds"
```

---

## Part 2: JWT Structure

```
A JWT has 3 parts separated by dots:

  eyJhbGciOiJSUz.eyJzdWIiOiIxMjM0.SflKxwRJSMeKKF2QT4fw

  ┌──────────┐   ┌──────────┐   ┌──────────┐
  │  HEADER  │ . │ PAYLOAD  │ . │SIGNATURE │
  └──────────┘   └──────────┘   └──────────┘
       │               │              │
  Algorithm &     Claims (data)   Proof that
  Key ID          User, Roles     nothing was
                  Expiry, Issuer  tampered with
```

---

## Part 3: Access Token — "What Can I Do?"

```bash
echo "=== HEADER ==="
echo $ACCESS | cut -d'.' -f1 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq .

echo ""
echo "=== PAYLOAD ==="
decode "$ACCESS"
```

**Header tells you:**
```json
{
  "alg": "RS256",    ← Algorithm: RSA + SHA-256
  "typ": "JWT",      ← Type
  "kid": "abc..."    ← Key ID: which key to verify with
}
```

**Payload tells you:**
```json
{
  "sub": "user-uuid",              ← Unique user ID
  "preferred_username": "rahul",   ← Username
  "email": "rahul@foodexpress.com",← Email
  "name": "Rahul Sharma",         ← Full name
  "realm_access": {
    "roles": ["customer"]           ← Roles!
  },
  "scope": "openid profile email", ← Granted scopes
  "exp": 1789656013,               ← Expiry (Unix timestamp)
  "iss": "http://localhost:8180/...", ← Issuer
  "azp": "foodexpress-web"         ← Which client
}
```

```
ACCESS TOKEN:
  Purpose:    Call APIs (Resource Servers)
  Sent to:    API in Authorization: Bearer <token>
  Lifetime:   5 minutes (short — limits damage if stolen)
  Validated:  LOCALLY by Resource Server (JWKS public key)
```

---

## Part 4: Refresh Token — "Give Me a New Access Token"

```bash
decode "$REFRESH"
```

```
REFRESH TOKEN:
  Purpose:    Get a NEW access token without re-login
  Sent to:    ONLY Keycloak /token endpoint
  NEVER to:   APIs / Resource Servers
  Lifetime:   30 minutes
  Validated:  BY Keycloak (server-side)
```

### Demo — refresh the token:

```bash
NEW_RESPONSE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=refresh_token" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH")

echo "New access token: $(echo $NEW_RESPONSE | jq -r '.access_token' | cut -c1-40)..."
echo "Same as old?      $([ "$ACCESS" = "$(echo $NEW_RESPONSE | jq -r '.access_token')" ] && echo YES || echo NO)"
```

### Demo — old refresh token is now DEAD (rotation):

```bash
curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=refresh_token" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "refresh_token=$REFRESH" | jq .error
```

**Expected:** `"invalid_grant"` — rotation killed the old token.

```
ROTATION prevents theft:
  Attacker steals refresh_token_1 and uses it
  Real user tries refresh_token_1 → FAILS
  Keycloak detects: "Two parties used same token!"
  Keycloak REVOKES all tokens
  Both must re-login. User notices. Changes password.
```

---

## Part 5: ID Token — "Who Am I?"

```bash
decode "$ID_TOKEN"
```

```
ID TOKEN:
  Purpose:    Tell the CLIENT who the user is
  Sent to:    CLIENT app only
  NEVER to:   APIs / Resource Servers
  Lifetime:   5 minutes
  Only with:  scope=openid (OIDC)
```

---

## Part 6: The Three Tokens Compared

```
┌─────────────────────┬─────────────────┬─────────────────┬──────────────────┐
│                     │ ACCESS TOKEN    │ REFRESH TOKEN   │ ID TOKEN         │
├─────────────────────┼─────────────────┼─────────────────┼──────────────────┤
│ Purpose             │ Call APIs       │ Get new access  │ User identity    │
│ Send to             │ Resource Server │ Keycloak ONLY   │ Client app ONLY  │
│ Contains            │ User + roles    │ Session info    │ Name, email      │
│ Lifetime            │ 5 min (short)   │ 30 min (longer) │ 5 min (short)    │
│ Validated by        │ Resource Server │ Keycloak        │ Client app       │
│ If stolen           │ 5 min window    │ Rotation detects│ Identity leak    │
│ Audience (aud)      │ API             │ Keycloak        │ Client           │
└─────────────────────┴─────────────────┴─────────────────┴──────────────────┘
```

---

## Part 7: Signature Verification

```bash
# kid from token header
echo "Token kid:"
echo $ACCESS | cut -d'.' -f1 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq -r '.kid'

# kid from JWKS
echo "JWKS kid:"
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/certs \
  | jq -r '.keys[] | select(.use=="sig") | .kid'
```

**They match!**

```
HOW VERIFICATION WORKS:

  1. Resource Server receives: Bearer eyJhbG...
  2. Reads header → kid = "abc..."
  3. Downloads JWKS → finds key with matching kid
  4. Verifies signature using that public key
  5. Checks exp (not expired) and iss (correct issuer)

  ZERO network calls to Keycloak per request.
```

### Demo — tamper fails:

```bash
# Fake token with alg:none
FAKE_H=$(echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d '=' | tr '/+' '_-')
FAKE_P=$(echo -n '{"sub":"hacker","preferred_username":"admin"}' | base64 | tr -d '=' | tr '/+' '_-')

curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer ${FAKE_H}.${FAKE_P}." | jq .
```

> **Rejected.** Without Keycloak's private key, you can't forge a valid signature.

---

## Part 8: Token Expiry

```bash
decode "$ACCESS" '{issued: (.iat | todate), expires: (.exp | todate), ttl: (.exp - .iat)}'
```

```
TIMELINE:
  00:00  Login → access (5 min) + refresh (30 min)
  05:00  Access expires → API returns 401
  05:01  Refresh → new access (5 min) + new refresh (30 min)
  ...
  35:00  Refresh expires (30 min idle) → must login again
```

### Demo — wait for expiry:

```bash
# Set Access Token Lifespan to 30s in Keycloak Admin for testing
# Realm settings → Tokens → Access Token Lifespan → 30

TOKEN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password" \
  -d "client_id=foodexpress-web" \
  -d "client_secret=web-secret-123" \
  -d "username=rahul" \
  -d "password=password123" \
  | jq -r '.access_token')

echo "Works now:"
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer $TOKEN" | jq .preferred_username

sleep 35

echo "Expired:"
curl -s http://localhost:8180/realms/foodexpress/protocol/openid-connect/userinfo \
  -H "Authorization: Bearer $TOKEN" | jq .
```

> **Remember:** Set lifespan back to 300 after testing!

---

## Part 9: What You Now Know

```
After Labs 01-04, you understand:

✓ What an Authorization Server is (Keycloak)
✓ How to create realms, users, roles, clients
✓ Every endpoint an auth server exposes
✓ 4 grant types and when to use each
✓ JWT structure: header.payload.signature
✓ Access token: for APIs, short-lived, validated locally
✓ Refresh token: for renewal, rotation prevents theft
✓ ID token: for identity, OIDC only
✓ How signature verification works (JWKS)
✓ Why tokens expire and the refresh lifecycle

NOW we build:
  Lab 05: Auth Code Flow (Node.js client + Spring Boot resource server)
  Lab 06: Client Credentials (service-to-service)
  Lab 07: PKCE (SPA)
  Lab 08: OIDC (identity layer)
  Lab 09: Secure Microservices
  Lab 10: Token Security
```

---

**Next:** [Lab 05 — Authorization Code Flow (Build It)](../lab-05-auth-code-flow/LAB.md)
