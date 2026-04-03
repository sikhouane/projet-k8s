# NLP Multi-Agent Cloud Platform

**Production-ready Kubernetes deployment of an intelligent NLP application with weather intelligence capabilities on Google Cloud Platform.**

## Overview

This project demonstrates a complete, end-to-end cloud-native architecture combining:
- **AI/NLP** (Natural Language Processing) with multi-agent orchestration
- **Kubernetes orchestration** at scale on GCP
- **Infrastructure as Code** using Terraform
- **Modern DevOps practices** and cloud-native patterns

The system intelligently processes user questions through an LLM-powered agent that can fetch and analyze real-time weather data, then returns contextual, factual answers.

**Key Achievement**: Production-grade deployment from development to GCP cloud using Industry-standard tools (Terraform, Kubernetes, Docker).

## Tech stack

### Cloud & Infrastructure
- **Google Cloud Platform (GCP)**: GKE cluster, Artifact Registry, IAM policies
- **Terraform**: Infrastructure as Code for reproducible, version-controlled deployments
- **Kubernetes**: Container orchestration, service discovery, network management, storage
- **Docker**: Multi-stage containerization with optimized images

### Backend & AI
- **Python 3.x**: Core application logic
- **LLM Integration**: Agent-based AI with tool-calling capabilities
- **FastAPI/Python Web Framework**: RESTful API endpoints
- **Multi-Agent Architecture**: Extensible, composable weather tools + routing logic

### Frontend & Routing
- **HTML/JavaScript**: Responsive user interface
- **Nginx**: Reverse proxy, static file serving, load balancing
- **NGINX Ingress Controller**: Production traffic management

### Data
- **PostgreSQL (Containerized)**: Persistent data storage with PVC


## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                  GCP GKE Cluster                          │
├───────────────────────────────────────────────────────────┤
│                                                           │
│  ┌─────────────────────────────────────────────────────┐ │
│  │  NGINX Ingress Controller (Public LoadBalancer)    │ │
│  │  • HTTPS termination                               │ │
│  │  • Intelligent routing (api → backend, / → front)  │ │
│  └─────────────────────────────────────────────────────┘ │
│                      ↓                                    │
│    ┌─────────────────────────────────────┐               │
│    │ NLP Backend Pods (Replicas)         │               │
│    ├─────────────────────────────────────┤               │
│    │ • FastAPI application                │               │
│    │ • LLM agent orchestration            │               │
│    │ • Weather API integration            │               │
│    │ • Health checks & monitoring         │               │
│    └─────────────────────────────────────┘               │
│                 ↓                                         │
│    ┌──────────────┐  ┌──────────────┐                   │
│    │ Frontend Pods │  │  Database    │                   │
│    │ (Replicas)   │  │  (PostgreSQL)│                   │
│    │ • Nginx      │  │  • PVC       │                   │
│    │ • Static UI  │  │  • Persistent│                   │
│    └──────────────┘  └──────────────┘                   │
│                                                           │
└───────────────────────────────────────────────────────────┘
         ↑                                    ↑
    External Users              External Weather APIs
