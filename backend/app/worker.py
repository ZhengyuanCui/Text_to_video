import os
from celery import Celery
from redis import Redis
from .gpu_pool import next_device
from .model.mochi import get_model_for_device
from .storage import set_job_metadata, ARTIFACT_DIR
from .schemas import JobStatus

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis = Redis.from_url(REDIS_URL, decode_responses=True)

celery_app = Celery("text2video")
celery_app.config_from_object("celeryconfig")

@celery_app.task(name="generate_video")
def generate_video(prompt: str, length_sec: int, resolution: str):
    job_id = generate_video.request.id
    try:
        set_job_metadata(redis, job_id, status=JobStatus.PROCESSING)
        device_id = next_device()
        model = get_model_for_device(device_id)
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        out_path = os.path.join(ARTIFACT_DIR, f"{job_id}.mp4")
        model.generate(prompt, length_sec, resolution, out_path)
        set_job_metadata(redis, job_id, status=JobStatus.COMPLETED, output_path=out_path)
        return {"output_path": out_path}
    except Exception as e:
        set_job_metadata(redis, job_id, status=JobStatus.FAILED, error=str(e))
        raise
