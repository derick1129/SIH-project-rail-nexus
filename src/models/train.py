from datetime import datetime, timedelta
from typing import Optional, List
from dataclasses import dataclass
from enums import TrainType, TrainStatus

@dataclass
class Train:
    """Represents a train in the railway system"""
    
    train_id: str
    train_number: str
    train_type: TrainType
    scheduled_arrival: datetime
    scheduled_departure: datetime
    current_position: Optional[str] = None  # Current track segment
    status: TrainStatus = TrainStatus.SCHEDULED
    actual_arrival: Optional[datetime] = None
    actual_departure: Optional[datetime] = None
    priority_score: Optional[int] = None
    
    def __post_init__(self):
        """Calculate priority score based on train type and delay"""
        if self.priority_score is None:
            self.priority_score = self.calculate_priority()
    
    def calculate_priority(self) -> int:
        """Calculate dynamic priority based on type, delay, and other factors"""
        base_priority = int(self.train_type)
        
        # Add delay penalty (negative for delayed trains)
        if self.status == TrainStatus.DELAYED:
            delay_penalty = -10
        else:
            delay_penalty = 0
            
        return base_priority * 100 + delay_penalty
    
    @property
    def is_delayed(self) -> bool:
        """Check if train is currently delayed"""
        if self.actual_arrival and self.scheduled_arrival:
            return self.actual_arrival > self.scheduled_arrival
        return self.status == TrainStatus.DELAYED
    
    @property
    def delay_minutes(self) -> int:
        """Calculate delay in minutes"""
        if not self.is_delayed or not self.actual_arrival:
            return 0
        return int((self.actual_arrival - self.scheduled_arrival).total_seconds() / 60)
    
    @property
    def expected_travel_time(self) -> timedelta:
        """Expected time to traverse the section"""
        # Simplified calculation based on train type
        base_minutes = {
            TrainType.EXPRESS: 15,
            TrainType.PASSENGER: 20,
            TrainType.FREIGHT: 30
        }
        return timedelta(minutes=base_minutes.get(self.train_type, 20))
    
    def update_position(self, new_position: str):
        """Update train's current position"""
        self.current_position = new_position
        if self.status == TrainStatus.SCHEDULED:
            self.status = TrainStatus.RUNNING
    
    def set_delay(self, delay_minutes: int):
        """Set train delay and update status"""
        if delay_minutes > 0:
            self.status = TrainStatus.DELAYED
            if self.actual_arrival is None:
                self.actual_arrival = self.scheduled_arrival + timedelta(minutes=delay_minutes)
        else:
            self.status = TrainStatus.RUNNING
    
    def to_dict(self) -> dict:
        """Convert train to dictionary for JSON serialization"""
        return {
            'train_id': self.train_id,
            'train_number': self.train_number,
            'train_type': self.train_type.name,
            'scheduled_arrival': self.scheduled_arrival.isoformat(),
            'scheduled_departure': self.scheduled_departure.isoformat(),
            'current_position': self.current_position,
            'status': self.status.value,
            'priority_score': self.priority_score,
            'is_delayed': self.is_delayed,
            'delay_minutes': self.delay_minutes
        }
