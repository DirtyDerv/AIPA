# AI Personal Assistant - User Guide

## Welcome to Your AI PA!

This guide shows you how to use your AI Personal Assistant system effectively. Once setup is complete, this is your day-to-day reference.

---

## Quick Start

### Your Daily Routine

**Every Morning** (8:00 AM - automatic):
- Receive daily briefing via Telegram
- Review schedule, urgent emails, and priorities

**Throughout the Day**:
- Respond to urgent notifications
- Use natural language to interact with PA
- Check context-specific summaries as needed

**End of Day** (optional):
- Log BMF work hours if applicable
- Review completed tasks
- Preview tomorrow's schedule

---

## Telegram Commands Reference

### Essential Commands

#### `/start`
**Purpose**: Initialize or reset the bot
**When to use**: First time setup, or if bot seems unresponsive
**Response**: Welcome message with capabilities overview

---

#### `/briefing`
**Purpose**: Get comprehensive daily summary
**When to use**: Every morning, or anytime you need a full overview
**Response**:
```
🌅 Good morning, Woody!

📅 TODAY'S SCHEDULE
• 9:00 AM - BMF Project Call (60 min) 💼
• 2:00 PM - Woody's: Production (120 min) 🏢

📧 EMAIL UPDATES (12 unread)
• Woody's: 3 new orders, 1 supplier
• DJ: 2 bookings (URGENT) 🔴
• BMF: 1 project update
• Personal: 6 (auto-filed)

✅ PRIORITIES TODAY
1. [DJ] Respond to booking inquiries
2. [Woody's] Process new orders

💡 INSIGHTS
- DJ bookings up 40% this month
- Oak wood stock low
```

**Pro Tips**:
- Run `/briefing` first thing every morning
- Use again before bed to preview tomorrow
- Check mid-day if you feel overwhelmed

---

#### `/email`
**Purpose**: Get email triage summary
**When to use**: When you see notification, or checking what needs attention
**Response**:
```
📧 UNPROCESSED EMAILS

🏢 Woody's Creations: 3 (1 URGENT 🔴)
🎵 DJ Business: 2 (2 URGENT 🔴)
💼 BMF Work: 1
👤 Personal: 6

Total: 12 emails
🔴 3 require immediate attention
```

**What to do next**:
- Check Gmail for urgent items
- Reply to time-sensitive emails first
- Others can wait for batch processing

---

#### `/calendar`
**Purpose**: View today's schedule
**When to use**: Planning your day, before scheduling new events
**Response**:
```
📅 TODAY'S SCHEDULE

💼 09:00 - BMF Project Call (60 min)
   📍 Zoom link in calendar

🏢 14:00 - Production Time (120 min)
   📍 Workshop

👤 19:00 - Dinner with Angie (90 min)
   📍 Home
```

**Pro Tips**:
- Check before agreeing to new meetings
- Use to plan breaks between events
- Review at start of day to mentally prepare

---

#### `/tasks`
**Purpose**: See pending tasks across all businesses
**When to use**: Planning work, checking what's due
**Response**:
```
✅ PENDING TASKS

🔴 URGENT:
• [DJ] Respond to booking inquiry (Today, 5 PM)
• [Woody's] Order #WC001 - Customer follow-up (Overdue)

HIGH PRIORITY:
• [BMF] Complete Phase 2 deliverables (Nov 5)
• [Woody's] Order wood supplies (This week)

MEDIUM:
• [Personal] Schedule dentist appointment
• [DJ] Update website portfolio
```

**Actions**:
- Tap task to mark complete
- View details for more info
- Snooze if not ready to tackle

---

#### `/context [business]`
**Purpose**: Switch business context for focused work
**When to use**: Deep work on one business, reviewing specific area
**Usage**:
```
/context
/context woodys
/context dj
/context bmf
/context pub
/context personal
```
**Response**: Context menu or confirmation of switch

**Why use this**:
- Focus on one business at a time
- Reduce cognitive load
- Get context-specific insights

---

#### `/help`
**Purpose**: Show command reference
**When to use**: Forgot a command, exploring features
**Response**: Full command list with descriptions

---

### Advanced Commands (Coming Soon)

#### `/report [business]`
**Purpose**: Get business metrics and insights
**Example**: `/report dj`
**Response**: Weekly/monthly performance summary

#### `/schedule [event]`
**Purpose**: Add calendar event with natural language
**Example**: `/schedule DJ practice tomorrow 2-4 PM`

#### `/task [description]`
**Purpose**: Quick task creation
**Example**: `/task Call oak supplier about bulk order`

