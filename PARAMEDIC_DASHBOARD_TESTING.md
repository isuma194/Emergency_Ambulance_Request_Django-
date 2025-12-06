# Paramedic Dashboard Testing Guide

## Quick Start

### 1. Access the Paramedic Interface
- URL: `http://127.0.0.1:8000/emergencies/paramedic-interface/`
- Log in as: `jane_paramedic` (or any paramedic user)
- You should see the paramedic dashboard

### 2. Understand the Layout

**Header Section:**
- Left: "Field Paramedic Interface" title
- Right: WebSocket status (green = connected) and logged-in user name

**Main Content:**
- Left Side (60%): Active call information
- Right Side (40%): Quick actions and details

**No Active Call State:**
- Shows waiting spinner
- "No Active Call - Waiting for dispatch assignment..."
- Availability toggle available
- System polls server every 10 seconds for new assignments

---

## Test Scenarios

### Test 1: Receive New Emergency Assignment

**Setup:**
1. Open browser tab 1: Paramedic interface (logged in as paramedic)
2. Open browser tab 2: Dispatcher dashboard (logged in as dispatcher)
3. Verify paramedic sees "No Active Call" state

**Execution:**
1. In dispatcher tab, create new emergency:
   - Click "Create Emergency"
   - Fill form (address, type, priority, etc.)
   - Click "Create"

2. In dispatcher tab, click "Dispatch Ambulance"
3. Select available ambulance
4. Click "Dispatch"

**Expected Results:**
1. Paramedic tab automatically reloads within 10 seconds
2. Active call card appears with:
   - Call ID and emergency type
   - Patient location
   - Patient information (if available)
   - Status: "DISPATCHED"
3. Action buttons appear:
   - EN ROUTE (enabled)
   - ON SCENE (disabled)
   - TRANSPORTING (disabled)
   - HOSPITAL (disabled)
   - BACK IN SERVICE (disabled)

**Verification:**
- [ ] Call appears automatically (or within 10 sec)
- [ ] All call details display correctly
- [ ] WebSocket indicator shows "WS: connected"
- [ ] Only EN ROUTE button is enabled
- [ ] Priority color matches emergency priority

---

### Test 2: Complete Status Workflow

**Setup:**
- Active call visible on paramedic dashboard
- Status: DISPATCHED

**Execution & Verification:**

#### Step 1: EN ROUTE
1. Click EN ROUTE button
2. Watch button show loading spinner
3. Wait for button to return to normal

**Expected:**
- [ ] Button shows loading state
- [ ] Status badge updates to "EN ROUTE"
- [ ] EN ROUTE button disabled, ON SCENE enabled
- [ ] No page reload needed

#### Step 2: ON SCENE
1. Click ON SCENE button
2. Confirm status update

**Expected:**
- [ ] Status updates to "ON SCENE"
- [ ] ON SCENE disabled, TRANSPORTING enabled

#### Step 3: TRANSPORTING
1. Click TRANSPORTING button

**Expected:**
- [ ] Status updates to "TRANSPORTING"
- [ ] TRANSPORTING disabled, HOSPITAL enabled

#### Step 4: AT HOSPITAL
1. Click HOSPITAL button
2. Confirm in dialog: "Confirm arrival at hospital?"

**Expected:**
- [ ] Confirmation dialog appears
- [ ] Status updates to "AT_HOSPITAL"
- [ ] HOSPITAL disabled, BACK IN SERVICE enabled

#### Step 5: BACK IN SERVICE
1. Click BACK IN SERVICE button
2. Confirm in dialog: "Close the call and return to service?"

**Expected:**
- [ ] Confirmation dialog appears
- [ ] Status updates to "CLOSED"
- [ ] Page reloads automatically
- [ ] Returns to "No Active Call" waiting state

---

### Test 3: GPS Location Sharing

**Setup:**
- Browser has geolocation permission granted
- Active call visible
- Location indicator shows "GPS: idle"

**Execution:**
1. Click "Share Location" button
2. Allow browser permission prompt (if appears)
3. Watch status change

**Expected Results:**
- [ ] Status changes to "GPS: acquiring..."
- [ ] Button becomes disabled
- [ ] Within 2 seconds, status shows "GPS: shared (±Xm)"
- [ ] Accuracy displayed (e.g., "±42m")
- [ ] Button re-enables after 2 seconds
- [ ] Status returns to "GPS: idle"

