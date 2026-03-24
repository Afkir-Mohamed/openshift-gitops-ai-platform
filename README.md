# OpenShift GitOps & AI Platform

A production-grade cloud-native platform demonstrating Red Hat enterprise technologies,
built on Kubernetes with full GitOps automation, Ansible configuration management,
live observability, and an AI inference layer.

## Architecture
```
GitHub Repository (Single Source of Truth)
           |
           | GitOps (ArgoCD watches and syncs)
           |
    Kubernetes Cluster
    ├── monitoring/
    │   ├── Prometheus    (metrics collection)
    │   ├── Grafana       (live dashboards)
    │   └── Node Exporter (host metrics)
    ├── ai-inference/
    │   ├── Ollama        (Llama 3 AI inference)
    │   └── my-app        (Python API - built by CI/CD)
    └── argocd/
        └── ArgoCD        (GitOps controller)
```

## Red Hat Technology Mapping

| Component in this project       | Red Hat Equivalent                        |
|---------------------------------|-------------------------------------------|
| ArgoCD                          | Red Hat OpenShift GitOps                  |
| Ansible Playbooks               | Red Hat Ansible Automation Platform       |
| Prometheus + Grafana            | Red Hat OpenShift Monitoring              |
| Ollama + Llama 3                | Red Hat AI Platform / InstructLab        |
| GitHub Actions + Podman         | Red Hat OpenShift Pipelines               |
| Kubernetes RBAC + NetworkPolicy | Red Hat Advanced Cluster Security         |
| k3s (local) / OpenShift Sandbox | Red Hat OpenShift Container Platform      |

## What This Demonstrates

### GitOps with ArgoCD
- All cluster state managed declaratively from Git
- Automatic drift detection and self-healing (`selfHeal: true`)
- Push to Git → ArgoCD detects change → deploys automatically
- Zero manual `kubectl apply` in production workflow

### Ansible Automation
- Idempotent namespace and RBAC provisioning
- Run the same playbook 100 times — only changes what needs changing
- Demonstrates Red Hat Ansible Automation Platform principles

### AI Inference on Kubernetes
- Llama 3 (1B) running as a native Kubernetes workload
- REST API exposed via Kubernetes Service
- Aligned with Red Hat AI Platform / InstructLab enterprise use case
- Enterprise rationale: run AI inference on-premises for data sovereignty

### Full Observability Stack
- Prometheus scraping node metrics every 15 seconds
- Grafana dashboards with live CPU, RAM, disk, and network data
- ServiceMonitor pattern for automatic target discovery

### CI/CD Pipeline
- GitHub Actions builds container image using Podman (not Docker)
- Image pushed to GitHub Container Registry (ghcr.io)
- Pipeline updates Git manifest automatically
- ArgoCD detects manifest change and deploys — full GitOps loop

## Quick Start

### Prerequisites
- WSL2 (Ubuntu) on Windows, or Linux/Mac
- k3s: `curl -sfL https://get.k3s.io | sh -`
- kubectl, ArgoCD CLI, Ansible, Podman

### Deploy ArgoCD
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl port-forward svc/argocd-server -n argocd 8080:443 &
```

### Deploy the Platform
```bash
# Deploy monitoring stack
kubectl apply -f manifests/argocd/app-monitoring.yml

# Deploy AI inference layer
kubectl apply -f manifests/argocd/app-ai-inference.yml

# ArgoCD handles everything else automatically
```

### Run Ansible Automation
```bash
ansible-playbook ansible/playbooks/site.yml -i ansible/inventory/hosts.yml
```

### Test AI Inference
```bash
kubectl port-forward svc/ollama-service -n ai-inference 11435:11434 &
curl http://localhost:11435/api/generate -d '{
  "model": "llama3.2:1b",
  "prompt": "What is Red Hat OpenShift?",
  "stream": false
}'
```

## Sandbox Adaptation Notes

This project was originally designed for the Red Hat Developer Sandbox but adapted
to run on k3s due to Sandbox namespace-scope restrictions blocking ArgoCD CRD and
ClusterRole creation. Key adaptations:

- Used k3s instead of OpenShift Sandbox for full admin access
- All namespaces created manually instead of via `oc new-project`
- ArgoCD installed via standard manifests instead of OpenShift GitOps Operator
- This mirrors real-world enterprise scenarios where environment constraints
  require architectural adaptation — a core Solution Architect skill

## Key Interview Talking Points

**On GitOps:** "Every change to this cluster flows through Git. ArgoCD's selfHeal
means if anyone manually changes something in the cluster, it gets automatically
reverted to match the Git state within seconds."

**On Ansible:** "I can run the provisioning playbook 100 times against a production
cluster and it will never cause unintended changes — that's idempotency, which is
why enterprises trust Ansible Automation Platform."

**On AI:** "Enterprises want to run AI inference on-premises via OpenShift rather
than sending sensitive data to external APIs. This project demonstrates exactly
that architecture using Ollama as an analogue for Red Hat AI Platform."

**On the Sandbox adaptation:** "I diagnosed a cascading failure where OpenShift's
Security Context Constraints blocked Redis from starting as root, which prevented
the argocd-redis secret from being created, causing all dependent pods to fail.
I pivoted to k3s to maintain project momentum — adapting to environment constraints
is a core part of the Solution Architect role."

## Author
Mohamed Afkir — linkedin.com/in/mohamed-afkir
