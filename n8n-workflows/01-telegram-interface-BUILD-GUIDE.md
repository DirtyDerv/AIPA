# Telegram Interface Workflow - Build Guide

## Overview
This is the main entry point for all Telegram interactions. It receives messages, validates users, routes commands, and sends responses.

## Workflow Summary
```
Telegram Webhook → Validate User → Route Command/Message → Process → Send Response
```

---

## Step-by-Step Build Instructions

### Node 1: Telegram Trigger
1. Add node: **Telegram Trigger**
2. Configure:
   - **Credential**: `AIPA Telegram Bot`
   - **Updates**: `Message`
3. This creates webhook automatically at: `/webhook/telegram-bot`
4. Note the webhook URL for Telegram setup

### Node 2: Extract Message Data
1. Add node: **Code** (after Telegram Trigger)
2. Name it: `Extract Message Info`
3. Paste this JavaScript code:
```javascript
// Extract relevant data from Telegram message
const message = $input.first().json.message;

return [{
  json: {
    telegram_id: message.from.id,
    telegram_username: message.from.username || '',
    first_name: message.from.first_name || '',
    chat_id: message.chat.id,
    message_text: message.text || '',
    message_type: message.text?.startsWith('/') ? 'command' : 'text',
    command: message.text?.startsWith('/') ? message.text.split(' ')[0].substring(1) : null,
    command_args: message.text?.startsWith('/') ? message.text.split(' ').slice(1).join(' ') : null,
    timestamp: new Date(message.date * 1000).toISOString()
  }
}];
```

### Node 3: Validate User in Database
1. Add node: **Postgres** (after Extract Message Info)
2. Name it: `Check User Exists`
3. Configure:
   - **Credential**: `AIPA Supabase DB`
   - **Operation**: `Execute Query`
   - **Query**:
```sql
SELECT
  id,
  telegram_id,
  first_name,
  role,
  allowed_contexts,
  is_active
FROM users
WHERE telegram_id = {{ $json.telegram_id }}
AND is_active = true
LIMIT 1;
```

### Node 4: Check If User Found
1. Add node: **IF** (after Check User Exists)
2. Name it: `User Authorized?`
3. Configure:
   - **Conditions**:
     - **Condition 1**: `{{ $json.id }}` exists
   - Alternative simple check: `{{ $json.length > 0 }}`

### Node 5a: Unauthorized Response (IF False path)
1. Add node: **Telegram** (connect to IF false output)
2. Name it: `Send Unauthorized Message`
3. Configure:
   - **Credential**: `AIPA Telegram Bot`
   - **Resource**: `Message`
   - **Operation**: `Send Message`
   - **Chat ID**: `{{ $('Extract Message Info').item.json.chat_id }}`
   - **Text**:
```
⛔ Unauthorized Access

This AI Personal Assistant is private.

If you should have access, please contact the administrator with your Telegram ID: {{ $('Extract Message Info').item.json.telegram_id }}
```
4. This ends the workflow for unauthorized users

### Node 6: Save Conversation to Database (IF True path)
1. Add node: **Postgres** (connect to IF true output)
2. Name it: `Log Conversation`
3. Configure:
   - **Credential**: `AIPA Supabase DB`
   - **Operation**: `Execute Query`
   - **Query**:
```sql
INSERT INTO conversations (
  user_id,
  business_context_id,
  message_text,
  message_type,
  intent,
  created_at
) VALUES (
  '{{ $('Check User Exists').item.json.id }}',
  (SELECT id FROM business_contexts WHERE name = 'personal' LIMIT 1),
  '{{ $('Extract Message Info').item.json.message_text }}',
  'user',
  '{{ $('Extract Message Info').item.json.command || "chat" }}',
  NOW()
);
```

### Node 7: Route Command
1. Add node: **Switch** (after Log Conversation)
2. Name it: `Command Router`
3. Configure Mode: **Expression**
4. Add these routes:

**Route 0**: `/start` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'start' }}`

**Route 1**: `/briefing` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'briefing' }}`

**Route 2**: `/email` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'email' }}`

**Route 3**: `/calendar` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'calendar' }}`

**Route 4**: `/tasks` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'tasks' }}`

**Route 5**: `/context` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'context' }}`

**Route 6**: `/help` command
- Expression: `{{ $('Extract Message Info').item.json.command === 'help' }}`

**Route 7** (Default): Natural language
- Expression: `{{ true }}` (catches everything else)

---

## Command Handlers

### Handler for `/start`
1. Add node: **Telegram** (connect to Switch Route 0)
2. Name it: `Send Welcome Message`
3. Configure:
   - **Chat ID**: `{{ $('Extract Message Info').item.json.chat_id }}`
   - **Text**:
```
👋 Welcome to Your AI Personal Assistant!

I'm here to manage your multiple businesses and personal life:
🏢 Woody's Creations
🎵 DJ Business
💼 BMF Work
🍺 Pub (Future)
👤 Personal

What I can do:
✅ Triage emails automatically
✅ Manage your calendar across all contexts
✅ Track tasks and priorities
✅ Provide daily briefings
✅ Generate business insights
✅ Answer questions in natural language

Quick Commands:
/briefing - Daily summary
/email - Email triage
/calendar - Today's schedule
/tasks - View tasks
/help - Full command list

Or just chat with me naturally:
"What's urgent today?"
"Show me DJ bookings this month"
"Create task: Follow up with supplier"

Let's get started! Try /briefing to see what's on your plate today.
```
   - **Additional Fields** > **Parse Mode**: `Markdown`

