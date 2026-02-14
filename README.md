# Collider Platform - Particle Collision Visualization & Analysis

A digital twin platform for visualizing and analyzing particle collision events, similar to real-world colliders like the LHC.

## 🚀 Features

- **3D Event Display**: Interactive Three.js visualization of particle tracks and detector geometry
- **Physics Analysis**: Calculate and visualize kinematic quantities (invariant mass, missing ET, jets)
- **Real-time Processing**: Kafka-based event streaming and processing pipeline
- **Digital Twin**: Configurable detector geometry to mirror real collider setups
- **Analytics Dashboard**: Histogram generation and statistical analysis
- **Scalable Architecture**: Microservices-based design ready for production deployment

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Vue.js + Three.js                        │
│              (Event Display & Analytics Dashboard)           │
└────────────────────┬────────────────────────────────────────┘
                     │ WebSocket + REST API
┌────────────────────▼────────────────────────────────────────┐
│                   FastAPI Gateway                            │
└─────┬──────────────┬──────────────┬────────────────────┬────┘
      │              │               │                    │
┌─────▼─────┐  ┌────▼─────┐  ┌──────▼──────┐  ┌─────────▼──────┐
│ Collision │  │ Analysis │  │   Config    │  │   Real-time    │
│  Service  │  │ Service  │  │   Service   │  │   Streaming    │
└─────┬──────┘  └────┬─────┘  └──────┬──────┘  └─────────┬──────┘
      │              │               │                    │
      ▼              ▼               ▼                    ▼
┌─────────────────────────────────────────────────────────────┐
│                      Kafka Cluster                           │
└────────────────────┬────────────────────────────────────────┘
                     │
      ┌──────────────┼──────────────┐
      ▼              ▼               ▼
┌──────────┐  ┌──────────┐  ┌────────────────┐
│PostgreSQL│  │  Redis   │  │ Object Storage │
└──────────┘  └──────────┘  └────────────────┘
```

## 🛠️ Tech Stack

### Backend
- **Python FastAPI** - REST API gateway
- **Apache Kafka** - Event streaming
- **PostgreSQL** - Event metadata and kinematics storage
- **Redis** - Caching and real-time data
- **Awkward Arrays** - HEP-optimized data structures

### Frontend
- **Vue.js 3** - Progressive web framework
- **Three.js** - 3D visualization
- **Chart.js** - Statistical plots
- **Axios** - HTTP client

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Development orchestration
- **Kubernetes-ready** - Production deployment

## 📋 Prerequisites

- Docker and Docker Compose
- 8GB RAM minimum
- 10GB free disk space

## 🚀 Quick Start

### 1. Clone and Start Services

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Check service health
docker-compose ps
```

### 2. Wait for Services to Initialize

Services will be ready when you see:
- Kafka: "Kafka Server started"
- PostgreSQL: "database system is ready to accept connections"
- API Gateway: "Uvicorn running on http://0.0.0.0:8000"

This typically takes 30-60 seconds.

### 3. Access the Platform

- **Frontend**: http://localhost:8080
- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api/v1

## 📊 Usage

### Event Display

1. Navigate to the Event Display view
2. Click "Load Latest Event" to fetch recent collision events
3. Interact with the 3D visualization:
   - **Rotate**: Left click + drag
   - **Zoom**: Scroll wheel
   - **Pan**: Right click + drag
4. Click on events in the list to view different collisions

### Analysis Dashboard

1. Navigate to the Analysis view
2. Select a physics variable from the dropdown
3. Adjust number of bins if needed
4. Click "Generate" to create histogram
5. View statistics cards for overall event summary

### Configuration

1. Navigate to Configuration view
2. View current detector configuration
3. See geometry parameters for tracker, ECAL, and HCAL
4. Digital twin ready for importing real detector configs

## 🔧 Development

### Project Structure

```
collider-platform/
├── collision_service/      # Event generation service
│   ├── generator.py        # Physics event generator
│   ├── kafka_producer.py   # Kafka publisher
│   └── main.py            # Service entry point
│
├── analysis_service/       # Event analysis service
│   ├── processor.py        # Physics calculations
│   ├── database.py         # PostgreSQL operations
│   ├── cache.py           # Redis operations
│   └── main.py            # Service entry point
│
├── api_gateway/           # FastAPI REST API
│   ├── main.py            # FastAPI application
│   ├── schemas.py         # Pydantic models
│   ├── database_service.py # Database queries
│   └── config.py          # Configuration
│
├── frontend/              # Vue.js application
│   ├── src/
│   │   ├── components/    # Vue components
│   │   │   └── EventDisplay3D.vue
│   │   ├── views/         # Page views
│   │   │   ├── EventDisplay.vue
│   │   │   ├── AnalysisDashboard.vue
│   │   │   └── Configuration.vue
│   │   ├── services/      # API clients
│   │   └── store/         # Vuex state
│   └── public/
│
├── scripts/               # Database initialization
│   └── init_db.sql
│
└── docker-compose.yml     # Service orchestration
```

