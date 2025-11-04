# AI Personal Assistant (AIPA) - Complete Setup Guide

## Overview
This is your master guide to setting up the complete AI Personal Assistant system. Follow these steps in order for a smooth setup experience.

## System Requirements
- ✅ n8n self-hosted and running at `https://uniterative-futile-charmain.ngrok-free.dev`
- ✅ ngrok tunnel active and stable
- ✅ Google account (Gmail)
- ✅ Telegram account
- ✅ Internet connection
- ✅ 2-4 hours for complete setup

---

## Setup Phases

### Phase 1: Foundation (30-45 minutes)
Set up accounts and infrastructure

### Phase 2: Integration (45-60 minutes)
Connect services and configure credentials

### Phase 3: Build Workflows (60-90 minutes)
Create n8n automation workflows

### Phase 4: Testing & Launch (30-45 minutes)
Verify everything works and go live

---

## Phase 1: Foundation Setup

### Step 1.1: Create Telegram Bot (15 minutes)
📖 **Guide**: `02-TELEGRAM-BOT-SETUP.md`

**Quick Steps**:
1. Open Telegram, find @BotFather
2. Send `/newbot` command
3. Set name: `Woody's AI PA` (or your choice)
4. Set username: `woodys_personal_assistant_bot` (must end in 'bot')
5. **Save the bot token** securely
6. Configure bot with `/setdescription` and `/setcommands`
7. Get your Telegram User ID from @userinfobot
8. **Save your User ID**

**✅ Checkpoint**: You have bot token and your Telegram User ID saved

### Step 1.2: Set Up Supabase Database (20-30 minutes)
📖 **Guide**: `04-SUPABASE-SETUP.md`

**Quick Steps**:
1. Sign up at https://supabase.com (use GitHub for quick signup)
2. Create new organization: `Woody's AI PA`
3. Create new project: `AIPA-System`
4. **Save database password** securely
5. Wait for project initialization (2-3 minutes)
6. Go to Settings > API, **save**:
   - Project URL
   - Anon public key
   - Service role key (secret!)
7. Open SQL Editor
8. Copy ALL content from `database/schema.sql`
9. Paste and execute in SQL Editor
10. Verify tables created (check Table Editor)
11. Add your user:
```sql
INSERT INTO users (telegram_id, telegram_username, first_name, role, allowed_contexts) VALUES
(123456789, 'your_username', 'Woody', 'admin', ARRAY['personal', 'woodys-creations', 'dj-business', 'bmf-work', 'pub-future']);
```
(Replace with YOUR Telegram ID)

**✅ Checkpoint**: Database created, tables exist, your user added

### Step 1.3: Organize Google Workspace (20-30 minutes)
📖 **Guide**: `03-GOOGLE-WORKSPACE-SETUP.md`

**Quick Steps**:
1. **Create Gmail Labels** (10 minutes):
   - Main: `WoodysCreations`, `DJ-Business`, `BMF-Work`, `Pub-Future`, `Personal`
   - Sub-labels: `/Urgent`, `/Orders`, `/Processed`, etc.
   - Apply colors to each main label

2. **Create Google Calendars** (10 minutes):
   - "Woody's Creations" (Green)
   - "DJ Business" (Red)
   - "BMF Work" (Orange)
   - "Pub Management" (Purple)
   - "Personal" (Blue)
   - **Save each Calendar ID** (from Settings > Integrate calendar)

3. **Set Up Google Drive Folders** (10 minutes):
   - Create root: `AI-PA-System`
   - Create subfolders for each business
   - **Save each Folder ID** (from URL: `/folders/FOLDER_ID`)

4. Update Supabase with IDs:
```sql
UPDATE business_contexts SET calendar_id = 'your-calendar-id@group.calendar.google.com' WHERE name = 'woodys-creations';
-- Repeat for each business context
UPDATE business_contexts SET drive_folder_id = 'your-folder-id' WHERE name = 'woodys-creations';
-- Repeat for each business context
```

**✅ Checkpoint**: Gmail labels organized, calendars created, Drive structured

---

## Phase 2: Integration Setup

