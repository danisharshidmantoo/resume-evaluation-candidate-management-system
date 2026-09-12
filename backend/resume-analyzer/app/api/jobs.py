from fastapi import APIRouter

from app.models.schemas import JobCreate, Job
from app.services import job_service
from app.services.candidate_retrieval import CandidateRetrievalService


router = APIRouter()

retrieval_service = CandidateRetrievalService()


@router.post("/", response_model=Job)
async def create_job(job: JobCreate):
    job_id = await job_service.save_job(
        title=job.title,
        job_description=job.job_description,
    )

    return await job_service.get_job(job_id)


@router.get("/{job_id}/matches")
async def get_job_matches(job_id: str):
    job = await job_service.get_job(job_id)

    if not job:
        return {"error": "Job not found"}

    candidates = await retrieval_service.find_relevant_candidates(
        job_description=job.job_description,
    )

    return {
        "job_id": job.id,
        "candidates": candidates,
    }