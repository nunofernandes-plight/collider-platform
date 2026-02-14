<template>
  <div class="event-display-3d">
    <div ref="canvasContainer" class="canvas-container"></div>
    
    <div class="controls-overlay">
      <div class="info-panel">
        <h3>Event Information</h3>
        <div v-if="event">
          <p><strong>Event ID:</strong> {{ event.event_id.substring(0, 8) }}...</p>
          <p><strong>Particles:</strong> {{ event.num_particles }}</p>
          <p v-if="kinematics">
            <strong>Invariant Mass:</strong> {{ kinematics.invariant_mass?.toFixed(2) }} GeV
          </p>
          <p v-if="kinematics">
            <strong>Jets:</strong> {{ kinematics.num_jets || 0 }}
          </p>
          <p v-if="kinematics">
            <strong>Leptons:</strong> {{ kinematics.num_leptons || 0 }}
          </p>
        </div>
        <p v-else class="no-event">No event loaded</p>
      </div>
      
      <div class="view-controls">
        <button @click="resetCamera">Reset View</button>
        <button @click="toggleDetector">{{ showDetector ? 'Hide' : 'Show' }} Detector</button>
      </div>
    </div>
  </div>
</template>

<script>
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'

export default {
  name: 'EventDisplay3D',
  
  props: {
    event: {
      type: Object,
      default: null
    },
    kinematics: {
      type: Object,
      default: null
    },
    detectorConfig: {
      type: Object,
      default: null
    }
  },
  
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      controls: null,
      showDetector: true,
      detectorMeshes: [],
      particleMeshes: []
    }
  },
  
  mounted() {
    this.initThreeJS()
    this.createDetectorGeometry()
    if (this.event) {
      this.renderEvent()
    }
    this.animate()
  },
  
  beforeUnmount() {
    if (this.renderer) {
      this.renderer.dispose()
    }
    if (this.controls) {
      this.controls.dispose()
    }
  },
  
  watch: {
    event() {
      this.renderEvent()
    }
  },
  
  methods: {
    initThreeJS() {
      // Scene
      this.scene = new THREE.Scene()
      this.scene.background = new THREE.Color(0x0a0e27)
      
      // Camera
      this.camera = new THREE.PerspectiveCamera(
        75,
        this.$refs.canvasContainer.clientWidth / this.$refs.canvasContainer.clientHeight,
        0.1,
        1000
      )
      this.camera.position.set(5, 5, 5)
      this.camera.lookAt(0, 0, 0)
      
      // Renderer
      this.renderer = new THREE.WebGLRenderer({ antialias: true })
      this.renderer.setSize(
        this.$refs.canvasContainer.clientWidth,
        this.$refs.canvasContainer.clientHeight
      )
      this.$refs.canvasContainer.appendChild(this.renderer.domElement)
      
      // Controls
      this.controls = new OrbitControls(this.camera, this.renderer.domElement)
      this.controls.enableDamping = true
      this.controls.dampingFactor = 0.05
      
      // Lights
      const ambientLight = new THREE.AmbientLight(0xffffff, 0.5)
      this.scene.add(ambientLight)
      
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8)
      directionalLight.position.set(5, 10, 7.5)
      this.scene.add(directionalLight)
      
      // Grid
      const gridHelper = new THREE.GridHelper(10, 20, 0x444444, 0x222222)
      this.scene.add(gridHelper)
      
      // Axes
      const axesHelper = new THREE.AxesHelper(5)
      this.scene.add(axesHelper)
      
      // Handle window resize
      window.addEventListener('resize', this.onWindowResize)
    },
    
    createDetectorGeometry() {
      // Clear existing detector meshes
      this.detectorMeshes.forEach(mesh => this.scene.remove(mesh))
      this.detectorMeshes = []
      
      const config = this.detectorConfig || {
        geometry: {
          tracker: { inner_radius: 0.04, outer_radius: 1.2, length: 5.0 },
          ecal: { inner_radius: 1.3, outer_radius: 1.8, length: 6.0 },
          hcal: { inner_radius: 1.9, outer_radius: 3.0, length: 7.0 }
        }
      }
      
      // Tracker (inner cylinder)
      const trackerGeom = new THREE.CylinderGeometry(
        config.geometry.tracker.outer_radius,
        config.geometry.tracker.outer_radius,
        config.geometry.tracker.length,
        32,
        1,
        true
      )
      const trackerMat = new THREE.MeshPhongMaterial({
        color: 0x4488ff,
        transparent: true,
        opacity: 0.2,
        side: THREE.DoubleSide
      })
      const tracker = new THREE.Mesh(trackerGeom, trackerMat)
      tracker.rotation.x = Math.PI / 2
      this.scene.add(tracker)
      this.detectorMeshes.push(tracker)
      
      // ECAL (electromagnetic calorimeter)
      const ecalGeom = new THREE.CylinderGeometry(
        config.geometry.ecal.outer_radius,
        config.geometry.ecal.outer_radius,
        config.geometry.ecal.length,
        32,
        1,
        true
      )
      const ecalMat = new THREE.MeshPhongMaterial({
        color: 0x44ff88,
        transparent: true,
        opacity: 0.15,
        side: THREE.DoubleSide
      })
      const ecal = new THREE.Mesh(ecalGeom, ecalMat)
      ecal.rotation.x = Math.PI / 2
      this.scene.add(ecal)
      this.detectorMeshes.push(ecal)
      
      // HCAL (hadronic calorimeter)
      const hcalGeom = new THREE.CylinderGeometry(
        config.geometry.hcal.outer_radius,
        config.geometry.hcal.outer_radius,
        config.geometry.hcal.length,
        32,
        1,
        true
      )
      const hcalMat = new THREE.MeshPhongMaterial({
        color: 0xff8844,
        transparent: true,
        opacity: 0.1,
        side: THREE.DoubleSide
      })
      const hcal = new THREE.Mesh(hcalGeom, hcalMat)
      hcal.rotation.x = Math.PI / 2
      this.scene.add(hcal)
      this.detectorMeshes.push(hcal)
    },
    
    renderEvent() {
      // Clear existing particles
      this.particleMeshes.forEach(mesh => this.scene.remove(mesh))
      this.particleMeshes = []
      
      if (!this.event || !this.event.particles) return
      
      const particles = this.event.particles
      
      for (let i = 0; i < particles.px.length; i++) {
        const px = particles.px[i]
        const py = particles.py[i]
        const pz = particles.pz[i]
        const pdgId = Math.abs(particles.pdg_id[i])
        
        // Calculate track parameters
        const pt = Math.sqrt(px * px + py * py)
        const p = Math.sqrt(px * px + py * py + pz * pz)
        const phi = Math.atan2(py, px)
        
        // Create particle track
        const points = []
        const numPoints = 50
        const maxR = 3.0  // Maximum radius
        
        for (let j = 0; j <= numPoints; j++) {
          const t = j / numPoints
          const r = t * Math.min(pt / 20, maxR)
          const x = r * Math.cos(phi)
          const y = r * Math.sin(phi)
          const z = t * pz / 10  // Scale z component
          points.push(new THREE.Vector3(x, z, y))  // Y and Z swapped for display
        }
        
        const trackGeometry = new THREE.BufferGeometry().setFromPoints(points)
        
        // Color by particle type
        let color
        if (pdgId === 11) color = 0xff0000      // Electron - red
        else if (pdgId === 13) color = 0x00ff00  // Muon - green
        else if (pdgId === 22) color = 0xffff00  // Photon - yellow
        else color = 0x00ffff                    // Other - cyan
        
        const trackMaterial = new THREE.LineBasicMaterial({
          color: color,
          linewidth: 2
        })
        
        const track = new THREE.Line(trackGeometry, trackMaterial)
        this.scene.add(track)
        this.particleMeshes.push(track)
        
        // Add particle marker at origin
        const markerGeom = new THREE.SphereGeometry(0.05, 8, 8)
        const markerMat = new THREE.MeshBasicMaterial({ color: color })
        const marker = new THREE.Mesh(markerGeom, markerMat)
        this.scene.add(marker)
        this.particleMeshes.push(marker)
      }
    },
    
    resetCamera() {
      this.camera.position.set(5, 5, 5)
      this.camera.lookAt(0, 0, 0)
      this.controls.reset()
    },
    
    toggleDetector() {
      this.showDetector = !this.showDetector
      this.detectorMeshes.forEach(mesh => {
        mesh.visible = this.showDetector
      })
    },
    
    animate() {
      requestAnimationFrame(this.animate)
      this.controls.update()
      this.renderer.render(this.scene, this.camera)
    },
    
    onWindowResize() {
      if (!this.$refs.canvasContainer) return
      
      this.camera.aspect = this.$refs.canvasContainer.clientWidth / this.$refs.canvasContainer.clientHeight
      this.camera.updateProjectionMatrix()
      this.renderer.setSize(
        this.$refs.canvasContainer.clientWidth,
        this.$refs.canvasContainer.clientHeight
      )
    }
  }
}
</script>

<style scoped>
.event-display-3d {
  position: relative;
  width: 100%;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.canvas-container {
  width: 100%;
  height: 100%;
}

.controls-overlay {
  position: absolute;
  top: 1rem;
  left: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-panel {
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  padding: 1rem;
  border-radius: 8px;
  min-width: 250px;
}

.info-panel h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #667eea;
}

.info-panel p {
  margin: 0.25rem 0;
  font-size: 0.9rem;
}

.no-event {
  color: #888;
  font-style: italic;
}

.view-controls {
  display: flex;
  gap: 0.5rem;
}

.view-controls button {
  background: rgba(102, 126, 234, 0.8);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.3s;
}

.view-controls button:hover {
  background: rgba(102, 126, 234, 1);
}
</style>
