"""Kafka producer for collision events"""
import json
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError
import awkward as ak
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CollisionEventProducer:
    """Produces collision events to Kafka"""
    
    def __init__(self, bootstrap_servers: str, topic: str):
        """
        Initialize Kafka producer
        
        Args:
            bootstrap_servers: Kafka bootstrap servers
            topic: Topic to publish to
        """
        self.topic = topic
        self.producer = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',  # Wait for all replicas
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        logger.info(f"Kafka producer initialized for topic: {topic}")
    
    def send_event(self, event: Dict[str, Any]) -> bool:
        """
        Send a single event to Kafka
        
        Args:
            event: Event dictionary
            
        Returns:
            Success status
        """
        try:
            # Convert Awkward Array to serializable format
            serializable_event = self._prepare_event(event)
            
            # Send to Kafka
            future = self.producer.send(
                self.topic,
                key=serializable_event['event_id'],
                value=serializable_event
            )
            
            # Wait for confirmation (synchronous for demo)
            record_metadata = future.get(timeout=10)
            
            logger.debug(
                f"Event {event['event_id']} sent to "
                f"{record_metadata.topic}:{record_metadata.partition}:{record_metadata.offset}"
            )
            return True
            
        except KafkaError as e:
            logger.error(f"Failed to send event: {e}")
            return False
    
    def send_batch(self, events: list) -> int:
        """
        Send a batch of events
        
        Args:
            events: List of event dictionaries
            
        Returns:
            Number of successfully sent events
        """
        success_count = 0
        for event in events:
            if self.send_event(event):
                success_count += 1
        
        self.producer.flush()
        logger.info(f"Sent {success_count}/{len(events)} events to {self.topic}")
        return success_count
    
    def _prepare_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare event for serialization
        Convert Awkward Arrays to lists
        """
        serializable = event.copy()
        
        # Convert particles Awkward Array to dict of lists
        if 'particles' in event and isinstance(event['particles'], ak.Array):
            particles = event['particles']
            serializable['particles'] = {
                'pdg_id': ak.to_list(particles.pdg_id),
                'px': ak.to_list(particles.px),
                'py': ak.to_list(particles.py),
                'pz': ak.to_list(particles.pz),
                'energy': ak.to_list(particles.energy),
                'charge': ak.to_list(particles.charge),
                'mass': ak.to_list(particles.mass),
            }
        
        return serializable
    
    def close(self):
        """Close the producer"""
        self.producer.close()
        logger.info("Kafka producer closed")
