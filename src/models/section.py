from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class TrackSegment:
    """Represents a track segment within a railway section"""
    
    segment_id: str
    name: str
    length_km: float
    capacity: int = 1  # Number of trains that can occupy simultaneously
    is_platform: bool = False
    platform_capacity: int = 1
    current_occupancy: List[str] = None  # List of train IDs currently on this segment
    
    def __post_init__(self):
        if self.current_occupancy is None:
            self.current_occupancy = []
    
    @property
    def is_available(self) -> bool:
        """Check if segment has available capacity"""
        max_capacity = self.platform_capacity if self.is_platform else self.capacity
        return len(self.current_occupancy) < max_capacity
    
    @property
    def occupancy_rate(self) -> float:
        """Calculate current occupancy rate (0.0 to 1.0)"""
        max_capacity = self.platform_capacity if self.is_platform else self.capacity
        return len(self.current_occupancy) / max_capacity if max_capacity > 0 else 0.0
    
    def add_train(self, train_id: str) -> bool:
        """Add a train to this segment if capacity allows"""
        if self.is_available and train_id not in self.current_occupancy:
            self.current_occupancy.append(train_id)
            return True
        return False
    
    def remove_train(self, train_id: str) -> bool:
        """Remove a train from this segment"""
        if train_id in self.current_occupancy:
            self.current_occupancy.remove(train_id)
            return True
        return False
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'segment_id': self.segment_id,
            'name': self.name,
            'length_km': self.length_km,
            'capacity': self.capacity,
            'is_platform': self.is_platform,
            'platform_capacity': self.platform_capacity,
            'current_occupancy': self.current_occupancy,
            'is_available': self.is_available,
            'occupancy_rate': self.occupancy_rate
        }


@dataclass
class Section:
    """Represents a railway section managed by a section controller"""
    
    section_id: str
    name: str
    track_segments: List[TrackSegment]
    min_headway_minutes: int = 5  # Minimum time between trains
    
    def __post_init__(self):
        self._segment_lookup = {seg.segment_id: seg for seg in self.track_segments}
    
    def get_segment(self, segment_id: str) -> Optional[TrackSegment]:
        """Get a track segment by ID"""
        return self._segment_lookup.get(segment_id)
    
    def get_available_segments(self) -> List[TrackSegment]:
        """Get list of segments with available capacity"""
        return [seg for seg in self.track_segments if seg.is_available]
    
    def get_platform_segments(self) -> List[TrackSegment]:
        """Get list of platform segments"""
        return [seg for seg in self.track_segments if seg.is_platform]
    
    @property
    def total_capacity(self) -> int:
        """Total capacity of all segments in the section"""
        return sum(seg.capacity for seg in self.track_segments)
    
    @property
    def current_occupancy(self) -> int:
        """Current number of trains in the section"""
        return sum(len(seg.current_occupancy) for seg in self.track_segments)
    
    @property
    def utilization_rate(self) -> float:
        """Current utilization rate of the section (0.0 to 1.0)"""
        return self.current_occupancy / self.total_capacity if self.total_capacity > 0 else 0.0
    
    def can_accommodate_train(self, segment_id: str) -> bool:
        """Check if a specific segment can accommodate another train"""
        segment = self.get_segment(segment_id)
        return segment.is_available if segment else False
    
    def assign_train_to_segment(self, train_id: str, segment_id: str) -> bool:
        """Assign a train to a specific segment"""
        segment = self.get_segment(segment_id)
        if segment:
            return segment.add_train(train_id)
        return False
    
    def remove_train_from_segment(self, train_id: str, segment_id: str) -> bool:
        """Remove a train from a specific segment"""
        segment = self.get_segment(segment_id)
        if segment:
            return segment.remove_train(train_id)
        return False
    
    def find_train_position(self, train_id: str) -> Optional[str]:
        """Find which segment a train is currently occupying"""
        for segment in self.track_segments:
            if train_id in segment.current_occupancy:
                return segment.segment_id
        return None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'section_id': self.section_id,
            'name': self.name,
            'track_segments': [seg.to_dict() for seg in self.track_segments],
            'min_headway_minutes': self.min_headway_minutes,
            'total_capacity': self.total_capacity,
            'current_occupancy': self.current_occupancy,
            'utilization_rate': self.utilization_rate
        }
