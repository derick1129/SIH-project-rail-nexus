from enum import Enum, IntEnum

class TrainType(IntEnum):
    """Train types with priority levels (higher number = higher priority)"""
    FREIGHT = 1
    PASSENGER = 2
    EXPRESS = 3
    
class TrainStatus(Enum):
    """Current status of a train"""
    SCHEDULED = "scheduled"
    RUNNING = "running"
    DELAYED = "delayed"
    HELD = "held"
    COMPLETED = "completed"
    
class ConflictType(Enum):
    """Types of scheduling conflicts"""
    SAME_TRACK = "same_track"  # Two trains scheduled on same track segment
    CROSSING = "crossing"      # Trains need to cross at junction
    PLATFORM = "platform"     # Platform capacity conflict
    HEADWAY = "headway"       # Insufficient headway between trains
