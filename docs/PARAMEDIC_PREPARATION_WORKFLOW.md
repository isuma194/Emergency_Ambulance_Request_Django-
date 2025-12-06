# Paramedic Preparation Workflow Guide

## Overview

When a dispatcher assigns an ambulance to a paramedic, the paramedic receives an immediate real-time notification with emergency details and a preparation checklist. This workflow ensures hospitals are ready to receive patients before the ambulance arrives.

## Workflow Stages

### Stage 1: Dispatch Notification
When dispatcher assigns ambulance to paramedic:

1. **Dispatcher Action**: Selects ambulance for emergency call
2. **System Event**: `UNIT_DISPATCHED` event sent via WebSocket to paramedic
3. **Paramedic Receives**:
   - Visual alert (green notification banner)
   - Audio notification (800Hz sine wave beep)
   - Emergency details (ID, type, location, priority)

### Stage 2: Automatic Acknowledgment
When paramedic receives notification:

1. **System automatically calls**: `POST /emergencies/api/emergencies/{id}/acknowledge/`
2. **Backend logs**: Paramedic acknowledgment timestamp
3. **Response includes**:
   - Confirmation of acknowledgment
   - Complete emergency details
   - Preparation tasks list
   - Hospital destination
   - Dispatcher contact information

### Stage 3: Preparation Tasks
Paramedic reviews dashboard showing 5 required tasks:

1. **Bed Allocation** - Prepare suitable bed based on patient condition
2. **Ward Assignment** - Assign to appropriate ward for emergency type
3. **Equipment Setup** - Ready monitoring and diagnostic equipment
4. **Staff Notification** - Alert ward staff and notify physicians
5. **Emergency Medications** - Prepare relevant medications

## Real-Time Notification System

### Visual Components

**Notification Alert:**
```
╔════════════════════════════════════════════╗
║ 🔔 New Dispatch Assignment!                ║
║                                            ║
║ Emergency ID: 25                           ║
║ Type: Trauma/Accident                      ║
║ Location: 123 Main St, City                ║
║ Priority: High/Critical                    ║
║                                            ║
║ Preparing dashboard... [spinner]           ║
╚════════════════════════════════════════════╝
```

**Duration**: 3 seconds auto-dismiss

### Audio Notification
- **Frequency**: 800Hz sine wave
- **Duration**: 0.5 seconds
- **Volume**: 30% (0.3 gain, exponential fade out)
- **Purpose**: Ensures paramedic notices dispatch even if not watching screen

### Auto-Reload
After notification dismissed (2-3 seconds), dashboard automatically reloads to show:
- New active call details
- Ambulance assignment status
- Patient information
- Destination hospital details

## WebSocket Communication Flow

```
Dispatcher Dashboard
        ↓
[dispatch_ambulance() called]
        ↓
send_emergency_notification(event='UNIT_DISPATCHED')
        ↓
WebSocket: ParamedicConsumer.emergency_update()
        ↓
Paramedic Client receives event
        ↓
showDispatchNotification() displays alert
        ↓
playNotificationSound() plays 800Hz beep
        ↓
POST /emergencies/api/emergencies/{id}/acknowledge/
        ↓
Backend logs acknowledgment timestamp
        ↓
location.reload() refreshes dashboard
        ↓
Paramedic Dashboard shows:
- Preparation Required Card
- 5 Preparation Tasks
- Response Timeline
- Active Call Details
```

## API Endpoints

### Paramedic Dispatch Acknowledgment
**Endpoint**: `POST /emergencies/api/emergencies/{emergency_id}/acknowledge/`

**Authentication**: Required (authenticated paramedic)

**Authorization**: Only assigned paramedic can acknowledge

**Request Headers**:
```
X-CSRFToken: <csrf_token>
Content-Type: application/json
```

