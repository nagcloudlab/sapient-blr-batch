# Docker Part 2 -- Submission Checklist
## Module 25 | Day 28

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Dockerfile: Uses specific Node.js version tag (not latest) | [ ] |
| 2 | Dockerfile: WORKDIR is set | [ ] |
| 3 | Dockerfile: package.json copied BEFORE npm ci | [ ] |
| 4 | Dockerfile: Uses npm ci (not npm install) | [ ] |
| 5 | Dockerfile: Source code copied AFTER npm ci | [ ] |
| 6 | Dockerfile: EXPOSE 3000 | [ ] |
| 7 | Dockerfile: Non-root user created and set | [ ] |
| 8 | Dockerfile: CMD uses exec form | [ ] |
| 9 | Dockerfile: HEALTHCHECK defined | [ ] |
| 10 | MySQL: Volume mounts to /var/lib/mysql | [ ] |
| 11 | MySQL: MYSQL_ROOT_PASSWORD set | [ ] |
| 12 | MySQL: Restart policy configured | [ ] |
| 13 | MySQL: Init SQL script mounted | [ ] |
| 14 | MySQL: Data persists after container removal | [ ] |

---

## Self-Check Questions

1. **Why copy package.json before source code?** If only source code changes, npm ci is cached from the previous build, saving 30-120 seconds.
2. **What is the difference between npm install and npm ci?** `npm ci` does a clean install from package-lock.json exactly; `npm install` can modify the lock file.
3. **Why use alpine images?** Alpine is ~7MB vs ~80MB for Debian-based, resulting in smaller images and less attack surface.
4. **Where does MySQL store data by default?** `/var/lib/mysql` -- this is what you must mount a volume to.
5. **What is `/docker-entrypoint-initdb.d/`?** MySQL's official image runs any `.sql` or `.sh` files in this directory on first startup when the data directory is empty.
6. **Why `--restart unless-stopped`?** The container restarts automatically after crashes or host reboots, UNLESS you explicitly `docker stop` it.
7. **What does `docker volume prune` do?** Removes ALL volumes not attached to a running container. Be careful -- it can delete database data!
8. **Why exec form CMD over shell form?** Exec form makes your process PID 1, so it receives SIGTERM for graceful shutdown. Shell form wraps in `/bin/sh -c`.
9. **What is a Docker layer?** Each instruction in a Dockerfile creates a read-only layer. Layers are cached and shared between images.
10. **Why is running as root in containers dangerous?** A container escape vulnerability combined with root access could give an attacker root on the host machine.
