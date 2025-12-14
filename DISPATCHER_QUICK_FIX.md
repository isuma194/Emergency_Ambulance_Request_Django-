# DISPATCHER DASHBOARD - QUICK FIX GUIDE

## 🚀 Quick Start (5 Minutes)

### Step 1: Run Diagnostic
```bash
python diagnose_dispatcher.py
```

### Step 2: Fix Common Issues

**If "No dispatcher users found":**
```bash
python manage.py shell
```
```python
from core.models import User
user = User.objects.get(username='YOUR_USERNAME')
user.is_dispatcher = True
user.save()
exit()
```

**If "No emergency data":**
```bash
python manage.py setup_sample_data
```

**If "No ambulances":**
```bash
python create_test_ambulances.py
```

### Step 3: Start Server
```bash
python manage.py runserver
```

### Step 4: Test Dashboard
1. Open browser: `http://localhost:8000/core/login/`
2. Login as dispatcher
3. Navigate to: `http://localhost:8000/dashboard/`
4. Press F12 to open console
5. Look for: "✓✓✓ DISPATCHER DASHBOARD INITIALIZED ✓✓✓"

---

## 🐛 Error Messages Decoder

### "WS: error" (Yellow Badge)

**Meaning**: WebSocket failed to connect

**Check**:
1. Is server running? `python manage.py runserver`
2. Are you logged in as dispatcher?
3. Check browser console for error code

**Quick Fix**:
- Error 4001 = Not authenticated as dispatcher
  - Fix: Set `is_dispatcher=True` in user model
- Error 1006 = Server not running
  - Fix: Start Django server

---

### "No calls in this category"

**Meaning**: No emergency data in database

**Quick Fix**:
```bash
python manage.py setup_sample_data
# or
python create_test_emergency.py
```

---

### "L is not defined"

**Meaning**: Leaflet library not loaded

**Quick Fix**:
1. Check internet connection (CDN resource)
2. Hard refresh: Ctrl+F5
3. Clear browser cache

---

### Authentication Error Modal

**Meaning**: User doesn't have dispatcher permissions

**Quick Fix**:
```python
# Django shell
from core.models import User
user = User.objects.get(username='USERNAME')
user.is_dispatcher = True
user.role = 'DISPATCHER'
user.save()
```

---

## 📊 What Should You See?

### Browser Console (F12) - Success
```
========================================
DISPATCHER DASHBOARD INITIALIZATION
========================================
✓ Required libraries loaded
✓ Map initialized successfully
Attempting to connect to WebSocket: ws://localhost:8000/ws/dispatchers/
WebSocket connected successfully
Received initial_data message
Received initial data: {emergencies: 5, ambulances: 3, hospitals: 2}
✓ Initial data loaded and rendered successfully
✓ Call filters configured
✓✓✓ DISPATCHER DASHBOARD INITIALIZED ✓✓✓
========================================
```

### Server Console - Success
```
==================================================
DISPATCHER WEBSOCKET CONNECTION ATTEMPT
==================================================
User: dispatcher_user
Username: dispatcher
Is Authenticated: True
Is Dispatcher: True
✅ WebSocket authentication SUCCESSFUL for dispatcher: dispatcher
✅ WebSocket connection ACCEPTED for dispatcher: dispatcher
📥 Starting send_initial_data()...
✅ Initial data sent successfully
```

### Dashboard UI - Success
- ✅ Green badge: "WS: connected"
- ✅ Emergency calls listed in left panel
- ✅ Map shows markers
- ✅ Fleet list shows ambulances
- ✅ No error modals

---

## 🔧 Common Fixes

### Fix 1: User Not Dispatcher
```python
# Option A: Django Shell
python manage.py shell
from core.models import User
u = User.objects.get(username='dispatcher')
u.is_dispatcher = True
u.save()

# Option B: Django Admin
# Login to /admin/
# Go to Users
# Edit user
# Check "is_dispatcher" checkbox
# Save
```

### Fix 2: No Sample Data
```bash
# Full sample data (recommended)
python manage.py setup_sample_data

# Or individual scripts
python create_test_emergency.py
python create_test_ambulances.py
python create_hospitals.py
```

### Fix 3: Channel Layer Error
```bash
# If Redis not available, edit settings.py
# Ensure InMemoryChannelLayer is configured
# (Already handled automatically in settings.py)

# To use Redis (optional):
# 1. Install Redis: https://redis.io/download
# 2. Start Redis: redis-server
# 3. Restart Django server
```

### Fix 4: Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput

# Restart server
python manage.py runserver
```

---

## 📝 Testing Checklist

- [ ] Run `python diagnose_dispatcher.py` - all checks pass
- [ ] Server starts without errors
- [ ] Login as dispatcher succeeds
- [ ] Dashboard loads without error modal
- [ ] WebSocket badge shows "WS: connected" (green)
- [ ] Emergency calls appear in left panel
- [ ] Map shows emergency markers
- [ ] Fleet list shows ambulances
- [ ] Browser console shows initialization success
- [ ] Server console shows WebSocket connection accepted

---

## 🆘 Still Having Issues?

### Check These Files:

1. **Browser Console** (F12)
   - Look for red errors
   - Check for "✓✓✓ DISPATCHER DASHBOARD INITIALIZED ✓✓✓"

2. **Server Console**
   - Look for WebSocket logs
   - Check for "✅ WebSocket authentication SUCCESSFUL"

3. **Diagnostic Script Output**
   ```bash
   python diagnose_dispatcher.py
   ```
   - Shows exactly what's misconfigured

### Get More Details:

**Browser Console**:
- Error messages now show:
  - File name
  - Function name
  - Error type
  - Suggested fix

**Server Console**:
- WebSocket logs show:
  - User authentication status
  - Permission checks
  - Connection acceptance/rejection reason

**Error Modals**:
- Authentication errors show:
  - Exact reason for failure
  - Step-by-step fix instructions

---

## 💡 Pro Tips

1. **Always keep browser console open** (F12) during testing
2. **Watch server console** for WebSocket connection logs
3. **Run diagnostic script** before reporting issues
4. **Clear browser cache** if seeing old errors
5. **Check user has is_dispatcher=True** first

---

## 🎯 Expected Behavior

### New Emergency Created
1. Server broadcasts to dispatcher WebSocket group
2. Dashboard receives `new_ambulance_request` message
3. Alert modal pops up with emergency details
4. Sound notification plays (if enabled)
5. Emergency appears in "Pending" calls list
6. Map marker added at emergency location

### Ambulance Dispatched
1. Dispatcher selects ambulance and clicks "Dispatch"
2. POST request to `/dispatch/api/dispatch/`
3. Server updates emergency and ambulance status
4. WebSocket broadcasts `emergency_update` message
5. Dashboard updates call status automatically
6. Map updates ambulance marker color

---

## 📚 Documentation Files

- **Full Report**: `DISPATCHER_DEBUG_FIX_REPORT.md`
- **Diagnostic Tool**: `diagnose_dispatcher.py`
- **This Guide**: `DISPATCHER_QUICK_FIX.md`

---

**Last Updated**: December 12, 2025  
**Status**: ✅ Fully debugged and documented
