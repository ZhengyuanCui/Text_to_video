from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class SubmitJobRequest(BaseModel):
    prompt: str
    length_sec: int = 4
    resolution: str = "512x512"

class SubmitJobResponse(BaseModel):
    job_id: str

class JobStatus(str):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class JobInfo(BaseModel):
    job_id: str
    status: JobStatus
    created_at: datetime
    updated_at: datetime
    error: Optional[str] = None
    output_path: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True

class ListJobsResponse(BaseModel):
    jobs: List[JobInfo]
