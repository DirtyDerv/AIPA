# n8n Workflows for AIPA System

## Overview
This folder contains all n8n workflows for the AI Personal Assistant system. Each workflow is saved as a JSON file that can be imported into n8n.

## Workflow List

### Core Workflows (Build These First)
1. **01-telegram-interface.json** - Main communication hub (Telegram bot)
2. **05-ai-agent-router.json** - Smart AI selection (Claude vs Gemini)
3. **02-email-processing.json** - Automated email triage (runs every 15 min)
4. **08-task-management.json** - Task creation and tracking
5. **04-daily-briefing.json** - Morning summary (8 AM daily)

### Business-Specific Workflows
6. **09-dj-booking-pipeline.json** - DJ inquiry processing
7. **10-woodys-order-manager.json** - Order management for Woody's Creations
8. **11-bmf-work-tracker.json** - Timesheet logging for BMF

### Advanced Workflows
9. **03-calendar-management.json** - Calendar operations and conflict detection
10. **06-business-strategist.json** - Weekly business reports
11. **07-marketing-manager.json** - Marketing campaign assistance
12. **09-discord-natural-language.json** - **NEW!** AI-powered Discord message processing

## Import Instructions

### Step 1: Open n8n
1. Navigate to: `https://uniterative-futile-charmain.ngrok-free.dev`
2. Sign in to your n8n instance

### Step 2: Import Workflow
1. Click **Workflows** in top menu
2. Click the **+** button or **Add Workflow**
3. Click the **⋯** (three dots menu) in top right
4. Select **Import from File**
5. Choose the JSON file from this folder
6. Click **Open**

### Step 3: Configure Credentials
After importing each workflow:
1. n8n will show warnings for missing credentials
2. Click on each node with a warning (red triangle)
3. Select the appropriate credential you set up earlier:
   - **AIPA Telegram Bot** (for Telegram nodes)
   - **AIPA Gmail** (for Gmail/Calendar/Drive nodes)
   - **AIPA Supabase DB** (for Postgres nodes)
   - **Claude API** (for Claude HTTP nodes)
   - **Gemini API** (for Gemini HTTP nodes)
4. Save the workflow

### Step 4: Activate Workflow
1. Toggle the **Active** switch in top right (should turn blue/green)
2. For trigger-based workflows (Telegram, Email Processing, Daily Briefing), activation starts them
3. For manual workflows, they run when called by other workflows

## Workflow Dependencies

Some workflows call other workflows. Import in this order:

```
1. AI Agent Router (05) ← Called by most workflows
2. Task Management (08) ← Called by Email, Calendar
3. Telegram Interface (01) ← Main entry point
4. Email Processing (02) ← Runs on schedule
5. Daily Briefing (04) ← Runs on schedule
6. Calendar Management (03)
7. DJ Booking Pipeline (09)
8. Woody's Order Manager (10)
9. BMF Work Tracker (11)
10. Business Strategist (06)
11. Marketing Manager (07)
```

## Webhook URLs

After importing workflows with webhooks, note these URLs:

### Telegram Webhook
- **Workflow**: 01-telegram-interface.json
- **Webhook Path**: `/webhook/telegram-bot`
- **Full URL**: `https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot`
- **Set in Telegram**: See `02-TELEGRAM-BOT-SETUP.md`

### Other Webhooks (if used)
- Email notifications: `/webhook/email-notification`
- Calendar webhooks: `/webhook/calendar-event`

## Testing Workflows

### Test Telegram Interface
1. Send `/start` to your Telegram bot
2. Check n8n execution log (click **Executions** in left sidebar)
3. Should see successful execution with your message

### Test Email Processing
1. Manually execute workflow (click **Execute Workflow** button)
2. Should fetch recent emails and classify them
3. Check Supabase `emails` table for results

