# Kubernetes
## Module 29 | Sustain Engineering Training | Day 32

---

## Agenda -- Day 32

| # | Topic |
|---|-------|
| 01 | Why Container Orchestration? |
| 02 | Kubernetes Architecture Deep Dive |
| 03 | Pods, ReplicaSets, and Deployments |
| 04 | Services & Pod Connectivity |
| 05 | ConfigMaps, Secrets & Namespaces |
| 06 | Health Checks & Self-Healing |
| 07 | Resource Management & Scaling |
| 08 | Lab: Fix FoodExpress K8s Manifests |
| 09 | Monitoring & Troubleshooting |
| 10 | Day 32 Wrap-up |

---

## Why Container Orchestration?

### The Problem with Running Containers Manually

```
FoodExpress: 6 microservices x 3 replicas = 18 containers

Manual management headaches:
  - Which host runs which container?
  - What if a container crashes at 3 AM?
  - How to roll out a new version without downtime?
  - How to scale order-service during Diwali rush?
  - How do containers find each other?
```

Container orchestration automates deployment, scaling, networking, and self-healing across a cluster of machines.

---

## Container Orchestration Landscape

| Tool | Description | Use Case |
|------|-------------|----------|
| **Kubernetes (K8s)** | Industry standard, CNCF graduated | Production workloads |
| Docker Swarm | Built into Docker Engine | Simple setups |
| Amazon ECS | AWS-native orchestrator | AWS-only shops |
| Nomad | HashiCorp, multi-workload | Mixed container/VM |
| OpenShift | Red Hat's K8s distribution | Enterprise K8s |

**Kubernetes won** -- 92% of organizations use K8s for container orchestration (CNCF Survey 2024).

---

## What is Kubernetes?

### Open-source container orchestration platform

- Originally designed by Google (based on Borg)
- Donated to CNCF in 2014
- Written in Go

### Core capabilities:
1. **Service discovery & load balancing** -- containers find each other
2. **Storage orchestration** -- mount volumes automatically
3. **Automated rollouts & rollbacks** -- declarative updates
4. **Self-healing** -- restart crashed containers automatically
5. **Secret & configuration management** -- decouple config from code
6. **Horizontal scaling** -- add/remove pods based on load

---

## Kubernetes Architecture Overview

<!--VISUAL:k8s-architecture-->

```
┌──────────────────────────────────────────────────────────┐
│                    CONTROL PLANE                         │
│                                                          │
│  ┌────────────┐  ┌───────────┐  ┌────────────────────┐  │
│  │ API Server │  │ Scheduler │  │ Controller Manager  │  │
│  │  (kube-    │  │           │  │  - ReplicaSet ctrl  │  │
│  │  apiserver)│  │           │  │  - Deployment ctrl  │  │
│  └─────┬──────┘  └───────────┘  │  - Node ctrl        │  │
│        │                        └────────────────────┘  │
│  ┌─────▼──────┐                                         │
│  │   etcd     │  (Cluster state store)                  │
│  └────────────┘                                         │
├──────────────────────────────────────────────────────────┤
│                    DATA PLANE (Worker Nodes)             │
│                                                          │
│  ┌─────────────────┐   ┌─────────────────┐              │
│  │   Worker Node 1 │   │   Worker Node 2 │              │
│  │  ┌───────────┐  │   │  ┌───────────┐  │              │
│  │  │  kubelet  │  │   │  │  kubelet  │  │              │
│  │  ├───────────┤  │   │  ├───────────┤  │              │
│  │  │kube-proxy │  │   │  │kube-proxy │  │              │
│  │  ├───────────┤  │   │  ├───────────┤  │              │
│  │  │ Container │  │   │  │ Container │  │              │
│  │  │ Runtime   │  │   │  │ Runtime   │  │              │
│  │  └───────────┘  │   │  └───────────┘  │              │
│  └─────────────────┘   └─────────────────┘              │
└──────────────────────────────────────────────────────────┘
```

---

## Control Plane Components

| Component | Role | FoodExpress Analogy |
|-----------|------|---------------------|
| **kube-apiserver** | Front door to the cluster; all commands go through it | Restaurant reception -- all orders go through it |
| **etcd** | Distributed key-value store; holds cluster state | The order ledger -- source of truth |
| **kube-scheduler** | Assigns pods to nodes based on resources | Kitchen manager assigning dishes to chefs |
| **controller-manager** | Runs control loops (desired state vs actual state) | Quality supervisor checking every dish matches the order |
| **cloud-controller-manager** | Integrates with cloud provider APIs | The franchise HQ connecting to cloud kitchens |

