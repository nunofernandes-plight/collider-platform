"""
Analysis Service Main Application
Consumes collision events from Kafka, processes them, and stores results
"""
import logging
import json
import signal
import sys
from kafka import KafkaConsumer
from config import config
from processor import PhysicsProcessor
from database import DatabaseHandler
from cache import CacheHandler

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AnalysisService:
    """Main analysis service application"""
    
    def __init__(self):
        self.processor = PhysicsProcessor()
        self.db = DatabaseHandler(config.DATABASE_URL)
        self.cache = CacheHandler(config.REDIS_HOST, config.REDIS_PORT, config.REDIS_DB)
        
        # Initialize Kafka consumer
        self.consumer = KafkaConsumer(
            config.KAFKA_TOPIC_COLLISION_EVENTS,
            bootstrap_servers=config.KAFKA_BOOTSTRAP_SERVERS,
            group_id=config.KAFKA_GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            max_poll_records=config.BATCH_SIZE
        )
        
        self.running = True
        self.total_processed = 0
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("Analysis Service initialized")
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def run(self):
        """Main run loop"""
        logger.info("Analysis Service starting...")
        logger.info(f"Consuming from topic: {config.KAFKA_TOPIC_COLLISION_EVENTS}")
        
        try:
            for message in self.consumer:
                if not self.running:
                    break
                
                # Process event
                event = message.value
                self.process_event(event)
                
                if self.total_processed % 10 == 0:
                    logger.info(f"Processed {self.total_processed} events")
                    
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.shutdown()
    
    def process_event(self, event: dict):
        """
        Process a single collision event
        
        Args:
            event: Event dictionary from Kafka
        """
        try:
            # Calculate kinematics
            kinematics = self.processor.calculate_kinematics(event)
            
            # Store to database
            success = self.db.store_event(event, kinematics)
            
            if success:
                # Cache the processed event
                combined_data = {**event, 'kinematics': kinematics}
                self.cache.cache_event(event['event_id'], combined_data)
                
                # Add to recent events
                self.cache.add_to_recent_events(event['event_id'])
                
                # Increment processed counter
                self.cache.increment_counter('stats:events_processed')
                
                self.total_processed += 1
                
                logger.debug(
                    f"Processed event {event['event_id']}: "
                    f"M={kinematics['invariant_mass']:.2f} GeV, "
                    f"MET={kinematics['missing_et']:.2f} GeV, "
                    f"Jets={kinematics['num_jets']}"
                )
            else:
                logger.warning(f"Failed to store event {event['event_id']}")
                
        except Exception as e:
            logger.error(f"Error processing event: {e}", exc_info=True)
    
    def shutdown(self):
        """Cleanup and shutdown"""
        logger.info("Shutting down analysis service...")
        self.consumer.close()
        self.db.close()
        self.cache.close()
        logger.info(f"Service stopped. Total events processed: {self.total_processed}")

def main():
    """Entry point"""
    service = AnalysisService()
    service.run()

if __name__ == '__main__':
    main()
