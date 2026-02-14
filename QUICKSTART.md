# ⚡ Quick Start Guide

Get the Collider Platform running in **under 5 minutes**!

## Prerequisites

- Docker Desktop installed and running
- 8GB RAM available
- 10GB free disk space

## 🚀 Start the Platform

```bash
# Clone or extract the project
cd collider-platform

# Start everything (one command!)
./start.sh
```

**That's it!** The script will:
1. Check Docker is installed
2. Clean up any old containers
3. Start all services
4. Wait for everything to be ready
5. Show you the access URLs

## 🎯 Access the Platform

Once the start script completes (30-60 seconds):

### Frontend UI
Open in your browser: **http://localhost:8080**

### API Documentation
Interactive API docs: **http://localhost:8000/docs**

## 🎮 First Steps

### 1. View Events (Event Display Tab)
- Click "Load Latest Event"
- Interact with 3D visualization:
  - **Rotate**: Click and drag
  - **Zoom**: Scroll wheel
  - **Pan**: Right-click and drag
- Click different events in the list below

### 2. Analyze Data (Analysis Tab)
- View statistics cards
- Select a variable (e.g., "Invariant Mass")
- Click "Generate" to create histogram
- Try different variables

### 3. Check Configuration (Configuration Tab)
- View detector geometry
- See magnetic field settings
- Understand the digital twin concept

## 📊 Verify It's Working

Check event generation:
```bash
# Should show increasing event count
docker-compose exec postgres psql -U physics -d collider_db \
  -c "SELECT COUNT(*) as total_events FROM events;"
```

Check services are running:
```bash
docker-compose ps
# All services should be "Up"
```

View logs:
```bash
docker-compose logs -f collision-service
# You should see "Sent X/Y events to collision-events"
```

## 🛠️ Useful Commands

```bash
# Stop everything
docker-compose down

# Restart everything
docker-compose restart

# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api-gateway

# Rebuild after code changes
docker-compose up -d --build

# Clean restart (removes data)
docker-compose down -v
./start.sh
```

## 🐛 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# Clean restart
docker-compose down -v
./start.sh
```

### No events in UI
```bash
# Wait 30 seconds for services to sync
# Then check database
docker-compose exec postgres psql -U physics -d collider_db \
  -c "SELECT COUNT(*) FROM events;"

# If 0, check collision service
docker-compose logs collision-service
```

### Port already in use
```bash
# Stop conflicting service or change ports in docker-compose.yml
# Default ports: 8080 (frontend), 8000 (API), 5432 (postgres)
```

## 🎯 What Next?

Once everything is running:

1. **Experiment**: Try different physics variables in the analysis dashboard
2. **Modify**: Edit code in any service and restart that service
3. **Extend**: Add new features or physics calculations
4. **Learn**: Check the full README.md for architecture details

## 📚 Documentation

- **Full Documentation**: See README.md
- **API Reference**: http://localhost:8000/docs
- **Contributing**: See CONTRIBUTING.md

## 💬 Need Help?

1. Check the logs: `docker-compose logs -f`
2. Verify services: `docker-compose ps`
3. Check README.md troubleshooting section
4. Open an issue on GitHub

---

**Ready to explore particle physics? Go to http://localhost:8080** 🚀⚛️