### Test Daily Briefing
1. Manually execute to test (don't wait for 8 AM)
2. Should send briefing to Telegram
3. Verify all sections appear correctly

## Troubleshooting

### Issue: "Workflow could not be imported"
**Solution**:
- Ensure JSON file is not corrupted
- Try opening in text editor to verify valid JSON
- Re-download from repository

### Issue: "Credential not found"
**Solution**:
- Set up credentials first (see `05-N8N-CREDENTIALS.md`)
- Ensure credential names match exactly
- Reconnect OAuth credentials if expired

### Issue: "Webhook not accessible"
**Solution**:
- Check ngrok is running
- Verify webhook URL in Telegram/Google
- Test webhook with curl:
  ```bash
  curl -X POST https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot \
  -H "Content-Type: application/json" \
  -d '{"message": {"text": "test"}}'
  ```

### Issue: "Database connection failed"
**Solution**:
- Check Supabase project isn't paused
- Verify connection details in credential
- Test with simple query: `SELECT 1`

### Issue: "AI API errors"
**Solution**:
- Check API keys are valid
- Verify API quotas not exceeded
- Check request format matches API docs

## Customization

### Changing Schedule Times

**Daily Briefing Time** (default: 8 AM):
```json
// In 04-daily-briefing.json, find Cron node
"cronExpression": "0 8 * * *"  // Hour Minute Day Month DayOfWeek
// Change "8" to desired hour (24-hour format)
```

**Email Check Interval** (default: 15 min):
```json
// In 02-email-processing.json, find Cron node
"cronExpression": "*/15 * * * *"  // Every 15 minutes
// Change "15" to desired interval
```

### Adding New Business Context

If you add a new business later:

1. Add to `business_contexts` table in Supabase
2. Update email classification prompt (`ai-prompts/email-classifier.md`)
3. Update Telegram Interface switch statement
4. Add new calendar and Drive folder
5. Update Daily Briefing to include new context

### Changing AI Models

In workflows using AI:
```json
// For Claude, find HTTP Request node
"url": "https://api.anthropic.com/v1/messages"
"body": {
  "model": "claude-3-5-sonnet-20241022"  // Change model here
}

// For Gemini, find HTTP Request node
"url": "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
// Change "gemini-pro" to "gemini-pro-vision" or "gemini-ultra"
```

## Workflow Execution Limits

### Free n8n Self-Hosted
- ✅ Unlimited workflow executions
- ✅ Unlimited active workflows
- ✅ No time limits

### API Limits (External Services)
- **Claude**: ~20-30 requests/day (free tier)
- **Gemini**: 1,500 requests/day (free tier)
- **Supabase**: 50,000 DB requests/month
- **Gmail API**: 1 billion quota units/day (very high)
- **Telegram**: 30 messages/second

## Monitoring Workflows

### View Executions
1. Click **Executions** in left sidebar
2. See all workflow runs with status
3. Click any execution to view details
4. Debug failed executions by checking node outputs

### Enable Debug Mode
1. In workflow editor, click **Settings**
2. Enable **Save Execution Progress**
3. Shows intermediate results for debugging

### Set up Error Notifications
Add an "Error Trigger" node to critical workflows:
1. Add **Error Trigger** node
2. Connect to **Telegram** node
3. Send error message to yourself
4. Activates only when workflow fails

## Backup Workflows

### Export All Workflows
1. Go to **Workflows**
2. Select workflows to backup (Ctrl+Click multiple)
3. Click **⋯** > **Export**
4. Save JSON files to safe location

### Automated Backup (Recommended)
Create a workflow that:
1. Runs weekly (Cron trigger)
2. Exports all workflows via n8n API
3. Saves to Google Drive
4. Sends confirmation to Telegram

## Performance Tips

1. **Reduce API Calls**
   - Cache frequently accessed data
   - Batch operations where possible
   - Use Gemini for simple tasks (faster, cheaper)

2. **Optimize Database Queries**
   - Use indexes (already in schema)
   - Limit result sets
   - Use views for complex queries

3. **Parallel Execution**
   - Use Split In Batches for large datasets
   - Enable parallel processing in settings

4. **Error Handling**
   - Add Try/Catch blocks (Error Workflow)
   - Implement retry logic for flaky APIs
   - Log errors to database for analysis

## Version Control (Advanced)

Track workflow changes:

1. Export workflows regularly
2. Store JSON files in Git repository
3. Use meaningful commit messages
4. Tag stable versions (v1.0, v1.1, etc.)

```bash
cd AIPA/
git add n8n-workflows/
git commit -m "Update email processing workflow - added spam filter"
git tag v1.1
git push
```

## Need Help?

- **n8n Documentation**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io
- **AIPA Documentation**: See `docs/` folder
- **Troubleshooting**: See `08-TROUBLESHOOTING.md`

---

**Ready to import workflows!** Start with the core workflows and test each one before moving to the next.
