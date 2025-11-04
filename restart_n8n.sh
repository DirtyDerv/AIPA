#!/bin/bash
# Safe script to restart n8n Docker with HTTPS webhook support

echo "Stopping existing n8n container..."
docker stop $(docker ps -q --filter ancestor=n8nio/n8n) 2>/dev/null

echo "Removing old container..."
docker rm $(docker ps -aq --filter ancestor=n8nio/n8n) 2>/dev/null

echo "Starting n8n with HTTPS webhook URL..."
docker run \
  --hostname=5cbd5e6e12a6 \
  --user=node \
  --env=PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
  --env=NODE_VERSION=22.18.0 \
  --env=YARN_VERSION=1.22.22 \
  --env=NODE_ICU_DATA=/usr/local/lib/node_modules/full-icu \
  --env=NODE_ENV=production \
  --env=N8N_RELEASE_TYPE=stable \
  --env=SHELL=/bin/sh \
  --env=WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev \
  --network=bridge \
  --workdir=/home/node \
  -p 5678:5678 \
  --restart=always \
  --name=n8n \
  --label='org.opencontainers.image.description=Workflow Automation Tool' \
  --label='org.opencontainers.image.source=https://github.com/n8n-io/n8n' \
  --label='org.opencontainers.image.title=n8n' \
  --label='org.opencontainers.image.url=https://n8n.io' \
  --label='org.opencontainers.image.version=1.117.3' \
  --runtime=runc \
  -d \
  n8nio/n8n:latest

echo ""
echo "Waiting for n8n to start..."
sleep 5

echo ""
echo "Checking status..."
docker ps | grep n8n

echo ""
echo "Done! n8n should now be running with HTTPS webhook support."
echo ""
echo "Next steps:"
echo "1. Open http://192.168.0.14:5678"
echo "2. Go to Workflows > AIPA - Telegram Main Interface"
echo "3. Click the Telegram Trigger node"
echo "4. Verify webhook URL shows HTTPS"
echo "5. Activate the workflow"
echo "6. Send /start to your Telegram bot"
