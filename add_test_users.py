#!/usr/bin/env python
"""
Simple script to add test users to the database
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
sys.path.insert(0, os.path.dirname(__file__))

django.setup()

from core.models import User

print("=" * 60)
print("Creating Test Users...")
print("=" * 60)

# Create Dispatcher
try:
    dispatcher, created = User.objects.get_or_create(
        username='dispatcher',
        defaults={
            'email': 'dispatcher@test.com',
            'first_name': 'John',
            'last_name': 'Dispatcher',
            'role': 'dispatcher',
            'is_staff': True,
            'is_active': True,
        }
    )
    dispatcher.set_password('dispatcher123')
    dispatcher.save()
    status = "✓ CREATED" if created else "✓ UPDATED"
    print(f"\n{status}: Dispatcher Account")
    print(f"  Username: dispatcher")
    print(f"  Password: dispatcher123")
except Exception as e:
    print(f"\n✗ ERROR creating dispatcher: {e}")

# Create Paramedic
try:
    paramedic, created = User.objects.get_or_create(
        username='paramedic',
        defaults={
            'email': 'paramedic@test.com',
            'first_name': 'Jane',
            'last_name': 'Paramedic',
            'role': 'paramedic',
            'is_staff': True,
            'is_active': True,
            'is_available_for_dispatch': True,
        }
    )
    paramedic.set_password('paramedic123')
    paramedic.save()
    status = "✓ CREATED" if created else "✓ UPDATED"
    print(f"\n{status}: Paramedic Account")
    print(f"  Username: paramedic")
    print(f"  Password: paramedic123")
except Exception as e:
    print(f"\n✗ ERROR creating paramedic: {e}")

# Create Admin
try:
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'role': 'admin',
            'is_staff': True,
            'is_active': True,
            'is_superuser': True,
        }
    )
    admin.set_password('admin123')
    admin.save()
    status = "✓ CREATED" if created else "✓ UPDATED"
    print(f"\n{status}: Admin Account")
    print(f"  Username: admin")
    print(f"  Password: admin123")
except Exception as e:
    print(f"\n✗ ERROR creating admin: {e}")

print("\n" + "=" * 60)
print("All users ready! You can now log in.")
print("=" * 60)
print("\nAccess the system at:")
print("  Dashboard: http://localhost:8000/dashboard/")
print("  Paramedic: http://localhost:8000/paramedic/")
print("  Admin: http://localhost:8000/admin/")
print("=" * 60)
