# Paramedic Activity Notification Testing Guide

## Quick Start Test (5 minutes)

### Prerequisites
- Django development server running at http://127.0.0.1:8000
- Two browsers open (or use private/incognito windows)
- Test users created:
  - `dispatcher1` (dispatcher user)
  - `paramedic1` (paramedic user)

### Test Steps

**Step 1: Login as Dispatcher**
```
1. Open http://127.0.0.1:8000/login/ in Browser 1
2. Login with dispatcher credentials (e.g., dispatcher1 / password)
3. Navigate to Dispatcher Dashboard
4. Create a new emergency call:
   - Click "New Emergency Call"
   - Fill in patient details (name, age, condition)
   - Select hospital destination
   - Set priority level
   - Click "Submit"
```

**Step 2: Open Paramedic Interface**
```
1. Open http://127.0.0.1:8000/paramedic/ in Browser 2
2. Login as paramedic (e.g., paramedic1 / password)
3. You should see "No Active Call" dashboard
4. Note: Pre-dispatch preparation checklist is visible
```

**Step 3: Dispatch Ambulance**
```
1. In Browser 1 (Dispatcher), locate the emergency just created
2. Under "Available Ambulances", click "Dispatch"
3. Select an ambulance from the dropdown
4. Click "Dispatch Ambulance"
5. Wait 1-2 seconds
```

**Step 4: Observe Notification in Paramedic Interface**
```
Expected in Browser 2:
✅ Green notification banner appears at top
✅ Shows: Emergency ID, Type, Location, Priority
✅ Displays: "Preparing dashboard..."
✅ Audio beep plays (800Hz sine wave, 0.5 seconds)
✅ Banner auto-dismisses after 3 seconds
✅ Page automatically reloads
✅ "Preparation Required" card appears with 5 tasks:
   - Bed Allocation
   - Ward Assignment
   - Equipment Setup
   - Staff Notification
   - Emergency Medications
✅ Response Timeline card appears
✅ Active call details displayed
```

**Step 5: Verify Acknowledgment**
```
1. Open browser console (F12) in Browser 2
2. Check Network tab → XHR/Fetch
3. Should see POST request to /emergencies/api/emergencies/{id}/acknowledge/
4. Response should be 200 OK with preparation tasks
```

## Detailed Testing Scenarios

### Scenario 1: Single Dispatch Notification

**Objective**: Verify paramedic receives notification when ambulance dispatched

**Preconditions**:
- Paramedic user logged in and idle (no active call)
- Emergency call created in dispatcher dashboard
- Ambulance available and assigned to paramedic

**Test Case**:
```
Given: Paramedic is viewing paramedic dashboard
When: Dispatcher clicks "Dispatch" and selects ambulance
Then:
  - Notification alert appears on paramedic dashboard
  - Alert displays emergency details (ID, type, location, priority)
  - Audio notification plays (800Hz beep)
  - Dashboard reloads after 3 seconds
  - "Preparation Required" card displays 5 tasks
```

**Validation Points**:
- [ ] Notification appears within 2 seconds
- [ ] All 4 details shown in alert (ID, type, location, priority)
- [ ] Audio plays once (not repeated)
- [ ] Auto-dismiss timer works (3 seconds)
- [ ] Auto-reload successful
- [ ] Preparation tasks visible after reload
- [ ] Server logs show acknowledgment endpoint called

### Scenario 2: Multiple Paramedics

**Objective**: Verify notifications only go to assigned paramedic

**Preconditions**:
- Two paramedic users logged in (paramedic1 and paramedic2)
- One emergency call created
- One ambulance assigned to paramedic1

**Test Case**:
```
Given: Both paramedics viewing their dashboards
When: Dispatcher dispatches ambulance to paramedic1
Then:
  - paramedic1 receives notification
  - paramedic2 does NOT receive notification
```

**Validation Points**:
- [ ] paramedic1 sees alert, preparation tasks, active call
- [ ] paramedic2 still sees "No Active Call"
- [ ] paramedic2 doesn't hear audio notification
- [ ] paramedic1 acknowledgment endpoint called with correct paramedic ID
- [ ] paramedic2 acknowledgment endpoint NOT called

### Scenario 3: Audio Notification Edge Cases

**Objective**: Verify audio notification works reliably

**Test Cases**:

**3A: Audio with Sound Unmuted**
```
Given: Browser volume is unmuted
When: Dispatch notification received
Then: 800Hz sine wave beep plays for 0.5 seconds
```

