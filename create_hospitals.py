#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from dispatch.models import Hospital

# Create test hospitals if they don't exist
hospitals_data = [
    {
        'name': 'Central Medical Hospital',
        'address': '123 Main St, Downtown',
        'latitude': 40.7128,
        'longitude': -74.0060,
        'phone_number': '555-0101',
        'total_beds': 500,
        'available_beds': 45,
        'emergency_capacity': 'MODERATE',
        'specialties': 'Cardiology, Trauma, Neurology, Orthopedics'
    },
    {
        'name': 'St. Johns Emergency Hospital',
        'address': '456 Hospital Blvd, Midtown',
        'latitude': 40.7589,
        'longitude': -73.9851,
        'phone_number': '555-0202',
        'total_beds': 300,
        'available_beds': 12,
        'emergency_capacity': 'HIGH',
        'specialties': 'Trauma, Cardiac, Pediatrics'
    },
    {
        'name': 'Harbor View Medical Center',
        'address': '789 Waterfront Ave, Harborside',
        'latitude': 40.6892,
        'longitude': -74.0445,
        'phone_number': '555-0303',
        'total_beds': 400,
        'available_beds': 156,
        'emergency_capacity': 'LOW',
        'specialties': 'General Surgery, Orthopedics, Respiratory'
    },
    {
        'name': 'Riverside Emergency Center',
        'address': '321 River Road, Southside',
        'latitude': 40.6501,
        'longitude': -73.9496,
        'phone_number': '555-0404',
        'total_beds': 250,
        'available_beds': 0,
        'emergency_capacity': 'FULL',
        'specialties': 'Neurology, Cardiology'
    }
]

created_count = 0
for data in hospitals_data:
    hospital, created = Hospital.objects.get_or_create(
        name=data['name'],
        defaults=data
    )
    if created:
        created_count += 1
        print(f"✓ Created: {hospital.name}")
    else:
        print(f"✗ Already exists: {hospital.name}")

print(f"\n{created_count} new hospitals created")
print(f"Total hospitals: {Hospital.objects.count()}")
