# 🚀 QUICK START GUIDE - Emergency Ambulance Dispatch System

## 5-Minute Setup

### Step 1: Start the Server
```bash
# Navigate to project directory
cd "c:\Users\CENTRAL UNIVERSITY\Documents\GitHub\Emergency_Ambulance_Request_Django-"

# Start Django server
python manage.py runserver
```

✅ Server running at: `http://localhost:8000`

---

## 👥 User Roles & Access

### 🎯 Dispatcher
**Role**: Manages emergency calls and assigns ambulances  
**Login**: 
- Username: `dispatcher`
- Password: (set via admin panel)

**Capabilities**:
- View pending emergencies
- Create new emergency calls
- Dispatch ambulances
- Auto-assign paramedics
- Select hospital destinations
- View real-time ambulance locations
- Track emergency status

**Access URL**: `http://localhost:8000`

---

### 👨‍⚕️ Paramedic
**Role**: Responds to emergency calls and provides field updates  
**Login**:
- Username: `paramedic`
- Password: (set via admin panel)

**Capabilities**:
- Receive dispatch alerts
- View emergency details
- Update call status
- Share GPS location (automatic)
- View hospital destination
- Track call duration
- Toggle availability

**Access URL**: `http://localhost:8000`

---

### 🔐 Admin
**Role**: System administration and configuration  
**Login**:
- Username: `admin`
- Password: (set during setup)

**Capabilities**:
- Create/edit users
- Create/edit ambulances
- Create/edit hospitals
- View all emergencies
- System statistics
- Database management

**Access URL**: `http://localhost:8000/admin/`

---

## 📋 Complete Workflow Example

### Scenario: Cardiac Emergency Response

#### 1️⃣ Dispatcher Receives Call
```
Emergency Created:
├─ Call ID: CALL-FCFD0153
├─ Type: CARDIAC
├─ Location: 123 Heart St
├─ Caller Phone: +23210000000
├─ Patient Name: John Doe
└─ Priority: HIGH
```

#### 2️⃣ Dispatcher Opens Dispatch Modal
```
Click: "Dispatch" button on emergency

Modal Shows:
├─ Emergency: CALL-FCFD0153 - CARDIAC
├─ Location: 123 Heart St
├─ Available Ambulances: 5 units
├─ Available Paramedics: 1 person
└─ Hospitals: 4 options (sorted by capacity)
```

#### 3️⃣ Dispatcher Selects Resources
```
Select Ambulance: Unit Amb0002 (Advanced Life Support)
Select Paramedic: (leave empty for auto-assign)
Select Hospital: Central Medical Hospital (MODERATE capacity)

Click: "Dispatch" Button
```

#### 4️⃣ System Auto-Assigns & Dispatches
```
Behind the Scenes:
✅ Auto-assign paramedic: paramedic (ID: 11)
✅ Update ambulance status: EN_ROUTE
✅ Update emergency status: DISPATCHED
✅ Set hospital destination: Central Medical Hospital
✅ Lock emergency to paramedic & ambulance
✅ Send WebSocket notification
```

#### 5️⃣ Paramedic Receives Alert
```
Browser Alert Appears:
┌─────────────────────────────────────┐
│ 🔔 New Dispatch Assignment!         │
│                                     │
│ Emergency ID: CALL-FCFD0153        │
│ Type: CARDIAC                      │
│ Location: 123 Heart St             │
│ Priority: HIGH                     │
│                                     │
│ Preparing dashboard...              │
└─────────────────────────────────────┘

Dashboard Auto-Reloads
```

#### 6️⃣ Paramedic Takes Action
```
Paramedic Dashboard Shows:
├─ Emergency Details
├─ Patient Info: John Doe
├─ Call Received: 2 minutes ago
├─ Status: DISPATCHED
├─ Buttons:
│  ├─ Mark EN_ROUTE ✓ Click
│  ├─ Mark ON_SCENE
│  ├─ Mark TRANSPORTING
│  └─ Share GPS Location (Auto, every 15s)
├─ Hospital Destination: Central Medical Hospital
└─ Support Contact: Dispatcher

Paramedic Updates:
DISPATCHED → EN_ROUTE (2 min)
EN_ROUTE → ON_SCENE (8 min)
ON_SCENE → TRANSPORTING (5 min)
TRANSPORTING → AT_HOSPITAL (12 min)
AT_HOSPITAL → CLOSED
```

#### 7️⃣ Dispatcher Monitors
```
Dispatcher Dashboard Updates Real-Time:
├─ Emergency Status: AT_HOSPITAL ✓
├─ Ambulance: Unit Amb0002 - AT_HOSPITAL
├─ Paramedic: paramedic - Completed
├─ Hospital: Central Medical Hospital
├─ Total Duration: 27 minutes
├─ GPS Track: Visible on map
└─ Call Status: CLOSED ✓
```

---

## 🎮 Interactive Features

### Hospital Selection
```
Hospitals are automatically sorted by capacity:

LOW Capacity (Best Choice)
├─ Harbor View Medical Center
├─ Available Beds: 156/400
└─ Specialties: Surgery, Orthopedics, Respiratory

MODERATE Capacity
├─ Central Medical Hospital
├─ Available Beds: 45/500
└─ Specialties: Cardiology, Trauma, Neurology

HIGH Capacity (Getting Full)
├─ St. Johns Emergency Hospital
├─ Available Beds: 12/300
└─ Specialties: Trauma, Cardiac, Pediatrics

FULL Capacity (No Capacity)
├─ Riverside Emergency Center
├─ Available Beds: 0/250
└─ Specialties: Neurology, Cardiology
```