**3B: Audio with Sound Muted**
```
Given: Browser volume is muted
When: Dispatch notification received
Then: 
  - Audio beep plays but inaudible
  - Visual notification still appears
  - Dashboard updates normally
```

**3C: Audio Context Not Available**
```
Given: Browser doesn't support Web Audio API (unlikely)
When: Dispatch notification received
Then:
  - Graceful fallback occurs
  - Error logged in console
  - Visual notification still works
  - Dashboard updates normally
```

**3D: Multiple Dispatches**
```
Given: Paramedic receives 2+ notifications quickly
When: Two ambulances dispatched to same paramedic within 5 seconds
Then:
  - Each notification plays unique sound
  - Sounds don't overlap or interfere
  - Both notifications visible (if queued)
  - Last dispatch takes precedence for dashboard reload
```

### Scenario 4: Acknowledgment Endpoint Validation

**Objective**: Verify acknowledgment endpoint security and functionality

**Test Case 4A: Valid Request**
```
Given: Authenticated paramedic user
When: POST /emergencies/api/emergencies/{id}/acknowledge/ called
Then:
  - Response 200 OK
  - Body contains preparation_tasks array with 5 items
  - Body contains emergency details
  - Backend logs acknowledgment timestamp
```

**Test Case 4B: Unauthorized Paramedic**
```
Given: Wrong paramedic user (not assigned to call)
When: POST /emergencies/api/emergencies/{id}/acknowledge/ called
Then:
  - Response 403 Forbidden
  - Body contains error message
  - Backend does NOT log acknowledgment
```

**Test Case 4C: Unauthenticated Request**
```
Given: No authentication token
When: POST /emergencies/api/emergencies/{id}/acknowledge/ called
Then:
  - Response 401 Unauthorized
  - Redirect to login page
```

**Test Case 4D: Non-Existent Emergency**
```
Given: Valid paramedic, invalid emergency ID
When: POST /emergencies/api/emergencies/9999/acknowledge/ called
Then:
  - Response 404 Not Found
  - Body contains "Emergency call not found"
```

### Scenario 5: Dashboard State Transitions

**Objective**: Verify dashboard updates correctly when notification received

**Preconditions**:
- Paramedic logged in, dashboard loaded
- No active emergency call
- Pre-dispatch checklist visible

**Test Case**:
```
Given: Paramedic viewing "No Active Call" state
When: Dispatch notification received and page reloaded
Then:
  - "No Active Call" card is replaced with "Preparation Required" card
  - 5 preparation tasks displayed
  - Response timeline card appears
  - Active call details card shows patient info
  - Hospital destination card shows assigned hospital
  - Ambulance status updated
  - All data matches emergency call details
```

**Validation Points**:
- [ ] Old "No Active Call" state removed
- [ ] New "Preparation Required" state visible
- [ ] All 5 tasks listed with descriptions
- [ ] Timeline shows DISPATCHED status
- [ ] Patient data matches emergency call
- [ ] Hospital matches dispatcher's selection
- [ ] No layout breaks or missing elements

### Scenario 6: Preparation Cards Display

**Objective**: Verify all preparation-related UI elements render correctly

**Preconditions**:
- Paramedic has active emergency call (from dispatch notification)

**Test Case 6A: Pre-Dispatch Checklist (When Idle)**
```
Given: Paramedic idle, no active call
Then: Card displays:
  - Title: "Pre-Dispatch Preparation Checklist"
  - 4 checkboxes:
    [ ] Equipment Check - Verify all medical equipment
    [ ] Fuel Level - Ensure sufficient fuel
    [ ] Team Readiness - Confirm partner ready
    [ ] Communication Setup - Test radio/phone
```

**Test Case 6B: Preparation Required Card (When Active)**
```
Given: Paramedic has active emergency call
Then: Card displays:
  - Title: "Preparation Required"
  - Subtitle: "(Before patient arrival)"
  - 5 numbered items:
    1️⃣  Bed Allocation - description
    2️⃣  Ward Assignment - description
    3️⃣  Equipment Setup - description
    4️⃣  Staff Notification - description
    5️⃣  Emergency Medications - description
```

**Test Case 6C: Response Timeline Card**
```
Given: Paramedic has active emergency call
Then: Card displays:
  - Title: "Response Timeline"
  - 5 status steps:
    ✅ DISPATCHED - with timestamp
    ⏳ EN_ROUTE
    ⏳ ON_SCENE
    ⏳ TRANSPORTING
    ⏳ AT_HOSPITAL
  - "Response Time So Far" counter
```