> The control plane ensures the **desired state** (what you declared) matches the **actual state** (what is running).

---

## Data Plane Components

### Every Worker Node runs:

| Component | Role |
|-----------|------|
| **kubelet** | Agent on each node; ensures pods are running as declared |
| **kube-proxy** | Manages network rules; enables Service abstraction |
| **Container Runtime** | Runs containers (containerd, CRI-O) |

```
API Server says: "Run 3 replicas of order-service"

kubelet on Node 1: "I'll run replica 1" ✓
kubelet on Node 2: "I'll run replica 2" ✓
kubelet on Node 3: "I'll run replica 3" ✓
```

The kubelet watches the API server and ensures its node runs the assigned pods.

---

## Management Plane: kubectl

### The CLI for interacting with Kubernetes

```bash
# Get cluster info
kubectl cluster-info

# List all pods
kubectl get pods

# Describe a specific pod
kubectl describe pod order-service-7d4b8c6f5-x2k9j

# Apply a manifest
kubectl apply -f deployment.yaml

# View logs
kubectl logs order-service-7d4b8c6f5-x2k9j

# Execute into a running pod
kubectl exec -it order-service-7d4b8c6f5-x2k9j -- /bin/sh
```

**Key pattern:** `kubectl <verb> <resource> [name] [flags]`

---

## Pods: The Smallest Deployable Unit

### A pod wraps one or more containers

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: order-service
  labels:
    app: foodexpress
    tier: backend
    service: order
spec:
  containers:
    - name: order-service
      image: foodexpress/order-service:1.2.0
      ports:
        - containerPort: 8080
```

### Key facts:
- Pods share network namespace (localhost communication)
- Pods share storage volumes
- Pods are **ephemeral** -- they can be killed and recreated
- Never create bare pods; use Deployments

---

## Pod Lifecycle

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌────────────┐
│ Pending │───>│ Running │───>│Succeeded│ or │   Failed   │
└─────────┘    └─────────┘    └─────────┘    └────────────┘
     │              │
     │              ▼
     │         ┌─────────┐
     │         │CrashLoop│
     │         │BackOff  │
     │         └─────────┘
     │
     ▼
┌──────────┐
│  Unknown │  (Node lost contact)
└──────────┘
```

| Phase | Meaning |
|-------|---------|
| Pending | Accepted but not yet running (image pull, scheduling) |
| Running | At least one container is running |
| Succeeded | All containers terminated successfully |
| Failed | At least one container failed |
| CrashLoopBackOff | Container keeps crashing, K8s backs off restarts |

---

## Deployments & ReplicaSets

### Deployment manages ReplicaSet manages Pods

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: order-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: order-service
  template:
    metadata:
      labels:
        app: order-service
    spec:
      containers:
        - name: order-service
          image: foodexpress/order-service:1.2.0
          resources:
            requests:
              cpu: "250m"
              memory: "256Mi"
            limits:
              cpu: "500m"
              memory: "512Mi"
```

Deployment ensures exactly 3 pods are always running. If one crashes, a new one is created.

---

## Rolling Updates & Rollbacks

### Zero-downtime deployments

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1        # 1 extra pod during update
      maxUnavailable: 0   # Never go below desired count
```

```
Update from v1.2.0 to v1.3.0:

Step 1:  v1.2 v1.2 v1.2 v1.3    (maxSurge=1: create 1 new)
Step 2:  v1.2 v1.2 v1.3 v1.3    (terminate 1 old, create 1 new)
Step 3:  v1.2 v1.3 v1.3 v1.3    (terminate 1 old, create 1 new)
Step 4:  v1.3 v1.3 v1.3         (terminate last old)
```

```bash
# Rollback to previous version
kubectl rollout undo deployment/order-service

# Check rollout status
kubectl rollout status deployment/order-service
```

---

## Services: Pod Connectivity

### The problem: Pods have ephemeral IPs

```
Pod order-service-abc  IP: 10.244.1.5  → dies
Pod order-service-xyz  IP: 10.244.2.9  → new pod, new IP!
```

A **Service** provides a stable virtual IP and DNS name for a set of pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: order-service
spec:
  selector:
    app: order-service    # Finds pods with this label
  ports:
    - port: 80            # Service port
      targetPort: 8080    # Container port
  type: ClusterIP
```

Other pods access it via: `http://order-service:80`

---

## Service Types

