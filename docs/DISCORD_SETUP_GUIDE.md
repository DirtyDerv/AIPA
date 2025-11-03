# Discord Setup Guide

## Discord Server Configuration

### 1. Create Discord Server
1. Open Discord
2. Click "+" to create server
3. Choose "Create My Own"
4. Name: "AIPA Business Management"

### 2. Create Channels
```
💬 Text Channels:
├── #general
├── #aipa-logs
├── #personal
├── #woodys-creations
├── #dj-business
├── #bmf-work
├── #the-top-odd
├── #email-alerts
├── #calendar-updates
└── #task-reminders
```

### 3. Configure Webhooks
For each channel:
1. Right-click channel → Edit Channel
2. Go to Integrations → Webhooks
3. Click "New Webhook"
4. Copy webhook URL
5. Save URLs in `config/CREDENTIALS.md`

## Discord Bot Setup

### 1. Create Discord Application
1. Go to https://discord.com/developers/applications
2. Click "New Application"
3. Name: "AIPA Bot"
4. Go to "Bot" section
5. Click "Add Bot"

### 2. Configure Bot Permissions
**Required Permissions:**
- [x] Send Messages
- [x] Use Slash Commands
- [x] Read Message History
- [x] Embed Links
- [x] Attach Files
- [x] Use External Emojis

**Privileged Gateway Intents:**
- [x] Message Content Intent (CRITICAL!)
- [x] Server Members Intent

### 3. Get Bot Token
1. In Bot section, click "Reset Token"
2. Copy token immediately
3. Add to `config/CREDENTIALS.md`

### 4. Invite Bot to Server
1. Go to "OAuth2" → "URL Generator"
2. Select scopes:
   - [x] bot
   - [x] applications.commands
3. Select permissions (same as above)
4. Copy generated URL
5. Open URL and invite to your server

## Bot Deployment

### Local Testing
```bash
# Update credentials first
cp config/CREDENTIALS.md.template config/CREDENTIALS.md
# Edit config/CREDENTIALS.md with actual values

# Test bot locally
python bot/discord_bot_bmf.py
```

### Server Deployment
```bash
# Copy to server
scp bot/discord_bot_bmf.py user@192.168.0.14:/home/user/aipa/

# SSH to server
ssh user@192.168.0.14

# Install dependencies
pip install discord.py requests

# Update credentials in bot file
nano discord_bot_bmf.py

# Run bot
python discord_bot_bmf.py

# Run as service (optional)
nohup python discord_bot_bmf.py &
```

## Bot Features

### Slash Commands
- `/bmf [description]` - Log BMF work entry
- `/status` - Check bot status

### Message Processing
- **Auto-detection**: Messages containing "BMF" automatically logged
- **Channel-specific**: #bmf-work channel processes all messages
- **Rich embeds**: Colorful responses with status indicators

### Voice Processing
- Send voice messages in any channel
- Automatic transcription via Gemini AI
- Smart responses based on content

## Testing

### 1. Basic Bot Test
1. Type in Discord: "BMF work: test entry"
2. Bot should respond with confirmation embed
3. Check database for logged entry

### 2. Slash Command Test
1. Type: `/bmf test work description`
2. Bot should log and confirm

### 3. Voice Test
1. Send voice message
2. Bot should transcribe and respond

## Troubleshooting

### Bot Not Responding
- Check Message Content Intent is enabled
- Verify bot has permissions in channel
- Check bot token in code

### Slash Commands Not Working
- Reinvite bot with applications.commands scope
- Wait up to 1 hour for commands to sync

### Voice Not Processing
- Check Gemini API credentials
- Verify n8n workflow is active

## Security Notes

⚠️ **Never commit real tokens to git**
✅ Use environment variables in production
🔒 Rotate tokens regularly
🛡️ Limit bot permissions to minimum required

## Production Recommendations

1. **Run on dedicated server** for 24/7 operation
2. **Use process manager** like pm2 or systemd
3. **Configure logging** for monitoring
4. **Set up health checks** for reliability
5. **Backup bot configuration** regularly