# Google Workspace Setup Guide

## Overview
This guide configures your Gmail, Google Calendar, and Google Drive for multi-business context management. The AI PA will automatically organize everything by business context.

## Prerequisites
- Google account with Gmail access
- Chrome browser recommended (for easier setup)

---

## Part 1: Gmail Labels Setup

Gmail labels will be automatically applied to incoming emails based on AI classification.

### 1.1 Create Main Business Labels

1. Open Gmail (https://gmail.com)
2. In the left sidebar, scroll down and click **"Create new label"**
3. Create these **parent labels**:

```
🏢 WoodysCreations
🎵 DJ-Business
💼 BMF-Work
🍺 Pub-Future
👤 Personal
```

**Label Creation Steps (repeat for each):**
1. Click "Create new label"
2. Enter label name exactly as shown (including emoji if supported)
3. Leave "Nest label under" unchecked
4. Click "Create"
5. Choose a color:
   - WoodysCreations: Green
   - DJ-Business: Red
   - BMF-Work: Orange
   - Pub-Future: Purple
   - Personal: Blue

### 1.2 Create Sub-Labels

For each main label, create nested sub-labels:

**Under 🏢 WoodysCreations:**
```
├── WoodysCreations/Urgent
├── WoodysCreations/Orders
├── WoodysCreations/Suppliers
├── WoodysCreations/Customers
├── WoodysCreations/Processed
└── WoodysCreations/AwaitingReply
```

**Under 🎵 DJ-Business:**
```
├── DJ-Business/Urgent
├── DJ-Business/Bookings
├── DJ-Business/Inquiries
├── DJ-Business/Contracts
├── DJ-Business/Processed
└── DJ-Business/AwaitingReply
```

**Under 💼 BMF-Work:**
```
├── BMF-Work/Urgent
├── BMF-Work/Projects
├── BMF-Work/Timesheets
├── BMF-Work/Processed
└── BMF-Work/AwaitingReply
```

**Under 🍺 Pub-Future:**
```
├── Pub-Future/Urgent
├── Pub-Future/Licensing
├── Pub-Future/Suppliers
├── Pub-Future/Processed
└── Pub-Future/AwaitingReply
```

**Under 👤 Personal:**
```
├── Personal/Urgent
├── Personal/Family
├── Personal/Bills
├── Personal/Processed
└── Personal/AwaitingReply
```

**How to Create Nested Labels:**
1. Click "Create new label"
2. Enter sub-label name (e.g., "Urgent")
3. Check "Nest label under"
4. Select parent label (e.g., "WoodysCreations")
5. Click "Create"

### 1.3 Configure Label Visibility

Make all labels visible in the sidebar:
1. Hover over each label
2. Click the 3 dots that appear
3. Select "Show in message list"

### 1.4 Create Gmail Filters (Optional but Recommended)

Pre-filter known senders automatically:

**Example: Brian Farmer (BMF Work)**
1. Gmail Settings (gear icon) > **See all settings**
2. Go to **Filters and Blocked Addresses** tab
3. Click **Create a new filter**
4. In "From" field: `brian@bmfwork.com` (replace with actual email)
5. Click **Create filter**
6. Check **Apply the label** and select "BMF-Work"
7. Check **Also apply filter to matching conversations**
8. Click **Create filter**

**Repeat for:**
- Known Woody's Creations suppliers
- Etsy order notifications
- Known DJ clients
- Personal contacts

### 1.5 Get Label IDs for n8n

n8n needs Gmail label IDs (not names). To get them:

**Method 1: Using n8n Gmail node**
1. In n8n, add a Gmail node
2. Operation: "Get All Labels"
3. Execute the node
4. Copy the IDs you need

**Method 2: Using Gmail API Explorer**
1. Go to: https://developers.google.com/gmail/api/v1/reference/users/labels/list
2. Click "Try this method"
3. Authorize your Google account
4. Execute
5. Find your labels and copy their IDs

**Save these for later:**
```
WoodysCreations: Label_xxxxx
DJ-Business: Label_xxxxx
BMF-Work: Label_xxxxx
Pub-Future: Label_xxxxx
Personal: Label_xxxxx
```

---

## Part 2: Google Calendar Setup

Create separate calendars for each business context with conflict detection.

### 2.1 Create New Calendars

1. Open Google Calendar (https://calendar.google.com)
2. Left sidebar, next to "Other calendars", click **+**
3. Select **Create new calendar**

**Create these calendars:**

**Calendar 1: Woody's Creations**
- Name: `Woody's Creations`
- Description: `Production schedules, supplier meetings, craft events, order deadlines`
- Time zone: `Europe/London`
- Click **Create calendar**
- After creation, find it in "My calendars"
- Click the 3 dots > **Settings and sharing**
- Under "Access permissions", ensure "Make available to public" is **OFF**
- Choose calendar color: **Green**

**Calendar 2: DJ Business**
- Name: `DJ Business`
- Description: `Event bookings, client meetings, equipment maintenance, gig dates`
- Time zone: `Europe/London`
- Color: **Red**

**Calendar 3: BMF Work**
- Name: `BMF Work`
- Description: `Project schedules, meetings with Brian, work blocks, deadlines`
- Time zone: `Europe/London`
- Color: **Orange**

**Calendar 4: Pub (Future)**
- Name: `Pub Management`
- Description: `Licensing appointments, supplier meetings, staff schedules, pub events`
- Time zone: `Europe/London`
- Color: **Purple**

**Calendar 5: Personal** (Use existing or create new)
- Name: `Personal`
- Description: `Family time, personal appointments, hobbies, health`
- Time zone: `Europe/London`
- Color: **Blue**

### 2.2 Configure Calendar Settings

For **each** calendar:
1. Click the calendar name in sidebar
2. Click 3 dots > **Settings and sharing**
3. Under **Event notifications**, add:
   - **10 minutes before** (Notification)
   - **1 day before** (Email)
4. Under **General notifications**, enable:
   - **Email** for "Events added to this calendar"
   - **Email** for "Changed events"
5. Scroll down to **Integrate calendar**
6. **Copy the Calendar ID** (looks like: `abc123@group.calendar.google.com`)
7. Save this ID - you'll need it for n8n and Supabase

**Save Calendar IDs:**
```
Woody's Creations: woodys_creations@group.calendar.google.com
DJ Business: dj_business@group.calendar.google.com
BMF Work: bmf_work@group.calendar.google.com
Pub Management: pub_management@group.calendar.google.com
Personal: your_email@gmail.com (or personal@group.calendar.google.com)
```

### 2.3 Share Calendar with Angie (Woody's Creations)

1. Open **Woody's Creations** calendar settings
2. Under **Share with specific people**, click **Add people**
3. Enter Angie's Gmail address
4. Set permissions: **Make changes to events**
5. Click **Send**

### 2.4 Update Database with Calendar IDs

After setting up Supabase, update the business_contexts table:
```sql
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

---

## Part 3: Google Drive Folder Structure

Organize files by business context with shared access where needed.

### 3.1 Create Root Folder

1. Open Google Drive (https://drive.google.com)
2. Click **New** > **Folder**
3. Name it: `AI-PA-System`
4. Right-click the folder > **Organize** > **Add star** (for easy access)

### 3.2 Create Business Context Folders

Inside `AI-PA-System`, create these folders:

```
AI-PA-System/
├── 👤 Personal/
│   ├── Documents/
│   ├── Photos/
│   ├── Finance/
│   └── Health/
│
├── 🏢 WoodysCreations/
│   ├── Orders/
│   │   ├── 2025/
│   │   │   ├── January/
│   │   │   ├── February/
│   │   │   └── ...
│   │   └── Templates/
│   ├── Designs/
│   │   ├── Active/
│   │   ├── Archive/
│   │   └── Customer-Submitted/
│   ├── Marketing/
│   │   ├── Social-Media/
│   │   ├── Product-Photos/
│   │   └── Promotional/
│   ├── Finances/
│   │   ├── Invoices/
│   │   ├── Receipts/
│   │   └── Reports/
│   ├── Suppliers/
│   │   ├── Wood-Suppliers/
│   │   ├── Hardware/
│   │   └── Packaging/
│   └── Equipment/
│       └── Laser-Maintenance/
│
├── 🎵 DJ-Business/
│   ├── Bookings/
│   │   ├── 2025/
│   │   │   ├── January/
│   │   │   └── ...
│   │   └── Templates/
│   │       ├── Contract-Template.pdf
│   │       ├── Quote-Template.pdf
│   │       └── Invoice-Template.pdf
│   ├── Music/
│   │   ├── Playlists/
│   │   └── Requests/
│   ├── Marketing/
│   │   ├── Promo-Materials/
│   │   ├── Event-Photos/
│   │   └── Social-Media/
│   ├── Finances/
│   │   ├── Invoices/
│   │   ├── Receipts/
│   │   └── Reports/
│   ├── Clients/
│   │   └── Event-Details/
│   └── Equipment/
│       ├── Inventory/
│       └── Maintenance/
│
├── 💼 BMF-Work/
│   ├── Projects/
│   │   ├── Active/
│   │   ├── Completed/
│   │   └── Archive/
│   ├── Timesheets/
│   │   └── 2025/
│   ├── Documents/
│   │   ├── Contracts/
│   │   └── NDAs/
│   ├── Invoices/
│   └── Notes/
│
├── 🍺 Pub-Future/
│   ├── Planning/
│   │   ├── Business-Plan/
│   │   ├── Budget/
│   │   └── Research/
│   ├── Licenses/
│   │   ├── Applications/
│   │   └── Approved/
│   ├── Marketing/
│   │   ├── Logo/
│   │   ├── Menu/
│   │   └── Social-Media/
│   ├── Suppliers/
│   │   ├── Brewery/
│   │   ├── Food/
│   │   └── Equipment/
│   ├── Property/
│   │   ├── Lease/
│   │   └── Renovations/
│   └── Staff/
│
└── 📁 Shared-Resources/
    ├── Templates/
    ├── Brand-Assets/
    └── Reference-Documents/
```

**Folder Creation Tips:**
- Right-click > **New folder** to create each
- Use emojis in folder names for easy identification
- Color-code folders (right-click > **Change color**)

### 3.3 Set Folder Permissions

**Woody's Creations - Share with Angie:**
1. Right-click `🏢 WoodysCreations` folder
2. Click **Share**
3. Enter Angie's Gmail address
4. Set access: **Editor** (can edit/delete files)
5. Uncheck "Notify people"
6. Click **Share**

**BMF Work - Keep Private:**
- Don't share this folder (contains Brian's confidential work)

**All Others:**
- Keep private unless specific sharing is needed

### 3.4 Get Folder IDs for Database

Each folder has a unique ID in its URL:
```
https://drive.google.com/drive/folders/FOLDER_ID_HERE
```

**To get Folder ID:**
1. Open the folder in Google Drive
2. Look at the URL in your browser
3. Copy the ID after `/folders/`
4. Save it for database update

Example:
```
https://drive.google.com/drive/folders/1a2B3c4D5e6F7g8H9i0J
                                          ^^^^^^^^^^^^^^^^^^^^
                                          This is the Folder ID
```

**Save Folder IDs:**
```
AI-PA-System root: 1a2B3c4D5e6F7g8H9i0J
Personal: 2b3C4d5E6f7G8h9I0j1K
WoodysCreations: 3c4D5e6F7g8H9i0J1k2L
DJ-Business: 4d5E6f7G8h9I0j1K2l3M
BMF-Work: 5e6F7g8H9i0J1k2L3m4N
Pub-Future: 6f7G8h9I0j1K2l3M4n5O
Shared-Resources: 7g8H9i0J1k2L3m4N5o6P
```

### 3.5 Update Database with Folder IDs

```sql
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

---

## Part 4: Google OAuth for n8n

n8n needs OAuth access to interact with Gmail, Calendar, and Drive.

### 4.1 Create Google Cloud Project

1. Go to Google Cloud Console: https://console.cloud.google.com
2. Click **Select a project** (top bar)
3. Click **NEW PROJECT**
4. Project name: `AIPA-System`
5. Click **CREATE**
6. Wait for project to be created
7. Select the new project from the dropdown

### 4.2 Enable Required APIs

1. In Cloud Console, go to **APIs & Services** > **Library**
2. Search and enable these APIs (click each, then click **ENABLE**):
   - **Gmail API**
   - **Google Calendar API**
   - **Google Drive API**
   - **Google Sheets API** (optional, for future reports)

### 4.3 Configure OAuth Consent Screen

1. Go to **APIs & Services** > **OAuth consent screen**
2. Choose **External** (since it's just your personal account)
3. Click **CREATE**
4. Fill out:
   - **App name**: `AIPA System`
   - **User support email**: Your Gmail address
   - **Developer contact**: Your Gmail address
5. Click **SAVE AND CONTINUE**
6. Scopes: Click **ADD OR REMOVE SCOPES**
   - Select: `Gmail` (all scopes)
   - Select: `Google Calendar` (all scopes)
   - Select: `Google Drive` (all scopes)
7. Click **UPDATE** then **SAVE AND CONTINUE**
8. Test users: Click **ADD USERS**
   - Add your Gmail address
   - Add Angie's Gmail (if she'll use it)
9. Click **SAVE AND CONTINUE**
10. Click **BACK TO DASHBOARD**

### 4.4 Create OAuth Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **CREATE CREDENTIALS** > **OAuth client ID**
3. Application type: **Web application**
4. Name: `n8n AIPA`
5. Under **Authorized redirect URIs**, click **ADD URI**
6. Add: `https://uniterative-futile-charmain.ngrok-free.dev/rest/oauth2-credential/callback`
7. Click **CREATE**
8. Copy **Client ID** and **Client Secret** - you'll need these for n8n

**Save these securely:**
```
Client ID: 123456789-abcdefgh.apps.googleusercontent.com
Client Secret: GOCSPX-AbCdEfGhIjKlMnOpQrStUvWxYz
```

---

## Part 5: Test Google Workspace Integration

### 5.1 Send Test Email with Labels

1. Send yourself an email
2. Subject: `Test WoodysCreations Order`
3. In n8n (once configured), trigger email processing
4. Check if email gets labeled correctly

### 5.2 Create Test Calendar Event

1. In Google Calendar, create event in "Woody's Creations" calendar
2. Title: `Test Production Schedule`
3. Set for tomorrow at 10 AM
4. Check if n8n can read this event

### 5.3 Upload Test File to Drive

1. Upload a file to `WoodysCreations/Orders` folder
2. Check if n8n can access and read it

---

## Part 6: Mobile Access (Optional but Recommended)

### 6.1 Gmail App
- Install Gmail app on mobile
- Labels will sync automatically
- Swipe to apply labels manually

### 6.2 Google Calendar App
- Install Google Calendar app
- All 5 calendars will appear with colors
- Toggle visibility as needed

### 6.3 Google Drive App
- Install Google Drive app
- Star the `AI-PA-System` folder for quick access
- Enable offline access for important folders

---

## Maintenance & Best Practices

### Regular Tasks
- **Weekly**: Review and archive old emails
- **Monthly**: Clean up Drive folders
- **Quarterly**: Review calendar past events

### Naming Conventions
**Emails:**
- Use consistent subject lines for orders: `Order #WC20251101-0001`
- Use consistent subject lines for bookings: `DJ Booking: [Event Type] - [Date]`

**Files:**
- Orders: `WC20251101-0001_CustomerName_ProductDescription.pdf`
- Designs: `Design_ProductName_v1.svg`
- Invoices: `Invoice_WC20251101-0001.pdf`

**Calendar Events:**
- Woody's: `[ORDER] WC20251101-0001 - Production`
- DJ: `[GIG] Client Name - Venue`
- BMF: `[PROJECT] Project Name - Task`

---

## Troubleshooting

### Labels not appearing in Gmail
1. Check label visibility settings
2. Refresh Gmail (F5)
3. Clear browser cache

### Calendar events not syncing
1. Check time zone consistency
2. Verify calendar sharing settings
3. Re-sync calendar in mobile apps

### Drive folders not accessible
1. Check sharing permissions
2. Verify folder isn't in Trash
3. Check if you're signed into correct Google account

### n8n can't access Google services
1. Re-authenticate OAuth in n8n credentials
2. Check API quotas in Google Cloud Console
3. Verify all required APIs are enabled
4. Check redirect URI matches exactly (including https/http)

---

## Security Checklist

- ✅ All business calendars are PRIVATE (not public)
- ✅ BMF Work folder NOT shared with anyone
- ✅ OAuth client secret stored securely in n8n
- ✅ Two-factor authentication enabled on Google account
- ✅ Regular review of connected apps: https://myaccount.google.com/permissions
- ✅ Periodic password changes
- ✅ Security checkup: https://myaccount.google.com/security-checkup

---

## Next Steps

After completing Google Workspace setup:
1. ✅ Gmail labels created and configured
2. ✅ Google Calendar business calendars created
3. ✅ Google Drive folder structure built
4. ✅ OAuth credentials generated
5. ✅ Calendar IDs and Folder IDs saved
6. → Continue to: `04-SUPABASE-SETUP.md`
7. → Then: `05-N8N-CREDENTIALS.md`

---

## Quick Reference

### Label Names (for n8n)
```
WoodysCreations
DJ-Business
BMF-Work
Pub-Future
Personal
```

### Calendar IDs (save after creation)
```
woodys_creations@group.calendar.google.com
dj_business@group.calendar.google.com
bmf_work@group.calendar.google.com
pub_management@group.calendar.google.com
your_email@gmail.com
```

### OAuth Credentials
```
Client ID: [saved in password manager]
Client Secret: [saved in password manager]
Redirect URI: https://uniterative-futile-charmain.ngrok-free.dev/rest/oauth2-credential/callback
```

---

**Setup Complete!** Your Google Workspace is now organized for multi-business AI PA management.
