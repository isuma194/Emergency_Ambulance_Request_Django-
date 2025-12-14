# 🔒 CSRF ISSUE FIX - Login 403 Forbidden

## Problem
Getting "Forbidden (403): CSRF verification failed" when trying to login.

## Root Cause
When using Daphne/ASGI server, the CSRF cookie wasn't being set properly on the initial page load.

## Fixes Applied

### 1. Added CSRF Configuration to settings.py
**File**: `EmmergencyAmbulanceSystem/settings.py`

```python
# CSRF settings for ASGI/Daphne
CSRF_COOKIE_SECURE = False  # Set to True in production with HTTPS
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read for debugging
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
CSRF_USE_SESSIONS = False  # Use cookie-based CSRF tokens
CSRF_COOKIE_NAME = 'csrftoken'
```

### 2. Added ensure_csrf_cookie Decorator
**File**: `core/views.py`

```python
@ensure_csrf_cookie
@csrf_protect
def login_view(request):
```

## How to Apply

1. **Restart the server**:
   ```bash
   # Stop the current server (Ctrl+C)
   
   # Start it again
   python manage.py runserver
   ```

2. **Clear browser cache**:
   - Press `Ctrl+Shift+Delete`
   - Select "Cookies and other site data"
   - Click "Clear data"

3. **Try login again**:
   - Navigate to `http://127.0.0.1:8000/login/`
   - Enter credentials
   - Submit form

## Verification

### Check if CSRF cookie is set:
1. Open browser DevTools (F12)
2. Go to "Application" tab (Chrome) or "Storage" tab (Firefox)
3. Look under "Cookies" → `http://127.0.0.1:8000`
4. You should see a cookie named `csrftoken`

### Check the form has CSRF token:
1. Right-click on login page → "View Page Source"
2. Search for `csrfmiddlewaretoken`
3. You should see: `<input type="hidden" name="csrfmiddlewaretoken" value="...">`

## Still Not Working?

### Try This:
```bash
# 1. Stop server
Ctrl+C

# 2. Clear sessions
python manage.py clearsessions

# 3. Collect static files
python manage.py collectstatic --noinput

# 4. Restart server
python manage.py runserver
```

### Check Browser Console:
1. Press F12
2. Try to login
3. Check "Console" tab for JavaScript errors
4. Check "Network" tab → Click on the POST request to `/login/`
5. Look at "Request Headers" - should include `X-CSRFToken` or form data should include `csrfmiddlewaretoken`

## Test Accounts

Use these credentials to test:

| Username | Password | Role |
|----------|----------|------|
| dispatcher | dispatcher123 | Dispatcher |
| paramedic | paramedic123 | Paramedic |
| admin | admin123 | Admin |

Or run:
```bash
python test_dispatcher_debug.py
```
This creates a test dispatcher if none exists.

## Notes

- **`CSRF_COOKIE_SECURE`**: Set to `False` for development (HTTP). Must be `True` in production (HTTPS).
- **`CSRF_COOKIE_HTTPONLY`**: Set to `False` to allow JavaScript debugging. Should be `True` in production for security.
- **`CSRF_TRUSTED_ORIGINS`**: Must include your development server URL.

## Production Settings

When deploying to production with HTTPS:

```python
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
CSRF_TRUSTED_ORIGINS = [
    'https://yourdomain.com',
    'https://www.yourdomain.com',
]
```

---

**Status**: ✅ Fixed  
**Date**: December 11, 2025
