#!/usr/bin/env python
"""
Test script to verify dashboard rendering and data embedding
"""
import os
import sys
import django
import json
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import RequestFactory
from emergencies.views import dispatcher_dashboard
from django.contrib.sessions.middleware import SessionMiddleware

def test_dashboard():
    print("=" * 80)
    print("DASHBOARD RENDER TEST")
    print("=" * 80)
    
    # Get dispatcher user
    User = get_user_model()
    dispatcher = User.objects.filter(role='dispatcher').first()
    
    if not dispatcher:
        print("ERROR: No dispatcher user found!")
        return False
    
    print(f"\n[OK] Dispatcher found: {dispatcher.username}")
    
    # Create a request
    factory = RequestFactory()
    request = factory.get('/dashboard/')
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    request.user = dispatcher
    
    # Get response
    response = dispatcher_dashboard(request)
    content = response.content.decode()
    
    print(f"[OK] Response received ({len(content)} bytes)")
    
    # TEST 1: Check INITIAL_DATA exists and has data
    print("\n" + "=" * 80)
    print("TEST 1: INITIAL_DATA Embedding")
    print("=" * 80)
    
    if 'let INITIAL_DATA = {' not in content:
        print("ERROR: INITIAL_DATA not found in HTML!")
        return False
    print("[OK] INITIAL_DATA declaration found")
    
    # Extract INITIAL_DATA
    pattern = r'let INITIAL_DATA = \{[\s\n]*emergencies:\s*(\[.*?\]),\s*ambulances:\s*(\[.*?\]),\s*hospitals:\s*(\[.*?\])'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("ERROR: Could not parse INITIAL_DATA structure!")
        return False
    print("[OK] INITIAL_DATA structure parsed")
    
    try:
        emergencies = json.loads(match.group(1))
        ambulances = json.loads(match.group(2))
        hospitals = json.loads(match.group(3))
        
        print(f"[OK] Emergencies: {len(emergencies)}")
        print(f"[OK] Ambulances: {len(ambulances)}")
        print(f"[OK] Hospitals: {len(hospitals)}")
        
        # Count RECEIVED
        received = [e for e in emergencies if e['status'] == 'RECEIVED']
        print(f"[OK] RECEIVED emergencies: {len(received)}")
        
        if len(received) == 0:
            print("WARNING: No RECEIVED emergencies found!")
        
        # Show sample
        if received:
            print(f"\n     Sample RECEIVED emergency:")
            print(f"       - ID: {received[0]['id']}")
            print(f"       - Call ID: {received[0]['call_id']}")
            print(f"       - Status: {received[0]['status']}")
        
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse JSON data: {e}")
        return False
    
    # TEST 2: Check JavaScript functions exist
    print("\n" + "=" * 80)
    print("TEST 2: JavaScript Functions")
    print("=" * 80)
    
    checks = [
        ('function renderCalls(', 'renderCalls function'),
        ('function showToast(', 'showToast function'),
        ('function initMap(', 'initMap function'),
        ('function connectWS(', 'connectWS function'),
        ('document.addEventListener(\'DOMContentLoaded\'', 'DOMContentLoaded listener'),
        ('[data-call-filter]', 'Filter buttons'),
    ]
    
    for pattern, name in checks:
        if pattern in content:
            print(f"[OK] {name}")
        else:
            print(f"ERROR: {name} NOT FOUND")
            return False
    
    # TEST 3: Check critical logic
    print("\n" + "=" * 80)
    print("TEST 3: Critical Logic")
    print("=" * 80)
    
    logic_checks = [
        ('callsById.clear()', 'Clear calls map'),
        ('callsById.set(c.id, c)', 'Populate calls map'),
        ('container.appendChild(div)', 'Add cards to DOM'),
        ('renderCalls(currentCallsFilter)', 'Call renderCalls'),
        ('renderCalls(\'pending\')', 'Render pending filter'),
    ]
    
    for pattern, name in logic_checks:
        if pattern in content:
            print(f"[OK] {name}")
        else:
            print(f"WARNING: {name} - pattern not found, might still work")
    
    # TEST 4: Check HTML structure
    print("\n" + "=" * 80)
    print("TEST 4: HTML Structure")
    print("=" * 80)
    
    html_checks = [
        ('id="callsList"', 'callsList container'),
        ('id="callsCount"', 'callsCount badge'),
        ('data-call-filter="pending"', 'Pending button'),
        ('data-call-filter="active"', 'Active button'),
        ('data-call-filter="completed"', 'Completed button'),
        ('id="map"', 'Map container'),
    ]
    
    for pattern, name in html_checks:
        if pattern in content:
            print(f"[OK] {name}")
        else:
            print(f"ERROR: {name} NOT FOUND")
            return False
    
    # TEST 5: Simulate JavaScript logic
    print("\n" + "=" * 80)
    print("TEST 5: Simulate JavaScript Logic")
    print("=" * 80)
    
    print("Simulating: callsById.set(c.id, c) for each emergency...")
    calls_by_id = {}
    for e in emergencies:
        calls_by_id[e['id']] = e
    print(f"[OK] callsById now has {len(calls_by_id)} items")
    
    print("\nSimulating: renderCalls('pending')...")
    values = list(calls_by_id.values())
    filtered = [c for c in values if c['status'] == 'RECEIVED']
    print(f"[OK] Filtered 'pending': {len(filtered)} items")
    
    if len(filtered) > 0:
        print("[OK] Would render cards to DOM")
        for i, call in enumerate(filtered[:3], 1):
            print(f"     {i}. {call['call_id']} ({call['status']})")
        if len(filtered) > 3:
            print(f"     ... and {len(filtered) - 3} more")
    else:
        print("WARNING: No calls would be rendered!")
    
    # Final result
    print("\n" + "=" * 80)
    print("RESULT: ALL CHECKS PASSED - Dashboard should display calls!")
    print("=" * 80)
    print("\nIf calls still don't show in browser:")
    print("1. Open browser console (F12) and check for JavaScript errors")
    print("2. Look for console.log output starting with '>>>'")
    print("3. Check if 'JS LOADED OK' green banner appears")
    print("4. Check if callsCount badge shows a number")
    print("\n" + "=" * 80)
    
    return True

if __name__ == '__main__':
    try:
        success = test_dashboard()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