```

## Features

- **AI-Powered Q&A Engine**: Advanced natural language understanding with contextual responses
- **Real-Time Data Integration**: Live weather API data fetching and analysis
- **REST API**: Clean, well-structured endpoints for seamless integration
- **Production-Grade Kubernetes**: Multi-pod deployments with health checks, restart policies
- **High Availability**: Replicated pods for backend, frontend, and database
- **Persistent Storage**: Kubernetes PersistentVolumeClaim for database data durability
- **Load Balancing**: Nginx Ingress for intelligent traffic distribution
- **Secret Management**: Kubernetes Secrets for secure credential handling
- **Configuration Management**: ConfigMaps for environment-specific settings

---

## Technical skills

### Container Orchestration & DevOps
- Designed and deployed multi-tier Kubernetes manifests (Deployments, Services, StatefulSets, PVCs, Ingress)
- Implemented namespace isolation for workload segregation
- Configured health checks (liveness & readiness probes) for reliability
- Managed resource requests/limits for optimal cluster utilization

### Infrastructure as Code
- Built Terraform modules for automated GKE cluster provisioning
- Implemented version-controlled infrastructure with state management
- Created reproducible deployments across environments
- Defined GCP IAM policies with least-privilege principles

### Cloud Platform (GCP)
- Provisioned Google Kubernetes Engine (GKE) clusters
- Managed Google Artifact Registry for Docker image storage
- Configured IAM service accounts and role-based access control
- Set up Cloud networking with public/private resources

### Containerization & CI/CD Concepts
- Built multi-stage Dockerfiles for optimized image sizes
- Pushed images to private Docker registry (Artifact Registry)
- Implemented image versioning and tagging strategies
- Understood container lifecycle and orchestration

### Backend Development
- Developed Python APIs with FastAPI framework
- Implemented multi-agent architecture for extensible AI
- Integrated external APIs (weather services) with error handling
- Designed tool-calling patterns for LLM agent coordination

### Networking & Ingress
- Configured Nginx Ingress Controller for HTTP(S) routing
- Implemented service discovery using Kubernetes DNS
- Set up load balancing between pod replicas
- Managed network policies for traffic control

### Debugging & Operations
- Used kubectl for pod inspection, log aggregation, and diagnostics
- Implemented troubleshooting workflows for cluster issues
- Verified service connectivity and network reachability
- Managed deployment versioning and rollback strategies


## Structure

```
projet-k8s/
├── k8s/                              # Kubernetes Manifests
│   ├── 00-namespace.yaml             # Namespace: nlp
│   ├── 01-config-back.yaml           # Backend ConfigMap
│   ├── 02-secret.yaml                # Database credentials
│   ├── 03-db-pvc.yaml                # Persistent volume claim
│   ├── 04-db-deployment.yaml         # PostgreSQL Deployment
│   ├── 05-db-service.yaml            # Database ClusterIP Service
│   ├── 06-back-deployment.yaml       # Backend NLP Deployment
│   ├── 07-back-service.yaml          # Backend ClusterIP Service
│   ├── 08-front-deployment.yaml      # Frontend Deployment
│   ├── 09-front-service.yaml         # Frontend ClusterIP Service
│   ├── 10-ingress-api.yaml           # API Ingress routing
│   └── 11-ingress-front.yaml         # Frontend Ingress routing
│
├── terraform/gke/                    # Infrastructure as Code
│   ├── gke.tf                        # GKE cluster definition
│   ├── provider.tf                   # GCP provider configuration
│   ├── gke-variables.tf              # Variables & outputs
│   ├── create-namespace.sh           # Setup script
│   └── terraform.tfstate             # State file (prod only)
│
├── NLP_Project/                      # Backend Application
│   ├── api.py                        # FastAPI endpoints
│   ├── weather_router_agent.py       # Multi-agent orchestration
│   ├── weather_tools.py              # Weather API integration
│   ├── code_exec.py                  # Code execution capability
│   ├── requirements.txt              # Python dependencies
│   ├── Dockerfile                    # Multi-stage backend image
│   └── README.md                     # Backend documentation
│
├── front/                            # Frontend Application
│   ├── index.html                    # React/HTML UI
│   ├── Dockerfile                    # NGINX-based frontend
│   └── nginx.conf                    # NGINX configuration
│
├── nginx.conf                        # Optional: Nginx config
└── README.md                         # This documentation
```

---

## Security Considerations

- **Kubernetes Secrets**: Sensitive data (DB passwords, API keys) encrypted at rest
- **Namespace Isolation**: Workloads confined to nlp namespace for multi-tenancy
- **IAM Policies**: GCP service accounts with minimal required permissions (least privilege)
- **Network Ingress**: Public traffic routed only through NGINX controller
- **ConfigMaps vs Secrets**: Clear separation of configuration from credentials
- **Image Registry**: Private Artifact Registry with authentication required

## Key Learnings & Takeaways

1. **Production Readiness**: Gap between local development and cloud production (networking, statelessness, scaling)
2. **Infrastructure Automation**: Version-controlled, repeatable infrastructure reduces errors and enables disaster recovery
3. **Container Best Practices**: Image optimization, layer caching, registry organization
4. **Kubernetes Complexity**: Real-world challenges (networking, storage, RBAC, resource management)
5. **DevOps Mindset**: Building systems that enable continuous integration, deployment, and operational excellence
6. **Cloud Economics**: Understanding resource allocation, cost optimization, and cloud pricing models
7. **Monitoring & Observability**: Importance of logs, metrics, and alerting for production systems

## Potential enhancements

- [ ] **CI/CD Pipeline**: GitOps with GitHub Actions / Cloud Build for automated deployments
- [ ] **Auto-Scaling**: Horizontal Pod Autoscaler based on CPU/Memory metrics
- [ ] **Monitoring Stack**: Prometheus + Grafana for metrics visualization
- [ ] **Centralized Logging**: ELK Stack or GCP Cloud Logging for aggregated logs
- [ ] **Certificate Management**: Cert-Manager for automatic HTTPS certificate renewal
- [ ] **Database Backups**: Automated backup strategies and disaster recovery
- [ ] **Service Mesh**: Istio for advanced traffic management and observability
- [ ] **API Documentation**: OpenAPI/Swagger integration for interactive API docs

## Educational project - All rights reserved.
