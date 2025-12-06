# Quick Start: Ambulance Dispatch

## System Requirements

- Python 3.9+
- Django 5.2.6+
- Django REST Framework
- PostgreSQL or SQLite (included)

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py migrate
```

### 3. Create a Dispatcher User

```bash
python manage.py shell
```

Then run:
```python
from django.contrib.auth import get_user_model
User = get_user_model()

dispatcher = User.objects.create_user(
    username='dispatcher1',
    password='password123',
    first_name='John',
    last_name='Dispatcher',
    role='dispatcher'
)

paramedic = User.objects.create_user(
    username='paramedic1',
    password='password123',
    first_name='Jane',
    last_name='Paramedic',
    role='paramedic'
)

print(f"Created dispatcher: {dispatcher.username}")
print(f"Created paramedic: {paramedic.username}")
```

### 4. Create Ambulances and Hospitals

```python
from dispatch.models import Ambulance, Hospital

ambulance = Ambulance.objects.create(
    unit_number='AMB001',
    unit_type='BASIC',
    status='AVAILABLE',
    current_latitude=8.4606,
    current_longitude=-13.2317,
    max_patients=2
)

hospital = Hospital.objects.create(
    name='Central Hospital',
    address='123 Hospital St',
    latitude=8.4650,
    longitude=-13.2280,
    phone_number='07654321',
    total_beds=100,
    available_beds=20
)

print(f"Created ambulance: {ambulance.unit_number}")
print(f"Created hospital: {hospital.name}")
```

### 5. Start the Server

```bash
python manage.py runserver
```

Server will be available at: `http://localhost:8000`

## How to Dispatch an Ambulance

### Via API (REST)

**1. Authenticate**
```bash
curl -X POST http://localhost:8000/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "dispatcher1", "password": "password123"}'
```

**2. Create an Emergency Call**
```bash
curl -X POST http://localhost:8000/emergencies/api/calls/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "caller_name": "John Smith",
    "caller_phone": "07654321",
    "emergency_type": "CARDIAC",
    "description": "Patient experiencing severe chest pain",
    "location_address": "22 Peace Village",
    "latitude": "8.4606",
    "longitude": "-13.2317",
    "priority": "HIGH"
  }'
```

Response will include `"id": 1`

**3. Dispatch an Ambulance**
```bash
curl -X POST http://localhost:8000/dispatch/api/dispatch/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 1,
    "ambulance_id": 1,
    "paramedic_id": 1,
    "hospital_id": 1
  }'
```

**Success Response:**
```json
{
  "message": "Ambulance dispatched successfully",
  "emergency_call": {
    "id": 1,
    "call_id": "CALL-XXXXXXXX",
    "status": "DISPATCHED",
    "assigned_ambulance": 1,
    "assigned_paramedic": 1,
    "hospital_destination": "Central Hospital",
    "dispatched_at": "2025-12-03T13:53:42.912406Z"
  },
  "ambulance": {
    "id": 1,
    "unit_number": "AMB001",
    "status": "EN_ROUTE",
    "assigned_paramedic": 1
  }
}
```

### Via Web Dashboard

1. Navigate to dispatcher dashboard
2. View pending emergency calls
3. Click "Dispatch" on an emergency
4. Select an available ambulance
5. Assign a paramedic (optional)
6. Select destination hospital (optional)
7. Click "Dispatch"

## Valid Status Transitions

### Ambulance Status
- AVAILABLE → EN_ROUTE (when dispatched)
- EN_ROUTE → ON_SCENE
- ON_SCENE → TRANSPORTING
- TRANSPORTING → AVAILABLE (at hospital)
- Any → MAINTENANCE (can be set manually)
- Any → OUT_OF_SERVICE (can be set manually)

### Emergency Status
- RECEIVED → DISPATCHED (when ambulance dispatched)
- DISPATCHED → EN_ROUTE (when ambulance en route)
- EN_ROUTE → ON_SCENE
- ON_SCENE → TRANSPORTING
- TRANSPORTING → AT_HOSPITAL
- AT_HOSPITAL → CLOSED

## Phone Number Format

Phone numbers must match the pattern: `^(\+232|0)?[0-9]{8,9}$`

Valid examples:
- `07654321` ✓
- `076543210` ✓
- `+2327654321` ✓
- `+23276543210` ✓

Invalid examples:
- `123` ✗ (too short)
- `+1-234-567-8900` ✗ (wrong format)

## Testing

Run the comprehensive test suite:
```bash
python test_dispatch.py
```

Expected output:
```
================================================================================
AMBULANCE DISPATCH FUNCTIONALITY TEST
================================================================================

[1/6] Setting up test data...
✓ Created dispatcher: dispatcher_test
✓ Created paramedic: paramedic_test
✓ Created ambulance: TESTAMB001 (Status: AVAILABLE)
✓ Created hospital: Test Hospital

✓ ALL TESTS PASSED - DISPATCH FUNCTIONALITY WORKING CORRECTLY
================================================================================
```

## Troubleshooting

### Error: "Ambulance is not available for dispatch"
- **Cause**: Ambulance is already assigned to another emergency
- **Solution**: Select a different ambulance with status AVAILABLE

### Error: "Emergency call must be in RECEIVED status"
- **Cause**: Emergency has already been dispatched
- **Solution**: Create a new emergency call or select a pending emergency

### Error: "Ambulance not found"
- **Cause**: Ambulance ID doesn't exist
- **Solution**: Verify the ambulance ID is correct using GET `/dispatch/api/ambulances/`

### Error: "Only dispatchers can dispatch ambulances"
- **Cause**: User role is not 'dispatcher'
- **Solution**: Use a dispatcher account to dispatch ambulances

### Error: "Hospital not found"
- **Cause**: Hospital ID doesn't exist (optional parameter)
- **Solution**: Either omit hospital_id or verify it exists

## Common Tasks

### List All Available Ambulances
```bash
curl http://localhost:8000/dispatch/api/ambulances/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### List All Hospitals
```bash
curl http://localhost:8000/dispatch/api/hospitals/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### View Emergency Call Details
```bash
curl http://localhost:8000/emergencies/api/calls/1/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Update Ambulance Location
```bash
curl -X POST http://localhost:8000/dispatch/api/ambulances/1/location/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_latitude": "8.4700",
    "current_longitude": "-13.2200"
  }'
```

## Architecture

### Key Components

1. **Dispatcher View** (`dispatch/views.py`)
   - Handles ambulance dispatch logic
   - Validates all inputs
   - Manages database transactions
   - Sends real-time notifications

2. **Ambulance Model** (`dispatch/models.py`)
   - Manages ambulance state
   - Tracks current assignment
   - Updates location

3. **Emergency Model** (`emergencies/models.py`)
   - Tracks emergency lifecycle
   - Records all timestamps
   - Links ambulance and paramedic

4. **WebSocket Consumers** (`emergencies/consumers.py`)
   - Real-time updates to dispatchers
   - Broadcast ambulance status
   - Send emergency notifications

## Security Notes

- Always authenticate before accessing dispatch endpoints
- Only dispatchers can dispatch ambulances
- Ambulances can only be assigned by paramedics assigned to them
- All operations are logged for audit purposes
- Database transactions ensure data consistency

## Support

For issues or questions:
1. Check the error message and this troubleshooting guide
2. Review the DISPATCHER_FIX_REPORT.md for detailed information
3. Check the server logs for detailed error messages
4. Run the test suite to verify system functionality

---

**Version:** 1.0  
**Last Updated:** December 3, 2025  
**Status:** Production Ready ✓
