

install ingress controller in kind k8s cluster
```bash
kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
```

deploy foo & bar app

```bash
kubectl apply -f foo-bar-apps.yaml
kubectl get pods
kubectl get svc
```
