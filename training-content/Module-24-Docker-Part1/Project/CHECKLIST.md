# Docker Part 1 -- Submission Checklist
## Module 24 | Day 27

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Dockerfile: FROM uses Java 17 JRE image (not Python) | [ ] |
| 2 | Dockerfile: WORKDIR /app is set | [ ] |
| 3 | Dockerfile: COPY has correct JAR filename | [ ] |
| 4 | Dockerfile: EXPOSE 8081 (not 3000) | [ ] |
| 5 | Dockerfile: Non-root user created and set with USER | [ ] |
| 6 | Dockerfile: CMD uses exec form with correct path | [ ] |
| 7 | Dockerfile: HEALTHCHECK is defined | [ ] |
| 8 | Container builds successfully with docker build | [ ] |
| 9 | Container runs and health check passes | [ ] |
| 10 | Lab 2: NGINX container running on port 8080 | [ ] |
| 11 | Lab 2: Container inspected and IP found | [ ] |
| 12 | Lab 2: Cleanup commands executed | [ ] |
| 13 | Lab 2: Image size comparison completed | [ ] |

---

## Self-Check Questions

1. **What is the difference between a Docker image and a container?** An image is a read-only template (like a class); a container is a running instance (like an object).
2. **Why use alpine-based images?** Alpine images are ~5MB base vs ~80MB for Debian-based, resulting in smaller, faster-to-pull images.
3. **What does EXPOSE do?** It documents which port the container listens on. It does NOT actually publish the port -- that's done with `-p` flag.
4. **Why run as non-root in containers?** If a container is compromised, root in the container may escalate to root on the host. Non-root limits the blast radius.
5. **What is the difference between CMD and ENTRYPOINT?** CMD provides defaults that can be overridden at `docker run`. ENTRYPOINT sets a fixed command; CMD then provides default arguments.
6. **Why exec form `["java", "-jar"]` over shell form?** Exec form makes the process PID 1 in the container, so it receives SIGTERM for graceful shutdown. Shell form wraps in `/bin/sh -c` which doesn't forward signals.
7. **What does `docker image prune -a` do?** Removes all images that are not referenced by any container (running or stopped).
8. **How do containers share the host kernel?** Containers use Linux namespaces for isolation and cgroups for resource limits, but they all use the same host kernel. This is why Linux containers can't run on Windows without a Linux VM.
9. **What is a Docker layer?** Each instruction in a Dockerfile creates a layer. Layers are cached and reused. Only changed layers are rebuilt.
10. **Why not use `latest` tag in production?** `latest` is mutable -- it changes with each new push. Using specific version tags ensures reproducible deployments.