### Handler for `/briefing`
1. Add node: **Execute Workflow** (connect to Switch Route 1)
2. Name it: `Call Daily Briefing Workflow`
3. Configure:
   - **Source**: `Database`
   - **Workflow**: Select `04-daily-briefing` (you'll create this next)
   - **Note**: For now, you can use a placeholder Telegram message

**Temporary Placeholder** (until Daily Briefing workflow is built):
1. Add node: **Code**
2. Name it: `Generate Quick Briefing`
3. Code:
```javascript
const chatId = $('Extract Message Info').item.json.chat_id;
const userName = $('Extract Message Info').item.json.first_name;

// Get current date/time
const now = new Date();
const greeting = now.getHours() < 12 ? 'Good morning' : now.getHours() < 18 ? 'Good afternoon' : 'Good evening';

return [{
  json: {
    chat_id: chatId,
    text: `${greeting}, ${userName}! 📊

📅 TODAY'S BRIEFING
Coming soon - connecting to database...

For now, try these commands:
/help - See all commands
/email - Check emails
/tasks - View tasks

The full briefing system is being set up!`
  }
}];
```
4. Add **Telegram** node after this Code node to send the message

### Handler for `/email`
1. Add node: **Postgres** (connect to Switch Route 2)
2. Name it: `Get Unprocessed Emails`
3. Query:
```sql
SELECT
  bc.display_name as business,
  bc.emoji,
  COUNT(*) as count,
  SUM(CASE WHEN e.priority = 'urgent' THEN 1 ELSE 0 END) as urgent_count
FROM emails e
JOIN business_contexts bc ON e.business_context_id = bc.id
WHERE e.is_processed = false
GROUP BY bc.display_name, bc.emoji
ORDER BY urgent_count DESC;
```

4. Add node: **Code** (after Get Unprocessed Emails)
5. Name it: `Format Email Summary`
6. Code:
```javascript
const emailData = $input.all();
const chatId = $('Extract Message Info').item.json.chat_id;

if (emailData.length === 0) {
  return [{
    json: {
      chat_id: chatId,
      text: "📧 All caught up! No unprocessed emails. 🎉"
    }
  }];
}

let message = "📧 UNPROCESSED EMAILS\n\n";
let totalCount = 0;
let totalUrgent = 0;

emailData.forEach(row => {
  const business = row.json.business;
  const emoji = row.json.emoji;
  const count = row.json.count;
  const urgent = row.json.urgent_count;

  totalCount += count;
  totalUrgent += urgent;

  message += `${emoji} ${business}: ${count}`;
  if (urgent > 0) {
    message += ` (${urgent} URGENT 🔴)`;
  }
  message += `\n`;
});

message += `\n**Total: ${totalCount} emails**`;
if (totalUrgent > 0) {
  message += `\n🔴 **${totalUrgent} require immediate attention**`;
}

message += `\n\nUse the email processing workflow to see details.`;

return [{
  json: {
    chat_id: chatId,
    text: message
  }
}];
```

7. Add **Telegram** node to send formatted summary

### Handler for `/calendar`
1. Add node: **Postgres** (connect to Switch Route 3)
2. Name it: `Get Today's Calendar`
3. Query:
```sql
SELECT
  ce.title,
  ce.start_time,
  ce.end_time,
  ce.location,
  bc.display_name as business,
  bc.emoji
FROM calendar_events ce
JOIN business_contexts bc ON ce.business_context_id = bc.id
WHERE DATE(ce.start_time) = CURRENT_DATE
  AND ce.status = 'confirmed'
ORDER BY ce.start_time;
```

4. Add node: **Code** (after Get Today's Calendar)
5. Name it: `Format Calendar`
6. Code:
```javascript
const events = $input.all();
const chatId = $('Extract Message Info').item.json.chat_id;

if (events.length === 0) {
  return [{
    json: {
      chat_id: chatId,
      text: "📅 No events scheduled for today. Enjoy your free time! ✨"
    }
  }];
}

let message = "📅 TODAY'S SCHEDULE\n\n";

events.forEach(event => {
  const startTime = new Date(event.json.start_time);
  const endTime = new Date(event.json.end_time);
  const emoji = event.json.emoji;
  const title = event.json.title;
  const location = event.json.location;

  const timeStr = `${startTime.getHours().toString().padStart(2, '0')}:${startTime.getMinutes().toString().padStart(2, '0')}`;
  const duration = Math.round((endTime - startTime) / 1000 / 60); // minutes

  message += `${emoji} ${timeStr} - ${title} (${duration} min)\n`;
  if (location) {
    message += `   📍 ${location}\n`;
  }
  message += `\n`;
});

return [{
  json: {
    chat_id: chatId,
    text: message
  }
}];
```

7. Add **Telegram** node to send calendar

### Handler for `/tasks`
1. Add node: **Postgres** (connect to Switch Route 4)
2. Name it: `Get Pending Tasks`
3. Query:
```sql
SELECT
  t.title,
  t.priority,
  t.due_date,
  bc.display_name as business,
  bc.emoji,
  t.status
FROM tasks t
JOIN business_contexts bc ON t.business_context_id = bc.id
WHERE t.status IN ('pending', 'in_progress')
ORDER BY
  CASE t.priority
    WHEN 'urgent' THEN 1
    WHEN 'high' THEN 2
    WHEN 'medium' THEN 3
    ELSE 4
  END,
  t.due_date ASC NULLS LAST
LIMIT 20;
```

4. Add **Code** and **Telegram** nodes similar to above to format and send

### Handler for `/context`
1. Add node: **Telegram** (connect to Switch Route 5)
2. Name it: `Show Context Menu`
3. Configure:
   - **Reply Markup**: `Inline Keyboard`
   - **Text**: `Select business context:`
   - **Inline Keyboard** (JSON):
```json
{
  "inline_keyboard": [
    [{"text": "🏢 Woody's Creations", "callback_data": "ctx_woodys"}],
    [{"text": "🎵 DJ Business", "callback_data": "ctx_dj"}],
    [{"text": "💼 BMF Work", "callback_data": "ctx_bmf"}],
    [{"text": "🍺 Pub (Future)", "callback_data": "ctx_pub"}],
    [{"text": "👤 Personal", "callback_data": "ctx_personal"}]
  ]
}
```

### Handler for `/help`
1. Add node: **Telegram** (connect to Switch Route 6)
2. Name it: `Send Help Message`
3. Text:
```
📖 AI PA COMMAND REFERENCE

**Main Commands:**
/briefing - Daily summary (emails, calendar, tasks)
/email - Unprocessed email summary
/calendar - Today's schedule
/tasks - Pending tasks list
/context - Switch business context
/help - This message

**Business Contexts:**
🏢 Woody's Creations - Laser gifts
🎵 DJ Business - Event DJ services
💼 BMF Work - Contract work
🍺 Pub - Future pub management
👤 Personal - Personal life

**Natural Language:**
Just chat normally! Examples:
• "What's urgent today?"
• "Show me DJ bookings this month"
• "Create task: Call supplier"
• "When is my next meeting?"
• "How many orders this week?"

**Tips:**
- Use /briefing every morning
- Check /email regularly
- Natural language is powerful!

Need more help? Just ask!
```

### Handler for Natural Language (Default Route)
1. Add node: **Code** (connect to Switch Route 7)
2. Name it: `Prepare AI Request`
3. Code:
```javascript
const userMessage = $('Extract Message Info').item.json.message_text;
const userName = $('Extract Message Info').item.json.first_name;
const chatId = $('Extract Message Info').item.json.chat_id;

// Get context from database (simplified for now)
return [{
  json: {
    chat_id: chatId,
    user_message: userMessage,
    user_name: userName,
    system_prompt: `You are ${userName}'s Executive Assistant AI. Respond helpfully and concisely to: "${userMessage}"`
  }
}];
```

4. Add node: **HTTP Request** (after Prepare AI Request)
5. Name it: `Call Claude API`
6. Configure:
   - **Method**: `POST`
   - **URL**: `https://api.anthropic.com/v1/messages`
   - **Authentication**: `Generic Credential Type`
   - **Credential**: `Claude API`
   - **Body** (JSON):
