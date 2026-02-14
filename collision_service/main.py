"""
Collision Service Main Application
Generates particle collision events and publishes to Kafka
"""
import logging
import time
import signal
import sys
from config import Config
from generator import SimpleCollisionGenerator
from kafka_producer import CollisionEventProducer

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CollisionService:
    """Main collision service application"""
    
    def __init__(self):
        self.generator = SimpleCollisionGenerator(Config.CENTER_OF_MASS_ENERGY)
        self.producer = CollisionEventProducer(
            Config.KAFKA_BOOTSTRAP_SERVERS,
            Config.KAFKA_TOPIC_COLLISION_EVENTS
        )
        self.running = True
        self.total_events = 0
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.running = False
    
    def run(self):
        """Main run loop"""
        logger.info("Collision Service starting...")
        logger.info(f"Generating {Config.EVENTS_PER_BATCH} events every {Config.BATCH_INTERVAL_SECONDS}s")
        logger.info(f"Center of mass energy: {Config.CENTER_OF_MASS_ENERGY} GeV")
        
        try:
            while self.running:
                # Generate batch of events
                logger.info(f"Generating batch of {Config.EVENTS_PER_BATCH} events...")
                events = self.generator.generate_batch(Config.EVENTS_PER_BATCH)
                
                # Send to Kafka
                success_count = self.producer.send_batch(events)
                self.total_events += success_count
                
                logger.info(
                    f"Batch complete. Total events generated: {self.total_events}"
                )
                
                # Wait before next batch
                time.sleep(Config.BATCH_INTERVAL_SECONDS)
                
        except Exception as e:
            logger.error(f"Error in main loop: {e}", exc_info=True)
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Cleanup and shutdown"""
        logger.info("Shutting down collision service...")
        self.producer.close()
        logger.info(f"Service stopped. Total events generated: {self.total_events}")

def main():
    """Entry point"""
    service = CollisionService()
    service.run()

if __name__ == '__main__':
    main()
