# Docker Part 2 -- Trainer Solutions & Hints
## Module 25 | Day 28

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Dockerfile | node:latest->node:18-alpine, COPY package*.json first, npm ci, EXPOSE 3000, add USER, exec form CMD, HEALTHCHECK | Students fix the tag but keep COPY order wrong. They copy all files, then npm ci -- losing cache benefit | Ask: "If you change one line of code, what layers should rebuild?" (Only the COPY . . and CMD layers) |
| 2 | Fix Volume Config | -v mysql-data:/var/lib/mysql, add MYSQL_ROOT_PASSWORD, --restart unless-stopped, mount init.sql to /docker-entrypoint-initdb.d/ | Students forget that /docker-entrypoint-initdb.d/ only runs on FIRST start (empty volume) | Ask: "If you already have data in the volume, will init.sql run again?" (No -- only on first initialization) |
| 3 | Multi-Stage Build | Two FROM stages, COPY --from=builder, final image ~200MB vs ~800MB | Students copy the entire target/ directory instead of just the JAR | Ask: "What's in the target/ directory besides the JAR?" (Test reports, classes, dependency JARs) |

---

## Key Discussion Points

1. Why `npm ci` over `npm install`? (ci = clean install from lock file, deterministic; install modifies lock file)
2. Why alpine images? (Smaller base ~7MB, but uses musl libc -- some packages may need rebuilding)
3. When NOT to use alpine? (When native dependencies need glibc, when debugging tools are needed)
4. Why does Docker layer order matter for build speed? (Changed layer invalidates all subsequent layers)
5. Named volumes vs bind mounts for databases? (Named volumes for production data, bind mounts for config/dev)

---

## Dockerfile Fix Details

| Bug | Buggy | Fixed | Why |
|-----|-------|-------|-----|
| Base tag | `FROM node:latest` | `FROM node:18-alpine` | Reproducible, smaller |
| COPY order | `COPY . .` before npm | `COPY package*.json ./` then `COPY . .` | Cache optimization |
| npm command | `npm install` | `npm ci --only=production` | Deterministic, no dev deps |
| EXPOSE | `EXPOSE 8080` | `EXPOSE 3000` | Correct port |
| User | (missing) | `RUN addgroup... USER appuser` | Security |
| CMD form | `CMD npm start` | `CMD ["node", "server.js"]` | Signal handling |
| HEALTHCHECK | (missing) | `HEALTHCHECK --interval=30s...` | Health monitoring |
| WORKDIR | (missing) | `WORKDIR /app` | Organized layout |

## Volume Fix Details

| Bug | Buggy | Fixed | Why |
|-----|-------|-------|-----|
| Mount path | `/data/mysql` | `/var/lib/mysql` | MySQL default data directory |
| Password | (missing) | `-e MYSQL_ROOT_PASSWORD=secret` | MySQL requires it |
| Restart | (missing) | `--restart unless-stopped` | Auto-restart |
| Init script | (missing) | `-v init.sql:/docker-entrypoint-initdb.d/` | Database setup |
