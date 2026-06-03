import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

// create axios instance with base URL
// all requests automatically prepend this URL
const api = axios.create({
    baseURL: API_BASE_URL
})

// runs a full evaluation for a single prompt
// data = { prompt, model_id, reference, source }
export const evaluateModel = async (data) => {
    const response = await api.post('/evaluate', data)
    return response.data
}

// fetches all evaluation results ordered by most recent
export const getAllResults = async () => {
    const response = await api.get('/results')
    return response.data
}

// fetches all evaluations for a specific model
export const getResultsByModel = async (modelId) => {
    const response = await api.get(`/results/${modelId}`)
    return response.data
}