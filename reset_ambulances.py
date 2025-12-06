#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from dispatch.models import Ambulance
from emergencies.models import EmergencyCall

# Reset ambulances to available
ambulances = Ambulance.objects.all()
for amb in ambulances:
    amb.status = 'AVAILABLE'
    amb.current_emergency = None
    amb.assigned_paramedic = None
    amb.save()
    print(f"✓ Reset Unit {amb.unit_number} to AVAILABLE")

print(f"\nTotal available ambulances: {Ambulance.objects.filter(status='AVAILABLE').count()}")

# Create test emergency if needed
emergencies = EmergencyCall.objects.filter(status='RECEIVED')
if not emergencies.exists():
    e = EmergencyCall.objects.create(
        emergency_type='MEDICAL',
        location_address='123 Test St',
        caller_phone='+23210000000',
        patient_name='Test Patient',
        priority='HIGH'
    )
    print(f"✓ Created test emergency: {e.call_id}")
else:
    print(f"✓ Test emergencies exist: {emergencies.count()}")
