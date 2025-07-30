# Project variables
PROJECT_NAME = text2video
BACKEND_IMAGE = $(PROJECT_NAME)-backend
FRONTEND_IMAGE = $(PROJECT_NAME)-frontend
DOCKER_COMPOSE_FILE = infra/compose/docker-compose.yml
K8S_DIR = infra/k8s

# Docker Hub or Registry (set your Docker Hub username or private registry)
REGISTRY = zhengyuancui

# ==== Local Development ====

.PHONY: dev
dev:
	@echo "Starting local development stack (backend, worker, redis, frontend)..."
	docker compose -f $(DOCKER_COMPOSE_FILE) up --build

.PHONY: stop
stop:
	@echo "Stopping local development stack..."
	docker compose -f $(DOCKER_COMPOSE_FILE) down

.PHONY: logs
logs:
	@echo "Tailing logs from backend and worker..."
	docker compose -f $(DOCKER_COMPOSE_FILE) logs -f backend worker

# ==== Docker Build and Push ====

.PHONY: build
build:
	@echo "Building backend and frontend Docker images..."
	docker build -t $(REGISTRY)/$(BACKEND_IMAGE):latest ./backend
	docker build -t $(REGISTRY)/$(FRONTEND_IMAGE):latest ./frontend

.PHONY: push
push: build
	@echo "Pushing backend and frontend images to registry..."
	docker push $(REGISTRY)/$(BACKEND_IMAGE):latest
	docker push $(REGISTRY)/$(FRONTEND_IMAGE):latest

# ==== Kubernetes Deployment ====

.PHONY: k8s-deploy
k8s-deploy: push
	@echo "Applying all Kubernetes manifests..."
	kubectl apply -f $(K8S_DIR)/namespace.yaml
	kubectl -n $(PROJECT_NAME) apply -f $(K8S_DIR)

.PHONY: k8s-logs
k8s-logs:
	@echo "Streaming logs from backend pods..."
	kubectl -n $(PROJECT_NAME) logs -l app=$(PROJECT_NAME)-api -f

.PHONY: k8s-delete
k8s-delete:
	@echo "Deleting all resources for $(PROJECT_NAME)..."
	kubectl -n $(PROJECT_NAME) delete all --all
