from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import pulp

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Train, Section, Conflict, TrainType

class TrainScheduler:
    """Priority-based train scheduler using linear programming"""
    
    def __init__(self, section: Section):
        self.section = section
        
    def optimize_schedule(self, trains: List[Train], conflicts: List[Conflict]) -> Dict[str, any]:
        """Optimize train schedule to resolve conflicts and maximize throughput"""
        
        # For MVP, use a simplified greedy algorithm based on priority
        # In a full implementation, this would use more sophisticated optimization
        
        optimized_trains = []
        recommendations = []
        total_delay = 0
        
        # Sort trains by priority (higher priority first)
        sorted_trains = sorted(trains, key=lambda t: t.priority_score, reverse=True)
        
        # Track segment reservations
        segment_reservations = {}  # segment_id -> [(start_time, end_time, train_id)]
        
        for train in sorted_trains:
            original_arrival = train.scheduled_arrival
            new_schedule = self._find_optimal_slot(train, segment_reservations)
            
            if new_schedule:
                # Update train schedule
                optimized_train = self._create_optimized_train(train, new_schedule)
                optimized_trains.append(optimized_train)
                
                # Record reservation
                segment_id = new_schedule['segment_id']
                if segment_id not in segment_reservations:
                    segment_reservations[segment_id] = []
                
                segment_reservations[segment_id].append((
                    new_schedule['arrival_time'],
                    new_schedule['departure_time'],
                    train.train_id
                ))
                
                # Calculate delay
                delay = (new_schedule['arrival_time'] - original_arrival).total_seconds() / 60
                if delay > 0:
                    total_delay += delay
                    
                # Generate recommendation
                if delay > 0:
                    recommendations.append({
                        'train_id': train.train_id,
                        'action': 'delay',
                        'delay_minutes': int(delay),
                        'reason': f"Priority-based rescheduling to resolve conflicts",
                        'new_arrival': new_schedule['arrival_time'].isoformat(),
                        'segment_id': segment_id
                    })
                else:
                    recommendations.append({
                        'train_id': train.train_id,
                        'action': 'proceed',
                        'reason': "No conflicts detected",
                        'segment_id': segment_id
                    })
            else:
                # Could not find optimal slot - recommend holding
                optimized_trains.append(train)
                recommendations.append({
                    'train_id': train.train_id,
                    'action': 'hold',
                    'reason': "No available slots found",
                    'recommended_delay': 15  # Default hold time
                })
                total_delay += 15
        
        return {
            'optimized_trains': optimized_trains,
            'recommendations': recommendations,
            'total_delay_minutes': total_delay,
            'throughput_improvement': self._calculate_throughput_improvement(trains, optimized_trains),
            'optimization_timestamp': datetime.now().isoformat()
        }
    
    def _find_optimal_slot(self, train: Train, reservations: Dict[str, List[Tuple]]) -> Optional[Dict]:
        """Find the optimal time slot for a train"""
        
        # Try the train's preferred segment first
        preferred_segment = train.current_position or self._get_best_segment_for_train(train)
        
        if not preferred_segment:
            return None
        
        segment = self.section.get_segment(preferred_segment)
        if not segment:
            return None
        
        # Get existing reservations for this segment
        existing_reservations = reservations.get(preferred_segment, [])
        existing_reservations.sort()  # Sort by start time
        
        # Try to schedule at original time first
        desired_start = train.scheduled_arrival
        desired_end = train.scheduled_departure or (desired_start + train.expected_travel_time)
        
        if self._slot_is_available(desired_start, desired_end, existing_reservations):
            return {
                'segment_id': preferred_segment,
                'arrival_time': desired_start,
                'departure_time': desired_end
            }
        
        # Find next available slot after desired time
        min_headway = timedelta(minutes=self.section.min_headway_minutes)
        
        # Try slots after each existing reservation
        search_time = desired_start
        max_search_time = desired_start + timedelta(hours=2)  # Reasonable search window
        
        while search_time < max_search_time:
            slot_end = search_time + train.expected_travel_time
            
            if self._slot_is_available(search_time, slot_end, existing_reservations):
                return {
                    'segment_id': preferred_segment,
                    'arrival_time': search_time,
                    'departure_time': slot_end
                }
            
            # Move to next potential slot
            search_time += min_headway
        
        return None
    
    def _slot_is_available(self, start_time: datetime, end_time: datetime, 
                          reservations: List[Tuple]) -> bool:
        """Check if a time slot is available given existing reservations"""
        min_headway = timedelta(minutes=self.section.min_headway_minutes)
        
        for res_start, res_end, _ in reservations:
            # Check for overlap with required headway
            if not (end_time + min_headway <= res_start or start_time >= res_end + min_headway):
                return False
        
        return True
    
    def _get_best_segment_for_train(self, train: Train) -> Optional[str]:
        """Get the best segment for a train based on type and availability"""
        available_segments = self.section.get_available_segments()
        
        if not available_segments:
            return None
        
        # For express trains, prefer non-platform segments if available
        if train.train_type == TrainType.EXPRESS:
            non_platform_segments = [s for s in available_segments if not s.is_platform]
            if non_platform_segments:
                return non_platform_segments[0].segment_id
        
        # For passenger trains, prefer platform segments
        elif train.train_type == TrainType.PASSENGER:
            platform_segments = [s for s in available_segments if s.is_platform]
            if platform_segments:
                return platform_segments[0].segment_id
        
        # Default: return first available segment
        return available_segments[0].segment_id
    
    def _create_optimized_train(self, original_train: Train, new_schedule: Dict) -> Train:
        """Create a new train object with optimized schedule"""
        optimized_train = Train(
            train_id=original_train.train_id,
            train_number=original_train.train_number,
            train_type=original_train.train_type,
            scheduled_arrival=new_schedule['arrival_time'],
            scheduled_departure=new_schedule['departure_time'],
            current_position=new_schedule['segment_id'],
            status=original_train.status,
            actual_arrival=original_train.actual_arrival,
            actual_departure=original_train.actual_departure,
            priority_score=original_train.priority_score
        )
        
        # Set delay if rescheduled later
        delay_minutes = (new_schedule['arrival_time'] - original_train.scheduled_arrival).total_seconds() / 60
        if delay_minutes > 0:
            optimized_train.set_delay(int(delay_minutes))
        
        return optimized_train
    
    def _calculate_throughput_improvement(self, original_trains: List[Train], 
                                        optimized_trains: List[Train]) -> float:
        """Calculate throughput improvement percentage"""
        # Simplified calculation based on conflict reduction
        # In reality, this would be more sophisticated
        
        original_conflicts = len([t for t in original_trains if t.is_delayed])
        optimized_conflicts = len([t for t in optimized_trains if t.is_delayed])
        
        if original_conflicts == 0:
            return 0.0
        
        improvement = (original_conflicts - optimized_conflicts) / original_conflicts * 100
        return max(0.0, improvement)
    
    def generate_priority_explanation(self, train: Train) -> str:
        """Generate explanation for train's priority calculation"""
        base_priority = int(train.train_type)
        explanations = []
        
        explanations.append(f"Base priority: {train.train_type.name} = {base_priority}")
        
        if train.is_delayed:
            explanations.append("Delay penalty: -10 points")
        
        explanations.append(f"Final priority score: {train.priority_score}")
        
        return "; ".join(explanations)
