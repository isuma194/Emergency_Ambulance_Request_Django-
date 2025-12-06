# Paramedic Dashboard Improvements

## Overview

The paramedic interface has been significantly enhanced with a modern, responsive layout and improved user experience for field operations.

## Key Improvements

### 1. **Responsive Two-Column Layout**
- **Left Column (60% width)**: Main active call information
- **Right Column (40% width)**: Quick actions and detailed information cards
- Automatically adjusts to mobile devices with full-width single column

### 2. **Enhanced Header**
- Clear title with icon: "Field Paramedic Interface"
- WebSocket connection status indicator (real-time color updates)
- Current user display with full name
- Better visual hierarchy

### 3. **Active Call Display (Redesigned)**

#### Call Header Section
- Color-coded alert based on priority level
- Call ID and Emergency Type with icons
- Priority badge with visual color coding
- Clear emergency classification

#### Location Section
- Street address display
- GPS coordinates (when available)
- Clean, scannable format for quick reference

#### Description
- Patient condition and situation context
- Formatted with warning background color for visibility

#### Patient Information Card
- Structured table format for clarity
- Patient name, age, and medical condition
- All patient details in one place

#### Current Status Display
- Large status badge showing current emergency status
- Call received time with automatic duration tracking
- Updates every second to show elapsed time
- Format: "Received: X minutes ago"

### 4. **Improved Action Buttons**
All status transition buttons reorganized for workflow:

| Button | Action | Icon | Color |
|--------|--------|------|-------|
| EN ROUTE | Paramedic is heading to scene | 🚗 | Primary |
| ON SCENE | Paramedic arrived at location | 🏥 | Danger |
| TRANSPORTING | Patient being transported to hospital | 🚑 | Warning |
| HOSPITAL | Arrived at hospital destination | 🏢 | Success |
| BACK IN SERVICE | Call complete, returning to service | ✓ | Secondary |

**Features:**
- Buttons arranged in 2-column grid for accessibility
- Disabled states during update (prevents double-clicks)
- Loading spinner while updating status
- Confirmation dialogs for critical transitions (AT_HOSPITAL, CLOSED)
- Visual feedback during API calls

### 5. **Quick Actions Card**
- **Share Location Button**: One-click GPS sharing
  - Shows acquisition status (acquiring, shared, failed)
  - Displays accuracy radius (e.g., "±42m")
  - Auto-shares every 15 seconds when active call exists
  
- **Availability Toggle**: 
  - Simple checkbox switch
  - Disabled during active call
  - Instant API feedback
  - Shows availability status clearly

### 6. **Assigned Ambulance Information Card**
Displays (when active call exists):
- Unit number/identifier
- Vehicle type (ALS/BLS)
- Current status
- Patient capacity
- Quick reference format

### 7. **Dispatcher Contact Card**
Shows:
- Dispatcher name
- Clickable phone number (tel: link)
- Direct communication reference
- Builds paramedic-dispatcher relationship

### 8. **Hospital Destination Card**
- Destination hospital name
- Quick reference for patient handoff
- Visible only when hospital assigned

### 9. **Emergency Images Section**
- Thumbnail grid of emergency scene images
- Click to view in full-size modal
- Better image organization than before
- Scrollable gallery format

### 10. **No Active Call State**
When waiting for assignment:
- Large, friendly "No Active Call" icon
- Waiting message with animated spinner
- Availability toggle available
- Clear indication of idle state

## Technical Features

### Real-Time Updates
- **WebSocket Connection**: Persistent connection for real-time emergency updates
- **WebSocket Indicator**: Shows connection status (green=connected, red=disconnected)
- **Auto-polling**: 10-second poll for new assignments when idle
- **Event-driven Updates**: Automatic reload when new call received

### GPS & Location Tracking
- **One-Click Sharing**: Manual GPS share button
- **Auto-Sharing**: Every 15 seconds when active call exists
- **Accuracy Display**: Shows GPS accuracy radius
- **Error Handling**: Clear error messages if geolocation fails
- **Cleanup**: Auto-stops on page unload

### Status Validation
- **Allowed Transitions Map**: Prevents invalid status changes
  - DISPATCHED → EN_ROUTE
  - EN_ROUTE → ON_SCENE
  - ON_SCENE → TRANSPORTING
  - TRANSPORTING → AT_HOSPITAL
  - AT_HOSPITAL → CLOSED
- **Client-side Validation**: Instant feedback without server calls
- **Confirmation Dialogs**: Confirm critical transitions
- **Button State Management**: Buttons disabled during updates

### Call Duration Tracking
- **Automatic Updates**: Every 1 second
- **Human-Readable Format**: 
  - "25 seconds ago"
  - "3 minutes ago"
  - "1 hour 15 minutes ago"
