# AIPA - AI Personal Assistant

## Project Status
✅ **Discord Migration Complete**
✅ **Project Cleanup Complete**  
✅ **BMF Work Logging Functional**
🔄 **Bot Deployment Pending**

## Quick Start
1. **BMF Work Logging**: Run `python tools/bmf_immediate.py`
2. **Discord Bot**: Deploy `bot/discord_bot_bmf.py` to server
3. **Web Interface**: Open `web/bmf_web_logger.html`

## Project Structure
```
📁 AIPA/
├── 🤖 bot/           # Discord bot files
├── 📋 docs/          # Documentation
├── ⚙️ config/        # Configuration & credentials
├── 🔧 tools/         # Scripts & utilities
├── 📊 workflows/     # n8n workflow backups
├── 🌐 web/           # Web interfaces
└── 🗃️ backups/       # Project backups
```

## Active Systems
- **n8n**: 20 active workflows on 192.168.0.14:5678
- **Gmail Organizer**: Auto-organizing emails daily at 2 AM
- **Discord Voice**: Processing voice messages with Gemini AI
- **BMF Logging**: Multiple working solutions available

## Core Features
- 📧 **Gmail Organization**: AI-powered email sorting and labeling
- 🎵 **Discord Voice Processing**: Voice-to-text with Gemini AI
- 📝 **BMF Work Logging**: Track and log work entries
- 📱 **Discord Integration**: Rich embeds and slash commands
- 🤖 **AI Processing**: Google Gemini for smart responses

## Business Contexts
1. **Woody's Creations UK** - Laser-cut gifts and signs manufacturing
2. **DJ Business** - Event DJ services
3. **BMF** - Contract work for Brian Farmer
4. **Personal** - Personal life management

## Tech Stack
- **n8n** (Self-hosted): Workflow orchestration and automation
- **Discord Bot**: User interface and communication (migrated from Telegram)
- **Supabase**: Database and context storage
- **Google Gemini AI**: Cost-effective AI processing (migrated from Claude)
- **Google Workspace**: Gmail, Calendar, Drive integration
- **GitHub**: Code repository and version control

## Discord Integration
- **Server**: AIPA Business Management
- **Bot**: AIPA Bot (discord_bot_bmf.py)
- **Channels**: 9 specialized channels with webhooks
- **Voice Processing**: Gemini AI for voice-to-text
- **Commands**: Slash commands and natural language

## Active Workflows (n8n)
1. Gmail Organization & Cleanup (Daily 2 AM)
2. Discord Voice Processing
3. BMF Work Logging
4. Discord Message Processing
5. Business Intelligence & Reports
6. Calendar Management
7. Email Processing with AI
8. And 13+ more business automation workflows

## BMF Work Logging Solutions
1. **Discord Bot**: `bot/discord_bot_bmf.py` - Auto-detects BMF messages
2. **Immediate Script**: `tools/bmf_immediate.py` - Command-line logging
3. **Web Interface**: `web/bmf_web_logger.html` - Browser-based
4. **n8n Workflow**: Automated processing via Discord webhooks

## Installation & Setup

### Prerequisites
- n8n server running (192.168.0.14:5678)
- Discord server and bot token
- Google Workspace account
- Supabase database
- Gemini API access

### Quick Setup
1. Clone this repository
2. Install dependencies: `pip install -r config/requirements.txt`
3. Configure credentials in `config/CREDENTIALS.md`
4. Import n8n workflows from `workflows/`
5. Deploy Discord bot: `python bot/discord_bot_bmf.py`

## Usage

### Discord Commands
```
/bmf [work_description] - Log BMF work
/status - Check system status
Type naturally: "BMF work: tomorrow eddison and wanless fitting leadscrew"
```

### Natural Language
Simply message in Discord:
- "BMF work: installed new machinery today"
- "Check my calendar for tomorrow"
- "Organize my emails"
- Voice messages are automatically processed

## Recent Accomplishments
- ✅ Successfully migrated from Telegram to Discord
- ✅ Integrated Google Gemini AI for cost optimization
- ✅ Created comprehensive BMF work logging system
- ✅ Organized project structure from 100+ scattered files
- ✅ Cleaned up n8n from 25 to 20 active workflows
- ✅ Implemented advanced Gmail organization with AI
- ✅ Added Discord voice processing capabilities

## Next Steps
1. Deploy Discord bot to server for 24/7 operation
2. Monitor and maintain active workflows
3. Expand Discord command capabilities
4. Implement customer-facing features

## Documentation
See `docs/` folder for:
- Complete setup guides
- Credential configuration
- Workflow documentation
- Troubleshooting guides
- User manuals

## Support
- **Documentation**: See `docs/WORKLOG_COMPLETE.md` for comprehensive system overview
- **Issues**: GitHub Issues for bug reports
- **Setup**: Follow guides in `docs/` folder

## Version
Current Version: 2.0.0 (Discord Migration Complete)
Last Updated: 2025-11-03

---

**Note**: This system has evolved from a Telegram-based to a Discord-based AI assistant with comprehensive business automation, Gmail organization, voice processing, and work logging capabilities. All major components are operational and documented.