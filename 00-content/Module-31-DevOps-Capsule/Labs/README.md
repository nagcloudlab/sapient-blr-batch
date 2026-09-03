# Module 31: DevOps Capsule -- Lab Setup

## Prerequisites

- Docker Desktop (with docker compose)
- Jenkins (Docker-based from Module 28)
- kubectl and minikube (from Module 29)
- Ansible (from Module 30)
- All tools from Modules 24-30 must be working before starting this capsule

## Running the Starter Code

This is an integration capsule -- there is no single "run" command. Follow `Project/BRIEF.md` for
the full project sequence:

1. Build and push Docker images for all FoodExpress services.
2. Start the full stack with `docker compose up` and verify locally.
3. Run the Jenkins pipeline end-to-end (build > test > containerise > push).
4. Deploy to minikube with `kubectl apply -f manifests/`.
5. Run the Ansible playbook to configure the monitoring host.

## Verifying Your Work

```bash
# Step 1 -- Compose stack healthy
docker compose ps       # All services Running

# Step 2 -- Jenkins pipeline
# Check Stage View: all stages green

# Step 3 -- Kubernetes deployment
kubectl get pods        # All pods Running
kubectl get svc         # Services accessible

# Step 4 -- End-to-end API test
curl http://$(minikube ip):30080/api/health
```

## Expected Behavior

- Full pipeline runs: code commit triggers build, tests pass, image is pushed, deployed to K8s.
- All services reachable through the Kubernetes NodePort service.
- Ansible playbook deploys Prometheus/Grafana config without errors.
- `Project/CHECKLIST.md` items are all ticked.

## Troubleshooting

**Start with one service end-to-end first:** Get the Order Service through the full pipeline before
adding others. Debugging one service at a time is faster than debugging the full stack at once.

**minikube cannot pull local images:** Run `eval $(minikube docker-env)` before building images so
they are built directly into minikube's Docker daemon.
