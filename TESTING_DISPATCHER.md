# 🚑 Dispatcher Testing Guide

## Server Status
✅ **Server Running:** http://127.0.0.1:8000/

---

## Quick Test Steps

### 1. **Login as Dispatcher**
```bash
POST http://127.0.0.1:8000/login/
Content-Type: application/json

{
  "username": "dispatcher1",
  "password": "password123"
}
```

### 2. **View Available Ambulances**
```bash
GET http://127.0.0.1:8000/dispatch/api/ambulances/
Authorization: Bearer YOUR_TOKEN
```

### 3. **View Hospitals**
```bash
GET http://127.0.0.1:8000/dispatch/api/hospitals/
Authorization: Bearer YOUR_TOKEN
```

### 4. **View Emergency Calls**
```bash
GET http://127.0.0.1:8000/emergencies/api/calls/
Authorization: Bearer YOUR_TOKEN
```

### 5. **Dispatch an Ambulance**
```bash
POST http://127.0.0.1:8000/dispatch/api/dispatch/
Authorization: Bearer YOUR_TOKEN
Content-Type: application/json

{
  "emergency_call_id": 1,
  "ambulance_id": 1,
  "paramedic_id": 1,
  "hospital_id": 1
}
```

---

## Test Data Already Available

From the earlier test run, you have:
- **Dispatcher:** dispatcher_test / test123
- **Paramedic:** paramedic_test / test123
- **Ambulance:** TESTAMB001 (Unit ID: 6, Status: AVAILABLE)
- **Hospital:** Test Hospital (ID: 6)
- **Emergency:** CALL-44C65DC8 (ID: 43)

---

## Key API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/dispatch/api/ambulances/` | List all ambulances |
| POST | `/dispatch/api/ambulances/` | Create ambulance |
| GET | `/dispatch/api/ambulances/{id}/` | Get ambulance details |
| POST | `/dispatch/api/ambulances/{id}/location/` | Update location |
| GET | `/dispatch/api/hospitals/` | List hospitals |
| POST | `/dispatch/api/hospitals/` | Create hospital |
| GET | `/emergencies/api/calls/` | List emergency calls |
| POST | `/emergencies/api/calls/` | Create emergency call |
| POST | `/dispatch/api/dispatch/` | **DISPATCH AMBULANCE** |

---

## Testing Dispatcher in Browser

1. Navigate to: http://127.0.0.1:8000/
2. Admin dashboard should appear
3. You can view fleet status and pending emergencies

---

## HTTP Status Codes to Expect

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 400 | Validation error (check input) |
| 403 | Not authorized (use dispatcher account) |
| 404 | Resource not found |
| 409 | Resource conflict (ambulance already dispatched) |
| 500 | Server error |

---

## Testing with cURL Examples

### Get all ambulances
```bash
curl http://127.0.0.1:8000/dispatch/api/ambulances/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Dispatch ambulance (MAIN TEST)
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "emergency_call_id": 43,
    "ambulance_id": 6,
    "paramedic_id": 20,
    "hospital_id": 6
  }'
```

Expected response:
```json
{
  "message": "Ambulance dispatched successfully",
  "emergency_call": {
    "id": 43,
    "call_id": "CALL-44C65DC8",
    "status": "DISPATCHED",
    "assigned_ambulance": 6,
    "hospital_destination": "Test Hospital"
  },
  "ambulance": {
    "id": 6,
    "unit_number": "TESTAMB001",
    "status": "EN_ROUTE"
  }
}
```

---

## Dispatcher Dashboard Features

- **View Pending Emergencies:** See all RECEIVED status calls
- **View Available Ambulances:** Check AVAILABLE ambulances
- **Dispatch Ambulance:** Click dispatch button to assign unit
- **Select Paramedic:** Assign paramedic to dispatch
- **Choose Hospital:** Set destination hospital
- **Real-time Updates:** WebSocket updates to dashboard

---

## Troubleshooting During Testing

### "Ambulance is not available"
- Ambulance is already assigned to another call
- Try with a different ambulance ID

### "Emergency call must be in RECEIVED status"
- Emergency was already dispatched
- Create a new emergency call first

### "Only dispatchers can dispatch ambulances"
- Make sure you're using dispatcher account
- Token must be for dispatcher user

### "Hospital not found"
- Hospital ID doesn't exist
- This is optional - you can omit it

---

## Next Steps

1. **Create Test Data** (if needed):
   - Create dispatcher user
   - Create paramedic user
   - Create ambulance
   - Create hospital
   - Create emergency call

2. **Test Dispatch Flow**:
   - Verify ambulance available
   - Send dispatch request
   - Verify status changes
   - Verify relationships created

3. **Test Error Cases**:
   - Try dispatching non-existent ambulance
   - Try as non-dispatcher user
   - Try with invalid emergency ID

---

## Server Logs

Watch the server terminal for:
- ✅ HTTP 200 = Successful dispatch
- ✅ HTTP 400 = Validation error (check input)
- ✅ HTTP 403 = Permission error
- ⚠️ Check the error message for details

---

**Ready to test? Start with the dispatch endpoint above!**
