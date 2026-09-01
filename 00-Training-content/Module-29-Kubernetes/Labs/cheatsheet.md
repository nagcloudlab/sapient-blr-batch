# Kubernetes (kubectl) Quick Reference

> Single-page reference for kubectl commands and common YAML manifests. Replace `<name>`, `<namespace>`, `<image>` with actual values. Default namespace is `default` unless `-n` is specified.

---

## Cluster Info

| Command | Example | Description |
|---|---|---|
| `kubectl version` | `kubectl version` | Show client and server versions |
| `kubectl cluster-info` | `kubectl cluster-info` | Cluster API endpoint and DNS |
| `kubectl get nodes` | `kubectl get nodes` | List all cluster nodes |
| `kubectl get nodes -o wide` | `kubectl get nodes -o wide` | Nodes with IP, OS, kernel info |
| `kubectl describe node <name>` | `kubectl describe node worker-1` | Detailed node info and resource usage |
| `kubectl config get-contexts` | `kubectl config get-contexts` | List kubeconfig contexts |
| `kubectl config use-context <ctx>` | `kubectl config use-context prod-cluster` | Switch active context |
| `kubectl config current-context` | `kubectl config current-context` | Show current context |
| `kubectl api-resources` | `kubectl api-resources` | List all supported resource types |

---

## Pods

| Command | Example | Description |
|---|---|---|
| `kubectl get pods` | `kubectl get pods` | List pods in default namespace |
| `kubectl get pods -n <ns>` | `kubectl get pods -n foodexpress` | List pods in a namespace |
| `kubectl get pods -A` | `kubectl get pods -A` | List pods in all namespaces |
| `kubectl get pods -o wide` | `kubectl get pods -o wide` | Include node and IP columns |
| `kubectl get pods -w` | `kubectl get pods -w` | Watch pod status changes live |
| `kubectl get pod <name> -o yaml` | `kubectl get pod fe-api-abc123 -o yaml` | Full pod spec and status as YAML |
| `kubectl describe pod <name>` | `kubectl describe pod fe-api-abc123` | Detailed pod info, events, conditions |
| `kubectl logs <pod>` | `kubectl logs fe-api-abc123` | Pod stdout logs |
| `kubectl logs <pod> -f` | `kubectl logs fe-api-abc123 -f` | Follow logs live |
| `kubectl logs <pod> --tail=100` | `kubectl logs fe-api-abc123 --tail=100` | Last 100 lines |
| `kubectl logs <pod> -c <container>` | `kubectl logs fe-api-abc123 -c api` | Logs from specific container in pod |
| `kubectl logs <pod> --previous` | `kubectl logs fe-api-abc123 --previous` | Logs from previous (crashed) container |
| `kubectl exec -it <pod> -- <cmd>` | `kubectl exec -it fe-api-abc123 -- sh` | Interactive shell in pod |
| `kubectl exec <pod> -- <cmd>` | `kubectl exec fe-api-abc123 -- cat /etc/hosts` | Non-interactive command in pod |
| `kubectl exec -it <pod> -c <ctr> -- sh` | `kubectl exec -it fe-api-abc123 -c api -- sh` | Shell in specific container |
| `kubectl delete pod <name>` | `kubectl delete pod fe-api-abc123` | Delete pod (Deployment will recreate) |
| `kubectl delete pod <name> --force` | `kubectl delete pod fe-api-abc123 --force` | Force delete (skips graceful shutdown) |
| `kubectl run <name> --image=<img>` | `kubectl run debug --image=busybox --rm -it -- sh` | Run temporary debug pod |

---

## Deployments

