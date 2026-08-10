# Screenshot Naming Convention

## Format

```
M{module}-{type}-{description}.png
```

### Examples

| Filename | When to Capture |
|----------|----------------|
| `M01-bug01-grid-fixed.png` | After fixing bug #1 in Module 01 |
| `M01-bug02-cart-mobile.png` | After fixing cart sidebar overlap on mobile |
| `M05-test-orders-pass.png` | After all order tests pass |
| `M24-docker-build-success.png` | After successful Docker build |
| `M29-kubectl-pods-running.png` | After K8s pods are running |
| `M32-grafana-dashboard.png` | After Grafana dashboard is configured |

## Type Codes

| Code | Meaning | When |
|------|---------|------|
| `bug{nn}` | Bug fix evidence | After fixing a specific bug |
| `enh{nn}` | Enhancement evidence | After completing an enhancement |
| `test` | Test results | After running test suites |
| `docker` | Docker evidence | After build/run/compose operations |
| `k8s` | Kubernetes evidence | After kubectl commands |
| `config` | Configuration | After config changes (Apache, Ansible, etc.) |
| `demo` | Demo screenshot | For capsule day presentations |

## What to Capture

### For Bug Fixes
1. The bug in action (before fixing) -- optional but helpful
2. The fixed behavior (after fixing) -- required
3. DevTools/console showing no errors -- for frontend bugs

### For Backend Fixes
1. Terminal output showing the fix works
2. API response (use Postman or curl)
3. Test output (if tests exist)

### For Infrastructure
1. Terminal command + output
2. Service status (systemctl, docker ps, kubectl get)
3. Dashboard/monitoring view

## How to Take Screenshots

- **Windows:** `Win + Shift + S` (Snipping Tool) or `PrtSc`
- **Mac:** `Cmd + Shift + 4`
- **Linux:** `PrtSc` or `gnome-screenshot`
- **Chrome DevTools:** Right-click element > "Capture node screenshot"

## Where to Save

Save all screenshots in your personal folder:
```
evidence/
  M01/
    M01-bug01-grid-fixed.png
    M01-bug02-cart-mobile.png
  M05/
    M05-bug01-discount-fixed.png
  ...
```
