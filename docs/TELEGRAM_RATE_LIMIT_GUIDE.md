# Telegram Rate Limit Guide - Avoiding the Frustration

## What's Happening

Telegram Bot API has strict rate limits to prevent spam:

### Rate Limits
- **30 messages per second** (per bot, across all chats)
- **1 message per second per chat** (to same chat)
- **20 messages per minute per chat group**
- **Burst limit**: Can send ~20 messages quickly, then throttled

### When You Hit the Limit
Telegram returns:
- HTTP 429 "Too Many Requests"
- Retry-After header (seconds to wait)
- Typical wait: 1-30 seconds

## Why It's Happening to You

Your AIPA system has **8 workflows** that all use Telegram:
1. Main Interface
2. Calendar Management
3. Email Processing
4. BI Reports
5. BMF Work Logging
6. DJ Booking
7. Woody's Creations
8. Marketing Campaigns

**Problem:** When testing, multiple workflows trigger → multiple messages → rate limit hit

## Solutions

### 1. Add Delays Between Telegram Nodes ⭐ BEST FIX

Add a 1-2 second delay between Telegram message nodes:

**In n8n:**
- Add a "Wait" node between consecutive Telegram nodes
- Set wait time: 1000-2000ms (1-2 seconds)

**Where to add:**
- Between menu message and options
- Between confirmation messages
- After sending lists/reports

### 2. Batch Messages Together

Instead of:
```
Send message 1
Send message 2
Send message 3
```

Do:
```
Combine into one message:
"Message 1\n\nMessage 2\n\nMessage 3"
Send once
```

### 3. Use Edit Message Instead of New Messages

For status updates, use `editMessageText` instead of sending new messages:
```
Send: "Processing..."
Edit: "Processing... 50%"
Edit: "Processing... 100%"
Edit: "Complete!"
```

### 4. Implement Message Queue

Create a dedicated "Telegram Message Queue" workflow:
- Receives message requests from all workflows
- Sends them with proper delays
- Handles rate limiting automatically

### 5. Test Mode - Disable Non-Critical Messages

During testing, comment out or disable:
- Welcome messages
- Confirmation messages
- Status updates
- Only keep critical error messages

### 6. Use Multiple Bots (Advanced)

Split workflows across multiple Telegram bots:
- Bot 1: Main Interface + Calendar
- Bot 2: BMF + DJ + Woody's
- Bot 3: Email + BI Reports + Marketing

Each bot has its own rate limit!

## Quick Fix for Testing

### Option A: Add Wait Nodes (5 minutes work)

1. Open each workflow in n8n
2. Find consecutive Telegram nodes
3. Add "Wait" node between them
4. Set to 1500ms
5. Save and test

### Option B: Disable Auto-Responses

Temporarily disable these nodes:
- "Welcome Message" in Main Interface
- "Confirm..." nodes in all workflows
- Menu messages (use direct commands instead)

### Option C: Manual Testing Protocol

Test ONE workflow at a time:
1. Deactivate all except 1 workflow
2. Test that workflow thoroughly
3. Activate next workflow
4. Repeat

Wait 60 seconds between tests.

## Monitoring Rate Limits

Check if you're being rate limited:
- Telegram will send 429 error
- n8n execution will show error
- Check n8n execution logs for "429" or "rate limit"

## Long-Term Best Practices

### 1. Rate Limit Handler Workflow

Create a central workflow that:
```javascript
// Pseudo-code
if (lastMessageTime + 1000 < now) {
  sendMessage();
  updateLastMessageTime();
} else {
  wait(1000);
  retry();
}
```

### 2. Priority Queue

- High priority: Error messages, critical alerts
- Low priority: Confirmations, status updates
- Send high priority first

### 3. Message Throttling

Set a global variable:
- Track messages sent in last second
- If > threshold, wait
- Then send

### 4. Smarter Workflows

Instead of:
- ❌ Send menu → Send confirmation → Send result

Do:
- ✅ Send menu with inline buttons
- ✅ Send result (confirmation implied)

## Emergency: Currently Rate Limited?

**What to do RIGHT NOW:**

1. **Stop testing** - Wait 60 seconds
2. **Deactivate all workflows** - Stop triggers
3. **Wait 5 minutes** - Let rate limit reset
4. **Reactivate ONE workflow** - Test slowly
5. **Add delays** - Before activating others

## Code: Add Wait Function to All Workflows

Here's a quick fix - add this Function node before each Telegram send:

```javascript
// Rate Limit Delay
const DELAY_MS = 1500; // 1.5 seconds

// Get last send time from static data
const lastSend = $workflow.staticData.lastTelegramSend || 0;
const now = Date.now();
const timeSinceLastSend = now - lastSend;

if (timeSinceLastSend < DELAY_MS) {
  // Need to wait
  const waitTime = DELAY_MS - timeSinceLastSend;
  await new Promise(resolve => setTimeout(resolve, waitTime));
}

// Update last send time
$workflow.staticData.lastTelegramSend = Date.now();

return items;
```

## Testing Schedule (Rate-Limit Safe)

**Monday:**
- Test: Main Interface + Calendar
- Wait: 5 minutes between tests

**Tuesday:**
- Test: BMF + DJ workflows
- Wait: 5 minutes between tests

**Wednesday:**
- Test: Email + BI Reports
- Wait: 5 minutes between tests

**Thursday:**
- Test: Woody's + Marketing
- Wait: 5 minutes between tests

**Friday:**
- Full integration test
- ONE command at a time
- 2-minute waits between commands

## Alternative: Use Webhook Instead

For status updates, consider:
- Send to webhook endpoint
- Log to database
- User checks via command
- Reduces message volume by 70%

## Summary

**Immediate Actions:**
1. ✅ Wait 5 minutes (rate limit reset)
2. ✅ Add 1.5s Wait nodes between Telegram messages
3. ✅ Test ONE workflow at a time
4. ✅ Combine multiple messages into one

**Long-Term:**
1. ✅ Create message queue workflow
2. ✅ Use edit message for updates
3. ✅ Implement priority system
4. ✅ Consider multiple bots for load distribution

The key is: **1-2 seconds between ANY Telegram API calls**
