# Telegram Bot Setup Guide

## Overview
This guide walks you through creating a Telegram bot that will serve as the primary interface for your AI Personal Assistant system.

## Prerequisites
- Active Telegram account
- Telegram app installed (mobile or desktop)
- n8n instance running at `https://uniterative-futile-charmain.ngrok-free.dev`

---

## Step 1: Create Your Bot with BotFather

### 1.1 Open Telegram and Find BotFather
1. Open Telegram app
2. Search for `@BotFather` in the search bar
3. Start a chat with BotFather (verified account with blue checkmark)

### 1.2 Create New Bot
1. Send the command: `/newbot`
2. BotFather will ask for a **name** for your bot
   - Example: `Woody's AI PA`
   - This is the display name users will see
3. BotFather will then ask for a **username**
   - Must end in `bot` (e.g., `woodys_ai_pa_bot`)
   - Must be unique across all Telegram
   - Suggestion: `woodys_personal_assistant_bot`

### 1.3 Save Your Bot Token
After creation, BotFather will provide:
```
Done! Congratulations on your new bot. You will find it at t.me/woodys_personal_assistant_bot. You can now add a description, about section and profile picture for your bot, see /help for a list of commands.

Use this token to access the HTTP API:
1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890

Keep your token secure and store it safely, it can be used by anyone to control your bot.
```

**IMPORTANT**:
- Copy this token immediately and store it securely
- This is your `BOT_TOKEN` - you'll need it for n8n configuration
- Never share this token publicly (GitHub, Discord, etc.)
- If compromised, revoke and regenerate using `/token` command with BotFather

---

## Step 2: Configure Bot Settings

### 2.1 Set Bot Description
```
/setdescription
```
Then select your bot and enter:
```
Your AI Personal Assistant managing multiple businesses: Woody's Creations, DJ services, BMF work, and personal life. Powered by Claude AI and Gemini.
```

### 2.2 Set About Text
```
/setabouttext
```
Then select your bot and enter:
```
AI PA System - Multi-business personal assistant with intelligent email triage, calendar management, task tracking, and business insights.
```

### 2.3 Set Bot Commands (Optional but Recommended)
```
/setcommands
```
Then select your bot and paste:
```
start - Initialize the PA system
context - Switch business context
briefing - Get daily summary
email - Email triage overview
calendar - Today's schedule
tasks - View and manage tasks
report - Business insights and metrics
help - Show available commands
```

### 2.4 Set Profile Picture (Optional)
1. Use `/setuserpic` command
2. Select your bot
3. Upload an image (512x512 px recommended)
4. Suggestion: AI assistant icon or your business logo

### 2.5 Enable Inline Mode (For Future Features)
```
/setinline
```
Select your bot and set inline placeholder text:
```
Search tasks, emails, or ask a question...
```

---

## Step 3: Get Your Telegram User ID

### 3.1 Find Your User ID
1. Open a chat with `@userinfobot`
2. Send any message or `/start`
3. The bot will reply with your user information:
   ```
   User ID: 123456789
   First name: Woody
   Username: @woodys_username
   ```
4. **Save your User ID** - you'll need this for database setup

### 3.2 Add User to Database
After setting up Supabase, you'll manually add your user record:
```sql
INSERT INTO users (telegram_id, telegram_username, first_name, role, allowed_contexts) VALUES
    (123456789, 'woodys_username', 'Woody', 'admin', ARRAY['personal', 'woodys-creations', 'dj-business', 'bmf-work', 'pub-future']);
```

---

## Step 4: Configure Webhook in n8n

### 4.1 Webhook URL Structure
Your Telegram webhook will use this URL format:
```
https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot
```

### 4.2 Set Webhook via BotFather API
You have two options to set the webhook:

**Option A: Using Browser (Easiest)**
1. Replace `YOUR_BOT_TOKEN` and `YOUR_WEBHOOK_URL` in this URL:
   ```
   https://api.telegram.org/bot YOUR_BOT_TOKEN/setWebhook?url=YOUR_WEBHOOK_URL
   ```
2. Example:
   ```
   https://api.telegram.org/bot1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890/setWebhook?url=https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot
   ```
3. Open this URL in your browser
4. You should see:
   ```json
   {"ok":true,"result":true,"description":"Webhook was set"}
   ```

**Option B: Using n8n Telegram Trigger Node (Recommended)**
1. In n8n, add a **Telegram Trigger** node
2. It will automatically handle webhook setup
3. Just provide your bot token
4. n8n manages the webhook registration

### 4.3 Verify Webhook Status
Check if webhook is set correctly:
```
https://api.telegram.org/botYOUR_BOT_TOKEN/getWebhookInfo
```

Expected response:
```json
{
  "ok": true,
  "result": {
    "url": "https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot",
    "has_custom_certificate": false,
    "pending_update_count": 0,
    "max_connections": 40
  }
}
```

---

## Step 5: Test Your Bot

### 5.1 Start Chat with Your Bot
1. In Telegram, search for your bot username (e.g., `@woodys_personal_assistant_bot`)
2. Click **Start** button
3. Your bot should respond (once n8n workflow is configured)

### 5.2 Initial Test Messages
Try these commands once your n8n workflow is set up:
- `/start` - Should initialize and greet you
- `/help` - Should show available commands
- `Hello` - Should get a response from the AI

### 5.3 Troubleshooting First Connection
If bot doesn't respond:
1. Check n8n workflow execution logs
2. Verify webhook is set correctly (Step 4.3)
3. Ensure ngrok tunnel is active
4. Check bot token is correct in n8n credentials
5. Review Telegram Trigger node configuration

