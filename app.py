"""
Entry point for Render deployment.
This file serves as an alternative entry point for deployment platforms.
"""
import subprocess
import sys
import os

if __name__ == "__main__":
    # Get port from environment variable (Render provides this)
    port = os.environ.get("PORT", "8501")
    
    # Run Streamlit with proper configuration for Render
    cmd = [
        sys.executable, "-m", "streamlit", "run",
        "main_web.py",
        "--server.port", port,
        "--server.address", "0.0.0.0",
        "--server.headless", "true",
        "--server.enableCORS", "false",
        "--server.enableXsrfProtection", "false"
    ]
    
    subprocess.run(cmd)

