#!/bin/bash
# n8n Webhook Configuration Script
# Run this on the machine where n8n is running (192.168.0.14)

echo "========================================"
echo "n8n Webhook HTTPS Configuration"
echo "========================================"
echo ""

# Set the webhook URL
export WEBHOOK_URL="https://uniterative-futile-charmain.ngrok-free.dev"

echo "✓ Webhook URL set to: $WEBHOOK_URL"
echo ""

# Check if n8n is running
if pgrep -f "n8n" > /dev/null; then
    echo "⚠ n8n is currently running. Stopping it..."
    pkill -f "n8n"
    sleep 2
    echo "✓ n8n stopped"
    echo ""
fi

# Create or update .bashrc to make it permanent
if ! grep -q "WEBHOOK_URL" ~/.bashrc; then
    echo "" >> ~/.bashrc
    echo "# n8n Webhook Configuration" >> ~/.bashrc
    echo "export WEBHOOK_URL=\"https://uniterative-futile-charmain.ngrok-free.dev\"" >> ~/.bashrc
    echo "✓ Added WEBHOOK_URL to ~/.bashrc (permanent)"
else
    echo "✓ WEBHOOK_URL already in ~/.bashrc"
fi

echo ""
echo "Starting n8n with HTTPS webhook support..."
echo ""

# Start n8n with the webhook URL
nohup n8n start > ~/n8n.log 2>&1 &

sleep 3

# Check if n8n started successfully
if pgrep -f "n8n" > /dev/null; then
    echo "========================================"
    echo "✓ SUCCESS! n8n is now running with HTTPS webhooks"
    echo "========================================"
    echo ""
    echo "Next steps:"
    echo "1. Open http://192.168.0.14:5678 in your browser"
    echo "2. Open 'AIPA - Telegram Main Interface' workflow"
    echo "3. Click on the 'Telegram Trigger' node"
    echo "4. Verify the webhook URL shows HTTPS"
    echo "5. Activate the workflow"
    echo "6. Test by sending /start to your Telegram bot"
    echo ""
    echo "n8n logs: tail -f ~/n8n.log"
else
    echo "❌ ERROR: n8n failed to start"
    echo "Check logs: cat ~/n8n.log"
fi
