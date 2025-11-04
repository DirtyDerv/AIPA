# Supabase Database Setup Guide

## Overview
Supabase provides the PostgreSQL database for storing conversations, tasks, emails, bookings, orders, and business metrics. The free tier is sufficient for your AI PA system.

## Prerequisites
- Email address for Supabase account
- GitHub account (optional, for easier signup)

---

## Part 1: Create Supabase Account

### 1.1 Sign Up
1. Go to: https://supabase.com
2. Click **Start your project**
3. Sign up with:
   - GitHub (recommended - one-click)
   - OR Email/password
4. Verify your email if using email signup

### 1.2 Create New Organization
1. After signup, you'll be prompted to create an organization
2. Organization name: `Woody's AI PA` (or personal name)
3. Plan: **Free** (includes 500 MB database, 2 GB bandwidth)
4. Click **Create organization**

---

## Part 2: Create Your Project

### 2.1 Project Setup
1. Click **New project**
2. Fill out details:
   - **Name**: `AIPA-System`
   - **Database Password**: Generate a strong password (save it securely!)
     ```
     Example: P@ssw0rd_AIPA_2025_Secure!123
     ```
   - **Region**: Choose closest to you (likely `West EU (London)`)
   - **Pricing Plan**: **Free**
3. Click **Create new project**
4. Wait 2-3 minutes for project to initialize

### 2.2 Save Project Credentials
Once project is ready, go to **Settings** > **API**:

**Copy and save these values:**
```
Project URL: https://abcdefghijklmnop.supabase.co
Project API Key (anon public): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Project API Key (service_role - KEEP SECRET): eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Database Password: [your generated password]
```

**IMPORTANT**:
- The `anon public` key is safe for client-side use
- The `service_role` key has full database access - keep it secret
- For n8n, you'll use the `service_role` key

---

## Part 3: Run Database Schema

### 3.1 Open SQL Editor
1. In Supabase dashboard, click **SQL Editor** in left sidebar
2. Click **New query**

### 3.2 Load Schema File
1. Open `AIPA/database/schema.sql` from this repository
2. Copy **ALL** the SQL code
3. Paste into Supabase SQL Editor
4. Click **Run** (or press Ctrl+Enter)
5. Wait for execution to complete (should take 10-20 seconds)

**Expected Output:**
```
Success. No rows returned
NOTICE: AIPA Database Schema created successfully!
NOTICE: Next steps:
NOTICE: 1. Configure Row Level Security policies in Supabase dashboard
NOTICE: 2. Run seed-data.sql to add test data (optional)
NOTICE: 3. Note your Supabase URL and API key for n8n configuration
```

### 3.3 Verify Tables Created
1. Click **Table Editor** in left sidebar
2. You should see these tables:
   - business_contexts
   - users
   - conversations
   - tasks
   - emails
   - calendar_events
   - dj_bookings
   - woodys_orders
   - bmf_work_log
   - ai_decisions
   - api_usage
   - notifications
   - business_metrics
   - system_settings

---

## Part 4: Add Your User

### 4.1 Insert Your Telegram User
1. Go to **SQL Editor** > **New query**
2. Paste this SQL (replace with YOUR details from Telegram bot setup):
```sql
INSERT INTO users (telegram_id, telegram_username, first_name, last_name, role, allowed_contexts, is_active)
VALUES (
    123456789,  -- YOUR Telegram ID from @userinfobot
    'woody_username',  -- Your Telegram username (without @)
    'Woody',  -- Your first name
    '',  -- Your last name (optional)
    'admin',  -- Role (admin has full access)
    ARRAY['personal', 'woodys-creations', 'dj-business', 'bmf-work', 'pub-future'],  -- All contexts
    true  -- Active user
);
```
3. Click **Run**

### 4.2 Verify User Added
1. Go to **Table Editor** > **users**
2. You should see your user record
3. Copy your user `id` (UUID) - you might need it later

---

## Part 5: Update Business Contexts

### 5.1 Add Calendar IDs
After setting up Google Calendars (from previous guide), update the database:

```sql
-- Replace with YOUR actual Calendar IDs from Google Calendar setup
UPDATE business_contexts SET calendar_id = 'woodys_creations@group.calendar.google.com'
WHERE name = 'woodys-creations';

UPDATE business_contexts SET calendar_id = 'dj_business@group.calendar.google.com'
WHERE name = 'dj-business';

UPDATE business_contexts SET calendar_id = 'bmf_work@group.calendar.google.com'
WHERE name = 'bmf-work';

UPDATE business_contexts SET calendar_id = 'pub_management@group.calendar.google.com'
WHERE name = 'pub-future';

UPDATE business_contexts SET calendar_id = 'your_email@gmail.com'
WHERE name = 'personal';
```

### 5.2 Add Drive Folder IDs
After setting up Google Drive folders:

```sql
-- Replace with YOUR actual Folder IDs from Google Drive
UPDATE business_contexts SET drive_folder_id = '3c4D5e6F7g8H9i0J1k2L'
WHERE name = 'woodys-creations';

UPDATE business_contexts SET drive_folder_id = '4d5E6f7G8h9I0j1K2l3M'
WHERE name = 'dj-business';

UPDATE business_contexts SET drive_folder_id = '5e6F7g8H9i0J1k2L3m4N'
WHERE name = 'bmf-work';

UPDATE business_contexts SET drive_folder_id = '6f7G8h9I0j1K2l3M4n5O'
WHERE name = 'pub-future';

UPDATE business_contexts SET drive_folder_id = '2b3C4d5E6f7G8h9I0j1K'
WHERE name = 'personal';
```

### 5.3 Verify Updates
```sql
SELECT name, display_name, calendar_id, drive_folder_id FROM business_contexts;
```

---

## Part 6: Configure Row Level Security (RLS)

Row Level Security ensures users can only access their own data.

### 6.1 Create Policy for Users Table
```sql
-- Allow users to read their own user record
CREATE POLICY "Users can view own record"
ON users FOR SELECT
USING (auth.uid()::text = id::text OR telegram_id = current_setting('app.current_user_telegram_id')::bigint);
```

### 6.2 Create Policy for Conversations
```sql
-- Allow users to access their own conversations
CREATE POLICY "Users can view own conversations"
ON conversations FOR SELECT
USING (user_id IN (SELECT id FROM users WHERE telegram_id = current_setting('app.current_user_telegram_id')::bigint));

-- Allow users to insert their own conversations
CREATE POLICY "Users can insert own conversations"
ON conversations FOR INSERT
WITH CHECK (user_id IN (SELECT id FROM users WHERE telegram_id = current_setting('app.current_user_telegram_id')::bigint));
```

### 6.3 Create Policy for Tasks
```sql
-- Allow users to manage tasks in their allowed contexts
CREATE POLICY "Users can view tasks in allowed contexts"
ON tasks FOR SELECT
USING (
    business_context_id IN (
        SELECT bc.id FROM business_contexts bc, users u
        WHERE u.telegram_id = current_setting('app.current_user_telegram_id')::bigint
        AND bc.name = ANY(u.allowed_contexts)
    )
);

CREATE POLICY "Users can create tasks in allowed contexts"
ON tasks FOR INSERT
WITH CHECK (
    business_context_id IN (
        SELECT bc.id FROM business_contexts bc, users u
        WHERE u.telegram_id = current_setting('app.current_user_telegram_id')::bigint
        AND bc.name = ANY(u.allowed_contexts)
    )
);

CREATE POLICY "Users can update own tasks"
ON tasks FOR UPDATE
USING (user_id IN (SELECT id FROM users WHERE telegram_id = current_setting('app.current_user_telegram_id')::bigint));

CREATE POLICY "Users can delete own tasks"
ON tasks FOR DELETE
USING (user_id IN (SELECT id FROM users WHERE telegram_id = current_setting('app.current_user_telegram_id')::bigint));
```

**Note**: For n8n workflows, you'll use the `service_role` key which bypasses RLS. RLS is more important if you build a web interface later.

---

## Part 7: Test Database Connection

