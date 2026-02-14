import { createStore } from 'vuex'
import apiService from '../services/api.service'

export default createStore({
  state: {
    currentEvent: null,
    events: [],
    statistics: null,
    detectorConfig: null,
    loading: false,
    error: null
  },
  
  mutations: {
    SET_CURRENT_EVENT(state, event) {
      state.currentEvent = event
    },
    SET_EVENTS(state, events) {
      state.events = events
    },
    SET_STATISTICS(state, stats) {
      state.statistics = stats
    },
    SET_DETECTOR_CONFIG(state, config) {
      state.detectorConfig = config
    },
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    SET_ERROR(state, error) {
      state.error = error
    }
  },
  
  actions: {
    async fetchEvent({ commit }, eventId) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const event = await apiService.getEvent(eventId)
        commit('SET_CURRENT_EVENT', event)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchEvents({ commit }, params = {}) {
      commit('SET_LOADING', true)
      commit('SET_ERROR', null)
      
      try {
        const response = await apiService.getEvents(params)
        commit('SET_EVENTS', response.events)
      } catch (error) {
        commit('SET_ERROR', error.message)
      } finally {
        commit('SET_LOADING', false)
      }
    },
    
    async fetchStatistics({ commit }) {
      try {
        const stats = await apiService.getStatistics()
        commit('SET_STATISTICS', stats)
      } catch (error) {
        commit('SET_ERROR', error.message)
      }
    },
    
    async fetchDetectorConfigs({ commit }) {
      try {
        const configs = await apiService.getDetectorConfigs()
        if (configs && configs.length > 0) {
          // Get the active config or first one
          const activeConfig = configs.find(c => c.is_active) || configs[0]
          commit('SET_DETECTOR_CONFIG', activeConfig)
        }
      } catch (error) {
        commit('SET_ERROR', error.message)
      }
    }
  },
  
  getters: {
    hasCurrentEvent: state => !!state.currentEvent,
    eventCount: state => state.events.length,
    isLoading: state => state.loading,
    hasError: state => !!state.error
  }
})
