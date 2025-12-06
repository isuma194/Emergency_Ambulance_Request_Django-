#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from core.models import User

# Create Dispatcher user
dispatcher_data = {
    'username': 'dispatcher',
    'password': 'dispatcher123',
    'email': 'dispatcher@test.com',
    'first_name': 'John',
    'last_name': 'Dispatcher',
    'role': 'dispatcher',
}

# Create Paramedic user
paramedic_data = {
    'username': 'paramedic',
    'password': 'paramedic123',
    'email': 'paramedic@test.com',
    'first_name': 'Jane',
    'last_name': 'Paramedic',
    'role': 'paramedic',
}

users_to_create = [
    ('dispatcher', dispatcher_data),
    ('paramedic', paramedic_data),
]

for username, data in users_to_create:
    password = data.pop('password')
    try:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': data['email'],
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'role': data['role'],
            }
        )
        user.set_password(password)
        user.save()
        print(f"✓ {data['role'].title()} user created: {username}")
        print(f"  Password: {password}\n")
    except Exception as e:
        print(f"✗ Error creating {username}: {str(e)}\n")

print("\n" + "="*50)
print("ALL LOGIN CREDENTIALS:")
print("="*50)
print("\n1. ADMIN")
print("   Username: admin")
print("   Password: admin123")
print("\n2. DISPATCHER")
print("   Username: dispatcher")
print("   Password: dispatcher123")
print("\n3. PARAMEDIC")
print("   Username: paramedic")
print("   Password: paramedic123")
print("\n" + "="*50)
