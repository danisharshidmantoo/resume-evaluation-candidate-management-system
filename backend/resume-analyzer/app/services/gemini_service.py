import json
import logging
import re
from typing import Any, Dict

from groq import Groq

from app.core.config import settings
from app.models.schemas import AnalysisResult, ExtractedSkills, SkillsExtractionResponse

logger = logging.getLogger(__name__)


def _parse_json_response(raw: str) -> Dict[str, Any]:
    cleaned = re.sub(r"```(?:json)?", "", raw).strip().rstrip("```")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error. Raw:\n{raw}\nError: {e}")
        raise ValueError(f"LLM returned invalid JSON: {e}")


ANALYSIS_PROMPT = """You are an expert technical recruiter. Analyze the resume against the job description.

Return ONLY a valid JSON object with this exact structure:
{{
  "overallScore": <integer 0-100>,
  "verdict": "<Excellent Match | Strong Match | Good Match | Partial Match | Weak Match>",
  "candidateName": "<name from resume or Unknown>",
  "experience": "<Fresher | Junior | Mid-Level | Senior>",
  "metrics": {{
    "skillsMatch": <integer 0-100>,
    "experienceRelevance": <integer 0-100>,
    "keywordDensity": <integer 0-100>,
    "projectAlignment": <integer 0-100>,
    "communicationClarity": <integer 0-100>
  }},
  "matchedSkills": ["skill1", "skill2"],
  "missingSkills": ["skill1", "skill2"],
  "bonusSkills": ["skill1", "skill2"],
  "suggestions": [
    {{"priority": "high", "title": "title", "detail": "2-3 sentence suggestion"}},
    {{"priority": "high", "title": "title", "detail": "2-3 sentence suggestion"}},
    {{"priority": "med", "title": "title", "detail": "2-3 sentence suggestion"}},
    {{"priority": "low", "title": "title", "detail": "2-3 sentence suggestion"}}
  ],
  "summary": "<3-4 sentence overall assessment>"
}}

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Return only valid JSON, no markdown, no extra text."""


SKILLS_PROMPT = """Extract skills from this resume. Return ONLY valid JSON:
{{
  "technical": ["skill"],
  "soft": ["skill"],
  "tools": ["tool"],
  "languages": ["language"],
  "frameworks": ["framework"]
}}

RESUME:
{resume_text}"""


async def analyze_resume(resume_text: str, job_description: str) -> AnalysisResult:
    client = Groq(api_key=settings.GEMINI_API_KEY)

    prompt = ANALYSIS_PROMPT.format(
        resume_text=resume_text.strip(),
        job_description=job_description.strip()
    )

    logger.info(f"Sending request to Groq ({settings.GEMINI_MODEL})")
    response = client.chat.completions.create(
        model=settings.GEMINI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2000,
    )

    raw = response.choices[0].message.content
    data = _parse_json_response(raw)
    result = AnalysisResult(**data)
    logger.info(f"Analysis complete: score={result.overallScore}")
    return result


async def extract_skills(resume_text: str) -> SkillsExtractionResponse:
    client = Groq(api_key=settings.GEMINI_API_KEY)

    prompt = SKILLS_PROMPT.format(resume_text=resume_text.strip())
    response = client.chat.completions.create(
        model=settings.GEMINI_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=500,
    )

    raw = response.choices[0].message.content
    data = _parse_json_response(raw)
    return SkillsExtractionResponse(
        skills=ExtractedSkills(**data),
        raw_text_length=len(resume_text),
    )