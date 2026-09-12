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