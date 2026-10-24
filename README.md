# Self-Healing Infrastructure with Docker, Prometheus, and Ansible

## Overview

This project demonstrates a local self-healing infrastructure workflow using Docker, Prometheus, Blackbox Exporter, Alertmanager, Python, and Ansible.

The goal is to detect an NGINX service failure and automatically trigger a recovery action through an alert-driven automation workflow.

## Architecture

NGINX Web Server
       |
       v
Blackbox Exporter
       |
       v
Prometheus Monitoring
       |
       v
Alertmanager
       |
       v
Python Recovery Webhook
       |
       v
Ansible Playbook
       |
       v
Restart NGINX Container

## Technologies Used

- Docker and Docker Compose
- NGINX
- Prometheus
- Blackbox Exporter
- Alertmanager
- Python
- Ansible
- YAML
- Linux and Ubuntu WSL

## Project Structure

    self-healing-infrastructure/
    ├── app/
    │   ├── Dockerfile
    │   └── webhook.py
    ├── alertmanager/
    │   └── alertmanager.yml
    ├── ansible/
    │   ├── inventory.ini
    │   └── restart_nginx.yml
    ├── nginx/
    │   └── default.conf
    ├── prometheus/
    │   ├── alert_rules.yml
    │   ├── blackbox.yml
    │   └── prometheus.yml
    ├── docker-compose.yml
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Prerequisites

- Docker Desktop
- Docker Compose
- Ubuntu on WSL2 or another Linux environment
- Git

## Getting Started

### 1. Clone the repository

    git clone https://github.com/rayyanjpathan123-stack/self-healing-infrastructure.git
    cd self-healing-infrastructure

### 2. Start the infrastructure

    docker compose up -d --build

### 3. Check container status

    docker compose ps

### 4. Access the services

- NGINX: http://localhost:8081
- NGINX health endpoint: http://localhost:8081/health
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093

## Health Check

Run:

    curl http://localhost:8081/health

Expected response:

    healthy

## Recovery Workflow

1. Blackbox Exporter probes the NGINX health endpoint.
2. Prometheus evaluates the NGINX failure alert rule.
3. Alertmanager forwards firing alerts to the recovery webhook.
4. The Python webhook invokes the Ansible recovery playbook.
5. Ansible requests that the NGINX container be started and restarted.

The complete automatic recovery workflow must be tested to confirm end-to-end recovery.

## Useful Commands

Start services:

    docker compose up -d --build

View service status:

    docker compose ps

View logs:

    docker compose logs -f

Stop services:

    docker compose down

View recovery logs:

    docker compose logs recovery

## Security Notes

- This is a local demonstration project.
- The recovery service mounts the Docker socket, which grants powerful control over the Docker host.
- Do not expose the recovery webhook or Docker socket to the public internet.
- Production deployments should implement authentication, access controls, audit logging, and additional safeguards.

## Learning Outcomes

- Containerizing an application with Docker.
- Orchestrating multiple services with Docker Compose.
- Defining service health checks and Prometheus alert rules.
- Configuring Alertmanager webhook notifications.
- Automating recovery actions using Python and Ansible.
- Troubleshooting containerized infrastructure.

## Project Status

The Docker Compose services have been started, and the NGINX homepage has responded successfully.

End-to-end monitoring and automatic recovery verification remain pending.

## Author

Rayyan Pathan

GitHub: https://github.com/rayyanjpathan123-stack
