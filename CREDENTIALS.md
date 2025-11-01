# AIPA System Credentials Reference
# Created: November 1, 2025
# WARNING: Keep this file secure and private!

## Telegram Bot
Bot Username: @aipa_woody_bot
Bot Token: 8266056282:AAHhTaM_1sRI5ekjnCHuBjlKmRvbKQQTEhI
Your Telegram ID: 1523060830

## Supabase Database
Project URL: https://neoeoabqcfpopzkwvcxq.supabase.co
Project Ref: neoeoabqcfpopzkwvcxq
Anon Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck
Database Password: #ErazerP15
Database Host: db.neoeoabqcfpopzkwvcxq.supabase.co
Database User: postgres
Database Name: postgres
Database Port: 5432

## n8n Server
Local URL: http://192.168.0.14:5678
API Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmMTFlODY2Zi0wZTViLTRiYzUtYjU0NC00YzhkNTkwNjljNWYiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzYyMDIxODg4fQ.FwFK-AbfuTuNOqTntG3otFfo7eOoklVLSzdRx9aMrdI

## n8n Credential Names (for reference)
- AIPA Telegram Bot (Telegram API) ✅
- AIPA Supabase REST (Header Auth) ✅ - Using REST API instead of direct PostgreSQL
- AIPA Gmail (Gmail OAuth2) ✅ - Google OAuth setup
- Google OAuth (for Calendar/Drive) ✅ - Google OAuth setup

## Supabase REST API Details
Base URL: https://neoeoabqcfpopzkwvcxq.supabase.co/rest/v1/
API Key Header: apikey
API Key Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck

## Business Contexts in Database
1. personal - Personal life management
2. woodys-creations - Woody's Creations UK (laser-cut gifts)
3. dj-business - DJ Business (event services)
4. bmf-work - BMF Work (contract work)
5. the-top-odd - The Top Odd (pub management)

## Gmail Labels Created
Main Labels:
- WoodysCreations (Green)
- DJ-Business (Red)
- BMF-Work (Orange)
- TheTopOdd (Purple)
- Personal (Blue)

Each with sub-labels: /Urgent, /Orders or /Bookings, /Suppliers, /Customers, /Processed, /AwaitingReply

## User Account
Telegram ID: 1523060830
Username: woody
Role: admin
Access: All business contexts

## Security Notes
- Keep this file private and secure
- Never commit to Git or share publicly
- Rotate credentials regularly
- Use environment variables in production

## Setup Status
✅ Phase 1: Foundation (Telegram, Supabase, Gmail Labels)
✅ Phase 2: Integration (Google OAuth, Telegram Bot, Database)
🔄 Phase 3: Build Workflows (Next step)