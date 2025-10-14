---
title: "Self-hosted KernelCI Architecture Documentation"
date: 2025-08-06
description: "Overview for self-hosted KernelCI"
weight: 10
---

# Self-hosted KernelCI from DevOps Perspective

This document provides an overview of the architecture and deployment of a self-hosted KernelCI instance, focusing on DevOps aspects. It covers infrastructure setup, deployment options, configuration, and maintenance strategies.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Infrastructure Components](#infrastructure-components)
3. [Deployment Options](#deployment-options)
   - [Docker Compose Deployment](#docker-compose-deployment)
   - [Kubernetes Deployment](#kubernetes-deployment)
4. [Configuration](#configuration)
5. [KCIDB-NG Deployment](#kcidb-ng-deployment)
   - [Architecture Overview](#architecture-overview-1)
   - [Deployment Options](#deployment-options-1)
   - [Database Management](#database-management)
   - [Production Considerations](#production-considerations)
   - [Troubleshooting](#troubleshooting)
6. [Resources and References](#resources-and-references)

---

## Architecture Overview

A self-hosted KernelCI instance consists of two main independent components:

### 1. Maestro
**Purpose**: Orchestrates git checkout, kernel builds, testing jobs, and manages the overall workflow.

**Components**:
- **API Service**:
  - Core RESTful API for system interaction
  - Built with Python and FastAPI framework
  - Uses Beanie ODM for MongoDB document management
  - Authentication via fastapi-users with JWT tokens
  - Dependencies: MongoDB (data storage), Redis (Pub/Sub messaging)
  - Versioned API with /latest and /v0 endpoints

- **Pipeline Service**:
  - Orchestrates kernel builds and test jobs
  - Manages workflow across build systems and test frameworks
  - Sub-components:
    - Checkout trigger
    - Schedulers (Kubernetes, Shell, Docker, LAVA)
    - Tarball manager
  - Requirements: Access to Maestro API and artifact storage

### 2. KCIDB
**Purpose**: Database and services for storing and processing test results.

**Components**:
- **PostgreSQL Database**: Stores test results, build information, and metadata
- **KCIDB-NG**:
  - REST service built with Rust (kcidb-restd-rs)
  - Receives test results from labs via HTTP/HTTPS
  - Ingester (Python) processes and stores results in PostgreSQL
  - LogSpec worker identifies issues and creates incidents from logs
- **Web Dashboard**:
  - React + TypeScript frontend
  - Django + DRF backend
  - Provides visualization and analysis of test results

---

## Infrastructure Components

### Required Infrastructure

#### For Maestro API:
- **Container Runtime**: Docker or Kubernetes cluster
- **Databases**:
  - MongoDB 5.0+ (API data storage)
  - Redis 6.2+ (pub/sub messaging)
- **Storage**: HTTP-based or SSH-based artifact storage (optional nginx container for local development)
- **Python**: Python 3.8+ with FastAPI, Beanie, fastapi-users
- **Build Infrastructure**: Kubernetes cluster for running builds (managed separately by kernelci-pipeline)

#### For KCIDB:
- **Database**: PostgreSQL instance
- **Processing Services**: KCIDB-NG, Ingester, LogSpec

---

## Deployment Options

### Docker Compose Deployment

**Best for**: Development, testing, and small to medium setups

#### Prerequisites
- Docker and Docker Compose installed on your server

#### Setup Steps

1. **Clone Required Repositories**
   ```bash
   # For API service
   git clone https://github.com/kernelci/kernelci-api
   cd kernelci-api

   # For Pipeline service
   git clone https://github.com/kernelci/kernelci-pipeline
   cd kernelci-pipeline
   ```

   **Note**: The kernelci-api and kernelci-pipeline are separate repositories and can be deployed independently. However, kernelci-pipeline requires a running kernelci-api instance to function.

2. **Configure Environment Variables**

   **For kernelci-api**:
   ```bash
   cd kernelci-api
   cp env.sample .env

   # Edit .env and add required configuration:
   # - SECRET_KEY: Secret key for JWT token signing (required)
   # - MONGO_SERVICE: MongoDB connection string (default: mongodb://db:27017)
   # - REDIS_HOST: Redis host (default: redis)
   # - SMTP settings for email (optional)
   ```

   **For kernelci-pipeline**:
   ```bash
   cd kernelci-pipeline
   touch .env

   # Add required environment variables:
   # - KCI_API_TOKEN: API token for authentication with kernelci-api
   # - KCI_SETTINGS: Path to configuration file (default: /home/kernelci/config/kernelci.toml)
   # - KCIDB_REST: KCIDB REST API endpoint (optional, for sending results to KCIDB)
   # - LAVA_CALLBACK_PORT: Port for LAVA callback service (default: 8100)
   ```

   Edit `config/kernelci.toml` to configure:
   - API endpoint connection
   - Storage configuration
   - Scheduler settings
   - LAVA runtime tokens (in separate secrets file)

3. **Create Admin User (API only)**
   After starting kernelci-api services, create an admin user:
   ```bash
   docker exec -it kernelci-api python3 /scripts/setup_admin_user
   ```

4. **Launch Services**

   **kernelci-api** docker-compose files:
   - `docker-compose.yaml` - Base services (production images)
   - `dev-docker-compose.yaml` - Development with local builds and volume mounts
   - `test-docker-compose.yaml` - Testing environment

   **kernelci-pipeline** docker-compose files:
   - `docker-compose.yaml` - Main pipeline services (monitor, scheduler, tarball, trigger, timeout, patchset, job-retry)
   - `docker-compose-lava.yaml` - LAVA callback service
   - `docker-compose-kcidb.yaml` - KCIDB integration service
   - `docker-compose-production.yaml` - Production-specific overrides for lava-callback

   **Pipeline services include**:
   - **monitor**: Prints API events for debugging and monitoring
   - **scheduler**: Manages job submission to shell runtime
   - **scheduler-docker**: Manages job submission to Docker runtime
   - **scheduler-lava**: Manages job submission to multiple LAVA labs
   - **scheduler-k8s**: Manages job submission to Kubernetes clusters
   - **tarball**: Creates and uploads kernel source tarballs
   - **trigger**: Monitors git repositories and triggers builds on new commits
   - **timeout**: Handles job timeouts
   - **timeout-closing**: Closes timed-out jobs
   - **timeout-holdoff**: Manages holdoff periods for jobs
   - **patchset**: Handles patchset testing from mailing lists
   - **job-retry**: Retries failed jobs
   - **lava-callback**: Receives HTTP callbacks from LAVA labs with test results AND provides REST API for pipeline control (custom checkouts, patchset testing, job retries, etc.)

   **Prepare data directories** (required for pipeline services):
   ```bash
   cd kernelci-pipeline

   # Create required directories
   mkdir -p data/output
   mkdir -p data/src
   mkdir -p data/ssh
   mkdir -p data/k8s-credentials/.kube
   mkdir -p data/k8s-credentials/.config/gcloud
   mkdir -p data/k8s-credentials/.azure
   mkdir -p logs

   # For SSH-based storage, add SSH key
   cp ~/.ssh/storage_key data/ssh/id_rsa_tarball
   chmod 600 data/ssh/id_rsa_tarball

   # For Kubernetes schedulers, add k8s credentials
   cp ~/.kube/config data/k8s-credentials/.kube/config
   # For GKE: copy gcloud credentials
   # For AKS: copy Azure credentials
   ```

   **Starting services**:
   ```bash
   # Start all pipeline services
   docker-compose up -d

   # Start LAVA callback service
   docker-compose -f docker-compose-lava.yaml up -d

   # Start KCIDB integration
   docker-compose -f docker-compose-kcidb.yaml up -d

   # Check service status
   docker-compose ps

   # View logs
   docker-compose logs -f
   ```

   **Note**:
   - The `data/` directory is mounted into containers and stores git checkouts, build artifacts, and temporary files
   - The `logs/` directory contains service logs for debugging
   - Each scheduler mounts only the volumes it needs (see docker-compose.yaml for details)

#### Custom Docker Images

By default, Docker Compose uses pre-built images from Docker Hub. For production or customized setups, you may want to build your own images.

**Available Image Types**:

1. **Compiler Images** - For building kernels across different architectures:
   - Architectures: arc, arm, armv5, arm64, x86, mips, riscv64
   - Compilers: clang-15, clang-17, gcc-12
   - Includes: kselftest, kernelci tools

2. **Miscellaneous Images**:
   - `kernelci` - Base KernelCI tools image
   - `kernelci api` - API service image
   - `kernelci pipeline` - Pipeline service image
   - `kernelci lava-callback` - LAVA callback handler
   - `k8s kernelci` - Kubernetes integration image
   - `qemu` - QEMU emulation environment
   - `buildroot kernelci` - Buildroot-based images
   - `debos kernelci` - Debian OS builder
   - `gcc-12 kunit kernelci` - KUnit testing with GCC
   - `rustc-1.74/1.75 kselftest kernelci` - Rust toolchain images

**Building Custom Images**:

Using the `kci` command-line tool from kernelci-core:

```bash
# Clone repositories
git clone https://github.com/kernelci/kernelci-core
git clone https://github.com/kernelci/kernelci-api
git clone https://github.com/kernelci/kernelci-pipeline

# Install kernelci-core tools
cd kernelci-core
python3 -m pip install '.[dev]'
sudo cp -R config /etc/kernelci/

# Build a compiler image for specific architecture
export core_rev=$(git rev-parse HEAD)
export core_url=$(git remote get-url origin)
./kci docker build --verbose --build-arg core_rev=$core_rev \
    --build-arg core_url=$core_url \
    clang-17 kselftest kernelci --arch arm64

# Build service images (API, Pipeline, etc.)
cd ../kernelci-core
core_rev=$(git rev-parse HEAD)
cd ../kernelci-api
api_rev=$(git rev-parse HEAD)
cd ../kernelci-pipeline
pipeline_rev=$(git rev-parse HEAD)
cd ../kernelci-core

# Build API image
./kci docker build --verbose \
    --build-arg core_rev=$core_rev \
    --build-arg api_rev=$api_rev \
    --build-arg pipeline_rev=$pipeline_rev \
    kernelci api

# Build Pipeline image
./kci docker build --verbose \
    --build-arg core_rev=$core_rev \
    --build-arg api_rev=$api_rev \
    --build-arg pipeline_rev=$pipeline_rev \
    kernelci pipeline
```

**Image Naming Convention**:

Images are tagged based on branch and registry:
- **Main branch**: `ghcr.io/kernelci/<image-name>` or `kernelci/<image-name>`
- **Other branches**: `ghcr.io/kernelci/staging-<image-name>` or `kernelci/staging-<image-name>`

**Pushing to Registries**:

```bash
# Push to GitHub Container Registry
./kci docker build --verbose --push --prefix=ghcr.io/kernelci/ kernelci api

# Get image name and tag for Docker Hub
NAME=$(./kci docker name --prefix=ghcr.io/kernelci/ kernelci api)
DHNAME=$(./kci docker name --prefix=kernelci/ kernelci api)
docker tag $NAME $DHNAME
docker push $DHNAME
```

**Automated Builds**:

The project uses GitHub Actions for automated image building:
- **Workflow**: `.github/workflows/docker_images.yml`
- **Triggered by**: Authorized maintainers
- **Builds**: Both compiler and miscellaneous images
- **Registries**: GitHub Container Registry (ghcr.io) and Docker Hub

**Prerequisites for Building**:
- Docker installed and running
- Python 3 with pip
- Git read-only access to kernelci repositories
- Docker registry credentials (for pushing)

**Reference**:
- Workflow file: https://github.com/kernelci/kernelci-core/blob/main/.github/workflows/docker_images.yml
- Full list of supported architectures and compilers in workflow matrix

---

### Kubernetes Deployment

**Best for**: Production environments and larger setups

#### Current Status
- Production deployment uses Azure AKS
- **kernelci-api**: Basic Kubernetes manifests available in `kube/aks/` directory of kernelci-api repository
- **kernelci-pipeline**: Kubernetes manifests available in `kube/aks/` directory (production AKS-specific deployments)
- Full deployment automation (Helm charts and scripts) managed in separate [kernelci-deploy](https://github.com/kernelci/kernelci-deploy) repository
- AKS manifests are currently Azure-specific (adaptation needed for other providers)

#### Prerequisites

1. **Kubernetes Cluster**
   - Any Kubernetes provider supported (production reference: Azure AKS)
   - For Azure: Resource Group and cluster created via `az` CLI
   - kubectl configured with cluster context
   - Helm 3 installed

2. **Required Tools**
   - `kubectl` - Kubernetes CLI
   - `helm` - Kubernetes package manager (v3+)
   - `yq` (Mike Farah's Go version v4.35.2+) - YAML processor
   - For Azure: `az` CLI configured and authenticated

3. **Configuration Files**

   You need to prepare the following configuration files before deployment:

   **a) deploy.cfg**

   Main configuration file containing sensitive deployment parameters:

   ```bash
   export API_TOKEN="<token-for-pipeline-to-api-authentication>"
   export MONGO="<mongodb-connection-string>"
   export API_SECRET_KEY="<secret-for-jwt-signing>"
   export EMAIL_USER="<email-sender-address>"
   export EMAIL_PASSWORD="<email-password>"
   export KCIDB_REST="<kcidb-rest-endpoint-url>"
   export IP_API="<optional-static-ip-for-api>"
   export IP_PIPELINE="<optional-static-ip-for-pipeline>"
   ```

   **Note**: For Azure deployments, `IP_API` and `IP_PIPELINE` can be auto-allocated on first run.

   **b) kernelci-secrets.toml**

   Pipeline secrets configuration (see Configuration section for details). This is specific to kernelci-pipeline.

   Important sections include:
   - `[jwt]` - Secret for signing JWT tokens for pipeline API
   - `[storage.<name>]` - Storage credentials for different storage backends
   - `[runtime.lava-<name>]` - LAVA lab runtime tokens and callback tokens
   - `[send_kcidb]` - KCIDB PostgreSQL credentials (if using KCIDB integration)

   **c) k8s.tgz**

   Tarball containing Kubernetes credentials for build clusters (used by kernelci-pipeline):
   - `k8s-credentials/.kube/config` - Kubernetes config file
   - For GKE: `k8s-credentials/.config/gcloud/` - gcloud credentials
   - For AKS: `k8s-credentials/.azure/` - Azure CLI credentials

   **d) id_rsa**

   SSH private key for artifact storage access (SSH-based storage only)

   **Note**: The kernelci-api service primarily requires only the `deploy.cfg` with MongoDB and Redis connection strings. The other files (b, c, d) are for kernelci-pipeline integration.

4. **Deployment Script Variables**

   Edit `api-pipeline-deploy.sh` to customize for your environment:

   ```bash
   # Azure-specific (unset if not using Azure)
   AZURE_RG="kernelci-api-1_group"        # Azure resource group
   LOCATION="westus3"                      # Azure region

   # Cluster configuration
   CONTEXT="kernelci-api-1"                # kubectl context name
   CLUSTER_NAME="kernelci-api-1"           # Cluster name

   # Namespace and DNS configuration
   NS_PIPELINE="kernelci-pipeline"         # Pipeline namespace
   DNS_PIPELINE="kernelci-pipeline"        # Pipeline DNS label
   NS_API="kernelci-api"                   # API namespace
   DNS_API="kernelci-api"                  # API DNS label

   # TLS certificate configuration
   ACME="staging"                          # Use "staging" for testing, "production" for live

   # Repository branch
   BRANCH="main"                           # Git branch to deploy
   ```

#### Initial Deployment

**Azure-Specific Setup**

For Azure AKS deployments, the script automates several Azure-specific tasks:

1. **Static IP Allocation**:
   ```bash
   # Automatically creates public IPs on first run
   az network public-ip create --resource-group $AZURE_RG \
       --name ${DNS_API}-ip --sku Standard \
       --allocation-method static --location $LOCATION
   ```

2. **DNS Configuration**:
   - Automatically assigns FQDN: `${DNS_API}.${LOCATION}.cloudapp.azure.com`
   - Updates ingress manifests with correct hostnames

3. **RBAC Permissions**:
   - Grants cluster Network Contributor role to manage public IPs
   - Required for ingress controller to attach static IPs

4. **Load Balancer Configuration**:
   - Uses Azure Standard Load Balancer SKU
   - Configures annotations for Azure-specific features

**Deployment Steps**

1. **Clone Deployment Repository**
   ```bash
   git clone https://github.com/kernelci/kernelci-deploy
   cd kernelci-deploy/kubernetes
   ```

2. **Prepare Configuration Files**
   ```bash
   # Create deploy.cfg from example
   cp deploy.cfg.example deploy.cfg
   # Edit deploy.cfg with your values
   vim deploy.cfg

   # Prepare kernelci-secrets.toml
   cp kernelci-secrets.toml.example kernelci-secrets.toml
   vim kernelci-secrets.toml

   # Prepare k8s credentials tarball
   tar czf k8s.tgz -C /path/to/credentials .kube .azure

   # Copy SSH key for storage (if using SSH storage)
   cp ~/.ssh/storage_key id_rsa
   ```

3. **Run Initial Deployment**
   ```bash
   # Full deployment
   ./api-pipeline-deploy.sh full
   ```

   This script performs the following operations:
   - Downloads required tools (yq, helm) if missing
   - Clones kernelci-api and kernelci-pipeline repositories
   - Creates or recreates namespaces (kernelci-api, kernelci-pipeline)
   - Updates all manifests with correct namespace configuration
   - **(Azure only)** Allocates static public IPs
   - **(Azure only)** Configures DNS names and FQDN
   - **(Azure only)** Assigns RBAC permissions for IP management
   - Installs cert-manager for TLS certificates
   - Deploys ingress-nginx controllers (separate per namespace)
   - Creates Kubernetes secrets (API tokens, credentials, TOML config, k8s credentials)
   - Deploys MongoDB and Redis (for kernelci-api)
   - Deploys kernelci-api service
   - Deploys kernelci-pipeline components:
     - **trigger**: Monitors git repositories and triggers builds on new commits
     - **tarball**: Creates and uploads kernel source tarballs
     - **monitor**: Prints API events for debugging and monitoring
     - **scheduler-shell**: Manages job submission to shell runtime
     - **scheduler-k8s**: Manages job submission to Kubernetes build clusters
     - **scheduler-lava**: Manages job submission to LAVA labs
     - **timeout**: Handles job timeout management
     - **timeout-closing**: Closes timed-out jobs
     - **timeout-holdoff**: Manages holdoff periods for jobs
     - **test-report**: (Deprecated, will be removed)
     - **regression-tracker**: (Deprecated, will be removed)
     - **lava-callback**: Receives HTTP callbacks from LAVA labs with test results
     - **pipeline-kcidb**: Sends test results to KCIDB
     - **kcidb-postgres-proxy**: (Deprecated, will be removed)
   - Configures cert-manager ClusterIssuer for Let's Encrypt
   - Deploys ingress resources with TLS (lava-callback endpoint exposed via ingress)

4. **Verify Deployment**
   ```bash
   # Check API namespace
   kubectl --context=kernelci-api-1 get pods -n kernelci-api

   # Check Pipeline namespace
   kubectl --context=kernelci-api-1 get pods -n kernelci-pipeline

   # Test API endpoint (Azure)
   curl https://kernelci-api.westus3.cloudapp.azure.com/latest/

   # Test Pipeline callback endpoint
   curl https://kernelci-pipeline.westus3.cloudapp.azure.com/
   ```

5. **Post-Deployment Configuration**

   After initial deployment, you need to create admin user and API tokens:

   ```bash
   # Create admin user (run inside API pod)
   # The setup_admin_user script is from kernelci-api repository at scripts/setup_admin_user
   kubectl exec -it -n kernelci-api <api-pod-name> -- \
       python3 /scripts/setup_admin_user

   # Generate API token through API or admin interface
   # Update deploy.cfg with API_TOKEN

   # Deploy pipeline credentials with token (for pipeline integration)
   ./api-pipeline-deploy.sh pipeline-credentials
   ```

#### Ingress Controller Configuration

The deployment uses separate ingress-nginx controllers for each namespace:

**API Ingress** (kernelci-api namespace):
```bash
helm install ingress-nginx ingress-nginx/ingress-nginx \
    -n kernelci-api \
    --set controller.replicaCount=1 \
    --set controller.service.loadBalancerIP="${IP_API}" \
    --set controller.ingressClassResource.name=ingressclass-api \
    --set controller.scope.enabled=true \
    --set controller.scope.namespace=kernelci-api
```

**Pipeline Ingress** (kernelci-pipeline namespace):
```bash
helm install ingress-nginx2 ingress-nginx/ingress-nginx \
    -n kernelci-pipeline \
    --set controller.service.loadBalancerIP="${IP_PIPELINE}" \
    --set controller.ingressClassResource.name=ingressclass-pipeline \
    --set controller.scope.enabled=true \
    --set controller.scope.namespace=kernelci-pipeline \
    --set controller.service.annotations."nginx\.ingress\.kubernetes\.io/proxy-body-size"="128m"
```

**Key Features**:
- **Namespace Isolation**: Each ingress controller is scoped to its namespace
- **Static IPs**: Pre-allocated static IPs for stable DNS configuration
- **Azure Integration** (Azure only): Automatic DNS label assignment
- **Large Payloads**: Pipeline ingress configured for 128MB body size (LAVA callbacks with large log files)

**Pipeline Ingress Exposes**:
- **lava-callback service**: Receives HTTP callbacks from LAVA labs on port 8000
  - Path: `/` (all requests routed to lava-callback)
  - Used by LAVA labs to report test results
  - Requires valid JWT token in Authorization header

**Non-Azure Deployments**:
For non-Azure providers, you need to:
1. Manually allocate static IPs or use LoadBalancer-assigned IPs
2. Remove Azure-specific annotations from Helm values
3. Configure DNS manually to point to ingress IPs
4. Update `update_fqdn` function or skip it entirely

#### MongoDB Configuration

**Local MongoDB** (default in manifests):
- Deployed as a single pod with persistent volume
- Suitable for testing and small deployments

**External MongoDB** (recommended for production):
```bash
# Set MONGO in deploy.cfg to external MongoDB connection string
export MONGO="mongodb://user:pass@mongo-host:27017/kernelci?authSource=admin"
```

For production, consider:
- MongoDB Atlas (managed service)
- Self-hosted MongoDB replica set
- Azure Cosmos DB with MongoDB API (Azure deployments)

#### TLS Certificates

The deployment uses cert-manager with Let's Encrypt:

**Staging Environment** (default, for testing):
```bash
ACME="staging"
```
- Uses Let's Encrypt staging servers
- Avoids rate limits during testing
- Certificates will show browser warnings

**Production Environment**:
```bash
ACME="production"
```
- Uses Let's Encrypt production servers
- Valid certificates trusted by browsers
- Subject to rate limits (50 certificates per domain per week)

**Certificate Issuer Configuration**:
The script creates a ClusterIssuer with ACME DNS01 challenges configured for both API and Pipeline domains.

#### Production Updates

**Update Methods**:

1. **Automated Updates** (Recommended):
   - Workflow: https://github.com/kernelci/kernelci-core/blob/main/.github/workflows/production.yml
   - Triggered automatically on commits or manually by maintainers

2. **Manual Updates**:
   ```bash
   ./api-production-update.sh
   ```

**Update Process**:

The update script performs the following steps:

1. **Clone Fresh Repositories**:
   ```bash
   git clone https://github.com/kernelci/kernelci-core
   git clone https://github.com/kernelci/kernelci-api
   git clone https://github.com/kernelci/kernelci-pipeline
   ```

2. **Build and Push Docker Images**:
   - Builds latest images from main branch
   - Tags with sha256 digests for immutable deployments
   - Pushes to Docker Hub (kernelci/* namespace)

   Images built:
   - `kernelci/kernelci:api@sha256:...`
   - `kernelci/kernelci:pipeline@sha256:...`
   - `kernelci/kernelci:lava-callback@sha256:...`

3. **Update Kubernetes Manifests**:
   Uses `yq` to update image references with new sha256 digests:
   ```bash
   ./yq e ".spec.template.spec.containers[0].image = \
       \"kernelci/kernelci:api@$SHA256\"" -i api.yaml
   ```

4. **Update Configuration**:
   - Pulls latest kernelci-pipeline/config
   - Updates pipeline-configmap in Kubernetes

5. **Apply to Cluster**:
   ```bash
   kubectl apply --namespace kernelci-api -f api.yaml
   kubectl apply --namespace kernelci-pipeline -f pipeline-manifests/
   ```

6. **Verification**:
   ```bash
   # Check pod status
   kubectl get pods -n kernelci-api
   kubectl get pods -n kernelci-pipeline

   # Check for restarts or errors
   kubectl describe pod <pod-name> -n <namespace>

   # Check logs if issues
   kubectl logs <pod-name> -n <namespace>
   ```

#### Deployment Management Commands

The `api-pipeline-deploy.sh` script provides several management commands:

```bash
# Configuration management
./api-pipeline-deploy.sh config [dir]              # Update pipeline configmap
./api-pipeline-deploy.sh backup-config             # Backup pipeline configmap
./api-pipeline-deploy.sh pipeline-configmap        # Redeploy configmap only

# Credentials and secrets
./api-pipeline-deploy.sh token                     # Update API token
./api-pipeline-deploy.sh pipeline-credentials      # Update pipeline secrets
./api-pipeline-deploy.sh deploy_secret_toml_only   # Update kernelci-secrets.toml
./api-pipeline-deploy.sh retrieve_secrets_toml     # Extract current TOML
./api-pipeline-deploy.sh retrieve_k8s_credentials  # Extract k8s credentials
./api-pipeline-deploy.sh update_k8s_credentials    # Update with k8s-new.tgz

# Pod management
./api-pipeline-deploy.sh api-restart-pods          # Restart all API pods
./api-pipeline-deploy.sh pipeline-restart-pods     # Restart all pipeline pods

# MongoDB operations
./api-pipeline-deploy.sh backup-mongo              # Backup MongoDB
./api-pipeline-deploy.sh mongo-shell               # Access MongoDB shell

# Infrastructure
./api-pipeline-deploy.sh cert                      # Update cert-manager issuer
./api-pipeline-deploy.sh patch-nginx               # Patch nginx for large payloads

# Cleanup
./api-pipeline-deploy.sh delete                    # Delete all namespaces
```

#### Creating Build Clusters (Azure)

For Azure deployments, use `create_kci_k8s_azure_build.sh` to create dedicated build clusters:

```bash
# Create full build cluster with spot instances
./create_kci_k8s_azure_build.sh full
```

This creates:
- **Resource Group**: `rg-kbuild-westus3`
- **Cluster**: `aks-kbuild-medium-1`
- **Control Plane**: 1x Standard_D2as_v5 (permanent)
- **Spot Node Pool**: Up to 13x Standard_D8as_v5 (auto-scaling, 0-13 nodes)
- **Spot Price Cap**: $0.04/hour per node
- **Auto-scaling**: Scales to 0 when idle

**Features**:
- **Spot Instances**: 70-90% cost savings vs regular VMs
- **Auto-scaling**: Scales down to 0 nodes when no builds running
- **Eviction Policy**: Graceful deletion on spot eviction
- **Kubernetes Secrets**: Automatically installs API tokens

**Secrets Installation**:
```bash
# Install/update secrets only
./create_kci_k8s_azure_build.sh secrets
```

Required secrets in `secrets/` directory:
- `token-staging-api` - API token for staging
- `token-early-access` - API token for early access
- `azure_sas_staging` - Azure SAS token for storage

#### Troubleshooting

**Common Issues**:

1. **Pods not starting**:
   ```bash
   kubectl describe pod <pod-name> -n <namespace>
   kubectl logs <pod-name> -n <namespace>
   ```

2. **Ingress not getting IP**:
   - Check LoadBalancer service status
   - For Azure: Verify RBAC permissions
   - Check cloud provider integration

3. **Certificate issues**:
   ```bash
   kubectl describe certificate -n <namespace>
   kubectl logs -n cert-manager <cert-manager-pod>
   ```

4. **Pipeline not connecting to API**:
   - Verify API_TOKEN in secrets
   - Check API service accessibility from pipeline pods
   - Review pipeline pod logs for authentication errors

5. **Large LAVA callbacks failing**:
   ```bash
   ./api-pipeline-deploy.sh patch-nginx
   ```

**Azure-Specific Issues**:

1. **Static IP not attaching**:
   - Verify Network Contributor role assigned to cluster identity
   - Check IP resource group matches cluster resource group
   - Ensure IP is in same region as cluster

2. **DNS not resolving**:
   - Verify DNS label is unique in the region
   - Check Azure Portal for Public IP DNS configuration
   - Allow time for DNS propagation (5-10 minutes)

#### Migration from Docker Compose

When migrating from Docker Compose to Kubernetes:

1. **Export Data**:
   - Backup MongoDB data
   - Export configuration files
   - Document current settings

2. **Deploy to Kubernetes**:
   - Follow initial deployment steps
   - Import MongoDB backup
   - Configure with existing settings

3. **Verify**:
   - Test all API endpoints
   - Verify pipeline triggers
   - Check LAVA callback functionality

4. **Cutover**:
   - Update DNS to point to Kubernetes ingress
   - Monitor for issues
   - Keep Docker Compose as rollback option initially

---

## Configuration

### Kubernetes Builder Configuration

**Requirements**:
- Kubernetes cluster for running builds
- Multiple clusters supported
- Build pods need:
  - Access to Maestro API
  - Upload permissions to artifact storage

### Storage Configuration

**Supported Storage Types**:

1. **HTTP-based Storage** (Recommended)
   - Custom storage server: https://github.com/kernelci/kernelci-storage
   - Backend options:
     - Azure Blob Storage
     - Plain filesystem

2. **SSH-based Storage** (Not recommended for production)
   - Less tested
   - Limited support

### LAVA Lab Configuration

The pipeline supports submitting jobs to multiple LAVA (Linaro Automated Validation Architecture) labs and receiving results via HTTP callbacks.

#### Runtime Configuration

Configure LAVA labs in pipeline YAML configuration files (e.g., `config/pipeline.yaml`):

```yaml
runtimes:
  lava-collabora: &lava-collabora
    lab_type: lava
    url: https://lava.collabora.dev/
    priority_min: 40
    priority_max: 60
    notify:
      callback:
        token: kernelci-api-token-staging
```

**Parameters**:
- `lab_type`: Set to `lava`
- `url`: LAVA lab API endpoint where jobs will be submitted
- `priority_min`/`priority_max`: Job priority range
- `notify.callback.token`: Token **description** (not the actual token value) used in LAVA job definition

#### LAVA Token Configuration

LAVA uses two types of tokens:
1. **Token Name/Description**: Used in YAML runtime configuration
2. **Token Value/Secret**: Used in TOML secrets file

**How LAVA tokens work**:
- If you specify a token name that does **not exist** in LAVA (under the submitting user), the callback will return the token **description** as the secret
- If you specify a token name that **matches an existing token** in LAVA, the callback will return the actual token **value/secret** from LAVA

**Creating tokens in LAVA**:
1. Log in to LAVA web interface
2. Navigate to "API" → "Tokens"
3. Create a new token with a description (e.g., "kernelci-api-token-staging")
4. View the token hash by clicking the green eye icon ("View token hash")
5. Copy the token value for use in kernelci-secrets.toml

#### Secrets Configuration

Configure LAVA runtime tokens in `kernelci-secrets.toml`:

```toml
[runtime.lava-collabora]
# Token used to submit jobs to LAVA (authentication)
runtime_token = "REPLACE-WITH-LAVA-TOKEN-VALUE"
# Token expected in LAVA callback (if different from runtime_token)
callback_token = "REPLACE-WITH-LAVA-TOKEN-VALUE"
```

**Token Types**:
- `runtime_token`: Used by scheduler to authenticate when submitting jobs to LAVA
- `callback_token`: Expected in the Authorization header of LAVA callbacks

If you use the same token for both submission and callback, only specify `runtime_token`.

#### LAVA Callback Service

The `lava-callback` service receives notifications from LAVA labs after jobs complete:

- Listens on port 8000 (default)
- Expects token value/secret in the `Authorization` header
- Maps token values to lab names using TOML configuration
- Processes test results and updates the KernelCI API

**Callback URL**: Set via `KCI_INSTANCE_CALLBACK` environment variable or pipeline configuration

Example callback URL: `https://kernelci-pipeline.example.com/lava/callback/`

#### Summary

- **Token Name (Description)**: Used in YAML runtime configuration (`notify.callback.token`)
- **Token Value (Secret)**: Used in TOML secrets configuration (`runtime_token`, `callback_token`)
- The scheduler uses `runtime_token` to submit jobs
- LAVA sends the token in callbacks, which is matched against `callback_token` (or `runtime_token` if `callback_token` is not set)

### Configuration Files

#### 1. k8s.tgz
Contains Kubernetes credentials for cluster access.

**Required contents**:
- `k8s-credentials/.kube/config` - Kubernetes config file

**Provider-specific additions**:
- **GKE**:
  - gcloud SDK installed and configured
  - Credentials in `k8s-credentials/.config/gcloud`
- **AKS**:
  - Azure CLI installed and configured
  - Credentials in `k8s-credentials/.azure`

#### 2. kernelci-secrets.toml
Main secrets configuration file.

**Required sections**:

```toml
[DEFAULT]
# Default API instance to use
api_config = "production"
# Default storage config to use
storage_config = "kci-storage-production"

[jwt]
# Used to provide API over kernelci-pipeline HTTP endpoint
secret = "<secret for signing jwt tokens>"

[storage.kci-storage-production]
storage_cred = "<secret for accessing storage>"

[runtime.lava-somename]
runtime_token = "<secret for accessing lava-somename>"

[send_kcidb]
# Configure this section if sending results to KCIDB

[tarball]
kdir = "/home/kernelci/data/src/linux"
output = "/home/kernelci/data/output"

[scheduler]
output = "/home/kernelci/data/output"
```

#### 3. kernelci-pipeline/config
Main configuration file for kernelci-pipeline.

**Documentation**: https://github.com/kernelci/kernelci-pipeline/blob/main/doc/config-reference.md

#### 4. build-configs.yaml
Contains config fragments for kernel builds.

**Location**: https://github.com/kernelci/kernelci-core/blob/main/config/core/build-configs.yaml

**Note**: Adapt this file for your specific build requirements.

---

### Pipeline API and JWT Token Generation

The **lava-callback** service provides a REST API for controlling pipeline operations beyond just receiving LAVA callbacks. This API is useful for:
- Triggering custom git checkouts
- Testing patchsets from email or URLs
- Retrying failed jobs
- Watching job status and results
- Other pipeline control operations

#### JWT Secret Configuration

To enable the Pipeline API, configure a JWT secret in `kernelci-secrets.toml`:

```toml
[jwt]
secret = "your-secret-string-here"
```

This secret is used to sign and verify JWT tokens for API authentication.

#### Generating JWT Tokens for Users

Use the `jwt_generator.py` tool from the `tools/` directory to generate user tokens:

```bash
cd kernelci-pipeline/tools
python3 jwt_generator.py --secret "your-secret-string-here" --email user@example.com
```

**Parameters**:
- `--secret`: The JWT secret from kernelci-secrets.toml `[jwt]` section
- `--email`: User email address to embed in the token

**Output**: A JWT token string that can be used for authentication

#### Using the Pipeline API

The Pipeline API is exposed through the same ingress endpoint as the LAVA callback service.

**Method 1: Using kci-dev CLI Tool** (Recommended)

The [kci-dev](https://github.com/kernelci/kci-dev) tool provides a command-line interface for interacting with the Pipeline API. It's a standalone tool for Linux kernel developers and maintainers to interact with KernelCI.

**Installation**:

Using PyPI (recommended for users):
```bash
# Using virtualenv
virtualenv .venv
source .venv/bin/activate
pip install kci-dev
```

Or for development:
```bash
# Clone and install with poetry
git clone https://github.com/kernelci/kci-dev
cd kci-dev
virtualenv .venv
source .venv/bin/activate
pip install poetry
poetry install
```

**Configuration**:

Create a configuration file using:
```bash
kci-dev config
```

This creates a config file template at `~/.config/kci-dev/kci-dev.toml`. Edit it with your instance details:

```toml
default_instance="staging"

[local]
pipeline="https://127.0.0.1"
api="https://127.0.0.1:8001/"
token="your-jwt-token-here"

[staging]
pipeline="https://staging.kernelci.org:9100/"
api="https://staging.kernelci.org:9000/"
token="your-jwt-token-here"

[production]
pipeline="https://kernelci-pipeline.westus3.cloudapp.azure.com/"
api="https://kernelci-api.westus3.cloudapp.azure.com/"
token="your-jwt-token-here"
```

**Available Commands**:

1. **checkout**: Trigger ad-hoc test of specific tree/branch/commit
   ```bash
   # Test a specific commit
   kci-dev checkout \
     --giturl https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
     --branch master \
     --commit f06021a18fcf8d8a1e79c5e0a8ec4eb2b038e153 \
     --job-filter "kbuild-gcc-12-x86"

   # Test latest commit with filters and watch results
   kci-dev checkout \
     --giturl https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
     --branch master \
     --tipoftree \
     --job-filter baseline-nfs-arm64-qualcomm \
     --platform-filter sc7180-trogdor-kingoftown \
     --watch

   # Watch for specific test result (useful for bisection)
   kci-dev checkout \
     --giturl https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git \
     --branch master \
     --tipoftree \
     --job-filter baseline \
     --watch \
     --test baseline.login
   ```

   Exit codes when using `--test`:
   - `0`: Test passed
   - `1`: Test failed
   - `2`: Error (prior steps failed, infrastructure error)
   - `64`: Critical error (kci-dev crashed)

2. **testretry**: Retry failed or incomplete test jobs
   ```bash
   kci-dev testretry --nodeid 65a5c89f1234567890abcdef
   ```

3. **watch**: Watch for results of a specific node
   ```bash
   kci-dev watch \
     --nodeid 679a91b565fae3351e2fac77 \
     --job-filter "kbuild-gcc-12-x86-chromeos-amd" \
     --test crit
   ```

4. **results**: Pull results from Web Dashboard (no token required)
   ```bash
   kci-dev results --tree mainline --branch master
   ```

5. **maestro-results**: Pull Maestro results in JSON format
   ```bash
   kci-dev maestro-results --nodes --filter "status=fail"
   ```

**Configuration Priority**:

kci-dev loads configuration files in the following order (later files override earlier ones):
1. Global: `/etc/kci-dev.toml`
2. User: `~/.config/kci-dev/kci-dev.toml`
3. Site-specific: `.kci-dev.toml` (or override with `--settings` option)

**Instance Selection**:

Override the default instance for a specific command:
```bash
kci-dev --instance production checkout --giturl ... --branch ... --tipoftree
```

**Method 2: Direct API Calls**

You can also interact directly with the API using curl or similar tools:

```bash
# Trigger custom checkout
curl -X POST https://kernelci-pipeline.example.com/api/checkout \
  -H "Authorization: YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git",
       "branch": "master",
       "commit": "abc123...",
       "jobfilter": ["baseline"]}'

# Retry a job
curl -X POST https://kernelci-pipeline.example.com/api/jobretry \
  -H "Authorization: YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nodeid": "65a5c89f1234567890abcdef"}'
```

**Note**: The Pipeline API requires proper configuration in the `[jwt]` section of kernelci-secrets.toml. Without this configuration, only LAVA callback functionality will be available.

**Additional Resources**:
- **kci-dev Documentation**: https://kernelci.github.io/kci-dev/
- **kci-dev Repository**: https://github.com/kernelci/kci-dev
- **PyPI Package**: https://pypi.org/project/kci-dev/
- **Issue Tracker**: https://github.com/kernelci/kci-dev/issues

---

## KCIDB-NG Deployment

KCIDB-NG is a complete rewrite of the KernelCI Database services, providing REST API access for submitting kernel test data and log analysis capabilities.

### Architecture Overview

KCIDB-NG consists of the following components:

1. **kcidb-restd-rs** - Rust-based REST API service
   - Receives JSON submissions via HTTP/HTTPS (ports 80/443)
   - Authenticates users via JWT tokens
   - Stores submissions in spool directory for processing
   - Provides status endpoints for tracking submissions

2. **ingester** - Python submission processor
   - Monitors spool directory for new submissions
   - Validates submissions against KCIDB schema
   - Loads validated data into PostgreSQL database
   - Archives processed submissions

3. **logspec-worker** - Python log analysis service
   - Monitors database for failed tests and builds
   - Downloads and analyzes log files using logspec library
   - Identifies issues and creates incidents
   - Submits findings back to KCIDB

4. **PostgreSQL Database** - Data storage
   - Stores all test results, builds, and metadata
   - Can be self-hosted or cloud-hosted

### Required Infrastructure

#### For KCIDB-NG:
- **Container Runtime**: Docker with Docker Compose v2.0+
- **Database**: PostgreSQL 17+ instance
- **Storage**: Persistent volumes for:
  - `/spool` - Incoming submissions and archives
  - `/state` - Application state (processed builds/tests tracking)
  - `/cache` - Downloaded log files
  - `/db` - PostgreSQL data (self-hosted mode)
  - `/certs` - TLS certificates (optional)

#### For Dashboard:
- **Container Runtime**: Docker with Docker Compose v2.0+
- **Database**: PostgreSQL instance (can share with KCIDB-NG)
- **Additional Services**:
  - Redis 8.0+ (for caching and task queuing)
  - Nginx proxy (for frontend routing)
- **Optional**: Google Cloud SQL proxy (for Google Cloud deployments)

### Deployment Options

#### Option 1: KCIDB-NG Only (Standalone)

**Best for**: Deploying only the data ingestion and processing services without the web dashboard.

**Prerequisites**:
- Docker and Docker Compose v2.0+ installed
- Git

**Setup Steps**:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/kernelci/kcidb-ng
   cd kcidb-ng
   ```

2. **Configure Environment Variables**

   Create a `.env` file in the root directory:

   ```bash
   # PostgreSQL configuration
   POSTGRES_PASSWORD=kcidb
   PG_PASS=kcidb
   PG_URI=postgresql:dbname=kcidb user=kcidb_editor password=kcidb host=db port=5432

   # Verbosity (set to 0 in production)
   KCIDB_VERBOSE=1

   # LogSpec dry-run mode (set to 0 to enable database modifications)
   KCIDB_DRY_RUN=1

   # JWT authentication secret
   JWT_SECRET=your_jwt_secret_here
   ```

   **Important**: Generate a strong JWT secret:
   ```bash
   openssl rand -hex 32
   ```

3. **Choose Deployment Profile**

   **Self-hosted mode** (with local PostgreSQL):
   ```bash
   docker compose --profile=self-hosted up -d --build
   ```

   This profile:
   - Starts local PostgreSQL database container
   - Runs database initialization (dbinit service)
   - Starts kcidb-rest, ingester, and logspec-worker services

   **Google Cloud SQL mode**:
   ```bash
   docker compose --profile=google-cloud-sql up -d --build
   ```

   For Google Cloud SQL, you need to:
   - Add Google Cloud credentials to `./config/db.json`
   - Ensure Cloud SQL Proxy has access to your instance

4. **Generate JWT Tokens**

   For production deployments with JWT authentication enabled:

   ```bash
   kcidb-restd-rs/tools/jwt_rest.py --secret YOUR_SECRET --origin YOUR_ORIGIN
   ```

   To disable JWT authentication (not recommended for production), uncomment this line in `docker-compose.yaml`:
   ```yaml
   command: ["/usr/local/bin/kcidb-restd-rs","-j",""]
   ```

5. **Verify Deployment**

   ```bash
   # Check running containers
   docker compose ps

   # View logs
   docker logs kcidb-rest
   docker logs ingester
   docker logs logspec-worker

   # Test API endpoint (with JWT token)
   curl -X GET \
     -H "Authorization: Bearer <jwt_token>" \
     https://localhost:443/authtest
   ```

6. **Submit Test Data**

   ```bash
   curl -X POST \
     -H "Authorization: Bearer <jwt_token>" \
     -H "Content-Type: application/json" \
     -d @submission.json \
     https://localhost:443/submit
   ```

   Check submission status:
   ```bash
   curl -X GET \
     -H "Authorization: Bearer <jwt_token>" \
     https://localhost:443/status?id=<submission_id>
   ```

   **Possible status values**:
   - `inprogress` - Upload not yet complete (.json.temp file exists)
   - `ready` - File ready for processing
   - `processed` - Successfully processed and archived
   - `failed` - Failed validation
   - `notfound` - Submission ID not found
   - `error` - Invalid request

**Services and Ports**:
- **kcidb-rest**: Ports 80 (HTTP), 443 (HTTPS)
- **PostgreSQL**: Port 5432 (internal to Docker network in default config)
- **ingester**: No exposed ports (processes files from spool)
- **logspec-worker**: No exposed ports (processes database records)

**Directory Structure**:
- `/spool` - Stores incoming submissions
  - `/spool/failed` - Failed submissions
  - `/spool/archive` - Successfully processed submissions
- `/state` - Application state
  - `processed_builds.db` - Tracks processed builds
  - `processed_tests.db` - Tracks processed tests
- `/cache` - Downloaded log files for analysis
- `/db` - PostgreSQL data (self-hosted mode only)

#### Option 2: Dashboard Only (Standalone)

**Best for**: Deploying only the web dashboard to visualize existing KCIDB data.

**Prerequisites**:
- Docker and Docker Compose v2.0+ installed
- Access to existing KCIDB PostgreSQL database
- Git

**Setup Steps**:

1. **Clone Dashboard Repository**
   ```bash
   git clone https://github.com/kernelci/dashboard
   cd dashboard
   ```

2. **Configure Environment Variables**

   Create `.env` file in `/dashboard` directory:
   ```bash
   cp ./dashboard/.env.example ./dashboard/.env
   ```

   Edit `.env` with your configuration:
   ```bash
   # API endpoint for frontend
   VITE_API_URL=http://localhost:8000
   ```

   Create backend environment file:
   ```bash
   # Django configuration
   export DJANGO_SECRET_KEY=$(openssl rand -base64 22)
   export DB_DEFAULT_USER=your_db_user@example.com
   export DB_DEFAULT_NAME=kcidb
   export DB_DEFAULT_HOST=db_host
   export DB_DEFAULT_PORT=5432

   # CORS allowed origins (required for non-production)
   export CORS_ALLOWED_ORIGINS='["https://dashboard.example.com"]'

   # Optional: Discord webhook for notifications
   export DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
   ```

3. **Setup Database Credentials**

   For Google Cloud SQL:
   ```bash
   # Setup cloud-sql-proxy
   gcloud auth application-default login
   cp ~/.config/gcloud/application_default_credentials.json .

   # Verify permissions
   ls -l application_default_credentials.json
   ```

   For direct PostgreSQL connection:
   ```bash
   # Create secrets directory
   mkdir -p backend/runtime/secrets
   echo "<your_password>" > backend/runtime/secrets/postgres_password_secret
   ```

4. **Launch Dashboard Services**

   ```bash
   docker compose up --build -d
   ```

   This starts:
   - **dashboard_db** (optional local PostgreSQL) - Port 5434
   - **cloudsql-proxy** (for Google Cloud) - Port 5432
   - **redis** - Port 6379
   - **backend** (Django API) - Port 8000
   - **dashboard** (React frontend build)
   - **proxy** (Nginx reverse proxy) - Port 80

5. **Access Dashboard**

   - Frontend: `http://localhost`
   - Backend API: `http://localhost/api`
   - Direct backend access: `http://localhost:8000`

6. **Setup Cron Jobs** (optional)

   The dashboard backend includes cron jobs for automated tasks (email notifications, etc.).

   Verify cron jobs are running:
   ```bash
   docker exec -it dashboard_backend_service crontab -l
   ```

#### Option 3: Combined KCIDB-NG + Dashboard (Recommended)

**Best for**: Complete self-hosted KernelCI test result system with data ingestion and visualization.

**Prerequisites**:
- Docker and Docker Compose v2.0+ installed
- Git

**Quick Start**:

1. **Clone KCIDB-NG Repository**
   ```bash
   git clone https://github.com/kernelci/kcidb-ng
   cd kcidb-ng
   ```

2. **Run Installation Script**

   ```bash
   ./self-hosted.sh run
   ```

   This automated script will:
   - Clone the dashboard repository (if not present)
   - Generate default `.env` configuration with random JWT secret
   - Create dashboard environment files from examples
   - Create secrets directory for dashboard
   - Start all services using `docker-compose-all.yaml`
   - Copy logspec worker configuration

   **Generated `.env` contents**:
   ```bash
   # PostgreSQL configuration
   POSTGRES_PASSWORD=kcidb
   PG_PASS=kcidb
   PG_URI=postgresql:dbname=kcidb user=kcidb_editor password=kcidb host=db port=5432
   # Programs will be more talkative if this is set
   KCIDB_VERBOSE=1
   # logspec will not modify database in dry-run mode
   KCIDB_DRY_RUN=1
   # JWT authentication
   JWT_SECRET=<randomly_generated>
   ```

3. **Verify Services**

   ```bash
   # Check all running containers
   docker compose -f docker-compose-all.yaml --profile=self-hosted ps

   # View logs
   ./self-hosted.sh logs
   ```

4. **Access Services**

   - **KCIDB REST API**: `https://localhost:443` or `http://localhost:8080`
   - **Dashboard Frontend**: `http://localhost:80`
   - **Dashboard Backend API**: `http://localhost:80/api`

5. **Management Commands**

   ```bash
   # Stop services
   ./self-hosted.sh down

   # View logs
   ./self-hosted.sh logs

   # Update to latest versions
   ./self-hosted.sh update

   # Complete cleanup (removes all data)
   ./self-hosted.sh clean
   ```

**Architecture**:

The combined deployment uses a shared PostgreSQL database and separate Docker networks:

```
┌─────────────────────────────────────────────────────────────┐
│                         Network: private                    │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │  kcidb-rest  │    │   ingester   │    │logspec-worker│   │
│  │  (Port 443)  │    │              │    │              │   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘   │
│         │                   │                   │           │
│         └───────────────────┴───────────────────┘           │
│                             │                               │
│                      ┌──────▼───────┐                       │
│                      │  PostgreSQL  │                       │
│                      │   (Port 5432)│                       │
│                      └──────────────┘                       │
│                                                             │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐   │
│  │   Backend    │◄───┤    Redis     │    │ Dashboard DB │   │
│  │  (Port 8000) │    │  (Port 6379) │    │  (Port 5434) │   │
│  └──────┬───────┘    └──────────────┘    └──────────────┘   │
│         │                                                   │
└─────────┼───────────────────────────────────────────────────┘
          │
┌─────────▼────────────────────────────────────────────────────┐
│                     Network: public                          │
│                                                              │
│  ┌──────────────┐    ┌──────────────┐                        │
│  │    Proxy     │    │  Dashboard   │                        │
│  │  (Port 80)   │◄───┤   (static)   │                        │
│  └──────────────┘    └──────────────┘                        │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │
    User Browser
```

**Docker Compose Configuration**:

The `docker-compose-all.yaml` includes the dashboard services via:
```yaml
include:
  - path: ./dashboard/docker-compose.yml
```

**Shared Resources**:
- PostgreSQL database (primary KCIDB data)
- Separate dashboard_db for dashboard-specific data
- Shared `private` network for backend communication

### Database Management

#### Self-hosted PostgreSQL Setup

The database is automatically initialized by the `dbinit` service when using `--profile=self-hosted`.

**Manual setup** (if needed):

```bash
# Run setup script
./scripts/setup_pgsql.sh
```

This creates:
- Database: `kcidb`
- User: `kcidb` with password `kcidb` (superuser)
- Additional users created by dbinit:
  - `kcidb_editor` - Write access
  - `kcidb_viewer` - Read-only access

#### Connecting to the Database

```bash
# Via docker container
docker exec -it postgres psql -U kcidb_editor -d kcidb

# Query test results
SELECT * FROM tests LIMIT 10;

# Check database schema
\dt
```

#### Database Backup

```bash
# Backup database
docker exec postgres pg_dump -U kcidb_editor kcidb > backup.sql

# Restore database
docker exec -i postgres psql -U kcidb_editor kcidb < backup.sql
```

### Configuration Files

#### 1. .env (KCIDB-NG)

Primary environment configuration:
```bash
# PostgreSQL connection
POSTGRES_PASSWORD=kcidb
PG_PASS=kcidb
PG_URI=postgresql:dbname=kcidb user=kcidb_editor password=kcidb host=db port=5432

# Logging verbosity (0=quiet, 1=verbose)
KCIDB_VERBOSE=1

# LogSpec dry-run mode (1=no database writes, 0=write to database)
KCIDB_DRY_RUN=1

# JWT secret for authentication
JWT_SECRET=<random_hex_string>

# Optional: TLS/SSL configuration
# CERTBOT_DOMAIN=example.com
# CERTBOT_EMAIL=admin@example.com
```

#### 2. config/logspec_worker.yaml

LogSpec worker configuration (copied from example on first run):

```yaml
# Log analysis configuration
origins:
  - microsoft
  - collabora

# Issue detection patterns
patterns:
  - name: kernel_panic
    regex: "Kernel panic"
  - name: oops
    regex: "Oops:"
```

#### 3. dashboard/.env.backend

Dashboard backend configuration:

```bash
# Database connection
DB_DEFAULT_USER=kcidb_editor
DB_DEFAULT_NAME=kcidb
DB_DEFAULT_HOST=db
DB_DEFAULT_PORT=5432

# Django settings
DJANGO_SECRET_KEY=<random_base64_string>
DEBUG=False

# CORS configuration
CORS_ALLOWED_ORIGINS=["http://localhost","http://localhost:80"]

# Optional: Discord notifications
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...

# Optional: Email configuration
# EMAIL_HOST=smtp.example.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
```

### Production Considerations

#### Security

1. **JWT Authentication**:
   - Always enable JWT authentication in production
   - Use strong, random secrets (32+ bytes)
   - Rotate tokens regularly

2. **TLS/SSL**:
   - Enable HTTPS for kcidb-rest service
   - Use Let's Encrypt or proper certificates
   - Configure reverse proxy (Nginx/Traefik) for TLS termination

3. **Database**:
   - Use strong PostgreSQL passwords
   - Restrict database access to internal network
   - Enable SSL connections for remote databases

4. **Network**:
   - Use Docker networks for service isolation
   - Expose only necessary ports to public network
   - Consider using firewall rules

#### Scalability

1. **Horizontal Scaling**:
   - Run multiple ingester instances for higher throughput
   - Run multiple logspec-worker instances for parallel log processing
   - Use load balancer for kcidb-rest service

2. **Database**:
   - Consider PostgreSQL replication for high availability
   - Use managed PostgreSQL services (AWS RDS, Google Cloud SQL, Azure Database)
   - Implement connection pooling (PgBouncer)

3. **Storage**:
   - Mount network storage for `/spool` and `/cache` volumes
   - Use S3-compatible storage for archives
   - Implement log rotation and cleanup policies

#### Monitoring

1. **Service Health**:
   ```bash
   # Check service status
   docker compose ps

   # Monitor resource usage
   docker stats

   # Check logs for errors
   docker compose logs --tail=100 -f
   ```

2. **Database Monitoring**:
   ```bash
   # Check database connections
   docker exec postgres psql -U kcidb_editor -d kcidb \
     -c "SELECT count(*) FROM pg_stat_activity;"

   # Monitor database size
   docker exec postgres psql -U kcidb_editor -d kcidb \
     -c "SELECT pg_size_pretty(pg_database_size('kcidb'));"
   ```

3. **Submission Tracking**:
   ```bash
   # Monitor spool directory
   ls -la spool/
   ls -la spool/archive/
   ls -la spool/failed/

   # Check processing state
   sqlite3 state/processed_builds.db "SELECT COUNT(*) FROM builds;"
   sqlite3 state/processed_tests.db "SELECT COUNT(*) FROM tests;"
   ```

#### Maintenance

1. **Log Rotation**:
   - Configure Docker logging driver
   - Set log size and rotation limits
   - Example docker-compose configuration:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

2. **Database Maintenance**:
   ```bash
   # Vacuum database
   docker exec postgres psql -U kcidb_editor -d kcidb -c "VACUUM ANALYZE;"

   # Reindex database
   docker exec postgres psql -U kcidb_editor -d kcidb -c "REINDEX DATABASE kcidb;"
   ```

3. **Archive Cleanup**:
   ```bash
   # Remove old archived submissions (older than 30 days)
   find ./spool/archive -type f -mtime +30 -delete

   # Remove old cached logs
   find ./cache -type f -mtime +7 -delete
   ```

#### Updates and Upgrades

1. **Update containers**:
   ```bash
   # Using self-hosted script
   ./self-hosted.sh update

   # Manual update
   docker compose -f docker-compose-all.yaml --profile=self-hosted pull
   docker compose -f docker-compose-all.yaml --profile=self-hosted up -d --build
   ```

2. **Database migrations**:
   - Check for schema changes in release notes
   - Backup database before major updates
   - Test migrations in staging environment first

### Troubleshooting

#### Common Issues

1. **Services not starting**:
   ```bash
   # Check logs
   docker compose logs <service_name>

   # Check configuration
   docker compose config

   # Verify environment variables
   docker compose config | grep -A 5 "environment:"
   ```

2. **Database connection issues**:
   ```bash
   # Test database connection
   docker exec -it postgres psql -U kcidb_editor -d kcidb

   # Check database logs
   docker logs postgres

   # Verify network connectivity
   docker exec kcidb-rest ping -c 3 db
   ```

3. **JWT authentication failing**:
   - Verify JWT_SECRET matches between token generation and service
   - Check token expiration
   - Validate token format (Bearer <token>)

4. **Dashboard not loading**:
   ```bash
   # Check proxy logs
   docker logs dashboard-proxy-1

   # Check backend logs
   docker logs dashboard_backend_service

   # Verify CORS configuration
   docker exec dashboard_backend_service env | grep CORS
   ```

5. **LogSpec not processing logs**:
   ```bash
   # Check worker logs
   docker logs logspec-worker

   # Verify configuration
   cat config/logspec_worker.yaml

   # Check cache directory permissions
   ls -la cache/
   ```

#### Debug Mode

Enable verbose logging:

```bash
# Edit .env
KCIDB_VERBOSE=1
DEBUG=True
DEBUG_SQL_QUERY=True  # For Django SQL debugging

# Restart services
docker compose restart
```

#### Manual Log Processing

Test log processing without database writes:

```bash
docker exec -it logspec-worker python /app/logspec_worker.py \
  --spool-dir /app/spool \
  --origins microsoft \
  --dry-run
```

### Migration from Legacy KCIDB

If migrating from the original Python-based KCIDB system:

1. **Export existing data**:
   - Use `kcidb-query` to export data in JSON format
   - Backup PostgreSQL database

2. **Import into KCIDB-NG**:
   - Submit exported JSON via REST API
   - Or restore database backup directly

3. **Update submission scripts**:
   - Change endpoint URLs to KCIDB-NG REST API
   - Add JWT authentication headers
   - Update JSON format if needed (should be compatible)

4. **Verify data integrity**:
   - Compare record counts
   - Validate test results via dashboard
   - Check for missing or duplicate data

---

## Resources and References

### Repositories

#### Maestro (Pipeline and API)
- **Maestro API**: https://github.com/kernelci/kernelci-api
- **Maestro Pipeline**: https://github.com/kernelci/kernelci-pipeline
- **Deployment Scripts**: https://github.com/kernelci/kernelci-deploy
- **Storage Server**: https://github.com/kernelci/kernelci-storage
- **Core Configuration**: https://github.com/kernelci/kernelci-core
- **Pipeline CLI Tool (kci-dev)**: https://github.com/kernelci/kci-dev

#### KCIDB-NG (Database and Dashboard)
- **KCIDB-NG**: https://github.com/kernelci/kcidb-ng
- **Web Dashboard**: https://github.com/kernelci/dashboard

### Documentation
- **Pipeline Configuration Reference**: https://github.com/kernelci/kernelci-pipeline/blob/main/doc/config-reference.md
- **Pipeline Developer Documentation**: https://github.com/kernelci/kernelci-pipeline/blob/main/doc/developer-documentation.md
- **Connecting Lab to Pipeline**: https://github.com/kernelci/kernelci-pipeline/blob/main/doc/connecting-lab.md
- **Build Configs**: https://github.com/kernelci/kernelci-core/blob/main/config/core/build-configs.yaml

### Workflows
- **Docker Image Building**: https://github.com/kernelci/kernelci-core/blob/main/.github/workflows/docker_images.yml
- **Production Deployment**: https://github.com/kernelci/kernelci-core/blob/main/.github/workflows/production.yml
