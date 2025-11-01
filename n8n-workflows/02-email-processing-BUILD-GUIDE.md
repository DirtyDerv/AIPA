# Email Processing Workflow - Build Guide

## Overview
This workflow runs automatically every 15 minutes to:
1. Fetch new unread emails from Gmail
2. Classify them by business context using AI
3. Apply appropriate Gmail labels
4. Store in Supabase database
5. Send Telegram notification for urgent emails

## Workflow Summary
```
Cron Schedule (Every 15min) → Fetch Gmail → Classify with AI → Apply Labels → Store in DB → Notify if Urgent
```

---

## Step-by-Step Build Instructions

### Node 1: Schedule Trigger
1. Add node: **Schedule Trigger**
2. Name it: `Every 15 Minutes`
3. Configure:
   - **Trigger Interval**: `Minutes`
   - **Minutes Between Triggers**: `15`
   - Alternative: Use **Cron** for more control: `*/15 * * * *`
4. This triggers the workflow every 15 minutes

### Node 2: Fetch Unread Emails
1. Add node: **Gmail** (after Schedule Trigger)
2. Name it: `Get Unread Emails`
3. Configure:
   - **Credential**: `AIPA Gmail`
   - **Resource**: `Message`
   - **Operation**: `Get All`
   - **Filters**:
     - **Include Spam and Trash**: `false`
     - **Search**: `is:unread -label:processed`
   - **Additional Fields**:
     - **Max Results**: `10` (process 10 at a time to avoid timeout)
     - **Format**: `Metadata`
4. This fetches up to 10 unread emails

### Node 3: Check If Emails Found
1. Add node: **IF** (after Get Unread Emails)
2. Name it: `Any Emails?`
3. Configure:
   - **Condition**: `{{ $json.length > 0 }}`
4. If no emails, workflow ends here (no action needed)

### Node 4: Extract Email Data (IF True)
1. Add node: **Code** (connect to IF true output)
2. Name it: `Parse Email Data`
3. Code:
```javascript
const emails = $input.all();
const results = [];

for (const email of emails) {
  const data = email.json;

  // Extract sender info
  const fromHeader = data.payload.headers.find(h => h.name === 'From');
  const subjectHeader = data.payload.headers.find(h => h.name === 'Subject');
  const dateHeader = data.payload.headers.find(h => h.name === 'Date');
  const toHeader = data.payload.headers.find(h => h.name === 'To');

  // Parse sender name and email
  const fromFull = fromHeader?.value || '';
  const fromMatch = fromFull.match(/^(.+?)\s*<(.+?)>$/) || [null, fromFull, fromFull];
  const fromName = fromMatch[1]?.trim() || '';
  const fromEmail = fromMatch[2]?.trim() || fromFull;

  // Get snippet (preview text)
  const snippet = data.snippet || '';

  results.push({
    gmail_id: data.id,
    gmail_thread_id: data.threadId,
    subject: subjectHeader?.value || '(No Subject)',
    from_email: fromEmail,
    from_name: fromName,
    to_email: toHeader?.value || '',
    snippet: snippet.substring(0, 500), // Limit snippet
    received_at: dateHeader?.value || new Date().toISOString(),
    raw_data: data // Keep for later processing
  });
}

return results.map(r => ({ json: r }));
```

### Node 5: Classify Email with AI (Loop)
**Note**: This processes one email at a time through AI

1. Add node: **HTTP Request** (after Parse Email Data)
2. Name it: `Classify with Gemini`
3. Configure:
   - **Method**: `POST`
   - **URL**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={{ $credentials.geminapi }}`
   - **Authentication**: None (key in URL)
   - **Body** (JSON):
```json
{
  "contents": [{
    "parts": [{
      "text": "Classify this email into ONE business context. Return ONLY valid JSON.\n\nEmail:\nFrom: {{ $json.from_email }} ({{ $json.from_name }})\nSubject: {{ $json.subject }}\nPreview: {{ $json.snippet }}\n\nBusiness contexts:\n- woodys-creations: Laser gifts, manufacturing, suppliers, Etsy\n- dj-business: DJ events, bookings, music, venues\n- bmf-work: Contract work for Brian Farmer\n- pub-future: Future pub landlord duties\n- personal: Personal matters\n\nReturn JSON format:\n{\n  \"business_context\": \"woodys-creations|dj-business|bmf-work|pub-future|personal\",\n  \"confidence\": 0.95,\n  \"priority\": \"urgent|high|medium|low\",\n  \"action_needed\": \"reply|schedule|file|forward|none\",\n  \"summary\": \"Brief 1-2 sentence summary\",\n  \"key_points\": [\"point 1\", \"point 2\"],\n  \"sentiment\": \"positive|neutral|negative\",\n  \"sub_category\": \"orders|suppliers|bookings|etc\",\n  \"urgency_reason\": \"why this priority\"\n}"
    }]
  }],
  "generationConfig": {
    "temperature": 0.1,
    "maxOutputTokens": 512
  }
}
```

### Node 6: Parse AI Response
1. Add node: **Code** (after Classify with Gemini)
2. Name it: `Extract Classification`
3. Code:
```javascript
const aiResponse = $input.first().json;
const emailData = $('Parse Email Data').item.json;

