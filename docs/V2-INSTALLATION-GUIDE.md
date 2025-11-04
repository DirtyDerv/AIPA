# AIPA V2 Enhanced System - Installation Guide

## Overview
This guide will help you install the enhanced AI PA system with multi-agent architecture, vector search, voice interface, and autonomous behaviors.

## What's New in V2

### Major Enhancements
- ✅ **CrewAI Multi-Agent System** - True collaborative AI agents
- ✅ **MCP Servers** - Native Claude Desktop integration
- ✅ **Vector Search** - Semantic search across all data (pgvector)
- ✅ **Agent Memory** - Persistent memory across sessions
- ✅ **RAG Knowledge Base** - Business-specific knowledge retrieval
- ✅ **Voice Interface** - Whisper transcription for voice messages
- ✅ **Autonomous Behaviors** - Proactive insights and task suggestions
- ✅ **Auto-Response System** - Draft emails for common inquiries
- ✅ **Customer Database** - Unified customer tracking
- ✅ **Enhanced Analytics** - Predictive insights and trends

---

## Prerequisites

### System Requirements
- **Python**: 3.10 or higher
- **Node.js**: 18+ (for n8n, optional if using pure Python)
- **PostgreSQL**: 14+ with pgvector extension
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space

### Accounts & API Keys
- Supabase account (free tier)
- Claude API key (free tier available)
- Google (Gemini) API key (free tier)
- Google Cloud project with Gmail/Calendar/Drive APIs enabled
- Telegram bot token
- ngrok account (free tier)

---

## Part 1: Python Environment Setup

### 1.1 Create Virtual Environment

```bash
cd C:\Users\woody\Documents\AI\AIPA
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 1.2 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 1.3 Verify Installation

```bash
python -c "import crewai; import langchain; import mcp; print('All core packages installed!')"
```

---

## Part 2: Enhanced Database Setup

### 2.1 Enable pgvector Extension in Supabase

1. Go to Supabase Dashboard
2. Navigate to **Database** > **Extensions**
3. Search for "vector"
4. Click **Enable** on `vector` extension
5. Wait for activation (30 seconds)

### 2.2 Run Enhanced Schema

1. Open Supabase SQL Editor
2. Load `database/schema-v2-enhanced.sql`
3. Execute the entire script
4. Verify new tables created:
   - customers
   - agent_memory
   - knowledge_base
   - agent_tasks
   - email_templates
   - insights
   - voice_messages

### 2.3 Verify Vector Support

```sql
-- Test pgvector
SELECT embedding FROM emails LIMIT 1;

-- Should show vector column exists
```

---

## Part 3: Environment Configuration

### 3.1 Create .env File

Create `.env` in project root:

```bash
# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
SUPABASE_HOST=db.your-project.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your-db-password

# AI APIs
ANTHROPIC_API_KEY=sk-ant-your-key
GOOGLE_API_KEY=your-gemini-key
OPENAI_API_KEY=your-openai-key-for-whisper

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_USER_ID=your-telegram-id

# Google OAuth (for MCP servers)
GOOGLE_CLIENT_ID=your-client-id
GOOGLE_CLIENT_SECRET=your-client-secret

# n8n (if using)
N8N_URL=https://your-ngrok-url.ngrok-free.dev
```

### 3.2 Set Environment Variables

```bash
# Windows
set PYTHONPATH=%PYTHONPATH%;C:\Users\woody\Documents\AI\AIPA

# Linux/Mac
export PYTHONPATH=$PYTHONPATH:/path/to/AIPA
```

---

## Part 4: MCP Server Setup

### 4.1 Install MCP Servers

```bash
cd mcp-servers

# Test Gmail server
python gmail_server.py --test