| Command | Example | Description |
|---|---|---|
| `kubectl get deployments` | `kubectl get deployments -n foodexpress` | List deployments |
| `kubectl get deploy <name>` | `kubectl get deploy fe-api` | Single deployment status |
| `kubectl describe deploy <name>` | `kubectl describe deploy fe-api` | Deployment details and events |
| `kubectl create deployment <name> --image=<img>` | `kubectl create deployment fe-api --image=foodexpress-api:1.0` | Create deployment imperatively |
| `kubectl apply -f <file>` | `kubectl apply -f deployment.yaml` | Apply manifest from file |
| `kubectl apply -f <dir>` | `kubectl apply -f ./manifests/` | Apply all manifests in directory |
| `kubectl scale deploy <name> --replicas=n` | `kubectl scale deploy fe-api --replicas=3` | Scale deployment |
| `kubectl set image deploy/<name> <ctr>=<img>` | `kubectl set image deploy/fe-api api=foodexpress-api:1.1` | Update container image |
| `kubectl rollout status deploy/<name>` | `kubectl rollout status deploy/fe-api` | Watch rollout progress |
| `kubectl rollout history deploy/<name>` | `kubectl rollout history deploy/fe-api` | Show rollout revision history |
| `kubectl rollout undo deploy/<name>` | `kubectl rollout undo deploy/fe-api` | Rollback to previous revision |
| `kubectl rollout undo deploy/<name> --to-revision=n` | `kubectl rollout undo deploy/fe-api --to-revision=2` | Rollback to specific revision |
| `kubectl rollout pause deploy/<name>` | `kubectl rollout pause deploy/fe-api` | Pause rollout |
| `kubectl rollout resume deploy/<name>` | `kubectl rollout resume deploy/fe-api` | Resume paused rollout |
| `kubectl delete deploy <name>` | `kubectl delete deploy fe-api` | Delete deployment |

---

## Services

| Command | Example | Description |
|---|---|---|
| `kubectl get svc` | `kubectl get svc -n foodexpress` | List services |
| `kubectl get svc -o wide` | `kubectl get svc -o wide` | Include selector and endpoints |
| `kubectl describe svc <name>` | `kubectl describe svc fe-api-svc` | Service details and endpoints |
| `kubectl expose deploy <name> --port=<p> --type=<T>` | `kubectl expose deploy fe-api --port=3000 --type=ClusterIP` | Create service for deployment |
| `kubectl expose deploy <name> --port=80 --type=NodePort` | `kubectl expose deploy fe-api --port=80 --type=NodePort` | Expose on a node port |
| `kubectl expose deploy <name> --port=80 --type=LoadBalancer` | `kubectl expose deploy fe-api --port=80 --type=LoadBalancer` | Expose via cloud load balancer |
| `kubectl delete svc <name>` | `kubectl delete svc fe-api-svc` | Remove service |

**Service types:**

| Type | Description |
|---|---|
| `ClusterIP` | Internal-only; reachable within the cluster (default) |
| `NodePort` | Exposes on a static port on each node (30000-32767) |
| `LoadBalancer` | Provisions cloud load balancer (AWS/GCP/Azure) |
| `ExternalName` | DNS alias to an external service |

---

## ConfigMaps and Secrets

| Command | Example | Description |
|---|---|---|
| `kubectl create configmap <name> --from-literal=K=V` | `kubectl create configmap fe-config --from-literal=NODE_ENV=production` | Create configmap from literal |
| `kubectl create configmap <name> --from-file=<file>` | `kubectl create configmap fe-config --from-file=app.conf` | Create configmap from file |
| `kubectl get configmap <name> -o yaml` | `kubectl get configmap fe-config -o yaml` | View configmap contents |
| `kubectl create secret generic <name> --from-literal=K=V` | `kubectl create secret generic fe-secrets --from-literal=DB_PASSWORD=s3cr3t` | Create generic secret |
| `kubectl create secret docker-registry <name> ...` | `kubectl create secret docker-registry regcred --docker-server=... --docker-username=... --docker-password=...` | Registry pull secret |
| `kubectl get secrets` | `kubectl get secrets -n foodexpress` | List secrets (values hidden) |
| `kubectl describe secret <name>` | `kubectl describe secret fe-secrets` | Secret metadata (values still hidden) |
| `kubectl get secret <name> -o jsonpath='{.data.KEY}' | base64 -d` | `kubectl get secret fe-secrets -o jsonpath='{.data.DB_PASSWORD}' | base64 -d` | Decode secret value |
| `kubectl delete configmap <name>` | `kubectl delete configmap fe-config` | Delete configmap |
| `kubectl delete secret <name>` | `kubectl delete secret fe-secrets` | Delete secret |

