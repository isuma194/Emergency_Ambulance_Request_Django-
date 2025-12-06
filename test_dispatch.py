#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to verify ambulance dispatch functionality works correctly.
Run with: python manage.py shell < test_dispatch.py
Or: python test_dispatch.py
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
import json

from core.models import User
from dispatch.models import Ambulance, Hospital
from emergencies.models import EmergencyCall

User = get_user_model()

def test_dispatch_workflow():
    """Test the complete ambulance dispatch workflow"""
    
    print("\n" + "="*80)
    print("AMBULANCE DISPATCH FUNCTIONALITY TEST")
    print("="*80)
    
    # Clean up test data
    print("\n[1/6] Setting up test data...")
    User.objects.filter(username__in=['dispatcher_test', 'paramedic_test']).delete()
    Ambulance.objects.filter(unit_number='TESTAMB001').delete()
    Hospital.objects.filter(name='Test Hospital').delete()
    EmergencyCall.objects.filter(call_id__startswith='CALL-TEST').delete()
    
    # Create test dispatcher user
    dispatcher = User.objects.create_user(
        username='dispatcher_test',
        password='test123',
        first_name='Test',
        last_name='Dispatcher',
        role='dispatcher'
    )
    print("[OK] Created dispatcher: {}".format(dispatcher.username))
    
    # Create test paramedic user
    paramedic = User.objects.create_user(
        username='paramedic_test',
        password='test123',
        first_name='Test',
        last_name='Paramedic',
        role='paramedic'
    )
    print("[OK] Created paramedic: {}".format(paramedic.username))
    
    # Create test ambulance
    ambulance = Ambulance.objects.create(
        unit_number='TESTAMB001',
        unit_type='BASIC',
        status='AVAILABLE',
        current_latitude=8.4606,
        current_longitude=-13.2317,
        equipment_list='Basic equipment',
        max_patients=2
    )
    print("[OK] Created ambulance: {} (Status: {})".format(ambulance.unit_number, ambulance.status))
    
    # Create test hospital
    hospital = Hospital.objects.create(
        name='Test Hospital',
        address='123 Hospital St',
        latitude=8.4650,
        longitude=-13.2280,
        phone_number='07654321',
        total_beds=100,
        available_beds=20
    )
    print("[OK] Created hospital: {}".format(hospital.name))
    
    # Create emergency call
    emergency = EmergencyCall.objects.create(
        caller_name='John Doe',
        caller_phone='07654321',
        emergency_type='CARDIAC',
        description='Patient experiencing chest pain',
        location_address='22 Peace Village',
        latitude=8.4606,
        longitude=-13.2317,
        status='RECEIVED',
        priority='HIGH'
    )
    print("[OK] Created emergency call: {} (Status: {})".format(emergency.call_id, emergency.status))
    
    # Test dispatch via API
    print("\n[2/6] Testing dispatch API endpoint...")
    api_client = APIClient()
    
    # Login as dispatcher
    api_client.force_authenticate(user=dispatcher)
    print("[OK] Authenticated as dispatcher")
    
    # Prepare dispatch payload
    dispatch_payload = {
        'emergency_call_id': emergency.id,
        'ambulance_id': ambulance.id,
        'paramedic_id': paramedic.id,
        'hospital_id': hospital.id
    }
    
    print("[OK] Dispatch payload: {}".format(dispatch_payload))
    
    # Send dispatch request
    print("\n[3/6] Sending dispatch request...")
    response = api_client.post(
        '/dispatch/api/dispatch/',
        data=dispatch_payload,
        format='json'
    )
    
    print("Response Status Code: {}".format(response.status_code))
    
    if response.status_code == status.HTTP_200_OK:
        print("[OK] Dispatch request successful!")
    else:
        print("[FAIL] Dispatch request failed with status {}".format(response.status_code))
        print("Error details: {}".format(response.data))
        return False
    
    # Verify ambulance status changed
    print("\n[4/6] Verifying ambulance status...")
    ambulance.refresh_from_db()
    print("Ambulance status: {}".format(ambulance.status))
    print("Ambulance current_emergency: {}".format(ambulance.current_emergency))
    print("Ambulance assigned_paramedic: {}".format(ambulance.assigned_paramedic))
    
    if ambulance.status == 'EN_ROUTE':
        print("[OK] Ambulance status correctly changed to EN_ROUTE")
    else:
        print("[FAIL] Ambulance status is {}, expected EN_ROUTE".format(ambulance.status))
        return False
    
    # Verify emergency call updated
    print("\n[5/6] Verifying emergency call status...")
    emergency.refresh_from_db()
    print("Emergency status: {}".format(emergency.status))
    print("Emergency assigned_ambulance: {}".format(emergency.assigned_ambulance))
    print("Emergency assigned_paramedic: {}".format(emergency.assigned_paramedic))
    print("Emergency dispatcher: {}".format(emergency.dispatcher))
    print("Emergency hospital_destination: {}".format(emergency.hospital_destination))
    
    if emergency.status == 'DISPATCHED':
        print("[OK] Emergency status correctly changed to DISPATCHED")
    else:
        print("[FAIL] Emergency status is {}, expected DISPATCHED".format(emergency.status))
        return False
    
    if emergency.assigned_ambulance == ambulance:
        print("[OK] Emergency correctly linked to ambulance")
    else:
        print("[FAIL] Emergency not linked to ambulance")
        return False
    
    if emergency.assigned_paramedic == paramedic:
        print("[OK] Emergency correctly linked to paramedic")
    else:
        print("[FAIL] Emergency not linked to paramedic")
        return False
    
    if emergency.dispatcher == dispatcher:
        print("[OK] Emergency correctly linked to dispatcher")
    else:
        print("[FAIL] Emergency not linked to dispatcher")
        return False
    
    if emergency.hospital_destination == hospital.name:
        print("[OK] Hospital destination correctly set")
    else:
        print("[FAIL] Hospital destination is {}, expected {}".format(emergency.hospital_destination, hospital.name))
        return False
    
    # Test failure cases
    print("\n[6/6] Testing error handling...")
    
    # Test 1: Try to dispatch unavailable ambulance
    print("\nTest 1: Dispatching unavailable ambulance...")
    emergency2 = EmergencyCall.objects.create(
        caller_name='Jane Doe',
        caller_phone='07654321',
        emergency_type='TRAUMA',
        description='Traffic accident',
        location_address='Main Street',
        latitude=8.4606,
        longitude=-13.2317,
        status='RECEIVED',
        priority='HIGH'
    )
    
    response = api_client.post(
        '/dispatch/api/dispatch/',
        data={
            'emergency_call_id': emergency2.id,
            'ambulance_id': ambulance.id,  # Already assigned
            'paramedic_id': paramedic.id,
        },
        format='json'
    )
    
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        print("[OK] Correctly rejected unavailable ambulance dispatch")
        print("  Error: {}".format(response.data))
    else:
        print("[FAIL] Should have rejected unavailable ambulance (got {})".format(response.status_code))
    
    # Test 2: Non-dispatcher trying to dispatch
    print("\nTest 2: Non-dispatcher attempting dispatch...")
    api_client.force_authenticate(user=paramedic)
    
    response = api_client.post(
        '/dispatch/api/dispatch/',
        data={
            'emergency_call_id': emergency2.id,
            'ambulance_id': ambulance.id,
        },
        format='json'
    )
    
    if response.status_code == status.HTTP_403_FORBIDDEN:
        print("[OK] Correctly rejected non-dispatcher dispatch attempt")
    else:
        print("[FAIL] Should have rejected non-dispatcher (got {})".format(response.status_code))
    
    print("\n" + "="*80)
    print("[SUCCESS] ALL TESTS PASSED - DISPATCH FUNCTIONALITY WORKING CORRECTLY")
    print("="*80 + "\n")
    
    return True

if __name__ == '__main__':
    try:
        test_dispatch_workflow()
    except Exception as e:
        print("\n[FAIL] TEST FAILED WITH ERROR: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        sys.exit(1)
