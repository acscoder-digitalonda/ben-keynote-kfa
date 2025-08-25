#!/usr/bin/env python3
"""
Streamlit launcher for Keynote KFA
"""
import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    # Change to the project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Run streamlit
    cmd = [sys.executable, "-m", "streamlit", "run", "app.py"]
    
    print("🚀 Starting Keynote KFA Streamlit App...")
    print(f"📁 Project directory: {project_dir}")
    print(f"🌐 App will be available at: http://localhost:8501")
    print("=" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Shutting down Keynote KFA...")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()