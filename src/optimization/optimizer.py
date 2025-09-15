from typing import List, Dict, Any
from datetime import datetime
import logging

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Train, Section, Conflict
from .conflict_detector import ConflictDetector
from .scheduler import TrainScheduler

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OptimizationEngine:
    """Main optimization engine that coordinates conflict detection and resolution"""
    
    def __init__(self, section: Section):
        self.section = section
        self.conflict_detector = ConflictDetector(section)
        self.scheduler = TrainScheduler(section)
        self.optimization_history = []
        
    def optimize(self, trains: List[Train]) -> Dict[str, Any]:
        """Main optimization method - detect conflicts and generate recommendations"""
        
        start_time = datetime.now()
        logger.info(f"Starting optimization for {len(trains)} trains")
        
        try:
            # Step 1: Detect conflicts
            conflicts = self.conflict_detector.detect_conflicts(trains)
            logger.info(f"Detected {len(conflicts)} conflicts")
            
            # Step 2: Generate conflict summary
            conflict_summary = self.conflict_detector.get_conflict_summary(conflicts)
            
            # Step 3: Optimize schedule if conflicts exist
            optimization_result = None
            if conflicts:
                optimization_result = self.scheduler.optimize_schedule(trains, conflicts)
                logger.info(f"Generated {len(optimization_result['recommendations'])} recommendations")
            else:
                # No conflicts - generate default recommendations
                optimization_result = self._generate_default_recommendations(trains)
                logger.info("No conflicts detected - proceeding with current schedule")
            
            # Step 4: Calculate performance metrics
            metrics = self._calculate_metrics(trains, conflicts, optimization_result)
            
            # Step 5: Compile final result
            result = {
                'timestamp': start_time.isoformat(),
                'section_id': self.section.section_id,
                'trains_analyzed': len(trains),
                'conflicts': [c.to_dict() for c in conflicts],
                'conflict_summary': conflict_summary,
                'optimization_result': optimization_result,
                'metrics': metrics,
                'processing_time_ms': int((datetime.now() - start_time).total_seconds() * 1000),
                'recommendations': optimization_result.get('recommendations', []),
                'status': 'success'
            }
            
            # Store in history
            self.optimization_history.append(result)
            
            # Keep only last 100 optimizations in memory
            if len(self.optimization_history) > 100:
                self.optimization_history = self.optimization_history[-100:]
            
            logger.info(f"Optimization completed in {result['processing_time_ms']}ms")
            return result
            
        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}")
            return {
                'timestamp': start_time.isoformat(),
                'section_id': self.section.section_id,
                'status': 'error',
                'error_message': str(e),
                'processing_time_ms': int((datetime.now() - start_time).total_seconds() * 1000)
            }
    
    def _generate_default_recommendations(self, trains: List[Train]) -> Dict[str, Any]:
        """Generate default recommendations when no conflicts exist"""
        recommendations = []
        
        for train in trains:
            recommendations.append({
                'train_id': train.train_id,
                'action': 'proceed',
                'reason': 'No conflicts detected',
                'segment_id': train.current_position,
                'priority_explanation': self.scheduler.generate_priority_explanation(train)
            })
        
        return {
            'optimized_trains': trains,
            'recommendations': recommendations,
            'total_delay_minutes': 0,
            'throughput_improvement': 0.0,
            'optimization_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_metrics(self, trains: List[Train], conflicts: List[Conflict], 
                          optimization_result: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate performance metrics for the optimization"""
        
        # Basic metrics
        total_trains = len(trains)
        delayed_trains = len([t for t in trains if t.is_delayed])
        express_trains = len([t for t in trains if t.train_type.name == 'EXPRESS'])
        passenger_trains = len([t for t in trains if t.train_type.name == 'PASSENGER'])
        freight_trains = len([t for t in trains if t.train_type.name == 'FREIGHT'])
        
        # Conflict metrics
        total_conflicts = len(conflicts)
        resolved_conflicts = len([c for c in conflicts if c.is_resolved])
        
        # Section utilization
        section_utilization = self.section.utilization_rate
        
        # Recommendations breakdown
        recommendations = optimization_result.get('recommendations', [])
        proceed_count = len([r for r in recommendations if r.get('action') == 'proceed'])
        delay_count = len([r for r in recommendations if r.get('action') == 'delay'])
        hold_count = len([r for r in recommendations if r.get('action') == 'hold'])
        
        return {
            'train_metrics': {
                'total_trains': total_trains,
                'delayed_trains': delayed_trains,
                'on_time_percentage': ((total_trains - delayed_trains) / total_trains * 100) if total_trains > 0 else 100,
                'express_trains': express_trains,
                'passenger_trains': passenger_trains,
                'freight_trains': freight_trains
            },
            'conflict_metrics': {
                'total_conflicts': total_conflicts,
                'resolved_conflicts': resolved_conflicts,
                'resolution_rate': (resolved_conflicts / total_conflicts * 100) if total_conflicts > 0 else 100
            },
            'section_metrics': {
                'utilization_rate': section_utilization,
                'available_capacity': self.section.total_capacity - self.section.current_occupancy,
                'total_capacity': self.section.total_capacity
            },
            'recommendation_metrics': {
                'proceed_recommendations': proceed_count,
                'delay_recommendations': delay_count,
                'hold_recommendations': hold_count,
                'total_delay_minutes': optimization_result.get('total_delay_minutes', 0),
                'throughput_improvement': optimization_result.get('throughput_improvement', 0.0)
            }
        }
    
    def get_optimization_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent optimization history"""
        return self.optimization_history[-limit:]
    
    def get_section_status(self) -> Dict[str, Any]:
        """Get current section status"""
        return {
            'section_info': self.section.to_dict(),
            'current_time': datetime.now().isoformat(),
            'optimization_count': len(self.optimization_history),
            'last_optimization': self.optimization_history[-1]['timestamp'] if self.optimization_history else None
        }
    
    def simulate_scenario(self, trains: List[Train], scenario_name: str = "Default") -> Dict[str, Any]:
        """Run what-if scenario analysis"""
        logger.info(f"Running scenario analysis: {scenario_name}")
        
        # Run optimization
        result = self.optimize(trains)
        
        # Add scenario metadata
        result['scenario_name'] = scenario_name
        result['scenario_timestamp'] = datetime.now().isoformat()
        
        return result
