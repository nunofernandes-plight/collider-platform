<template>
  <div class="analysis-dashboard">
    <h2>Analysis Dashboard</h2>
    
    <div class="stats-grid" v-if="statistics">
      <div class="stat-card">
        <h3>{{ statistics.total_events }}</h3>
        <p>Total Events</p>
      </div>
      <div class="stat-card">
        <h3>{{ statistics.events_with_leptons }}</h3>
        <p>Events with Leptons</p>
      </div>
      <div class="stat-card">
        <h3>{{ statistics.events_with_jets }}</h3>
        <p>Events with Jets</p>
      </div>
      <div class="stat-card">
        <h3>{{ statistics.average_invariant_mass?.toFixed(1) || 'N/A' }}</h3>
        <p>Avg. Invariant Mass (GeV)</p>
      </div>
    </div>
    
    <div class="histogram-section">
      <h3>Generate Histogram</h3>
      <div class="histogram-controls">
        <select v-model="selectedVariable">
          <option value="invariant_mass">Invariant Mass</option>
          <option value="missing_et">Missing ET</option>
          <option value="leading_jet_pt">Leading Jet pT</option>
          <option value="scalar_ht">Scalar HT</option>
        </select>
        <input
          type="number"
          v-model.number="numBins"
          min="10"
          max="200"
          placeholder="Bins"
        />
        <button @click="generateHistogram" :disabled="loading">
          {{ loading ? 'Loading...' : 'Generate' }}
        </button>
      </div>
      
      <div v-if="histogramData" class="histogram-display">
        <canvas ref="histogramCanvas"></canvas>
      </div>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import apiService from '../services/api.service'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

export default {
  name: 'AnalysisDashboard',
  
  data() {
    return {
      selectedVariable: 'invariant_mass',
      numBins: 50,
      histogramData: null,
      chart: null,
      loading: false,
      error: null
    }
  },
  
  computed: {
    ...mapState(['statistics'])
  },
  
  methods: {
    ...mapActions(['fetchStatistics']),
    
    async generateHistogram() {
      this.loading = true
      this.error = null
      
      try {
        this.histogramData = await apiService.getHistogram(
          this.selectedVariable,
          this.numBins
        )
        this.renderHistogram()
      } catch (err) {
        this.error = err.message || 'Failed to generate histogram'
      } finally {
        this.loading = false
      }
    },
    
    renderHistogram() {
      if (this.chart) {
        this.chart.destroy()
      }
      
      if (!this.histogramData || !this.$refs.histogramCanvas) return
      
      const ctx = this.$refs.histogramCanvas.getContext('2d')
      
      // Calculate bin centers for x-axis
      const bins = this.histogramData.bins
      const binCenters = []
      for (let i = 0; i < bins.length - 1; i++) {
        binCenters.push((bins[i] + bins[i + 1]) / 2)
      }
      
      this.chart = new Chart(ctx, {
        type: 'bar',
        data: {
          labels: binCenters.map(x => x.toFixed(1)),
          datasets: [{
            label: this.getVariableLabel(this.selectedVariable),
            data: this.histogramData.values,
            backgroundColor: 'rgba(102, 126, 234, 0.6)',
            borderColor: 'rgba(102, 126, 234, 1)',
            borderWidth: 1
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'Events',
                color: '#fff'
              },
              ticks: { color: '#fff' },
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            },
            x: {
              title: {
                display: true,
                text: `${this.getVariableLabel(this.selectedVariable)} (GeV)`,
                color: '#fff'
              },
              ticks: { color: '#fff', maxRotation: 45 },
              grid: { color: 'rgba(255, 255, 255, 0.1)' }
            }
          },
          plugins: {
            legend: {
              labels: { color: '#fff' }
            },
            title: {
              display: true,
              text: `${this.getVariableLabel(this.selectedVariable)} Distribution (${this.histogramData.num_events} events)`,
              color: '#fff',
              font: { size: 16 }
            }
          }
        }
      })
    },
    
    getVariableLabel(variable) {
      const labels = {
        'invariant_mass': 'Invariant Mass',
        'missing_et': 'Missing ET',
        'leading_jet_pt': 'Leading Jet pT',
        'scalar_ht': 'Scalar HT'
      }
      return labels[variable] || variable
    }
  },
  
  mounted() {
    this.fetchStatistics()
    // Auto-generate default histogram
    this.$nextTick(() => {
      setTimeout(() => this.generateHistogram(), 1000)
    })
  },
  
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.analysis-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.analysis-dashboard h2 {
  color: #667eea;
  margin-bottom: 2rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-card {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%);
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  border: 2px solid rgba(102, 126, 234, 0.3);
}

.stat-card h3 {
  margin: 0;
  font-size: 2.5rem;
  color: #667eea;
  font-weight: 700;
}

.stat-card p {
  margin: 0.5rem 0 0 0;
  color: #ccc;
  font-size: 0.9rem;
}

.histogram-section {
  background: rgba(26, 26, 46, 0.5);
  padding: 2rem;
  border-radius: 12px;
}

.histogram-section h3 {
  color: #667eea;
  margin: 0 0 1rem 0;
}

.histogram-controls {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.histogram-controls select,
.histogram-controls input {
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid rgba(102, 126, 234, 0.3);
  color: white;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 1rem;
}

.histogram-controls select {
  flex: 1;
  min-width: 200px;
}

.histogram-controls input {
  width: 100px;
}

.histogram-controls button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: transform 0.2s;
}

.histogram-controls button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.histogram-controls button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.histogram-display {
  background: rgba(0, 0, 0, 0.3);
  padding: 2rem;
  border-radius: 8px;
  height: 500px;
}

.histogram-display canvas {
  max-height: 100%;
}

.error-message {
  background: rgba(255, 0, 0, 0.1);
  border-left: 4px solid #ff0000;
  padding: 1rem;
  margin-top: 1rem;
  border-radius: 4px;
  color: #ff6b6b;
}
</style>