**Auto-GPS Sharing:**
1. Keep paramedic interface open with active call
2. Wait 15 seconds
3. Check server logs or dispatcher view for location updates

**Expected:**
- [ ] Location auto-updates every 15 seconds
- [ ] No button clicks needed
- [ ] Continuous location tracking

**Location Denied:**
1. Disable geolocation permission in browser
2. Click "Share Location" button

**Expected:**
- [ ] Status shows "GPS: User denied geolocation"
- [ ] Error message appears
- [ ] Button re-enables for retry

---

### Test 4: Availability Toggle

**Setup:**
- Paramedic dashboard open
- No active call (or disabled during active call)

**Execution:**
1. Locate "Available for dispatch" checkbox
2. Verify it's checked (enabled)
3. Click to uncheck

**Expected:**
- [ ] Checkbox becomes disabled during API call
- [ ] Brief loading state
- [ ] Checkbox updates
- [ ] Server receives availability change

**Re-Enable:**
1. Click checkbox again
2. Verify it re-enables

**Expected:**
- [ ] Checkbox becomes checked again
- [ ] Server updated
- [ ] Paramedic available for new assignments

**During Active Call:**
- [ ] Checkbox appears disabled (greyed out)
- [ ] Cannot toggle during active call
- [ ] Re-enables after call completed

---

### Test 5: Call Duration Tracking

**Setup:**
- Active call visible
- Status shows "Received: X seconds ago"

**Execution:**
1. Leave paramedic interface open
2. Watch the call duration display
3. Wait 1-2 minutes

**Expected:**
- [ ] Duration updates every second
- [ ] Format: "0 seconds ago" → "15 seconds ago" → "1 minute ago" → "2 minutes ago"
- [ ] Accurate time tracking
- [ ] No page reload needed

---

### Test 6: WebSocket Real-Time Updates

**Setup:**
- Paramedic 1 dashboard open (viewing active call)
- Paramedic 2 dashboard or dispatcher view open
- Both logged in

**Execution:**
1. In dispatcher/admin view, update emergency status
2. OR Paramedic 2 updates status
3. Watch Paramedic 1's view

**Expected:**
- [ ] WebSocket indicator shows "WS: connected"
- [ ] When status updated externally, Paramedic 1 view updates automatically
- [ ] No manual page refresh needed
- [ ] Real-time synchronization

**WebSocket Disconnect:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Disable network → Offline
4. Wait a few seconds
5. Re-enable network

**Expected:**
- [ ] WebSocket indicator changes to "WS: disconnected" (red)
- [ ] When re-enabled, indicator returns to "WS: connected" (green)
- [ ] Clear visual feedback of connection status

---

### Test 7: Invalid Status Transitions

**Setup:**
- Active call with status: ON_SCENE

**Execution:**
1. Try to click EN_ROUTE button (invalid transition from ON_SCENE)

**Expected:**
- [ ] Button briefly disables for 2 seconds
- [ ] No API call made
- [ ] Local validation prevents invalid transition
- [ ] Button re-enables

**Note:** This is client-side validation for UX feedback

---

### Test 8: Mobile Responsiveness

**Setup:**
- Browser open to paramedic interface
- Active call visible

**Execution:**
1. Resize browser to mobile width (375px)
2. Or open on actual mobile device
3. Interact with interface

**Expected:**
- [ ] Layout reorganizes to single column
- [ ] Left/right columns stack vertically
- [ ] Buttons remain accessible and clickable
- [ ] No horizontal scrolling needed
- [ ] Text remains readable
- [ ] Images scale appropriately

---

### Test 9: Emergency Images Viewing

**Setup:**
- Active emergency with images attached
- Emergency images visible in gallery

**Execution:**
1. Click on any emergency image thumbnail
2. Modal should open
3. Click modal close button or background
4. Modal closes

**Expected:**
- [ ] Thumbnail grid displays all images
- [ ] Click opens full-size modal
- [ ] Image displays in modal clearly
- [ ] Close button works
- [ ] Can click multiple images

---

### Test 10: Error Scenarios

### 10a: Lost Internet Connection Mid-Update

**Setup:**
- Active call visible
- Status update button ready

**Execution:**
1. Click status update button
2. Immediately disable network (DevTools → Offline)
3. Watch for error handling

