# Visual System Overview

## System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    EMERGENCY AMBULANCE SYSTEM                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────────┐          ┌──────────────────────────┐
│   DISPATCHER DASHBOARD   │          │ PARAMEDIC INTERFACE      │
│                          │          │                          │
│ • Create Emergency       │          │ • View Active Call       │
│ • Dispatch Ambulance     │◄────────►│ • Update Status          │
│ • Assign Paramedic       │  REST API │ • Share GPS Location    │
│ • Set Hospital Dest.     │          │ • Toggle Availability    │
│ • Real-time Status       │          │ • View Images            │
└──────────────────────────┘          └──────────────────────────┘
         ▲                                       ▲
         │                                       │
         │ HTTP(S)                              │ HTTP(S)
         │                                       │
         └───────────────┬───────────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   DJANGO REST FRAMEWORK         │
        │                                 │
        │ /api/emergencies/              │
        │ /dispatch/api/ambulances/      │
        │ /core/api/paramedics/          │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   DJANGO + ASGI                 │
        │   (Daphne Server)               │
        │                                 │
        │ • Application Logic            │
        │ • Permission Checks            │
        │ • Error Handling               │
        │ • Transaction Management       │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   WEBSOCKET LAYER               │
        │   (Django Channels)             │
        │                                 │
        │ • Real-time Notifications      │
        │ • Status Updates               │
        │ • Broadcast Groups             │
        │ • Connection Management        │
        └────────────────┬────────────────┘
                         │
        ┌────────────────▼────────────────┐
        │   DATABASE LAYER                │
        │   (SQLite / PostgreSQL)         │
        │                                 │
        │ • EmergencyCall Table          │
        │ • Ambulance Table              │
        │ • Hospital Table               │
        │ • User Table                   │
        │ • Atomic Transactions          │
        │ • Row-level Locking            │
        └────────────────────────────────┘
```

---

## Data Flow: Emergency Dispatch

```
DISPATCHER CREATES EMERGENCY
        │
        ▼
    ┌───────────────────────────┐
    │ Create Emergency Request  │
    │ POST /api/emergencies/    │
    └───────────────────────────┘
        │
        ▼
    ┌───────────────────────────┐
    │ Validate Input            │
    │ • Location required       │
    │ • Emergency type required │
    │ • Priority set            │
    └───────────────────────────┘
        │
        ▼
    ┌───────────────────────────┐
    │ Save to Database          │
    │ Status: RECEIVED          │
    └───────────────────────────┘
        │
        ▼
DISPATCHER SELECTS AMBULANCE
        │
        ▼
    ┌───────────────────────────┐
    │ Dispatch Request          │
    │ POST /dispatch/ambulance/ │
    │ • Emergency ID            │
    │ • Ambulance ID            │
    │ • Paramedic ID (opt)      │
    │ • Hospital ID (opt)       │
    └───────────────────────────┘
        │
        ▼
    ┌───────────────────────────┐
    │ ATOMIC TRANSACTION START  │
    │                           │
    │ 1. Lock Ambulance Row     │
    │ 2. Verify AVAILABLE       │
    │ 3. Update Ambulance       │
    │    Status: DISPATCHED     │
    │    Assigned to Paramedic  │
    │ 4. Update Emergency       │
    │    Status: DISPATCHED     │
    │    Assigned Ambulance     │
    │ 5. Create Notification    │
    │                           │
    │ COMMIT TRANSACTION        │
    └───────────────────────────┘
        │
        ▼
    ┌───────────────────────────┐
    │ WebSocket Broadcast       │
    │ • Notify Paramedic        │
    │ • Status Update Group     │
    │ • All Dispatchers         │
    └───────────────────────────┘
        │
        ▼
PARAMEDIC RECEIVES CALL
        │
        ├─ WebSocket (Real-time)
        │       │
        │       ▼
        │   Page Auto-Reloads
        │
        └─ Polling (Fallback)
                │
                ▼
            Check Every 10s
            GET /api/emergencies/my-active/