```
┌─────────────────────────────────────────────────────────┐
│                    EXTERNAL TRAFFIC                      │
│                         │                                │
│              ┌──────────▼──────────┐                    │
│              │    LoadBalancer     │  Cloud LB           │
│              │   (External IP)    │                      │
│              └──────────┬──────────┘                    │
│              ┌──────────▼──────────┐                    │
│              │      NodePort      │  Port on every node  │
│              │  (30000-32767)     │                      │
│              └──────────┬──────────┘                    │
│              ┌──────────▼──────────┐                    │
│              │     ClusterIP      │  Internal only       │
│              │  (default type)    │                      │
│              └──────────┬──────────┘                    │
│                    ┌────▼────┐                           │
│                    │  Pods   │                           │
│                    └─────────┘                           │
└─────────────────────────────────────────────────────────┘
```

| Type | Use Case | FoodExpress Example |
|------|----------|---------------------|
| **ClusterIP** | Internal service-to-service | order-service -> payment-service |
| **NodePort** | Dev/test external access | Testing on Minikube |
| **LoadBalancer** | Production external access | Customer-facing API gateway |

---

## Endpoints: How Services Find Pods

### Endpoints are the bridge between Services and Pods

```bash
$ kubectl get endpoints order-service
NAME            ENDPOINTS                                      AGE
order-service   10.244.1.5:8080,10.244.2.9:8080,10.244.3.2:8080   5m
```

```
Service (order-service:80)
    │
    ├──> Endpoint 10.244.1.5:8080 (Pod 1)
    ├──> Endpoint 10.244.2.9:8080 (Pod 2)
    └──> Endpoint 10.244.3.2:8080 (Pod 3)
```

- Endpoints are auto-managed by the Endpoints Controller
- When a pod matches the Service selector AND passes readiness checks, it gets added
- When a pod fails readiness checks, it is removed from endpoints (no traffic sent)

---

## ConfigMaps & Secrets

### Decouple configuration from container images

```yaml
# ConfigMap for FoodExpress
apiVersion: v1
kind: ConfigMap
metadata:
  name: foodexpress-config
data:
  DATABASE_HOST: "mysql-service"
  DATABASE_PORT: "3306"
  LOG_LEVEL: "info"
  MAX_ORDER_ITEMS: "50"
```

```yaml
# Secret for sensitive data
apiVersion: v1
kind: Secret
metadata:
  name: foodexpress-secrets
type: Opaque
data:
  DB_PASSWORD: cGFzc3dvcmQxMjM=      # base64 encoded
  JWT_SECRET: bXlTZWNyZXRLZXkxMjM=   # base64 encoded
```

> Secrets are base64 encoded, NOT encrypted by default. Use external secret managers (Vault, AWS Secrets Manager) in production.

---

## Namespaces: Virtual Clusters

### Isolate environments within a single cluster

```bash
$ kubectl get namespaces
NAME              STATUS   AGE
default           Active   30d
kube-system       Active   30d
foodexpress-dev   Active   15d
foodexpress-stg   Active   15d
foodexpress-prod  Active   15d
```

```
┌── Cluster ───────────────────────────────────────┐
│                                                    │
│  ┌─ foodexpress-dev ──┐  ┌─ foodexpress-prod ──┐  │
│  │  order-service     │  │  order-service      │  │
│  │  menu-service      │  │  menu-service       │  │
│  │  (relaxed limits)  │  │  (strict limits)    │  │
│  └────────────────────┘  └─────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

Use namespaces for: environment isolation, team separation, resource quotas.

---

## Health Checks: Probes

### Kubernetes checks if your app is healthy

| Probe | Purpose | What happens if it fails |
|-------|---------|-------------------------|
| **Liveness** | Is the container alive? | Container is restarted |
| **Readiness** | Is the container ready to serve traffic? | Removed from Service endpoints |
| **Startup** | Has the container started? | Liveness/readiness probes are disabled until it passes |

```yaml
containers:
  - name: order-service
    livenessProbe:
      httpGet:
        path: /actuator/health
        port: 8080
      initialDelaySeconds: 30
      periodSeconds: 10
      failureThreshold: 3
    readinessProbe:
      httpGet:
        path: /actuator/health/readiness
        port: 8080
      initialDelaySeconds: 5
      periodSeconds: 5
```

---

## Probe Types

### Three ways to check container health

```yaml
# HTTP GET probe (most common for web services)
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080

# TCP Socket probe (for non-HTTP services)
livenessProbe:
  tcpSocket:
    port: 3306