**Response (200 OK)**:
```json
{
  "status": "acknowledged",
  "emergency_id": 25,
  "call_id": "CALL-2025-12-03-001",
  "emergency_type": "Trauma/Accident",
  "priority": "High",
  "location": "123 Main St, City",
  "patient_name": "John Doe",
  "patient_age": 45,
  "patient_condition": "Severe head injury, conscious",
  "hospital_destination": "Central Hospital",
  "dispatcher_name": "Alice Johnson",
  "dispatcher_phone": "+1-555-1234",
  "preparation_tasks": [
    {
      "id": "bed",
      "title": "Bed Allocation",
      "description": "Prepare suitable bed based on patient condition"
    },
    {
      "id": "ward",
      "title": "Ward Assignment",
      "description": "Assign to appropriate ward for Trauma/Accident"
    },
    {
      "id": "equipment",
      "title": "Equipment Setup",
      "description": "Ready monitoring and diagnostic equipment"
    },
    {
      "id": "staff",
      "title": "Staff Notification",
      "description": "Alert ward staff and notify physicians"
    },
    {
      "id": "medications",
      "title": "Emergency Medications",
      "description": "Prepare relevant medications based on emergency type"
    }
  ]
}
```

**Error Responses**:

- **404 Not Found**: Emergency call not found
- **403 Forbidden**: User is not assigned to this call, or not a paramedic
- **401 Unauthorized**: User not authenticated

## Pre-Dispatch Preparation Checklist

When paramedic is idle (no active call), dashboard shows:

```
╔════════════════════════════════════════════╗
║ Pre-Dispatch Preparation Checklist         ║
║                                            ║
║ ☐ Equipment Check                          ║
║   Verify all medical equipment present     ║
║                                            ║
║ ☐ Fuel Level                               ║
║   Ensure ambulance has sufficient fuel     ║
║                                            ║
║ ☐ Team Readiness                           ║
║   Confirm partner is ready to depart       ║
║                                            ║
║ ☐ Communication Setup                      ║
║   Test radio and phone connectivity        ║
╚════════════════════════════════════════════╝
```

This keeps paramedics mentally prepared and ready to receive dispatch.

## Preparation Required Card

When active call assigned, shows:

```
╔════════════════════════════════════════════╗
║ Preparation Required                       ║
║ (Before patient arrival)                   ║
║                                            ║
║ 1️⃣  Bed Allocation                        ║
║    Prepare suitable bed based on condition ║
║                                            ║
║ 2️⃣  Ward Assignment                       ║
║    Assign to appropriate ward              ║
║                                            ║
║ 3️⃣  Equipment Setup                       ║
║    Ready monitoring equipment              ║
║                                            ║
║ 4️⃣  Staff Notification                    ║
║    Alert ward staff and physicians         ║
║                                            ║
║ 5️⃣  Emergency Medications                 ║
║    Prepare relevant medications            ║
╚════════════════════════════════════════════╝
```

## Response Timeline Card

Shows call workflow progression:

```
╔════════════════════════════════════════════╗
║ Response Timeline                          ║
║                                            ║
║ ✅ DISPATCHED          16:42:55           ║
║ ⏳ EN_ROUTE            --:--:--           ║
║ ⏳ ON_SCENE            --:--:--           ║
║ ⏳ TRANSPORTING        --:--:--           ║
║ ⏳ AT_HOSPITAL         --:--:--           ║
║                                            ║
║ Response Time So Far: 00:03:42             ║
╚════════════════════════════════════════════╝
```

## Notification Sound Details

**Web Audio API Implementation**:
```javascript
function playNotificationSound() {
    const audioContext = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioContext.createOscillator();
    const gainNode = audioContext.createGain();
    
    oscillator.connect(gainNode);
    gainNode.connect(audioContext.destination);
    
    oscillator.frequency.value = 800;      // 800Hz sine wave
    oscillator.type = 'sine';
    
    gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
    gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);
    
    oscillator.start(audioContext.currentTime);
    oscillator.stop(audioContext.currentTime + 0.5);
}
```

**Browser Support**: All modern browsers with Web Audio API
**Fallback**: If Web Audio API unavailable, error logged but workflow continues

