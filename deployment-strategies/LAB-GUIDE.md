# Kubernetes Deployment Strategies - Hands-On Lab

## Overview

This lab teaches **6 deployment strategies** using Kind (Kubernetes in Docker), Istio service mesh, and **Kiali** for real-time visual observation.

| Strategy | Downtime | Rollback Speed | Resource Cost | Traffic Control | Best For |
|---|---|---|---|---|---|
| **Recreate** | YES | Slow (redeploy) | Low | None | Dev/test, DB migrations |
| **Rolling Update** | No | Slow (rollback) | Medium | None | Default K8s workloads |
| **Blue-Green** | No | Instant (switch) | 2x resources | Binary switch | Critical apps, instant rollback |
| **Canary** | No | Fast (shift back) | Low-Medium | Weighted % | Gradual validation |
| **A/B Testing** | No | Fast | Medium | Header/cookie rules | Feature testing, user segments |
| **Dark Launch** | No | N/A (shadow) | 2x resources | Mirror copy | Testing with real traffic |

### App Versions (Visual Distinction)
- **v1** = Blue background (`#2196F3`)
- **v2** = Green background (`#4CAF50`)
- **v3** = Orange background (`#FF9800`)

---

## GCP VM Configuration

### Create the VM
```bash
gcloud compute instances create deployment-lab-vm \
    --zone=us-central1-a \
    --machine-type=e2-standard-4 \
    --boot-disk-size=50GB \
    --boot-disk-type=pd-ssd \
    --image-family=ubuntu-2204-lts \
    --image-project=ubuntu-os-cloud \
    --tags=deployment-lab
```

| Setting | Value | Why |
|---|---|---|
| Machine type | `e2-standard-4` (4 vCPUs, 16GB RAM) | Kind (3 nodes) + Istio + Kiali need at least 4 CPUs & 12GB RAM |
| Boot disk | 50GB SSD | Docker images + Kind nodes need space |
| OS | Ubuntu 22.04 LTS | Stable, good Docker/K8s support |
| Zone | us-central1-a | Change as needed |

### Create firewall rule (allow SSH + dashboard ports)
```bash
gcloud compute firewall-rules create allow-lab-ports \
    --direction=INGRESS \
    --action=ALLOW \
    --rules=tcp:22,tcp:8080,tcp:20001,tcp:3000,tcp:9090 \
    --source-ranges=0.0.0.0/0 \
    --target-tags=deployment-lab
```

### Delete VM when done
```bash
gcloud compute instances delete deployment-lab-vm --zone=us-central1-a
gcloud compute firewall-rules delete allow-lab-ports
```

---

## Step 0: Prerequisites - Install Tools on VM

### SCP lab files to VM
```bash
gcloud compute scp --recurse ~/deployment-strategies deployment-lab-vm:~ --zone=us-central1-a
```

### SSH into your GCP VM (with port tunneling for dashboards)
```bash
gcloud compute ssh deployment-lab-vm --zone=us-central1-a -- -L 8080:localhost:8080 -L 20001:localhost:20001 -L 3000:localhost:3000 -L 9090:localhost:9090
```

### Navigate to lab directory
```bash
cd ~/deployment-strategies
```

### Install Docker
```bash
sudo apt-get update -y
sudo apt-get install -y ca-certificates curl gnupg python3 python3-pip bc
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock
```

Verify:
```bash
docker --version
docker run hello-world
```

### Install kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

This downloads the latest stable kubectl binary for linux/amd64.

```bash
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
rm -f kubectl
```

Verify:
```bash
kubectl version --client
```

### Install Kind (Kubernetes in Docker)
```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
```

This downloads Kind v0.20.0 binary for linux/amd64.

```bash
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
```

Verify:
```bash
kind --version
```

### Install Istioctl
```bash
curl -L https://istio.io/downloadIstio | ISTIO_VERSION=1.20.0 TARGET_ARCH=x86_64 sh -
```

This downloads Istio 1.20.0 and extracts it to `./istio-1.20.0/`.

```bash
sudo cp istio-1.20.0/bin/istioctl /usr/local/bin/
```

Verify:
```bash
istioctl version --remote=false
```

### Verify all tools are installed
```bash
docker --version
kubectl version --client
kind --version
istioctl version --remote=false
```

