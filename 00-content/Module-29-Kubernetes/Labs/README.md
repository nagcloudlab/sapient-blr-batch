# Module 29: Kubernetes -- Lab Setup

## Prerequisites

- kubectl (`kubectl version --client` to confirm)
- minikube (`minikube version` to confirm)
- Docker Desktop running (minikube uses it as the driver on Windows/Mac)

## Running the Starter Code

```bash
minikube start --memory=4096 --cpus=2
kubectl apply -f Labs/starter-code/manifests/
kubectl get pods    # Expect some pods in CrashLoopBackOff or Pending states
```

Bugs are in the YAML manifests. Each failing pod corresponds to at least one issue in
`lab-exercises.md`. Fix the manifest and re-apply with `kubectl apply -f`.

## Verifying Your Fixes

```bash
# All pods should show Running / Ready
kubectl get pods -o wide

# Services should have the correct ports
kubectl get svc

# No warning events on healthy pods
kubectl describe pod <pod-name>

# No crash output in logs
kubectl logs <pod-name>
```

## Expected Behavior

- Order Service Deployment: 2 replicas running, liveness and readiness probes passing.
- Payment Service: image pulls without error, secrets loaded from a Kubernetes Secret object.
- Services: correct label selectors, targetPorts matching container ports, nodePort in 30000-32767.
- ResourceQuota: applied to the namespace with realistic CPU and memory limits.

## Troubleshooting

**ImagePullBackOff:** The image name or tag in the Deployment YAML is incorrect. Check the exact
image name with `docker images` and update the manifest to match.

**CrashLoopBackOff:** Run `kubectl logs <pod-name> --previous` to see the last crash output. The
most common cause is a wrong environment variable or a missing ConfigMap/Secret reference.
