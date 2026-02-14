"""API schemas using Pydantic models"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID

class ParticleData(BaseModel):
    """Particle 4-vector data"""
    pdg_id: List[int]
    px: List[float]
    py: List[float]
    pz: List[float]
    energy: List[float]
    charge: List[float]
    mass: List[float]

class EventCreate(BaseModel):
    """Event creation request"""
    event_type: str = Field(default='random', description="Type of event: 'dilepton', 'qcd', or 'random'")
    num_events: int = Field(default=1, ge=1, le=100, description="Number of events to generate")

class EventResponse(BaseModel):
    """Event response model"""
    event_id: str
    run_number: int
    event_number: int
    timestamp: str
    num_particles: int
    total_energy: Optional[float] = None
    center_of_mass_energy: float
    event_type: Optional[str] = None
    particles: Optional[ParticleData] = None

class KinematicsResponse(BaseModel):
    """Kinematics response model"""
    event_id: str
    invariant_mass: Optional[float] = None
    missing_et: Optional[float] = None
    missing_et_phi: Optional[float] = None
    scalar_ht: Optional[float] = None
    leading_jet_pt: Optional[float] = None
    leading_jet_eta: Optional[float] = None
    leading_jet_phi: Optional[float] = None
    num_jets: Optional[int] = None
    num_leptons: Optional[int] = None
    num_photons: Optional[int] = None

class EventDetailResponse(BaseModel):
    """Detailed event with kinematics"""
    event: EventResponse
    kinematics: Optional[KinematicsResponse] = None

class EventListResponse(BaseModel):
    """List of events"""
    events: List[EventDetailResponse]
    total: int
    page: int
    page_size: int

class HistogramRequest(BaseModel):
    """Histogram generation request"""
    variable: str = Field(..., description="Variable to histogram: 'invariant_mass', 'missing_et', 'leading_jet_pt', etc.")
    bins: int = Field(default=50, ge=10, le=200)
    range_min: Optional[float] = None
    range_max: Optional[float] = None
    run_numbers: Optional[List[int]] = None

class HistogramResponse(BaseModel):
    """Histogram response"""
    variable: str
    bins: List[float]
    values: List[int]
    num_events: int
    range_min: float
    range_max: float

class DetectorConfig(BaseModel):
    """Detector configuration"""
    name: str
    description: Optional[str] = None
    geometry: Dict[str, Any]
    magnetic_field: float
    trigger_thresholds: Optional[Dict[str, float]] = None

class DetectorConfigResponse(BaseModel):
    """Detector configuration response"""
    id: str
    name: str
    description: Optional[str]
    geometry: Dict[str, Any]
    magnetic_field: float
    trigger_thresholds: Optional[Dict[str, float]]
    is_active: bool
    created_at: datetime

class StatsResponse(BaseModel):
    """Statistics response"""
    total_events: int
    total_runs: int
    events_with_leptons: int
    events_with_jets: int
    average_invariant_mass: Optional[float] = None
    average_missing_et: Optional[float] = None

class GenerateResponse(BaseModel):
    """Event generation response"""
    message: str
    num_events: int
    event_ids: List[str]
