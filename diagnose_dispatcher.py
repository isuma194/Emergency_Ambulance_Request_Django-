"""
Diagnostic script for Dispatcher Dashboard issues.
Run this script to check common configuration problems.

Usage: python diagnose_dispatcher.py
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.contrib.auth import get_user_model
from emergencies.models import EmergencyCall
from dispatch.models import Ambulance, Hospital
from django.conf import settings

User = get_user_model()

def check_separator(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_users():
    """Check if dispatcher users exist and are properly configured"""
    check_separator("CHECKING DISPATCHER USERS")
    
    dispatchers = User.objects.filter(is_dispatcher=True)
    
    if dispatchers.count() == 0:
        print("❌ ERROR: No dispatcher users found!")
        print("   Create a dispatcher user with: python manage.py createsuperuser")
        print("   Then set is_dispatcher=True in admin panel or shell")
        return False
    
    print(f"✅ Found {dispatchers.count()} dispatcher user(s):")
    for d in dispatchers:
        print(f"   • {d.username} (ID: {d.id}, Role: {d.role})")
        print(f"     - is_dispatcher: {d.is_dispatcher}")
        print(f"     - is_active: {d.is_active}")
        print(f"     - is_staff: {d.is_staff}")
    
    return True

def check_data():
    """Check if there is any emergency data to display"""
    check_separator("CHECKING EMERGENCY DATA")
    
    emergencies = EmergencyCall.objects.all()
    active_emergencies = EmergencyCall.objects.filter(
        status__in=['RECEIVED', 'DISPATCHED', 'EN_ROUTE', 'ON_SCENE', 'TRANSPORTING']
    )
    
    print(f"Total emergencies: {emergencies.count()}")
    print(f"Active emergencies: {active_emergencies.count()}")
    
    if emergencies.count() == 0:
        print("ℹ️  No emergency calls in database")
        print("   Create test data with: python manage.py setup_sample_data")
    else:
        print(f"✅ Emergency data available")
        for e in active_emergencies[:5]:
            print(f"   • {e.call_id} - {e.emergency_type} ({e.status})")
    
    return True

def check_ambulances():
    """Check ambulance fleet"""
    check_separator("CHECKING AMBULANCE FLEET")
    
    ambulances = Ambulance.objects.all()
    available = Ambulance.objects.filter(status='AVAILABLE')
    
    print(f"Total ambulances: {ambulances.count()}")
    print(f"Available ambulances: {available.count()}")
    
    if ambulances.count() == 0:
        print("ℹ️  No ambulances in database")
        print("   Create test ambulances with: python create_test_ambulances.py")
    else:
        print(f"✅ Ambulance data available")
        for a in ambulances:
            print(f"   • Unit {a.unit_number} - {a.status}")
    
    return True

def check_hospitals():
    """Check hospital data"""
    check_separator("CHECKING HOSPITALS")
    
    hospitals = Hospital.objects.all()
    
    print(f"Total hospitals: {hospitals.count()}")
    
    if hospitals.count() == 0:
        print("ℹ️  No hospitals in database")
        print("   Create hospitals with: python create_hospitals.py")
    else:
        print(f"✅ Hospital data available")
        for h in hospitals:
            print(f"   • {h.name} - Capacity: {h.emergency_capacity}")
    
    return True

def check_channel_layer():
    """Check if channel layer is configured"""
    check_separator("CHECKING CHANNEL LAYER CONFIGURATION")
    
    try:
        from channels.layers import get_channel_layer
        
        channel_layer = get_channel_layer()
        
        if channel_layer is None:
            print("❌ ERROR: Channel layer is not configured!")
            print("   Check CHANNEL_LAYERS in settings.py")
            return False
        
        backend = settings.CHANNEL_LAYERS['default']['BACKEND']
        print(f"✅ Channel layer configured: {backend}")
        
        if 'InMemory' in backend:
            print("   ℹ️  Using in-memory channel layer (Redis not available)")
            print("   This is OK for development but may have limitations")
        elif 'Redis' in backend:
            print("   ✅ Using Redis channel layer (production-ready)")
            
            # Test Redis connection
            try:
                import redis
                r = redis.Redis(host='127.0.0.1', port=6379, socket_connect_timeout=1)
                r.ping()
                print("   ✅ Redis connection successful")
            except Exception as e:
                print(f"   ⚠️  Warning: Could not connect to Redis: {e}")
                print("   The system will fall back to in-memory channel layer")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR checking channel layer: {e}")
        return False

def check_asgi():
    """Check ASGI configuration"""
    check_separator("CHECKING ASGI CONFIGURATION")
    
    asgi_app = getattr(settings, 'ASGI_APPLICATION', None)
    
    if not asgi_app:
        print("❌ ERROR: ASGI_APPLICATION not set in settings.py!")
        return False
    
    print(f"✅ ASGI_APPLICATION: {asgi_app}")
    
    # Try to import the ASGI application
    try:
        from EmmergencyAmbulanceSystem.asgi import application
        print("✅ ASGI application imports successfully")
        
        # Check if WebSocket routing is configured
        from emergencies.routing import websocket_urlpatterns
        print(f"✅ WebSocket routing configured: {len(websocket_urlpatterns)} route(s)")
        for pattern in websocket_urlpatterns:
            print(f"   • {pattern.pattern}")
        
        return True
    except Exception as e:
        print(f"❌ ERROR importing ASGI application: {e}")
        return False

def check_permissions():
    """Check if any users have dispatcher permissions"""
    check_separator("CHECKING USER PERMISSIONS")
    
    all_users = User.objects.all()
    
    print(f"Total users in database: {all_users.count()}")
    print("\nUser roles breakdown:")
    
    for role in ['ADMIN', 'DISPATCHER', 'PARAMEDIC']:
        role_users = all_users.filter(role=role)
        print(f"  {role}: {role_users.count()}")
    
    # Check for users with is_dispatcher flag
    dispatcher_flag_users = all_users.filter(is_dispatcher=True)
    print(f"\nUsers with is_dispatcher=True: {dispatcher_flag_users.count()}")
    
    if dispatcher_flag_users.count() == 0:
        print("\n❌ CRITICAL: No users have is_dispatcher=True!")
        print("   This will prevent WebSocket connections from working.")
        print("\nTo fix this, run in Django shell:")
        print("   python manage.py shell")
        print("   >>> from core.models import User")
        print("   >>> user = User.objects.get(username='your_username')")
        print("   >>> user.is_dispatcher = True")
        print("   >>> user.save()")
        return False
    
    print("✅ Dispatcher permissions configured correctly")
    return True

def check_static_files():
    """Check if static files are configured"""
    check_separator("CHECKING STATIC FILES")
    
    static_url = getattr(settings, 'STATIC_URL', None)
    static_root = getattr(settings, 'STATIC_ROOT', None)
    staticfiles_dirs = getattr(settings, 'STATICFILES_DIRS', [])
    
    print(f"STATIC_URL: {static_url}")
    print(f"STATIC_ROOT: {static_root}")
    print(f"STATICFILES_DIRS: {staticfiles_dirs}")
    
    # Check if scripts.js exists
    for static_dir in staticfiles_dirs:
        scripts_js = os.path.join(static_dir, 'js', 'scripts.js')
        if os.path.exists(scripts_js):
            print(f"✅ Found scripts.js at: {scripts_js}")
            return True
    
    print("⚠️  Warning: scripts.js not found in STATICFILES_DIRS")
    print("   Run: python manage.py collectstatic")
    
    return True

def main():
    """Run all diagnostic checks"""
    print("\n" + "="*70)
    print("  DISPATCHER DASHBOARD DIAGNOSTIC TOOL")
    print("  This script checks for common configuration issues")
    print("="*70)
    
    checks = [
        ("User Permissions", check_permissions),
        ("Dispatcher Users", check_users),
        ("Emergency Data", check_data),
        ("Ambulance Fleet", check_ambulances),
        ("Hospitals", check_hospitals),
        ("Channel Layer", check_channel_layer),
        ("ASGI Configuration", check_asgi),
        ("Static Files", check_static_files),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ ERROR in {name} check: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    check_separator("DIAGNOSTIC SUMMARY")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    print(f"\nChecks passed: {passed}/{total}")
    print("\nResults:")
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    if passed == total:
        print("\n✅ All checks passed! Your dispatcher dashboard should work correctly.")
        print("\nNext steps:")
        print("  1. Start the server with: python manage.py runserver")
        print("  2. Login as a dispatcher user")
        print("  3. Navigate to the dispatcher dashboard")
        print("  4. Check the browser console (F12) for any errors")
    else:
        print("\n⚠️  Some checks failed. Please review the errors above and fix them.")
        print("\nCommon fixes:")
        print("  1. Create dispatcher users and set is_dispatcher=True")
        print("  2. Run: python manage.py setup_sample_data")
        print("  3. Run: python manage.py collectstatic")
        print("  4. Ensure Redis is running (or use in-memory channel layer)")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
