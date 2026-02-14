<template>
  <div class="event-display-view">
    <div class="header">
      <h2>3D Event Display</h2>
      <div class="controls">
        <button @click="loadLatestEvent" :disabled="loading">
          {{ loading ? 'Loading...' : 'Load Latest Event' }}
        </button>
      </div>
    </div>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <EventDisplay3D
      :event="currentEvent?.event"
      :kinematics="currentEvent?.kinematics"
      :detector-config="detectorConfig"
    />
    
    <div class="event-list" v-if="events.length > 0">
      <h3>Recent Events</h3>
      <div class="event-cards">
        <div
          v-for="evt in events"
          :key="evt.event.event_id"
          class="event-card"
          :class="{ active: currentEvent?.event.event_id === evt.event.event_id }"
          @click="selectEvent(evt)"
        >
          <p><strong>{{ evt.event.event_id.substring(0, 8) }}...</strong></p>
          <p>Particles: {{ evt.event.num_particles }}</p>
          <p v-if="evt.kinematics">
            M = {{ evt.kinematics.invariant_mass?.toFixed(1) }} GeV
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import EventDisplay3D from '../components/EventDisplay3D.vue'

export default {
  name: 'EventDisplay',
  
  components: {
    EventDisplay3D
  },
  
  computed: {
    ...mapState(['currentEvent', 'events', 'detectorConfig', 'loading', 'error'])
  },
  
  methods: {
    ...mapActions(['fetchEvents', 'fetchEvent', 'fetchDetectorConfigs']),
    
    async loadLatestEvent() {
      await this.fetchEvents({ page: 1, page_size: 10 })
      if (this.events.length > 0) {
        this.selectEvent(this.events[0])
      }
    },
    
    selectEvent(evt) {
      this.$store.commit('SET_CURRENT_EVENT', evt)
    }
  },
  
  mounted() {
    this.fetchDetectorConfigs()
    this.loadLatestEvent()
  }
}
</script>

<style scoped>
.event-display-view {
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.header h2 {
  margin: 0;
  color: #667eea;
}

.controls button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: transform 0.2s;
}

.controls button:hover:not(:disabled) {
  transform: translateY(-2px);
}

.controls button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  background: rgba(255, 0, 0, 0.1);
  border-left: 4px solid #ff0000;
  padding: 1rem;
  margin-bottom: 1rem;
  border-radius: 4px;
  color: #ff6b6b;
}

.event-list {
  margin-top: 2rem;
}

.event-list h3 {
  color: #667eea;
  margin-bottom: 1rem;
}

.event-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.event-card {
  background: rgba(102, 126, 234, 0.1);
  border: 2px solid transparent;
  padding: 1rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.event-card:hover {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.2);
}

.event-card.active {
  border-color: #667eea;
  background: rgba(102, 126, 234, 0.3);
}

.event-card p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}
</style>
