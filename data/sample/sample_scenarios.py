#!/usr/bin/env python3
"""
Sample scenarios for testing the Railway Traffic Control System
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

from datetime import datetime, timedelta
from models import Train, Section, TrackSegment, TrainType, TrainStatus
from optimization import OptimizationEngine
from interface.data_service import DataService

def create_high_congestion_scenario():
    """Create a high congestion scenario with 10 trains competing for resources"""
    
    data_service = DataService()
    section = data_service.get_sample_section()
    
    base_time = datetime.now().replace(second=0, microsecond=0)
    trains = []
    
    # Create 10 trains with overlapping schedules
    train_configs = [
        ("express_001", "12001", TrainType.EXPRESS, 0, "track_1"),
        ("passenger_002", "59301", TrainType.PASSENGER, 5, "platform_1"),
        ("express_003", "12007", TrainType.EXPRESS, 8, "track_1"),  # Conflict with express_001
        ("freight_004", "50001", TrainType.FREIGHT, 10, "track_3"),
        ("passenger_005", "59303", TrainType.PASSENGER, 12, "platform_1"),  # Conflict with passenger_002
        ("express_006", "12009", TrainType.EXPRESS, 15, "track_2"),
        ("freight_007", "50003", TrainType.FREIGHT, 18, "track_3"),  # Conflict with freight_004
        ("passenger_008", "59305", TrainType.PASSENGER, 20, "platform_2"),
        ("express_009", "12011", TrainType.EXPRESS, 22, "track_1"),  # Multiple conflicts
        ("passenger_010", "59307", TrainType.PASSENGER, 25, "platform_1")   # Platform overload
    ]
    
    for train_id, train_number, train_type, arrival_offset, position in train_configs:
        arrival_time = base_time + timedelta(minutes=arrival_offset)
        departure_time = arrival_time + timedelta(minutes=15 + (train_type.value * 5))
        
        train = Train(
            train_id=train_id,
            train_number=train_number,
            train_type=train_type,
            scheduled_arrival=arrival_time,
            scheduled_departure=departure_time,
            current_position=position,
            status=TrainStatus.SCHEDULED
        )
        
        trains.append(train)
    
    # Add some delays
    trains[2].set_delay(15)  # Express train delayed
    trains[4].set_delay(8)   # Passenger train delayed
    trains[8].set_delay(20)  # Another express train heavily delayed
    
    return section, trains

def create_platform_bottleneck_scenario():
    """Create a scenario focused on platform capacity issues"""
    
    data_service = DataService()
    section = data_service.get_sample_section()
    
    base_time = datetime.now().replace(second=0, microsecond=0)
    trains = []
    
    # Multiple passenger trains trying to use limited platforms
    passenger_configs = [
        ("pass_001", "59301", 0, "platform_1"),
        ("pass_002", "59303", 2, "platform_1"),
        ("pass_003", "59305", 5, "platform_1"),
        ("pass_004", "59307", 7, "platform_2"),
        ("pass_005", "59309", 10, "platform_2"),
    ]
    
    for train_id, train_number, arrival_offset, position in passenger_configs:
        arrival_time = base_time + timedelta(minutes=arrival_offset)
        departure_time = arrival_time + timedelta(minutes=25)  # Long platform occupancy
        
        train = Train(
            train_id=train_id,
            train_number=train_number,
            train_type=TrainType.PASSENGER,
            scheduled_arrival=arrival_time,
            scheduled_departure=departure_time,
            current_position=position,
            status=TrainStatus.SCHEDULED
        )
        
        trains.append(train)
    
    return section, trains

def create_express_priority_scenario():
    """Create scenario to test express train prioritization"""
    
    data_service = DataService()
    section = data_service.get_sample_section()
    
    base_time = datetime.now().replace(second=0, microsecond=0)
    trains = []
    
    # Mix of train types with express trains needing priority
    train_configs = [
        ("freight_001", "50001", TrainType.FREIGHT, 0, "track_3"),
        ("passenger_002", "59301", TrainType.PASSENGER, 5, "platform_1"),
        ("express_003", "12001", TrainType.EXPRESS, 10, "track_1"),  # Should get priority
        ("freight_004", "50003", TrainType.FREIGHT, 12, "track_2"),
        ("express_005", "12007", TrainType.EXPRESS, 15, "track_1"),  # Conflict, needs rerouting
        ("passenger_006", "59303", TrainType.PASSENGER, 18, "platform_2"),
    ]
    
    for train_id, train_number, train_type, arrival_offset, position in train_configs:
        arrival_time = base_time + timedelta(minutes=arrival_offset)
        departure_time = arrival_time + timedelta(minutes=train_type.value * 8)
        
        train = Train(
            train_id=train_id,
            train_number=train_number,
            train_type=train_type,
            scheduled_arrival=arrival_time,
            scheduled_departure=departure_time,
            current_position=position,
            status=TrainStatus.SCHEDULED
        )
        
        trains.append(train)
    
    # Delay the freight train to test if express gets precedence
    trains[0].set_delay(10)
    
    return section, trains

def run_scenario_test(scenario_name, section, trains):
    """Run optimization on a scenario and print results"""
    
    print(f"\\n{'='*60}")
    print(f"TESTING SCENARIO: {scenario_name}")
    print(f"{'='*60}")
    
    print(f"\\n📊 Initial State:")
    print(f"Total trains: {len(trains)}")
    print(f"Section capacity: {section.total_capacity}")
    print(f"Current utilization: {section.current_occupancy}/{section.total_capacity}")
    
    print(f"\\n🚆 Train Details:")
    for train in trains:
        delay_info = f" (+{train.delay_minutes}min delay)" if train.is_delayed else ""
        print(f"  {train.train_number} ({train.train_type.name}): "
              f"{train.scheduled_arrival.strftime('%H:%M')}{delay_info} "
              f"at {train.current_position} - Priority: {train.priority_score}")
    
    # Initialize optimization engine
    optimizer = OptimizationEngine(section)
    
    # Run optimization
    result = optimizer.optimize(trains)
    
    print(f"\\n⚡ Optimization Results:")
    print(f"Processing time: {result['processing_time_ms']}ms")
    print(f"Status: {result['status']}")
    
    if result['status'] == 'success':
        print(f"\\n🔍 Conflicts Detected: {len(result['conflicts'])}")
        for conflict in result['conflicts']:
            print(f"  - {conflict['conflict_type']}: {conflict['description']}")
        
        print(f"\\n💡 Recommendations ({len(result['recommendations'])}):")
        for rec in result['recommendations']:
            action = rec['action'].upper()
            delay_info = f" ({rec.get('delay_minutes', 0)}min)" if 'delay_minutes' in rec else ""
            print(f"  - {rec['train_id']}: {action}{delay_info} - {rec['reason']}")
        
        metrics = result['metrics']
        print(f"\\n📈 Performance Metrics:")
        train_metrics = metrics['train_metrics']
        print(f"  On-time percentage: {train_metrics['on_time_percentage']:.1f}%")
        print(f"  Total delay added: {result['optimization_result']['total_delay_minutes']:.1f} min")
        print(f"  Throughput improvement: {result['optimization_result']['throughput_improvement']:.1f}%")
        
        conflict_metrics = metrics['conflict_metrics']
        print(f"  Conflict resolution rate: {conflict_metrics['resolution_rate']:.1f}%")
        
    else:
        print(f"❌ Optimization failed: {result.get('error_message', 'Unknown error')}")
    
    return result

def main():
    """Run all test scenarios"""
    
    print("🚂 Railway Traffic Control System - Test Scenarios")
    print("=" * 60)
    
    scenarios = [
        ("High Congestion Test", create_high_congestion_scenario),
        ("Platform Bottleneck Test", create_platform_bottleneck_scenario),
        ("Express Priority Test", create_express_priority_scenario),
    ]
    
    results = {}
    
    for scenario_name, scenario_func in scenarios:
        try:
            section, trains = scenario_func()
            result = run_scenario_test(scenario_name, section, trains)
            results[scenario_name] = result
        except Exception as e:
            print(f"❌ Error in {scenario_name}: {str(e)}")
            results[scenario_name] = {"status": "error", "error": str(e)}
    
    # Summary
    print(f"\\n{'='*60}")
    print("SUMMARY OF ALL SCENARIOS")
    print(f"{'='*60}")
    
    for scenario_name, result in results.items():
        status = "✅ SUCCESS" if result.get('status') == 'success' else "❌ FAILED"
        processing_time = result.get('processing_time_ms', 0)
        print(f"{scenario_name}: {status} ({processing_time}ms)")
    
    print(f"\\n🎯 MVP Testing Complete!")
    print("🌐 Start the web interface with: python -m src.interface.app")

if __name__ == "__main__":
    main()