### Step 2.1: Google Cloud OAuth Setup (15-20 minutes)
📖 **Guide**: `03-GOOGLE-WORKSPACE-SETUP.md` (Part 4)

**Quick Steps**:
1. Go to https://console.cloud.google.com
2. Create new project: `AIPA-System`
3. Enable APIs:
   - Gmail API
   - Google Calendar API
   - Google Drive API
4. Configure OAuth Consent Screen (External)
   - App name: `AIPA System`
   - Add your email
5. Create OAuth credentials:
   - Type: Web application
   - Name: `n8n AIPA`
   - Redirect URI: `https://uniterative-futile-charmain.ngrok-free.dev/rest/oauth2-credential/callback`
6. **Save Client ID and Client Secret**

**✅ Checkpoint**: Google OAuth credentials created and saved

### Step 2.2: Get AI API Keys (10-15 minutes)
📖 **Guide**: `05-N8N-CREDENTIALS.md`

**Claude API Key**:
1. Go to https://console.anthropic.com/
2. Sign in
3. Create API key: `AIPA System`
4. **Save the key** (starts with `sk-ant-`)

**Gemini API Key**:
1. Go to https://aistudio.google.com/app/apikey
2. Create API key
3. **Save the key**

**✅ Checkpoint**: Claude and Gemini API keys saved

### Step 2.3: Configure n8n Credentials (20-30 minutes)
📖 **Guide**: `05-N8N-CREDENTIALS.md`

**In n8n**:
1. Open n8n at `https://uniterative-futile-charmain.ngrok-free.dev`
2. Go to Credentials

**Create These Credentials**:

1. **Telegram Bot**:
   - Type: Telegram API
   - Name: `AIPA Telegram Bot`
   - Token: [Your bot token]

2. **Gmail OAuth**:
   - Type: Gmail OAuth2 API
   - Name: `AIPA Gmail`
   - Client ID: [From Google Cloud]
   - Client Secret: [From Google Cloud]
   - Click "Connect my account"
   - Authorize all permissions

3. **Supabase Database**:
   - Type: Postgres
   - Name: `AIPA Supabase DB`
   - Host: `db.YOUR-PROJECT-REF.supabase.co`
   - Database: `postgres`
   - User: `postgres`
   - Password: [Your database password]
   - Port: `5432`
   - SSL: Enabled

4. **Claude API**:
   - Type: Header Auth
   - Name: `Claude API`
   - Header Name: `x-api-key`
   - Value: [Your Claude API key]

5. **Gemini API**:
   - Type: Header Auth
   - Name: `Gemini API`
   - Header Name: `x-goog-api-key`
   - Value: [Your Gemini API key]

**Test Each Credential**:
- Add a test node for each
- Execute to verify connection
- Troubleshoot any errors before continuing

**✅ Checkpoint**: All 5 credentials configured and tested in n8n

### Step 2.4: Set Telegram Webhook (5 minutes)
1. Open browser, paste this URL (replace YOUR_BOT_TOKEN):
```
https://api.telegram.org/botYOUR_BOT_TOKEN/setWebhook?url=https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot
```
2. Should see: `{"ok":true,"result":true}`
3. Verify with:
```
https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo
```

**✅ Checkpoint**: Telegram webhook configured

---

## Phase 3: Build Workflows

### Step 3.1: Build Telegram Interface (45-60 minutes)
📖 **Guide**: `n8n-workflows/01-telegram-interface-BUILD-GUIDE.md`

**This is the MOST IMPORTANT workflow**

1. Create new workflow in n8n
2. Name it: `01-Telegram Interface`
3. Follow the detailed build guide step-by-step
4. Build all nodes:
   - Telegram Trigger
   - Extract Message Data
   - Validate User
   - Command Router (Switch node)
   - All command handlers (start, help, briefing, email, etc.)
   - Natural language handler (AI)
5. **Save** the workflow
6. **Test**: Send `/start` to your bot
7. **Activate** the workflow

**✅ Checkpoint**: Telegram bot responds to commands

### Step 3.2: Build Email Processing (30-45 minutes)
📖 **Guide**: `n8n-workflows/02-email-processing-BUILD-GUIDE.md`