### Scenario 7: WebSocket Connection

**Objective**: Verify WebSocket maintains connection for real-time updates

**Preconditions**:
- Paramedic dashboard open in browser
- Developer console open

**Test Case**:
```
Given: Paramedic dashboard loaded
When: Open Network tab → WS (WebSocket)
Then:
  - Connection to /ws/emergencies/ established
  - Status shows "101 Web Socket Protocol Handshake"
  - Connection remains open for duration of session
  - Messages received when dispatch sent (UNIT_DISPATCHED event)
```

**Validation Points**:
- [ ] WebSocket connection established on page load
- [ ] Connection URL is /ws/emergencies/
- [ ] Status 101 (protocol upgrade) visible
- [ ] Connection stays open (not closed)
- [ ] UNIT_DISPATCHED message appears in WS traffic

### Scenario 8: Browser Compatibility

**Objective**: Verify notification works across different browsers

**Test Browsers**:
- Chrome 120+ (Chromium-based)
- Firefox 121+
- Safari 17+
- Edge 120+

**For Each Browser**:
```
1. Load paramedic dashboard
2. Trigger dispatch notification (from dispatcher)
3. Verify:
   - Alert appears
   - Audio plays (if unmuted)
   - Page reloads
   - Preparation tasks display
   - No console errors
```

### Scenario 9: Network Latency

**Objective**: Verify notification resilient to slow networks

**Setup**:
- Open DevTools Network tab
- Set throttling: Slow 3G (400 kbps)

**Test Case**:
```
Given: Network throttled to Slow 3G
When: Dispatch notification sent
Then:
  - Notification still appears (delayed but visible)
  - Audio plays when network allows
  - Page eventually reloads with data
  - No timeouts or error messages
```

**Validation Points**:
- [ ] Notification appears within 5 seconds (delayed is OK)
- [ ] Audio plays when ready
- [ ] Page reloads successfully
- [ ] No 504 or connection errors
- [ ] Fallback messages visible if delayed

### Scenario 10: Rapid Multiple Dispatches

**Objective**: Verify system handles rapid dispatch sequences

**Setup**:
- Create 3 emergency calls in quick succession
- Have ambulances assigned to same paramedic

**Test Case**:
```
Given: Paramedic idle
When: Dispatch 3 ambulances in 10 seconds
Then:
  - 3 notifications appear (shown sequentially or stacked)
  - Audio plays 3 times
  - Final page reload shows last active call
  - All 3 acknowledgments logged on backend
```

**Validation Points**:
- [ ] Each notification distinct and visible
- [ ] No notification "swallowed" or missed
- [ ] Dashboard shows correct final state
- [ ] Server logs show all 3 acknowledgments

## Server-Side Validation

### Database Inspection

Check that acknowledgments are being logged:

```sql
-- Check emergency call records
SELECT id, call_id, assigned_paramedic_id, status 
FROM emergencies_emergencycall 
WHERE assigned_paramedic_id = {paramedic_id}
ORDER BY created_at DESC
LIMIT 5;
```

### Server Logs

Watch for acknowledgment messages:

```
// Expected log entries after dispatch:
INFO 2025-12-03 16:42:55 dispatch HTTP POST /emergencies/api/emergencies/25/status/ 200
INFO 2025-12-03 16:42:56 emergencies Paramedic 5 acknowledged dispatch for emergency 25
INFO 2025-12-03 16:42:57 dispatch HTTP POST /emergencies/api/emergencies/25/acknowledge/ 200
```

### API Response Validation

Test endpoint directly with cURL:

```bash
curl -X POST http://127.0.0.1:8000/emergencies/api/emergencies/25/acknowledge/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "X-CSRFToken: YOUR_CSRF_TOKEN" \
  -H "Content-Type: application/json"
```

Expected response:
```json
{
  "status": "acknowledged",
  "emergency_id": 25,
  "call_id": "CALL-2025-12-03-001",
  "preparation_tasks": [...]
}
```

## Troubleshooting During Tests

### Problem: Notification doesn't appear

**Checklist**:
1. Is WebSocket connected? (Network tab → WS)
2. Is dispatch notification actually being sent? (Check server logs)
3. Are both browsers logged in as correct users?
4. Are both pages on correct URLs?
   - Dispatcher: /dashboard/
   - Paramedic: /paramedic/

