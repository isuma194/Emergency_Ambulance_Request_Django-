#!/usr/bin/env python
"""
Restart Django server with proper logging
"""
import subprocess
import sys
import os

print("=" * 70)
print("🔄 RESTARTING DJANGO SERVER WITH ENHANCED LOGGING")
print("=" * 70)
print()

# Change to project directory
project_dir = r"c:\Users\CENTRAL UNIVERSITY\Documents\GitHub\Emergency_Ambulance_Request_Django-"
os.chdir(project_dir)

print("📍 Working Directory:", os.getcwd())
print()

# Kill existing Python processes (optional)
print("🛑 Stopping any existing Django servers...")
try:
    subprocess.run(["taskkill", "/F", "/IM", "python.exe"], 
                   capture_output=True, timeout=5)
    print("  ✓ Existing servers stopped")
except:
    print("  ⚠ No existing servers to stop")

print()
print("=" * 70)
print("🚀 STARTING DJANGO SERVER")
print("=" * 70)
print()
print("📝 Server logs will appear below:")
print("   - Look for WebSocket connection messages")
print("   - Watch for 'send_initial_data()' calls")
print("   - Check for any ERROR messages")
print()
print("-" * 70)
print()

# Start Django server
subprocess.run([sys.executable, "manage.py", "runserver", "0.0.0.0:8000"])