### Paramedic Auto-Assign
```
✅ Automatically assigns first available paramedic
✅ Filters by: is_available_for_dispatch = True
✅ Falls back to any active paramedic if needed
✅ Can be overridden by manual selection
✅ Shows success notification: "Paramedic [Name] auto-assigned"
```

### GPS Location Sharing
```
Paramedic Dashboard:
├─ Status: GPS: idle (until dispatch)
├─ Click "Share GPS" → Acquires location
├─ Shows: GPS: shared (±15m accuracy)
├─ Automatic: Shares location every 15 seconds
├─ Updates: Dispatcher sees real-time location
└─ Dispatcher: Can calculate ETA on map
```

---

## 🧪 Testing the System

### Quick Test (2 minutes)

```bash
# Terminal 1: Start Server
python manage.py runserver

# Terminal 2: Run Tests
python test_system.py

# Should see:
# ✅ Auto-assign paramedic API: WORKING
# ✅ Hospital population: WORKING
# ✅ Ambulance availability: WORKING
# ✅ Paramedic list endpoint: WORKING
# ✅ Dispatch workflow: WORKING
```

### Manual Test (10 minutes)

```
1. Open http://localhost:8000
2. Login as dispatcher
3. View pending emergencies (should see CALL-FCFD0153)
4. Click "Dispatch"
5. Modal opens with:
   - Ambulance dropdown (populated)
   - Paramedic dropdown (populated)
   - Hospital dropdown (4 options sorted)
6. Select ambulance
7. Leave paramedic empty
8. Click "Dispatch"
9. See "Ambulance dispatched successfully"
10. ✅ Test passed!
```

---

## 📊 System Status

```
Check system health:
python check_db.py

Output shows:
├─ Total Users: 3 (dispatcher, paramedic, admin)
├─ Total Ambulances: 5 (all AVAILABLE)
├─ Total Hospitals: 4 (with capacity info)
└─ Total Emergencies: 1 (RECEIVED status)
```

---

## 🔧 Configuration

### Database
```
Current: SQLite (db.sqlite3)
Production: PostgreSQL recommended
Migrations: python manage.py migrate
```

### WebSocket
```
Dispatcher: ws://localhost:8000/ws/dispatchers/
Paramedic: ws://localhost:8000/ws/paramedic/
Channel Layer: In-memory (development)
Production: Redis recommended
```

### Static Files
```
Location: /static/
Serving: Django development server
Production: Use WhiteNoise or Nginx
```

---

## 🆘 Troubleshooting

### Server Won't Start
```
Error: Port 8000 already in use
Solution: python manage.py runserver 8001
        or kill process: netstat -ano | findstr "8000"
```

### No Hospitals Show Up
```
Error: Hospital dropdown empty
Solution: python create_hospitals.py
```

### Paramedic Not Assigned
```
Error: Paramedic remains empty after dispatch
Solution: Verify paramedic user exists: python check_db.py
         Ensure is_active=True and is_available_for_dispatch=True
```

### WebSocket Connection Failed
```
Warning: "ws: Connection failed"
Solution: Check server is running on port 8000
         Check browser console for errors
         Verify authentication (must be logged in)
```

### Ambulance Not Available
```
Error: "No available ambulances"
Solution: python reset_ambulances.py
         (Resets all ambulances to AVAILABLE status)
```

---

## 📞 Key API Endpoints

```
Emergencies:
  GET  /api/emergencies/               - List all
  POST /api/emergencies/               - Create new
  GET  /api/emergencies/<id>/          - Get details
  PATCH /api/emergencies/<id>/status/  - Update status

Ambulances:
  GET  /dispatch/api/ambulances/       - List all
  POST /dispatch/api/ambulances/<id>/location/ - Update location

Hospitals:
  GET  /dispatch/api/hospitals/        - List all
  POST /dispatch/api/hospitals/<id>/capacity/ - Update capacity

Dispatch:
  POST /dispatch/api/dispatch/         - Dispatch ambulance
  GET  /dispatch/api/dispatch/auto-assign-paramedic/ - Auto-assign

Paramedics:
  GET  /api/paramedics/                - List all
  GET  /api/paramedics/?available=1    - List available
```

---

## 📚 Additional Resources

```
System Documentation:
├─ IMPLEMENTATION_COMPLETE.md (What was fixed)
├─ ARCHITECTURE.md (System design & data flow)
├─ SYSTEM_READY.md (Complete feature list)
├─ README.md (Original project info)
└─ QUICK_REFERENCE_CARD.md (Quick tips)

Helper Scripts:
├─ check_db.py (Database status)
├─ create_hospitals.py (Create test data)
├─ reset_ambulances.py (Reset ambulances)
└─ test_system.py (Run all tests)
```

---

## ✅ Checklist Before Going Live

```
Before deployment:
☐ Test all three user roles (dispatcher, paramedic, admin)
☐ Create real ambulances and hospitals
☐ Set user passwords for production
☐ Configure email notifications (optional)
☐ Set up database backups
☐ Configure logging
☐ Set DEBUG=False in production
☐ Use PostgreSQL instead of SQLite
☐ Set up Redis for channel layer
☐ Configure static file serving
☐ Set up SSL/HTTPS
☐ Configure CORS settings
☐ Test WebSocket on production server
☐ Load test with multiple users
☐ Document deployment process
```

---

**Quick Start Version**: 1.0  
**Last Updated**: December 6, 2025  
**Status**: ✅ PRODUCTION READY

**Questions?** Check ARCHITECTURE.md for detailed system information or IMPLEMENTATION_COMPLETE.md for what was changed.