**Expected:**
- [ ] Loading spinner briefly shows
- [ ] Error alert appears: "Failed to update status. Please try again."
- [ ] Button becomes enabled again
- [ ] UI reverts to previous state
- [ ] User can retry when connection restored

### 10b: Server Error Response

**Setup:**
- Active call visible

**Execution:**
1. If server error occurs, watch error handling

**Expected:**
- [ ] User-friendly error message
- [ ] Button re-enables for retry
- [ ] Application remains stable
- [ ] No JavaScript console errors

---

## Verification Checklist

### Basic Functionality
- [ ] Paramedic interface loads
- [ ] WebSocket connects automatically
- [ ] Header displays user name
- [ ] User name changes based on logged-in user

### Active Call Display
- [ ] All call details show correctly
- [ ] Priority colors display
- [ ] Emergency type shows with icon
- [ ] Patient information displays (if available)
- [ ] Status badge shows current status
- [ ] Call duration updates every second

### Status Transitions
- [ ] Status buttons appear when call active
- [ ] Only allowed transitions enabled
- [ ] Transitions work smoothly
- [ ] Confirmation dialogs appear for important transitions
- [ ] Loading spinner shows during update
- [ ] Status badge updates after successful change

### GPS Functionality
- [ ] Share Location button works
- [ ] GPS status updates display
- [ ] Accuracy shown in format "±Xm"
- [ ] Auto-sharing works every 15 seconds
- [ ] Error handling for denied permission
- [ ] Cleanup when no active call

### UI/UX
- [ ] Colors are consistent and clear
- [ ] Icons display correctly
- [ ] Layout responsive on all screen sizes
- [ ] Buttons accessible and responsive
- [ ] No JavaScript errors in console
- [ ] Loading states visible during API calls

### Real-Time Features
- [ ] WebSocket connects immediately
- [ ] Connection status shows correctly
- [ ] Polling works when no active call (10 sec intervals)
- [ ] New assignments appear automatically
- [ ] External updates reflected in real-time

---

## Troubleshooting

### Problem: "No Active Call" doesn't update with new assignment
**Solution:**
1. Check WebSocket indicator (should be green)
2. Manually refresh page (F5)
3. Wait up to 10 seconds (polling interval)
4. Check browser console for errors
5. Verify server is running

### Problem: GPS not working
**Solution:**
1. Check browser permission for geolocation
2. Ensure you're on HTTPS (if in production)
3. Check browser location services enabled
4. Allow browser to use location
5. Check browser console for errors

### Problem: Status buttons don't work
**Solution:**
1. Check WebSocket is connected
2. Verify you're the assigned paramedic
3. Check network tab in DevTools for 404/500 errors
4. Refresh page and try again
5. Check server logs for API errors

### Problem: Page doesn't update when dispatcher assigns call
**Solution:**
1. Check "WS: connected" indicator
2. Try manual page refresh (F5)
3. Wait up to 10 seconds (polling interval)
4. Check if correct paramedic receiving call
5. Verify ambulance was dispatched to you

### Problem: Mobile buttons too small
**Solution:**
1. Ensure browser zoom is 100% (press Ctrl+0)
2. Hold phone in landscape orientation
3. Buttons designed for touch (40px+ height)
4. Resize browser window larger

---

## Performance Notes

- Page load time: ~1-2 seconds
- Status update response: <500ms
- GPS share response: <1 second
- WebSocket reconnection: ~3-5 seconds
- Polling interval: 10 seconds (adjustable)
- Auto-GPS interval: 15 seconds (adjustable)

---

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Mobile browsers (iOS Safari 14+, Chrome Mobile 90+)

---

## Test Data

### Test Users
- **Paramedic:** jane_paramedic / password
- **Dispatcher:** dispatcher_user / password
- **Admin:** admin / password

### Test Ambulances
- TEST-AMB-001 (AVAILABLE)
- TEST-AMB-002 (AVAILABLE)
- TEST-AMB-003 (AVAILABLE)
- TEST-AMB-004 (AVAILABLE)

All test ambulances are ALS units with 2-patient capacity.

---

## Reporting Issues

When reporting issues, include:
1. Steps to reproduce
2. Expected behavior vs actual behavior
3. Browser console errors (F12 → Console tab)
4. Network errors (F12 → Network tab)
5. Server logs output
6. Browser and OS information
7. Screenshots if applicable
