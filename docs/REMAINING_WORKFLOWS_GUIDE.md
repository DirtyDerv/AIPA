# Activating Remaining 7 Workflows

## ✅ SUCCESS: Telegram Main Interface is Working!

Now let's activate the other 7 workflows. They all have the same issue - old credential IDs that need to be reassigned.

---

## 🔑 For Each Workflow, You Need To:

1. **Open the workflow**
2. **Find ALL nodes with credentials** (Telegram, Supabase, Gmail, Google Calendar)
3. **Click each node and reassign credentials**
4. **Check for any missing table parameters in Supabase nodes**
5. **Save the workflow**
6. **Activate it**
7. **Test it**

---

## 📋 Workflow Activation Checklist

### 1. ⏳ Business Intelligence & Reports
**Credentials needed:**
- Telegram Bot API
- Supabase API

**Tables used:**
- `woodys_orders`
- `dj_bookings`
- `bmf_work_logs`
- `emails`

**To activate:**
1. Open workflow
2. Fix all Telegram nodes (reassign credential)
3. Fix all Supabase nodes (reassign credential + select tables)
4. Save and activate
5. Test: `/reports` in Telegram

---

### 2. ⏳ BMF Work Logging
**Credentials needed:**
- Telegram Bot API
- Supabase API

**Tables used:**
- `bmf_work_logs`

**To activate:**
1. Open workflow
2. Fix all Telegram nodes
3. Fix all Supabase nodes (table: `bmf_work_logs`)
4. Save and activate
5. Test: `/bmf` in Telegram

---

### 3. ⏳ Woody's Creations Order Processing
**Credentials needed:**
- Telegram Bot API
- Supabase API
- Gmail OAuth2 (for sending order confirmations)

**Tables used:**
- `woodys_orders`

**To activate:**
1. Open workflow
2. Fix all Telegram nodes
3. Fix all Supabase nodes (table: `woodys_orders`)
4. Fix Gmail nodes (if any)
5. Save and activate
6. Test: `/woodys` in Telegram

---

### 4. ⏳ DJ Booking Automation
**Credentials needed:**
- Telegram Bot API
- Supabase API

**Tables used:**
- `dj_bookings`

**To activate:**
1. Open workflow
2. Fix all Telegram nodes
3. Fix all Supabase nodes (table: `dj_bookings`)
4. Save and activate
5. Test: `/dj` in Telegram

---

### 5. ⏳ Multi-Business Calendar Management
**Credentials needed:**
- Telegram Bot API
- Supabase API
- Google Calendar OAuth2

**Tables used:**
- `calendar_events`

**To activate:**
1. Open workflow
2. Fix all Telegram nodes
3. Fix all Supabase nodes (table: `calendar_events`)
4. Fix Google Calendar nodes
5. Save and activate
6. Test: `/calendar` in Telegram

---

### 6. ⏳ Marketing Campaign Automation
**Credentials needed:**
- Telegram Bot API
- Supabase API

**Tables used:**
- Various (depends on campaign type)

**To activate:**
1. Open workflow
2. Fix all Telegram nodes
3. Fix all Supabase nodes
4. Save and activate
5. Test: `/marketing` in Telegram

---

### 7. ⏳ Email Processing with AI (LAST!)
**Credentials needed:**
- Gmail OAuth2
- Telegram Bot API
- Supabase API

**Tables used:**
- `emails`

**⚠️ Important:**
- This workflow runs automatically every minute
- Only activate after you've tested everything else
- Make sure Gmail labels are created: `Label_Woodys`, `Label_DJ`, `Label_BMF`, `Label_Pub`

**To activate:**
1. Open workflow
2. Fix Gmail nodes
3. Fix Telegram nodes
4. Fix all Supabase nodes (table: `emails`)
5. Save and activate
6. It will start processing emails immediately!

---

## 🚀 Quick Process for Each Workflow

```
1. Click Workflows → Select workflow
2. Look for red/orange nodes
3. Click each node → Reassign credential
4. For Supabase nodes → Also select table
5. Click Save
6. Toggle to activate
7. Check Executions tab for errors
8. Test the command in Telegram
9. Move to next workflow
```

---

## 🐛 Common Issues

### "Credential with ID X does not exist"
→ Click the node and reassign your credential

### "Could not find table X in schema cache"
→ Click Supabase node, reselect credential, then select table

### "Column X does not exist"
→ Table needs that column - let me know and I'll give you SQL to add it

### Workflow won't activate
→ Look for red nodes - they need to be fixed first

---

## 📊 Progress Tracker

- [x] 1. Telegram Main Interface ✅ **WORKING!**
- [ ] 2. Business Intelligence & Reports
- [ ] 3. BMF Work Logging
- [ ] 4. Woody's Order Processing
- [ ] 5. DJ Booking Automation
- [ ] 6. Calendar Management
- [ ] 7. Marketing Campaigns
- [ ] 8. Email Processing (do last)

---

## 💡 Pro Tips

1. **Start with simple ones first** (BMF, Reports, DJ)
2. **Leave Email Processing for last** (it auto-runs)
3. **Test each one immediately** after activating
4. **If you get stuck**, check the Executions tab for the error
5. **Each workflow takes 2-5 minutes** to fix

---

## 🎯 Estimated Time

- Simple workflows (BMF, DJ, Reports): ~5 minutes each
- Medium workflows (Woodys, Marketing): ~10 minutes each
- Complex workflows (Calendar, Email): ~15 minutes each

**Total: About 1 hour to activate all 7**

---

**Start with Business Intelligence & Reports - it's one of the simpler ones!**
