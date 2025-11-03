# AIPA System Setup Guide

## Overview
Complete setup instructions for the AIPA (AI Personal Assistant) system.

## Prerequisites
- **Server**: n8n server running (recommended: 192.168.0.14:5678)
- **Discord**: Discord account and server admin access
- **Google**: Google Workspace account (Gmail, Calendar, Drive)
- **Database**: Supabase account (free tier sufficient)
- **APIs**: Google Gemini API access
- **Python**: Python 3.8+ with pip

## Step 1: Repository Setup
```bash
git clone https://github.com/DirtyDerv/AIPA.git
cd AIPA
pip install -r config/requirements.txt
```

## Step 2: Database Setup
1. Create Supabase project at https://supabase.com
2. Go to SQL Editor
3. Run `database/supabase_schema.sql`
4. Note your project URL and anon key

## Step 3: Discord Setup
1. Create Discord server
2. Create Discord application at https://discord.com/developers/applications
3. Create bot and get token
4. Configure bot permissions:
   - Send Messages
   - Use Slash Commands
   - Read Message History
   - Message Content Intent (IMPORTANT!)
5. Invite bot to your server

## Step 4: Google APIs Setup
1. Go to Google Cloud Console
2. Enable Gmail API, Calendar API, Drive API
3. Create OAuth2 credentials
4. Enable Gemini API access

## Step 5: n8n Configuration
1. Access n8n at http://YOUR_SERVER:5678
2. Go to Credentials section
3. Add credentials for:
   - Discord OAuth2
   - Gmail OAuth2
   - Google Calendar OAuth2
   - Supabase HTTP
   - Google Gemini API

## Step 6: Import Workflows
1. Go to n8n Workflows section
2. Import workflows from `workflows/` directory
3. Link credentials to each workflow
4. Test and activate workflows

## Step 7: Configure Credentials
1. Copy `config/CREDENTIALS.md.template` to `config/CREDENTIALS.md`
2. Fill in all actual values:
   - Discord bot token
   - Discord webhook URLs
   - Supabase URL and keys
   - n8n API key
   - Google API credentials

## Step 8: Deploy Discord Bot
```bash
# Local testing
python bot/discord_bot_bmf.py

# Server deployment (recommended)
scp bot/discord_bot_bmf.py user@YOUR_SERVER:/path/to/aipa/
ssh user@YOUR_SERVER
cd /path/to/aipa
python discord_bot_bmf.py
```

## Step 9: Test System
1. Test BMF logging: `python tools/bmf_immediate.py`
2. Test Discord bot: Send message in Discord
3. Test Gmail organization: Check workflow executions
4. Test voice processing: Send voice message in Discord

## Step 10: Configure Automation
1. Set Gmail organizer to run daily at 2 AM
2. Configure Discord webhooks for all channels
3. Test all business contexts
4. Verify data flows to Supabase

## Production Checklist
- [ ] All credentials configured
- [ ] Discord bot deployed to server
- [ ] n8n workflows active
- [ ] Gmail automation working
- [ ] Voice processing functional
- [ ] BMF logging operational
- [ ] Database connectivity verified
- [ ] Backups configured

## Troubleshooting
See `docs/TROUBLESHOOTING.md` for common issues and solutions.

## Support
- Documentation: See other files in `docs/`
- Issues: Create GitHub issue
- Status: Check `docs/WORKLOG_COMPLETE.md`