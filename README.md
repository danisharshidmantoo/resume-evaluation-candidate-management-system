# Resume Evaluation & Candidate Management System

A full-stack AI-powered platform for **resume evaluation and intelligent candidate matching**.

The system combines **FastAPI, React, MongoDB, LLM APIs, vector embeddings, ChromaDB, and algorithmic ranking** to evaluate resumes against job descriptions and help employers discover the most relevant candidates from a resume pool.

---

## Overview

The system supports two core workflows:

### Candidate Workflow

A candidate can:

- Upload or provide their resume
- Provide a job description
- Receive an AI-generated resume evaluation
- View match scores and compatibility analysis
- Receive improvement recommendations
- Access previous analysis results

### Employer Workflow

An employer can:

- Create a job posting
- Store the job description in MongoDB
- Retrieve the most relevant candidates from the indexed resume pool
- Rank candidates using semantic similarity and DSA-driven ranking logic

The employer does **not** need to manually inspect every resume.

Instead:

```text
Job Description
      ↓
Embedding
      ↓
Vector Search
      ↓
Relevant Resume Chunks
      ↓
Candidate Aggregation
      ↓
Ranking
      ↓
Top Candidates

Key Features
AI-Powered Resume Evaluation

Resumes and job descriptions are processed and evaluated using an LLM to generate:

Match scoring
Compatibility analysis
Strengths and weaknesses
Improvement recommendations
Semantic Candidate Search

Candidate resumes are split into smaller chunks and converted into vector embeddings.

When an employer searches for candidates:

The job description is converted into an embedding.
ChromaDB performs semantic similarity search against indexed resume chunks.
The most relevant chunks are retrieved.
Chunks are grouped back by candidate.
Candidates are ranked based on their strongest matching chunks.

This allows the system to retrieve candidates based on meaning and contextual similarity, rather than relying only on keyword matching.

Chunk-Level Resume Indexing

Instead of storing one vector for an entire resume, resumes are divided into multiple chunks.

Resume
 ├── Chunk 0 → Vector
 ├── Chunk 1 → Vector
 ├── Chunk 2 → Vector
 ├── Chunk 3 → Vector
 └── ...

Each chunk stores metadata such as:

candidate_id
chunk_index

This allows the system to identify which candidate each retrieved chunk belongs to.

DSA-Driven Candidate Ranking

Retrieved chunks are grouped using a dictionary/hash map:

candidate_id → matched chunk distances

For each candidate:

Matching chunks are collected
Distances are sorted
The strongest matching chunks are selected
Their average distance is calculated
Candidates are sorted by the resulting score

Lower vector distance indicates stronger semantic similarity.

Persistent Storage

MongoDB stores structured application data including:

Candidate records
Resume text
Job descriptions
Job records
AI-generated evaluation results

ChromaDB acts as the semantic retrieval index for candidate resume chunks.

System Architecture
                         ┌──────────────────────┐
                         │      React UI        │
                         │                      │
                         │ Candidate / Employer │
                         └──────────┬───────────┘
                                    │
                                    │ HTTP
                                    ▼
                         ┌──────────────────────┐
                         │      FastAPI         │
                         │       Backend        │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌─────────────┐       ┌─────────────┐      ┌─────────────┐
       │   MongoDB   │       │ Embedding   │      │  LLM API    │
       │             │       │   Model     │      │             │
       │ Candidates  │       │             │      │ Evaluation   │
       │ Jobs        │       │ MiniLM      │      │             │
       │ Analyses    │       │             │      │             │
       └─────────────┘       └──────┬──────┘      └─────────────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │   ChromaDB    │
                            │               │
                            │ Resume Vector │
                            │    Index      │
                            └───────┬───────┘
                                    │
                                    ▼
                            ┌───────────────┐
                            │    Ranking    │
                            │               │
                            │ Chunk Grouping│
                            │ Top-K Selection
                            │ Distance Avg. │
                            │ Candidate Sort│
                            └───────────────┘
RAG / Candidate Matching Pipeline

The employer candidate-matching workflow follows this architecture:

Employer
   │
   │ Create Job
   ▼
MongoDB
   │
   │ Fetch Top Results
   ▼
Retrieve Job Description
   │
   ▼
Sentence Transformer
   │
   │ Job Embedding
   ▼
ChromaDB
   │
   │ Semantic Similarity Search
   ▼
Top Resume Chunks
   │
   ▼
Group by candidate_id
   │
   ▼
Select strongest matching chunks
   │
   ▼
Calculate candidate distance
   │
   ▼
Sort candidates
   │
   ▼
MongoDB
   │
   │ Retrieve candidate details
   ▼
Ranked Candidates
Resume Indexing Pipeline

When a candidate resume is added to the system:

Resume
  ↓
Text Extraction
  ↓
Recursive Character Chunking
  ↓
Resume Chunks
  ↓
Sentence Transformer Embeddings
  ↓
ChromaDB

Example:

Candidate Resume
      │
      ├── Chunk 0 ──→ Embedding ──→ ChromaDB
      ├── Chunk 1 ──→ Embedding ──→ ChromaDB
      ├── Chunk 2 ──→ Embedding ──→ ChromaDB
      └── Chunk N ──→ Embedding ──→ ChromaDB

Each vector is associated with the original candidate through metadata.

Technology Stack
Frontend
React
React Router
Axios
Vite
CSS Modules
Backend
Python
FastAPI
Pydantic
Uvicorn
AI / Machine Learning
LLM API for resume evaluation
Sentence Transformers
all-MiniLM-L6-v2
Vector embeddings
Semantic similarity search
RAG / Vector Database
ChromaDB
LangChain Text Splitters
Database
MongoDB
Motor / PyMongo
Development
Git
GitHub
ESLint
Project Structure
Resume_Analyser/
│
├── backend/
│   └── resume-analyzer/
│       │
│       ├── app/
│       │   ├── api/
│       │   ├── core/
│       │   ├── models/
│       │   └── services/
│       │
│       ├── data/
│       │   └── chroma/
│       │
│       ├── main.py
│       └── requirements.txt
│
├── Frontend/
│   ├── src/
│   │   ├── api/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   └── main.jsx
│   │
│   ├── package.json
│   └── vite.config.js
│
└── README.md
API Design
Resume Evaluation
POST /api/resume/analyze

Evaluates resume text against a job description.

Resume Upload
POST /api/resume/analyze/upload

Accepts a resume file and job description.

Analysis History
GET /api/resume/history

Retrieves previous resume evaluations.

Create Job
POST /api/jobs/

Creates and persists an employer job.

Example:

{
  "title": "Machine Learning Engineer",
  "job_description": "We are looking for a Machine Learning Engineer with strong Python, machine learning, TensorFlow, and scikit-learn experience."
}
Retrieve Candidate Matches
GET /api/jobs/{job_id}/matches

Runs semantic retrieval and candidate ranking for a job.

Example response:

{
  "job_id": "6aa4e7b2a35106a2476369d5",
  "candidates": [
    {
      "candidate_id": "...",
      "name": "Danish Arshid",
      "distance": 0.427,
      "matched_chunks": 3
    },
    {
      "candidate_id": "...",
      "name": "Danish Arshid",
      "distance": 0.556,
      "matched_chunks": 3
    }
  ]
}
Running Locally
1. Start MongoDB

Make sure MongoDB is running locally.

2. Start the FastAPI Backend

From:

backend/resume-analyzer

run:

../venv/bin/python -m uvicorn main:app --reload

The API will be available at:

http://localhost:8000
3. Start the React Frontend

From:

Frontend

run:

npm install
npm run dev

The frontend will be available at:

http://localhost:5173
Example Employer Flow

Create a job:

Machine Learning Engineer

with requirements such as:

Python
Machine Learning
TensorFlow
scikit-learn

Then select:

Fetch Top Results

The system performs semantic retrieval across the indexed resume pool and returns ranked candidates.

Example:

┌──────┬────────────────┬──────────────┐
│ Rank │ Candidate      │ Distance     │
├──────┼────────────────┼──────────────┤
│ 01   │ Candidate A    │ 0.427        │
│ 02   │ Candidate B    │ 0.556        │
└──────┴────────────────┴──────────────┘

A lower distance represents a stronger semantic match.

Engineering Decisions
Why chunk resumes?

Embedding an entire resume into one vector can lose important local information.

Chunking allows different sections of a resume to independently match different parts of a job description.

Why use ChromaDB?

ChromaDB provides a persistent vector store and similarity-search interface suitable for maintaining an indexed pool of resume chunks.

Why store candidate data in MongoDB?

MongoDB remains the source of truth for structured candidate and job information, while ChromaDB is used specifically for semantic retrieval.

This separates:

Structured Data → MongoDB
Semantic Index   → ChromaDB
Why group results by candidate?

Vector search operates on chunks, but employers ultimately need candidate-level results.

Therefore the system converts:

Chunk-level retrieval
        ↓
Candidate-level ranking

using the candidate_id metadata stored with every vector.

Current Status
Completed
 Resume text extraction
 Resume evaluation using an LLM
 AI-generated match scoring
 Compatibility analysis
 Improvement recommendations
 MongoDB persistence
 React dashboard
 Analysis history
 Resume chunking
 Vector embeddings
 ChromaDB resume index
 Job creation
 Semantic candidate retrieval
 Candidate-level aggregation
 DSA-driven candidate ranking
 Employer candidate-matching UI
 End-to-end Job → Candidates workflow
Planned
 Authentication
 Role-based authorization
 Candidate / Employer account separation
 Candidate ownership enforcement
 Employer job ownership enforcement
 Candidate profile management
 Employer candidate profiles
 Improved ranking and scoring strategies
 Production deployment
Future Authentication Architecture

The application is being designed around two roles:

                    Authentication
                         │
              ┌──────────┴──────────┐
              │                     │
          Candidate              Employer
              │                     │
       ┌──────┴──────┐       ┌──────┴──────┐
       │             │       │             │
    Analyze       History    Jobs      Candidates

Authorization will be enforced at the backend API level, rather than relying only on frontend visibility.

For example:

Candidate
    ↓
Can access own analyses
Can access own history
Cannot access employer APIs

Employer
    ↓
Can create own jobs
Can retrieve candidates for own jobs
Cannot access candidate-only resources
Why This Project?

Traditional resume screening often relies heavily on keyword matching.

This project explores a more intelligent approach:

Keyword Matching
       ↓
Semantic Retrieval
       ↓
Chunk-Level Matching
       ↓
Candidate Aggregation
       ↓
Algorithmic Ranking

The result is a system that combines LLM-based reasoning, vector search, database design, and classical data structures/algorithms into a practical full-stack application.

Author

Danish Arshid

Built with:

Python · FastAPI · React · MongoDB · ChromaDB
Sentence Transformers · LLM APIs · RAG

### One thing I especially like about this README

It tells a recruiter **what you actually engineered**, rather than just listing technologies.

The strongest section for your resume/project is probably this progression:

```text
Resume
  ↓
Chunking
  ↓
Embeddings
  ↓
ChromaDB
  ↓
Semantic Retrieval
  ↓
Hash Map Aggregation
  ↓
Sorting / Top-K Selection
  ↓
Candidate Ranking
  ↓
MongoDB
  ↓
React

