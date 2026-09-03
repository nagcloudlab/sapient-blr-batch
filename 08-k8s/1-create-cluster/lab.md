### install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/kubectl
kubectl version --client
```

### install kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind
kind version
```

### create k8s cluster

```bash
kind create cluster --config kind-k8s-cluster.yaml --name psi-k8s-cluster
```

### verify the cluster

```bash
kubectl cluster-info --context kind-psi-k8s-cluster
kubectl get nodes -o wide
```

### delete the cluster

```bash
kind delete cluster --name psi-k8s-cluster
```



### list k8s api versions

```bash
kubectl api-versions
kubectl api-resources
```

### list namespaces

```bash
kubectl get namespaces
```

### create namespace

```bash
kubectl create namespace psi-tng
```

### configure kubectl to use the namespace

```bash
kubectl config set-context --current --namespace=psi-tng
```

### delete namespace
```bash
kubectl delete namespace psi-tng
```

### list all the resources in the current namespace

```bash
kubectl get all
```