# Test Supabase server
python supabase_server.py --test
```

### 4.2 Configure Claude Desktop

Create/edit `~/.claude/config.json` (Windows: `%APPDATA%\Claude\config.json`):

```json
{
  "mcpServers": {
    "aipa-gmail": {
      "command": "python",
      "args": ["C:/Users/woody/Documents/AI/AIPA/mcp-servers/gmail_server.py"],
      "env": {
        "GOOGLE_CLIENT_ID": "your-client-id",
        "GOOGLE_CLIENT_SECRET": "your-client-secret"
      }
    },
    "aipa-database": {
      "command": "python",
      "args": ["C:/Users/woody/Documents/AI/AIPA/mcp-servers/supabase_server.py"],
      "env": {
        "SUPABASE_HOST": "db.your-project.supabase.co",
        "SUPABASE_PASSWORD": "your-password"
      }
    }
  }
}
```

### 4.3 Restart Claude Desktop

1. Close Claude Desktop completely
2. Reopen
3. Check that MCP servers show in tools list

---

## Part 5: CrewAI Agents Setup

### 5.1 Test Individual Agents

```bash
cd agents
python -c "from crew_system import AIPersonalAssistant; pa = AIPersonalAssistant(); print('Agents initialized!')"
```

### 5.2 Run Test Workflow

```bash
python test_crew.py
```

Expected output:
```
✅ Executive Assistant initialized
✅ Email Manager initialized
✅ Calendar Manager initialized
✅ All agents operational
```

---

## Part 6: Telegram Integration

### 6.1 Set Up Telegram Bot Webhook

The enhanced system uses webhooks OR polling. Choose one:

**Option A: Webhook (Recommended)**
```python
# In telegram_bot.py
from telegram.ext import Application

app = Application.builder().token(BOT_TOKEN).build()
app.run_webhook(
    listen="0.0.0.0",
    port=8443,
    url_path="telegram",
    webhook_url="https://your-ngrok-url/telegram"
)
```

**Option B: Polling (Easier for testing)**
```python
app.run_polling()
```

### 6.2 Start Telegram Bot

```bash
python telegram_bot.py
```

Test by sending `/start` to your bot.

---

## Part 7: Voice Interface Setup

### 7.1 Install ffmpeg (Required for Whisper)

**Windows**:
```bash
choco install ffmpeg
```

**Linux**:
```bash
sudo apt install ffmpeg
```

**Mac**:
```bash
brew install ffmpeg
```

### 7.2 Test Voice Processing

```bash
python -c "import whisper; model = whisper.load_model('base'); print('Whisper ready!')"
```

### 7.3 Configure Voice Handler

Voice messages are automatically processed when sent to Telegram bot.

---

## Part 8: Generate Initial Embeddings

### 8.1 Install Embedding Model

```bash
python -m sentence_transformers download all-MiniLM-L6-v2
```

### 8.2 Generate Embeddings for Existing Data

```bash
python scripts/generate_embeddings.py
```

This will:
- Generate embeddings for all emails
- Generate embeddings for conversations
- Generate embeddings for knowledge base
- Store in pgvector columns

### 8.3 Verify Embeddings

```sql
SELECT COUNT(*) FROM emails WHERE embedding IS NOT NULL;
SELECT COUNT(*) FROM knowledge_base WHERE embedding IS NOT NULL;
```

---

## Part 9: Knowledge Base Population

### 9.1 Add Business Knowledge

Edit `knowledge_base_seed.json` with your business info:

```json
[
  {
    "business": "dj-business",
    "title": "Standard Pricing",
    "content": "4 hours: £300, Full evening: £500, Wedding premium: +£100",
    "type": "price"
  },
  {
    "business": "woodys-creations",
    "title": "Lead Times",
    "content": "Standard: 5-7 days, Complex: 10-14 days, Rush: 2-3 days (+50%)",
    "type": "procedure"
  }
]
```

### 9.2 Import Knowledge Base

```bash
python scripts/import_knowledge.py knowledge_base_seed.json
```

---

## Part 10: Start All Services

### 10.1 Service Start Order

```bash
# Terminal 1: MCP Servers (if not using Claude Desktop integration)
# Not needed if using Claude Desktop

# Terminal 2: Telegram Bot
python telegram_bot.py

# Terminal 3: Autonomous Agent (Background tasks)
python autonomous_agent.py

# Terminal 4: n8n (Optional - if keeping hybrid approach)
n8n start
```

### 10.2 Verify All Services Running

```bash
# Check processes
ps aux | grep python  # Linux/Mac
tasklist | findstr python  # Windows

# Test Telegram
# Send message to bot and verify response

