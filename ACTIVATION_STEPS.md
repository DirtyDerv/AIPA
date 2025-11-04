# Workflow Activation Steps

## ✅ Prerequisites Complete
- [x] All credentials configured
- [x] Database tables created
- [x] All 8 workflows uploaded

---

## 🚀 Activation Order (Do These In Order)

### **Step 1: Activate Telegram Main Interface** ⭐ MOST IMPORTANT

1. Go to: http://192.168.0.14:5678
2. Click **Workflows** in sidebar
3. Click **"AIPA - Telegram Main Interface"**
4. Look for the **toggle switch** at the top right
5. Click it to **activate**

**⚠️ If you get an HTTPS webhook error:**
- The WEBHOOK_URL environment variable might not be set
- Make sure the Docker container has: `--env=WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev`
- You may need to restart the container with this setting

**✅ If it activates successfully:**
- The toggle will turn green/blue
- No error messages appear
- **IMMEDIATELY TEST:** Send `/start` to your Telegram bot
- You should get a welcome menu!

---

### **Step 2: Test Telegram Bot**

Before activating more workflows, verify the main interface works:

**Open Telegram and send to your bot:**
```
/start
```

**Expected response:**
A welcome message with a menu showing all available commands.

**If you get a response:** ✅ Everything is working! Continue to Step 3.

**If no response:**
- Check if workflow is actually active (green toggle)
- Check workflow execution logs (click "Executions" tab)
- Verify Telegram credential is correct
- Make sure bot is not blocked

---

### **Step 3: Activate Simple Workflows**

Once Telegram Main Interface works, activate these (they're simpler):

**3a. Business Intelligence & Reports**
1. Open workflow: "AIPA - Business Intelligence & Reports"
2. Click toggle to activate
3. Test: Send `/reports` in Telegram

**3b. BMF Work Logging**
1. Open workflow: "AIPA - BMF Work Logging"
2. Click toggle to activate
3. Test: Send `/bmf` in Telegram

---

### **Step 4: Activate Business Workflows**

**4a. Woody's Creations Order Processing**
1. Open workflow: "AIPA - Woody's Creations Order Processing"
2. Click toggle to activate
3. Test: Send `/woodys` in Telegram

**4b. DJ Booking Automation**
1. Open workflow: "AIPA - DJ Booking Automation"
2. Click toggle to activate
3. Test: Send `/dj` in Telegram

---

### **Step 5: Activate Advanced Workflows**

**5a. Calendar Management**
1. Open workflow: "AIPA - Multi-Business Calendar Management"
2. Click toggle to activate
3. Test: Send `/calendar` in Telegram
4. **Note:** Needs Google Calendar OAuth2 configured

**5b. Marketing Campaigns**
1. Open workflow: "AIPA - Marketing Campaign Automation"
2. Click toggle to activate
3. Test: Send `/marketing` in Telegram

---

### **Step 6: Email Processing (Last)**

**⚠️ WARNING: This workflow starts processing emails immediately once activated!**

**Before activating, make sure:**
- [ ] Gmail OAuth2 is configured
- [ ] Gmail labels created: Label_Woodys, Label_DJ, Label_BMF, Label_Pub
- [ ] You're ready for it to check emails every minute

**To activate:**
1. Open workflow: "AIPA - Email Processing with AI"
2. Click toggle to activate
3. **It will automatically check your inbox every minute**
4. Check "Executions" tab to see it processing emails

---

## 🧪 Complete Test Checklist

After all workflows are activated, test each command:

```
/start          → Should show main menu
/woodys         → Should show Woody's Creations menu
/dj             → Should show DJ booking menu
/bmf            → Should show BMF work logging menu
/calendar       → Should show calendar menu
/reports        → Should show business intelligence menu
/marketing      → Should show marketing menu
```

---

## 🐛 Troubleshooting

### Workflow won't activate - "Missing credentials"
1. Open the workflow
2. Look for red nodes (nodes with errors)
3. Click on the red node
4. Click "Select credential" dropdown
5. Choose your credential
6. Save workflow
7. Try activating again

### Workflow won't activate - "HTTPS webhook error"
The WEBHOOK_URL environment variable is not set. You need to:
1. Stop Docker container
2. Restart with: `--env=WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev`

### Bot doesn't respond to commands
1. Check if "Telegram Main Interface" is active (green toggle)
2. Click "Executions" tab - look for errors
3. Verify Telegram Bot Token is correct
4. Make sure you're messaging the right bot

### Database errors when testing
1. Verify Supabase credential is correct
2. Check all required tables exist
3. Verify service_role key has proper permissions

---

## 📊 Quick Status Check

After activation, you can see status here:

**Go to:** http://192.168.0.14:5678/workflows

All workflows should show:
- ✅ Green/blue toggle (active)
- No red error icons
- Recent executions visible

---

## 🎉 Success Criteria

You'll know everything is working when:
- [x] All 8 workflows show as "Active"
- [x] `/start` command returns menu
- [x] Each business command works (`/woodys`, `/dj`, `/bmf`, etc.)
- [x] No errors in execution logs
- [x] Telegram notifications arrive when expected

---

**Start with Step 1 and let me know if you hit any issues!**
