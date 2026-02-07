# Todo Application Helm Chart

A Helm chart for deploying the Todo application with frontend and backend services to Kubernetes.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.2.0+
- Minikube (for local development)

## Dependencies

This chart has no external dependencies.

## Installing the Chart

To install the chart with the release name `todo-app`:

```bash
helm install todo-app .
```

The command deploys the Todo application on the Kubernetes cluster in the default configuration. The [configuration](#configuration) section lists the parameters that can be configured during installation.

## Uninstalling the Chart

To uninstall/delete the `todo-app` deployment:

```bash
helm delete todo-app
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Configuration

The following table lists the configurable parameters of the Todo App chart and their default values.

### Global Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imagePullSecrets` | Global Docker registry secret names as an array | `[]` |
| `global.storageClass` | Global storage class for dynamic provisioning | `""` |
| `global.namespaceOverride` | Override the deployment namespace | `""` |
| `global.env` | Environment name (used for labeling) | `"production"` |
| `global.logLevel` | Logging level | `"info"` |
| `global.enableDebug` | Enable debug features | `false` |
| `global.externalApiUrl` | URL for external API access | `""` |
| `global.config` | Additional configuration values | `{}` |

### Frontend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.replicaCount` | Number of frontend pods to run | `1` |
| `frontend.strategy.type` | Update strategy for frontend deployment | `RollingUpdate` |
| `frontend.strategy.rollingUpdate.maxUnavailable` | Max unavailable pods during rolling update | `0` |
| `frontend.strategy.rollingUpdate.maxSurge` | Max surge pods during rolling update | `1` |
| `frontend.image.repository` | Frontend image repository | `"taskflow-frontend"` |
| `frontend.image.tag` | Frontend image tag | `"latest"` |
| `frontend.image.pullPolicy` | Frontend image pull policy | `"IfNotPresent"` |
| `frontend.service.type` | Frontend service type | `ClusterIP` |
| `frontend.service.port` | Frontend service port | `80` |
| `frontend.resources.limits.cpu` | Frontend CPU resource limit | `"500m"` |
| `frontend.resources.limits.memory` | Frontend memory resource limit | `"512Mi"` |
| `frontend.resources.requests.cpu` | Frontend CPU resource request | `"100m"` |
| `frontend.resources.requests.memory` | Frontend memory resource request | `"128Mi"` |
| `frontend.env.API_URL` | Backend API URL for frontend | `"http://todo-backend:8000"` |
| `frontend.annotations` | Additional annotations for frontend deployment | `{}` |
| `frontend.podAnnotations` | Additional annotations for frontend pods | `{}` |
| `frontend.podLabels` | Additional labels for frontend pods | `{}` |
| `frontend.nodeSelector` | Node selector for frontend pods | `{}` |
| `frontend.tolerations` | Tolerations for frontend pods | `[]` |
| `frontend.affinity` | Affinity settings for frontend pods | `{}` |
| `frontend.securityContext` | Security context for frontend container | `{}` |
| `frontend.podSecurityContext` | Pod security context for frontend | `{}` |
| `frontend.priorityClassName` | Priority class name for frontend | `""` |
| `frontend.hostAliases` | Host aliases for frontend pods | `[]` |
| `frontend.lifecycle` | Lifecycle hooks for frontend container | `{}` |
| `frontend.livenessProbe` | Liveness probe configuration | `{}` |
| `frontend.readinessProbe` | Readiness probe configuration | `{}` |
| `frontend.startupProbe` | Startup probe configuration | `{}` |
| `frontend.extraEnv` | Extra environment variables | `[]` |
| `frontend.envFrom` | Environment variables from ConfigMap/Secret | `[]` |
| `frontend.serviceAccountName` | Service account name for frontend | `""` |
| `frontend.topologySpreadConstraints` | Topology spread constraints | `[]` |

### Backend Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.replicaCount` | Number of backend pods to run | `1` |
| `backend.strategy.type` | Update strategy for backend deployment | `RollingUpdate` |
| `backend.strategy.rollingUpdate.maxUnavailable` | Max unavailable pods during rolling update | `0` |
| `backend.strategy.rollingUpdate.maxSurge` | Max surge pods during rolling update | `1` |
| `backend.image.repository` | Backend image repository | `"taskflow-backend"` |
| `backend.image.tag` | Backend image tag | `"latest"` |
| `backend.image.pullPolicy` | Backend image pull policy | `"IfNotPresent"` |
| `backend.service.type` | Backend service type | `ClusterIP` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.resources.limits.cpu` | Backend CPU resource limit | `"1000m"` |
| `backend.resources.limits.memory` | Backend memory resource limit | `"1Gi"` |
| `backend.resources.requests.cpu` | Backend CPU resource request | `"250m"` |
| `backend.resources.requests.memory` | Backend memory resource request | `"256Mi"` |
| `backend.annotations` | Additional annotations for backend deployment | `{}` |
| `backend.podAnnotations` | Additional annotations for backend pods | `{}` |
| `backend.podLabels` | Additional labels for backend pods | `{}` |
| `backend.nodeSelector` | Node selector for backend pods | `{}` |
| `backend.tolerations` | Tolerations for backend pods | `[]` |
| `backend.affinity` | Affinity settings for backend pods | `{}` |
| `backend.securityContext` | Security context for backend container | `{}` |
| `backend.podSecurityContext` | Pod security context for backend | `{}` |
| `backend.priorityClassName` | Priority class name for backend | `""` |
| `backend.hostAliases` | Host aliases for backend pods | `[]` |
| `backend.lifecycle` | Lifecycle hooks for backend container | `{}` |
| `backend.livenessProbe` | Liveness probe configuration | `{}` |
| `backend.readinessProbe` | Readiness probe configuration | `{}` |
| `backend.startupProbe` | Startup probe configuration | `{}` |
| `backend.extraEnv` | Extra environment variables | `[]` |
| `backend.envFrom` | Environment variables from ConfigMap/Secret | `[]` |
| `backend.serviceAccountName` | Service account name for backend | `""` |
| `backend.topologySpreadConstraints` | Topology spread constraints | `[]` |

### Database Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `database.url` | Database connection URL | `""` |
| `database.secretName` | Name of secret containing database credentials | `""` |

### Secrets Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `secrets.openrouterApiKey` | OpenRouter API key | `""` |
| `secrets.jwtSecret` | JWT secret for authentication | `""` |
| `secrets.encryptionKey` | Encryption key for sensitive data | `""` |

### Pod Disruption Budget Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `pdb.enabled` | Enable Pod Disruption Budgets | `true` |
| `pdb.minAvailable` | Minimum number of pods available during disruptions | `1` |

### Horizontal Pod Autoscaler Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `hpa.enabled` | Enable Horizontal Pod Autoscaler | `false` |
| `hpa.minReplicas` | Minimum number of replicas | `1` |
| `hpa.maxReplicas` | Maximum number of replicas | `5` |
| `hpa.targetCPUUtilizationPercentage` | Target CPU utilization | `80` |
| `hpa.targetMemoryUtilizationPercentage` | Target memory utilization | `80` |

### Ingress Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress controller resource | `false` |
| `ingress.className` | Ingress class name | `""` |
| `ingress.annotations` | Ingress annotations | `{}` |
| `ingress.hosts[0].host` | Hostname to your Todo installation | `todo.example.com` |
| `ingress.hosts[0].paths[0].path` | Path within the host | `/` |
| `ingress.hosts[0].paths[0].pathType` | Path type | `Prefix` |
| `ingress.tls` | TLS configuration | `[]` |

### Node Affinity and Tolerations

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.nodeSelector` | Node labels for frontend pod assignment | `{}` |
| `frontend.tolerations` | Tolerations for frontend pods | `[]` |
| `frontend.affinity` | Affinity for frontend pods | `{}` |
| `backend.nodeSelector` | Node labels for backend pod assignment | `{}` |
| `backend.tolerations` | Tolerations for backend pods | `[]` |
| `backend.affinity` | Affinity for backend pods | `{}` |

## Customizing Values

You can customize the deployment by providing a custom values file:

```bash
helm install todo-app -f my-values.yaml .
```

Or by setting individual values:

```bash
helm install todo-app --set frontend.replicaCount=2 --set backend.replicaCount=2 .
```

## Environment-Specific Configurations

The chart includes sample values files for different environments:

- `values-dev.yaml`: Optimized for development
- `values-staging.yaml`: Optimized for staging
- `values-prod.yaml`: Optimized for production

To deploy with environment-specific values:

```bash
# For development
helm install todo-dev -f values-dev.yaml .

# For staging
helm install todo-staging -f values-staging.yaml .

# For production
helm install todo-prod -f values-prod.yaml .
```

## Health Checks

The chart includes liveness and readiness probes for both frontend and backend services:
- Frontend: Checks `/health` endpoint
- Backend: Checks `/api/health` endpoint

## Security Considerations

- Sensitive data is stored in Kubernetes Secrets
- Resource limits are enforced to prevent resource exhaustion
- Pod Disruption Budgets ensure availability during maintenance
- Rolling updates prevent downtime during deployments

## Upgrading

To upgrade the chart to a new version:

```bash
helm upgrade todo-app .
```

The chart supports zero-downtime upgrades using rolling update strategy.

## Local Development with Minikube

For local development using Minikube:

1. Start Minikube:
```bash
minikube start --memory=4g --cpus=2
```

2. Load your Docker images into Minikube:
```bash
minikube image load taskflow-frontend:latest
minikube image load taskflow-backend:latest
```

3. Install the chart with NodePort services:
```bash
helm install todo-local . -f values-minikube.yaml
```

4. Access the services:
```bash
minikube service todo-local-frontend
```

Where `values-minikube.yaml` contains:
```yaml
frontend:
  service:
    type: NodePort
    port: 80
  resources:
    limits:
      cpu: "500m"
      memory: "256Mi"
    requests:
      cpu: "100m"
      memory: "128Mi"

backend:
  service:
    type: NodePort
    port: 8000
  resources:
    limits:
      cpu: "750m"
      memory: "512Mi"
    requests:
      cpu: "200m"
      memory: "256Mi"
```

## AI-Assisted Kubernetes Operations

This deployment supports AI-assisted Kubernetes operations using kubectl-ai and kagent:

### Using kubectl-ai for Natural Language Commands

You can use natural language to manage your deployment:

```bash
# Deploy the frontend with 2 replicas
kubectl ai "deploy the todo frontend with 2 replicas"

# Scale the backend to handle more load
kubectl ai "scale the backend deployment to 3 replicas"

# Check why pods are failing
kubectl ai "check why the pods are failing"

# Get resource usage
kubectl ai "show me the CPU and memory usage of all pods"

# Create a new service
kubectl ai "create a service for the todo backend that exposes port 8000"

# Update configuration
kubectl ai "update the frontend environment variable API_URL to point to the backend service"
```

### Using kagent for Advanced Operations

For more complex operations, use kagent:

```bash
# Analyze cluster health
kagent "analyze the cluster health and report any issues"

# Optimize resource allocation
kagent "optimize resource allocation for the todo-app deployments"

# Troubleshoot issues
kagent "troubleshoot why the frontend pods are restarting frequently"

# Security analysis
kagent "perform a security analysis of the todo-app namespace"
```

### Prerequisites for AI Tools

To use kubectl-ai and kagent, you need to have them installed:

1. Install kubectl-ai plugin:
```bash
# Follow the installation instructions from the kubectl-ai documentation
kubectl krew install ai
```

2. Install kagent (if available in your environment):
```bash
# Installation varies by environment
# Check your system documentation for kagent installation
```

Once installed, you can use natural language to manage your Kubernetes resources instead of remembering complex kubectl commands.