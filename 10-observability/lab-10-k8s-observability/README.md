# Lab 10: Observability on Kubernetes
## 45 min | Prerequisite: Lab 08, Kubernetes knowledge

---

## What You'll Learn
- How Prometheus auto-discovers services on Kubernetes (no hardcoded targets!)
- Pod annotations that enable Prometheus scraping
- Installing a complete monitoring stack with one Helm command
- Kubernetes-specific metrics: pod restarts, CPU/memory per pod, ready status
- Pre-built Grafana dashboards for K8s
- Simulating pod failure and watching auto-recovery

## Why This Matters
In Docker Compose (Lab 07), you hardcoded targets: `targets: ['order-service:8080']`. In Kubernetes, pods are ephemeral -- they're created, destroyed, moved, and scaled constantly. You can't hardcode targets because IPs and pod names change. Prometheus must DISCOVER pods automatically. This is how production monitoring works at scale.

## New Terms

| Term | Meaning |
|------|---------|
| **Service discovery** | Prometheus automatically finds pods to scrape by querying the K8s API. When new pods appear or old ones die, Prometheus updates its target list automatically. |
| **Pod annotations** | Metadata you add to pod specs. `prometheus.io/scrape: "true"` tells Prometheus "hey, scrape me!" without touching any Prometheus config file. |
| **kube-prometheus-stack** | A Helm chart that installs Prometheus + Grafana + AlertManager + Node Exporter + kube-state-metrics. One command = full K8s observability. |
| **Helm** | A package manager for Kubernetes. Like `npm` for Node.js or `apt` for Ubuntu, but for K8s applications. |
| **Node Exporter** | An agent that runs on each K8s node and exposes host-level metrics: CPU, memory, disk, network of the underlying machine. |
| **kube-state-metrics** | A service that exposes Kubernetes OBJECT metrics: pod status, deployment replica count, job completion status. Not about resource usage -- about K8s state. |
| **CrashLoopBackOff** | A K8s state where a pod keeps crashing and restarting repeatedly. Detected via the `kube_pod_container_status_restarts_total` metric. |
| **Liveness probe** | A health check K8s runs periodically. If it fails, K8s KILLS and restarts the pod. |
| **Readiness probe** | A health check that determines if a pod is ready to receive traffic. If it fails, K8s stops sending traffic but doesn't kill the pod. |
| **HPA** | Horizontal Pod Autoscaler -- automatically scales the number of pods based on metrics (CPU, memory, or custom metrics from Prometheus). |

---

## Docker Compose vs Kubernetes Observability

| Docker Compose (Lab 07) | Kubernetes (Lab 10) |
|------------------------|---------------------|
| Hardcoded `targets: ['order-service:8080']` | Pod annotations: `prometheus.io/scrape: "true"` |
| `docker compose up` | `helm install` + `kubectl apply` |
| Fixed number of containers | Pods scale up/down, auto-restart on failure |
| Manual Grafana data source | Pre-provisioned by Helm chart |
| No infrastructure metrics | Node Exporter + kube-state-metrics included |
| No pre-built dashboards | 20+ K8s dashboards out of the box |

---

## Step 1: Understand pod annotations

Copy `k8s-manifests.yml` from this folder. The key element is the **pod annotations**:

```yaml
template:
  metadata:
    labels:
      app: order-service
    annotations:
      prometheus.io/scrape: "true"     # "Prometheus, please scrape me!"
      prometheus.io/port: "8080"       # On this port
      prometheus.io/path: "/metrics"   # At this path
```

> **How auto-discovery works:**
> 1. You deploy a pod with `prometheus.io/scrape: "true"`
> 2. Prometheus periodically queries K8s API: "give me all pods with this annotation"
> 3. Prometheus automatically starts scraping each discovered pod
> 4. When a pod dies or a new one is created, the target list updates automatically
> 5. **You never edit prometheus.yml again.**

