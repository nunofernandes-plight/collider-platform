"""Configuration for collision service"""
import os
from typing import Dict, Any

class Config:
    """Service configuration"""
    
    # Kafka settings
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_COLLISION_EVENTS = 'collision-events'
    KAFKA_TOPIC_DETECTOR_CONFIG = 'detector-config'
    
    # Generation settings
    EVENTS_PER_BATCH = int(os.getenv('EVENTS_PER_BATCH', '10'))
    BATCH_INTERVAL_SECONDS = float(os.getenv('BATCH_INTERVAL_SECONDS', '5.0'))
    CENTER_OF_MASS_ENERGY = 13000.0  # GeV (LHC energy)
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def get_default_detector_config() -> Dict[str, Any]:
        """Default detector configuration"""
        return {
            'magnetic_field': 2.0,  # Tesla
            'geometry': {
                'tracker': {
                    'inner_radius': 0.04,  # meters
                    'outer_radius': 1.2,
                    'length': 5.0,
                    'layers': 8
                },
                'ecal': {
                    'inner_radius': 1.3,
                    'outer_radius': 1.8,
                    'length': 6.0,
                    'granularity': 0.025
                },
                'hcal': {
                    'inner_radius': 1.9,
                    'outer_radius': 3.0,
                    'length': 7.0,
                    'granularity': 0.1
                }
            }
        }