// Extract text from Gemini response
const aiText = aiResponse.candidates[0].content.parts[0].text;

// Try to parse JSON from AI response
let classification;
try {
  // Find JSON in the response (might have extra text)
  const jsonMatch = aiText.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    classification = JSON.parse(jsonMatch[0]);
  } else {
    throw new Error('No JSON found in response');
  }
} catch (error) {
  // Fallback classification if AI fails
  classification = {
    business_context: 'personal',
    confidence: 0.5,
    priority: 'medium',
    action_needed: 'file',
    summary: 'Auto-classified as personal due to classification error',
    key_points: [],
    sentiment: 'neutral',
    sub_category: 'unknown',
    urgency_reason: 'Default classification'
  };
}

// Merge email data with classification
return [{
  json: {
    ...emailData,
    ...classification,
    classified_at: new Date().toISOString()
  }
}];
```

### Node 7: Get Business Context ID
1. Add node: **Postgres** (after Extract Classification)
2. Name it: `Lookup Context ID`
3. Query:
```sql
SELECT id, gmail_label
FROM business_contexts
WHERE name = '{{ $json.business_context }}'
LIMIT 1;
```

### Node 8: Store Email in Database
1. Add node: **Postgres** (after Lookup Context ID)
2. Name it: `Save to Database`
3. Query:
```sql
INSERT INTO emails (
  gmail_id,
  gmail_thread_id,
  business_context_id,
  subject,
  from_email,
  from_name,
  to_email,
  received_at,
  priority,
  ai_summary,
  action_needed,
  sentiment,
  key_points,
  is_processed,
  created_at
) VALUES (
  '{{ $('Extract Classification').item.json.gmail_id }}',
  '{{ $('Extract Classification').item.json.gmail_thread_id }}',
  '{{ $json.id }}',
  '{{ $('Extract Classification').item.json.subject }}',
  '{{ $('Extract Classification').item.json.from_email }}',
  '{{ $('Extract Classification').item.json.from_name }}',
  '{{ $('Extract Classification').item.json.to_email }}',
  '{{ $('Extract Classification').item.json.received_at }}',
  '{{ $('Extract Classification').item.json.priority }}',
  '{{ $('Extract Classification').item.json.summary }}',
  '{{ $('Extract Classification').item.json.action_needed }}',
  '{{ $('Extract Classification').item.json.sentiment }}',
  '{{ JSON.stringify($('Extract Classification').item.json.key_points) }}',
  false,
  NOW()
)
ON CONFLICT (gmail_id) DO NOTHING;
```

### Node 9: Apply Gmail Label
1. Add node: **Gmail** (after Save to Database)
2. Name it: `Add Label to Email`
3. Configure:
   - **Credential**: `AIPA Gmail`
   - **Resource**: `Message`
   - **Operation**: `Add Label`
   - **Message ID**: `{{ $('Extract Classification').item.json.gmail_id }}`
   - **Label IDs**: `{{ $('Lookup Context ID').item.json.gmail_label }}`
     - Note: You need to get label IDs first (see Gmail setup guide)
     - Or use label names if your Gmail node supports it

**Alternative**: Create labels dynamically
1. Add **Gmail** node with **Get All Labels** operation
2. Find matching label ID
3. Apply to email

### Node 10: Check If Urgent
1. Add node: **IF** (after Add Label to Email)
2. Name it: `Is Urgent?`
3. Configure:
   - **Condition**: `{{ $('Extract Classification').item.json.priority === 'urgent' }}`

### Node 11: Send Telegram Notification (IF Urgent = True)
1. Add node: **Telegram** (connect to IF true output)
2. Name it: `Notify Urgent Email`
3. Configure:
   - **Credential**: `AIPA Telegram Bot`
   - **Chat ID**: `123456789` (your Telegram user ID)
   - **Text**:
```
🔴 URGENT EMAIL

{{ $('Lookup Context ID').item.json.emoji }} {{ $('Extract Classification').item.json.subject }}

From: {{ $('Extract Classification').item.json.from_name }}
Business: {{ $('Lookup Context ID').item.json.display_name }}

Summary: {{ $('Extract Classification').item.json.summary }}

Action: {{ $('Extract Classification').item.json.action_needed }}

