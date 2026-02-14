<template>
  <div class="configuration-view">
    <h2>Detector Configuration</h2>
    <p class="subtitle">Digital Twin Configuration Management</p>
    
    <div v-if="configs.length > 0" class="config-grid">
      <div
        v-for="config in configs"
        :key="config.id"
        class="config-card"
        :class="{ active: config.is_active }"
      >
        <div class="config-header">
          <h3>{{ config.name }}</h3>
          <span v-if="config.is_active" class="active-badge">Active</span>
        </div>
        
        <p class="config-description">{{ config.description }}</p>
        
        <div class="config-details">
          <div class="detail-row">
            <span class="label">Magnetic Field:</span>
            <span class="value">{{ config.magnetic_field }} T</span>
          </div>
          
          <div class="detail-section">
            <h4>Tracker</h4>
            <div class="detail-row">
              <span class="label">Inner Radius:</span>
              <span class="value">{{ config.geometry.tracker.inner_radius }} m</span>
            </div>
            <div class="detail-row">
              <span class="label">Outer Radius:</span>
              <span class="value">{{ config.geometry.tracker.outer_radius }} m</span>
            </div>
            <div class="detail-row">
              <span class="label">Length:</span>
              <span class="value">{{ config.geometry.tracker.length }} m</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>ECAL</h4>
            <div class="detail-row">
              <span class="label">Inner Radius:</span>
              <span class="value">{{ config.geometry.ecal.inner_radius }} m</span>
            </div>
            <div class="detail-row">
              <span class="label">Outer Radius:</span>
              <span class="value">{{ config.geometry.ecal.outer_radius }} m</span>
            </div>
          </div>
          
          <div class="detail-section">
            <h4>HCAL</h4>
            <div class="detail-row">
              <span class="label">Inner Radius:</span>
              <span class="value">{{ config.geometry.hcal.inner_radius }} m</span>
            </div>
            <div class="detail-row">
              <span class="label">Outer Radius:</span>
              <span class="value">{{ config.geometry.hcal.outer_radius }} m</span>
            </div>
          </div>
        </div>
        
        <div class="config-footer">
          <small>Created: {{ formatDate(config.created_at) }}</small>
        </div>
      </div>
    </div>
    
    <div v-else class="no-configs">
      <p>No detector configurations found.</p>
    </div>
    
    <div class="info-box">
      <h3>💡 Digital Twin Concept</h3>
      <p>
        The detector configuration defines the geometry and parameters of the virtual collider.
        This allows you to simulate different detector designs and compare their performance.
      </p>
      <p>
        In a production system, you could upload real detector configurations to create
        a true digital twin that mirrors your physical detector.
      </p>
    </div>
  </div>
</template>

<script>
import apiService from '../services/api.service'

export default {
  name: 'Configuration',
  
  data() {
    return {
      configs: [],
      loading: false,
      error: null
    }
  },
  
  methods: {
    async loadConfigs() {
      this.loading = true
      this.error = null
      
      try {
        this.configs = await apiService.getDetectorConfigs()
      } catch (err) {
        this.error = err.message || 'Failed to load configurations'
      } finally {
        this.loading = false
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
    }
  },
  
  mounted() {
    this.loadConfigs()
  }
}
</script>

<style scoped>
.configuration-view {
  max-width: 1400px;
  margin: 0 auto;
}

.configuration-view h2 {
  color: #667eea;
  margin-bottom: 0.5rem;
}

.subtitle {
  color: #888;
  margin-bottom: 2rem;
  font-size: 1.1rem;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.config-card {
  background: rgba(26, 26, 46, 0.5);
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s;
}

.config-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.2);
}

.config-card.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.1);
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.config-header h3 {
  margin: 0;
  color: #667eea;
  font-size: 1.3rem;
}

.active-badge {
  background: #667eea;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.config-description {
  color: #ccc;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.config-details {
  margin-bottom: 1rem;
}

.detail-section {
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 8px;
}

.detail-section h4 {
  margin: 0 0 0.75rem 0;
  color: #888;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.detail-row .label {
  color: #888;
}

.detail-row .value {
  color: #fff;
  font-weight: 500;
}

.config-footer {
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(102, 126, 234, 0.2);
  color: #666;
  font-size: 0.85rem;
}

.no-configs {
  text-align: center;
  padding: 3rem;
  color: #888;
}

.info-box {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 2px solid rgba(102, 126, 234, 0.3);
  border-radius: 12px;
  padding: 2rem;
  margin-top: 2rem;
}

.info-box h3 {
  color: #667eea;
  margin: 0 0 1rem 0;
}

.info-box p {
  color: #ccc;
  line-height: 1.7;
  margin: 0.5rem 0;
}
</style>
