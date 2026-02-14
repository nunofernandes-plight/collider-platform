import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  // Events
  async getEvent(eventId) {
    const response = await apiClient.get(`/events/${eventId}`)
    return response.data
  },
  
  async getEvents(params = {}) {
    const response = await apiClient.get('/events', { params })
    return response.data
  },
  
  async generateEvents(eventType = 'random', numEvents = 10) {
    const response = await apiClient.post('/collisions/generate', {
      event_type: eventType,
      num_events: numEvents
    })
    return response.data
  },
  
  // Analysis
  async getHistogram(variable, bins = 50, rangeMin = null, rangeMax = null) {
    const response = await apiClient.post('/analysis/histogram', {
      variable,
      bins,
      range_min: rangeMin,
      range_max: rangeMax
    })
    return response.data
  },
  
  async getStatistics() {
    const response = await apiClient.get('/statistics/summary')
    return response.data
  },
  
  // Configuration
  async getDetectorConfigs() {
    const response = await apiClient.get('/config/detector')
    return response.data
  }
}