---

## Natural Language Interaction

The most powerful way to use your AI PA is through natural conversation.

### What You Can Ask

#### Email Queries
```
"What's urgent today?"
"Show me Woody's Creations emails"
"Any new DJ inquiries?"
"Has Brian emailed about the project?"
"Show me unread emails from this week"
```

#### Calendar Queries
```
"What's on my calendar tomorrow?"
"When is my next meeting?"
"Am I free Thursday afternoon?"
"What time is the DJ gig on Saturday?"
"Show me this week's schedule"
```

#### Task Queries
```
"What should I work on today?"
"Show me overdue tasks"
"List all Woody's Creations tasks"
"What's due this week?"
"Create a task to follow up with supplier"
```

#### Business Queries
```
"How many DJ bookings this month?"
"Show me recent Woody's Creations orders"
"What BMF projects am I working on?"
"What's my revenue for DJ business?"
"Compare this month to last month"
```

#### General Queries
```
"What should I prioritize right now?"
"Give me a quick update"
"What did I forget to do?"
"Schedule a production block tomorrow"
"Remind me to call the wood supplier"
```

### How AI PA Responds

**Quick Factual Answers**:
```
You: "When's my next meeting?"
PA: "Your next meeting is tomorrow at 9 AM - BMF Project Call with Brian."
```

**Actionable Summaries**:
```
You: "What's urgent?"
PA: "3 urgent items:
1. DJ booking inquiry (respond by 5 PM today)
2. Woody's order delayed - customer waiting
3. BMF deliverable due tomorrow

Start with the DJ inquiry?"
```

**Proactive Suggestions**:
```
You: "What should I do next?"
PA: "Based on your priorities:

1. Reply to 2 urgent DJ inquiries (15 min)
2. Schedule production for Woody's orders (30 min)
3. Prep for tomorrow's BMF call (20 min)

You have a 2-hour block free now. Start with DJ?"
```

---

## Working with Business Contexts

### Woody's Creations 🏢

**Common Tasks**:
- Process new orders
- Schedule production time
- Manage supplier communications
- Track inventory
- Follow up with customers

**Typical Workflow**:
1. Check new order emails (morning)
2. Schedule production blocks in calendar
3. Create tasks for each order
4. Update customers on progress
5. Mark orders complete when shipped

**AI PA Helps With**:
- Classifying order vs. inquiry emails
- Estimating production time needed
- Flagging material shortages
- Reminding about due dates
- Tracking revenue

---

### DJ Business 🎵

**Common Tasks**:
- Respond to booking inquiries
- Send quotes and contracts
- Schedule gig dates
- Track deposits and payments
- Follow up after events

**Typical Workflow**:
1. New inquiry email arrives → AI PA flags as urgent
2. Check calendar for availability
3. Send quote (use template)
4. Contract signed → Add to calendar
5. Prep checklist before event
6. Post-event follow-up

**AI PA Helps With**:
- Prioritizing hot leads
- Checking calendar conflicts
- Tracking payment status
- Event preparation reminders
- Revenue and booking trends

---

### BMF Work 💼

**Common Tasks**:
- Log work hours daily
- Track project milestones
- Respond to Brian's emails
- Submit timesheets
- Invoice tracking

**Typical Workflow**:
1. Morning: Review project tasks
2. Work on deliverables
3. End of day: Log hours
4. Weekly: Submit timesheet
5. Monthly: Track invoicing

**AI PA Helps With**:
- Daily work hour reminders
- Project deadline tracking
- Email summaries from Brian
- Timesheet calculations
- Invoice status monitoring

---

### Personal 👤

**Common Tasks**:
- Family appointments
- Bill payments
- Personal errands
- Health tracking
- Social plans

**AI PA Helps With**:
- Separating work from personal
- Bill due date reminders
- Appointment scheduling
- Family calendar coordination

---

## Email Management

### How Email Processing Works

**Every 15 minutes automatically**:
1. AI PA fetches new unread emails
2. Classifies by business context
3. Determines priority and action needed
4. Applies Gmail labels
5. Stores in database
6. Notifies you if urgent

### Priority Levels

**🔴 URGENT** (Immediate notification):
- Customer complaints
- Last-minute booking changes
- Today's deadlines
- Payment issues
- Emergency situations

**HIGH** (In briefing):
- New orders/bookings
- Supplier issues
- This week's deadlines
- Client responses

**MEDIUM** (Batch review):
- General inquiries
- Updates
- Non-urgent follow-ups

**LOW** (Weekly review):
- Newsletters
- Marketing
- General information

### Action Types

