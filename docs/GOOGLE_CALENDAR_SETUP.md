# Google Calendar OAuth2 Setup Guide

## The Issue
Google Calendar OAuth2 credential needs "scopes" defined - these are permissions that tell Google what the app can access.

---

## 🔧 How to Fix

### Option 1: Set Scopes in n8n Credential

1. **Go to:** http://192.168.0.14:5678
2. **Click:** Settings → Credentials
3. **Find:** Your Google Calendar OAuth2 credential
4. **Click:** The credential to edit it
5. **Look for:** "Scopes" or "OAuth Scopes" field
6. **Add these scopes** (one per line or comma-separated):

```
https://www.googleapis.com/auth/calendar
https://www.googleapis.com/auth/calendar.events
```

**OR for full access, just use:**
```
https://www.googleapis.com/auth/calendar
```

7. **Click:** "Reconnect" or "Reauthorize" button
8. **Sign in** to Google again
9. **Grant permissions** when asked
10. **Save** the credential

---

### Option 2: Use Different Scopes (More Specific)

If you want more control, use specific scopes:

**For reading and writing events:**
```
https://www.googleapis.com/auth/calendar.events
```

**For read-only access:**
```
https://www.googleapis.com/auth/calendar.readonly
```

**For full calendar access (recommended):**
```
https://www.googleapis.com/auth/calendar
```

---

## 📋 Step-by-Step (Detailed)

### Step 1: Edit the Credential

1. Settings (gear icon) → Credentials
2. Find "Google Calendar OAuth2" credential
3. Click on it to open

### Step 2: Add Scopes

Look for a field labeled one of these:
- "Scopes"
- "OAuth Scopes"
- "Scope"
- "Permission Scopes"

**Enter:**
```
https://www.googleapis.com/auth/calendar
```

### Step 3: Reauthorize

1. Click "Connect my account" or "Reauthorize" button
2. Choose your Google account
3. Review permissions (should show "See, edit, share, and permanently delete all calendars you can access using Google Calendar")
4. Click "Allow"

### Step 4: Save

Click "Save" at the bottom

---

## 🔍 Alternative: Create New Credential

If editing doesn't work, create a new Google Calendar credential:

1. **Settings → Credentials → Add Credential**
2. Search for **"Google Calendar OAuth2"**
3. **Name it:** "Google Calendar - Full Access"
4. **Scopes:** `https://www.googleapis.com/auth/calendar`
5. **Click:** "Connect my account"
6. **Sign in** to Google
7. **Allow** permissions
8. **Save**

Then:
1. Go to Calendar Management workflow
2. Click each Google Calendar node
3. Select the NEW credential you just created
4. Save workflow
5. Reactivate

---

## 🎯 Quick Reference

**Most Common Scope (Use This):**
```
https://www.googleapis.com/auth/calendar
```

**This gives:**
- ✅ Read calendars
- ✅ Create events
- ✅ Update events
- ✅ Delete events
- ✅ Full calendar access

---

## ⚠️ Common Issues

### "Scope is invalid"
- Make sure you copied the URL exactly
- Include `https://`
- No extra spaces

### "Access denied"
- Your Google account might need to enable API access
- Try signing in with a different Google account
- Make sure you clicked "Allow" when asked for permissions

### Still not working?
- Delete the old credential
- Create a brand new one
- Make sure scopes are set BEFORE connecting

---

## 🚀 After Setting Scopes

1. **Save** the credential
2. Go back to **Calendar Management** workflow
3. **Deactivate** it (toggle off)
4. **Reactivate** it (toggle on)
5. **Test:** `/calendar` in Telegram

---

## 📝 What n8n Needs

When you create/edit a Google Calendar OAuth2 credential in n8n:

1. **Client ID** - From Google Cloud Console
2. **Client Secret** - From Google Cloud Console
3. **Scopes** - `https://www.googleapis.com/auth/calendar`
4. **Authorization** - Connect and allow permissions

If you haven't set up Google Cloud Console OAuth2 credentials yet, that's a separate step (let me know if you need that guide too).

---

**Go ahead and add the scope to your Google Calendar credential, then test again!**