---

## Step 1: Create Kind Kubernetes Cluster

Kind creates a multi-node K8s cluster using Docker containers as nodes.

### View the cluster config
```bash
cat setup/kind-cluster.yaml
```

This creates 1 control-plane + 2 worker nodes with port mappings.

### Create the cluster
```bash
kind create cluster --config setup/kind-cluster.yaml --wait 60s
```

### Verify the cluster
```bash
kubectl cluster-info --context kind-deployment-lab
kubectl get nodes
```

Expected output: 3 nodes (1 control-plane, 2 workers) in Ready state.

---

## Step 2: Install Istio Service Mesh

Istio provides traffic management, observability, and security for microservices.

### Install Istio with demo profile
```bash
istioctl install --set profile=demo -y
```

### Enable automatic sidecar injection
```bash
kubectl label namespace default istio-injection=enabled --overwrite
```

Every pod in the `default` namespace will now get an Istio proxy sidecar automatically.

### Verify Istio installation
```bash
kubectl get pods -n istio-system
```

Expected: `istiod`, `istio-ingressgateway`, and `istio-egressgateway` pods running.

```bash
kubectl wait --for=condition=available deployment/istiod -n istio-system --timeout=120s
kubectl wait --for=condition=available deployment/istio-ingressgateway -n istio-system --timeout=120s
```

### Deploy Istio Gateway
```bash
kubectl apply -f setup/gateway.yaml
```

Verify:
```bash
kubectl get gateway
```

---

## Step 3: Install Observability Addons (Kiali, Prometheus, Grafana)

### Install Prometheus (metrics collection - required by Kiali)
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/prometheus.yaml
```

### Install Grafana (metrics dashboards)
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/grafana.yaml
```

### Install Kiali (service mesh dashboard)
```bash
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
```

If Kiali shows CRD errors, wait 5 seconds and re-apply:
```bash
sleep 5
kubectl apply -f https://raw.githubusercontent.com/istio/istio/release-1.20/samples/addons/kiali.yaml
```

### Wait for all addons to be ready
```bash
kubectl wait --for=condition=available deployment/prometheus -n istio-system --timeout=120s
kubectl wait --for=condition=available deployment/grafana -n istio-system --timeout=120s
kubectl wait --for=condition=available deployment/kiali -n istio-system --timeout=120s
```

### Verify all pods
```bash
kubectl get pods -n istio-system
```

Expected: `kiali`, `prometheus`, `grafana` pods all running alongside Istio pods.

---

## Step 4: Open Dashboards (Port Forwarding)

Run each in a **separate terminal** (or use `&` to background):

### Terminal 1: Ingress Gateway (App access)
```bash
kubectl port-forward -n istio-system svc/istio-ingressgateway 8080:80 &
```

### Terminal 2: Kiali Dashboard
```bash
kubectl port-forward -n istio-system svc/kiali 20001:20001 &
```

### Terminal 3: Grafana Dashboard
```bash
kubectl port-forward -n istio-system svc/grafana 3000:3000 &
```

### Terminal 4: Prometheus
```bash
kubectl port-forward -n istio-system svc/prometheus 9090:9090 &
```

### Access URLs (via SSH tunnel on your local browser)

| Dashboard  | URL                        |
|------------|----------------------------|
| App        | http://localhost:8080       |
| Kiali      | http://localhost:20001      |
| Grafana    | http://localhost:3000       |
| Prometheus | http://localhost:9090       |

### Configure Kiali for best experience

1. Open http://localhost:20001
2. Go to **Graph** (left menu)
3. Select namespace: **default**
4. Set Graph type: **Versioned app graph**
5. Click **Display** dropdown and enable:
   - [x] Traffic Distribution (shows % on edges)
   - [x] Traffic Animation (animated dots)
   - [x] Traffic Rate (req/s on edges)
   - [x] Security (mTLS icons)
6. Set refresh: **Every 10s**
7. Set time range: **Last 1m**

---

## Step 5: Build & Load Sample Application

