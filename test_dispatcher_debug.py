"""
Comprehensive Dispatcher Dashboard Debug Script
================================================

This script performs a complete system check to diagnose any issues
with the dispatcher dashboard, WebSocket connections, and data loading.

Run this script to verify your system is working correctly.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.contrib.auth import get_user_model
from emergencies.models import EmergencyCall
from dispatch.models import Ambulance, Hospital
from emergencies.serializers import EmergencyCallSerializer
from dispatch.serializers import AmbulanceSerializer, HospitalSerializer
from django.conf import settings
import json

User = get_user_model()

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_check(passed, message):
    """Print a check result"""
    symbol = "✓" if passed else "✗"
    status = "PASS" if passed else "FAIL"
    color = "\033[92m" if passed else "\033[91m"
    reset = "\033[0m"
    print(f"{color}{symbol} {status}{reset}: {message}")

def test_database_connection():
    """Test database connectivity"""
    print_header("DATABASE CONNECTION TEST")
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            print_check(True, "Database connection successful")
            return True
    except Exception as e:
        print_check(False, f"Database connection failed: {e}")
        return False

def test_user_authentication():
    """Test dispatcher user exists and is properly configured"""
    print_header("USER AUTHENTICATION TEST")
    
    # Check for dispatcher users
    dispatchers = User.objects.filter(role='dispatcher')
    dispatcher_count = dispatchers.count()
    
    print(f"   Total dispatcher users: {dispatcher_count}")
    
    if dispatcher_count == 0:
        print_check(False, "No dispatcher users found!")
        print("   Creating test dispatcher user...")
        try:
            test_user = User.objects.create_user(
                username='dispatcher_test',
                password='test123',
                email='dispatcher@test.com',
                first_name='Test',
                last_name='Dispatcher',
                role='dispatcher'
            )
            print_check(True, f"Test dispatcher created: {test_user.username}")
            print(f"   Username: dispatcher_test")
            print(f"   Password: test123")
        except Exception as e:
            print_check(False, f"Failed to create test user: {e}")
            return False
    else:
        for dispatcher in dispatchers[:3]:
            print(f"   - {dispatcher.username} ({dispatcher.get_full_name()})")
        print_check(True, f"Found {dispatcher_count} dispatcher user(s)")
    
    return True

def test_emergency_data():
    """Test emergency call data and serialization"""
    print_header("EMERGENCY DATA TEST")
    
    # Count emergencies
    all_emergencies = EmergencyCall.objects.all()
    active_emergencies = EmergencyCall.objects.filter(
        status__in=['RECEIVED', 'DISPATCHED', 'EN_ROUTE', 'ON_SCENE', 'TRANSPORTING']
    )
    
    print(f"   Total emergencies: {all_emergencies.count()}")
    print(f"   Active emergencies: {active_emergencies.count()}")
    
    if all_emergencies.count() == 0:
        print_check(False, "No emergency calls in database")
        print("   Run: python manage.py shell -c \"from core.management.commands.setup_sample_data import Command; Command().handle()\"")
        return False
    
    # Test serialization
    try:
        serialized = EmergencyCallSerializer(active_emergencies, many=True).data
        print_check(True, f"Successfully serialized {len(serialized)} emergencies")
        
        # Check data structure
        if len(serialized) > 0:
            sample = serialized[0]
            required_fields = ['id', 'call_id', 'status', 'emergency_type', 'location_address']
            missing_fields = [field for field in required_fields if field not in sample]
            
            if missing_fields:
                print_check(False, f"Missing fields in serialized data: {missing_fields}")
            else:
                print_check(True, "All required fields present in serialized data")
                
                # Show sample
                print(f"\n   Sample emergency:")
                print(f"     - ID: {sample['id']}")
                print(f"     - Call ID: {sample['call_id']}")
                print(f"     - Status: {sample['status']}")
                print(f"     - Type: {sample.get('emergency_type_display', sample['emergency_type'])}")
                print(f"     - Location: {sample['location_address'][:50]}...")
        
        return True
    except Exception as e:
        print_check(False, f"Serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ambulance_data():
    """Test ambulance fleet data and serialization"""
    print_header("AMBULANCE FLEET TEST")
    
    ambulances = Ambulance.objects.all()
    print(f"   Total ambulances: {ambulances.count()}")
    
    if ambulances.count() == 0:
        print_check(False, "No ambulances in database")
        return False
    
    # Test serialization
    try:
        serialized = AmbulanceSerializer(ambulances, many=True).data
        print_check(True, f"Successfully serialized {len(serialized)} ambulances")
        
        if len(serialized) > 0:
            sample = serialized[0]
            print(f"\n   Sample ambulance:")
            print(f"     - ID: {sample['id']}")
            print(f"     - Unit: {sample.get('unit_number', 'N/A')}")
            print(f"     - Status: {sample.get('status_display', sample.get('status', 'Unknown'))}")
        
        return True
    except Exception as e:
        print_check(False, f"Serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_hospital_data():
    """Test hospital data and serialization"""
    print_header("HOSPITAL DATA TEST")
    
    hospitals = Hospital.objects.all()
    print(f"   Total hospitals: {hospitals.count()}")
    
    if hospitals.count() == 0:
        print_check(False, "No hospitals in database")
        return False
    
    # Test serialization
    try:
        serialized = HospitalSerializer(hospitals, many=True).data
        print_check(True, f"Successfully serialized {len(serialized)} hospitals")
        
        if len(serialized) > 0:
            sample = serialized[0]
            print(f"\n   Sample hospital:")
            print(f"     - ID: {sample['id']}")
            print(f"     - Name: {sample.get('name', 'N/A')}")
            print(f"     - Capacity: {sample.get('emergency_capacity_display', sample.get('emergency_capacity', 'Unknown'))}")
        
        return True
    except Exception as e:
        print_check(False, f"Serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_websocket_config():
    """Test WebSocket and ASGI configuration"""
    print_header("WEBSOCKET CONFIGURATION TEST")
    
    # Check ASGI application
    asgi_app = getattr(settings, 'ASGI_APPLICATION', None)
    if asgi_app:
        print_check(True, f"ASGI_APPLICATION: {asgi_app}")
    else:
        print_check(False, "ASGI_APPLICATION not configured")
    
    # Check channel layers
    channel_layers = getattr(settings, 'CHANNEL_LAYERS', {})
    if channel_layers:
        backend = channel_layers.get('default', {}).get('BACKEND', 'Not configured')
        print_check(True, f"Channel Layer Backend: {backend}")
        
        if 'InMemory' in backend:
            print("   ⚠ Using in-memory channel layer (Redis not available)")
            print("   ℹ This is OK for development, but Redis is recommended for production")
        elif 'Redis' in backend:
            print("   ✓ Using Redis channel layer (recommended)")
    else:
        print_check(False, "CHANNEL_LAYERS not configured")
    
    # Check required packages
    packages = ['channels', 'daphne', 'channels_redis']
    for package in packages:
        try:
            __import__(package)
            print_check(True, f"Package '{package}' is installed")
        except ImportError:
            print_check(False, f"Package '{package}' is NOT installed")
            print(f"   Install with: pip install {package}")
    
    return True

def test_json_serialization():
    """Test that all data can be JSON serialized (for WebSocket transmission)"""
    print_header("JSON SERIALIZATION TEST")
    
    try:
        # Get data
        emergencies = EmergencyCallSerializer(
            EmergencyCall.objects.filter(
                status__in=['RECEIVED', 'DISPATCHED', 'EN_ROUTE', 'ON_SCENE', 'TRANSPORTING']
            ), many=True
        ).data
        
        ambulances = AmbulanceSerializer(Ambulance.objects.all(), many=True).data
        hospitals = HospitalSerializer(Hospital.objects.all(), many=True).data
        
        # Try to JSON serialize
        data = {
            'emergencies': emergencies,
            'ambulances': ambulances,
            'hospitals': hospitals
        }
        
        json_str = json.dumps(data)
        json_len = len(json_str)
        
        print_check(True, f"All data successfully JSON serialized ({json_len} bytes)")
        
        # Parse back
        parsed = json.loads(json_str)
        print_check(True, "JSON data successfully parsed back")
        
        return True
    except Exception as e:
        print_check(False, f"JSON serialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all diagnostic tests"""
    print("\n" + "█" * 80)
    print("  DISPATCHER DASHBOARD DIAGNOSTIC TOOL")
    print("  Version 1.0")
    print("█" * 80)
    
    results = []
    
    results.append(("Database Connection", test_database_connection()))
    results.append(("User Authentication", test_user_authentication()))
    results.append(("Emergency Data", test_emergency_data()))
    results.append(("Ambulance Fleet", test_ambulance_data()))
    results.append(("Hospital Data", test_hospital_data()))
    results.append(("WebSocket Config", test_websocket_config()))
    results.append(("JSON Serialization", test_json_serialization()))
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        print_check(result, name)
    
    print(f"\n   Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("\n   ✅ ALL TESTS PASSED! Your system is configured correctly.")
        print("   You can now start the server and access the dispatcher dashboard.")
    else:
        print("\n   ⚠ SOME TESTS FAILED! Please fix the issues above.")
        print("   Check the error messages for guidance.")
    
    print("\n" + "=" * 80)

if __name__ == '__main__':
    run_all_tests()
