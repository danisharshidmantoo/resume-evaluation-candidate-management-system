import { Outlet, NavLink } from 'react-router-dom'
import styles from './Layout.module.css'

const nav = [
  { to: '/', label: 'Analyze', icon: '⚡' },
  { to: '/history', label: 'History', icon: '🕓' },
]

export default function Layout() {
  return (
    <div className={styles.shell}>
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          <span className={styles.logoMark}>R/</span>
          <div>
            <div className={styles.logoName}>ResumeAI</div>
            <div className={styles.logoSub}>Analyzer v1.0</div>
          </div>
        </div>
        <nav className={styles.nav}>
          {nav.map(({ to, label, icon }) => (
            <NavLink
              key={to}
              to={to}
              end={to === '/'}
              className={({ isActive }) =>
                `${styles.navItem} ${isActive ? styles.active : ''}`
              }
            >
              <span>{icon}</span>
              {label}
            </NavLink>
          ))}
        </nav>
        <div className={styles.footer}>
          FastAPI · MongoDB · Gemini AI
        </div>
      </aside>
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}