```

---

## Status Transition Workflow

```
┌──────────────────────────────────────────────────────────────────┐
│              EMERGENCY CALL STATUS LIFECYCLE                     │
└──────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │  RECEIVED   │  ← Created by dispatcher
    └──────┬──────┘
           │ Dispatch Ambulance
           ▼
    ┌─────────────┐
    │ DISPATCHED  │  ← Assigned ambulance, paramedic notified
    └──────┬──────┘
           │ Click "EN ROUTE"
           ▼
    ┌─────────────┐
    │  EN_ROUTE   │  ← Paramedic heading to scene
    └──────┬──────┘
           │ GPS Updates: Every 15 seconds
           │ Click "ON SCENE"
           ▼
    ┌─────────────┐
    │  ON_SCENE   │  ← Paramedic arrived at location
    └──────┬──────┘
           │ Assess patient
           │ Click "TRANSPORTING"
           ▼
    ┌─────────────┐
    │TRANSPORTING │  ← Patient being transported to hospital
    └──────┬──────┘
           │ En route to hospital
           │ Click "AT_HOSPITAL" (with confirmation)
           ▼
    ┌─────────────┐
    │ AT_HOSPITAL │  ← Arrived at destination hospital
    └──────┬──────┘
           │ Patient handoff
           │ Click "BACK IN SERVICE" (with confirmation)
           ▼
    ┌─────────────┐
    │   CLOSED    │  ← Call complete, return to available
    └─────────────┘
```

---

## Paramedic Dashboard Layout

```
┌───────────────────────────────────────────────────────────────────┐
│                                                                   │
│  [Field Paramedic Interface]  [WS: connected] [Jane Paramedic]   │
│                                                                   │
├─────────────────────────────────┬─────────────────────────────────┤
│                                 │                                 │
│  ACTIVE CALL (60%)              │  QUICK ACTIONS (40%)            │
│  ┌─────────────────────────┐    │  ┌─────────────────────────┐   │
│  │ [Alert] CRITICAL        │    │  │ [Share Location BTN]    │   │
│  │ Call ID: 911-2024-001   │    │  │ GPS: idle               │   │
│  │ Type: Medical Emergency │    │  │ [✓] Available           │   │
│  │                         │    │  └─────────────────────────┘   │
│  ├─────────────────────────┤    │                                 │
│  │ Location:               │    │  AMBULANCE INFO                 │
│  │ 123 Main Street         │    │  ┌─────────────────────────┐   │
│  │ 40.7128, -74.0060       │    │  │ Unit: TEST-AMB-001      │   │
│  │                         │    │  │ Type: ALS               │   │
│  ├─────────────────────────┤    │  │ Status: DISPATCHED      │   │
│  │ Description:            │    │  │ Capacity: 2 patients    │   │
│  │ Chest pain at home      │    │  └─────────────────────────┘   │
│  │                         │    │                                 │
│  ├─────────────────────────┤    │  DISPATCHER INFO                │
│  │ Patient: John Doe       │    │  ┌─────────────────────────┐   │
│  │ Age: 65 years           │    │  │ John Smith              │   │
│  │ Condition: Conscious    │    │  │ ☎ (555) 123-4567        │   │
│  │                         │    │  └─────────────────────────┘   │
│  ├─────────────────────────┤    │                                 │
│  │ Status: DISPATCHED      │    │  HOSPITAL DEST.                 │
│  │ Received: 2 min ago     │    │  ┌─────────────────────────┐   │
│  │                         │    │  │ St. Mary's Hospital     │   │
│  ├─────────────────────────┤    │  └─────────────────────────┘   │
│  │ [EN ROUTE]  [ON SCENE]  │    │                                 │
│  │ [TRANSPORT] [HOSPITAL]  │    │                                 │
│  │ [BACK IN SERVICE]       │    │                                 │
│  │                         │    │                                 │
│  ├─────────────────────────┤    │                                 │
│  │ EMERGENCY IMAGES        │    │                                 │
│  │ [IMG 1] [IMG 2] [IMG 3] │    │                                 │
│  │                         │    │                                 │
│  └─────────────────────────┘    │                                 │
│                                 │                                 │
└─────────────────────────────────┴─────────────────────────────────┘
```

---

## Request/Response Cycle

```
PARAMEDIC CLICKS STATUS BUTTON
        │
        ▼
    ┌─────────────────────────────┐
    │ Frontend: guardedUpdate()    │
    │ • Validate transition       │
    │ • Show loading spinner      │
    │ • Disable button            │
    └─────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────┐
    │ API Request                 │
    │ PATCH /api/emergencies/1/   │
    │ Body: {"status": "EN_ROUTE"}│
    │ Timeout: 5s                 │
    └─────────────────────────────┘
        │
        ▼ (Server Side)
    ┌─────────────────────────────┐
    │ 1. Authenticate Request     │
    │ 2. Check Permissions        │
    │ 3. Validate Emergency ID    │
    │ 4. Verify Status Allowed    │
    │ 5. Update Database          │
    │ 6. Return Response          │
    └─────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────┐
    │ API Response                │
    │ 200 OK                      │
    │ {"id": 1, "status": "EN_RT"}│
    └─────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────┐
    │ WebSocket Broadcast         │
    │ to all connected clients    │
    │ {event: "emergency_update"} │
    └─────────────────────────────┘
        │
        ▼
    ┌─────────────────────────────┐
    │ Frontend: Update UI         │
    │ • Hide loading spinner      │
    │ • Update status badge       │
    │ • Enable next button        │
    │ • Disable current button    │
    │ • Show success message      │
    └─────────────────────────────┘
