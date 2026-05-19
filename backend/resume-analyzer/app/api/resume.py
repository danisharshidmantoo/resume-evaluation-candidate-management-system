import logging
from typing import List, Optional

from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile, status

from app.core.config import settings
from app.models.schemas import (
    AnalysisListItem,
    AnalysisResult,
    AnalyzeTextRequest,
    SkillsExtractionResponse,
)
from app.services import db_service, gemini_service
from app.utils.file_parser import extract_text_from_file, validate_file_size

logger = logging.getLogger(__name__)
router = APIRouter()


# ─── Analyze from raw text ────────────────────────────────────────────────────

@router.post(
    "/analyze",
    response_model=AnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Analyze resume text against a job description",
)
async def analyze_resume_text(body: AnalyzeTextRequest):
    """
    Submit resume text and job description for AI-powered analysis.

    Returns a structured match report with:
    - Overall score (0–100)
    - Metrics breakdown across 5 dimensions
    - Matched/missing/bonus skills
    - Prioritized improvement suggestions
    - Human-readable summary
    """
    try:
        result = await gemini_service.analyze_resume(
            resume_text=body.resume_text,
            job_description=body.job_description,
        )
        doc_id = await db_service.save_analysis(result, user_id=body.user_id)
        result.id = doc_id
        return result

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="AI analysis failed. Please try again.")


# ─── Analyze from file upload ────────────────────────────────────────────────

@router.post(
    "/analyze/upload",
    response_model=AnalysisResult,
    status_code=status.HTTP_200_OK,
    summary="Upload a resume file and analyze against a job description",
)
async def analyze_resume_file(
    resume_file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., min_length=30, description="Target job description"),
    user_id: Optional[str] = Form(None),
):
    """
    Upload a resume file (PDF/DOCX/TXT) and analyze it against a job description.
    Text is extracted automatically before being sent to the AI.
    """
    # Validate extension
    filename = resume_file.filename or ""
    allowed = settings.ALLOWED_EXTENSIONS
    if not any(filename.lower().endswith(ext) for ext in allowed):
        raise HTTPException(
            status_code=415,
            detail=f"Unsupported file type. Allowed: {', '.join(allowed)}",
        )

    file_bytes = await resume_file.read()

    try:
        validate_file_size(file_bytes, max_mb=settings.MAX_FILE_SIZE_MB)
        resume_text, fmt = extract_text_from_file(file_bytes, filename)
        logger.info(f"Extracted {len(resume_text)} chars from {fmt.upper()} file")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if len(resume_text.strip()) < 50:
        raise HTTPException(
            status_code=422,
            detail="Extracted text is too short. Please ensure the file contains readable text.",
        )

    try:
        result = await gemini_service.analyze_resume(
            resume_text=resume_text,
            job_description=job_description,
        )
        doc_id = await db_service.save_analysis(result, user_id=user_id)
        result.id = doc_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="AI analysis failed. Please try again.")


# ─── Extract skills only ──────────────────────────────────────────────────────

@router.post(
    "/extract-skills",
    response_model=SkillsExtractionResponse,
    summary="Extract categorized skills from a resume",
)
async def extract_skills(body: AnalyzeTextRequest):
    """
    Extract and categorize skills from a resume without running a full analysis.
    Returns skills grouped as: technical, soft, tools, languages, frameworks.
    """
    try:
        return await gemini_service.extract_skills(body.resume_text)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Skill extraction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Skill extraction failed.")


# ─── Get analysis history ────────────────────────────────────────────────────

@router.get(
    "/history",
    response_model=List[AnalysisListItem],
    summary="List past analyses",
)
async def get_history(
    user_id: Optional[str] = Query(None, description="Filter by user ID"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
):
    return await db_service.list_analyses(user_id=user_id, skip=skip, limit=limit)


# ─── Get single analysis ──────────────────────────────────────────────────────

@router.get(
    "/{analysis_id}",
    response_model=AnalysisResult,
    summary="Get a specific analysis by ID",
)
async def get_analysis(analysis_id: str):
    result = await db_service.get_analysis(analysis_id)
    if not result:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return result


# ─── Delete analysis ──────────────────────────────────────────────────────────

@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an analysis",
)
async def delete_analysis(analysis_id: str):
    deleted = await db_service.delete_analysis(analysis_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis not found")