**REPLY**:
- Questions needing response
- Customer service
- Booking inquiries
- Project discussions

**SCHEDULE**:
- Meeting requests
- Appointments
- Event bookings
- Deadlines to calendar

**FILE**:
- Receipts
- Confirmations
- Reference documents

**FORWARD**:
- Needs someone else (rare)
- Angie should handle

**NONE**:
- FYI only
- Already handled
- Spam/marketing

### Managing Your Inbox

**Best Practices**:
1. Trust the AI classification
2. Focus on urgent items first
3. Batch process medium priority
4. Archive low priority weekly
5. Report misclassifications (AI learns)

**Daily Routine**:
- Morning: Review urgent via `/email`
- Mid-day: Check notifications
- Evening: Batch process remaining
- Weekly: Archive old processed emails

---

## Calendar Management

### Multi-Calendar System

You have 5 color-coded calendars:
- 🏢 **Woody's Creations** (Green) - Production, suppliers
- 🎵 **DJ Business** (Red) - Gigs, client meetings
- 💼 **BMF Work** (Orange) - Project work, calls with Brian
- 🍺 **Pub Future** (Purple) - Planning, licensing
- 👤 **Personal** (Blue) - Family, appointments

### Scheduling Best Practices

**Use context blocking**:
```
Monday AM: BMF Work (deep focus)
Monday PM: Woody's Production
Tuesday PM: DJ bookings
```

**Buffer time**:
- 15 min between meetings
- 30 min for transitions
- 1 hour for lunch

**Protect time**:
- Block personal time
- Schedule "focus blocks"
- Mark unavailable periods

### AI PA Calendar Features

**Conflict Detection**:
- Warns before double-booking
- Suggests alternative times
- Checks across all contexts

