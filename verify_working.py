#!/usr/bin/env python3
"""
Quick verification that the Railway Traffic Control System works
"""

import sys
from pathlib import Path

# Add src to path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

print("🚂 RAILWAY TRAFFIC CONTROL SYSTEM - VERIFICATION")
print("=" * 60)

try:
    # Test 1: Core functionality
    print("1. Testing core system...")
    from interface.data_service import DataService
    from optimization.optimizer import OptimizationEngine
    
    data_service = DataService()
    section = data_service.get_sample_section()
    trains = data_service.get_sample_trains()
    optimizer = OptimizationEngine(section)
    result = optimizer.optimize(trains)
    
    print(f"   ✅ Processed {len(trains)} trains")
    print(f"   ✅ Detected {len(result['conflicts'])} conflicts")
    print(f"   ✅ Generated {len(result['recommendations'])} recommendations")
    print(f"   ✅ Status: {result['status']}")
    
    # Test 2: Web app creation
    print("\\n2. Testing web application...")
    from interface.app import create_app
    app = create_app()
    print(f"   ✅ Flask app created successfully")
    print(f"   ✅ Template directory: {app.template_folder}")
    print(f"   ✅ Debug mode: {app.debug}")
    
    print("\\n🎉 VERIFICATION COMPLETE - SYSTEM IS WORKING!")
    print("\\n📋 What you can do now:")
    print("   python3 run_tests.py    # Run full test suite")
    print("   python3 run_app.py      # Start web interface")  
    print("   python3 launch.py       # Interactive launcher")
    print("\\n🌐 Once started, open: http://127.0.0.1:5000")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
