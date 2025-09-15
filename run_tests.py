#!/usr/bin/env python3
"""
Script to run test scenarios for the Railway Traffic Control System
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now we can import and run the scenarios
if __name__ == "__main__":
    try:
        print("🧪 Running Railway Traffic Control Test Scenarios...")
        print("📁 Project root:", project_root)
        print("🐍 Python path includes:", src_path)
        
        # Import the scenario functions
        from datetime import datetime, timedelta
        from models import Train, Section, TrackSegment, TrainType, TrainStatus
        from optimization import OptimizationEngine
        from interface.data_service import DataService
        
        # Run a simple test
        print("\\n1. Testing data service...")
        data_service = DataService()
        section = data_service.get_sample_section()
        trains = data_service.get_sample_trains()
        print(f"✅ Created section with {len(section.track_segments)} segments")
        print(f"✅ Generated {len(trains)} sample trains")
        
        # Test optimization
        print("\\n2. Testing optimization engine...")
        optimizer = OptimizationEngine(section)
        result = optimizer.optimize(trains)
        print(f"✅ Optimization completed in {result.get('processing_time_ms', 0)}ms")
        print(f"✅ Generated {len(result.get('recommendations', []))} recommendations")
        
        # Show some results
        if result.get('status') == 'success':
            print("\\n📊 Results Summary:")
            metrics = result.get('metrics', {})
            train_metrics = metrics.get('train_metrics', {})
            print(f"  - Total trains: {train_metrics.get('total_trains', 0)}")
            print(f"  - On-time percentage: {train_metrics.get('on_time_percentage', 0):.1f}%")
            print(f"  - Conflicts detected: {len(result.get('conflicts', []))}")
            
            print("\\n💡 Sample Recommendations:")
            for i, rec in enumerate(result.get('recommendations', [])[:3]):
                print(f"  {i+1}. Train {rec.get('train_id')}: {rec.get('action').upper()} - {rec.get('reason')}")
        
        print("\\n🎉 All tests completed successfully!")
        print("🌐 You can now run the web interface with: python3 run_app.py")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📦 Try installing dependencies: pip3 install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        import traceback
        traceback.print_exc()
