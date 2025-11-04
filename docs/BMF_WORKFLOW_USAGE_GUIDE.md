# BMF Work Logging Workflow - Usage Guide

## Workflow Structure

The BMF workflow has **2 separate entry points** (webhooks):

### Entry Point 1: Main Menu (`/bmf` command)
- **Trigger**: BMF Command Trigger (webhook)
- **Purpose**: Shows the BMF menu with options
- **Flow**: BMF Command → Show Menu → User selects option

### Entry Point 2: Hours Input (after selecting "Log hours")
- **Trigger**: Wait for Hours Input (Telegram Trigger)
- **Purpose**: Receives the hours data after user selects option 1
- **Flow**: Wait for Input → Parse Hours → Save to Database → Confirm

## How to Use

### Step 1: Send `/bmf` command
Send `/bmf` to your Telegram bot to open the BMF menu.

**Expected Response:**
```
💼 BMF Work Logging

What would you like to do?

1️⃣ Log hours worked
2️⃣ View this week's hours
3️⃣ View this month's hours
4️⃣ Generate timesheet

Reply with a number.
```

### Step 2: Select Option 1 (Log hours)
Reply with `1` or tap "1 - Log Hours" button.

**Expected Response:**
```
📝 Log Your Hours

Please provide your hours in this format:

Line 1: Hours worked (e.g., 8 or 8.5)
Line 2: Task description
Line 3: Date (optional - today/yesterday/YYYY-MM-DD)

Example:
7.5
Website development and bug fixes
today
```

### Step 3: Send Hours Data
Send a message in the format requested:
```
8
Fixed authentication system
today
```

**Expected Response:**
```
✅ Hours Logged Successfully!

📅 Date: 2025-11-02
⏱️ Hours: 8
💰 Earnings: £280
📝 Task: Fixed authentication system

Logged to BMF work log.
```

## Troubleshooting

### Error: "Please provide hours and description"

**Causes:**
1. Message format is incorrect
2. Missing hours or description
3. Sent to wrong webhook

**Solution:**
- Make sure to send hours on line 1
- Description on line 2
- Optional date on line 3
- Send AFTER selecting "Log hours" option

**Correct format:**
```
8
Task description here
```

**Incorrect formats:**
```
8 hours - Task description  ❌ (all on one line)
Task description\n8         ❌ (reversed order)
8                           ❌ (missing description)
```

### Error: "First line must be a number"

**Cause:** The first line contains text instead of a number

**Solution:** Make sure line 1 is ONLY a number:
```
8.5           ✅
eight         ❌
8 hours       ❌
```

### Error: "No input data received"

**Causes:**
1. Workflow not activated
2. Telegram webhook not configured
3. Network/connection issue

**Solution:**
1. Check workflow is ACTIVE in n8n UI
2. Check Telegram webhook is registered
3. Try sending `/bmf` again to restart the flow

## Workflow Activation

**The BMF workflow MUST be activated** for both webhooks to work:

1. Go to http://192.168.0.14:5678
2. Navigate to "BMF Work Logging" workflow
3. Toggle "Active" switch ON
4. Verify both webhooks are registered:
   - BMF Command Trigger webhook
   - Wait for Hours Input webhook

## Data Format

### Hours Worked
- Can be integer or decimal
- Examples: `8`, `7.5`, `4.25`
- Range: typically 0.5 to 12 hours

### Task Description
- Any text describing the work done
- Examples:
  - "Website development"
  - "Client meeting and proposal"
  - "Bug fixes and testing"

### Date (Optional)
- `today` (default if not specified)
- `yesterday`
- `YYYY-MM-DD` format (e.g., `2025-11-01`)

## Database Storage

Hours are saved to Supabase table: `bmf_work_logs`

**Columns:**
- `work_date` - Date of work
- `hours_worked` - Hours as decimal
- `task_description` - Description text
- `hourly_rate` - £35/hour (configurable in workflow)
- `earnings` - Calculated (hours × rate)
- `status` - 'logged'

## Current Fix Applied

**Issue Fixed:** Parse Hours Entry node now handles:
- ✅ Missing input data
- ✅ Alternative data structures
- ✅ Better error messages
- ✅ Invalid hours (non-numeric)

The workflow should now be more robust and provide clearer error messages.
