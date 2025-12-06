#!/usr/bin/env python
import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EmmergencyAmbulanceSystem.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()
client = Client()

print("\n" + "="*70)
print("API ENDPOINT DIAGNOSTICS")
print("="*70)

# Login as dispatcher
dispatcher = User.objects.filter(role='dispatcher').first()
if dispatcher:
    client.force_login(dispatcher)
    print(f"\n✅ Logged in as: {dispatcher.username}")
    
    # Test emergencies API endpoints
    endpoints = [
        '/api/emergencies/active/?status=pending',
        '/api/emergencies/active/?status=active',
        '/api/emergencies/active/?status=completed',
        '/api/emergencies/pending/',
    ]
    
    for endpoint in endpoints:
        print(f"\n🔗 Testing: {endpoint}")
        response = client.get(endpoint)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if isinstance(data, list):
                    print(f"   Results: {len(data)} items")
                    for item in data[:2]:
                        call_id = item.get('call_id', 'N/A')
                        status = item.get('status', 'N/A')
                        print(f"     • {call_id} - {status}")
                else:
                    print(f"   Response type: {type(data).__name__}")
                    print(f"   Keys: {list(data.keys())[:5] if hasattr(data, 'keys') else 'N/A'}")
            except Exception as e:
                print(f"   Error parsing JSON: {e}")
        else:
            print(f"   Error: {response.text[:100]}")

print("\n" + "="*70)