> **Quick Question:** In Lab 03, you had to edit `prometheus.yml` every time you added a service. In a system with 200 microservices, would that approach work? (No -- that's why service discovery exists.)

The manifest also includes health probes:

```yaml
livenessProbe:       # K8s kills and restarts pod if this fails
  httpGet:
    path: /health
    port: 8080
readinessProbe:      # K8s stops sending traffic if this fails
  httpGet:
    path: /health
    port: 8080
```

---

## Step 2: Install the monitoring stack with Helm

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set grafana.adminPassword=admin123 \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

> **What this ONE command installs:**
>
> | Component | What it does |
> |-----------|-------------|
> | **Prometheus** | Metrics collection with K8s auto-discovery |
> | **Grafana** | Pre-loaded with 20+ K8s dashboards |
> | **AlertManager** | Alert routing (already configured) |
> | **Node Exporter** | Host-level metrics on every K8s node |
> | **kube-state-metrics** | K8s object metrics (pods, deployments, jobs) |

---

## Step 3: Deploy FoodExpress services

```bash
# Build images (if using minikube)
eval $(minikube docker-env)
cd ~/obs-labs/lab-08-multi-service-tracing
docker build -t foodexpress-microservices:v1 .

# Deploy to K8s
kubectl apply -f k8s-manifests.yml

# Verify pods are running
kubectl get pods       # 2 order-service, 2 payment-service, 1 notification-service
kubectl get svc        # Services with ClusterIP or LoadBalancer
```

---

## Step 4: Access Prometheus and Grafana

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090 &
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80 &
```

- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin / admin123)

---

## Step 5: Verify auto-discovery

Go to Prometheus -> **Status > Targets**

You should see your FoodExpress pods auto-discovered -- **without any prometheus.yml changes**:
- order-service (2 pods)
- payment-service (2 pods)
- notification-service (1 pod)

Plus built-in targets from kube-prometheus-stack:
- node-exporter (every K8s node)
- kube-state-metrics
- Various internal K8s components

Try these queries:
```promql
# Are all our services UP?
up{app=~"order-service|payment-service|notification-service"}

# Total request rate across all order-service pods (load-balanced)
sum(rate(http_requests_total{app="order-service"}[5m]))
```

> **Discussion:** You did NOT edit any prometheus.yml for these services. The annotations on the pods were enough. When a developer deploys a new service, they just add the annotation and Prometheus discovers it automatically.

---

## Step 6: Explore pre-built K8s dashboards

In Grafana: **Dashboards > Browse**, search "kubernetes":

| Dashboard | What it shows |
|-----------|-------------|
| Kubernetes / Compute Resources / Namespace | CPU + memory per namespace |
| Kubernetes / Compute Resources / Pod | CPU + memory per pod |
| Kubernetes / Networking / Namespace | Network traffic per namespace |
| Node Exporter / Nodes | Host: CPU, memory, disk, network |

> **Think About It:** All these dashboards came FREE with the Helm chart. In Docker Compose, you built dashboards manually. This is the power of the kube-prometheus-stack.

---

## Step 7: K8s-specific PromQL queries

```promql
# Pod restarts (detect CrashLoopBackOff)
rate(kube_pod_container_status_restarts_total{namespace="default"}[15m])

# Pod CPU usage
rate(container_cpu_usage_seconds_total{namespace="default", container!=""}[5m])

# Pod memory usage (working set = actual usage)
container_memory_working_set_bytes{namespace="default", container!=""}

# Pods NOT ready (stuck or failing readiness check)
kube_pod_status_ready{condition="false", namespace="default"}

# Current replicas vs desired
kube_deployment_status_replicas{namespace="default"}
kube_deployment_spec_replicas{namespace="default"}
```

---

## Step 8: Generate load

```bash
kubectl port-forward svc/order-service 8080:8080 &

for i in $(seq 1 200); do
  curl -s -X POST http://localhost:8080/api/orders > /dev/null
  sleep 0.05
done
```

Watch in Grafana's "Pod" dashboard: CPU and memory climbing across pods.

---

## Step 9: Simulate pod failure

```bash
# Kill a pod -- K8s auto-restarts it
kubectl delete pod -l app=order-service --wait=false
```

Watch the sequence:
1. **Prometheus:** `up{app="order-service"}` drops for killed pod
2. **K8s:** New pod created automatically (`kubectl get pods` shows new pod)
3. **Prometheus:** New pod discovered, target returns to UP
4. **Grafana:** Brief dip in request rate, then recovery

```promql
# Track restarts
increase(kube_pod_container_status_restarts_total{pod=~"order.*"}[5m])
```

> **Discussion:** In Docker Compose (Lab 07), `docker stop` killed the service and it stayed dead until you manually ran `docker start`. In K8s, the pod is recreated automatically. Prometheus detects both the failure AND the recovery. No human intervention needed.

---

## Cleanup

```bash
kubectl delete -f k8s-manifests.yml
helm uninstall monitoring -n monitoring
kubectl delete namespace monitoring
```

---

## Complete Lab Journey

| Lab | Pillar | What you learned | Platform |
|-----|--------|-----------------|----------|
| 01 | -- | The pain of running blind | Node.js |
| 02 | Metrics | Instrumented app with Counter, Gauge, Histogram | Node.js |
| 03 | Metrics | Prometheus scraping, PromQL: rate(), histogram_quantile() | Docker |
| 04 | Metrics | Grafana dashboards, Golden Signals, SLI/SLO/SLA | Docker |
| 05 | Logs | Structured JSON logging, requestId, log levels | Docker |
| 06 | Alerting | Alert rules, `for` duration, severity, alert fatigue | Docker |
| 07 | Full Stack | Docker Compose, provisioning, incident simulation | Docker Compose |
| 08 | Traces | Multi-service tracing, Trace ID propagation, bottleneck ID | Docker Compose |
| 08b | Traces (Production) | Jaeger + OpenTelemetry, trace waterfall, service dependency graph | Docker Compose |
| 09 | Review | 9 real-world config bugs (Prometheus + Grafana + Alerts) | Config files |
| 10 | Production | K8s service discovery, Helm, pod annotations, auto-recovery | Kubernetes |

---

## Discussion

1. What's the advantage of pod annotations over hardcoded Prometheus targets?
2. What does kube-prometheus-stack give you that you'd have to build manually?
3. How does K8s auto-restart change the way you think about service failures?
4. What would you add to this setup for a real production system? (Log aggregation with Loki/ELK, distributed tracing with Jaeger/Tempo, service mesh for automatic tracing)
