# Kubernetes -- Lab Exercises
## Module 29 | Day 32

---

## Client Email

```
From: vikram.shah@foodexpress.in
To: sustain-engineering@team.com
Subject: Kubernetes Deployment Issues -- URGENT
Date: 2026-09-05

Team,

Our FoodExpress microservices deployment on Kubernetes has
several critical issues:

1. The order-service keeps going into CrashLoopBackOff
2. The payment-service is unreachable from other services
3. We have no health checks -- dead pods still receive traffic
4. During the lunch rush, the cluster ran out of resources
   because no limits were set

Please fix the K8s manifests and get our services healthy.

-- Vikram Shah, Platform Engineering Lead, FoodExpress
```

---

## Lab 1: Fix the Order Service Deployment (4 bugs)

### File: `starter-code/order-deployment.yaml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The liveness probe path does not match the actual health endpoint exposed by the Spring Boot app | Liveness probe fails every time, K8s restarts the pod endlessly (CrashLoopBackOff) |
| 2 | The container port declared in the manifest does not match the port the application actually listens on | Traffic never reaches the app; connection refused errors |
| 3 | There are no resource requests or limits defined on the container | Pod can consume unlimited resources; scheduler cannot make informed decisions; noisy neighbor problem |
| 4 | The `initialDelaySeconds` for the liveness probe is too short for a Spring Boot app that takes 20-30 seconds to start | Pod is killed before it finishes starting, creating a permanent CrashLoopBackOff |

### Verification
- `kubectl apply -f order-deployment.yaml` -- no errors
- `kubectl get pods` -- order-service pods in Running state (not CrashLoopBackOff)
- `kubectl describe pod <order-pod>` -- liveness probe succeeds

---

## Lab 2: Fix the Order Service (Networking) (3 bugs)

### File: `starter-code/order-service.yaml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The Service selector label does not match the pod labels defined in the Deployment | Service has zero endpoints; no traffic reaches the pods |
| 2 | The `targetPort` does not match the container port in the Deployment | Even if selector matches, traffic goes to the wrong port |
| 3 | The Service type is `NodePort` but the nodePort value is outside the valid range (30000-32767) | Service creation fails with validation error |

### Verification
- `kubectl apply -f order-service.yaml` -- no errors
- `kubectl get endpoints order-service` -- should show pod IPs
- `curl http://<node-ip>:<nodePort>/actuator/health` -- returns 200

---

## Lab 3: Fix the Payment Service Deployment (3 bugs)

### File: `starter-code/payment-deployment.yaml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The image tag is set to `latest` and `imagePullPolicy` is `Never` | In a cluster without the local image, pods are stuck in ImagePullBackOff; even if available, `latest` is non-deterministic |
| 2 | The readiness probe is missing entirely | Pods receive traffic before the application is ready; customers see 503 errors during deployments |
| 3 | The environment variable for the database password is hardcoded in plain text instead of referencing a Secret | Security violation; password visible in `kubectl describe pod` and in source control |

### Verification
- `kubectl apply -f payment-deployment.yaml` -- no errors
- `kubectl get pods` -- payment pods Running and Ready (1/1)
- `kubectl describe pod <payment-pod>` -- no plaintext password visible

---

## Lab 4: Fix the Namespace & Resource Quota (2 bugs)

### File: `starter-code/namespace-config.yaml`

| # | Hint | Impact |
|---|------|--------|
| 1 | The ResourceQuota `hard` limits are unrealistically low (e.g., 100m CPU total for a namespace running 6 services) | New pods cannot be scheduled; `kubectl get events` shows "exceeded quota" |
| 2 | The LimitRange `default` and `defaultRequest` are inverted -- limits are lower than requests | Every pod creation fails with validation error: "limit must be >= request" |

### Verification
- `kubectl apply -f namespace-config.yaml` -- no errors
- `kubectl describe resourcequota -n foodexpress-prod` -- reasonable limits
- New pods in the namespace can be scheduled without quota errors

---

## Bonus Challenges

1. **Create an HPA** for order-service that scales between 2 and 8 replicas at 70% CPU utilization
2. **Add a Network Policy** that only allows order-service to talk to payment-service (deny all other ingress)
3. **Write a PodDisruptionBudget** for order-service ensuring at least 2 pods are always available during node maintenance

---

## Summary

| Lab | Files | Bugs | Focus Area |
|-----|-------|------|------------|
| 1 | order-deployment.yaml | 4 | Probes, ports, resources, startup timing |
| 2 | order-service.yaml | 3 | Selectors, targetPort, NodePort range |
| 3 | payment-deployment.yaml | 3 | Image policy, readiness, secrets |
| 4 | namespace-config.yaml | 2 | ResourceQuota, LimitRange |
| **Total** | **4 files** | **12 bugs** | |
