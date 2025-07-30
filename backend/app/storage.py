import os
from typing import Optional, List
from datetime import datetime
from .schemas import JobInfo, JobStatus

ARTIFACT_DIR = os.getenv("ARTIFACT_DIR", "/videos")

def get_job_metadata(redis, job_id: str) -> Optional[JobInfo]:
    data = redis.hgetall(f"job:{job_id}")
    if not data:
        return None
    return JobInfo(
        job_id=job_id,
        status=data["status"],
        created_at=datetime.fromisoformat(data["created_at"]),
        updated_at=datetime.fromisoformat(data["updated_at"]),
        error=data.get("error"),
        output_path=data.get("output_path")
    )

def set_job_metadata(redis, job_id: str, **kwargs):
    redis.hset(f"job:{job_id}", mapping={**kwargs, "updated_at": datetime.utcnow().isoformat()})

def list_jobs_metadata(redis, limit: int = 100) -> List[JobInfo]:
    ids = redis.lrange("jobs:index", 0, limit-1)
    return [md for job_id in ids if (md := get_job_metadata(redis, job_id))]
