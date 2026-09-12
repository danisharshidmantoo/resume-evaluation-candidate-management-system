import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Analyze from './pages/Analyze'
import History from './pages/History'
import Results from './pages/Results'
import Employer from './pages/Employer'

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Analyze />} />
          <Route path="history" element={<History />} />
          <Route path="results/:id" element={<Results />} />
          <Route path="employer" element={<Employer />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