**Debug Steps**:
```javascript
// Open console in paramedic browser
// Check WebSocket connection
console.log('WebSocket readyState:', ws.readyState); // Should be 1 (OPEN)

// Manually trigger notification (for testing)
showDispatchNotification({
  call_id: 'TEST-001',
  emergency_type_display: 'Test',
  location_address: '123 Test St',
  priority_display: 'Medium'
});
```

### Problem: Audio doesn't play

**Checklist**:
1. Is browser volume unmuted?
2. Does browser support Web Audio API?
3. Has user interacted with page? (Security requirement)

**Debug Steps**:
```javascript
// Open console in paramedic browser
// Test audio context
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
console.log('AudioContext state:', audioContext.state); // Should be 'running'

// Try playing test sound
playNotificationSound();
```

### Problem: Page doesn't auto-reload

**Checklist**:
1. Check browser console for errors (F12)
2. Is JavaScript enabled?
3. Did notification function complete successfully?

**Debug Steps**:
```javascript
// Add to console
document.addEventListener('visibilitychange', () => {
  console.log('Page visibility changed:', document.hidden);
});

// Manually reload to test
location.reload();
```

### Problem: "403 Forbidden" on acknowledge

**Checklist**:
1. Is paramedic logged in? (Check /paramedic/ loads)
2. Is this the correct paramedic for the ambulance?
3. Was ambulance actually dispatched to this paramedic?

**Debug Steps**:
```javascript
// Check current user in console
fetch('/api/users/me/').then(r => r.json()).then(console.log);

// Check active call assignment
fetch('/emergencies/api/emergencies/my-active/').then(r => r.json()).then(console.log);
```

## Performance Metrics

**Expected Performance**:

| Metric | Target | Acceptable | Unacceptable |
|--------|--------|-----------|-------------|
| Notification to display | 0.5-1s | <2s | >3s |
| Audio latency | 0.2-0.5s | <1s | >2s |
| Page reload time | 0.5-1s | <2s | >3s |
| Acknowledgment endpoint response | <100ms | <500ms | >1s |
| WebSocket latency | <50ms | <200ms | >500ms |

**How to Measure**:
- Use browser DevTools Performance tab
- Measure from dispatch click to notification display
- Check Network tab for endpoint response times
- Use Network throttling for realistic conditions

## Pass/Fail Criteria

**Test Passes If**:
- ✅ Notification appears within 2 seconds of dispatch
- ✅ Audio plays exactly once per notification
- ✅ Page auto-reloads with new call data
- ✅ Preparation tasks display correctly
- ✅ Acknowledgment endpoint responds 200 OK
- ✅ Only assigned paramedic receives notification
- ✅ No console errors
- ✅ All 5 preparation tasks visible

**Test Fails If**:
- ❌ No notification appears after 5 seconds
- ❌ Wrong paramedic receives notification
- ❌ Audio plays but no visual notification
- ❌ Page reloads but shows wrong call data
- ❌ Acknowledgment endpoint returns error
- ❌ Preparation tasks missing or cut off
- ❌ Console shows JavaScript errors
- ❌ WebSocket connection drops

## Regression Testing Checklist

After any code changes, verify:

- [ ] Paramedic notification still appears on dispatch
- [ ] Audio plays without errors
- [ ] Page reloads with correct data
- [ ] Preparation cards display fully
- [ ] Acknowledgment endpoint works
- [ ] No new console errors
- [ ] WebSocket connection stable
- [ ] Multiple dispatches handled correctly
- [ ] Wrong paramedic still rejected
- [ ] Performance metrics maintained

## Quick Reference: Test Commands

**Create test emergency call via API**:
```bash
curl -X POST http://127.0.0.1:8000/emergencies/api/emergencies/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "patient_name": "Test Patient",
    "patient_age": 35,
    "patient_condition": "Test condition",
    "location_address": "123 Test St",
    "emergency_type": "TR",
    "priority": "UR",
    "hospital_destination": 1,
    "assigned_paramedic": 2
  }'
```

**Dispatch ambulance via API**:
```bash
curl -X POST http://127.0.0.1:8000/dispatch/api/dispatch/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ambulance_id": 1}'
```

## Next Steps After Testing

1. **If all tests pass**: Ready for production deployment
2. **If some tests fail**: Document failures, fix code, retest
3. **Performance optimization**: Profile slow operations
4. **Load testing**: Test with multiple paramedics/calls simultaneously
5. **User acceptance testing**: Get feedback from real paramedics
