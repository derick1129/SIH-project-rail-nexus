#!/usr/bin/env python3
"""
Simple script to run the Railway Traffic Control web application
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))

# Now we can import and run the app
if __name__ == "__main__":
    try:
        from interface.app import main
        print("🚂 Starting Railway Traffic Control System...")
        print("📁 Project root:", project_root)
        print("🐍 Python path includes:", src_path)
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running from the project root directory")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