### 7.1 Test Query
In SQL Editor, run:
```sql
-- Check business contexts
SELECT * FROM business_contexts;

-- Check your user
SELECT * FROM users;

-- Check system settings
SELECT * FROM system_settings;
```

All queries should return data successfully.

### 7.2 Test from n8n (After Credentials Setup)
1. In n8n, add a **Postgres** node
2. Configure with Supabase credentials
3. Operation: **Execute Query**
4. Query: `SELECT * FROM business_contexts`
5. Execute node
6. Should return 5 business contexts

---

## Part 8: Enable Realtime (Optional)

Supabase Realtime allows live updates. Useful for multi-user scenarios.

### 8.1 Enable Realtime on Tables
1. Go to **Database** > **Replication**
2. Click on **Replication** tab
3. Enable replication for these tables:
   - tasks
   - notifications
   - calendar_events
4. Click **Save**

**Note**: Not critical for initial setup, can enable later if needed.

---

## Part 9: Database Backups

### 9.1 Automatic Backups
Supabase free tier includes:
- Daily automated backups (kept for 7 days)
- Point-in-time recovery (24 hours)

View backups:
1. Go to **Settings** > **Database**
2. Scroll to **Backup** section

### 9.2 Manual Backup
Create manual backup anytime:
```bash
# Using pg_dump (requires PostgreSQL installed locally)
pg_dump "postgresql://postgres:[password]@db.[project-ref].supabase.co:5432/postgres" > backup.sql
```

Replace:
- `[password]` with your database password
- `[project-ref]` with your project reference (from project URL)

---

## Part 10: Database Maintenance

### 10.1 Monitor Usage
Check your database usage:
1. Go to **Settings** > **Usage**
2. Monitor:
   - Database size (limit: 500 MB on free tier)
   - Bandwidth (limit: 2 GB/month)
   - API requests (limit: 50,000/month)

### 10.2 Clean Old Data
Run this monthly to keep database size down:
```sql
-- Delete conversations older than 90 days
DELETE FROM conversations
WHERE created_at < NOW() - INTERVAL '90 days';

-- Delete processed emails older than 60 days
DELETE FROM emails
WHERE is_processed = true
AND received_at < NOW() - INTERVAL '60 days';

-- Delete completed tasks older than 30 days
DELETE FROM tasks
WHERE status = 'completed'
AND completed_at < NOW() - INTERVAL '30 days';

-- Delete old AI decisions (keep last 1000)
DELETE FROM ai_decisions
WHERE id NOT IN (
    SELECT id FROM ai_decisions
    ORDER BY created_at DESC
    LIMIT 1000
);

-- Delete old API usage logs (keep last 10,000)
DELETE FROM api_usage
WHERE id NOT IN (
    SELECT id FROM api_usage
    ORDER BY created_at DESC
    LIMIT 10000
);

-- Vacuum the database to reclaim space
VACUUM FULL;
```

### 10.3 Index Maintenance
Indexes are already created in schema. To rebuild if needed:
```sql
REINDEX DATABASE postgres;
```

---

## Part 11: Useful Queries for Monitoring

### 11.1 Dashboard Query
Get overview of system:
```sql
SELECT
    (SELECT COUNT(*) FROM tasks WHERE status IN ('pending', 'in_progress')) as pending_tasks,
    (SELECT COUNT(*) FROM emails WHERE is_processed = false) as unprocessed_emails,
    (SELECT COUNT(*) FROM dj_bookings WHERE status = 'inquiry') as dj_inquiries,
    (SELECT COUNT(*) FROM woodys_orders WHERE status IN ('received', 'in_design')) as pending_orders,
    (SELECT SUM(hours_worked) FROM bmf_work_log WHERE work_date >= DATE_TRUNC('month', CURRENT_DATE)) as bmf_hours_this_month;
```

### 11.2 Recent Activity
```sql
SELECT
    'conversation' as type,
    created_at,
    message_text as content
FROM conversations
WHERE created_at > NOW() - INTERVAL '24 hours'
UNION ALL
SELECT
    'task' as type,
    created_at,
    title as content
FROM tasks
WHERE created_at > NOW() - INTERVAL '24 hours'
ORDER BY created_at DESC
LIMIT 20;
```