### Build 3 versions with different colors
```bash
cd ~/deployment-strategies

docker build -t sample-app:v1 --build-arg VERSION=v1 --build-arg COLOR="#2196F3" --build-arg APP_NAME="App V1" app/

docker build -t sample-app:v2 --build-arg VERSION=v2 --build-arg COLOR="#4CAF50" --build-arg APP_NAME="App V2" app/

docker build -t sample-app:v3 --build-arg VERSION=v3 --build-arg COLOR="#FF9800" --build-arg APP_NAME="App V3" app/
```

### Load images into Kind cluster
```bash
kind load docker-image sample-app:v1 sample-app:v2 sample-app:v3 --name deployment-lab
```

### Verify images are loaded
```bash
docker exec deployment-lab-control-plane crictl images | grep sample-app
```

---

## Lab 1: Recreate Deployment

### Theory

The simplest strategy. Kubernetes terminates ALL existing pods first, then creates new pods. This causes **downtime** during the transition.

```
v1 v1 v1  ->  --- --- ---  ->  v2 v2 v2
 running       terminating      starting
              (DOWNTIME!)
```

**Use when:** Dev/test, DB migrations, apps that can't run 2 versions simultaneously

### Deploy v1

```bash
kubectl apply -f strategies/1-recreate/deployment-v1.yaml
```

Wait for pods:
```bash
kubectl rollout status deployment/sample-app
kubectl get pods -l app=sample-app
```

### Verify v1 is running

Open browser: http://localhost:8080 (Blue page = v1)

```bash
curl -s http://localhost:8080/api/info | python3 -m json.tool
```

### Generate traffic for Kiali

```bash
for i in $(seq 1 50); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

### Observe in Kiali (before update)
- **Graph**: `istio-ingressgateway -> sample-app (v1)` with green edges
- **Workloads**: sample-app shows 3/3 healthy pods

### Update to v2

```bash
kubectl apply -f strategies/1-recreate/deployment-v2.yaml
```

### Watch the recreate in real-time

```bash
kubectl get pods -l app=sample-app -w
```

(Press Ctrl+C after all v2 pods are Running)

```bash
kubectl rollout status deployment/sample-app
```

### Test multiple requests during/after update

```bash
for i in $(seq 1 10); do
    curl -s http://localhost:8080/api/info 2>/dev/null | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])" 2>/dev/null || echo "DOWN"
    sleep 1
done
```

### Observe in Kiali (during & after update)
- **During**: Edges go **RED** or disappear (downtime!)
- **After**: Green edges reappear, now pointing to v2
- **Workloads**: Pods show v2 image

### Discussion
- Why did we see downtime?
- How long was the downtime window?
- When would this be acceptable in production?

### Cleanup before next lab

```bash
kubectl delete deployment --all
kubectl delete service sample-app
kubectl delete virtualservice sample-app
```

Wait for cleanup:
```bash
kubectl get pods -l app=sample-app
```

(Should show no pods or all Terminating)

---

## Lab 2: Rolling Update

### Theory

Default K8s strategy. Gradually replaces old pods with new ones. **Zero downtime** - old and new coexist during transition.

```
v1 v1 v1 v1 v1 -> v1 v1 v1 v1 v2 -> v1 v1 v2 v2 v2 -> v2 v2 v2 v2 v2
```

Key parameters:
- **maxSurge=1**: Allow 1 extra pod above desired count
- **maxUnavailable=0**: Never go below desired count (zero downtime)

### Deploy v1 with 5 replicas

```bash
kubectl apply -f strategies/2-rolling-update/deployment-v1.yaml
kubectl rollout status deployment/sample-app
kubectl get pods -l app=sample-app
```

### Generate traffic

```bash
for i in $(seq 1 100); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

### Observe in Kiali (before update)
- **Graph**: Clean single path to v1, green edges
- **Workloads**: 5 healthy v1 pods

### Rolling update to v2 (conservative)

```bash
kubectl apply -f strategies/2-rolling-update/deployment-v2.yaml
```

### Watch pods rolling one at a time

```bash
kubectl get pods -l app=sample-app -w
```

(Press Ctrl+C after all v2 pods are Running)

### Observe in Kiali (during update) - KEY MOMENT
- **Graph (Versioned app graph)**: BOTH v1 and v2 nodes appear!
- Traffic splits between v1 and v2 as pods rotate
- **Both edges stay GREEN** (no downtime!)
- After completion: only v2 node remains

