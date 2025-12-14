py#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from core.models import User

# Create users one by one
try:
    User.objects.filter(username='dispatcher').delete()
    u1 = User.objects.create_user(username='dispatcher', password='dispatcher123', email='dispatcher@test.com', role='dispatcher', is_staff=True)
    print("Dispatcher OK")
except Exception as e:
    print(f"Dispatcher error: {e}")

try:
    User.objects.filter(username='paramedic').delete()
    u2 = User.objects.create_user(username='paramedic', password='paramedic123', email='paramedic@test.com', role='paramedic', is_staff=True)
    print("Paramedic OK")
except Exception as e:
    print(f"Paramedic error: {e}")

try:
    User.objects.filter(username='admin').delete()
    u3 = User.objects.create_superuser(username='admin', password='admin123', email='admin@test.com')
    u3.role = 'admin'
    u3.save()
    print("Admin OK")
except Exception as e:
    print(f"Admin error: {e}")

print("Done!")
