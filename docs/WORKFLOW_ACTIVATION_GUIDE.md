# n8n Workflow Activation Guide

**Date:** November 2, 2025
**Status:** 4 workflows ready to activate

---

## Current Workflow Status

### ✅ ACTIVE (4 workflows)
1. **AIPA - Telegram Main Interface** - Main bot interface
2. **AIPA - Multi-Business Calendar Management** - Calendar operations
3. **AIPA - Email Processing with AI** - Email triage and processing
4. **AIPA - Business Intelligence & Reports** - Analytics and reports

### ⚪ INACTIVE - Ready to Activate (4 workflows)
1. **AIPA - Woody's Creations Order Processing** - Order management
2. **AIPA - Marketing Campaign Automation** - Marketing campaigns
3. **AIPA - DJ Booking Automation** - DJ booking pipeline
4. **AIPA - BMF Work Logging** - BMF work tracking

---

## Diagnostic Results

✅ **All workflows passed diagnostic checks:**
- All credentials properly configured
- All trigger nodes set up correctly
- All workflow connections defined
- No missing credential IDs
- No configuration errors

**Conclusion:** Workflows are ready to activate!

---

## How to Activate Workflows

### Step-by-Step Instructions

#### 1. Open n8n Web Interface
```
http://192.168.0.14:5678
```

#### 2. Activate Each Workflow

For each inactive workflow:

1. Click on the workflow name in the sidebar
2. The workflow editor will open
3. Look at the top-right corner for the **"Active"** toggle switch
4. Click the toggle to turn it **ON** (it should turn blue/green)
5. If successful, you'll see a confirmation message
6. If it fails, check for error messages

**Workflows to activate:**
- AIPA - Woody's Creations Order Processing
- AIPA - Marketing Campaign Automation
- AIPA - DJ Booking Automation
- AIPA - BMF Work Logging

#### 3. Verify Activation

After activating each workflow:
- The toggle should stay ON
- No error messages should appear
- The workflow should appear in the "Active Workflows" list

---

## Troubleshooting

### If a Workflow Won't Activate:

1. **Check for credential warnings:**
   - Look for red warning icons on nodes
   - Click on nodes to see if credentials are missing
   - Re-select credentials if needed

2. **Check execution history:**
   - Click "Executions" tab
   - Look for error messages
   - Address any errors shown

3. **Check webhook URLs:**
   - For webhook triggers, ensure URLs are correct
   - Verify WEBHOOK_URL environment variable is set

4. **Restart n8n (if needed):**
   ```bash
   docker restart n8n
   ```

### Common Issues:

**Issue:** Toggle won't stay ON
**Solution:** Check credentials - all credential nodes must have valid credentials assigned

**Issue:** Webhook error
**Solution:** Ensure n8n is accessible at the webhook URL (currently: http://192.168.0.14:5678)

**Issue:** Telegram webhook error
**Solution:** Telegram requires HTTPS - make sure ngrok is running or use local-only triggers

---

## Why API Activation Doesn't Work

The n8n REST API does not support direct workflow activation via PATCH/PUT methods. The API returns:
- **PATCH:** "405 Method Not Allowed"
- **PUT with active field:** "active is read-only"

This is by design in recent n8n versions. Workflows must be activated through the web UI.

---

## After Activation

### Test the Workflows

Once all workflows are active, test them via Telegram:

```
/start - Telegram interface menu
/woodys - Woody's Creations menu
/dj - DJ booking menu
/bmf - BMF work logging menu
/marketing - Marketing campaigns menu
/calendar - Calendar management
/reports - Business intelligence
/email - Email processing
```

### Monitor Executions

Check the "Executions" tab regularly to ensure workflows are running correctly:
```
http://192.168.0.14:5678/executions
```

---

## Quick Activation Checklist

- [ ] Open http://192.168.0.14:5678
- [ ] Activate: AIPA - Woody's Creations Order Processing
- [ ] Activate: AIPA - Marketing Campaign Automation
- [ ] Activate: AIPA - DJ Booking Automation
- [ ] Activate: AIPA - BMF Work Logging
- [ ] Verify all 8 workflows show as ACTIVE
- [ ] Test via Telegram bot: /start
- [ ] Test each command: /woodys, /dj, /bmf, /marketing

---

## Need Help?

Run diagnostic script again:
```bash
python check_workflow_issues.py
```

Check workflow status:
```bash
python temp_list_workflows.py
```

---

**Ready to Activate!** All workflows are properly configured and waiting for manual activation in the web UI.