---

## Namespaces

| Command | Example | Description |
|---|---|---|
| `kubectl get namespaces` | `kubectl get namespaces` | List all namespaces |
| `kubectl create namespace <name>` | `kubectl create namespace foodexpress` | Create namespace |
| `kubectl delete namespace <name>` | `kubectl delete namespace old-env` | Delete namespace and all its resources |
| `kubectl config set-context --current --namespace=<ns>` | `kubectl config set-context --current --namespace=foodexpress` | Set default namespace for current context |
| `kubectl get all -n <ns>` | `kubectl get all -n foodexpress` | All resources in a namespace |

---

## Common YAML Manifests

**Pod:**
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fe-api-pod
  namespace: foodexpress
  labels:
    app: fe-api
spec:
  containers:
    - name: api
      image: foodexpress-api:1.0
      ports:
        - containerPort: 3000
      env:
        - name: NODE_ENV
          value: "production"
      resources:
        requests:
          cpu: "100m"
          memory: "128Mi"
        limits:
          cpu: "500m"
          memory: "512Mi"
```

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fe-api
  namespace: foodexpress
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fe-api
  template:
    metadata:
      labels:
        app: fe-api
    spec:
      containers:
        - name: api
          image: foodexpress-api:1.0
          ports:
            - containerPort: 3000
          envFrom:
            - configMapRef:
                name: fe-config
            - secretRef:
                name: fe-secrets
          livenessProbe:
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 15
            periodSeconds: 20
          readinessProbe:
            httpGet:
              path: /ready
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 10
```

**Service:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: fe-api-svc
  namespace: foodexpress
spec:
  selector:
    app: fe-api
  type: ClusterIP
  ports:
    - protocol: TCP
      port: 80
      targetPort: 3000
```

**ConfigMap:**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: fe-config
  namespace: foodexpress
data:
  NODE_ENV: "production"
  LOG_LEVEL: "info"
  DB_HOST: "mysql-svc"
```

---

## Debugging

| Command | Example | Description |
|---|---|---|
| `kubectl top nodes` | `kubectl top nodes` | CPU and memory usage per node |
| `kubectl top pods` | `kubectl top pods -n foodexpress` | CPU and memory usage per pod |
| `kubectl top pod <name> --containers` | `kubectl top pod fe-api-abc123 --containers` | Per-container resource usage |
| `kubectl get events -n <ns>` | `kubectl get events -n foodexpress` | Recent cluster events |
| `kubectl get events --sort-by=.lastTimestamp` | `kubectl get events -n foodexpress --sort-by=.lastTimestamp` | Events sorted by time |
| `kubectl port-forward pod/<name> <lport>:<cport>` | `kubectl port-forward pod/fe-api-abc123 8080:3000` | Forward local port to pod port |
| `kubectl port-forward svc/<name> <lport>:<sport>` | `kubectl port-forward svc/fe-api-svc 8080:80` | Forward local port to service port |
| `kubectl get pod <name> -o jsonpath='{.status.conditions}'` | `kubectl get pod fe-api-abc123 -o jsonpath='{.status.conditions}'` | Inspect pod conditions |
| `kubectl get pod <name> -o jsonpath='{.status.containerStatuses}'` | `kubectl get pod fe-api-abc123 -o jsonpath='{.status.containerStatuses}'` | Container state and restart count |
| `kubectl auth can-i <verb> <resource>` | `kubectl auth can-i create pods` | Check RBAC permission |

**Pod status troubleshooting:**

| Status | Likely Cause |
|---|---|
| `Pending` | No node with sufficient resources; PVC unbound |
| `CrashLoopBackOff` | Container exits repeatedly; check `kubectl logs --previous` |
| `ImagePullBackOff` | Wrong image name/tag or missing registry credentials |
| `OOMKilled` | Container exceeded memory limit |
| `Error` | Container exited with non-zero code; check logs |
| `Terminating` | Pod stuck deleting; may need `--force` delete |

---

*FoodExpress Training | Module 29: Kubernetes | Publicis Sapient Sustain Eng 2026*
