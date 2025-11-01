# n8n Credentials Configuration Guide

## Overview
This guide shows you how to configure all credentials needed for the AI PA system in n8n. You'll need credentials for Telegram, Google services, Supabase, Claude, and Gemini.

## Prerequisites
- n8n installed and running at `https://uniterative-futile-charmain.ngrok-free.dev`
- Completed previous setup guides (Telegram, Google, Supabase)
- All API keys and tokens saved from previous steps

---

## Accessing Credentials Manager

1. Open n8n at `https://uniterative-futile-charmain.ngrok-free.dev`
2. Click your profile icon (bottom left)
3. Select **Credentials**
4. Or go directly to: `https://uniterative-futile-charmain.ngrok-free.dev/credentials`

---

## Credential 1: Telegram Bot API

### Setup
1. Click **Add Credential** > Search "Telegram"
2. Select **Telegram API**
3. Fill in:
   - **Credential name**: `AIPA Telegram Bot`
   - **Access Token**: Your bot token from BotFather
     ```
     Example: 1234567890:ABCdefGHIjklMNOpqrsTUVwxyz1234567890
     ```
4. Click **Save**

### Test
1. Add a **Telegram** node to any workflow
2. Select operation: **Send Message**
3. Select this credential
4. Enter your Telegram user ID (from @userinfobot)
5. Message: `Credential test successful`
6. Execute node - you should receive the message

---

## Credential 2: Gmail OAuth2

### Setup
1. Click **Add Credential** > Search "Gmail"
2. Select **Gmail OAuth2 API**
3. Fill in:
   - **Credential name**: `AIPA Gmail`
   - **Client ID**: From Google Cloud Console (Part 4.4 of Google Workspace guide)
   - **Client Secret**: From Google Cloud Console
   - **Auth URI**: `https://accounts.google.com/o/oauth2/v2/auth`
   - **Token URI**: `https://oauth2.googleapis.com/token`
   - **Auth Provider X509 Cert URL**: `https://www.googleapis.com/oauth2/v1/certs`
4. Click **Connect my account**
5. Sign in with your Gmail account
6. Grant all requested permissions (Gmail, Calendar, Drive)
7. Click **Save**

### Important Notes
- The OAuth redirect must match: `https://uniterative-futile-charmain.ngrok-free.dev/rest/oauth2-credential/callback`
- If ngrok URL changes, update in Google Cloud Console
- Token refreshes automatically

### Test
1. Add **Gmail** node
2. Operation: **Get All Messages**
3. Select this credential
4. Limit: 1
5. Execute - should return your latest email

---

## Credential 3: Google Calendar OAuth2

### Setup
**Option A: Reuse Gmail OAuth (Recommended)**
If you granted Calendar permissions during Gmail OAuth, use the same credential:
1. When adding **Google Calendar** node
2. Select credential: `AIPA Gmail`
3. n8n automatically uses the same OAuth token

**Option B: Separate Credential**
1. Click **Add Credential** > Search "Google Calendar"
2. Select **Google Calendar OAuth2 API**
3. Use same Client ID and Secret as Gmail
4. Connect and authorize

### Test
1. Add **Google Calendar** node
2. Operation: **Get All Calendars**
3. Execute - should list all your calendars

---

## Credential 4: Google Drive OAuth2

### Setup
Same as Calendar - can reuse the Gmail OAuth credential.

1. When adding **Google Drive** node
2. Select credential: `AIPA Gmail`
3. OAuth token works for Drive too

### Test
1. Add **Google Drive** node
2. Operation: **List Folders**
3. Execute - should list your Drive folders

---

## Credential 5: Supabase (PostgreSQL)

### Setup
1. Click **Add Credential** > Search "Postgres"
2. Select **Postgres**
3. Fill in:
   - **Credential name**: `AIPA Supabase DB`
   - **Host**: `db.YOUR-PROJECT-REF.supabase.co`
     - Get from Supabase > Settings > Database > Host
   - **Database**: `postgres`
   - **User**: `postgres`
   - **Password**: Your database password from Supabase setup
   - **Port**: `5432`
   - **SSL**: Enable (toggle ON)
