# PARAMEDIC DISPATCH NOTIFICATION - QUICK TEST GUIDE

## ⚡ 5-Minute Test

### Prerequisites
- Django server running
- Dispatcher user exists with `is_dispatcher=True`
- Paramedic user exists with `is_paramedic=True`
- At least one ambulance exists with status "AVAILABLE"

---

## 🧪 Test Steps

### 1. Setup (2 minutes)

**Terminal 1: Start Server**
```bash
python manage.py runserver
```

**Browser 1: Dispatcher Login**
```
URL: http://localhost:8000/core/login/
Login as: dispatcher user
Navigate to: http://localhost:8000/dashboard/
```

**Browser 2: Paramedic Login** (use incognito/different browser)
```
URL: http://localhost:8000/core/login/
Login as: paramedic user
Navigate to: http://localhost:8000/paramedic/
```

### 2. Verify Initial State (30 seconds)

**Dispatcher Dashboard (Browser 1)**:
- ✅ Should see green badge: "WS: connected"
- ✅ Should see pending emergency calls OR ability to create new one

**Paramedic Interface (Browser 2)**:
- ✅ Should see green badge: "WS: connected"
- ✅ Should see "No Active Call" message
- ✅ Console should show: "WebSocket connected"

### 3. Create Emergency (1 minute)

**In Dispatcher Dashboard (Browser 1)**:
1. Click "New Emergency" button OR use existing emergency
2. Fill in:
   - Caller Name: "Test Patient"
   - Phone: "+232876543210"
   - Emergency Type: "Cardiac Arrest"
   - Location: "123 Main Street, Freetown"
   - Description: "Chest pain, difficulty breathing"
3. Click "Create Emergency Call"

### 4. Dispatch Ambulance (1 minute)

**In Dispatcher Dashboard (Browser 1)**:
1. Find the newly created emergency in "Pending" calls
2. Click the ambulance icon OR click the call card
3. In "Dispatch Ambulance" modal:
   - **Select Ambulance**: Choose available unit
   - **Assign Paramedic**: **IMPORTANT - Select the logged-in paramedic**
   - (Optional) Select destination hospital
4. Click "Dispatch" button

### 5. Verify Notification (30 seconds)

**Immediately in Paramedic Interface (Browser 2)**:

**✅ Expected Behavior:**
1. **Sound**: Two-tone beep starts playing (repeats every 2 seconds)
2. **Modal**: Full-screen modal appears showing:
   - Emergency details (Call ID, type, priority)
   - Patient information (name, age, condition)
   - Ambulance details (unit number, type)
   - Dispatcher information
   - Preparation checklist
3. **Banner**: Red banner appears at top of page
4. **Console**: Should show:
   ```
   ========================================
   📧 WebSocket message received
   ========================================
   Message type: ambulance_dispatched_to_paramedic
   🚑 AMBULANCE DISPATCHED TO PARAMEDIC!
   ========================================
   🚑 HANDLING DISPATCH NOTIFICATION
   ========================================
   🔔 Starting dispatch alert sound...
   ✅ Dispatch notification displayed
   ```

### 6. Acknowledge (30 seconds)

**In Paramedic Interface (Browser 2)**:
1. Click "Acknowledge & Prepare" button in modal
2. **Expected**:
   - Sound stops immediately
   - Modal closes
   - Banner disappears
   - Page auto-reloads (within 0.5 seconds)
   - Shows the new active call with all details
   - Status badge shows "DISPATCHED"

---

## ✅ Success Checklist

After completing the test, verify:

- [ ] Paramedic receives notification within 1 second of dispatch
- [ ] Two-tone beep sound plays automatically
- [ ] Modal shows all emergency details correctly
- [ ] Patient name, age, and condition are displayed
- [ ] Ambulance unit number is shown
- [ ] Dispatcher name is visible
- [ ] Preparation checklist is displayed
- [ ] Persistent banner appears at top
- [ ] Sound repeats every 2 seconds
- [ ] Clicking "Acknowledge & Prepare" stops sound
- [ ] Clicking "Acknowledge & Prepare" closes modal
- [ ] Clicking "Acknowledge & Prepare" removes banner
- [ ] Page reloads after acknowledgment
- [ ] New active call appears with correct details
- [ ] No JavaScript errors in console
- [ ] WebSocket status remains "connected" throughout

---

## 🐛 Troubleshooting

### Issue: No notification appears

