import styles from './ScoreCard.module.css'

const getColor = (score) => {
  if (score >= 80) return 'var(--green)'
  if (score >= 60) return 'var(--accent)'
  if (score >= 40) return 'var(--amber)'
  return 'var(--red)'
}

const priorityMap = {
  high: { label: 'High', color: 'var(--red)', bg: 'rgba(248,113,113,0.1)' },
  med:  { label: 'Medium', color: 'var(--amber)', bg: 'rgba(251,191,36,0.1)' },
  low:  { label: 'Low', color: 'var(--green)', bg: 'rgba(52,211,153,0.1)' },
}

const metricLabels = {
  skillsMatch: 'Skills Match',
  experienceRelevance: 'Experience',
  keywordDensity: 'Keywords',
  projectAlignment: 'Projects',
  communicationClarity: 'Clarity',
}

export default function ScoreCard({ result }) {
  const color = getColor(result.overallScore)

  return (
    <div className={styles.wrap}>
      {/* Score header */}
      <div className={styles.scoreCard} style={{ borderColor: color + '40' }}>
        <div className={styles.scoreLeft}>
          <div className={styles.scoreRing} style={{ '--color': color }}>
            <svg viewBox="0 0 120 120" width="120" height="120">
              <circle cx="60" cy="60" r="50" fill="none" stroke="var(--surface2)" strokeWidth="10" />
              <circle
                cx="60" cy="60" r="50"
                fill="none"
                stroke={color}
                strokeWidth="10"
                strokeLinecap="round"
                strokeDasharray={`${2 * Math.PI * 50}`}
                strokeDashoffset={`${2 * Math.PI * 50 * (1 - result.overallScore / 100)}`}
                transform="rotate(-90 60 60)"
              />
            </svg>
            <div className={styles.scoreCenter}>
              <div className={styles.scoreNum} style={{ color }}>{result.overallScore}</div>
              <div className={styles.scoreLabel}>/100</div>
            </div>
          </div>
          <div className={styles.verdict} style={{ color }}>{result.verdict}</div>
          <div className={styles.candidate}>{result.candidateName} · {result.experience}</div>
        </div>

        <div className={styles.scoreRight}>
          <div className={styles.sectionTitle}>Metrics Breakdown</div>
          {Object.entries(result.metrics || {}).map(([key, val]) => (
            <div key={key} className={styles.metric}>
              <div className={styles.metricLabel}>{metricLabels[key] || key}</div>
              <div className={styles.metricBar}>
                <div
                  className={styles.metricFill}
                  style={{ width: `${val}%`, background: getColor(val) }}
                />
              </div>
              <div className={styles.metricVal}>{val}%</div>
            </div>
          ))}
        </div>
      </div>

      {/* Summary */}
      <div className={styles.card}>
        <div className={styles.sectionTitle}>AI Summary</div>
        <p className={styles.summary}>{result.summary}</p>
      </div>

      {/* Skills */}
      <div className={styles.card}>
        <div className={styles.sectionTitle}>Skills Breakdown</div>

        <div className={styles.skillSection}>
          <div className={styles.skillLabel}>✅ Matched Skills</div>
          <div className={styles.tags}>
            {(result.matchedSkills || []).map(s => (
              <span key={s} className={styles.tagGreen}>{s}</span>
            ))}
            {!result.matchedSkills?.length && <span className={styles.empty}>None detected</span>}
          </div>
        </div>

        <div className={styles.skillSection}>
          <div className={styles.skillLabel}>❌ Missing from Resume</div>
          <div className={styles.tags}>
            {(result.missingSkills || []).map(s => (
              <span key={s} className={styles.tagRed}>{s}</span>
            ))}
            {!result.missingSkills?.length && <span className={styles.empty}>Great coverage!</span>}
          </div>
        </div>

        {result.bonusSkills?.length > 0 && (
          <div className={styles.skillSection}>
            <div className={styles.skillLabel}>⭐ Bonus Skills</div>
            <div className={styles.tags}>
              {result.bonusSkills.map(s => (
                <span key={s} className={styles.tagBlue}>{s}</span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Suggestions */}
      <div className={styles.card}>
        <div className={styles.sectionTitle}>Improvement Suggestions</div>
        {(result.suggestions || []).map((s, i) => {
          const p = priorityMap[s.priority] || priorityMap.low
          return (
            <div key={i} className={styles.suggestion} style={{ borderLeftColor: p.color }}>
              <span className={styles.priorityBadge} style={{ background: p.bg, color: p.color }}>
                {p.label}
              </span>
              <div>
                <div className={styles.suggTitle}>{s.title}</div>
                <div className={styles.suggDetail}>{s.detail}</div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