4. Click **Save**

### Test
1. Add **Postgres** node
2. Operation: **Execute Query**
3. Query: `SELECT * FROM business_contexts`
4. Execute - should return 5 business contexts

---

## Credential 6: Claude API (HTTP Request Method)

Claude doesn't have a native n8n node, so we'll use HTTP Request.

### Setup
1. Get your Claude API key:
   - Go to: https://console.anthropic.com/
   - Sign in with your Claude Pro account
   - Navigate to **API Keys**
   - Click **Create Key**
   - Name it: `AIPA System`
   - Copy the key (starts with `sk-ant-`)

2. In n8n, click **Add Credential** > Search "Header Auth"
3. Select **Header Auth**
4. Fill in:
   - **Credential name**: `Claude API`
   - **Name**: `x-api-key`
   - **Value**: Your Claude API key
     ```
     sk-ant-api03-...
     ```
5. Click **Save**

### Alternative: Generic Credential
1. Add **Credential** > **HTTP Request**
2. Select **Generic Credential Type**
3. Credential name: `Claude API`
4. Add these headers:
   ```
   x-api-key: sk-ant-api03-...
   anthropic-version: 2023-06-01
   content-type: application/json
   ```

### Test
1. Add **HTTP Request** node
2. Method: **POST**
3. URL: `https://api.anthropic.com/v1/messages`
4. Authentication: **Generic Credential Type**
5. Select credential: `Claude API`
6. Body (JSON):
   ```json
   {
     "model": "claude-3-5-sonnet-20241022",
     "max_tokens": 1024,
     "messages": [
       {
         "role": "user",
         "content": "Say hello!"
       }
     ]
   }
   ```
7. Execute - should get Claude's response

---

## Credential 7: Gemini API (HTTP Request Method)

### Setup
1. Get your Gemini API key:
   - Go to: https://aistudio.google.com/app/apikey
   - Click **Create API Key**
   - Select your Google Cloud project (or create new)
   - Copy the API key

2. In n8n, click **Add Credential** > Search "Header Auth"
3. Select **Header Auth**
4. Fill in:
   - **Credential name**: `Gemini API`
   - **Name**: `x-goog-api-key`
   - **Value**: Your Gemini API key
5. Click **Save**

### Test
1. Add **HTTP Request** node
2. Method: **POST**
3. URL: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent`
4. Authentication: **Generic Credential Type**
5. Select credential: `Gemini API`
6. Body (JSON):
   ```json
   {
     "contents": [{
       "parts": [{
         "text": "Say hello!"
       }]
     }]
   }
   ```
7. Execute - should get Gemini's response

---

## Credential 8: Supabase REST API (Optional)

For direct REST API calls instead of SQL.

### Setup
1. Click **Add Credential** > Search "Header Auth"
2. Select **Header Auth**
3. Fill in:
   - **Credential name**: `Supabase REST API`
   - **Name**: `apikey`
   - **Value**: Your Supabase `service_role` key
4. Add **Another Header**:
   - **Name**: `Authorization`
   - **Value**: `Bearer YOUR_SERVICE_ROLE_KEY`
5. Click **Save**

### Test
1. Add **HTTP Request** node
2. Method: **GET**
3. URL: `https://YOUR-PROJECT-REF.supabase.co/rest/v1/business_contexts`
4. Authentication: **Generic Credential Type**
5. Select credential: `Supabase REST API`
6. Execute - should return business contexts as JSON

---

## Summary of Credentials

You should now have these credentials configured:

| # | Credential Name | Type | Used For |
|---|----------------|------|----------|
| 1 | AIPA Telegram Bot | Telegram API | Sending/receiving messages |
| 2 | AIPA Gmail | Gmail OAuth2 | Email reading, labeling |
| 3 | AIPA Gmail | Google Calendar OAuth2 | Calendar management |
| 4 | AIPA Gmail | Google Drive OAuth2 | File storage/retrieval |
| 5 | AIPA Supabase DB | PostgreSQL | Database operations |
| 6 | Claude API | Header Auth | AI reasoning & analysis |
| 7 | Gemini API | Header Auth | AI classification & processing |
| 8 | Supabase REST API | Header Auth | REST API calls (optional) |

