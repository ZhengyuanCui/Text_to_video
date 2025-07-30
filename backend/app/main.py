from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from celery.result import AsyncResult
from redis import Redis
from datetime import datetime
import os

from .schemas import SubmitJobRequest, SubmitJobResponse, JobInfo, ListJobsResponse, JobStatus
from .worker import celery_app
from .storage import get_job_metadata, list_jobs_metadata

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)

app = FastAPI(title="Text2Video API", version="0.1.0")

@app.post("/jobs", response_model=SubmitJobResponse)
def submit_job(req: SubmitJobRequest):
    task = celery_app.send_task(
        "generate_video",
        kwargs={"prompt": req.prompt, "length_sec": req.length_sec, "resolution": req.resolution}
    )
    # persist minimal metadata for listing
    now = datetime.utcnow().isoformat()
    redis.hset(f"job:{task.id}", mapping={
        "status": JobStatus.PENDING,
        "created_at": now,
        "updated_at": now
    })
    redis.lpush("jobs:index", task.id)
    return SubmitJobResponse(job_id=task.id)

@app.get("/jobs/{job_id}", response_model=JobInfo)
def get_job_status(job_id: str):
    md = get_job_metadata(redis, job_id)
    if not md:
        raise HTTPException(status_code=404, detail="job not found")
    return md

@app.get("/jobs", response_model=ListJobsResponse)
def list_jobs():
    jobs = list_jobs_metadata(redis, limit=100)
    return ListJobsResponse(jobs=jobs)

@app.get("/jobs/{job_id}/result")
def get_result(job_id: str):
    md = get_job_metadata(redis, job_id)
    if not md or md.status != JobStatus.COMPLETED or not md.output_path:
        raise HTTPException(status_code=404, detail="result not available")
    return FileResponse(md.output_path, media_type="video/mp4", filename=f"{job_id}.mp4")
