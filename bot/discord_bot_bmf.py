#!/usr/bin/env python3
"""
AIPA Discord Bot - Message Listener
This bot listens for Discord messages and processes BMF work entries

NOTE: Replace placeholder values with actual credentials from config/CREDENTIALS.md
"""

import discord
from discord.ext import commands
import requests
import json
from datetime import datetime
import asyncio

# Discord Bot Token from CREDENTIALS.md
BOT_TOKEN = "YOUR_DISCORD_BOT_TOKEN_HERE"

# BMF Work Channel ID (get from Discord Developer Portal)
BMF_CHANNEL_ID = 1234567890123456789  # Replace with actual channel ID

# Webhook URLs
BMF_WEBHOOK = "YOUR_DISCORD_WEBHOOK_URL_HERE"
N8N_BMF_WEBHOOK = "http://YOUR_N8N_SERVER_IP:5678/webhook/bmf-fixed"

# Supabase config
SUPABASE_URL = "YOUR_SUPABASE_URL_HERE/rest/v1/conversations"
SUPABASE_HEADERS = {
    'Content-Type': 'application/json',
    'apikey': 'YOUR_SUPABASE_ANON_KEY_HERE',
    'Authorization': 'Bearer YOUR_SUPABASE_ANON_KEY_HERE',
    'Prefer': 'return=minimal'
}

# Set up Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def process_bmf_work(content, author_name, channel):
    """Process a BMF work entry"""
    
    print(f"Processing BMF work: {content} from {author_name}")
    
    # Extract work description
    work_desc = content
    if content.lower().startswith('bmf work:'):
        work_desc = content[9:].strip()
    elif content.lower().startswith('bmf:'):
        work_desc = content[4:].strip()
    
    timestamp = datetime.now().isoformat()
    
    # Try to log to Supabase
    db_data = {
        'user_id': author_name,
        'message': work_desc,
        'timestamp': timestamp,
        'message_type': 'work_log'
    }
    
    db_success = False
    try:
        db_response = requests.post(SUPABASE_URL, json=db_data, headers=SUPABASE_HEADERS)
        db_success = db_response.status_code in [200, 201]
        if not db_success:
            print(f"Database error: {db_response.status_code} - {db_response.text}")
    except Exception as e:
        print(f"Database exception: {e}")
    
    # Send confirmation to Discord
    embed = discord.Embed(
        title="✅ BMF Work Logged",
        description=work_desc,
        color=0xFF6600  # Orange color for BMF
    )
    embed.add_field(name="User", value=author_name, inline=True)
    embed.add_field(name="Time", value=datetime.now().strftime("%H:%M"), inline=True)
    embed.add_field(name="Database", value="✅ Logged" if db_success else "⚠️ Partial", inline=True)
    embed.set_footer(text="AIPA Discord Bot - BMF Logging")
    
    await channel.send(embed=embed)
    
    return True

@bot.event
async def on_ready():
    """Bot is ready"""
    print(f'🤖 AIPA Bot is ready! Logged in as {bot.user}')
    print(f'🔍 Listening for BMF work entries...')
    
    # Send startup message to BMF channel
    channel = bot.get_channel(BMF_CHANNEL_ID)
    if channel:
        embed = discord.Embed(
            title="🤖 AIPA Bot Online",
            description="I'm now listening for BMF work entries!",
            color=0x00FF00
        )
        embed.add_field(
            name="📝 How to Log Work",
            value="• Type: `BMF work: your description`\n• Or just: `your work description`\n• I'll process and log it automatically!",
            inline=False
        )
        await channel.send(embed=embed)

@bot.event
async def on_message(message):
    """Handle incoming messages"""
    
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return
    
    # Check if it's in the BMF channel or mentions BMF
    is_bmf_channel = message.channel.id == BMF_CHANNEL_ID
    has_bmf_content = 'bmf' in message.content.lower()
    
    if is_bmf_channel or has_bmf_content:
        # Process as BMF work entry
        await process_bmf_work(message.content, message.author.name, message.channel)
    
    # Process other bot commands
    await bot.process_commands(message)

@bot.command(name='bmf')
async def bmf_command(ctx, *, work_description):
    """Manual BMF logging command"""
    await process_bmf_work(f"BMF work: {work_description}", ctx.author.name, ctx.channel)

@bot.command(name='status')
async def status_command(ctx):
    """Check bot status"""
    embed = discord.Embed(
        title="🤖 AIPA Bot Status",
        description="Bot is running and monitoring for BMF entries",
        color=0x0099FF
    )
    embed.add_field(name="🔍 Monitoring", value="BMF work entries", inline=True)
    embed.add_field(name="💾 Database", value="Supabase connected", inline=True)
    embed.add_field(name="🕐 Uptime", value="Active", inline=True)
    await ctx.send(embed=embed)

if __name__ == "__main__":
    print("🚀 Starting AIPA Discord Bot...")
    print("📋 Features:")
    print("   • BMF work entry logging")
    print("   • Automatic message processing")
    print("   • Database integration")
    print("   • Discord confirmations")
    
    try:
        bot.run(BOT_TOKEN)
    except Exception as e:
        print(f"❌ Bot failed to start: {e}")
        print("💡 Make sure discord.py is installed: pip install discord.py")
        print("💡 Update credentials in config/CREDENTIALS.md")