"""
FastAPI Gateway for Collider Platform
Main API application
"""
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import json
from typing import List, Optional
import asyncio

from config import settings
from schemas import (
    EventCreate, EventResponse, EventDetailResponse, EventListResponse,
    HistogramRequest, HistogramResponse, DetectorConfig, DetectorConfigResponse,
    StatsResponse, GenerateResponse, KinematicsResponse
)
from database_service import DatabaseService

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API for particle collision visualization and analysis platform"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database service
db_service = DatabaseService(
    settings.DATABASE_URL,
    settings.REDIS_HOST,
    settings.REDIS_PORT
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "api-gateway"}

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Collider Platform API",
        "version": settings.API_VERSION,
        "docs": "/docs"
    }

# Events endpoints
@app.post(f"{settings.API_PREFIX}/collisions/generate", response_model=GenerateResponse)
async def generate_events(request: EventCreate):
    """
    Trigger collision event generation
    
    This endpoint triggers the collision service to generate events.
    In a real system, this would send a message to Kafka.
    For the hackathon MVP, we'll return a placeholder response.
    """
    logger.info(f"Generating {request.num_events} events of type {request.event_type}")
    
    # For hackathon: The collision service continuously generates events
    # This endpoint could be enhanced to trigger on-demand generation
    
    return GenerateResponse(
        message=f"Event generation triggered (collision service generates continuously)",
        num_events=request.num_events,
        event_ids=[]
    )

@app.get(f"{settings.API_PREFIX}/events/{{event_id}}", response_model=EventDetailResponse)
async def get_event(event_id: str):
    """Get specific event by ID"""
    event_data = db_service.get_event(event_id)
    
    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Split into event and kinematics
    event = {
        'event_id': str(event_data['event_id']),
        'run_number': event_data['run_number'],
        'event_number': event_data['event_number'],
        'timestamp': event_data['timestamp'].isoformat(),
        'num_particles': event_data['num_particles'],
        'total_energy': event_data.get('total_energy'),
        'center_of_mass_energy': event_data.get('center_of_mass_energy', 13000.0)
    }
    
    kinematics = {
        'event_id': str(event_data['event_id']),
        'invariant_mass': event_data.get('invariant_mass'),
        'missing_et': event_data.get('missing_et'),
        'missing_et_phi': event_data.get('missing_et_phi'),
        'scalar_ht': event_data.get('scalar_ht'),
        'leading_jet_pt': event_data.get('leading_jet_pt'),
        'leading_jet_eta': event_data.get('leading_jet_eta'),
        'leading_jet_phi': event_data.get('leading_jet_phi'),
        'num_jets': event_data.get('num_jets'),
        'num_leptons': event_data.get('num_leptons'),
        'num_photons': event_data.get('num_photons')
    }
    
    return EventDetailResponse(
        event=EventResponse(**event),
        kinematics=KinematicsResponse(**kinematics) if kinematics['invariant_mass'] else None
    )

@app.get(f"{settings.API_PREFIX}/events", response_model=EventListResponse)
async def get_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    min_invariant_mass: Optional[float] = None,
    min_jets: Optional[int] = None,
    run_number: Optional[int] = None
):
    """Get list of events with pagination and filters"""
    offset = (page - 1) * page_size
    
    filters = {}
    if min_invariant_mass:
        filters['min_invariant_mass'] = min_invariant_mass
    if min_jets is not None:
        filters['min_jets'] = min_jets
    if run_number:
        filters['run_number'] = run_number
    
    events_data = db_service.get_events(page_size, offset, filters)
    total = db_service.get_event_count(filters)
    
    events = []
    for event_data in events_data:
        event = {
            'event_id': str(event_data['event_id']),
            'run_number': event_data['run_number'],
            'event_number': event_data['event_number'],
            'timestamp': event_data['timestamp'].isoformat(),
            'num_particles': event_data['num_particles'],
            'total_energy': event_data.get('total_energy'),
            'center_of_mass_energy': event_data.get('center_of_mass_energy', 13000.0)
        }
        
        kinematics = None
        if event_data.get('invariant_mass') is not None:
            kinematics = {
                'event_id': str(event_data['event_id']),
                'invariant_mass': event_data.get('invariant_mass'),
                'missing_et': event_data.get('missing_et'),
                'missing_et_phi': event_data.get('missing_et_phi'),
                'scalar_ht': event_data.get('scalar_ht'),
                'leading_jet_pt': event_data.get('leading_jet_pt'),
                'leading_jet_eta': event_data.get('leading_jet_eta'),
                'leading_jet_phi': event_data.get('leading_jet_phi'),
                'num_jets': event_data.get('num_jets'),
                'num_leptons': event_data.get('num_leptons'),
                'num_photons': event_data.get('num_photons')
            }
        
        events.append(EventDetailResponse(
            event=EventResponse(**event),
            kinematics=KinematicsResponse(**kinematics) if kinematics else None
        ))
    
    return EventListResponse(
        events=events,
        total=total,
        page=page,
        page_size=page_size
    )

# Analysis endpoints
@app.post(f"{settings.API_PREFIX}/analysis/histogram", response_model=HistogramResponse)
async def generate_histogram(request: HistogramRequest):
    """Generate histogram for a physics variable"""
    histogram = db_service.get_histogram_data(
        request.variable,
        request.bins,
        request.range_min,
        request.range_max
    )
    
    if not histogram:
        raise HTTPException(status_code=404, detail="No data available for histogram")
    
    return HistogramResponse(**histogram)

@app.get(f"{settings.API_PREFIX}/statistics/summary", response_model=StatsResponse)
async def get_statistics():
    """Get overall statistics"""
    stats = db_service.get_statistics()
    
    if not stats:
        return StatsResponse(
            total_events=0,
            total_runs=0,
            events_with_leptons=0,
            events_with_jets=0
        )
    
    return StatsResponse(
        total_events=stats.get('total_events', 0),
        total_runs=stats.get('total_runs', 0),
        events_with_leptons=stats.get('events_with_leptons', 0),
        events_with_jets=stats.get('events_with_jets', 0),
        average_invariant_mass=stats.get('avg_invariant_mass'),
        average_missing_et=stats.get('avg_missing_et')
    )

# Configuration endpoints
@app.get(f"{settings.API_PREFIX}/config/detector", response_model=List[DetectorConfigResponse])
async def get_detector_configs():
    """Get all detector configurations"""
    configs = db_service.get_detector_configs()
    
    response = []
    for config in configs:
        response.append(DetectorConfigResponse(
            id=str(config['id']),
            name=config['name'],
            description=config.get('description'),
            geometry=config['geometry'],
            magnetic_field=config['magnetic_field'],
            trigger_thresholds=config.get('trigger_thresholds'),
            is_active=config['is_active'],
            created_at=config['created_at']
        ))
    
    return response

# WebSocket endpoint for live events
@app.websocket("/ws/live-events")
async def websocket_live_events(websocket: WebSocket):
    """WebSocket endpoint for streaming live events"""
    await manager.connect(websocket)
    
    try:
        # Send initial connection message
        await websocket.send_text(json.dumps({
            "type": "connected",
            "message": "Connected to live event stream"
        }))
        
        # Keep connection alive and send periodic updates
        while True:
            # In a real implementation, this would listen to Kafka
            # For demo, send periodic statistics
            await asyncio.sleep(5)
            
            stats = db_service.get_statistics()
            await websocket.send_text(json.dumps({
                "type": "stats_update",
                "data": stats
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
