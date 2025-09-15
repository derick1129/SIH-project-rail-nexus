from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
from enums import ConflictType

@dataclass
class Conflict:
    """Represents a scheduling conflict between trains"""
    
    conflict_id: str
    conflict_type: ConflictType
    train_ids: List[str]
    segment_id: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    description: str = ""
    severity: int = 1  # 1-5 scale, 5 being most severe
    is_resolved: bool = False
    resolution_action: Optional[str] = None
    resolved_at: Optional[datetime] = None
    
    @property
    def affected_train_count(self) -> int:
        """Number of trains affected by this conflict"""
        return len(self.train_ids)
    
    @property
    def priority_weight(self) -> int:
        """Calculate priority weight for conflict resolution"""
        # Higher severity and more trains = higher priority
        return self.severity * 10 + self.affected_train_count
    
    def add_train(self, train_id: str):
        """Add a train to the conflict"""
        if train_id not in self.train_ids:
            self.train_ids.append(train_id)
    
    def remove_train(self, train_id: str):
        """Remove a train from the conflict"""
        if train_id in self.train_ids:
            self.train_ids.remove(train_id)
    
    def resolve(self, action: str):
        """Mark conflict as resolved with specified action"""
        self.is_resolved = True
        self.resolution_action = action
        self.resolved_at = datetime.now()
    
    def generate_description(self, trains_info: Dict[str, Any] = None) -> str:
        """Generate human-readable description of the conflict"""
        if self.description:
            return self.description
            
        if self.conflict_type == ConflictType.SAME_TRACK:
            return f"Track occupancy conflict on segment {self.segment_id} involving {len(self.train_ids)} trains"
        elif self.conflict_type == ConflictType.HEADWAY:
            return f"Insufficient headway between trains {', '.join(self.train_ids)}"
        elif self.conflict_type == ConflictType.PLATFORM:
            return f"Platform capacity exceeded at {self.segment_id} with trains {', '.join(self.train_ids)}"
        elif self.conflict_type == ConflictType.CROSSING:
            return f"Crossing conflict between trains {', '.join(self.train_ids)}"
        else:
            return f"Conflict between trains {', '.join(self.train_ids)}"
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'conflict_id': self.conflict_id,
            'conflict_type': self.conflict_type.value,
            'train_ids': self.train_ids,
            'segment_id': self.segment_id,
            'scheduled_time': self.scheduled_time.isoformat() if self.scheduled_time else None,
            'description': self.generate_description(),
            'severity': self.severity,
            'is_resolved': self.is_resolved,
            'resolution_action': self.resolution_action,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'affected_train_count': self.affected_train_count,
            'priority_weight': self.priority_weight
        }
