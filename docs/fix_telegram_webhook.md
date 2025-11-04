# Fix Telegram Webhook HTTPS Error

## The Problem
Telegram requires HTTPS URLs for webhooks. Your n8n is running on HTTP locally, but you have ngrok providing HTTPS access.

**Your ngrok URL:** https://uniterative-futile-charmain.ngrok-free.dev ✅ (Working!)

---

## Solution: Configure n8n to Use HTTPS URL

### Step 1: Stop n8n
If n8n is running, stop it first (Ctrl+C in terminal, or stop the service)

### Step 2: Set Webhook URL Environment Variable

**If running n8n via command line:**
```bash
# On Windows PowerShell:
$env:WEBHOOK_URL="https://uniterative-futile-charmain.ngrok-free.dev"
n8n start

# On Windows CMD:
set WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev
n8n start

# On Linux/Mac:
WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev n8n start
```

**If running n8n via Docker:**
```bash
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n
```

**If running n8n as a service:**
Edit your service configuration file and add:
```
Environment="WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev"
```

### Step 3: Alternative - Use .env File

Create or edit file: `~/.n8n/.env` (or wherever your n8n data is stored)

Add this line:
```
WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev
```

Then restart n8n.

---

## Step 4: Verify Configuration

After restarting n8n:

1. Open n8n UI: http://192.168.0.14:5678
2. Open any workflow with a Telegram Trigger node
3. Click on the Telegram Trigger node
4. Look for the webhook URL shown in the node
5. **It should show:** `https://uniterative-futile-charmain.ngrok-free.dev/webhook/...`
   - NOT: `http://192.168.0.14:5678/webhook/...`

---

## Step 5: Activate Workflows

Once the webhook URL is configured correctly:

1. Go to Workflows
2. Click on "AIPA - Telegram Main Interface"
3. Click the toggle to activate
4. **Should now work without the HTTPS error!**

---

## Important Notes

### ⚠️ ngrok URL Changes
If you're using the free version of ngrok, your URL changes every time you restart ngrok. If that happens:
- You'll need to update the WEBHOOK_URL environment variable
- Deactivate and reactivate all Telegram workflows

### ✅ ngrok Static URL
If you have a paid ngrok account with a static URL, this is a one-time setup.

### 🔄 Keep ngrok Running
Make sure ngrok is always running when you want to use Telegram workflows:
```bash
ngrok http 5678
```

---

## Quick Checklist

- [ ] ngrok is running and forwarding to port 5678
- [ ] ngrok URL is: https://uniterative-futile-charmain.ngrok-free.dev
- [ ] n8n stopped
- [ ] WEBHOOK_URL environment variable set
- [ ] n8n restarted with new configuration
- [ ] Opened workflow and verified webhook URL shows HTTPS
- [ ] Activated "AIPA - Telegram Main Interface" workflow
- [ ] No HTTPS error!

---

## Testing

After activation, test your Telegram bot:

```
Send to your bot: /start
Expected: Welcome message with menu
```

If you still get an error, check:
1. Is ngrok still running?
2. Does the ngrok URL still work? (visit it in browser)
3. Did you restart n8n after setting WEBHOOK_URL?

---

## Alternative: Use Polling Instead of Webhooks

If you can't get webhooks working, you can use Telegram polling instead:

1. In the workflow, find the Telegram Trigger node
2. Change from "Webhook" mode to "Polling" mode
3. This doesn't require HTTPS but is less efficient

---

**Last Updated:** 2025-11-02
