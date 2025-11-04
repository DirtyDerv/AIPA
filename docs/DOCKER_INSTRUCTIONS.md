# Docker Instructions: Fix Telegram HTTPS Webhook

## Your Setup
- n8n running in Docker at **192.168.0.14**
- Need to add WEBHOOK_URL environment variable to the Docker container

---

## 🚀 Quick Fix (Recommended)

### Step 1: Access the Docker Host

**Connect to 192.168.0.14:**
```bash
ssh user@192.168.0.14
```
*(Replace "user" with your actual username)*

Or if you have direct access to that machine, just open a terminal there.

---

### Step 2: Run the Configuration Script

**Option A: Copy and run my script**

1. Copy `restart_n8n_docker.sh` to the Docker host
2. Run these commands:
   ```bash
   chmod +x restart_n8n_docker.sh
   ./restart_n8n_docker.sh
   ```

**Option B: Manual commands** (if script doesn't work)

Run these commands one by one:

```bash
# 1. Find your n8n container
docker ps -a | grep n8n

# 2. Stop the container (replace 'n8n' with actual container name if different)
docker stop n8n

# 3. Remove the container
docker rm n8n

# 4. Start new container with WEBHOOK_URL
docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e WEBHOOK_URL="https://uniterative-futile-charmain.ngrok-free.dev" \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# 5. Check if it's running
docker ps | grep n8n
```

---

### Step 3: Verify It Worked

```bash
# Check the logs
docker logs n8n

# You should see n8n starting up without errors
```

---

## ✅ Test the Configuration

### 1. Open n8n UI
Go to: http://192.168.0.14:5678

### 2. Check Webhook URL
1. Click **Workflows** → **"AIPA - Telegram Main Interface"**
2. Click the **"Telegram Trigger"** node (first blue box)
3. Look at the webhook URL displayed
4. **It should show:** `https://uniterative-futile-charmain.ngrok-free.dev/webhook/...`
   - ✅ **Good!** The HTTPS URL is being used
   - ❌ **Still HTTP?** The environment variable didn't apply, see troubleshooting below

### 3. Activate the Workflow
1. Click the **toggle switch** at the top
2. Should activate **without the HTTPS error!**

### 4. Test Your Bot
Send to your Telegram bot:
```
/start
```

You should get a welcome menu! 🎉

---

## 🔧 Troubleshooting

### If you get: "container already exists"

```bash
docker stop n8n
docker rm n8n
# Then run the docker run command again
```

### If you get: "port is already in use"

```bash
# Find what's using port 5678
docker ps -a

# Stop all containers using that port
docker stop $(docker ps -q --filter "publish=5678")

# Then run the docker run command again
```

### If webhook URL still shows HTTP (not HTTPS)

Check the environment variable is set:
```bash
docker inspect n8n | grep WEBHOOK_URL
```

Should show:
```
"WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev"
```

If it doesn't show up, the container wasn't started with the -e flag. Try the manual commands again.

---

## 📝 Alternative: Use Docker Compose

If you're using docker-compose, edit your `docker-compose.yml`:

```yaml
version: '3'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev
    volumes:
      - ~/.n8n:/home/node/.n8n
```

Then:
```bash
docker-compose down
docker-compose up -d
```

---

## ⚡ Emergency Alternative: Polling Mode

If you can't restart the container right now, use Polling mode instead:

1. Open the workflow in n8n UI
2. Click "Telegram Trigger" node
3. Find "Updates" parameter
4. Change to **"Polling"**
5. Save and activate

**Note:** Polling is slower but doesn't need HTTPS webhooks.

---

## 🆘 Still Need Help?

Tell me:
1. Can you SSH to 192.168.0.14? Or do you have physical access?
2. What error message do you get (if any)?
3. Output of: `docker ps -a | grep n8n`

And I'll provide more specific help!

---

**Quick Summary:**
```bash
ssh user@192.168.0.14
docker stop n8n && docker rm n8n
docker run -d --name n8n -p 5678:5678 \
  -e WEBHOOK_URL="https://uniterative-futile-charmain.ngrok-free.dev" \
  -v ~/.n8n:/home/node/.n8n n8nio/n8n
```

Then activate the workflow in the UI!
