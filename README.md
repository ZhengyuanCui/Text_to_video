# Text to video project

## Problems

### Get environment ready

Spend lots of time to get docker and vscode ready

### Can't open ubuntu terminal inside current workspace

`ctrl+shift+p` and select default profile to be any terminal.
Use `wsl -d Ubuntu` to convert to wsl terminal

### Forgot password of unbuntu

Don't do this again

### Installed a package but can't use it

Example: install uv but when I try `uv venv .venv`, still shows can't find command uv.

Path problem? See that it needs a restart but after restarting, the python version is now 3.5.2. Need to change python version. It shows that there is no alternative. This is weird because I can see 3.13 when I click on python icon on the left.

Installing python 3.13.3 failed. Interesting ... 


text2video/
  backend/
    app/
      __init__.py
      main.py                 # FastAPI app + routes
      schemas.py              # Pydantic models
      storage.py              # Local/PVC/S3 storage utils
      gpu_pool.py             # Simple GPU allocation helper
      worker.py               # Celery task definitions
      model/
        __init__.py
        mochi.py              # Wrapper around genmo/mochi-1-preview
    celeryconfig.py
    requirements.txt
    Dockerfile
  frontend/
    src/
      App.tsx
      api.ts
      index.tsx
    public/index.html
    package.json
    vite.config.ts
    Dockerfile
  infra/
    k8s/
      namespace.yaml
      redis-statefulset.yaml
      redis-service.yaml
      api-deployment.yaml
      api-service.yaml
      worker-deployment.yaml
      ingress.yaml
      hpa.yaml
      pvc.yaml
    compose/
      docker-compose.yml
  .devcontainer/
    devcontainer.json
    Dockerfile
    requirements.txt          # (can symlink to backend/requirements.txt)
  .vscode/
    launch.json
    settings.json
  Makefile
  README.md

