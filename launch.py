#!/usr/bin/env python3
"""
Launch script for Railway Traffic Control System MVP
Provides easy setup, testing, and demonstration capabilities
"""

import sys
import os
import subprocess
import time
import webbrowser
from pathlib import Path

def print_header():
    """Print welcome header"""
    print("=" * 70)
    print("🚂 RAILWAY TRAFFIC CONTROL SYSTEM - MVP")
    print("AI-Powered Precise Train Traffic Control for Indian Railways")
    print("=" * 70)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import flask
        import pulp
        import numpy
        import pandas
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e.name}")
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def run_tests():
    """Run test scenarios"""
    print("\\n🧪 Running test scenarios...")
    
    try:
        # Change to project directory
        os.chdir(Path(__file__).parent)
        
        # Run our test script instead
        result = subprocess.run([
            sys.executable, "run_tests.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All test scenarios completed successfully")
            print("\\n📊 Test Results Preview:")
            # Show last few lines of output
            lines = result.stdout.split('\\n')
            for line in lines[-10:]:
                if line.strip():
                    print(f"  {line}")
        else:
            print("❌ Some tests failed:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Error running tests: {str(e)}")

def start_web_server():
    """Start the web server"""
    print("\\n🌐 Starting web interface...")
    print("📍 Dashboard will be available at: http://127.0.0.1:5000")
    print("⏳ Server is starting...")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open("http://127.0.0.1:5000")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start Flask app with proper path setup
    try:
        # Add src to path
        project_root = Path(__file__).parent
        src_path = project_root / "src"
        sys.path.insert(0, str(src_path))
        
        from interface.app import main
        main()
    except KeyboardInterrupt:
        print("\\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {str(e)}")

def show_menu():
    """Show main menu"""
    print("\\n📋 What would you like to do?")
    print("1. 🧪 Run test scenarios only")
    print("2. 🌐 Start web interface only") 
    print("3. 🚀 Run tests and start web interface")
    print("4. 📖 Show project information")
    print("5. 🚪 Exit")
    
    choice = input("\\nEnter your choice (1-5): ").strip()
    return choice

def show_project_info():
    """Show project information"""
    print("\\n📖 PROJECT INFORMATION")
    print("-" * 50)
    print("🎯 Purpose: AI-powered train traffic optimization")
    print("🏗️ Architecture: Flask web app + optimization engine")
    print("📊 Features: Conflict detection, priority scheduling, real-time recommendations")
    print("🧪 Test Scenarios: High congestion, platform bottleneck, express priority")
    print("\\n📁 Key Files:")
    print("  - src/models/: Data models (Train, Section, etc.)")
    print("  - src/optimization/: AI algorithms and engines")
    print("  - src/interface/: Web dashboard and API")
    print("  - data/sample/: Test scenarios and sample data")
    print("\\n🔗 Quick Commands:")
    print("  - Test scenarios: python data/sample/sample_scenarios.py")
    print("  - Web interface: python -m src.interface.app")
    print("  - API endpoint: http://127.0.0.1:5000/api/trains")

def main():
    """Main launcher function"""
    print_header()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies. Please install manually.")
        return
    
    while True:
        choice = show_menu()
        
        if choice == "1":
            run_tests()
        elif choice == "2":
            start_web_server()
        elif choice == "3":
            run_tests()
            input("\\n⏸️  Press Enter to start the web interface...")
            start_web_server()
        elif choice == "4":
            show_project_info()
        elif choice == "5":
            print("\\n👋 Thank you for using Railway Traffic Control System!")
            print("🚂 Making Indian Railways more efficient, one optimization at a time.")
            break
        else:
            print("❌ Invalid choice. Please enter 1-5.")
        
        if choice in ["2", "3"]:
            break
        
        input("\\n⏸️  Press Enter to continue...")

if __name__ == "__main__":
    main()
