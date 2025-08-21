#!/usr/bin/env python3
"""
Simple launcher for AdinavAI Family System
This script will find an available port and start the application
"""

import socket
import subprocess
import sys
import os

def find_free_port():
    """Find a free port to use"""
    for port in [8080, 5000, 3000, 8000, 8888, 9000]:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(('localhost', port))
                return port
            except OSError:
                continue
    return 8080  # fallback

def main():
    print("=== AdinavAI Family System Launcher ===")
    
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Find free port
    port = find_free_port()
    os.environ['PORT'] = str(port)
    
    print(f"Starting AdinavAI on port {port}...")
    print(f"Access on computer: http://localhost:{port}")
    print(f"Access on mobile: http://192.168.1.156:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Launch the main application
        subprocess.run([sys.executable, 'family_app.py'], check=True)
    except KeyboardInterrupt:
        print("\nShutting down AdinavAI...")
    except Exception as e:
        print(f"Error starting application: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements.txt")

if __name__ == "__main__":
    main()