**This runs automatically every 15 minutes**

1. Create new workflow: `02-Email Processing`
2. Follow the build guide
3. Build all nodes:
   - Schedule Trigger (every 15 min)
   - Fetch Gmail
   - Classify with AI
   - Store in database
   - Apply labels
   - Notify if urgent
4. **Test manually** first (disable schedule, add manual trigger)
5. Verify: Send yourself a test email, run workflow, check classification
6. **Activate** for automatic processing

**✅ Checkpoint**: Emails automatically processed and classified

### Step 3.3: Optional: Additional Workflows
If time permits, build these:

- **Daily Briefing** (runs at 8 AM) - Similar structure to email processing
- **Task Management** - CRUD operations for tasks
- **Calendar Management** - Scheduling and conflict detection

These can be added later once core system is working.

---

## Phase 4: Testing & Launch

### Step 4.1: Integration Testing (20 minutes)

**Test 1: Telegram Commands**
```
Send to bot: /start
Expected: Welcome message

Send to bot: /help
Expected: Command list

Send to bot: /email
Expected: Email summary (may be empty at first)

Send to bot: Hello, what can you do?
Expected: AI response
```

**Test 2: Email Processing**
```
1. Send yourself an email about Woody's Creations
2. Wait 15 minutes (or manually trigger workflow)
3. Check:
   - Email appears in Supabase emails table
   - Gmail label applied
   - If urgent, Telegram notification received
```

**Test 3: Database**
```
Run in Supabase SQL Editor:

SELECT * FROM users;
-- Should show your user

SELECT * FROM business_contexts;
-- Should show 5 contexts

SELECT * FROM emails ORDER BY created_at DESC LIMIT 5;
-- Should show recent emails (after email processing runs)

SELECT * FROM conversations ORDER BY created_at DESC LIMIT 10;
-- Should show your Telegram messages
```

**✅ Checkpoint**: All tests pass

### Step 4.2: Optimize Settings (10 minutes)

**Adjust Email Check Frequency**:
- Default: Every 15 minutes
- If too frequent: Change to 30 minutes
- If not enough: Keep at 15 minutes

**Set Daily Briefing Time**:
- Default: 8:00 AM
- Adjust to your preferred wake-up time

**Configure Notifications**:
- Decide which priorities trigger Telegram notifications
- Adjust urgency thresholds in email classifier

**✅ Checkpoint**: System configured to your preferences

### Step 4.3: Go Live! (5 minutes)

1. **Activate all workflows**
2. **Send yourself confirmation**:
   ```
   /briefing
   ```
3. **Set reminder** to check daily at first
4. **Monitor executions** in n8n for first week
5. **Adjust** based on real usage

**✅ System is LIVE! 🎉**

---

## Post-Setup Tasks

### Week 1: Monitor & Adjust
- [ ] Check email classifications are accurate
- [ ] Adjust AI prompts if needed
- [ ] Fix any workflow errors
- [ ] Add missing Gmail filters
- [ ] Adjust notification preferences

### Week 2-4: Optimize
- [ ] Build additional workflows (DJ bookings, Order management)
- [ ] Add Angie's access to Woody's Creations
- [ ] Create email templates for common responses
- [ ] Set up automated backups

### Ongoing Maintenance
- [ ] Weekly: Check API usage (stay within free tiers)
- [ ] Monthly: Clean up old data in Supabase
- [ ] Quarterly: Review and update AI prompts
- [ ] As needed: Add new business contexts

---

## Troubleshooting Guide

### Issue: Telegram bot not responding
**Diagnosis**:
1. Check ngrok is running: Visit your URL in browser
2. Check webhook: `/getWebhookInfo` API call
3. Check n8n workflow is activated
4. Check executions log for errors

**Fix**:
1. Restart ngrok if URL changed
2. Update webhook URL
3. Reconnect Telegram credential
4. Check user is in database

### Issue: Emails not being processed
**Diagnosis**:
1. Check workflow is activated
2. Check Gmail OAuth token is valid
3. Check Gemini API key is working
4. Check database connection

