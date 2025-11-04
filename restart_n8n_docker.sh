#!/bin/bash
# Restart n8n Docker container with HTTPS webhook support
# Run this on the machine at 192.168.0.14

echo "========================================"
echo "n8n Docker - HTTPS Webhook Configuration"
echo "========================================"
echo ""

# Find the n8n container
CONTAINER_ID=$(docker ps -a --filter "ancestor=n8nio/n8n" --format "{{.ID}}" | head -1)

if [ -z "$CONTAINER_ID" ]; then
    # Try finding by name
    CONTAINER_ID=$(docker ps -a --filter "name=n8n" --format "{{.ID}}" | head -1)
fi

if [ -z "$CONTAINER_ID" ]; then
    echo "❌ ERROR: Could not find n8n Docker container"
    echo ""
    echo "Please run this command to see all containers:"
    echo "  docker ps -a"
    echo ""
    exit 1
fi

echo "✓ Found n8n container: $CONTAINER_ID"
echo ""

# Get current container info
CONTAINER_NAME=$(docker inspect --format='{{.Name}}' $CONTAINER_ID | sed 's/\///')
CONTAINER_IMAGE=$(docker inspect --format='{{.Config.Image}}' $CONTAINER_ID)
VOLUME_MOUNT=$(docker inspect --format='{{range .Mounts}}{{if eq .Type "bind"}}{{.Source}}{{end}}{{end}}' $CONTAINER_ID)

if [ -z "$VOLUME_MOUNT" ]; then
    VOLUME_MOUNT="$HOME/.n8n"
fi

echo "Container Name: $CONTAINER_NAME"
echo "Image: $CONTAINER_IMAGE"
echo "Data Volume: $VOLUME_MOUNT"
echo ""

# Stop and remove old container
echo "Stopping and removing old container..."
docker stop $CONTAINER_ID
docker rm $CONTAINER_ID
echo "✓ Old container removed"
echo ""

# Start new container with WEBHOOK_URL
echo "Starting new container with HTTPS webhook URL..."
echo ""

docker run -d \
  --name n8n \
  -p 5678:5678 \
  -e WEBHOOK_URL="https://uniterative-futile-charmain.ngrok-free.dev" \
  -v $VOLUME_MOUNT:/home/node/.n8n \
  $CONTAINER_IMAGE

# Wait for container to start
sleep 5

# Check if container is running
if docker ps | grep -q "n8n"; then
    echo ""
    echo "========================================"
    echo "✓ SUCCESS! n8n is running with HTTPS webhooks"
    echo "========================================"
    echo ""
    echo "Container details:"
    docker ps --filter "name=n8n" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
    echo ""
    echo "Next steps:"
    echo "1. Open http://192.168.0.14:5678 in your browser"
    echo "2. Open 'AIPA - Telegram Main Interface' workflow"
    echo "3. Click on the 'Telegram Trigger' node"
    echo "4. Verify webhook URL shows: https://uniterative-futile-charmain.ngrok-free.dev/webhook/..."
    echo "5. Activate the workflow (toggle switch at top)"
    echo "6. Test by sending /start to your Telegram bot"
    echo ""
    echo "To view logs: docker logs -f n8n"
else
    echo ""
    echo "❌ ERROR: Container failed to start"
    echo "Check logs: docker logs n8n"
fi
