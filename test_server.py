#!/usr/bin/env python3
"""
Simple test server to diagnose issues
"""

from flask import Flask
import sys
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>🎉 AdinavAI Test Server Working!</h1>
    <p>If you can see this, the server is running correctly.</p>
    <p>Python version: {}</p>
    <p>Flask is working!</p>
    <p><a href="/test">Test page</a></p>
    '''.format(sys.version)

@app.route('/test')
def test():
    return '<h2>Test page working!</h2><p><a href="/">Back to home</a></p>'

if __name__ == '__main__':
    print("=== AdinavAI Test Server ===")
    print("Testing basic Flask functionality...")
    
    # Try different ports
    ports = [8080, 5000, 3000, 8000, 8888]
    
    for port in ports:
        try:
            print(f"\\nTrying port {port}...")
            print(f"Access at: http://localhost:{port}")
            app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False)
            break
        except OSError as e:
            print(f"Port {port} failed: {e}")
            continue
    else:
        print("All ports failed!")