# ResumeAI Analyzer

AI-powered full-stack resume analysis system. Upload a resume, paste a job description, and get an LLM-generated match report with skill gaps and improvement suggestions.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js (Vite) |
| Backend | FastAPI (Python) |
| Database | MongoDB (Motor async driver) |
| AI | Google Gemini API |
| PDF Parsing | pypdf |
| DOCX Parsing | python-docx |

---

## Project Structure

```
resume-analyzer/
├── main.py                    # FastAPI app + lifespan
├── requirements.txt
├── .env.example
└── app/
    ├── api/
    │   ├── resume.py          # All resume endpoints
    │   └── health.py          # Health check
    ├── core/
    │   ├── config.py          # Pydantic settings (env vars)
    │   └── database.py        # MongoDB connection manager
    ├── models/
    │   └── schemas.py         # Pydantic request/response models
    ├── services/
    │   ├── gemini_service.py  # LLM prompting + response parsing
    │   └── db_service.py      # MongoDB CRUD operations
    └── utils/
        └── file_parser.py     # PDF / DOCX / TXT text extraction
```

---

## Setup

### 1. Clone and install

```bash
git clone https://github.com/yourusername/resume-analyzer
cd resume-analyzer
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — add your GEMINI_API_KEY and MONGODB_URL
```

### 3. Start MongoDB

```bash
# Local
mongod --dbpath ./data/db

# Or via Docker
docker run -d -p 27017:27017 --name mongo mongo:7
```

### 4. Run the API

```bash
uvicorn main:app --reload --port 8000
```

API docs auto-generated at: http://localhost:8000/docs

---

## API Endpoints

### POST `/api/resume/analyze`
Analyze resume text against a job description.

**Request body:**
```json
{
  "resume_text": "...",
  "job_description": "...",
  "user_id": "optional-user-id"
}
```

**Response:**
```json
{
  "id": "664abc...",
  "overallScore": 82,
  "verdict": "Strong Match",
  "candidateName": "Danish Khan",
  "experience": "Fresher",
  "metrics": {
    "skillsMatch": 88,
    "experienceRelevance": 75,
    "keywordDensity": 84,
    "projectAlignment": 90,
    "communicationClarity": 80
  },
  "matchedSkills": ["Python", "React.js", "MongoDB", "FastAPI"],
  "missingSkills": ["Docker", "Kubernetes"],
  "bonusSkills": ["Gemini API", "LangChain"],
  "suggestions": [
    {
      "priority": "high",
      "title": "Add Docker experience",
      "detail": "The JD explicitly requires Docker. ..."
    }
  ],
  "summary": "Strong candidate with excellent project alignment..."
}
```

---

### POST `/api/resume/analyze/upload`
Upload a resume file (PDF/DOCX/TXT) as `multipart/form-data`.

**Form fields:** `resume_file` (file), `job_description` (string), `user_id` (optional)

---

### POST `/api/resume/extract-skills`
Extract categorized skills from a resume without full analysis.

---

### GET `/api/resume/history`
List past analyses. Query params: `user_id`, `skip`, `limit`.

---

### GET `/api/resume/{analysis_id}`
Fetch a single stored analysis by MongoDB ObjectId.

---

### DELETE `/api/resume/{analysis_id}`
Delete a stored analysis.

---

### GET `/api/health`
Returns database connectivity status.

---

## Prompt Engineering

The Gemini prompts are designed for structured JSON output:

1. **System persona** — expert technical recruiter framing for consistent scoring standards
2. **Strict JSON schema** — exact field names with type constraints in the prompt
3. **Scoring rubric** — inline definitions for each metric to reduce variance
4. **Post-processing** — `_parse_json_response()` strips markdown fences before parsing
5. **Pydantic validation** — LLM output is validated against typed models before storage

---

## Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev  # Vite dev server on :5173
```

Key environment variable for frontend:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## Deployment Notes

- Use `gunicorn` with `uvicorn.workers.UvicornWorker` for production
- Set `MONGODB_URL` to Atlas connection string for cloud DB
- Add rate limiting via `slowapi` to protect Gemini API quota
- Consider caching identical resume+JD pairs with Redis to reduce API costs

---

## Resume on your CV

> **AI Resume Analyzer** — Full Stack + LLM Integration  
> *React, FastAPI, Python, MongoDB, Gemini API*
>
> - Built a full-stack AI system to analyze resumes and evaluate candidate profiles against job roles
> - Integrated LLM APIs to extract skills, generate match scores, and provide personalized improvement suggestions
> - Designed RESTful APIs for resume processing, text extraction, and AI-driven analysis
> - Implemented PDF parsing and prompt-engineered workflows for structured output generation