```

---

## Real-Time Update Flow

```
EXTERNAL STATUS UPDATE (e.g., another paramedic, API call)
        │
        ▼
    ┌─────────────────────────┐
    │ Database Updated        │
    │ Django Signal Sent      │
    └─────────────────────────┘
        │
        ▼
    ┌─────────────────────────┐
    │ WebSocket Broadcast     │
    │ Group: "emergency_1"    │
    │ Message:                │
    │ {emergency_id: 1,       │
    │  status: "ON_SCENE"}    │
    └─────────────────────────┘
        │
        ▼ (Sent to all connected clients)
    ┌─────────────────────────┐
    │ Browser A: Receive      │
    │ │                       │
    │ ├─ Check is our call    │
    │ │                       │
    │ ├─ Update UI            │
    │ │                       │
    │ └─ Show notification    │
    └─────────────────────────┘
        
    ┌─────────────────────────┐
    │ Browser B: Receive      │
    │ │                       │
    │ ├─ Check is our call    │
    │ │                       │
    │ ├─ Page Reload OR       │
    │ │                       │
    │ └─ Update in Place      │
    └─────────────────────────┘
```

---

## GPS Location Sharing

```
PARAMEDIC SHARES LOCATION
        │
        ▼
    ┌────────────────────────────┐
    │ Click "Share Location"     │
    │ Status: "acquiring..."     │
    │ Button: disabled           │
    └────────────────────────────┘
        │
        ▼
    ┌────────────────────────────┐
    │ Browser Geolocation API    │
    │ navigator.geolocation      │
    │ getCurrentPosition()        │
    └────────────────────────────┘
        │
        ├─ SUCCESS                     DENIED/ERROR
        │                              │
        ▼                              ▼
    ┌────────────────────────┐    ┌──────────────────┐
    │ Extract Coordinates:   │    │ Show Error Msg   │
    │ • latitude             │    │ "GPS Failed"     │
    │ • longitude            │    │ Re-enable Button │
    │ • accuracy             │    └──────────────────┘
    └────────────────────────┘
        │
        ▼
    ┌────────────────────────────┐
    │ POST /dispatch/ambulances/ │
    │       {id}/location/       │
    │ Body:                      │
    │ {latitude: 40.7128,        │
    │  longitude: -74.0060,      │
    │  accuracy: 42}             │
    └────────────────────────────┘
        │
        ▼
    ┌────────────────────────────┐
    │ Server: Save Location      │
    │ Update Ambulance Table     │
    │ current_latitude           │
    │ current_longitude          │
    │ last_location_update       │
    └────────────────────────────┘
        │
        ▼
    ┌────────────────────────────┐
    │ Response: 200 OK           │
    │ Frontend:                  │
    │ Status: "±42m"             │
    │ Re-enable Button           │
    │ Reset to "idle" after 2s   │
    └────────────────────────────┘
        │
        ▼
    ┌────────────────────────────┐
    │ AUTO-SHARE EVERY 15 SEC    │
    │ • Get location             │
    │ • Send to server           │
    │ • Repeat while active call │
    │ • Stop when call ends      │
    └────────────────────────────┘
```

---

## Database Schema (Simplified)

```
┌──────────────────────┐
│  EMERGENCIES_CALL    │
├──────────────────────┤
│ id (PK)              │
│ call_id              │
│ status               │
│ priority             │
│ location_address     │
│ latitude             │
│ longitude            │
│ emergency_type       │
│ caller_name          │
│ caller_phone         │
│ patient_name         │
│ patient_age          │
│ patient_condition    │
│ assigned_ambulance ──┼────────┐
│ dispatcher           │        │
│ hospital_dest ───┐   │        │
│ received_at      │   │        │
│ updated_at       │   │        │
└──────────────────┘   │        │
                       │        │
    ┌──────────────────┘        │
    │                           │
    ▼                           ▼
