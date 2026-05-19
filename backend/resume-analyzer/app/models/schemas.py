from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from datetime import datetime


# ─── Request Models ───────────────────────────────────────────────────────────

class AnalyzeTextRequest(BaseModel):
    resume_text: str = Field(..., min_length=50, description="Full resume text content")
    job_description: str = Field(..., min_length=30, description="Target job description")
    user_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "resume_text": "John Doe\nSoftware Engineer\n5 years Python experience...",
                "job_description": "We are looking for a Senior Python Developer...",
            }
        }


# ─── Response Models ──────────────────────────────────────────────────────────

class MetricsBreakdown(BaseModel):
    skillsMatch: int = Field(..., ge=0, le=100)
    experienceRelevance: int = Field(..., ge=0, le=100)
    keywordDensity: int = Field(..., ge=0, le=100)
    projectAlignment: int = Field(..., ge=0, le=100)
    communicationClarity: int = Field(..., ge=0, le=100)


class ImprovementSuggestion(BaseModel):
    priority: Literal["high", "med", "low"]
    title: str
    detail: str


class AnalysisResult(BaseModel):
    id: Optional[str] = None
    overallScore: int = Field(..., ge=0, le=100)
    verdict: str
    candidateName: str
    experience: str
    metrics: MetricsBreakdown
    matchedSkills: List[str]
    missingSkills: List[str]
    bonusSkills: List[str]
    suggestions: List[ImprovementSuggestion]
    summary: str
    created_at: Optional[datetime] = None


class AnalysisListItem(BaseModel):
    id: str
    candidateName: str
    overallScore: int
    verdict: str
    created_at: datetime


class ExtractedSkills(BaseModel):
    technical: List[str]
    soft: List[str]
    tools: List[str]
    languages: List[str]
    frameworks: List[str]


class SkillsExtractionResponse(BaseModel):
    skills: ExtractedSkills
    raw_text_length: int
