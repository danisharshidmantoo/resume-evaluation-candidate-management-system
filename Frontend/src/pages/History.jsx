import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getHistory, deleteAnalysis } from '../api/client'
import styles from './History.module.css'

const getColor = (score) => {
  if (score >= 80) return 'var(--green)'
  if (score >= 60) return 'var(--accent)'
  if (score >= 40) return 'var(--amber)'
  return 'var(--red)'
}

export default function History() {
  const navigate = useNavigate()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      const res = await getHistory()
      setItems(res.data)
    } catch {
      setError('Failed to load history. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const handleDelete = async (e, id) => {
    e.stopPropagation()
    try {
      await deleteAnalysis(id)
      setItems(items.filter(i => i.id !== id))
    } catch {
      alert('Delete failed.')
    }
  }

  if (loading) return (
    <div className={styles.center}>
      <div className={styles.spinner} />
      <div className={styles.loadingText}>Loading history...</div>
    </div>
  )

  if (error) return <div className={styles.error}>{error}</div>

  return (
    <div>
      <div className={styles.header}>
        <div className={styles.breadcrumb}>workspace / history</div>
        <h1 className={styles.title}>Analysis History</h1>
        <p className={styles.subtitle}>All past resume analyses stored in MongoDB.</p>
      </div>

      {items.length === 0 ? (
        <div className={styles.empty}>
          <div className={styles.emptyIcon}>🕓</div>
          <div className={styles.emptyText}>No analyses yet.</div>
          <div className={styles.emptySub}>Run your first analysis to see it here.</div>
          <button className={styles.goBtn} onClick={() => navigate('/')}>
            Go to Analyzer →
          </button>
        </div>
      ) : (
        <div className={styles.list}>
          {items.map(item => {
            const color = getColor(item.overallScore)
            return (
              <div
                key={item.id}
                className={styles.item}
                onClick={() => navigate(`/results/${item.id}`)}
              >
                <div className={styles.scoreBox} style={{ background: color + '20', color }}>
                  {item.overallScore}
                </div>
                <div className={styles.itemInfo}>
                  <div className={styles.itemName}>{item.candidateName}</div>
                  <div className={styles.itemDate}>
                    {new Date(item.created_at).toLocaleString()}
                  </div>
                </div>
                <span className={styles.verdict} style={{ background: color + '15', color, borderColor: color + '30' }}>
                  {item.verdict}
                </span>
                <button
                  className={styles.deleteBtn}
                  onClick={(e) => handleDelete(e, item.id)}
                  title="Delete"
                >
                  🗑
                </button>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
