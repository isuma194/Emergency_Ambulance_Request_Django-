#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from emergencies.models import EmergencyCall
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*60)
print("EMERGENCY SYSTEM DIAGNOSTIC")
print("="*60)

# Check emergencies
print("\n📋 EMERGENCIES:")
emergencies = EmergencyCall.objects.all().order_by('-created_at')[:10]
print(f"Total: {EmergencyCall.objects.count()}")
for e in emergencies:
    print(f"  • {e.call_id:20} | Status: {e.status:12} | Type: {e.emergency_type}")

# Check users
print("\n👥 USERS:")
users = User.objects.all()
print(f"Total: {users.count()}")
for u in users:
    print(f"  • {u.username:20} | Role: {getattr(u, 'role', 'N/A')}")

# Check pending emergencies (what dispatcher should see)
print("\n⚠️  PENDING EMERGENCIES (for dispatcher):")
pending = EmergencyCall.objects.filter(status='RECEIVED')
print(f"Total: {pending.count()}")
for e in pending[:5]:
    print(f"  • {e.call_id:20} | Location: {e.location_address}")

print("\n" + "="*60)
