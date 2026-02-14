"""Database operations for analysis service"""
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
from typing import Dict, Any, List
import json

logger = logging.getLogger(__name__)

class DatabaseHandler:
    """Handle database operations"""
    
    def __init__(self, database_url: str):
        """Initialize database connection"""
        self.engine = create_engine(
            database_url,
            poolclass=NullPool,  # Simple connection management
            echo=False
        )
        logger.info("Database connection initialized")
    
    def store_event(self, event: Dict[str, Any], kinematics: Dict[str, Any]) -> bool:
        """
        Store event and kinematics to database
        
        Args:
            event: Original event data
            kinematics: Calculated kinematics
            
        Returns:
            Success status
        """
        try:
            with self.engine.connect() as conn:
                # Start transaction
                with conn.begin():
                    # Insert event metadata
                    event_sql = text("""
                        INSERT INTO events 
                        (event_id, run_number, event_number, timestamp, 
                         num_particles, total_energy, center_of_mass_energy)
                        VALUES 
                        (:event_id, :run_number, :event_number, :timestamp,
                         :num_particles, :total_energy, :center_of_mass_energy)
                        ON CONFLICT (event_id) DO NOTHING
                    """)
                    
                    # Calculate total energy from particles
                    particles = event.get('particles', {})
                    if isinstance(particles, dict) and 'energy' in particles:
                        total_energy = sum(particles['energy'])
                    else:
                        total_energy = 0.0
                    
                    conn.execute(event_sql, {
                        'event_id': event['event_id'],
                        'run_number': event['run_number'],
                        'event_number': event['event_number'],
                        'timestamp': event['timestamp'],
                        'num_particles': event['num_particles'],
                        'total_energy': total_energy,
                        'center_of_mass_energy': event.get('center_of_mass_energy', 13000.0)
                    })
                    
                    # Insert kinematics
                    kinematics_sql = text("""
                        INSERT INTO event_kinematics
                        (event_id, invariant_mass, missing_et, missing_et_phi,
                         scalar_ht, leading_jet_pt, leading_jet_eta, leading_jet_phi,
                         num_jets, num_leptons, num_photons)
                        VALUES
                        (:event_id, :invariant_mass, :missing_et, :missing_et_phi,
                         :scalar_ht, :leading_jet_pt, :leading_jet_eta, :leading_jet_phi,
                         :num_jets, :num_leptons, :num_photons)
                        ON CONFLICT (event_id) DO NOTHING
                    """)
                    
                    conn.execute(kinematics_sql, kinematics)
                
                logger.debug(f"Stored event {event['event_id']} to database")
                return True
                
        except Exception as e:
            logger.error(f"Failed to store event: {e}")
            return False
    
    def store_batch(self, events_with_kinematics: List[tuple]) -> int:
        """
        Store batch of events and kinematics
        
        Args:
            events_with_kinematics: List of (event, kinematics) tuples
            
        Returns:
            Number of successfully stored events
        """
        success_count = 0
        for event, kinematics in events_with_kinematics:
            if self.store_event(event, kinematics):
                success_count += 1
        
        logger.info(f"Stored {success_count}/{len(events_with_kinematics)} events to database")
        return success_count
    
    def get_event_count(self) -> int:
        """Get total number of events in database"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM events"))
                count = result.scalar()
                return count
        except Exception as e:
            logger.error(f"Failed to get event count: {e}")
            return 0
    
    def close(self):
        """Close database connection"""
        self.engine.dispose()
        logger.info("Database connection closed")
