# 🚨 QUICK FIX GUIDE - Dispatcher Dashboard

## ⚡ 60-Second Diagnosis

```bash
# 1. Run diagnostic script
python test_dispatcher_debug.py

# 2. If all tests pass, start server
python manage.py runserver

# 3. Login and check browser console (F12)
# Look for: "✓✓✓ DISPATCHER DASHBOARD INITIALIZED ✓✓✓"
```

---

## 🔍 Common Issues & Instant Fixes

### Issue: "No dispatcher users found"
```bash
python test_dispatcher_debug.py
# Creates test user automatically
# Username: dispatcher_test
# Password: test123
```

### Issue: "No emergencies in database"
```bash
python manage.py shell -c "from core.management.commands.setup_sample_data import Command; Command().handle()"
```

### Issue: "WebSocket connection failed"
**Check**: Are you using the Django development server?
```bash
python manage.py runserver  # Uses ASGI automatically
```

### Issue: "Messages not appearing"
**Check Browser Console**: Press F12, look for:
- ❌ Red errors? → Read the detailed error message
- ⚠️ Yellow warnings? → Check what data is missing
- ✅ Green checks? → System working, check filters (Pending/Active/Completed)

---

## 📋 Console Output Reference

### ✅ GOOD - Everything Working
```
✓ Required libraries loaded
✓ Map initialized successfully
✓ WebSocket connection initiated
WebSocket connected successfully
Received initial_data message
Received initial data: {emergencies: 5, ambulances: 3, hospitals: 2}
✓ Initial data loaded and rendered successfully
Dashboard loaded successfully
```

### ❌ BAD - Something Failed
```
✗ Error initializing map: Leaflet is not defined
```
**Fix**: Check that Leaflet CDN is loading (check internet connection)

```
✗ WebSocket parse error: Unexpected token
```
**Fix**: Server sent invalid JSON - check server console for Python errors

```
Server sent incomplete initial data
```
**Fix**: Run `python test_dispatcher_debug.py` to check serialization

---

## 🎯 5-Minute Verification Checklist

- [ ] Run `python test_dispatcher_debug.py` - all tests pass
- [ ] Server starts without errors
- [ ] Can login as dispatcher
- [ ] Dashboard page loads (no white screen)
- [ ] Browser console shows "INITIALIZED" message
- [ ] Calls appear in the left panel (or "No calls" message)
- [ ] Map displays in center panel
- [ ] WebSocket indicator shows "WS: connected" (top-right of map)
- [ ] No red errors in console
- [ ] No error toast notifications

---

## 🔧 Emergency Troubleshooting

### Nuclear Option: Reset Everything
```bash
# Backup database
cp db.sqlite3 db.sqlite3.backup

# Re-run migrations
python manage.py migrate

# Create sample data
python manage.py shell -c "from core.management.commands.setup_sample_data import Command; Command().handle()"

# Create test dispatcher
python test_dispatcher_debug.py

# Start fresh
python manage.py runserver
```

---

## 📞 Quick Support Commands

### Check User Exists
```python
python manage.py shell
>>> from core.models import User
>>> User.objects.filter(role='dispatcher')
```

### Check Emergency Data
```python
python manage.py shell
>>> from emergencies.models import EmergencyCall
>>> EmergencyCall.objects.all().count()
```

### Manual Test User Creation
```bash
python manage.py createsuperuser
# Then set role to 'dispatcher' in admin
```

---

## 🎓 Understanding Error Messages

### Frontend Errors (Browser Console)

| Error | Meaning | Fix |
|-------|---------|-----|
| "Leaflet is not defined" | CDN didn't load | Check internet connection |
| "Bootstrap is not defined" | CDN didn't load | Check internet connection |
| "WebSocket creation failed" | Can't connect to server | Check server is running |
| "Server sent incomplete initial data" | Backend serialization error | Check server logs |
| "Error rendering calls" | Invalid data in database | Check data with diagnostic script |

### Backend Errors (Server Console)

| Error | Meaning | Fix |
|-------|---------|-----|
| "RelatedObjectDoesNotExist" | Missing foreign key data | Run migrations |
| "SerializationError" | Can't convert data to JSON | Check model fields |
| "Connection refused" | Redis not available | OK - fallback to InMemory |
| "Permission denied" | User not dispatcher | Check user role |

---

## ✨ Success Indicators

You know it's working when:
1. ✅ Page loads in <2 seconds
2. ✅ Console shows green checkmarks
3. ✅ Calls list shows emergencies (or "No calls" message)
4. ✅ Map shows with markers
5. ✅ No error toasts
6. ✅ WebSocket shows "connected"

---

## 📚 Full Documentation

See `DISPATCHER_FIX_COMPLETE.md` for:
- Complete list of all fixes
- Detailed technical explanations
- File-by-file changes
- Advanced troubleshooting

---

**Updated**: December 11, 2025  
**Status**: ✅ Fixes Complete