**Check**:
1. Did you select a paramedic in the dispatch modal? (Most common issue!)
2. Is the paramedic's WebSocket connected? (green badge)
3. Browser console showing any errors?
4. Server logs showing "🚑 Sending dispatch notification to paramedic X"?

**Solution**:
```bash
# Check server terminal for:
🚑 Sending dispatch notification to paramedic 5
✅ Dispatch notification sent to paramedic 5
```

### Issue: Sound doesn't play

**Check**:
1. Have you interacted with the page? (click anywhere first)
2. Is your browser volume muted?
3. Does your browser support Web Audio API?

**Solution**:
- Click anywhere on paramedic page before dispatching
- Try Chrome or Firefox (better Web Audio support)
- Check browser console for audio errors

### Issue: Modal appears but is blank/incomplete

**Check**:
1. Browser console for JavaScript errors
2. Server logs for serialization errors
3. Did dispatcher fill in patient details?

**Solution**:
- Check WebSocket message in console: `Full data: {...}`
- Verify all fields are present in the data object
- Re-dispatch with complete patient information

### Issue: Page doesn't reload after acknowledgment

**Check**:
1. Browser console for fetch errors
2. CSRF token errors?
3. Network tab showing 200 response?

**Solution**:
- Hard refresh page (Ctrl+F5)
- Clear cookies and re-login
- Check `/api/emergencies/{id}/acknowledge/` endpoint exists

---

## 📊 Server Logs to Watch

Open your Django server terminal and watch for these logs after dispatching:

```
INFO 🚑 Sending dispatch notification to paramedic 5
INFO ✅ Dispatch notification sent to paramedic 5
INFO 🚑 ParamedicConsumer.ambulance_dispatched_to_paramedic triggered
INFO Event data keys: dict_keys(['call', 'ambulance', 'eta_minutes'])
INFO ✅ Dispatch notification sent to paramedic WebSocket
```

---

## 🎯 Advanced Tests

### Test 1: Multiple Paramedics
- Open 3 browsers
- Login as Dispatcher (Browser 1)
- Login as Paramedic A (Browser 2)
- Login as Paramedic B (Browser 3)
- Dispatch to Paramedic A → only Browser 2 gets notification
- Dispatch to Paramedic B → only Browser 3 gets notification

### Test 2: WebSocket Reconnection
- Login as paramedic
- Verify "WS: connected"
- Stop Django server
- Should show "WS: disconnected" (red)
- Restart Django server
- Should reconnect within 3 seconds
- Dispatch ambulance → notification should work

### Test 3: Dismiss vs Acknowledge
- Receive notification
- Click "Dismiss (Stop Sound)" instead of Acknowledge
- Sound stops, modal closes
- Banner should remain
- Click X on banner → banner disappears
- Page does NOT reload
- Manual refresh shows active call

---

## 🚀 Production Checklist

Before deploying to production:

- [ ] Test with real emergency data
- [ ] Test with multiple simultaneous paramedics
- [ ] Test network interruption recovery
- [ ] Test on mobile devices (iOS Safari, Android Chrome)
- [ ] Test with slow network (throttle to 3G)
- [ ] Verify sound works on all browsers
- [ ] Test acknowledgment endpoint performance
- [ ] Monitor server logs for errors
- [ ] Set up error tracking (Sentry recommended)
- [ ] Document for training staff

---

## 📱 Mobile Testing

### iOS Safari
```
Expected: ✅ Works
Note: Sound may require first user interaction
```

### Android Chrome
```
Expected: ✅ Works
Note: Full support for Web Audio API
```

### Mobile Browser Tips
- Test in portrait and landscape
- Verify modal is responsive
- Check touch targets are large enough
- Test with device notification sounds

---

## ⏱️ Performance Benchmarks

**Expected Latency**:
- Dispatch button click → WebSocket event: < 100ms
- WebSocket event → Browser notification: < 50ms
- Total end-to-end: < 200ms
- Sound start delay: < 100ms
- Page reload time: < 1 second

**If slower**:
- Check network latency
- Monitor server CPU usage
- Check Redis performance (if using Redis channel layer)
- Optimize serializers if needed

---

## 📞 Support

If you encounter any issues:

1. **Check Documentation**: `PARAMEDIC_DISPATCH_NOTIFICATION_SYSTEM.md`
2. **Browser Console**: Press F12, check for errors
3. **Server Logs**: Look for detailed error messages
4. **Network Tab**: Verify WebSocket connection
5. **Django Admin**: Check user permissions

---

**Testing Complete!** 🎉

If all checks pass, the system is ready for production use.
