# Docker Part 3 -- Submission Checklist
## Module 26 | Day 29

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | All services reference correct network name (foodexpress-net) | [ ] |
| 2 | No port conflicts between services on host | [ ] |
| 3 | Order Service depends_on mysql-db and redis | [ ] |
| 4 | MySQL volume mounts to /var/lib/mysql | [ ] |
| 5 | MYSQL_ROOT_PASSWORD is set | [ ] |
| 6 | Restaurant Service is on foodexpress-net | [ ] |
| 7 | NGINX upstream uses port 8081 for Order Service | [ ] |
| 8 | Redis has restart policy | [ ] |
| 9 | Payment Service DB_HOST is mysql-db (not localhost) | [ ] |
| 10 | redis-data volume is declared in top-level volumes | [ ] |
| 11 | `docker compose up -d` starts all services without error | [ ] |
| 12 | All services show as "Up" in `docker compose ps` | [ ] |
| 13 | Services can reach each other by name (DNS resolution works) | [ ] |

---

## Self-Check Questions

1. **Why can't containers use `localhost` to reach each other?** Each container has its own network namespace. `localhost` refers to the container itself, not other containers.
2. **What is the difference between the default bridge and a user-defined bridge?** User-defined bridges provide automatic DNS resolution by container name. Default bridges only support IP-based communication.
3. **Does `ports: "8081:8081"` affect container-to-container communication?** No. The `ports` section maps container ports to host ports. Containers can always reach each other directly on any port within a shared network.
4. **What does `depends_on` actually guarantee?** Only startup ORDER, not readiness. The dependent service starts after the dependency, but the dependency may not be ready to accept connections yet.
5. **Why should redis-data be declared in the top-level `volumes` section?** Compose needs the volume declared to manage its lifecycle. Without it, Compose may refuse to start or create an anonymous volume.
6. **What happens to data in a named volume when you run `docker compose down`?** Data persists. Only `docker compose down -v` removes volumes.
7. **Why use `mysql-db` as DB_HOST instead of an IP address?** Container IPs can change on restart. DNS names are stable and resolved by Docker's embedded DNS.
8. **What is a 502 Bad Gateway from NGINX?** NGINX cannot connect to the upstream server. Usually means the upstream is down or the port is wrong.
9. **Why network isolation between frontend and backend?** If NGINX is compromised, the attacker can only reach services on the frontend network, not the database directly.
10. **When should you use `docker compose up --build`?** When you've changed Dockerfile or source code and need to rebuild images before starting containers.
