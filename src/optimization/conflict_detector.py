from typing import List, Dict, Tuple
from datetime import datetime, timedelta
import uuid

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Train, Section, Conflict, ConflictType

class ConflictDetector:
    """Detects scheduling conflicts between trains in a section"""
    
    def __init__(self, section: Section):
        self.section = section
        
    def detect_conflicts(self, trains: List[Train]) -> List[Conflict]:
        """Detect all types of conflicts for the given trains"""
        conflicts = []
        
        # Sort trains by scheduled arrival time
        sorted_trains = sorted(trains, key=lambda t: t.scheduled_arrival)
        
        # Detect track occupancy conflicts
        conflicts.extend(self._detect_track_conflicts(sorted_trains))
        
        # Detect headway violations
        conflicts.extend(self._detect_headway_conflicts(sorted_trains))
        
        # Detect platform capacity conflicts
        conflicts.extend(self._detect_platform_conflicts(sorted_trains))
        
        return conflicts
    
    def _detect_track_conflicts(self, trains: List[Train]) -> List[Conflict]:
        """Detect conflicts where multiple trains want the same track segment"""
        conflicts = []
        segment_schedules = {}
        
        for train in trains:
            if not train.current_position:
                continue
                
            segment_id = train.current_position
            if segment_id not in segment_schedules:
                segment_schedules[segment_id] = []
            
            # Calculate train's occupancy period
            start_time = train.scheduled_arrival
            end_time = train.scheduled_departure or (start_time + train.expected_travel_time)
            
            segment_schedules[segment_id].append({
                'train': train,
                'start': start_time,
                'end': end_time
            })
        
        # Check for overlapping occupancies in each segment
        for segment_id, schedule in segment_schedules.items():
            segment = self.section.get_segment(segment_id)
            if not segment:
                continue
                
            # Sort by start time
            schedule.sort(key=lambda x: x['start'])
            
            # Find overlapping periods that exceed segment capacity
            for i in range(len(schedule)):
                overlapping_trains = [schedule[i]['train']]
                current_end = schedule[i]['end']
                
                for j in range(i + 1, len(schedule)):
                    if schedule[j]['start'] < current_end:
                        overlapping_trains.append(schedule[j]['train'])
                        current_end = max(current_end, schedule[j]['end'])
                    else:
                        break
                
                # If more trains overlap than segment capacity, create conflict
                if len(overlapping_trains) > segment.capacity:
                    conflict = Conflict(
                        conflict_id=str(uuid.uuid4()),
                        conflict_type=ConflictType.SAME_TRACK,
                        train_ids=[t.train_id for t in overlapping_trains],
                        segment_id=segment_id,
                        scheduled_time=schedule[i]['start'],
                        severity=min(5, len(overlapping_trains)),
                        description=f"Track capacity exceeded: {len(overlapping_trains)} trains on segment {segment_id} (capacity: {segment.capacity})"
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def _detect_headway_conflicts(self, trains: List[Train]) -> List[Conflict]:
        """Detect insufficient headway between consecutive trains"""
        conflicts = []
        min_headway = timedelta(minutes=self.section.min_headway_minutes)
        
        for i in range(len(trains) - 1):
            current_train = trains[i]
            next_train = trains[i + 1]
            
            # Check if trains are on the same path or adjacent segments
            if self._trains_on_same_path(current_train, next_train):
                # Calculate actual headway
                current_departure = current_train.scheduled_departure or (
                    current_train.scheduled_arrival + current_train.expected_travel_time
                )
                
                actual_headway = next_train.scheduled_arrival - current_departure
                
                if actual_headway < min_headway:
                    conflict = Conflict(
                        conflict_id=str(uuid.uuid4()),
                        conflict_type=ConflictType.HEADWAY,
                        train_ids=[current_train.train_id, next_train.train_id],
                        scheduled_time=next_train.scheduled_arrival,
                        severity=3,
                        description=f"Insufficient headway: {actual_headway.total_seconds()/60:.1f} min (required: {self.section.min_headway_minutes} min)"
                    )
                    conflicts.append(conflict)
        
        return conflicts
    
    def _detect_platform_conflicts(self, trains: List[Train]) -> List[Conflict]:
        """Detect platform capacity conflicts"""
        conflicts = []
        platform_segments = self.section.get_platform_segments()
        
        for platform in platform_segments:
            # Get trains scheduled to use this platform
            platform_trains = []
            for train in trains:
                if train.current_position == platform.segment_id:
                    platform_trains.append(train)
            
            if len(platform_trains) > platform.platform_capacity:
                conflict = Conflict(
                    conflict_id=str(uuid.uuid4()),
                    conflict_type=ConflictType.PLATFORM,
                    train_ids=[t.train_id for t in platform_trains],
                    segment_id=platform.segment_id,
                    severity=4,
                    description=f"Platform capacity exceeded: {len(platform_trains)} trains at platform {platform.name} (capacity: {platform.platform_capacity})"
                )
                conflicts.append(conflict)
        
        return conflicts
    
    def _trains_on_same_path(self, train1: Train, train2: Train) -> bool:
        """Check if two trains are on the same path (simplified logic)"""
        # For MVP: assume trains are on same path if they have positions
        return bool(train1.current_position and train2.current_position)
    
    def get_conflict_summary(self, conflicts: List[Conflict]) -> Dict[str, int]:
        """Get summary statistics of conflicts"""
        summary = {
            'total_conflicts': len(conflicts),
            'resolved_conflicts': len([c for c in conflicts if c.is_resolved]),
            'pending_conflicts': len([c for c in conflicts if not c.is_resolved]),
            'high_severity': len([c for c in conflicts if c.severity >= 4]),
            'medium_severity': len([c for c in conflicts if c.severity == 3]),
            'low_severity': len([c for c in conflicts if c.severity <= 2])
        }
        
        # Count by type
        for conflict_type in ConflictType:
            type_count = len([c for c in conflicts if c.conflict_type == conflict_type])
            summary[f'{conflict_type.value}_conflicts'] = type_count
        
        return summary
