#!/usr/bin/env python
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

django.setup()

from core.models import User

print("Creating test users...")

# Delete existing test users
User.objects.filter(username__in=['dispatcher', 'paramedic', 'admin']).delete()

# Create dispatcher user
dispatcher = User.objects.create_user(
    username='dispatcher',
    password='dispatcher123',
    email='dispatcher@test.com',
    role='dispatcher',
    is_staff=True
)
print(f"✓ Dispatcher created: dispatcher / dispatcher123")

# Create paramedic user
paramedic = User.objects.create_user(
    username='paramedic',
    password='paramedic123',
    email='paramedic@test.com',
    role='paramedic',
    is_staff=True
)
print(f"✓ Paramedic created: paramedic / paramedic123")

# Create admin user
admin = User.objects.create_superuser(
    username='admin',
    password='admin123',
    email='admin@test.com'
)
admin.role = 'admin'
admin.save()
print(f"✓ Admin created: admin / admin123")

print("\n" + "="*50)
print("LOGIN CREDENTIALS")
print("="*50)
print("\n1. DISPATCHER LOGIN:")
print("   Username: dispatcher")
print("   Password: dispatcher123")
print("\n2. PARAMEDIC LOGIN:")
print("   Username: paramedic")
print("   Password: paramedic123")
print("\n3. ADMIN LOGIN:")
print("   Username: admin")
print("   Password: admin123")
print("="*50)
