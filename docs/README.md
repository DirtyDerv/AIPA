# AI Personal Assistant (AIPA) System

## Overview
A comprehensive AI-powered personal assistant system managing multiple business contexts through Telegram, using n8n orchestration with Claude and Gemini AI.

## Business Contexts
1. **Woody's Creations UK** - Laser-cut gifts and signs manufacturing
2. **DJ Business** - Event DJ services
3. **BMF** - Contract work for Brian Farmer
4. **Pub** (Future) - Landlord and pub management
5. **Personal** - Personal life management

## System Architecture

### Tech Stack
- **n8n** (Self-hosted): Workflow orchestration
- **Telegram Bot**: User interface and communication
- **Supabase**: Database and context storage (Free tier)
- **Claude API**: Advanced AI reasoning (Free tier)
- **Gemini API**: Cost-effective AI processing (Free tier)
- **Google Workspace**: Gmail, Calendar, Drive integration
- **Ngrok**: Public tunnel for self-hosted n8n

### Core Components
1. **Telegram Interface** - Main communication hub
2. **Email Processing** - Automated triage and categorization
3. **Calendar Management** - Multi-context scheduling
4. **Task Management** - Priority-based todo system
5. **AI Agent Router** - Smart API selection
6. **Business Intelligence** - Weekly reports and insights
7. **Specialized Managers** - DJ bookings, orders, work tracking

## Repository Structure

```
AIPA/
├── README.md (this file)
├── docs/
│   ├── 01-SETUP-GUIDE.md
│   ├── 02-TELEGRAM-BOT-SETUP.md
│   ├── 03-GOOGLE-WORKSPACE-SETUP.md
│   ├── 04-SUPABASE-SETUP.md
│   ├── 05-N8N-CREDENTIALS.md
│   ├── 06-USER-GUIDE.md
│   ├── 07-TESTING-CHECKLIST.md
│   └── 08-TROUBLESHOOTING.md
├── database/
│   ├── schema.sql
│   ├── seed-data.sql
│   └── migrations/
├── n8n-workflows/
│   ├── 01-telegram-interface.json
│   ├── 02-email-processing.json
│   ├── 03-calendar-management.json
│   ├── 04-daily-briefing.json
│   ├── 05-ai-agent-router.json
│   ├── 06-business-strategist.json
│   ├── 07-marketing-manager.json
│   ├── 08-task-management.json
│   ├── 09-dj-booking-pipeline.json
│   ├── 10-woodys-order-manager.json
│   └── 11-bmf-work-tracker.json
├── ai-prompts/
│   ├── executive-assistant.md
│   ├── business-strategist.md
│   ├── marketing-manager.md
│   ├── operations-manager.md
│   ├── booking-manager.md
│   ├── project-coordinator.md
│   └── financial-controller.md
└── scripts/
    ├── backup-database.sh
    └── restore-database.sh
```

## Quick Start

### Prerequisites
- Self-hosted n8n instance (running on home server)
- Ngrok tunnel configured: `https://uniterative-futile-charmain.ngrok-free.dev`
- Google account (Gmail, Calendar, Drive)
- Telegram account
- Supabase account (free tier)
- Claude API access (free tier)
- Gemini API access (free tier)

### Installation Steps
1. Follow `docs/01-SETUP-GUIDE.md` for complete setup
2. Configure credentials as per `docs/05-N8N-CREDENTIALS.md`
3. Import n8n workflows from `n8n-workflows/`
4. Set up database using `database/schema.sql`
5. Create Telegram bot following `docs/02-TELEGRAM-BOT-SETUP.md`
6. Configure Google Workspace per `docs/03-GOOGLE-WORKSPACE-SETUP.md`

## Features

### Core Capabilities
- ✅ Multi-business context management
- ✅ Intelligent email triage and categorization
- ✅ Cross-calendar scheduling with conflict detection
- ✅ Priority-based task management
- ✅ Daily briefings at 8 AM
- ✅ Weekly business strategy reports
- ✅ Marketing campaign planning
- ✅ Automated booking pipeline (DJ)
- ✅ Order management (Woody's Creations)
- ✅ Work logging and timesheet tracking (BMF)

### AI Agents
1. **Executive Assistant** - Primary interface and coordination
2. **Business Strategist** - Weekly insights and growth opportunities
3. **Marketing Manager** - Campaign planning and content ideas
4. **Operations Manager** - Woody's Creations production
5. **Booking Manager** - DJ business pipeline
6. **Project Coordinator** - BMF work tracking
7. **Financial Controller** - Multi-business expense and revenue

## Usage

### Telegram Commands
```
/start - Initialize the PA system
/context [business] - Switch business context
/briefing - Get current status summary
/email - Email triage summary
/calendar - Today's schedule
/tasks - View and manage tasks
/report - Business insights
/help - Command reference
```

### Natural Language
Simply message the bot naturally:
- "What's on my calendar today?"
- "Show me urgent emails for Woody's Creations"
- "Create a task to follow up with DJ inquiry"
- "What were my DJ bookings this month?"
- "Schedule production time for new orders"

## Documentation

- **Setup & Configuration**: See `docs/01-SETUP-GUIDE.md`
- **User Guide**: See `docs/06-USER-GUIDE.md`
- **Troubleshooting**: See `docs/08-TROUBLESHOOTING.md`

## API Usage & Limits

### Free Tier Allocations
- **Claude API**: ~20-30 requests/day (use for complex reasoning)
- **Gemini API**: 1,500 requests/day (use for classification/simple tasks)
- **Supabase**: 500 MB database, 2 GB bandwidth
- **Telegram Bot**: Unlimited messages
- **n8n**: No limits (self-hosted)

### Cost Management
- AI Agent Router automatically selects cheapest appropriate API
- Request usage tracked in Supabase
- Warnings sent when approaching limits

## Privacy & Security

### Data Handling
- Email content summarized before sending to AI APIs
- Financial details stored locally, not analyzed externally
- No sensitive passwords or credentials sent to AI
- Regular data cleanup (auto-delete old conversations >90 days)

### Access Control
- Primary user: Woody
- Secondary user: Angie (Woody's Creations context only)
- No external access to BMF confidential data

## Maintenance

### Regular Tasks
- Monitor API usage weekly
- Review AI decision logs monthly
- Update business contexts as needed
- Backup Supabase database weekly

### Troubleshooting
- Check ngrok tunnel if webhooks fail
- Verify API keys if AI responses stop
- Review n8n execution logs for workflow errors

## Future Enhancements
- Voice interface via Telegram voice messages
- Customer-facing chatbots (DJ inquiries, order status)
- Inventory management for Woody's Creations
- Pub-specific workflows when opening
- Staff scheduling for pub
- Financial forecasting and budget planning

## Support
- GitHub Issues: [Create issue]
- Documentation: See `docs/` folder
- n8n Community: https://community.n8n.io

## Version
Current Version: 1.0.0
Last Updated: 2025-11-01

---

**Note**: This is a self-hosted, zero-budget AI PA system built with free-tier services and open-source tools. All components are designed to operate within free tier limits while providing enterprise-level personal assistant capabilities.