---

## Credential Security Best Practices

### Storage
- ✅ n8n encrypts credentials automatically
- ✅ Never export workflows with credentials embedded
- ✅ Use environment variables for sensitive data if possible
- ❌ Don't commit credentials to Git
- ❌ Don't share screenshots showing credential values

### Access Control
- ✅ Use n8n's user management for multi-user access
- ✅ Limit credential access to specific workflows
- ✅ Regularly audit which workflows use which credentials
- ✅ Rotate API keys quarterly

### Monitoring
- ✅ Set up email alerts for failed authentications
- ✅ Monitor API usage in respective platforms:
  - Google Cloud Console for Google APIs
  - Anthropic Console for Claude
  - Google AI Studio for Gemini
  - Supabase Dashboard for database

---

## Troubleshooting

### Issue: OAuth token expired
**Solution:**
1. Go to Credentials > Select the credential
2. Click **Reconnect**
3. Authorize again

### Issue: "Invalid API key"
**Solution:**
1. Verify key is copied correctly (no extra spaces)
2. Check key hasn't been revoked
3. Regenerate key if needed
4. Update credential with new key

### Issue: Database connection fails
**Solution:**
1. Check database isn't paused (Supabase free tier)
2. Verify password is correct
3. Ensure SSL is enabled
4. Check firewall/network isn't blocking port 5432
5. Verify host address is correct

### Issue: ngrok URL changed, OAuth broken
**Solution:**
1. Get new ngrok URL
2. Update Google Cloud Console:
   - APIs & Services > Credentials
   - Edit OAuth Client ID
   - Update Authorized redirect URIs
3. Reconnect OAuth credentials in n8n

### Issue: API rate limits hit
**Solution:**
1. Check API usage dashboards
2. Add delays between requests
3. Implement request queuing
4. Use Gemini for simple tasks (higher limits)
5. Upgrade API plans if necessary

---

## Testing All Credentials

### Quick Test Workflow
Create a simple workflow to test all credentials:

1. **Start** node (manual trigger)
2. **Telegram** node → Send test message
3. **Gmail** node → Get latest email
4. **Google Calendar** node → List today's events
5. **Google Drive** node → List folders
6. **Postgres** node → Query business_contexts
7. **HTTP (Claude)** node → Get AI response
8. **HTTP (Gemini)** node → Get AI response

Execute workflow and verify all nodes succeed.

---

## Environment Variables (Advanced)

For extra security, use n8n environment variables:

### Setup in n8n
1. Edit your n8n startup script or `.env` file:
```bash
# Telegram
N8N_TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHI...

# Database
N8N_DB_PASSWORD=your_supabase_password

# API Keys
N8N_CLAUDE_API_KEY=sk-ant-api03-...
N8N_GEMINI_API_KEY=AIzaSyB...
```

2. In credentials, reference variables:
```
{{ $env.N8N_TELEGRAM_BOT_TOKEN }}
```

### Benefits
- Easier credential rotation
- Better security (not in database)
- Easier for multi-environment setups (dev/prod)

---

## Next Steps

After configuring all credentials:
1. ✅ All 8 credentials configured
2. ✅ Each credential tested successfully
3. ✅ Security practices reviewed
4. → Continue to: `06-USER-GUIDE.md` (for learning commands)
5. → Or jump to: Import n8n workflows and start using the system!

---

## Quick Reference

### Credential Names (Use Exactly These)
```
AIPA Telegram Bot
AIPA Gmail
AIPA Supabase DB
Claude API
Gemini API
Supabase REST API (optional)
```

### When to Use Which AI
- **Claude**: Complex reasoning, strategy, creative content, long context
- **Gemini**: Simple classification, data extraction, bulk processing

### API Endpoints
```
Claude: https://api.anthropic.com/v1/messages
Gemini: https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent
Supabase: https://YOUR-PROJECT-REF.supabase.co/rest/v1/
```

---

**Credentials Setup Complete!** You're now ready to import and use the n8n workflows.
