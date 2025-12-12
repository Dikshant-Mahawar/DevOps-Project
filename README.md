# AIOps-Driven Chatbot System with Kubernetes Deployment & ELK Observability

---

### Project Title  
**AIOps-Driven Chatbot System with Kubernetes Orchestration, CI/CD Automation, and ELK-based Observability Pipeline**

---

## Overview

This project demonstrates a **production-grade, cloud-native, AI-powered chatbot system** built using modern **AIOps and DevOps best practices**. It integrates:

- LLM-powered chatbot (via **Ollama**)
- Microservices architecture (FastAPI backend + React dashboards)
- Full **Kubernetes** deployment with HPA, rolling updates, and self-healing
- Real-time **observability** using **ELK Stack (Elasticsearch, Logstash, Kibana)** + Filebeat
- Automated **CI/CD pipeline** using **Jenkins**
- Containerization with **Docker**

The result is a scalable, observable, and intelligent chatbot platform suitable for real-world deployment.

---

## Architecture Diagram

User → Client Dashboard (React)
↓
FastAPI Backend ←→ Ollama (Local LLM)
↓
Kubernetes Cluster (Deployments, Services, HPA)
↓
Filebeat (DaemonSet) → Logstash → Elasticsearch → Kibana
↑
Supervisor Dashboard (Monitoring & Escalations)


---

## Key Components

| Component                  | Technology                  | Purpose |
|---------------------------|-----------------------------|--------|
| Backend                   | Python + FastAPI            | Chatbot logic, LLM orchestration, user management |
| LLM Integration           | Ollama (Local LLM server)   | On-cluster AI inference (e.g., Llama3, Mistral) |
| Client Dashboard          | React.js                    | User-facing chatbot interface |
| Supervisor Dashboard      | React.js                    | Admin monitoring & escalation handling |
| Containerization          | Docker                      | Portable, reproducible images |
| Orchestration             | Kubernetes (Minikube)       | Deployments, Services, HPA, DaemonSets |
| Log Collection            | Filebeat (DaemonSet)        | Collects logs from all pods with K8s metadata |
| Log Processing            | Logstash                   | Forwards enriched logs |
| Search & Storage          | Elasticsearch               | Indexed daily logs (`kubernetes-logs-YYYY.MM.DD`) |
| Visualization             | Kibana                      | Real-time operational dashboards |
| CI/CD Automation          | Jenkins + Jenkinsfile       | Build → Docker → Push → Deploy to K8s deploy |
| Autoscaling               | Horizontal Pod Autoscaler   | Scales backend based on CPU usage |

---

## Features Demonstrated

- [x] Real-time AI chatbot using local LLMs (Ollama)
- [x] Stateless microservices with horizontal scaling
- [x] Zero-downtime rolling updates
- [x] Self-healing pods (liveness/readiness probes)
- [x] Automated CI/CD with Jenkins
- [x] Full observability via ELK stack
- [x] Kubernetes metadata-enriched logging
- [x] Live Kibana dashboards showing pod activity and request patterns
- [x] Supervisor dashboard for monitoring escalations

---

## Project Structure

├── backend/                  # FastAPI + Ollama integration
├── frontend-client/          # React User Dashboard
├── frontend-supervisor/      # React Admin Dashboard
├── k8s/                      # Kubernetes manifests (Deployments, Services, HPA, Filebeat)
├── jenkins/                  # Jenkinsfile + pipeline config
├── docker/                   # Dockerfiles
├── filebeat/                 # Filebeat config for Kubernetes
├── logstash/                 # Logstash pipeline config
└── docs/                     # Report, screenshots, architecture diagrams


---

## How to Run (Demo Steps)

```bash
# 1. Start Minikube
minikube start

# 2. Deploy ELK Stack (if not using Docker Compose)
kubectl apply -f k8s/elk/

# 3. Deploy Filebeat as DaemonSet
kubectl apply -f k8s/filebeat/

# 4. Deploy Ollama + Backend + Frontends
kubectl apply -f k8s/

# 5. Access Services
minikube service client-dashboard --url
minikube service supervisor-dashboard --url
minikube service kibana --url

'''
CI/CD Pipeline (Jenkins)

Triggers on every Git push
Builds Docker images
Pushes to Docker Hub
Applies updated Kubernetes manifests
Performs rolling update → zero downtime


AIOps in Action (Demo Highlight)
When a user sends a message:

Request hits backend → generates structured log
Filebeat captures log + adds Kubernetes metadata
Log flows to Elasticsearch via Logstash
Kibana dashboard updates in real-time
Supervisor sees activity spike instantly

This shows true end-to-end observability and operational intelligence.

Conclusion
This project successfully demonstrates:

A working AI-powered chatbot using local LLMs
Full cloud-native deployment on Kubernetes
Automated DevOps with CI/CD
Real-time AIOps observability using ELK
Scalability, resilience, and maintainability

A complete blueprint for deploying intelligent applications in production.

minikube start

kubectl create secret generic ollama-secret \
  --from-literal=OLLAMA_USER=admin \
  --from-literal=OLLAMA_PASS=SuperSafe123 \


--kubectl apply -f k8s/ollama-deployment.yaml\
--kubectl apply -f k8s/backend-deployment.yaml\
--kubectl apply -f k8s/frontend-deployment.yaml\
--kubectl apply -f k8s/supervisor-dashboard.yaml\
--kubectl apply -f k8s/backend-hpa.yaml\


minikube service frontend-service\
minikube service supervisor-service\