```json
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "{{ $json.user_message }}"
    }
  ],
  "system": "{{ $json.system_prompt }}"
}
```

7. Add node: **Code** (after Call Claude API)
8. Name it: `Extract AI Response`
9. Code:
```javascript
const response = $input.first().json;
const chatId = $('Prepare AI Request').item.json.chat_id;
const aiMessage = response.content[0].text;

return [{
  json: {
    chat_id: chatId,
    text: aiMessage
  }
}];
```

10. Add **Telegram** node to send AI response

---

## Final Step: Merge All Responses

All handler paths should end with sending a Telegram message. The workflow naturally ends after responding.

---

## Testing the Workflow

1. **Save** the workflow
2. **Activate** it (toggle switch in top right)
3. Open Telegram and message your bot:
   - `/start` - Should get welcome message
   - `/help` - Should get command list
   - "Hello!" - Should get AI response
4. Check n8n **Executions** to debug any issues

---

## Next Steps

Once this workflow is working:
1. Build **04-daily-briefing** workflow
2. Build **02-email-processing** workflow
3. Enhance natural language handler with more context
4. Add inline keyboard buttons for quick actions

---

## Common Issues

**Issue**: Webhook not receiving messages
- Check Telegram webhook is set correctly
- Verify ngrok is running
- Test with: `curl -X POST https://your-ngrok-url/webhook/telegram-bot -d '{"message":{"text":"test"}}'`

**Issue**: Database queries fail
- Check Supabase credentials
- Verify tables exist
- Test query in Supabase SQL editor first

**Issue**: AI API errors
- Check API key is correct
- Verify request format
- Check API quotas

---

**Workflow Complete!** You now have a functional Telegram interface for your AI PA.
