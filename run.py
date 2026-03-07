import uvicorn
import subprocess
import sys
import threading
import time

def run_api():
    """Run the FastAPI backend."""
    uvicorn.run("app.main:app", host="0.0.0.0", port=8082, log_level="info")

def run_ui():
    """Run the Streamlit frontend."""
    time.sleep(2) # Give the API a moment to start
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py", 
        "--server.port", "8501", 
        "--server.address", "0.0.0.0",
        "--server.enableCORS", "false", 
        "--server.enableXsrfProtection", "false",
        "--browser.gatherUsageStats", "false"
    ])

if __name__ == "__main__":
    print("Starting Miss Writer...")
    print("Starting FastAPI Backend on http://localhost:8082")
    print("Starting Streamlit UI on http://localhost:8501")
    
    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()
    
    # Run UI in the main thread so it stays open
    try:
        run_ui()
    except KeyboardInterrupt:
        print("\nShutting down...")