### Verify

```bash
kubectl rollout status deployment/sample-app
kubectl get pods -l app=sample-app
curl -s http://localhost:8080/api/info | python3 -m json.tool
```

### Experiment: Aggressive Rolling Update

Reset to v1 first:
```bash
kubectl apply -f strategies/2-rolling-update/deployment-v1.yaml
kubectl rollout status deployment/sample-app
```

Generate traffic:
```bash
for i in $(seq 1 100); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

Now aggressive update (maxSurge=3, maxUnavailable=2):
```bash
kubectl apply -f strategies/2-rolling-update/deployment-v2-aggressive.yaml
kubectl get pods -l app=sample-app -w
```

### Kiali Comparison
- **Conservative**: v1 and v2 coexist in graph for LONGER
- **Aggressive**: v2 appears and v1 disappears MUCH faster
- **Both**: Edges stay green (no downtime)

### Bonus: Rollback

```bash
kubectl rollout undo deployment/sample-app
kubectl rollout status deployment/sample-app
curl -s http://localhost:8080/api/info | python3 -m json.tool
```

Check rollout history:
```bash
kubectl rollout history deployment/sample-app
```

### Kiali: Rollback is visible - traffic shifts back to v1

### Discussion
- How does this compare to Recreate in Kiali? (green vs red edges)
- What's the tradeoff between conservative and aggressive settings?
- During rolling update, users see mixed versions - is that a problem?

### Cleanup

```bash
kubectl delete deployment --all
kubectl delete service sample-app
kubectl delete virtualservice sample-app
```

---

## Lab 3: Blue-Green Deployment

### Theory

Run two identical environments (Blue and Green). Only one serves live traffic. Switch traffic **instantly** using Istio VirtualService.

```
Blue (v1) <-- ALL TRAFFIC     Green (v2) [idle, being tested]
                  |  INSTANT SWITCH  |
Blue (v1) [idle, standby]     Green (v2) <-- ALL TRAFFIC
```

**Key advantage**: Instant rollback!
**Cost**: 2x resources (both versions running)

### Deploy Blue (v1) - current production

```bash
kubectl apply -f strategies/3-blue-green/blue-deployment.yaml
kubectl rollout status deployment/sample-app-blue
```

### Route ALL traffic to Blue

```bash
kubectl apply -f strategies/3-blue-green/virtualservice-blue.yaml
```

### Verify Blue is serving traffic

```bash
curl -s http://localhost:8080/api/info | python3 -m json.tool
```

Generate traffic:
```bash
for i in $(seq 1 100); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

### Observe in Kiali
- **Graph**: `istio-ingressgateway -> sample-app-blue` with 100% traffic
- Only blue service has edges

### Deploy Green (v2) alongside Blue - NO traffic yet

```bash
kubectl apply -f strategies/3-blue-green/green-deployment.yaml
kubectl rollout status deployment/sample-app-green
```

### Verify both are running but only Blue gets traffic

```bash
kubectl get pods -l app=sample-app
```

```bash
# Run 5 times - all should show v1
for i in 1 2 3 4 5; do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done
```

### Observe in Kiali
- **Graph**: Traffic ONLY goes to blue
- **Workloads**: BOTH blue and green appear, but green has NO traffic edges
- Green is running idle - ready to receive traffic

### (Optional) Test Green directly before switching

```bash
kubectl port-forward svc/sample-app-green 8081:80 &
curl -s http://localhost:8081/api/info | python3 -m json.tool
kill %1
```

### THE SWITCH - Flip all traffic to Green!

```bash
kubectl apply -f strategies/3-blue-green/virtualservice-green.yaml
```

### Verify instant switch

```bash
# All should show v2 now
for i in 1 2 3 4 5; do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done
```

Generate traffic:
```bash
for i in $(seq 1 100); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

### Observe THE SWITCH in Kiali
- **Graph**: Traffic edge INSTANTLY moved from Blue to Green!
- No transition period - no mixed versions (unlike Rolling Update)
- No red edges (unlike Recreate)

### INSTANT ROLLBACK

```bash
kubectl apply -f strategies/3-blue-green/virtualservice-blue.yaml
```

```bash
# Back to v1
curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

### Kiali: Traffic INSTANTLY jumps back to Blue

