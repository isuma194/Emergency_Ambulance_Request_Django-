#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Create test ambulances for dispatcher testing
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from dispatch.models import Ambulance

try:
    print("\n[*] Clearing existing TEST ambulances...")
    deleted_count, _ = Ambulance.objects.filter(unit_number__startswith='TEST').delete()
    print("[OK] Deleted {} existing test ambulances".format(deleted_count))
    
    print("\n[*] Creating new test ambulances...")
    
    ambulances_data = [
        {
            'unit_number': 'TEST-AMB-001',
            'unit_type': 'BASIC',
            'status': 'AVAILABLE',
            'current_latitude': 6.5244,
            'current_longitude': 3.3792,
            'equipment_list': 'Oxygen, Bandages, Stretcher',
            'max_patients': 2
        },
        {
            'unit_number': 'TEST-AMB-002',
            'unit_type': 'ADVANCED',
            'status': 'AVAILABLE',
            'current_latitude': 6.5300,
            'current_longitude': 3.3850,
            'equipment_list': 'Advanced life support equipment',
            'max_patients': 3
        },
        {
            'unit_number': 'TEST-AMB-003',
            'unit_type': 'BASIC',
            'status': 'AVAILABLE',
            'current_latitude': 6.5150,
            'current_longitude': 3.3700,
            'equipment_list': 'Basic equipment',
            'max_patients': 2
        },
        {
            'unit_number': 'TEST-AMB-004',
            'unit_type': 'CRITICAL',
            'status': 'AVAILABLE',
            'current_latitude': 6.5400,
            'current_longitude': 3.3900,
            'equipment_list': 'Critical care equipment',
            'max_patients': 1
        },
    ]
    
    created_count = 0
    for amb_data in ambulances_data:
        amb = Ambulance.objects.create(**amb_data)
        print("[OK] Created ambulance: {} (ID: {}, Status: {})".format(
            amb.unit_number, amb.id, amb.status))
        created_count += 1
    
    print("\n[SUCCESS] Created {} ambulances".format(created_count))
    
    # Show summary
    available = Ambulance.objects.filter(status='AVAILABLE').count()
    total = Ambulance.objects.all().count()
    print("\n[SUMMARY]")
    print("  Total ambulances: {}".format(total))
    print("  Available: {}".format(available))
    print("\n[OK] All ambulances are AVAILABLE for dispatch!")
    
except Exception as e:
    print("[ERROR] {}".format(str(e)))
    import traceback
    traceback.print_exc()
    sys.exit(1)