- **Real-time Display**: Updates while paramedic views call

### Error Handling
- **Graceful Degradation**: UI works even if API fails
- **Status Restoration**: Rolls back UI if update fails
- **User Feedback**: Clear error messages and alerts
- **Retry Capability**: Manual button retry after failure

## UI/UX Enhancements

### Color Coding
- **Primary (Blue)**: Normal actions (EN ROUTE)
- **Danger (Red)**: On-scene actions (ON SCENE)
- **Warning (Yellow)**: Transport actions (TRANSPORTING)
- **Success (Green)**: Hospital arrival (HOSPITAL)
- **Secondary (Gray)**: Completion (BACK IN SERVICE)
- **Priority Levels**: Color-coded alert levels (CRITICAL=red, HIGH=yellow, etc.)

### Responsive Design
- **Desktop**: Two-column layout (60/40 split)
- **Tablet**: Stacked responsive columns
- **Mobile**: Full-width single column
- **Touch-friendly**: Larger button targets

### Accessibility
- **ARIA Labels**: Screen reader support
- **Color + Icons**: Don't rely on color alone
- **Keyboard Navigation**: Full keyboard support
- **Clear Labels**: All buttons and controls labeled

### Performance
- **Minimal API Calls**: Only necessary requests
- **Debounced Updates**: Prevents rapid-fire requests
- **Efficient Polling**: 10-second intervals (not too frequent)
- **Lazy Loading**: Images load on demand

## API Endpoints Used

1. **GET /api/emergencies/my-active/**
   - Polls for active emergency assignment
   - Called every 10 seconds when idle

2. **PATCH /api/emergencies/{id}/status/**
   - Updates emergency status
   - Called when paramedic changes status

3. **POST /dispatch/api/ambulances/{id}/location/**
   - Shares GPS location
   - Called on-demand and every 15 seconds (auto-share)

4. **POST /core/api/paramedics/toggle-availability/**
   - Toggles paramedic availability
   - Called on switch toggle

## WebSocket Events

### Incoming Events
- **emergency_update**: New emergency assigned or status changed
  - Triggers page reload to show updated call
  - Real-time synchronization across paramedics

## Browser Requirements

- **Geolocation API**: For GPS sharing (HTTPS required in production)
- **WebSocket Support**: Real-time features
- **Bootstrap 5**: CSS framework
- **Font Awesome 6**: Icons
- **Modern Browser**: Chrome, Firefox, Safari, Edge (recent versions)

## Testing the Dashboard

### Test Scenarios

1. **New Assignment**
   - Dispatcher creates emergency and assigns ambulance
   - Paramedic sees call appear in real-time
   - Click "EN ROUTE"

2. **Status Transitions**
   - Complete workflow: DISPATCHED → EN_ROUTE → ON_SCENE → TRANSPORTING → AT_HOSPITAL → CLOSED
   - Each transition validates against allowed transitions
   - Confirmation required for final transitions

3. **GPS Sharing**
   - Click "Share Location" button
   - Location acquired and sent to server
   - Accuracy displayed (e.g., "±42m")
   - Auto-shares every 15 seconds during active call

4. **Idle Waiting**
   - No active call shows waiting state
   - Spinner animates
   - Availability toggle available
   - System polls for new assignments every 10 seconds

5. **WebSocket Connection**
   - Check WS indicator at top right
   - Should show "WS: connected" (green)
   - Watch for real-time updates from other clients

## Files Modified

- `templates/emergencies/paramedic_interface.html` - Complete redesign with new layout and enhanced features

## Future Enhancements

1. **Map Integration**: Show location on map
2. **Voice Commands**: Voice-activated status updates
3. **Offline Mode**: Queue status updates when offline
4. **Call History**: View completed calls
5. **Notes Section**: Add notes during call
6. **Vital Signs Integration**: Display patient vital signs if available
7. **Hospital Bed Availability**: Show bed availability at destination
8. **Route Navigation**: Integrated route to scene/hospital
9. **Photo Capture**: Take photos directly in app
10. **Incident Classification**: Quick-classify incident type

## Known Limitations

1. **In-Memory WebSocket Layer**: Uses in-memory channels (development mode)
   - Doesn't work across multiple server processes
   - For production: Use Redis channel layer
   
2. **GPS Accuracy**: Depends on device and location
   - Outdoor accuracy typically ±5-10m
   - Indoor accuracy may be ±30-50m
   
3. **Offline Handling**: Limited offline support
   - App requires internet connection
   - Status updates require active connection

## Support

For issues or feature requests:
1. Check browser console (F12) for JavaScript errors
2. Verify WebSocket connection status indicator
3. Check API endpoints are responding
4. Ensure geolocation permission is granted
5. Review Django server logs for backend errors
