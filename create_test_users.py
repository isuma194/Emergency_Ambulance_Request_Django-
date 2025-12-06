#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from core.models import User

# Create Dispatcher
dispatcher, created = User.objects.get_or_create(
    username='dispatcher',
    defaults={
        'email': 'dispatcher@test.com',
        'first_name': 'John',
        'last_name': 'Dispatcher',
        'role': 'dispatcher',
        'is_staff': True,
    }
)
dispatcher.set_password('dispatcher123')
dispatcher.save()
print(f"Dispatcher: dispatcher / dispatcher123 - {'Created' if created else 'Updated'}")

# Create Paramedic
paramedic, created = User.objects.get_or_create(
    username='paramedic',
    defaults={
        'email': 'paramedic@test.com',
        'first_name': 'Jane',
        'last_name': 'Paramedic',
        'role': 'paramedic',
        'is_staff': True,
    }
)
paramedic.set_password('paramedic123')
paramedic.save()
print(f"Paramedic: paramedic / paramedic123 - {'Created' if created else 'Updated'}")

# Create Admin
admin, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@test.com',
        'first_name': 'Admin',
        'last_name': 'User',
        'role': 'admin',
        'is_staff': True,
        'is_superuser': True,
    }
)
admin.set_password('admin123')
admin.save()
print(f"Admin: admin / admin123 - {'Created' if created else 'Updated'}")

print("\n✓ All users created successfully!")