**Smart Suggestions**:
- Best times for production (when you're freshest)
- DJ gig prep time (before events)
- BMF meeting patterns (Brian's availability)

**Automatic Blocking**:
- DJ gig → +1 hour setup before
- Order confirmed → Production time blocked
- Meeting scheduled → Prep time added

---

## Task Management

### Task Lifecycle

1. **Created** (manually or auto from email)
2. **Pending** (in queue)
3. **In Progress** (actively working)
4. **Completed** (done!)
5. **Cancelled** (no longer needed)

### Task Priorities

**URGENT** (Do today):
- Deadline today
- Customer waiting
- Blocking others

**HIGH** (This week):
- Important deadlines
- Revenue-generating
- Client-facing

**MEDIUM** (Next 2 weeks):
- Planned work
- Improvements
- Follow-ups

**LOW** (Someday):
- Nice to have
- Ideas
- Backlog

### Working with Tasks

**Creating Tasks**:
```
Natural language:
"Create task: Order oak wood supplies"
"Remind me to follow up with DJ inquiry"
"Add task to call supplier tomorrow"

Command (future):
/task Order oak wood supplies by Friday
```

**Completing Tasks**:
```
"Mark task complete: Call supplier"
"Done with order #WC001"
```

**Rescheduling**:
```
"Move task to tomorrow: Update website"
"Snooze dentist appointment"
```

---

## Daily Workflow Example

### Morning (8:00 AM - 9:00 AM)

1. **Receive Daily Briefing** (automatic at 8 AM)
   - Review schedule
   - Note urgent emails
   - Check priorities

2. **Process Urgent Items** (15-30 min)
   ```
   "What's urgent today?"
   ```
   - Reply to DJ inquiries
   - Address customer issues
   - Handle time-sensitive items

3. **Plan Your Day** (10 min)
   ```
   "/calendar"
   "/tasks"
   ```
   - Confirm meetings
   - Prioritize tasks
   - Block focus time

### Throughout Day

4. **Check Notifications**
   - AI PA sends urgent alerts
   - Quick responses via Telegram
   - Defer non-urgent to batch time

5. **Context Switching**
   - Use `/context` to focus
   - Work in blocks (Woody's, DJ, BMF)
   - Minimize task switching

6. **Log Work** (BMF)
   - End of work: Log hours
   - Quick note on what was done

### Evening (6:00 PM - 7:00 PM)

7. **Batch Process Emails** (20 min)
   - Review non-urgent emails
   - Reply to what you can
   - Create tasks for rest

8. **Review Day** (10 min)
   - Mark completed tasks
   - Update any calendar changes
   - Check tomorrow's briefing preview

9. **Prepare for Tomorrow**
   ```
   "What's on my schedule tomorrow?"
   "Show me tomorrow's priorities"
   ```

---

## Tips & Tricks

### Productivity Tips

**Use Voice Messages** (future feature):
- Telegram voice → AI transcribes → Processes
- Faster than typing while working

**Batch Similar Tasks**:
- Process all Woody's emails together
- Make all supplier calls in one block
- Update all orders at once

**Context Blocking**:
- Monday AM: BMF only
- Tuesday PM: Woody's production
- Wednesday: DJ business focus

**Weekly Reviews**:
- Sunday evening: Business strategist report
- Review week's achievements
- Plan next week's priorities

### Communication Tips

**Be Specific**:
- Bad: "Show me emails"
- Good: "Show me urgent DJ emails from today"

**Use Context**:
- Start with `/context dj`
- Then ask DJ-specific questions
- AI PA maintains context

**Ask Follow-ups**:
```
You: "How many orders this week?"
PA: "7 orders for Woody's Creations"
You: "How does that compare to last week?"
PA: "Up 40% from last week's 5 orders"
```

### Efficiency Tips

**Create Templates**:
- Standard DJ quote response
- Order confirmation message
- Supplier inquiry format

**Use Shortcuts**:
- Save frequent queries
- Bookmark common views
- Use command history

**Automate Routines**:
- Daily briefing automatic
- Email processing automatic
- Reminders set once

---

## Troubleshooting

### "Bot not responding"
**Check**:
- Is ngrok running?
- Is workflow activated?
- Try `/start` to reset

### "Wrong email classification"
**Action**:
- Tell AI PA: "That email was wrong, it's actually DJ business"
- AI learns from corrections

### "Missing notifications"
**Check**:
- Telegram notifications enabled on phone
- Urgency settings correct
- Check "Executions" in n8n for errors

### "Calendar conflicts"
**Solution**:
- AI PA warns before double-booking
- Manually adjust in Google Calendar
- AI PA syncs automatically

---

## Getting Angie Set Up

When you're ready to give Angie access to Woody's Creations:

1. Get her Telegram User ID
2. Add her to database:
```sql
INSERT INTO users (telegram_id, telegram_username, first_name, role, allowed_contexts) VALUES
(987654321, 'angie_username', 'Angie', 'user', ARRAY['woodys-creations', 'personal']);
```
3. Share Woody's Creations Google Calendar
4. Share Google Drive folder
5. Show her how to use `/context woodys`

---

## Customization

### Change Briefing Time
1. Edit "Daily Briefing" workflow in n8n
2. Change cron: `0 8 * * *` → `0 7 * * *` (for 7 AM)

### Adjust Email Frequency
1. Edit "Email Processing" workflow
2. Change: `*/15 * * * *` → `*/30 * * * *` (for 30 min)

### Modify Priorities
1. Edit AI prompt: `ai-prompts/email-classifier.md`
2. Adjust urgency rules
3. AI PA adapts to your changes

---

## Keyboard Shortcuts (Telegram)

- `/` - Show command list
- `↑` - Previous message (edit/resend)
- `@` - Mention (for multi-user future)

---

## FAQ

**Q: Can I use this on multiple devices?**
A: Yes! Telegram syncs across all devices. Use phone, desktop, or web.

**Q: What if I miss a notification?**
A: All notifications stored in Telegram. Scroll up to review.

**Q: Can I undo a command?**
A: Most actions can be reversed. Ask AI PA: "Undo that" or manually fix in database.

**Q: How much does this cost to run?**
A: $0/month using free tiers. May need to upgrade if scaling significantly.

**Q: Is my data secure?**
A: Yes. Email summaries only (not full content) go to AI. Database is private. BMF work stays confidential.

**Q: Can I export my data?**
A: Yes. Supabase allows database exports. All your data is accessible.

**Q: What happens if ngrok crashes?**
A: Temporary downtime. Restart ngrok, update webhook URL. No data lost.

**Q: Can I add more businesses later?**
A: Absolutely! Add to business_contexts table and update workflows.

---

## Advanced Features (Coming Soon)

- Voice interaction
- Automated email responses
- Customer-facing booking forms
- Financial forecasting
- Inventory management
- Staff scheduling (pub)

---

## Support

Need help? Ask your AI PA:
```
"How do I...?"
"What does [command] do?"
"Show me an example of..."
```

Or check documentation:
- Setup issues: `01-SETUP-GUIDE.md`
- Workflow problems: `08-TROUBLESHOOTING.md`
- Feature requests: GitHub Issues

---

**Enjoy your AI Personal Assistant! 🚀**

Remember: The more you use it, the better it gets at understanding your preferences and patterns.

Start simple, explore features gradually, and customize to your workflow.
