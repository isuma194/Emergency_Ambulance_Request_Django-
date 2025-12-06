#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.contrib.auth import get_user_model
from dispatch.models import Ambulance, Hospital
from emergencies.models import EmergencyCall

User = get_user_model()

print("=" * 60)
print("DATABASE CHECK")
print("=" * 60)

print(f"\nTotal Users: {User.objects.count()}")
print("Users:")
for u in User.objects.all():
    role = getattr(u, 'role', 'N/A')
    print(f"  - {u.username:20} | Role: {role:12} | Active: {u.is_active}")

print(f"\nTotal Ambulances: {Ambulance.objects.count()}")
print("Ambulances:")
for a in Ambulance.objects.all():
    print(f"  - Unit {a.unit_number:5} | Status: {a.status:15} | Paramedic: {a.assigned_paramedic or 'None'}")

print(f"\nTotal Hospitals: {Hospital.objects.count()}")
print("Hospitals:")
for h in Hospital.objects.all():
    print(f"  - {h.name:30} | Capacity: {h.emergency_capacity}")

print(f"\nTotal Emergencies: {EmergencyCall.objects.count()}")
print("Recent Emergencies:")
for e in EmergencyCall.objects.all().order_by('-created_at')[:5]:
    print(f"  - {e.call_id:15} | Status: {e.status:15} | Type: {e.emergency_type}")

print("\n" + "=" * 60)