**Fix**:
1. Reconnect Gmail OAuth
2. Regenerate API keys if expired
3. Check Supabase isn't paused
4. Manually trigger workflow to test

### Issue: AI responses are bad
**Diagnosis**:
1. Check API keys are correct
2. Check request format
3. Review AI prompt

**Fix**:
1. Update AI prompts in `ai-prompts/` folder
2. Adjust temperature settings
3. Try different AI model
4. Add more context to prompts

### Issue: Database errors
**Diagnosis**:
1. Check Supabase project is active
2. Check credentials are correct
3. Check tables exist
4. Check RLS policies

**Fix**:
1. Wake Supabase project (free tier pauses after inactivity)
2. Re-enter password in credential
3. Re-run schema.sql if tables missing
4. Use service_role key (bypasses RLS)

---

## Success Checklist

Before considering setup complete, verify:

- [x] Telegram bot responds to `/start`
- [x] Telegram bot responds to natural language
- [x] Emails are fetched and classified
- [x] Gmail labels are applied automatically
- [x] Urgent emails trigger Telegram notifications
- [x] Database stores all data correctly
- [x] Google Calendar IDs are in database
- [x] Google Drive folders are organized
- [x] All n8n credentials work
- [x] Workflows execute without errors
- [x] You understand how to add/modify workflows

---

## Getting Help

### Documentation
- **Main README**: `README.md`
- **Setup Guides**: `docs/` folder
- **Workflow Guides**: `n8n-workflows/` folder
- **AI Prompts**: `ai-prompts/` folder

### External Resources
- **n8n Docs**: https://docs.n8n.io
- **n8n Community**: https://community.n8n.io
- **Supabase Docs**: https://supabase.com/docs
- **Telegram Bot API**: https://core.telegram.org/bots/api
- **Claude API**: https://docs.anthropic.com
- **Gemini API**: https://ai.google.dev/docs

### Common Commands
```bash
# Check ngrok status
curl https://uniterative-futile-charmain.ngrok-free.dev

# Test Telegram webhook
curl -X POST https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot -d '{"test":true}'

# Check database connection
psql "postgresql://postgres:PASSWORD@db.PROJECT-REF.supabase.co:5432/postgres" -c "SELECT 1;"
```

---

## Next Steps

### Immediate (Today)
1. Complete setup following this guide
2. Test all core functionality
3. Send yourself some test emails
4. Try various Telegram commands

### This Week
1. Use the system daily
2. Monitor workflow executions
3. Adjust settings based on usage
4. Build 1-2 additional workflows

### This Month
1. Add Angie's access
2. Build business-specific workflows (DJ, Orders, BMF)
3. Set up automated reports
4. Create email templates
5. Optimize AI prompts based on real usage

### Long Term
1. Add pub management when business opens
2. Create customer-facing chatbots
3. Implement voice interface
4. Build mobile app (if needed)
5. Scale to additional businesses

---

## Estimated Costs

### Current Setup (FREE!)
- n8n: $0 (self-hosted)
- Supabase: $0 (free tier - 500 MB database)
- Telegram: $0 (completely free)
- Claude API: $0 (free tier - 20-30 requests/day)
- Gemini API: $0 (free tier - 1,500 requests/day)
- Google APIs: $0 (generous free quotas)
- ngrok: $0 (free tier, but URL changes on restart)

**Total: $0/month**

### If You Need to Scale
- ngrok Pro: $8/month (stable URL)
- Supabase Pro: $25/month (8 GB database)
- Claude API Pro: $20/month (higher usage)
- n8n Cloud: $20/month (if not self-hosting)

**Total if scaling: ~$50-75/month**

---

## Congratulations! 🎉

You now have a fully functional AI Personal Assistant managing multiple businesses!

Your system can:
✅ Automatically triage emails
✅ Manage multiple calendars
✅ Track tasks across businesses
✅ Provide AI-powered insights
✅ Respond to natural language queries
✅ Send proactive notifications

**Welcome to the future of personal productivity!**

---

**Setup Version**: 1.0.0
**Last Updated**: 2025-11-01
**Next Review**: Check for updates monthly