# Test MCP (in Claude Desktop)
# Ask Claude: "Search my emails for DJ inquiries"
```

---

## Part 11: Testing & Validation

### 11.1 Run Test Suite

```bash
pytest tests/
```

### 11.2 Manual Tests

**Test 1: Daily Briefing**
```
Telegram: /briefing
Expected: Formatted summary with calendar, emails, tasks
```

**Test 2: Email Processing**
```
Send yourself a test email
Wait 15 minutes OR manually trigger
Telegram: /email
Expected: Email classified and summarized
```

**Test 3: Voice Message**
```
Send voice message: "What's on my calendar today?"
Expected: Transcription + response
```

**Test 4: Agent Memory**
```
Say: "I prefer oak for most orders"
Later say: "What material should I use?"
Expected: Agent recalls preference
```

**Test 5: Auto-Response**
```
Send fake DJ inquiry email
Expected: Draft response created
```

### 11.3 Performance Benchmarks

Expected response times:
- Daily briefing: 5-10 seconds
- Email classification: 1-2 seconds per email
- Voice transcription: 3-5 seconds
- Database queries: <500ms
- Agent collaboration: 10-30 seconds

---

## Part 12: Production Deployment

### 12.1 Systemd Services (Linux)

Create `/etc/systemd/system/aipa-telegram.service`:

```ini
[Unit]
Description=AIPA Telegram Bot
After=network.target

[Service]
Type=simple
User=woody
WorkingDirectory=/home/woody/AIPA
Environment="PATH=/home/woody/AIPA/venv/bin"
ExecStart=/home/woody/AIPA/venv/bin/python telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable aipa-telegram
sudo systemctl start aipa-telegram
```

### 12.2 Windows Service

Use `nssm` (Non-Sucking Service Manager):
```bash
nssm install AIPA-Telegram "C:\Users\woody\Documents\AI\AIPA\venv\Scripts\python.exe" "C:\Users\woody\Documents\AI\AIPA\telegram_bot.py"
nssm start AIPA-Telegram
```

### 12.3 Docker Deployment (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "telegram_bot.py"]
```

---

## Troubleshooting

### Issue: Embeddings not generating
**Solution**:
```bash
pip install --upgrade sentence-transformers
python scripts/generate_embeddings.py --force
```

### Issue: MCP servers not connecting
**Solution**:
1. Check Claude Desktop logs: `~/.claude/logs/`
2. Verify python path in config.json
3. Test servers manually: `python gmail_server.py`

### Issue: Agents not responding
**Solution**:
1. Check API keys are valid
2. Verify `.env` file loaded
3. Check agent logs: `logs/agents.log`
4. Test with simple query first

### Issue: Voice processing fails
**Solution**:
1. Verify ffmpeg installed: `ffmpeg -version`
2. Check audio file format supported
3. Try smaller audio file first

---

## Monitoring & Logs

### Log Locations
```
logs/telegram_bot.log - Telegram interactions
logs/agents.log - Agent decisions
logs/mcp_servers.log - MCP server activity
logs/autonomous.log - Background tasks
```

### Monitor API Usage

```bash
# Check today's usage
python scripts/check_api_usage.py

# Output:
# Claude: 45 requests / 200 daily limit
# Gemini: 234 requests / 1500 daily limit
```

### Database Monitoring

```sql
-- Active agents
SELECT agent_name, COUNT(*) as decisions_today
FROM ai_decisions
WHERE created_at > CURRENT_DATE
GROUP BY agent_name;

-- Memory usage
SELECT COUNT(*), pg_size_pretty(SUM(pg_column_size(embedding)))
FROM emails
WHERE embedding IS NOT NULL;
```

---

## Performance Optimization

### 1. Cache Frequently Used Data

```python
# In database_tools.py
@lru_cache(maxsize=100)
def get_knowledge_base_entry(title):
    # Cached lookups
    pass
```

### 2. Batch Embeddings

```python
# Generate embeddings in batches of 50
for batch in chunks(emails, 50):
    embeddings = model.encode([e['content'] for e in batch])
    # Save batch
```

### 3. Use Connection Pooling

Already configured in `supabase_server.py` with psycopg2.pool.

---

## Next Steps

After installation:
1. ✅ Run through all test scenarios
2. ✅ Customize knowledge base for your businesses
3. ✅ Set up daily briefing schedule
4. ✅ Configure auto-response templates
5. ✅ Add Angie's access (Woody's Creations only)
6. ✅ Monitor for first week, adjust settings
7. ✅ Enable autonomous behaviors gradually

---

## Upgrading from V1

See `V2-MIGRATION-GUIDE.md` for step-by-step migration from the basic system.

---

## Support & Resources

- **Documentation**: `docs/` folder
- **Examples**: `examples/` folder
- **Test Scripts**: `tests/` folder
- **MCP Docs**: https://modelcontextprotocol.io
- **CrewAI Docs**: https://docs.crewai.com
- **LangChain Docs**: https://docs.langchain.com

---

**Installation Complete!** 🎉

You now have a production-ready, multi-agent AI PA system with advanced capabilities far beyond the original design.

Start with: `python telegram_bot.py` and send `/start` to your bot!
