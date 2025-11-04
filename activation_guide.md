# n8n Workflow Activation Guide

## Current Status
✅ All credentials configured
⏳ All 8 workflows need to be activated manually

---

## How to Activate Workflows

### Step-by-Step Instructions

1. **Open n8n UI**
   - Go to: http://192.168.0.14:5678
   - Log in if prompted

2. **Navigate to Workflows**
   - Click "Workflows" in the left sidebar
   - You should see all 8 AIPA workflows

3. **Activate Each Workflow**
   - Click on a workflow to open it
   - Look for the toggle switch at the top (usually says "Inactive")
   - Click the toggle to activate
   - The workflow will turn green/active

4. **Verify Activation**
   - Check for any error messages
   - If there are credential issues, click "Open" on the error to fix

---

## Recommended Activation Order

Activate workflows in this order to test dependencies properly:

### ✅ Priority 1: Core System
**[ ] 1. AIPA - Telegram Main Interface**
- **Why first:** This is your main command interface
- **Test after activation:** Send `/start` to your Telegram bot
- **Expected response:** Menu showing all available commands

---

### ✅ Priority 2: Simple Workflows
**[ ] 2. AIPA - Business Intelligence & Reports**
- **Dependencies:** Supabase, Telegram
- **Test:** Send `/reports` command

**[ ] 3. AIPA - BMF Work Logging**
- **Dependencies:** Supabase, Telegram
- **Test:** Send `/bmf` command
- **What it does:** Track work hours for BMF job

---

### ✅ Priority 3: Business Workflows
**[ ] 4. AIPA - Woody's Creations Order Processing**
- **Dependencies:** Gmail, Supabase, Telegram
- **Test:** Send `/woodys` command
- **What it does:** Manage custom woodwork orders

**[ ] 5. AIPA - DJ Booking Automation**
- **Dependencies:** Supabase, Telegram
- **Test:** Send `/dj` command
- **What it does:** Handle DJ booking requests

---

### ✅ Priority 4: Advanced Workflows
**[ ] 6. AIPA - Multi-Business Calendar Management**
- **Dependencies:** Google Calendar, Supabase, Telegram
- **Test:** Send `/calendar` command
- **Watch out:** Needs Google Calendar OAuth configured

**[ ] 7. AIPA - Email Processing with AI**
- **Dependencies:** Gmail, Supabase, Telegram
- **Triggers automatically:** Checks Gmail every minute
- **What it does:**
  - Classifies emails by business (Woody's, DJ, BMF, Pub)
  - Uses AI to analyze and route emails
  - Creates draft responses for important emails
  - Sends Telegram notifications
- **Watch out:**
  - Needs Gmail labels created: Label_Woodys, Label_DJ, Label_BMF, Label_Pub
  - Will start processing immediately when activated

**[ ] 8. AIPA - Marketing Campaign Automation**
- **Dependencies:** Supabase, Telegram
- **Test:** Send `/marketing` command
- **What it does:** Generate marketing content with AI

---

## Troubleshooting Common Issues

### Issue: "Node is missing credentials"
**Solution:**
1. Click the red warning icon on the node
2. Click "Select credential"
3. Choose your configured credential from the dropdown
4. Save the workflow

### Issue: "Webhook is already taken"
**Solution:**
- Only one Telegram webhook can be active at a time
- If you see this, deactivate other Telegram workflows first
- Activate them one by one

### Issue: "Gmail labels not found"
**Solution for Email Processing workflow:**
1. Open Gmail
2. Create these labels:
   - Label_Woodys
   - Label_DJ
   - Label_BMF
   - Label_Pub

### Issue: "Table does not exist" (Supabase error)
**Solution:**
- Your Supabase database needs these tables:
  - `emails`
  - `woodys_orders`
  - `dj_bookings`
  - `bmf_work_logs`
  - `calendar_events`
- Run your database migration scripts

---

## Testing Your Workflows

### 1. Test Telegram Main Interface
```
Send to your Telegram bot:
/start

Expected response:
Welcome message with menu of all commands
```

### 2. Test Individual Business Commands
```
/woodys - Woody's Creations menu
/dj - DJ business menu
/bmf - BMF work logging menu
/calendar - Calendar management
/reports - Business intelligence
/marketing - Marketing tools
```

### 3. Test Email Processing (if activated)
```
Send yourself a test email mentioning:
- "Woody's Creations" or "custom sign"
- "DJ booking" or "event"
- Check if it gets labeled and you get a Telegram notification
```

---

## Quick Reference

| Workflow | ID | Command | Main Purpose |
|----------|-----|---------|--------------|
| Telegram Main Interface | srek2IWntwYinVeg | `/start` | Command center |
| Business Intelligence | JmRpF50T7syjavyx | `/reports` | Analytics |
| BMF Work Logging | cUpfgkHJrjGXpdaY | `/bmf` | Track work hours |
| Woody's Orders | 0omUZ8aqkKBhaauz | `/woodys` | Order management |
| DJ Booking | b1yMD7Z3YrORGygA | `/dj` | Booking management |
| Calendar Management | UjgOOdgTl1f6aCNR | `/calendar` | Multi-calendar |
| Email Processing | 3qUHiaT1cyqJkkIM | Auto | Email AI classification |
| Marketing | JeMfeB4VSArFk89X | `/marketing` | Campaign generation |

---

## After Activation Checklist

- [ ] All 8 workflows show "Active" status
- [ ] No red error icons on any workflow
- [ ] Telegram bot responds to `/start`
- [ ] Each business command (`/woodys`, `/dj`, `/bmf`) works
- [ ] Email processing receives and labels test email
- [ ] Telegram notifications arrive for important events

---

## Need Help?

If you run into issues:
1. Check the workflow's execution log (click "Executions" tab)
2. Look for red error messages
3. Verify credentials are still valid
4. Make sure database tables exist
5. Check Gmail labels are created

**Pro Tip:** Activate workflows one at a time and test each before moving to the next!

---

**Last Updated:** 2025-11-02
**Status:** Ready for manual activation
