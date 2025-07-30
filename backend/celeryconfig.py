import os

broker_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
result_backend = broker_url
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "UTC"
enable_utc = True
worker_prefetch_multiplier = 1  # good for GPU tasks (one task per worker at a time)
task_acks_late = True
