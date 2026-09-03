

Container core concepts

- how to build an image
- how to create container with resource limits
- how to use volumes
- how to use networks ( within host )


Why K8s?

Key Kubernetes (K8s) Features
Container Orchestration
Deploys and manages containers across multiple servers.
Automated Scheduling
Places Pods on suitable worker nodes based on resources and constraints.
Self-Healing
Restarts failed containers, replaces unhealthy Pods, and reschedules Pods when nodes fail.
Horizontal Scaling
Increases or decreases the number of Pods based on CPU, memory, or custom metrics.
Load Balancing and Service Discovery
Gives applications stable network identities and distributes traffic among healthy Pods.
Rolling Updates and Rollbacks
Updates applications gradually with minimal downtime and supports reverting to earlier versions.
Configuration Management
Stores application configuration using ConfigMaps.
Secret Management
Manages sensitive values such as passwords, tokens, and certificates using Secrets.
Storage Orchestration
Attaches persistent storage through Persistent Volumes and Persistent Volume Claims.
Resource Management
Controls CPU and memory through resource requests, limits, and quotas.
High Availability
Runs multiple application replicas across nodes to reduce downtime.
Declarative Management
You define the desired state in YAML; Kubernetes continuously works to maintain it.
Namespace-Based Isolation
Separates applications, environments, teams, and resources within a cluster.
Security and Access Control
Provides RBAC, ServiceAccounts, NetworkPolicies, and security contexts.
Extensibility
Supports custom resources, operators, plugins, and integrations with cloud-native tools.

In one sentence: Kubernetes automates the deployment, scaling, networking, recovery, configuration, and management of containerized applications.