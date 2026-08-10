# Docker Part 3 -- Project Brief
## Module 26 | Day 29

---

## Sustain Context

FoodExpress is deploying its full microservices stack using Docker Compose. The docker-compose.yml file has multiple networking, port, volume, and dependency configuration bugs that prevent the stack from starting. As a sustain engineer, you need to debug and fix the entire Compose configuration.

---

## Task Table

| # | Task | Description | Duration | Points |
|---|------|-------------|----------|--------|
| 1 | Fix docker-compose.yml | Fix 10 bugs: network names, port conflicts, depends_on, volumes, env vars, restart policy | 60 min | 30 |
| 2 | Networking Exploration | Inspect networks, test DNS, verify isolation, understand port mapping | 20 min | 10 |
| 3 | Bonus: nginx.conf | Write reverse proxy config routing to all services | 20 min | 10 |

**Total Points Available:** 50

---

## Deliverables

1. Fixed `docker-compose.yml` with all 10 bugs resolved
2. Full stack running with `docker compose up -d`
3. All services communicating correctly (verified with curl)
4. Network inspection output showing container IPs and DNS resolution
5. (Bonus) Working nginx.conf with proper routing
