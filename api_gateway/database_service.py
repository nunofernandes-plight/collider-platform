"""Database service for API Gateway"""
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from typing import List, Optional, Dict, Any
import redis
import json

logger = logging.getLogger(__name__)

class DatabaseService:
    """Database and cache operations"""
    
    def __init__(self, database_url: str, redis_host: str, redis_port: int):
        """Initialize database and Redis connections"""
        self.engine = create_engine(
            database_url,
            poolclass=QueuePool,
            pool_size=5,
            max_overflow=10,
            echo=False
        )
        
        self.redis_client = redis.Redis(
            host=redis_host,
            port=redis_port,
            db=0,
            decode_responses=True
        )
        
        logger.info("Database service initialized")
    
    def get_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get event by ID"""
        # Try cache first
        cached = self.redis_client.get(f"event:{event_id}:processed")
        if cached:
            return json.loads(cached)
        
        # Query database
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("""
                        SELECT e.*, k.*
                        FROM events e
                        LEFT JOIN event_kinematics k ON e.event_id = k.event_id
                        WHERE e.event_id = :event_id
                    """),
                    {"event_id": event_id}
                )
                row = result.fetchone()
                if row:
                    return dict(row._mapping)
                return None
        except Exception as e:
            logger.error(f"Error fetching event: {e}")
            return None
    
    def get_events(self, limit: int = 10, offset: int = 0, 
                   filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Get list of events with pagination"""
        try:
            with self.engine.connect() as conn:
                # Build query
                where_clauses = []
                params = {"limit": limit, "offset": offset}
                
                if filters:
                    if filters.get('min_invariant_mass'):
                        where_clauses.append("k.invariant_mass >= :min_inv_mass")
                        params['min_inv_mass'] = filters['min_invariant_mass']
                    
                    if filters.get('min_jets'):
                        where_clauses.append("k.num_jets >= :min_jets")
                        params['min_jets'] = filters['min_jets']
                    
                    if filters.get('run_number'):
                        where_clauses.append("e.run_number = :run_number")
                        params['run_number'] = filters['run_number']
                
                where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                query = text(f"""
                    SELECT e.*, k.*
                    FROM events e
                    LEFT JOIN event_kinematics k ON e.event_id = k.event_id
                    {where_clause}
                    ORDER BY e.timestamp DESC
                    LIMIT :limit OFFSET :offset
                """)
                
                result = conn.execute(query, params)
                return [dict(row._mapping) for row in result]
        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return []
    
    def get_event_count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """Get total event count"""
        try:
            with self.engine.connect() as conn:
                where_clauses = []
                params = {}
                
                if filters:
                    if filters.get('min_invariant_mass'):
                        where_clauses.append("k.invariant_mass >= :min_inv_mass")
                        params['min_inv_mass'] = filters['min_invariant_mass']
                    if filters.get('run_number'):
                        where_clauses.append("e.run_number = :run_number")
                        params['run_number'] = filters['run_number']
                
                where_clause = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
                
                query = text(f"""
                    SELECT COUNT(*)
                    FROM events e
                    LEFT JOIN event_kinematics k ON e.event_id = k.event_id
                    {where_clause}
                """)
                
                result = conn.execute(query, params)
                return result.scalar()
        except Exception as e:
            logger.error(f"Error getting count: {e}")
            return 0
    
    def get_histogram_data(self, variable: str, bins: int = 50,
                          range_min: Optional[float] = None,
                          range_max: Optional[float] = None) -> Optional[Dict[str, Any]]:
        """Get histogram data for a variable"""
        try:
            with self.engine.connect() as conn:
                # Get data for variable
                query = text(f"""
                    SELECT {variable}
                    FROM event_kinematics
                    WHERE {variable} IS NOT NULL
                """)
                
                result = conn.execute(query)
                values = [row[0] for row in result]
                
                if not values:
                    return None
                
                # Calculate histogram
                import numpy as np
                
                if range_min is None:
                    range_min = min(values)
                if range_max is None:
                    range_max = max(values)
                
                hist, bin_edges = np.histogram(values, bins=bins, range=(range_min, range_max))
                
                return {
                    'variable': variable,
                    'bins': bin_edges.tolist(),
                    'values': hist.tolist(),
                    'num_events': len(values),
                    'range_min': range_min,
                    'range_max': range_max
                }
        except Exception as e:
            logger.error(f"Error generating histogram: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get overall statistics"""
        try:
            with self.engine.connect() as conn:
                stats_query = text("""
                    SELECT 
                        COUNT(DISTINCT e.event_id) as total_events,
                        COUNT(DISTINCT e.run_number) as total_runs,
                        COUNT(CASE WHEN k.num_leptons > 0 THEN 1 END) as events_with_leptons,
                        COUNT(CASE WHEN k.num_jets > 0 THEN 1 END) as events_with_jets,
                        AVG(k.invariant_mass) as avg_invariant_mass,
                        AVG(k.missing_et) as avg_missing_et
                    FROM events e
                    LEFT JOIN event_kinematics k ON e.event_id = k.event_id
                """)
                
                result = conn.execute(stats_query)
                row = result.fetchone()
                return dict(row._mapping) if row else {}
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {}
    
    def get_detector_configs(self) -> List[Dict[str, Any]]:
        """Get all detector configurations"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(
                    text("SELECT * FROM detector_configs ORDER BY created_at DESC")
                )
                return [dict(row._mapping) for row in result]
        except Exception as e:
            logger.error(f"Error fetching detector configs: {e}")
            return []
