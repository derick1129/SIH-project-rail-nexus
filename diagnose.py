#!/usr/bin/env python3
"""
Railway Traffic Control System - Diagnostic Script
Run this to identify any issues with your setup
"""

import sys
import os
from pathlib import Path
import subprocess

def print_header(text):
    print(f"\n{'='*60}")
    print(f"🔍 {text}")
    print(f"{'='*60}")

def check_python():
    print_header("PYTHON ENVIRONMENT CHECK")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print(f"Current working directory: {os.getcwd()}")
    
    # Check if we're in the right directory
    expected_files = ['run_app.py', 'run_tests.py', 'launch.py', 'src', 'requirements.txt']
    missing_files = [f for f in expected_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        print("❌ You may not be in the correct directory!")
        print("💡 Make sure you're in the railway_traffic_control directory")
    else:
        print("✅ All expected files found")

def check_dependencies():
    print_header("DEPENDENCIES CHECK")
    dependencies = ['flask', 'pulp', 'numpy', 'pandas']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} - OK")
        except ImportError as e:
            print(f"❌ {dep} - MISSING: {e}")
    
    # Check if we can install missing dependencies
    print("\n📦 Checking requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip()
            print(f"Requirements file contents:\n{requirements}")
    except FileNotFoundError:
        print("❌ requirements.txt not found!")

def check_project_structure():
    print_header("PROJECT STRUCTURE CHECK")
    
    # Check src directory structure
    src_path = Path('src')
    if not src_path.exists():
        print("❌ src directory not found!")
        return
    
    expected_structure = {
        'src/__init__.py': 'Main package init',
        'src/models/__init__.py': 'Models package init',
        'src/models/train.py': 'Train model',
        'src/models/section.py': 'Section model',
        'src/models/enums.py': 'Enums',
        'src/optimization/__init__.py': 'Optimization package init',
        'src/optimization/optimizer.py': 'Optimization engine',
        'src/interface/__init__.py': 'Interface package init',
        'src/interface/app.py': 'Flask application',
        'src/interface/data_service.py': 'Data service',
        'templates/dashboard.html': 'Web dashboard template'
    }
    
    for file_path, description in expected_structure.items():
        if os.path.exists(file_path):
            print(f"✅ {file_path} - {description}")
        else:
            print(f"❌ {file_path} - MISSING")

def test_imports():
    print_header("IMPORT TESTS")
    
    # Add src to path
    project_root = Path.cwd()
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))
    print(f"Added to Python path: {src_path}")
    
    # Test basic imports
    import_tests = [
        ('models', 'Basic models package'),
        ('models.train', 'Train model'),
        ('models.section', 'Section model'),
        ('optimization', 'Optimization package'),
        ('optimization.optimizer', 'Optimization engine'),
        ('interface.app', 'Flask app'),
        ('interface.data_service', 'Data service')
    ]
    
    for module, description in import_tests:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError as e:
            print(f"❌ {module} - FAILED: {e}")

def test_basic_functionality():
    print_header("FUNCTIONALITY TESTS")
    
    try:
        # Add src to path
        project_root = Path.cwd()
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        print("1. Testing data service...")
        from interface.data_service import DataService
        data_service = DataService()
        section = data_service.get_sample_section()
        trains = data_service.get_sample_trains()
        print(f"   ✅ Created {len(trains)} trains in section with {len(section.track_segments)} segments")
        
        print("2. Testing optimization engine...")
        from optimization.optimizer import OptimizationEngine
        optimizer = OptimizationEngine(section)
        result = optimizer.optimize(trains)
        print(f"   ✅ Optimization completed: {result['status']}")
        
        print("3. Testing Flask app creation...")
        from interface.app import create_app
        app = create_app()
        print(f"   ✅ Flask app created successfully")
        
        print("✅ All basic functionality tests passed!")
        
    except Exception as e:
        print(f"❌ Functionality test failed: {e}")
        import traceback
        traceback.print_exc()

def test_scripts():
    print_header("SCRIPT TESTS")
    
    scripts = ['run_tests.py', 'run_app.py']
    
    for script in scripts:
        if not os.path.exists(script):
            print(f"❌ {script} - NOT FOUND")
            continue
            
        print(f"Testing {script}...")
        try:
            # Test import without running
            result = subprocess.run([
                sys.executable, '-c', 
                f'exec(open("{script}").read().split("if __name__")[0]); print("Import OK")'
            ], capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                print(f"   ✅ {script} - Import test passed")
            else:
                print(f"   ❌ {script} - Import test failed:")
                print(f"      Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"   ⏰ {script} - Timeout (may be waiting for input)")
        except Exception as e:
            print(f"   ❌ {script} - Test error: {e}")

def provide_solutions():
    print_header("SOLUTIONS & NEXT STEPS")
    
    print("🚀 Quick Start Commands:")
    print("   python3 run_tests.py       # Test core functionality")
    print("   python3 run_app.py         # Start web interface")
    print("   python3 launch.py          # Interactive launcher")
    
    print("\n🔧 If you have issues:")
    print("   1. Install dependencies:   pip3 install -r requirements.txt")
    print("   2. Check Python version:   python3 --version  (needs 3.9+)")
    print("   3. Verify directory:       ls -la  (should see run_*.py files)")
    print("   4. Check permissions:      chmod +x *.py")
    
    print("\n📞 Common Problems:")
    print("   - Import errors → Run from railway_traffic_control directory")
    print("   - Module not found → Install requirements.txt")
    print("   - Permission denied → chmod +x run_app.py")
    print("   - Port in use → Change port in .env file")
    
    print("\n✅ Success Indicators:")
    print("   - run_tests.py shows '🎉 All tests completed successfully!'")
    print("   - run_app.py shows '📍 Running on http://127.0.0.1:5000'")
    print("   - Browser at http://127.0.0.1:5000 shows dashboard")

def main():
    print("🚂 RAILWAY TRAFFIC CONTROL SYSTEM - DIAGNOSTIC")
    print("This script will help identify any issues with your setup")
    
    check_python()
    check_dependencies()
    check_project_structure()
    test_imports()
    test_basic_functionality()
    test_scripts()
    provide_solutions()
    
    print(f"\n{'='*60}")
    print("🎯 DIAGNOSIS COMPLETE")
    print(f"{'='*60}")
    print("If all tests above show ✅, your system should work!")
    print("If you see ❌ errors, follow the solutions provided above.")

if __name__ == "__main__":
    main()
