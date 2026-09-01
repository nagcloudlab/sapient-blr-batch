# Kubernetes -- Submission Checklist
## Module 29 | Day 32

---

## Submission Checklist

| # | Item | Done? |
|---|------|-------|
| 1 | Order Deployment: liveness probe path `/actuator/health` | [ ] |
| 2 | Order Deployment: containerPort set to 8080 | [ ] |
| 3 | Order Deployment: resource requests (cpu: 250m, memory: 256Mi) | [ ] |
| 4 | Order Deployment: resource limits (cpu: 500m, memory: 512Mi) | [ ] |
| 5 | Order Deployment: initialDelaySeconds >= 30 | [ ] |
| 6 | Order Service: selector `app: order-service` matches pod label | [ ] |
| 7 | Order Service: targetPort is 8080 | [ ] |
| 8 | Order Service: nodePort in valid range (30000-32767) | [ ] |
| 9 | Payment Deployment: specific image tag (not `latest`) | [ ] |
| 10 | Payment Deployment: imagePullPolicy is `IfNotPresent` or `Always` | [ ] |
| 11 | Payment Deployment: readiness probe added | [ ] |
| 12 | Payment Deployment: DB_PASSWORD uses secretKeyRef | [ ] |
| 13 | Namespace: ResourceQuota has realistic limits (>= 4 CPU) | [ ] |
| 14 | Namespace: LimitRange default >= defaultRequest | [ ] |
| 15 | HPA manifest created with correct scaleTargetRef | [ ] |

---

## Self-Check Questions

1. **Why not use `latest` tag?** The same tag can point to different images at different times, making deployments non-deterministic and rollbacks impossible.
2. **What is CrashLoopBackOff?** The container crashes repeatedly; K8s backs off restart attempts with exponential delay (10s, 20s, 40s...).
3. **Why does the selector label matter?** Services find pods via label selectors. If labels don't match, the Service has zero endpoints and no traffic flows.
4. **Why set resource limits?** Without limits, a single pod can consume all node resources (noisy neighbor), starving other pods.