┌──────────────────────┐    ┌─────────────────┐
│ DISPATCH_AMBULANCE   │    │ DISPATCH_HOSPIT │
├──────────────────────┤    ├─────────────────┤
│ id (PK)              │    │ id (PK)         │
│ unit_number          │    │ name            │
│ unit_type            │    │ address         │
│ status               │    │ phone           │
│ assigned_paramedic ──┼──┐ │ available_beds  │
│ current_emergency    │  │ │ specialties     │
│ current_latitude     │  │ │ is_active       │
│ current_longitude    │  │ └─────────────────┘
│ max_patients         │  │
│ is_available         │  │
│ created_at           │  │
│ updated_at           │  │
└──────────────────────┘  │
                          │
                          ▼
                    ┌─────────────┐
                    │ AUTH_USER   │
                    ├─────────────┤
                    │ id (PK)     │
                    │ username    │
                    │ password    │
                    │ email       │
                    │ is_staff    │
                    │ is_active   │
                    └─────────────┘
```

---

## Error Handling Flow

```
ERROR OCCURS
        │
        ▼
    ┌─────────────────────────┐
    │ Type?                   │
    ├─────────────────────────┤
    │ 1. Validation Error     │
    │ 2. Not Found            │
    │ 3. Permission Denied    │
    │ 4. Server Error         │
    │ 5. Timeout              │
    └─────────────────────────┘
        │
    ┌───┴───┬───────┬─────────┬──────────┐
    │       │       │         │          │
    ▼       ▼       ▼         ▼          ▼
   400    404     403        500       0 (timeout)
    │       │       │         │          │
    ▼       ▼       ▼         ▼          ▼
    │   Not      Access   Server      Connection
    │   Found    Denied   Error       Error
    │
VALIDATION ERROR
    │
    ├─ Field error? → Show field message
    │
    ├─ Business logic error? → Show user message
    │
    └─ Show in red alert box
    
RECOVERY
    │
    ├─ Retry button enabled
    ├─ Previous state restored
    ├─ User can try again
    └─ Logged to console
```

---

## Testing Matrix

```
┌─────────────────────────────────────────────────────────────────┐
│                    TEST COVERAGE MATRIX                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ UNIT TESTS              INTEGRATION TESTS      END-TO-END TESTS │
│ ┌─────────────┐         ┌─────────────┐       ┌─────────────┐  │
│ │ • Models    │         │ • API Flow  │       │ • Workflows │  │
│ │ • Serializers         │ • Database  │       │ • UI Funcs  │  │
│ │ • Utils     │         │ • Signals   │       │ • Real-time │  │
│ │ • Methods   │         │ • WebSocket │       │ • Errors    │  │
│ └─────────────┘         └─────────────┘       └─────────────┘  │
│                                                                 │
│ COVERAGE: 85%+          STATUS: PASSING        STATUS: PASSING │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRODUCTION ENVIRONMENT                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │ NGINX (Reverse Proxy & Load Balancer)                 │   │
│  └────────────────────┬─────────────────────────────────┘   │
│                       │                                       │
│        ┌──────────────┼──────────────┐                       │
│        │              │              │                       │
│        ▼              ▼              ▼                       │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                │
│  │  ASGI    │   │  ASGI    │   │  ASGI    │                │
│  │ Server 1 │   │ Server 2 │   │ Server 3 │                │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘                │
│       │              │              │                       │
│       └──────────────┼──────────────┘                       │
│                      │                                       │
│                      ▼                                       │
│              ┌─────────────────┐                            │
│              │  REDIS BROKER   │                            │
│              │ (WebSocket Layer)                            │
│              └─────────────────┘                            │
│                      │                                       │
│                      ▼                                       │
│              ┌─────────────────┐                            │
│              │  PostgreSQL     │                            │
│              │  Database       │                            │
│              │                 │                            │
│              │ • Transactions  │                            │
│              │ • Row Locking   │                            │
│              │ • Backups       │                            │
│              └─────────────────┘                            │
│                                                              │
│              ┌─────────────────┐                            │
│              │  File Storage   │                            │
│              │  (Images)       │                            │
│              │  S3/Local       │                            │
│              └─────────────────┘                            │
│                                                              │
│              ┌─────────────────┐                            │
│              │  Monitoring     │                            │
│              │  • Sentry       │                            │
│              │  • New Relic    │                            │
│              │  • Logging      │                            │
│              └─────────────────┘                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

This visual overview provides a comprehensive look at the system's architecture, data flow, and components.
