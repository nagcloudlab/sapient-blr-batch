# Docker Part 3 -- Trainer Solutions & Hints
## Module 26 | Day 29

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix docker-compose.yml | Network name mismatch, port conflict 8082, add depends_on, fix volume /var/lib/mysql, add MYSQL_ROOT_PASSWORD, add restaurant to network, fix DB_HOST localhost->mysql-db, add redis-data volume, restart policy, fix nginx port | Students fix the port conflict but forget the network name mismatch. Also, they add depends_on but don't realize it doesn't wait for readiness | Ask: "If depends_on doesn't wait for MySQL to be ready, how do you handle it?" (healthcheck + condition) |
| 2 | Networking | docker network inspect, DNS resolution test, cross-network isolation | Students assume all Compose services can talk to each other regardless of network config | Ask: "Can nginx reach mysql-db directly?" (Only if on the same network) |
| 3 | nginx.conf | upstream blocks with correct ports, location routing, proxy_pass, error pages | Students confuse container port vs published host port in upstream config | Ask: "In NGINX upstream, do you use the host port or container port?" (Container port -- NGINX is inside Docker too) |

---

## docker-compose.yml Fix Details

| # | Bug | Buggy | Fixed | Why |
|---|-----|-------|-------|-----|
| 1 | Network name | `app-network` | `foodexpress-net` | Must match the defined network |
| 2 | Port conflict | `8082:8081` | `8081:8081` | 8082 is already used by payment-service |
| 3 | Missing depends_on | (none) | `depends_on: [mysql-db, redis]` | Start order matters |
| 4 | Volume path | `/data` | `/var/lib/mysql` | MySQL default data directory |
| 5 | Missing password | (none) | `MYSQL_ROOT_PASSWORD: secret` | MySQL requires it |
| 6 | Missing network | (no networks) | `networks: [foodexpress-net]` | Restaurant was isolated |
| 7 | NGINX port | `8080` | `8081` | Order Service listens on 8081 |
| 8 | Restart policy | (none) | `restart: unless-stopped` | Redis auto-restarts |
| 9 | DB_HOST | `localhost` | `mysql-db` | Container DNS name |
| 10 | Volume decl | (missing) | `redis-data:` | Must declare named volumes |

---

## Key Discussion Points

1. Why user-defined bridge over default bridge? (DNS resolution by container name)
2. What happens if you use `localhost` as DB_HOST inside a container? (Points to the container itself, not the MySQL container)
3. Why separate frontend/backend networks? (Defense in depth -- limit blast radius)
4. Why not use host network for everything? (No isolation, port conflicts, security risk)
5. When to use Compose vs Kubernetes? (Compose: single host, dev/small; K8s: multi-host, production scale)
