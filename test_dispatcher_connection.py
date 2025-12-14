"""
Test script to verify dispatcher dashboard connection and authentication
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from core.models import User
from django.contrib.auth import authenticate

print("=" * 60)
print("DISPATCHER CONNECTION DIAGNOSTIC TEST")
print("=" * 60)

# Check if there are any dispatcher users
dispatchers = User.objects.filter(role='dispatcher')
print(f"\n✓ Found {dispatchers.count()} dispatcher(s) in database")

if dispatchers.count() > 0:
    print("\nDispatcher Users:")
    for dispatcher in dispatchers:
        print(f"  - Username: {dispatcher.username}")
        print(f"    Full Name: {dispatcher.get_full_name()}")
        print(f"    Is Active: {dispatcher.is_active}")
        print(f"    Is Dispatcher: {dispatcher.is_dispatcher}")
        print(f"    Role: {dispatcher.role}")
        print()
else:
    print("\n⚠ WARNING: No dispatcher users found!")
    print("Creating a test dispatcher account...")
    
    # Create a test dispatcher
    test_dispatcher = User.objects.create_user(
        username='dispatcher1',
        password='dispatcher123',
        email='dispatcher@ambulance.com',
        first_name='Test',
        last_name='Dispatcher',
        role='dispatcher'
    )
    print(f"✓ Created dispatcher: {test_dispatcher.username}")
    print(f"  Password: dispatcher123")

# Test authentication
print("\n" + "=" * 60)
print("TESTING AUTHENTICATION")
print("=" * 60)

if dispatchers.count() > 0:
    test_user = dispatchers.first()
    print(f"\nTesting with user: {test_user.username}")
    print(f"  Is authenticated: {test_user.is_authenticated}")
    print(f"  Is dispatcher: {test_user.is_dispatcher}")
    print(f"  Has password: {test_user.password != ''}")

# Check WebSocket configuration
print("\n" + "=" * 60)
print("WEBSOCKET CONFIGURATION")
print("=" * 60)

from django.conf import settings

print(f"\nASGI Application: {settings.ASGI_APPLICATION}")
print(f"Channel Layers Backend: {settings.CHANNEL_LAYERS['default']['BACKEND']}")

if 'InMemory' in settings.CHANNEL_LAYERS['default']['BACKEND']:
    print("  ⚠ Using in-memory channel layer (Redis not available)")
else:
    print("  ✓ Using Redis channel layer")

# Check if Daphne is installed
print("\n" + "=" * 60)
print("REQUIRED PACKAGES")
print("=" * 60)

try:
    import daphne
    print(f"✓ Daphne installed: {daphne.__version__}")
except ImportError:
    print("✗ Daphne not installed!")

try:
    import channels
    print(f"✓ Channels installed: {channels.__version__}")
except ImportError:
    print("✗ Channels not installed!")

try:
    import rest_framework
    print(f"✓ Django REST Framework installed: {rest_framework.__version__}")
except ImportError:
    print("✗ Django REST Framework not installed!")

print("\n" + "=" * 60)
print("DISPATCHER DASHBOARD ACCESS")
print("=" * 60)

print("\nTo access the dispatcher dashboard:")
print("1. Start the server: python manage.py runserver")
print("2. Navigate to: http://127.0.0.1:8000/login/")
print("3. Login with a dispatcher account")
print("4. You should be redirected to: http://127.0.0.1:8000/dashboard/")
print("\nCheck your browser's console (F12) for any JavaScript errors.")

if dispatchers.count() > 0:
    print(f"\nTest Credentials:")
    print(f"  Username: {dispatchers.first().username}")
    print(f"  (Use the password you set for this user)")

print("\n" + "=" * 60)