### Discussion
- How does the Kiali graph differ from Rolling Update? (instant vs gradual)
- What's the resource cost of keeping both deployments running?
- When would you decommission the old (Blue) deployment?

### Cleanup

```bash
kubectl delete deployment --all
kubectl delete service sample-app-blue sample-app-green
kubectl delete virtualservice sample-app
```

---

## Lab 4: Canary Deployment

### Theory

Gradually shift traffic from old to new version in controlled percentages. Monitor metrics at each stage.

```
Phase 1:  90% v1  /  10% v2   (initial canary)
Phase 2:  70% v1  /  30% v2   (gaining confidence)
Phase 3:  50% v1  /  50% v2   (half and half)
Phase 4:   0% v1  / 100% v2   (full rollout)
```

**Kiali tip**: Make sure **Traffic Distribution** is enabled in Display to see % labels on edges.

### Deploy v1 and v2 with DestinationRule

```bash
kubectl apply -f strategies/4-canary/deployment-v1.yaml
kubectl rollout status deployment/sample-app-v1
kubectl rollout status deployment/sample-app-v2
kubectl get pods -l app=sample-app
```

### Phase 1: 90% v1 / 10% v2

```bash
kubectl apply -f strategies/4-canary/virtualservice-90-10.yaml
```

Generate traffic and verify split:
```bash
for i in $(seq 1 100); do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done | sort | uniq -c
```

Expected: ~90 v1, ~10 v2

### Observe Phase 1 in Kiali
- **Graph**: Two edges from sample-app service:
  - **Thick** edge to v1 labeled ~90%
  - **Thin** edge to v2 labeled ~10%
- Both edges GREEN (both healthy)

### Phase 2: 70% v1 / 30% v2

```bash
kubectl apply -f strategies/4-canary/virtualservice-70-30.yaml
```

Verify:
```bash
for i in $(seq 1 100); do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done | sort | uniq -c
```

### Observe Phase 2 in Kiali
- v2 edge gets **thicker**, v1 edge gets **thinner**
- Labels update: ~70% / ~30%

### Phase 3: 50% v1 / 50% v2

```bash
kubectl apply -f strategies/4-canary/virtualservice-50-50.yaml
```

Verify:
```bash
for i in $(seq 1 100); do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done | sort | uniq -c
```

### Observe Phase 3 in Kiali
- Both edges roughly **equal thickness**
- Labels: ~50% / ~50% - the most visually symmetric view

### Phase 4: 100% v2 (full rollout)

```bash
kubectl apply -f strategies/4-canary/virtualservice-0-100.yaml
```

Verify:
```bash
for i in $(seq 1 100); do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done | sort | uniq -c
```

### Observe Phase 4 in Kiali
- Only v2 edge remains
- v1 edge disappears - full rollout complete

### Simulate Rollback

Imagine v2 has issues at 30% traffic:
```bash
kubectl apply -f strategies/4-canary/virtualservice-90-10.yaml
```

Kiali: v2 edge shrinks back, v1 edge grows

### Kiali Metrics Deep Dive (while canary is active)