## Implementation Files

**Backend Files**:
- `emergencies/views.py`: Added `paramedic_dispatch_acknowledged()` endpoint
- `emergencies/urls.py`: Route added for acknowledgment endpoint
- `emergencies/consumers.py`: WebSocket event handling for UNIT_DISPATCHED

**Frontend Files**:
- `templates/emergencies/paramedic_interface.html`: 
  - Updated `showDispatchNotification()` function
  - Added automatic acknowledgment API call
  - Pre-dispatch checklist (lines 200-250)
  - Preparation required card (lines 300-350)
  - Response timeline card (lines 350-400)
  - WebSocket event listener (lines 600-700)

## Testing the Workflow

### 1. Setup
1. Open dispatcher dashboard (admin user)
2. Open paramedic interface (paramedic user) in separate window
3. Create emergency call in dispatcher dashboard

### 2. Test Notification
1. Dispatcher clicks "Dispatch" for an ambulance
2. Observe paramedic window:
   - Green notification banner appears (3 seconds)
   - Audio beep plays (800Hz for 0.5 seconds)
   - Page reloads automatically
3. Check server logs: Acknowledgment endpoint called, timestamp recorded

### 3. Test Preparation Tasks
1. After reload, paramedic should see:
   - "Preparation Required" card with 5 tasks
   - Response timeline with DISPATCHED status
   - Call details (patient, location, hospital)
2. Paramedic can review tasks and prepare hospital

### 4. Test Audio/Visual Disabled Scenarios
1. Mute browser volume - notification should still update UI
2. Open browser console - should log "Dispatch notification received"

## Future Enhancements

**Phase 2: Preparation Status Tracking**
- Add checkboxes for paramedic to mark tasks complete
- Send preparation status updates to dispatcher in real-time
- Show preparation percentage (0%, 25%, 50%, 75%, 100%)

**Phase 3: Preparation Notes**
- Text field for paramedic to add notes
- Notes visible to dispatcher ("Ward 3B ready, Dr. Ahmed assigned")
- Timestamp for each task completion

**Phase 4: Dispatcher Dashboard Enhancement**
- Show preparation progress bar for each assigned paramedic
- Color-code: Red (0%), Orange (50%), Green (100%)
- Click to see detailed preparation status
- Time estimate when paramedic will be ready

**Phase 5: Advanced Features**
- Automatic notification to dispatcher when preparation complete
- Integration with hospital systems for bed availability
- Medication stock verification before dispatch
- Equipment status synced with IoT sensors

## Troubleshooting

**Issue**: No notification appears when dispatch sent
- **Solution**: Check WebSocket connection in browser console
- **Check**: ParamedicConsumer connected? UNIT_DISPATCHED event sent?

**Issue**: Notification appears but no sound
- **Solution**: Browser audio context may be blocked by browser
- **Workaround**: User must interact with page first (security feature)
- **Fix**: Click browser console shows error message

**Issue**: Page doesn't auto-reload after notification
- **Solution**: JavaScript error in showDispatchNotification()
- **Check**: Browser console for errors
- **Manual fix**: Page manually refreshed shows preparation tasks

**Issue**: Paramedic doesn't see "Not assigned" if ambulance wasn't dispatched to them
- **Solution**: System correctly handles - acknowledge endpoint validates paramedic match
- **Result**: 403 Forbidden if wrong paramedic tries to acknowledge

## Support Contacts

**For Technical Issues**:
- Check browser console (F12) for error messages
- Review server logs for backend errors
- Verify WebSocket connection: Network tab → WS

**For Workflow Questions**:
- Refer to this guide's "Workflow Stages" section
- Review emergency call creation process
- Understand ambulance dispatch procedure

## Related Documentation

- `docs/TESTING_GUIDE.md` - Full testing procedures
- `docs/WEBSOCKET_DEBUGGING.md` - WebSocket troubleshooting
- `docs/System_Workflow_Design.md` - Complete system architecture
