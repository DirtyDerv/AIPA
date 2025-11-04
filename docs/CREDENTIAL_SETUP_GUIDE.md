# Credential Setup Guide for n8n Workflows

## ✅ All 8 Workflows Successfully Re-Uploaded!

Now you need to configure the credentials before activating them.

---

## 🔑 Required Credentials

You need to set up **4 types of credentials** in n8n:

### 1. **Telegram Bot API** ⭐ (MOST IMPORTANT - Used by ALL workflows)
### 2. **Supabase API** ⭐ (Used by ALL workflows)
### 3. **Gmail OAuth2** (Used by 2 workflows)
### 4. **Google Calendar OAuth2** (Used by 1 workflow)

---

## 📋 Step-by-Step Setup

### Step 1: Open n8n Settings

1. Go to: **http://192.168.0.14:5678**
2. Click **Settings** (gear icon) in the left sidebar
3. Click **Credentials**

---

### Step 2: Add Telegram Bot API ⭐⭐⭐

**This is CRITICAL - all workflows need this!**

1. Click **"Add Credential"**
2. Search for **"Telegram"**
3. Select **"Telegram API"**
4. Enter your **Bot Token** (from BotFather)
   - Format looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`
5. Click **"Save"**

**How to get Telegram Bot Token:**
- If you already have a bot: Message @BotFather on Telegram → `/mybots` → Select your bot → API Token
- If you need a new bot: Message @BotFather → `/newbot` → Follow instructions → Copy the token

---

### Step 3: Add Supabase API ⭐⭐⭐

**Required for database operations in all workflows**

1. Click **"Add Credential"**
2. Search for **"Supabase"**
3. Select **"Supabase API"**
4. Enter:
   - **Host**: Your Supabase project URL (e.g., `https://xxxxx.supabase.co`)
   - **Service Role Secret**: Your Supabase service_role key
5. Click **"Save"**

**Where to find Supabase credentials:**
- Go to your Supabase project dashboard
- Click **Settings** → **API**
- Copy **Project URL** and **service_role key**

---

### Step 4: Add Gmail OAuth2 (Optional but recommended)

**Used by Email Processing and Woody's Order workflows**

1. Click **"Add Credential"**
2. Search for **"Gmail"**
3. Select **"Gmail OAuth2 API"**
4. Click **"Connect my account"**
5. Sign in with your Google account
6. Grant permissions
7. Click **"Save"**

**Note:** You may need to set up a Google Cloud Project first:
- Go to Google Cloud Console
- Enable Gmail API
- Create OAuth2 credentials
- Add your email to test users (if in development mode)

---

### Step 5: Add Google Calendar OAuth2 (Optional)

**Only needed for Calendar Management workflow**

1. Click **"Add Credential"**
2. Search for **"Google Calendar"**
3. Select **"Google Calendar OAuth2 API"**
4. Click **"Connect my account"**
5. Sign in with your Google account
6. Grant permissions
7. Click **"Save"**

---

## 🗄️ Database Setup Required

Your workflows expect these Supabase tables to exist:

### Create these tables in Supabase:

**1. emails table**
```sql
CREATE TABLE emails (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email_id TEXT UNIQUE,
  thread_id TEXT,
  sender TEXT,
  recipient TEXT,
  subject TEXT,
  received_at TIMESTAMP,
  business_context TEXT,
  category TEXT,
  priority TEXT,
  sentiment TEXT,
  requires_response BOOLEAN,
  ai_summary TEXT,
  suggested_action TEXT,
  processed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**2. woodys_orders table**
```sql
CREATE TABLE woodys_orders (
  id SERIAL PRIMARY KEY,
  customer_name TEXT,
  customer_email TEXT,
  customer_phone TEXT,
  product_type TEXT,
  description TEXT,
  custom_text TEXT,
  material TEXT,
  size TEXT,
  price DECIMAL,
  deadline DATE,
  status TEXT,
  order_date DATE,
  production_started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**3. dj_bookings table**
```sql
CREATE TABLE dj_bookings (
  id SERIAL PRIMARY KEY,
  client_name TEXT,
  client_email TEXT,
  client_phone TEXT,
  event_type TEXT,
  event_date DATE,
  event_time TIME,
  venue TEXT,
  duration_hours INTEGER,
  price DECIMAL,
  deposit_paid BOOLEAN DEFAULT FALSE,
  status TEXT,
  special_requests TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**4. bmf_work_logs table**
```sql
CREATE TABLE bmf_work_logs (
  id SERIAL PRIMARY KEY,
  log_date DATE,
  start_time TIME,
  end_time TIME,
  hours_worked DECIMAL,
  task_description TEXT,
  project TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**5. calendar_events table**
```sql
CREATE TABLE calendar_events (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  business_context TEXT,
  event_title TEXT,
  event_date DATE,
  event_time TIME,
  duration_minutes INTEGER,
  description TEXT,
  google_event_id TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📧 Gmail Labels Setup (for Email Processing workflow)

If you're using the Email Processing workflow, create these Gmail labels:

1. Open Gmail
2. Click **Settings** (gear icon) → **See all settings**
3. Go to **Labels** tab
4. Create new labels:
   - `Label_Woodys`
   - `Label_DJ`
   - `Label_BMF`
   - `Label_Pub`

---

## ✅ After Setting Up Credentials

### Workflow Activation Order (recommended):

1. **AIPA - Telegram Main Interface** (ID: DRuQZOp9tM79Sf6D)
   - Start with this - it's your command center

2. **AIPA - Business Intelligence & Reports** (ID: l4fNYmAfBcN2t4YQ)
   - Simple workflow to test database connectivity

3. **AIPA - BMF Work Logging** (ID: udPdDxTRVWWP67Tx)
   - Test work logging functionality

4. **AIPA - Woody's Creations Order Processing** (ID: dXRNts8WNKGOaXRW)
   - After Gmail is configured

5. **AIPA - DJ Booking Automation** (ID: s0dI6JlJ1iNRMxSu)
   - Test booking system

6. **AIPA - Multi-Business Calendar Management** (ID: JG4cI6JJErOgPenc)
   - After Google Calendar OAuth

7. **AIPA - Email Processing with AI** (ID: dsYFoJPM2wUqZaK3)
   - After Gmail OAuth + labels created
   - ⚠️ This will start processing emails automatically!

8. **AIPA - Marketing Campaign Automation** (ID: e5sxJhHN1p8I4aUX)
   - Last one to activate

---

## 🧪 Testing

After setting up credentials and activating "Telegram Main Interface":

1. Open Telegram
2. Find your bot
3. Send: **`/start`**
4. You should get a welcome menu with all commands!

**Available commands:**
- `/start` - Main menu
- `/woodys` - Woody's Creations orders
- `/dj` - DJ booking management
- `/bmf` - BMF work logging
- `/calendar` - Calendar management
- `/reports` - Business intelligence
- `/marketing` - Marketing campaigns

---

## 🆘 Troubleshooting

### "Missing credentials" error when activating
- Make sure you created the credential with the exact name the workflow expects
- Open the workflow → Click on the red node → Select your credential from dropdown

### Telegram webhook HTTPS error
- Make sure WEBHOOK_URL environment variable is set
- Container should have: `--env=WEBHOOK_URL=https://uniterative-futile-charmain.ngrok-free.dev`

### Database errors
- Make sure all tables are created in Supabase
- Verify Supabase credentials are correct
- Check service_role key has proper permissions

---

## 📊 Quick Checklist

- [ ] Telegram Bot API credential added
- [ ] Supabase API credential added
- [ ] Gmail OAuth2 credential added (optional)
- [ ] Google Calendar OAuth2 credential added (optional)
- [ ] All 5 Supabase tables created
- [ ] Gmail labels created (if using email workflow)
- [ ] Telegram Main Interface workflow activated
- [ ] Tested `/start` command in Telegram
- [ ] Other workflows activated as needed

---

**Once you've set up the credentials, activate the workflows and let me know if you need help testing them!**