1. Click v1 or v2 node in Graph > **Inbound Metrics** tab
2. Compare latency between v1 and v2
3. Check error rates per version
4. Go to **Grafana** (http://localhost:3000) > Istio Service Dashboard for detailed comparison

### Discussion
- How does Kiali help you decide whether to proceed to the next phase?
- What metrics would you check before increasing canary percentage?
- How is this different from Blue-Green? (gradual vs instant)

### Cleanup

```bash
kubectl delete deployment --all
kubectl delete service sample-app
kubectl delete virtualservice sample-app
kubectl delete destinationrule sample-app
```

---

## Lab 5: A/B Testing

### Theory

Route traffic based on **request attributes** (headers, cookies, user-agent) rather than random percentages. Same URL returns different versions based on who's asking.

```
Request with header "x-user-group: beta"  ->  v2 (new feature)
Request without special header             ->  v1 (stable)
```

**Unlike Canary**: A/B is DETERMINISTIC - same user always gets same version.

### Deploy both versions

```bash
kubectl apply -f strategies/5-ab-testing/deployment.yaml
kubectl rollout status deployment/sample-app-v1
kubectl rollout status deployment/sample-app-v2
```

---

### Experiment A: Header-Based Routing

```bash
kubectl apply -f strategies/5-ab-testing/virtualservice-header-based.yaml
```

#### Test - Normal user gets v1:
```bash
curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Test - Beta user gets v2:
```bash
curl -s -H "x-user-group: beta" http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Generate mixed traffic for Kiali:
```bash
for i in $(seq 1 50); do
    curl -s http://localhost:8080/api/info > /dev/null
    curl -s -H "x-user-group: beta" http://localhost:8080/api/info > /dev/null
done &
```

#### Observe in Kiali
- **Graph**: Two edges to v1 and v2
- **Istio Config** > VirtualService: Shows match rules with `headers.x-user-group.exact: beta`

---

### Experiment B: Cookie-Based Routing

```bash
kubectl apply -f strategies/5-ab-testing/virtualservice-cookie-based.yaml
```

#### Normal user -> v1:
```bash
curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Internal user (cookie) -> v2:
```bash
curl -s -b "user_type=internal" http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Generate mixed traffic:
```bash
for i in $(seq 1 50); do
    curl -s http://localhost:8080/api/info > /dev/null
    curl -s -b "user_type=internal" http://localhost:8080/api/info > /dev/null
done &
```

---

### Experiment C: User-Agent Based Routing

```bash
kubectl apply -f strategies/5-ab-testing/virtualservice-useragent-based.yaml
```

#### Desktop user -> v1:
```bash
curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Mobile user -> v2:
```bash
curl -s -H "User-Agent: Mozilla/5.0 (iPhone; Mobile; rv:1.0)" http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
```

#### Generate mixed traffic:
```bash
for i in $(seq 1 50); do
    curl -s http://localhost:8080/api/info > /dev/null
    curl -s -H "User-Agent: Mozilla/5.0 (iPhone; Mobile; rv:1.0)" http://localhost:8080/api/info > /dev/null
done &
```

### Observe in Kiali (all experiments)
- **Graph**: Traffic flows to both v1 and v2
- **Istio Config** > click VirtualService: Shows match rules with green validation checkmarks
- Any misconfig shows as yellow warnings or red errors

### Kiali vs Canary comparison
- **Canary**: Kiali shows percentage-based split with configured weights
- **A/B Testing**: Split depends on actual request patterns, not weights

### Discussion
- How is A/B testing different from canary in Kiali?
- What real-world scenarios need header-based vs cookie-based routing?
- How would you route by geographic region?

### Cleanup

```bash
kubectl delete deployment --all
kubectl delete service sample-app
kubectl delete virtualservice sample-app
kubectl delete destinationrule sample-app
```

---

## Lab 6: Dark Launch (Traffic Mirroring)

### Theory

Send a **copy** of production traffic to the new version without affecting users. v2 processes real requests but responses are **discarded**.

```
User Request -> v1 (response sent to user)
             \-> v2 (copy of request, response DISCARDED)
```

**Safest strategy** - zero user impact, real traffic testing.

### Deploy both versions

```bash
kubectl apply -f strategies/6-dark-launch/deployment.yaml
kubectl rollout status deployment/sample-app-v1
kubectl rollout status deployment/sample-app-v2
```

### Apply 100% traffic mirroring

```bash
kubectl apply -f strategies/6-dark-launch/virtualservice-mirror.yaml
```

### Verify: Users ALWAYS see v1

```bash
# Run 5 times - ALL should show v1
for i in 1 2 3 4 5; do
    curl -s http://localhost:8080/api/info | python3 -c "import sys,json; print(json.load(sys.stdin)['version'])"
done
```

### Send traffic so v2 receives mirror copies

```bash
for i in $(seq 1 30); do
    curl -s http://localhost:8080/api/info > /dev/null
    sleep 0.2
done
```

### Prove v2 received the mirrored traffic

```bash
kubectl logs -l version=v2 --tail=10
```

v2 pod logs will show it processed requests even though users never saw v2 responses!

### Generate more traffic for Kiali

```bash
for i in $(seq 1 100); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &
```

### Observe in Kiali - UNIQUE VIEW
- **Graph**:
  - Solid edge: `istio-ingressgateway -> sample-app (v1)` (real traffic)
  - **Mirrored edge**: to v2 (mirrored traffic, distinct visual!)
- **Both v1 and v2** show as receiving traffic
- But only v1 responses go back to the client
- **Workloads**: Both v1 and v2 show active inbound traffic

### Kiali Metrics for Dark Launch

1. Click **v2 node** in Graph > **Inbound Metrics**
2. Compare v1 vs v2: latency, error rate, throughput
3. This is exactly how you validate v2 before promoting it to production!

### Experiment: Partial Mirroring (50%)

```bash
kubectl apply -f strategies/6-dark-launch/virtualservice-mirror-partial.yaml
```

Send traffic:
```bash
for i in $(seq 1 40); do
    curl -s http://localhost:8080/api/info > /dev/null
    sleep 0.2
done
```

Check v2 logs - should be roughly half the requests:
```bash
kubectl logs -l version=v2 --tail=20
```

### Observe in Kiali (50% Mirror)
- v2 mirror edge is **thinner** (less traffic)
- Useful when v2 can't handle full production load yet

### Discussion
- Why is this the safest deployment strategy?
- What can you validate that you can't with other strategies?
- What metrics in Kiali would make you confident to promote v2?
- What's the infrastructure cost of mirroring?

### Cleanup

```bash
kubectl delete deployment --all
kubectl delete service sample-app
kubectl delete virtualservice sample-app
kubectl delete destinationrule sample-app
```

---

## Strategy Comparison Summary

### Kiali Visual Summary

| Strategy | What You See in Kiali Graph |
|---|---|
| **Recreate** | Traffic STOPS (red edges), then resumes to new version |
| **Rolling Update** | Both v1 and v2 nodes visible briefly, edges stay GREEN |
| **Blue-Green** | Traffic edge INSTANTLY jumps from Blue to Green service |
| **Canary** | Two edges with % labels, thickness shifts gradually |
| **A/B Testing** | Two edges, ratio depends on request patterns |
| **Dark Launch** | Solid edge to v1 + mirrored edge to v2 |

### Quick Decision Guide

| Scenario | Strategy |
|---|---|
| Dev/test, don't care about downtime | **Recreate** |
| Standard production deployment | **Rolling Update** |
| Mission-critical, need instant rollback | **Blue-Green** |
| Want to validate gradually with metrics | **Canary** |
| Test features with specific user groups | **A/B Testing** |
| Zero-risk testing with real traffic | **Dark Launch** |

### Risk vs Complexity

```
Low Risk  <------------------------------->  High Risk
Dark Launch > Canary > Blue-Green > A/B Testing > Rolling > Recreate

Simple    <------------------------------->  Complex
Recreate > Rolling > Blue-Green > Canary > A/B Testing > Dark Launch
```

---

## Full Cleanup

```bash
# Delete all resources
kubectl delete deployment --all
kubectl delete service --all
kubectl delete virtualservice --all
kubectl delete destinationrule --all
kubectl delete gateway --all

# Delete the Kind cluster
kind delete cluster --name deployment-lab
```

---

## Appendix: Useful Commands

```bash
# Watch pods in real-time
kubectl get pods -w

# Check VirtualService config
kubectl get virtualservice sample-app -o yaml

# Check DestinationRule
kubectl get destinationrule sample-app -o yaml

# View Istio proxy logs (sidecar)
kubectl logs <pod-name> -c istio-proxy

# Check Istio config for errors
istioctl analyze

# See all Istio resources
kubectl get gateway,virtualservice,destinationrule -A

# Kiali (alternative to port-forward)
istioctl dashboard kiali

# Grafana (alternative)
istioctl dashboard grafana
```

## Appendix: Kiali Troubleshooting

```bash
# Graph empty? Ensure traffic is flowing
for i in $(seq 1 50); do curl -s http://localhost:8080/api/info > /dev/null; sleep 0.2; done &

# Check sidecar injection is enabled
kubectl get namespace default --show-labels

# Kiali not running?
kubectl get pods -n istio-system -l app=kiali
kubectl logs -n istio-system -l app=kiali

# Prometheus not collecting?
kubectl get pods -n istio-system -l app=prometheus

# Restart Kiali
kubectl rollout restart deployment/kiali -n istio-system
```
