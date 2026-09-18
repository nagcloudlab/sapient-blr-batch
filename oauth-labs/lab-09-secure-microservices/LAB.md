# Lab 09: Secure Microservices — Token-Based Access Control

## The Problem

```
You have multiple services:
  - Order Service
  - Payment Service
  - Admin Dashboard
  - Public Menu

Each needs different access rules:
  - Menu: anyone can see it
  - Orders: only logged-in users
  - Dashboard: only restaurant owners
  - Admin: only admins

How do you enforce this with ONE token?
Answer: Role-based access control using JWT claims.
```

---

## Architecture

```
                              RESOURCE SERVER (:8080)
                              ┌──────────────────────────────┐
  CLIENT                      │                              │
  (any lab)     Keycloak      │  /public/menu       → open   │
                (:8180)       │  /orders            → auth   │
                   │          │  /profile           → auth   │
              token│          │  /restaurant/*      → owner  │
                   v          │  /admin/*           → admin  │
            Bearer token ──>  │  /debug/token       → auth   │
                              │                              │
                              │  Validates JWT locally       │
                              │  Extracts roles from token   │
                              └──────────────────────────────┘
```

---

## Step 1: Test with 3 Different Users

Paste the decode helper:
```bash
decode() { echo "$1" | cut -d'.' -f2 | tr '_-' '/+' | awk '{l=length%4;if(l)printf"%s%s",$0,substr("====",1,4-l);else print}' | base64 -D | jq "${2:-.}"; }
```

```bash
# Get tokens for all 3 users
RAHUL=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=rahul&password=password123" \
  | jq -r '.access_token')

PRIYA=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=priya&password=password123" \
  | jq -r '.access_token')

ADMIN=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=password&client_id=foodexpress-web&client_secret=web-secret-123&username=admin-user&password=admin123" \
  | jq -r '.access_token')

# See each user's roles
echo "Rahul's roles:" && decode "$RAHUL" '.realm_access.roles'
echo "Priya's roles:" && decode "$PRIYA" '.realm_access.roles'
echo "Admin's roles:" && decode "$ADMIN" '.realm_access.roles'
```

---

## Step 2: Test Access Matrix

```bash
echo "=== PUBLIC (no token) ==="
curl -s http://localhost:8080/public/menu | jq '.[0]'

echo "=== RAHUL (customer) ==="
curl -s -w "\n%{http_code}" http://localhost:8080/orders -H "Authorization: Bearer $RAHUL" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/restaurant/dashboard -H "Authorization: Bearer $RAHUL" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/admin/users -H "Authorization: Bearer $RAHUL" | tail -1

echo "=== PRIYA (restaurant-owner) ==="
curl -s -w "\n%{http_code}" http://localhost:8080/orders -H "Authorization: Bearer $PRIYA" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/restaurant/dashboard -H "Authorization: Bearer $PRIYA" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/admin/users -H "Authorization: Bearer $PRIYA" | tail -1

echo "=== ADMIN ==="
curl -s -w "\n%{http_code}" http://localhost:8080/orders -H "Authorization: Bearer $ADMIN" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/restaurant/dashboard -H "Authorization: Bearer $ADMIN" | tail -1
curl -s -w "\n%{http_code}" http://localhost:8080/admin/users -H "Authorization: Bearer $ADMIN" | tail -1
```

**Expected:**
```
                    /orders   /restaurant   /admin
                              /dashboard    /users
No token              401        401          401
Rahul (customer)      200        403          403
Priya (rest-owner)    200        200          403
Admin                 200        200          200
```

---

## Step 3: See What the Resource Server Sees

```bash
curl -s http://localhost:8080/debug/token -H "Authorization: Bearer $RAHUL" | jq .
```

Shows: header (alg, kid), all claims, roles, expiry — exactly what Spring Boot parsed from the JWT.

---

## Step 4: Service-to-Service (Client Credentials)

```bash
# Machine token — no user
MACHINE=$(curl -s -X POST http://localhost:8180/realms/foodexpress/protocol/openid-connect/token \
  -d "grant_type=client_credentials&client_id=foodexpress-api&client_secret=api-secret-456" \
  | jq -r '.access_token')

# Machine can access /orders (authenticated)
curl -s http://localhost:8080/orders -H "Authorization: Bearer $MACHINE" | jq .message

# Machine CANNOT access /admin (no admin role)
curl -s -w "\n%{http_code}" http://localhost:8080/admin/users -H "Authorization: Bearer $MACHINE" | tail -1
```

> **Same Resource Server, same rules.** User tokens and machine tokens both work. Roles decide access.

---

## Step 5: Read the Spring Boot Security Config

Open `resource-server/src/main/java/com/foodexpress/config/SecurityConfig.java`:

```java
.authorizeHttpRequests(auth -> auth
    .requestMatchers("/public/**").permitAll()         // no token needed
    .requestMatchers("/admin/**").hasRole("admin")     // admin role required
    .requestMatchers("/restaurant/**").hasAnyRole("restaurant-owner", "admin")
    .anyRequest().authenticated()                       // any valid token
)
.oauth2ResourceServer(oauth2 -> oauth2
    .jwt(jwt -> jwt.jwtAuthenticationConverter(...))    // extract roles from JWT
)
```

> **Key point:** Authorization rules are in ONE place. Resource Server reads roles from the JWT. No database lookup per request.

---

**Next:** [Lab 10 — Token Security](../lab-10-token-security/LAB.md)