### Service Ports

- Frontend: 8080
- API Gateway: 8000
- PostgreSQL: 5432
- Redis: 6379
- Kafka: 9092
- Zookeeper: 2181

### Environment Variables

Create `.env` file in service directories:

```bash
# API Gateway
POSTGRES_HOST=postgres
POSTGRES_DB=collider_db
POSTGRES_USER=physics
POSTGRES_PASSWORD=quantum2024
REDIS_HOST=redis
KAFKA_BOOTSTRAP_SERVERS=kafka:29092

# Collision Service
EVENTS_PER_BATCH=10
BATCH_INTERVAL_SECONDS=5.0
CENTER_OF_MASS_ENERGY=13000.0
```

### Running Individual Services

```bash
# API Gateway only
cd api_gateway
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend only
cd frontend
npm install
npm run serve
```

## 🧪 API Examples

### Get Events

```bash
curl http://localhost:8000/api/v1/events?page=1&page_size=10
```

### Get Specific Event

```bash
curl http://localhost:8000/api/v1/events/{event_id}
```

### Generate Histogram

```bash
curl -X POST http://localhost:8000/api/v1/analysis/histogram \
  -H "Content-Type: application/json" \
  -d '{
    "variable": "invariant_mass",
    "bins": 50
  }'
```

### Get Statistics

```bash
curl http://localhost:8000/api/v1/statistics/summary
```

## 🎯 Physics Features

### Event Generation

The collision service generates two types of events:

1. **Dilepton Events** (e⁺e⁻ → μ⁺μ⁻)
   - Simulates Z boson production and decay
   - Clean signature for testing

2. **QCD Multi-jet Events**
   - Multiple jets from quark production
   - Realistic hadronic events

### Calculated Quantities

- **Invariant Mass**: M² = (ΣE)² - (Σp)²
- **Transverse Momentum**: pT = √(px² + py²)
- **Pseudorapidity**: η = -ln(tan(θ/2))
- **Missing ET**: Momentum imbalance
- **Scalar HT**: Sum of transverse momenta

### Detector Simulation

- **Tracker**: Inner silicon tracking layers
- **ECAL**: Electromagnetic calorimeter
- **HCAL**: Hadronic calorimeter
- **Magnetic Field**: 2.0 Tesla (configurable)

## 🔍 Troubleshooting

### Services won't start

```bash
# Clean restart
docker-compose down -v
docker-compose up -d
```

### Database connection errors

```bash
# Check PostgreSQL is ready
docker-compose logs postgres | grep "ready to accept"

# Manually initialize database
docker-compose exec postgres psql -U physics -d collider_db -f /docker-entrypoint-initdb.d/init_db.sql
```

### No events appearing

```bash
# Check collision service is generating
docker-compose logs collision-service

# Check analysis service is consuming
docker-compose logs analysis-service

# Verify Kafka is working
docker-compose exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Frontend connection issues

```bash
# Check API is accessible
curl http://localhost:8000/health

# Rebuild frontend
docker-compose up -d --build frontend
```

## 📈 Performance Tuning

### Event Generation Rate

Edit `docker-compose.yml`:

```yaml
collision-service:
  environment:
    EVENTS_PER_BATCH: "50"      # Increase batch size
    BATCH_INTERVAL_SECONDS: "2.0"  # Faster generation
```

### Database Performance

For higher throughput, increase connection pool:

```python
# api_gateway/database_service.py
self.engine = create_engine(
    database_url,
    pool_size=20,        # Increase from 5
    max_overflow=40      # Increase from 10
)
```

## 🚢 Production Deployment

### Kubernetes

Convert to Kubernetes manifests:

```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-linux-amd64 -o kompose
chmod +x kompose
sudo mv kompose /usr/local/bin/

# Convert docker-compose to k8s
kompose convert
```

### Security Hardening

1. Use secrets management (Vault, K8s Secrets)
2. Enable TLS/SSL for all services
3. Implement authentication (JWT, OAuth)
4. Network policies for service isolation
5. Resource limits and quotas

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 🎓 Educational Use

This platform is designed for:
- Physics education and demonstrations
- Hackathons and coding challenges
- Learning distributed systems architecture
- Experimenting with data visualization
- Understanding HEP data analysis workflows

## 📚 References

- [CERN Open Data Portal](http://opendata.cern.ch/)
- [Particle Data Group](https://pdg.lbl.gov/)
- [ROOT Analysis Framework](https://root.cern/)
- [Awkward Array Documentation](https://awkward-array.org/)

## 💬 Support

For questions and discussions:
- Open an issue on GitHub
- Tag with appropriate labels (bug, enhancement, question)
- Provide logs and system information for bugs

---

**Built for Hackathon** | **Physics Meets Software Engineering** 🚀⚛️
