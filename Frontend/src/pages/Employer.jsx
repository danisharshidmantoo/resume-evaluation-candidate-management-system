import { useState } from 'react'
import { createJob, getJobMatches } from '../api/client'
import styles from './Employer.module.css'

export default function Employer() {
  const [title, setTitle] = useState('')
  const [jobDescription, setJobDescription] = useState('')

  const [job, setJob] = useState(null)
  const [candidates, setCandidates] = useState([])

  const [creating, setCreating] = useState(false)
  const [fetching, setFetching] = useState(false)
  const [error, setError] = useState('')

  const handleCreateJob = async () => {
    setError('')
    setCreating(true)

    try {
      const response = await createJob(title, jobDescription)
      setJob(response.data)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to create job.'
      )
    } finally {
      setCreating(false)
    }
  }

  const handleFetchResults = async () => {
    if (!job) return

    setError('')
    setFetching(true)

    try {
      const response = await getJobMatches(job.id)
      setCandidates(response.data.candidates || [])
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Failed to fetch candidate matches.'
      )
    } finally {
      setFetching(false)
    }
  }

  const canCreate =
    title.trim().length > 0 &&
    jobDescription.trim().length > 30 &&
    !creating

  return (
    <div>
      <div className={styles.header}>
        <div className={styles.breadcrumb}>
          workspace / jobs
        </div>

        <h1 className={styles.title}>
          Candidate Management
        </h1>

        <p className={styles.subtitle}>
          Create a job and find the most relevant candidates from your resume pool.
        </p>
      </div>

      {!job && (
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <span className={styles.cardTitle}>
              Create Job
            </span>
          </div>

          <label className={styles.label}>
            Job Title
          </label>

          <input
            className={styles.input}
            type="text"
            placeholder="e.g. Machine Learning Engineer"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />

          <label className={styles.label}>
            Job Description
          </label>

          <textarea
            className={styles.textarea}
            rows={10}
            placeholder="Paste the job description..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          {error && (
            <div className={styles.error}>
              {error}
            </div>
          )}

          <div className={styles.actions}>
            <span className={styles.charCount}>
              {jobDescription.length} characters
            </span>

            <button
              className={styles.primaryButton}
              onClick={handleCreateJob}
              disabled={!canCreate}
            >
              {creating ? 'Creating...' : 'Create Job'}
            </button>
          </div>
        </div>
      )}

      {job && (
        <>
          <div className={styles.card}>
            <div className={styles.jobHeader}>
              <div>
                <div className={styles.jobLabel}>
                  JOB
                </div>

                <h2 className={styles.jobTitle}>
                  {job.title}
                </h2>
              </div>

              <div className={styles.createdBadge}>
                Created
              </div>
            </div>

            <div className={styles.divider} />

            <div className={styles.jobDescription}>
              {job.job_description}
            </div>

            {error && (
              <div className={styles.error}>
                {error}
              </div>
            )}

            <div className={styles.actions}>
              <span className={styles.helperText}>
                Search the indexed candidate resumes for this role.
              </span>

              <button
                className={styles.primaryButton}
                onClick={handleFetchResults}
                disabled={fetching}
              >
                {fetching
                  ? 'Finding Candidates...'
                  : '⚡ Fetch Top Results'}
              </button>
            </div>
          </div>

          {fetching && (
            <div className={styles.loadingCard}>
              <div className={styles.spinner} />

              <div className={styles.loadingTitle}>
                Finding relevant candidates
              </div>

              <div className={styles.loadingSub}>
                Embedding job description · Searching resume vectors · Ranking candidates
              </div>
            </div>
          )}

          {!fetching && candidates.length > 0 && (
            <div className={styles.resultsCard}>
              <div className={styles.resultsHeader}>
                <div>
                  <div className={styles.cardTitle}>
                    Top Candidates
                  </div>

                  <div className={styles.resultsSub}>
                    Semantic retrieval + DSA-driven ranking
                  </div>
                </div>

                <div className={styles.resultCount}>
                  {candidates.length} candidates
                </div>
              </div>

              <div className={styles.candidateList}>
                {candidates.map((candidate, index) => (
                  <div
                    key={candidate.candidate_id}
                    className={styles.candidate}
                  >
                    <div className={styles.rank}>
                      {String(index + 1).padStart(2, '0')}
                    </div>

                    <div className={styles.candidateInfo}>
                      <div className={styles.candidateName}>
                        {candidate.name}
                      </div>

                      <div className={styles.candidateMeta}>
                        {candidate.matched_chunks} matched chunks
                      </div>
                    </div>

                    <div className={styles.match}>
                      <div className={styles.matchLabel}>
                        DISTANCE
                      </div>

                      <div className={styles.matchValue}>
                        {candidate.distance.toFixed(3)}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!fetching && candidates.length === 0 && (
            <div className={styles.empty}>
              Click <strong>Fetch Top Results</strong> to search the candidate pool.
            </div>
          )}
        </>
      )}
    </div>
  )
}