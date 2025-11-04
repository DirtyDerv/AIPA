# Simple Instructions: Fix Telegram HTTPS Error

## What's the problem?
Telegram needs HTTPS for webhooks. Your ngrok provides HTTPS, but n8n doesn't know to use it yet.

---

## 🎯 Simple Solution (Choose ONE based on your setup)

### Is n8n running on THIS Windows computer?

**Yes, it's on this computer:**
1. Double-click `configure_n8n.bat`
2. Wait for n8n to start
3. Go to step "After Configuration" below

**No, it's on a Linux/Raspberry Pi:**
1. Copy `configure_n8n.sh` to the machine running n8n
2. On that machine, run:
   ```bash
   chmod +x configure_n8n.sh
   ./configure_n8n.sh
   ```
3. Go to step "After Configuration" below

**I don't know / Not sure:**
- n8n is accessible at `192.168.0.14:5678`
- This means it's probably running on another device
- Do you have a Raspberry Pi or Linux server?
  - If yes → Use the Linux script
  - If no → Use the Windows script

---

## 🔧 After Configuration

### 1. Open n8n UI
Go to: http://192.168.0.14:5678

### 2. Check if it worked
1. Click "Workflows" → "AIPA - Telegram Main Interface"
2. Click on the "Telegram Trigger" node (the first blue node)
3. Look at the webhook URL displayed
4. **Good:** It shows `https://uniterative-futile-charmain.ngrok-free.dev/webhook/...`
5. **Bad:** It still shows `http://192.168.0.14:5678/webhook/...`

### 3. Activate the workflow
1. Click the toggle switch at the top
2. It should now activate WITHOUT the HTTPS error!

### 4. Test it!
Send `/start` to your Telegram bot

You should get a welcome message! 🎉

---

## ⚡ Quick Emergency Alternative

If the scripts don't work, here's a manual fix:

1. **Find where n8n is running** (open a terminal/SSH on that machine)

2. **Stop n8n:**
   ```bash
   pkill n8n
   ```
   or press Ctrl+C if it's running in a terminal

3. **Start with this exact command:**
   ```bash
   WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev n8n start
   ```

4. **Leave that terminal open** and proceed to "After Configuration" above

---

## 🆘 Still Not Working?

Try the **Polling Mode** (no HTTPS needed):

1. Open workflow → Click "Telegram Trigger" node
2. In the node settings, find "Updates" parameter
3. Change from whatever it is to **"Polling"**
4. Save the workflow
5. Activate it

Polling mode checks for messages instead of using webhooks. It works without HTTPS but is a bit slower.

---

## 📞 Need More Help?

Tell me:
1. What type of device is running n8n at 192.168.0.14?
   - Windows PC?
   - Raspberry Pi?
   - Linux server?
   - Docker container?

2. Can you access that device directly?
   - Do you have a keyboard/monitor connected?
   - Do you SSH into it?

And I'll give you more specific instructions!

---

**Most common solution:** n8n is on a Raspberry Pi or Linux server → Use `configure_n8n.sh`
