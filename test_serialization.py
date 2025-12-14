#!/usr/bin/env python
"""Test emergency serialization"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from emergencies.models import EmergencyCall
from emergencies.serializers import EmergencyCallSerializer

print("Testing emergency serialization...")
print("=" * 60)

# Get RECEIVED calls
calls = EmergencyCall.objects.filter(status='RECEIVED')[:3]
print(f"Found {calls.count()} RECEIVED emergency calls")
print()

for call in calls:
    print(f"  {call.call_id}")
    print(f"    Type: {call.emergency_type}")
    print(f"    Location: {call.location_address[:50]}")
    print()

# Test serialization
try:
    serialized = EmergencyCallSerializer(calls, many=True).data
    print(f"✅ Successfully serialized {len(serialized)} calls")
    
    if serialized:
        import json
        print("\nSample serialized data:")
        print(json.dumps(serialized[0], indent=2)[:800])
except Exception as e:
    print(f"❌ Serialization failed: {e}")
    import traceback
    traceback.print_exc()
