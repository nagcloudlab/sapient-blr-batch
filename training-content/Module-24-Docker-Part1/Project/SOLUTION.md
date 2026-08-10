# Docker Part 1 -- Trainer Solutions & Hints
## Module 24 | Day 27

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Dockerfile | FROM python->temurin:17-jre-alpine, add WORKDIR /app, fix COPY filename, EXPOSE 8081, add USER, fix CMD exec form, add HEALTHCHECK | Students fix FROM but forget to change CMD path. They also confuse EXPOSE with port publishing | Ask: "Does EXPOSE actually open a port?" (No -- it's documentation. -p flag does the mapping.) |
| 2 | Docker Commands | docker run -d --name fe-nginx -p 8080:80 nginx:1.25; docker inspect; docker logs; docker stop/rm; docker image prune | Students try to curl between containers by name without a shared network | Ask: "Can two containers talk to each other by name by default?" (No -- they need a shared Docker network) |
| 3 | Bonus: Static Page | FROM nginx:1.25-alpine; COPY index.html /usr/share/nginx/html/; EXPOSE 80; HEALTHCHECK | Students forget the full path for nginx html directory | Ask: "Where does nginx serve files from by default?" (/usr/share/nginx/html/) |

---

## Key Discussion Points

1. Why alpine-based images? (~5MB base vs ~80MB for debian-based)
2. Why JRE not JDK in production? (JDK includes compiler, debugger -- not needed at runtime)
3. Why non-root user? (Container escape vulnerability -- root in container may = root on host)
4. What's the difference between CMD and ENTRYPOINT? (CMD = default, can be overridden; ENTRYPOINT = fixed command)
5. Why exec form `["java", "-jar"]` over shell form `java -jar`? (Exec form gets PID 1, receives signals correctly)

---

## Dockerfile Fix Details

| Bug | Buggy | Fixed | Why |
|-----|-------|-------|-----|
| Base image | `FROM python:3.11-slim` | `FROM eclipse-temurin:17-jre-alpine` | Need JVM, not Python |
| WORKDIR | (missing) | `WORKDIR /app` | Organized layout |
| COPY | `COPY target/app.jar /application.jar` | `COPY target/order-service-1.0.0.jar app.jar` | Correct filename |
| EXPOSE | `EXPOSE 3000` | `EXPOSE 8081` | Correct port |
| USER | (missing) | `RUN addgroup... && adduser...` + `USER appuser` | Security |
| CMD | `CMD java -jar /wrong-path/service.jar` | `CMD ["java", "-Xmx512m", "-jar", "app.jar"]` | Correct path + exec form |
| HEALTHCHECK | (missing) | `HEALTHCHECK --interval=30s...` | Orchestrator monitoring |

---

## Lab 2 Command Answers

```bash
# Task 1
docker pull nginx:1.25
docker run -d --name fe-nginx -p 8080:80 nginx:1.25
curl http://localhost:8080

# Task 2
docker ps
docker inspect fe-nginx | grep IPAddress
docker logs --tail 20 fe-nginx

# Task 3
docker run -it ubuntu:22.04 /bin/bash
apt-get update && apt-get install -y curl
curl http://fe-nginx  # Fails -- not on same network
exit

# Task 4
docker stop $(docker ps -q)
docker rm $(docker ps -aq)
docker image prune -a
docker ps -a
docker images

# Task 5
docker pull eclipse-temurin:17-jre-alpine
docker pull eclipse-temurin:17-jre
docker images | grep temurin
docker history eclipse-temurin:17-jre-alpine
# Alpine: ~190MB vs non-alpine: ~270MB
```
