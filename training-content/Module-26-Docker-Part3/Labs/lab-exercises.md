# Docker Part 3 -- Lab Exercises
## Module 26 | Day 29

---

## Client Email

```
From: priya.sharma@foodexpress.in
To: sustain-engineering@team.com
Subject: Docker Compose Stack Broken -- Can't Deploy FoodExpress
Date: 2026-08-06

Team,

Our docker-compose.yml for the full FoodExpress stack is broken.
A developer made several changes and now nothing starts correctly.
Issues include:

1. Services can't find each other (networking)
2. Port conflicts between services
3. MySQL starts before the app is ready to connect
4. Missing volumes -- data gets lost on restart
5. Wrong network configuration

The compose file is in starter-code/. Fix all bugs and bring
the entire stack up with `docker compose up -d`.

-- Priya Sharma, DevOps Lead, FoodExpress
```

---

## Lab 1: Fix docker-compose.yml (10 bugs)

### Duration: 60 minutes | Points: 30

**File to fix:** `starter-code/docker-compose.yml`

### Bugs to Find and Fix

| # | Hint | What's Wrong | Impact |
|---|------|-------------|--------|
| 1 | Check network names | Order Service references `app-network` but network is defined as `foodexpress-net` | Service can't join network |
| 2 | Check Order Service port | Host port 8082 conflicts with Payment Service | "port already allocated" error |
| 3 | Check depends_on for Order Service | Missing dependency on `mysql-db` | Order Service starts before DB |
| 4 | Check MySQL volume mount | Volume mount path is `/data` not `/var/lib/mysql` | MySQL data not persisted correctly |
| 5 | Check MySQL environment | `MYSQL_ROOT_PASSWORD` is missing | MySQL refuses to start |
| 6 | Check Restaurant Service network | Not connected to any network | Isolated, can't reach other services |
| 7 | Check NGINX upstream port | NGINX config routes to port 8080 but Order Service is on 8081 | 502 Bad Gateway |
| 8 | Check Redis restart policy | No restart policy | Redis doesn't restart after crash |
| 9 | Check Payment Service environment | `DB_HOST` points to `localhost` instead of `mysql-db` | Connection refused |
| 10 | Check volume declarations | `redis-data` volume used but not declared in top-level `volumes` | Compose refuses to start |

### Verification Steps

```bash
# Start the stack
docker compose up -d

# Verify all services are running
docker compose ps

# Test service connectivity
docker compose exec order-service curl http://mysql-db:3306
docker compose exec order-service curl http://restaurant-service:3000/health
docker compose exec nginx curl http://order-service:8081/actuator/health

# Test from host
curl http://localhost:80
curl http://localhost:8081/actuator/health
curl http://localhost:3000/health
```

---

## Lab 2: Docker Networking Exploration (4 tasks)

### Duration: 20 minutes | Points: 10

### Task 1: Inspect the network
```bash
# List all Docker networks
# Inspect the foodexpress-net network
# Find the IP addresses of all containers on the network
```

### Task 2: Test DNS resolution
```bash
# Exec into the order-service container
# Ping mysql-db by name (does it resolve?)
# Ping restaurant-service by name
# Try pinging a container NOT on the same network
```

### Task 3: Network isolation test
```bash
# Create a second network: isolated-net
# Start a test container on isolated-net
# Try to reach order-service from the test container
# Expected: FAIL (different networks)
```

### Task 4: Port vs container communication
```bash
# From inside order-service, can you reach mysql-db:3306?
# From the host, can you reach mysql-db:3306?
# What's the difference?
```

---

## Lab 3: Write nginx.conf for Reverse Proxy (Bonus)

### Duration: 20 minutes | Points: 10

Write an NGINX configuration that:
- Routes `/api/orders/*` to `order-service:8081`
- Routes `/api/restaurants/*` to `restaurant-service:3000`
- Routes `/api/payments/*` to `payment-service:8082`
- Serves static files at `/`
- Returns proper error pages for 502/504

---

## Scoring

| Task | Points |
|------|--------|
| Lab 1: Fix docker-compose.yml (10 bugs) | 30 |
| Lab 2: Networking exploration (4 tasks) | 10 |
| Lab 3: Bonus nginx.conf | 10 |
| **Total** | **50** |
