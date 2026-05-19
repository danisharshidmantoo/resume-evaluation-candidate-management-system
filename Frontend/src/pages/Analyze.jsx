import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeText, analyzeFile } from '../api/client'
import ScoreCard from '../components/ScoreCard'
import styles from './Analyze.module.css'

export default function Analyze() {
  const navigate = useNavigate()
  const [resumeText, setResumeText] = useState('')
  const [jdText, setJdText] = useState('')
  const [file, setFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  const handleFile = (f) => {
    if (!f) return
    setFile(f)
    const reader = new FileReader()
    reader.onload = (e) => setResumeText(e.target.result)
    reader.readAsText(f)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    const f = e.dataTransfer.files[0]
    if (f) handleFile(f)
  }

  const handleSubmit = async () => {
    setError('')
    setResult(null)
    setLoading(true)
    try {
      let res
      if (file) {
        res = await analyzeFile(file, jdText)
      } else {
        res = await analyzeText(resumeText, jdText)
      }
      setResult(res.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Check your API key and try again.')
    } finally {
      setLoading(false)
    }
  }

  const canSubmit = resumeText.trim().length > 50 && jdText.trim().length > 30 && !loading

  const loadDemo = () => {
    setResumeText(`DANISH KHAN
Final Year B.Tech CSE | 2022BCSE082
Email: danish@example.com | GitHub: github.com/danish

SKILLS
Python, JavaScript, React.js, Node.js, FastAPI, MongoDB, Gemini API, Docker, Git

PROJECTS
SmartNotes — AI Note-Taking App
• Built full-stack app using React.js, Node.js, MongoDB, Gemini API
• Implemented AI flashcards, ELI5 explanations, smart summaries
• Reduced note review time by 35%

Resume Analyzer — Full Stack + LLM
• Built AI resume analysis system with FastAPI and Gemini API
• Designed RESTful APIs for resume processing and text extraction
• Implemented PDF parsing and prompt-engineered workflows

EDUCATION
B.Tech Computer Science — 2022–2026 | CGPA: 8.4/10

EXPERIENCE
Web Dev Intern — TechStartup (Summer 2024)
• Built 3 REST APIs in FastAPI serving 500+ daily requests`)

    setJdText(`SDE-1 — Full Stack Engineer
Requirements:
• Proficiency in Python and JavaScript/TypeScript
• Experience with React.js or similar frontend frameworks  
• Backend with Node.js, FastAPI, or Django
• REST APIs and microservices architecture
• MongoDB or PostgreSQL
• Git, CI/CD, deployment pipelines
• Bonus: LLM APIs (OpenAI, Gemini)
• Strong DSA fundamentals`)
  }

  return (
    <div>
      <div className={styles.header}>
        <div className={styles.breadcrumb}>workspace / analyze</div>
        <h1 className={styles.title}>Resume Analyzer</h1>
        <p className={styles.subtitle}>
          Upload your resume and paste a job description to get an AI-powered match report.
        </p>
      </div>

      {!result && (
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <span className={styles.cardTitle}>Resume</span>
            <button className={styles.demoBtn} onClick={loadDemo}>Load Demo ↗</button>
          </div>

          {/* Upload zone */}
          <div
            className={styles.uploadZone}
            onDrop={handleDrop}
            onDragOver={(e) => e.preventDefault()}
            onClick={() => document.getElementById('file-input').click()}
          >
            <div className={styles.uploadIcon}>📄</div>
            <div className={styles.uploadTitle}>Drop resume here or click to browse</div>
            <div className={styles.uploadSub}>PDF, DOCX, TXT supported</div>
            {file && <div className={styles.filePill}>📎 {file.name}</div>}
          </div>
          <input
            id="file-input"
            type="file"
            accept=".pdf,.docx,.txt"
            style={{ display: 'none' }}
            onChange={(e) => handleFile(e.target.files[0])}
          />

          <div className={styles.divider}><span>or paste text</span></div>

          <label className={styles.label}>Resume Content</label>
          <textarea
            className={styles.textarea}
            rows={7}
            placeholder="Paste your full resume — experience, skills, education, projects..."
            value={resumeText}
            onChange={(e) => setResumeText(e.target.value)}
          />

          <div className={styles.divider}><span>Job Description</span></div>

          <label className={styles.label}>Target Role / JD</label>
          <textarea
            className={styles.textarea}
            rows={5}
            placeholder="Paste the job description you're targeting..."
            value={jdText}
            onChange={(e) => setJdText(e.target.value)}
          />

          {error && <div className={styles.error}>{error}</div>}

          <div className={styles.actions}>
            <span className={styles.charCount}>
              Resume: {resumeText.length} chars · JD: {jdText.length} chars
            </span>
            <button
              className={styles.analyzeBtn}
              onClick={handleSubmit}
              disabled={!canSubmit}
            >
              {loading ? 'Analyzing...' : '⚡ Analyze Now'}
            </button>
          </div>
        </div>
      )}

      {loading && (
        <div className={styles.loaderCard}>
          <div className={styles.spinner} />
          <div className={styles.loaderText}>Analyzing with Gemini AI...</div>
          <div className={styles.loaderSub}>Extracting skills · Scoring match · Generating suggestions</div>
        </div>
      )}

      {result && !loading && (
        <div className={styles.resultWrap}>
          <ScoreCard result={result} />
          <div className={styles.resultActions}>
            <button className={styles.backBtn} onClick={() => setResult(null)}>
              ← Edit & Re-analyze
            </button>
            {result.id && (
              <button className={styles.historyBtn} onClick={() => navigate('/history')}>
                View in History →
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