---

## Step 6: Security Best Practices

### 6.1 Bot Token Security
- ✅ Store token in n8n credentials (not hardcoded in workflows)
- ✅ Use environment variables if possible
- ❌ Never commit token to Git
- ❌ Never share token in screenshots or documentation

### 6.2 User Access Control
Your bot should verify user Telegram ID before processing:
```javascript
// In n8n Function node
const allowedUsers = [123456789]; // Your Telegram ID
const userTelegramId = $json.message.from.id;

if (!allowedUsers.includes(userTelegramId)) {
    return [{
        json: {
            chatId: $json.message.chat.id,
            text: "⛔ Unauthorized access. This bot is private."
        }
    }];
}
```

### 6.3 Rate Limiting
Telegram allows:
- 30 messages per second to different users
- 1 message per second to the same user

n8n can handle this automatically, but be aware for high-volume scenarios.

---

## Step 7: Bot Credentials in n8n

### 7.1 Create Telegram Credential
1. In n8n, go to **Credentials** > **New**
2. Search for "Telegram"
3. Select **Telegram API**
4. Enter your bot token from Step 1.3
5. Click **Save**
6. Name it: `AIPA Telegram Bot`

### 7.2 Test Credential
1. Add a **Telegram** node to any workflow
2. Select your saved credential
3. Choose operation: "Send Message"
4. Enter your Telegram User ID (from Step 3.1)
5. Enter test message: "Bot credential test"
6. Execute node
7. Check Telegram for message

---

## Step 8: Angie's Access (Future)

### 8.1 Get Angie's Telegram User ID
1. Have Angie open chat with `@userinfobot`
2. Get her User ID
3. Add to database:
```sql
INSERT INTO users (telegram_id, telegram_username, first_name, role, allowed_contexts) VALUES
    (987654321, 'angies_username', 'Angie', 'user', ARRAY['personal', 'woodys-creations']);
```

### 8.2 Update n8n User Verification
Add Angie's ID to allowed users list in workflows:
```javascript
const allowedUsers = [
    123456789,  // Woody (admin)
    987654321   // Angie (user)
];
```

---

## Bot Features Checklist

Once fully configured, your bot will support:

### Commands
- ✅ `/start` - Onboarding and initialization
- ✅ `/context` - Switch business context
- ✅ `/briefing` - Daily summary (emails, calendar, tasks)
- ✅ `/email` - Email triage and urgent items
- ✅ `/calendar` - Today's schedule
- ✅ `/tasks` - Task list by context
- ✅ `/report` - Weekly business insights
- ✅ `/help` - Command reference

### Natural Language Processing
- ✅ "What's on my calendar today?"
- ✅ "Show urgent emails for Woody's Creations"
- ✅ "Create task: Follow up with DJ inquiry"
- ✅ "How many bookings this month?"
- ✅ "Schedule production time for order WC20251101-0042"

### Interactive Features
- ✅ Inline keyboard buttons for quick actions
- ✅ Callback query handling for button clicks
- ✅ File upload support (for designs, invoices, etc.)
- ✅ Voice message support (future: transcribe and process)
- ✅ Location sharing (for venue addresses)

---

## Common Issues & Solutions

### Issue: Bot doesn't respond to commands
**Solutions:**
1. Verify webhook is set: `/getWebhookInfo`
2. Check ngrok is running and tunnel is active
3. Review n8n execution logs for errors
4. Ensure Telegram Trigger node is active
5. Test with curl:
   ```bash
   curl -X POST https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot \
   -H "Content-Type: application/json" \
   -d '{"test": true}'
   ```

### Issue: "Unauthorized" error in n8n
**Solutions:**
1. Regenerate bot token from BotFather
2. Update credential in n8n
3. Reset webhook with new token
4. Restart n8n workflows

### Issue: ngrok tunnel URL changed
**Solutions:**
1. Get new ngrok URL
2. Update webhook URL:
   ```
   https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=NEW_NGROK_URL
   ```
3. Update n8n Telegram Trigger node if needed
4. Consider ngrok paid plan for stable URL

### Issue: Webhook timeout errors
**Solutions:**
1. Telegram webhooks timeout after 60 seconds
2. For long-running tasks, respond immediately with "Processing..."
3. Use n8n "Respond to Webhook" node early
4. Process heavy tasks asynchronously
5. Send result as new message when ready

---

## Next Steps

After completing Telegram bot setup:
1. ✅ Bot created and token saved
2. ✅ Webhook configured
3. ✅ User ID obtained and saved
4. → Continue to: `03-GOOGLE-WORKSPACE-SETUP.md`
5. → Then configure: `05-N8N-CREDENTIALS.md`
6. → Finally import: n8n workflows

---

## Quick Reference

### Important Information to Save
```
Bot Username: @woodys_personal_assistant_bot
Bot Token: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
Telegram User ID (Woody): 123456789
Webhook URL: https://uniterative-futile-charmain.ngrok-free.dev/webhook/telegram-bot
```

### Useful BotFather Commands
- `/mybots` - List all your bots
- `/token` - Regenerate token (revokes old one)
- `/setname` - Change bot display name
- `/setdescription` - Update description
- `/setcommands` - Update command list
- `/deletebot` - Permanently delete bot

### Telegram API Documentation
- Official: https://core.telegram.org/bots/api
- n8n Telegram Docs: https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.telegram/

---

**Setup Complete!** Your Telegram bot is ready to be integrated with n8n workflows.
