import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getAnalysis } from '../api/client'
import ScoreCard from '../components/ScoreCard'
import styles from './Results.module.css'

export default function Results() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    getAnalysis(id)
      .then(res => setResult(res.data))
      .catch(() => setError('Analysis not found.'))
      .finally(() => setLoading(false))
  }, [id])

  if (loading) return (
    <div className={styles.center}>
      <div className={styles.spinner} />
    </div>
  )

  if (error) return (
    <div className={styles.error}>
      {error}
      <button className={styles.backBtn} onClick={() => navigate('/history')}>← Back to History</button>
    </div>
  )

  return (
    <div>
      <div className={styles.header}>
        <button className={styles.back} onClick={() => navigate('/history')}>← History</button>
        <div className={styles.breadcrumb}>workspace / history / result</div>
        <h1 className={styles.title}>Analysis Result</h1>
        {result?.created_at && (
          <div className={styles.date}>{new Date(result.created_at).toLocaleString()}</div>
        )}
      </div>
      {result && <ScoreCard result={result} />}
      <div style={{ height: 40 }} />
    </div>
  )
}
