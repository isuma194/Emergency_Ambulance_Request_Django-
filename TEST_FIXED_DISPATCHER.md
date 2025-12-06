# Test the Fixed Dispatcher

## Server is Running
- URL: http://127.0.0.1:8000/
- Ready for dispatch testing

## Key Fix Applied
✅ **paramedic_id is now optional** - Can be null or omitted
- Changed `paramedic_id` to `required=False, allow_null=True`
- Updated dispatch view to handle None/null paramedic gracefully
- Added checks to skip paramedic assignment if not provided

## How to Test Now

### Option 1: Dispatch WITHOUT Paramedic (RECOMMENDED)
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 1,
    "ambulance_id": 1,
    "hospital_id": 1
  }'
```

### Option 2: Dispatch WITH Paramedic
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 1,
    "ambulance_id": 1,
    "paramedic_id": 1,
    "hospital_id": 1
  }'
```

### Option 3: Dispatch WITH OPTIONAL Hospital (Hospital can also be omitted)
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 1,
    "ambulance_id": 1
  }'
```

## Required vs Optional Fields

| Field | Required | Notes |
|-------|----------|-------|
| emergency_call_id | ✅ YES | Must be in RECEIVED status |
| ambulance_id | ✅ YES | Must be AVAILABLE status |
| paramedic_id | ❌ NO | Can be null or omitted |
| hospital_id | ❌ NO | Can be null or omitted |

## Expected Success Response (200 OK)
```json
{
  "message": "Ambulance dispatched successfully",
  "emergency_call": {
    "id": 1,
    "status": "DISPATCHED",
    "assigned_ambulance": 1
  },
  "ambulance": {
    "id": 1,
    "status": "EN_ROUTE",
    "unit_number": "AMB001"
  }
}
```

## Error Responses

| Error | Status | Cause |
|-------|--------|-------|
| Emergency call not found | 404 | Invalid emergency_call_id |
| Ambulance not found | 404 | Invalid ambulance_id |
| Ambulance is not available | 400 | Ambulance already assigned |
| Emergency call must be in RECEIVED status | 400 | Emergency already dispatched |
| Paramedic not found | 404 | Invalid paramedic_id (if provided) |
| Only dispatchers can dispatch | 403 | Wrong user role |

## Quick Test Steps

1. Check available ambulances:
```bash
curl http://127.0.0.1:8000/dispatch/api/ambulances/
```

2. Check emergency calls:
```bash
curl http://127.0.0.1:8000/emergencies/api/calls/
```

3. Dispatch without paramedic (SIMPLEST TEST):
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/ \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 1,
    "ambulance_id": 1
  }'
```

## Fixes Applied

✅ Serializer now allows null paramedic_id  
✅ View now handles null paramedic gracefully  
✅ Ambulance assignment works without paramedic  
✅ Emergency still gets dispatcher info  
✅ Hospital is optional  

## Try This Now

Try the dispatch without paramedic - it should now work!