# Command probe (run a script inside the container)
livenessProbe:
  exec:
    command:
      - cat
      - /tmp/healthy
```

**FoodExpress pattern:** All microservices expose `/actuator/health` (Spring Boot) or `/healthz` (Node.js).

---

## Resource Management

### Requests vs Limits

```yaml
resources:
  requests:          # Minimum guaranteed
    cpu: "250m"      # 250 millicores = 0.25 CPU
    memory: "256Mi"  # 256 MiB
  limits:            # Maximum allowed
    cpu: "500m"      # 500 millicores = 0.5 CPU
    memory: "512Mi"  # 512 MiB
```

| Concept | Purpose | What happens |
|---------|---------|-------------|
| **Request** | Scheduling guarantee | Scheduler places pod on a node with enough capacity |
| **Limit** | Hard cap | CPU: throttled. Memory: OOMKilled |

```
FoodExpress resource planning:

order-service:   req 250m/256Mi, lim 500m/512Mi  (medium)
menu-service:    req 100m/128Mi, lim 250m/256Mi  (light)
payment-service: req 250m/256Mi, lim 500m/512Mi  (medium)
delivery-service:req 100m/128Mi, lim 250m/256Mi  (light)
```

---

## Horizontal Pod Autoscaler (HPA)

### Scale pods based on metrics

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
```

```
Normal day:    2 pods  (min)
Lunch rush:    5 pods  (CPU > 70%)
Diwali sale:  10 pods  (max)
Late night:    2 pods  (scales back down)
```

---

## Scaling Strategies

| Strategy | How | When |
|----------|-----|------|
| **HPA** | Add more pods | CPU/memory pressure |
| **VPA** | Increase pod resources | Right-sizing containers |
| **Cluster Autoscaler** | Add more nodes | No room for new pods |
| **KEDA** | Event-driven scaling | Queue depth, custom metrics |

```
FoodExpress Diwali scaling scenario:

1. Order flood arrives
2. HPA: 2 pods → 10 pods (CPU > 70%)
3. Nodes full → Cluster Autoscaler adds 2 nodes
4. KEDA: Scale notification-service based on message queue depth
5. After rush: scale down (cooldown period)
```

---

## Kubernetes Networking Model

### Every pod gets its own IP address

```
┌── Cluster Network (10.244.0.0/16) ──────────────────┐
│                                                       │
│  Node 1 (10.244.1.0/24)    Node 2 (10.244.2.0/24)  │
│  ┌──────────────────┐      ┌──────────────────┐      │
│  │ Pod A: 10.244.1.5│─────>│ Pod C: 10.244.2.3│      │
│  │ Pod B: 10.244.1.6│      │ Pod D: 10.244.2.4│      │
│  └──────────────────┘      └──────────────────┘      │
│                                                       │
│  Rules:                                               │
│  1. Every pod can reach every other pod (no NAT)     │
│  2. Agents on a node can reach all pods on that node │
│  3. Pods see their own IP (no surprises)             │
└───────────────────────────────────────────────────────┘
```

CNI plugins (Calico, Flannel, Cilium) implement this network model.

---

## Ingress: HTTP Routing

### Route external HTTP traffic to Services

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: foodexpress-ingress
spec:
  rules:
    - host: api.foodexpress.in
      http:
        paths:
          - path: /api/v1/menu
            pathType: Prefix
            backend:
              service:
                name: menu-service
                port:
                  number: 80
          - path: /api/v1/orders
            pathType: Prefix
            backend:
              service:
                name: order-service
                port:
                  number: 80
```

Ingress Controller (NGINX, Traefik) handles TLS termination, path routing, rate limiting.

---

## FoodExpress on Kubernetes

### Complete architecture

```
                    Internet
                       │
              ┌────────▼────────┐
              │    Ingress      │
              │  (NGINX ctrl)   │
              └────────┬────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
  ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
  │   Menu    │ │   Order   │ │ Delivery  │
  │  Service  │ │  Service  │ │  Service  │
  │ (3 pods)  │ │ (3 pods)  │ │ (2 pods)  │
  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘
        │              │              │
  ┌─────▼─────┐ ┌─────▼─────┐ ┌─────▼─────┐
  │  Menu DB  │ │ Order DB  │ │Delivery DB│
  │ (MySQL)   │ │ (MySQL)   │ │ (MongoDB) │
  └───────────┘ └───────────┘ └───────────┘