---
{{ $('Extract Classification').item.json.urgency_reason }}
```
   - **Parse Mode**: `Markdown`

---

## Additional Enhancements

### Enhancement 1: Mark as Read (Optional)
After processing, mark email as read:

1. Add **Gmail** node at end
2. Operation: **Mark as Read**
3. Message ID: `{{ $('Extract Classification').item.json.gmail_id }}`

### Enhancement 2: Daily Summary (Not Urgent)
Instead of notifying for each email, collect and send daily summary:

1. Don't send Telegram notification in workflow
2. Create separate **Daily Email Summary** workflow
3. Runs at end of day (e.g., 6 PM)
4. Sends summary of all emails processed today

### Enhancement 3: Auto-Reply for Common Inquiries
For DJ/Woody's Creations inquiries:

1. After classification, add **IF** node
2. Check if `sub_category === 'inquiry'`
3. Generate auto-reply with AI
4. Send via Gmail node
5. Mark in database that auto-reply was sent

### Enhancement 4: Create Tasks Automatically
For emails needing action:

1. After Save to Database
2. Add **IF** node: `action_needed === 'reply'`
3. Insert task into `tasks` table:
```sql
INSERT INTO tasks (
  business_context_id,
  title,
  description,
  priority,
  due_date,
  created_by_ai,
  ai_suggested_reason
) VALUES (
  '{{ $('Lookup Context ID').item.json.id }}',
  'Reply to: {{ $('Extract Classification').item.json.subject }}',
  '{{ $('Extract Classification').item.json.summary }}',
  '{{ $('Extract Classification').item.json.priority }}',
  NOW() + INTERVAL '24 hours',
  true,
  'Auto-created from email classification'
);
```

### Enhancement 5: Spam Detection
Add node before AI classification:

1. **Code** node to check for spam indicators
2. Common spam patterns:
   - All caps subject
   - No sender name
   - Common spam keywords
3. If spam detected, skip AI classification
4. Apply "spam" label directly

---

## Error Handling

### Handle AI API Failures
1. Wrap **Classify with Gemini** node in **Try/Catch**
2. On error, use default classification:
```javascript
{
  business_context: 'personal',
  priority: 'medium',
  action_needed: 'file',
  summary: 'Classification failed - manual review needed',
  confidence: 0.1
}
```

### Handle Gmail API Rate Limits
1. Add **Split In Batches** node before Gmail operations
2. Process 5 emails at a time
3. Add **Wait** node (5 seconds) between batches

### Log Errors
1. On any error, insert into database:
```sql
INSERT INTO ai_decisions (
  decision_type,
  input_data,
  ai_output,
  user_approved,
  created_at
) VALUES (
  'email_classification_error',
  '{{ JSON.stringify($input.first().json) }}',
  '{{ $error.message }}',
  false,
  NOW()
);
```

---

## Testing the Workflow

### Test Manually
1. **Disable** the schedule trigger temporarily
2. Add a **Manual Trigger** node at the start
3. Click **Execute Workflow**
4. Check:
   - Emails fetched correctly
   - AI classification makes sense
   - Labels applied in Gmail
   - Database updated
   - Telegram notification sent for urgent

### Test with Sample Email
1. Send yourself a test email
2. Subject: "Test Order - Custom Oak Sign"
3. Run workflow manually
4. Verify classified as "woodys-creations"

### Enable Schedule
1. Once tested, remove Manual Trigger
2. **Activate** the workflow
3. It will now run every 15 minutes automatically

---

## Monitoring

### Check Executions
1. Go to **Executions** in n8n
2. Filter by this workflow
3. Review any failed executions

### Monitor API Usage
1. Check Gemini API usage: https://aistudio.google.com/app/apikey
2. Query database for daily usage:
```sql
SELECT
  DATE(created_at) as date,
  COUNT(*) as email_count,
  AVG(confidence) as avg_confidence
FROM emails
WHERE created_at > NOW() - INTERVAL '7 days'
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Set Up Alerts
1. Add **Error Trigger** to workflow
2. On error, send Telegram notification:
```
⚠️ Email Processing Error

Workflow failed at: {{ new Date().toISOString() }}
Error: {{ $error.message }}

Check n8n executions for details.
```

---

## Performance Tips

### Reduce API Costs
- Use Gemini (free 1500/day) instead of Claude
- Cache common classifications
- Implement spam filter before AI

### Speed Up Processing
- Process in parallel with **Split In Batches**
- Reduce max emails per run if timeout issues
- Use lightweight database queries

### Improve Accuracy
- Fine-tune AI prompt based on misclassifications
- Log AI decisions for review
- Add user feedback loop (correct classifications)

---

## Next Steps

Once email processing works:
1. Build **04-daily-briefing** to include email summary
2. Add automatic task creation for actionable emails
3. Implement auto-replies for common inquiries
4. Create email templates for frequent responses

---

## Common Issues

**Issue**: No emails found
- Check Gmail search query: `is:unread -label:processed`
- Verify Gmail API is enabled
- Check OAuth permissions include Gmail

**Issue**: AI classification is wrong
- Review and refine the classification prompt
- Add more examples for edge cases
- Increase temperature for more creative classification
- Or decrease temperature for more consistent results

**Issue**: Gmail labels not applying
- Check label IDs are correct
- Verify labels exist in Gmail
- Use label names if IDs not working

**Issue**: Too many API calls
- Reduce max emails per run
- Increase interval (30 min instead of 15)
- Implement better spam filtering

---

**Workflow Complete!** Your emails are now automatically triaged and organized.
