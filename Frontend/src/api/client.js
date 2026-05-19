import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api',
  timeout: 60000,
})

export const analyzeText = (resumeText, jobDescription) =>
  api.post('/resume/analyze', { resume_text: resumeText, job_description: jobDescription })

export const analyzeFile = (file, jobDescription) => {
  const form = new FormData()
  form.append('resume_file', file)
  form.append('job_description', jobDescription)
  return api.post('/resume/analyze/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

export const extractSkills = (resumeText) =>
  api.post('/resume/extract-skills', { resume_text: resumeText, job_description: 'n/a' })

export const getHistory = (skip = 0, limit = 20) =>
  api.get('/resume/history', { params: { skip, limit } })

export const getAnalysis = (id) =>
  api.get(`/resume/${id}`)

export const deleteAnalysis = (id) =>
  api.delete(`/resume/${id}`)

export const checkHealth = () =>
  api.get('/health')

export default api