```

Each service: Deployment + Service + ConfigMap + Secret + HPA

---

## Monitoring K8s with kubectl

### Essential troubleshooting commands

```bash
# Cluster health
kubectl get nodes
kubectl top nodes

# Pod issues
kubectl get pods -n foodexpress-prod
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous    # logs from crashed container
kubectl logs <pod-name> -f            # stream logs

# Resource usage
kubectl top pods -n foodexpress-prod

# Events (recent cluster activity)
kubectl get events --sort-by=.lastTimestamp

# Debug networking
kubectl exec -it <pod> -- curl http://order-service:80/health
```

---

## Common K8s Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|-------------|-----|
| **ImagePullBackOff** | Wrong image name or registry auth | Check image tag, imagePullSecrets |
| **CrashLoopBackOff** | App crashes on startup | Check logs: `kubectl logs --previous` |
| **Pending** | Insufficient resources | Check node capacity, resource requests |
| **OOMKilled** | Memory limit exceeded | Increase memory limit or fix memory leak |
| **Service not reachable** | Selector mismatch | Compare service selector vs pod labels |
| **Readiness probe failing** | App not ready, wrong port/path | Check probe config, app startup time |

---

## K8s Dashboard & Monitoring

### Built-in and third-party tools

```
┌─────────────────────────────────────────────┐
│             Monitoring Stack                │
│                                             │
│  ┌─────────────┐    ┌──────────────────┐   │
│  │ Prometheus  │───>│    Grafana       │   │
│  │ (metrics)   │    │  (dashboards)    │   │
│  └─────────────┘    └──────────────────┘   │
│                                             │
│  ┌─────────────┐    ┌──────────────────┐   │
│  │  Loki       │───>│    Grafana       │   │
│  │ (logs)      │    │  (log viewer)    │   │
│  └─────────────┘    └──────────────────┘   │
│                                             │
│  ┌─────────────┐                            │
│  │ K8s         │  (Web UI)                  │
│  │ Dashboard   │                            │
│  └─────────────┘                            │
└─────────────────────────────────────────────┘
```

Metrics Server is required for `kubectl top` and HPA.

---

## Kubernetes RBAC

### Role-Based Access Control

```yaml
# Role: what actions are allowed
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: foodexpress-prod
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods", "pods/log"]
    verbs: ["get", "list", "watch"]

---
# RoleBinding: who gets the role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  namespace: foodexpress-prod
  name: read-pods
subjects:
  - kind: User
    name: sustain-engineer
roleRef:
  kind: Role
  name: pod-reader
```

Sustain engineers typically get read access to prod, write access to dev/staging.

---

## Lab: Fix FoodExpress K8s Manifests

### Scenario

FoodExpress K8s deployment has bugs causing:
- CrashLoopBackOff on order-service
- Payment-service unreachable from order-service
- No health checks (dead pods serve traffic)
- Missing resource limits (noisy neighbor problem)

### Files to fix:
1. `order-deployment.yaml` -- 4 bugs
2. `order-service.yaml` -- 3 bugs
3. `payment-deployment.yaml` -- 3 bugs
4. `namespace-config.yaml` -- 2 bugs

See `Labs/lab-exercises.md` for detailed bug list.

---

## Best Practices for Production K8s

| Practice | Why |
|----------|-----|
| Always set resource requests AND limits | Prevent noisy neighbors, enable scheduling |
| Use readiness AND liveness probes | Remove unhealthy pods from traffic |
| Never use `latest` tag | Non-deterministic deployments |
| Use namespaces for isolation | Separate dev/staging/prod |
| Store secrets in external vault | K8s secrets are only base64 |
| Set PodDisruptionBudgets | Ensure availability during node drain |
| Use Network Policies | Restrict pod-to-pod communication |
| Label everything consistently | Enable filtering and selection |

---

## Key Takeaways

| Concept | Key Point |
|---------|-----------|
| Control Plane | API Server, Scheduler, Controller Manager, etcd |
| Data Plane | kubelet, kube-proxy, container runtime on each node |
| Pod | Smallest deployable unit; ephemeral; use Deployments |
| Service | Stable IP/DNS for pod discovery (ClusterIP, NodePort, LoadBalancer) |
| Probes | Liveness (restart), Readiness (remove from traffic), Startup (slow apps) |
| Resources | Requests (scheduling), Limits (hard cap); always set both |
| HPA | Auto-scale pods based on CPU/memory/custom metrics |
| Namespaces | Virtual clusters for environment isolation |

> **Next:** Module 30 -- Ansible (Configuration Management & Automation)