### 11.3 Business Metrics
```sql
-- DJ Business: Monthly bookings
SELECT
    DATE_TRUNC('month', event_date) as month,
    COUNT(*) as booking_count,
    SUM(quoted_price) as total_value
FROM dj_bookings
WHERE status != 'cancelled'
GROUP BY DATE_TRUNC('month', event_date)
ORDER BY month DESC;

-- Woody's Creations: Order pipeline
SELECT
    status,
    COUNT(*) as count,
    SUM(quoted_price) as total_value
FROM woodys_orders
WHERE status != 'cancelled'
GROUP BY status;

-- BMF: Hours by month
SELECT
    TO_CHAR(work_date, 'YYYY-MM') as month,
    SUM(hours_worked) as total_hours,
    SUM(invoice_amount) as invoiced
FROM bmf_work_log
GROUP BY TO_CHAR(work_date, 'YYYY-MM')
ORDER BY month DESC;
```

---

## Part 12: Troubleshooting

### Issue: Can't connect from n8n
**Solutions:**
1. Verify you're using `service_role` key (not anon key)
2. Check database isn't paused (free tier pauses after 7 days inactivity)
3. Verify connection string format:
   ```
   Host: db.abcdefghijklmnop.supabase.co
   Port: 5432
   Database: postgres
   User: postgres
   Password: [your database password]
   ```
4. Check SSL mode is enabled

### Issue: RLS policies blocking queries
**Solutions:**
1. Use `service_role` key in n8n (bypasses RLS)
2. Or disable RLS temporarily:
   ```sql
   ALTER TABLE table_name DISABLE ROW LEVEL SECURITY;
   ```

### Issue: Database size limit reached
**Solutions:**
1. Run cleanup queries (Part 10.2)
2. Vacuum database to reclaim space
3. Upgrade to paid plan if needed ($25/month for 8 GB)

### Issue: Query performance slow
**Solutions:**
1. Check indexes are created (should be from schema)
2. Analyze query with EXPLAIN:
   ```sql
   EXPLAIN ANALYZE SELECT * FROM tasks WHERE status = 'pending';
   ```
3. Add specific indexes if needed:
   ```sql
   CREATE INDEX idx_custom ON table_name(column_name);
   ```

---

## Part 13: Security Best Practices

### 13.1 Key Management
- ✅ Never commit API keys to Git
- ✅ Store keys in n8n credentials (encrypted)
- ✅ Use `service_role` key only in n8n (not client-side)
- ✅ Rotate database password if compromised

### 13.2 Access Control
- ✅ Keep database password secure
- ✅ Don't share `service_role` key
- ✅ Limit user access via `allowed_contexts` array
- ✅ Regularly review connected apps

### 13.3 Data Privacy
- ✅ Email content stored as summaries (not full text)
- ✅ Financial data only in database (not sent to AI APIs)
- ✅ BMF work details kept confidential
- ✅ Regular data cleanup maintains privacy

---

## Next Steps

After completing Supabase setup:
1. ✅ Supabase project created
2. ✅ Database schema deployed
3. ✅ User account added
4. ✅ Business contexts configured
5. ✅ RLS policies set up
6. ✅ Credentials saved securely
7. → Continue to: `05-N8N-CREDENTIALS.md`
8. → Then import n8n workflows

---

## Quick Reference

### Connection Details
```
Project URL: https://abcdefghijklmnop.supabase.co
Database Host: db.abcdefghijklmnop.supabase.co
Database Port: 5432
Database Name: postgres
Database User: postgres
Database Password: [your password]

API Keys:
- anon public: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (for client apps)
- service_role: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (for n8n)
```

### Important Tables
- `business_contexts` - Business definitions
- `users` - System users
- `tasks` - Todo items
- `emails` - Processed emails
- `calendar_events` - Synced events
- `dj_bookings` - DJ pipeline
- `woodys_orders` - Order pipeline
- `bmf_work_log` - Timesheet
- `ai_decisions` - AI audit trail
- `api_usage` - Cost monitoring

---

**Setup Complete!** Your Supabase database is ready for the AI PA system.
