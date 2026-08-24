# Kubernetes -- Trainer Solutions & Hints
## Module 29 | Day 32

---

## Solution & Hints Table

| # | Task | Key Fix | Common Pitfalls | Trainer Hint |
|---|------|---------|-----------------|--------------|
| 1 | Fix Order Deployment | Probe path `/actuator/health`, port 8080, add resources block, initialDelaySeconds 30 | Students fix the probe path but forget to also fix the containerPort. Both must be consistent | Ask: "What happens if your probe checks port 8080 but your container declares port 3000?" |
| 2 | Fix Order Service | Selector `app: order-service`, targetPort 8080, nodePort 30080 | Students change the selector but create a new label instead of matching the existing pod label. Emphasize: Service finds pods via labels | Ask: "How do you check if a Service actually found any pods?" (`kubectl get endpoints`) |
| 3 | Fix Payment Deployment | Specific image tag `1.2.0`, imagePullPolicy `IfNotPresent`, add readinessProbe, use secretKeyRef for password | Students add readiness probe but copy the liveness probe exactly. Readiness should have shorter delay and period | Ask: "What is the difference between liveness and readiness? What happens if each fails?" |
| 4 | Fix Namespace Config | Quota: 4 CPU / 4Gi memory requests; LimitRange: default limits >= defaultRequest | Students set very high quotas (100 CPU). Guide them to calculate: 6 services x avg 500m = 3 CPU minimum | Ask: "If each service needs 250m CPU request and you have 6 services with 3 replicas each, what is your minimum CPU quota?" |
| 5 | Design HPA | minReplicas 2, maxReplicas 8, target CPU 70%, scaleTargetRef to order-service Deployment | Students forget that HPA requires Metrics Server to be installed | Ask: "What happens to HPA if Metrics Server is not running?" |
| 6 | Network Policy | Default deny all ingress, then allow order-service -> payment-service on port 8080 | Students create an allow rule but forget the default deny. Without default deny, all traffic is allowed | Ask: "If you only create an allow rule without a default deny, what changes?" |

---

## Key Discussion Points

1. Why is `latest` tag dangerous in production? (Non-deterministic; same tag can point to different images)
2. What is the difference between liveness and readiness probes? When would you want a pod to fail liveness but pass readiness?
3. Why are resource requests and limits both needed? What happens if you set only one?
4. When should you use ClusterIP vs NodePort vs LoadBalancer?
5. How does Kubernetes achieve self-healing? (Controller loop: desired state vs actual state)
6. What is a PodDisruptionBudget and why is it important for sustain engineering?
