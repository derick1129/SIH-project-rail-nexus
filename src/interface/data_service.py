from typing import List, Dict, Any
from datetime import datetime, timedelta
import random

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models import Train, Section, TrackSegment, TrainType, TrainStatus

class DataService:
    """Service for managing sample data and train scenarios"""
    
    def __init__(self):
        self.sample_section = self._create_sample_section()
        self.base_trains = self._create_base_trains()
    
    def get_sample_section(self) -> Section:
        """Get the sample railway section"""
        return self.sample_section
    
    def get_sample_trains(self) -> List[Train]:
        """Get sample trains for the section"""
        # Return fresh copies to avoid state issues
        return [self._copy_train(train) for train in self.base_trains]
    
    def apply_modifications(self, trains: List[Train], modifications: Dict[str, Any]) -> List[Train]:
        """Apply modifications to trains (delays, etc.)"""
        
        train_delays = modifications.get('train_delays', {})
        
        for train in trains:
            if train.train_id in train_delays:
                delay_minutes = train_delays[train.train_id]
                train.set_delay(delay_minutes)
        
        return trains
    
    def create_scenario_trains(self, scenario_data: Dict[str, Any]) -> List[Train]:
        """Create trains based on scenario parameters"""
        
        # Default scenario uses base trains
        if not scenario_data or scenario_data.get('use_default', True):
            return self.get_sample_trains()
        
        # Custom scenario parameters
        num_trains = scenario_data.get('num_trains', 5)
        train_types = scenario_data.get('train_types', ['EXPRESS', 'PASSENGER', 'FREIGHT'])
        delay_probability = scenario_data.get('delay_probability', 0.2)
        max_delay_minutes = scenario_data.get('max_delay_minutes', 30)
        
        trains = []
        base_time = datetime.now().replace(second=0, microsecond=0)
        segments = ['track_1', 'platform_1', 'track_2', 'platform_2', 'track_3']
        
        for i in range(num_trains):
            # Random train type
            train_type_name = random.choice(train_types)
            train_type = TrainType[train_type_name]
            
            # Schedule with some spacing
            arrival_time = base_time + timedelta(minutes=i * 15 + random.randint(-5, 5))
            departure_time = arrival_time + timedelta(minutes=random.randint(10, 30))
            
            train = Train(
                train_id=f"scenario_train_{i+1}",
                train_number=f"SC{1000 + i}",
                train_type=train_type,
                scheduled_arrival=arrival_time,
                scheduled_departure=departure_time,
                current_position=random.choice(segments),
                status=TrainStatus.SCHEDULED
            )
            
            # Apply random delays
            if random.random() < delay_probability:
                delay = random.randint(5, max_delay_minutes)
                train.set_delay(delay)
            
            trains.append(train)
        
        return trains
    
    def _create_sample_section(self) -> Section:
        """Create a sample railway section with track segments"""
        
        track_segments = [
            TrackSegment(
                segment_id="track_1",
                name="Main Line Track 1",
                length_km=2.5,
                capacity=1
            ),
            TrackSegment(
                segment_id="platform_1",
                name="Platform 1",
                length_km=0.3,
                capacity=1,
                is_platform=True,
                platform_capacity=2
            ),
            TrackSegment(
                segment_id="track_2",
                name="Main Line Track 2",
                length_km=3.0,
                capacity=1
            ),
            TrackSegment(
                segment_id="platform_2",
                name="Platform 2",
                length_km=0.4,
                capacity=1,
                is_platform=True,
                platform_capacity=1
            ),
            TrackSegment(
                segment_id="track_3",
                name="Freight Siding",
                length_km=1.8,
                capacity=2
            )
        ]
        
        section = Section(
            section_id="mumbai_central_west",
            name="Mumbai Central West Section",
            track_segments=track_segments,
            min_headway_minutes=5
        )
        
        return section
    
    def _create_base_trains(self) -> List[Train]:
        """Create base sample trains"""
        
        base_time = datetime.now().replace(second=0, microsecond=0)
        
        trains = [
            Train(
                train_id="express_001",
                train_number="12001",
                train_type=TrainType.EXPRESS,
                scheduled_arrival=base_time + timedelta(minutes=10),
                scheduled_departure=base_time + timedelta(minutes=25),
                current_position="track_1",
                status=TrainStatus.RUNNING
            ),
            Train(
                train_id="passenger_002",
                train_number="59301",
                train_type=TrainType.PASSENGER,
                scheduled_arrival=base_time + timedelta(minutes=15),
                scheduled_departure=base_time + timedelta(minutes=35),
                current_position="platform_1",
                status=TrainStatus.SCHEDULED
            ),
            Train(
                train_id="express_003",
                train_number="12007",
                train_type=TrainType.EXPRESS,
                scheduled_arrival=base_time + timedelta(minutes=20),
                scheduled_departure=base_time + timedelta(minutes=30),
                current_position="track_2",
                status=TrainStatus.DELAYED
            ),
            Train(
                train_id="freight_004",
                train_number="50001",
                train_type=TrainType.FREIGHT,
                scheduled_arrival=base_time + timedelta(minutes=25),
                scheduled_departure=base_time + timedelta(minutes=55),
                current_position="track_3",
                status=TrainStatus.SCHEDULED
            ),
            Train(
                train_id="passenger_005",
                train_number="59303",
                train_type=TrainType.PASSENGER,
                scheduled_arrival=base_time + timedelta(minutes=30),
                scheduled_departure=base_time + timedelta(minutes=45),
                current_position="platform_2",
                status=TrainStatus.SCHEDULED
            ),
            Train(
                train_id="express_006",
                train_number="12009",
                train_type=TrainType.EXPRESS,
                scheduled_arrival=base_time + timedelta(minutes=35),
                scheduled_departure=base_time + timedelta(minutes=45),
                current_position="track_1",
                status=TrainStatus.SCHEDULED
            )
        ]
        
        # Set some trains as delayed
        trains[2].set_delay(10)  # Express train 3 delayed by 10 minutes
        
        return trains
    
    def _copy_train(self, train: Train) -> Train:
        """Create a copy of a train"""
        return Train(
            train_id=train.train_id,
            train_number=train.train_number,
            train_type=train.train_type,
            scheduled_arrival=train.scheduled_arrival,
            scheduled_departure=train.scheduled_departure,
            current_position=train.current_position,
            status=train.status,
            actual_arrival=train.actual_arrival,
            actual_departure=train.actual_departure,
            priority_score=train.priority_score
        )
