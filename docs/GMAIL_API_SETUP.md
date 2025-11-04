# Gmail API Setup for AIPA Organizer

## 🔑 Required: Gmail API Authentication

Your Gmail organizer workflow needs Gmail API access to read and organize your emails. Here's how to set it up:

## Step 1: Enable Gmail API in Google Cloud

### 1.1 Go to Google Cloud Console
1. Visit: https://console.cloud.google.com/
2. Create a new project or select existing one
3. Name: "AIPA Gmail Access" (or similar)

### 1.2 Enable Gmail API
1. Go to **APIs & Services** > **Library**
2. Search for "Gmail API"
3. Click **Gmail API** → **Enable**

### 1.3 Create OAuth2 Credentials
1. Go to **APIs & Services** > **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Application type: **Web application**
4. Name: **AIPA n8n Gmail Access**
5. **Authorized redirect URIs**: Add these:
   ```
   http://192.168.0.14:5678/rest/oauth2-credential/callback
   http://localhost:5678/rest/oauth2-credential/callback
   ```
6. Click **Create**
7. **Save the Client ID and Client Secret** - you'll need these!

## Step 2: Configure n8n Gmail Credential

### 2.1 Open n8n
1. Go to: http://192.168.0.14:5678
2. Click **Credentials** in left sidebar
3. Click **+ Add Credential**

### 2.2 Create Gmail OAuth2 Credential
1. Search for and select **Gmail OAuth2 API**
2. Fill in the form:
   - **Credential Name**: `AIPA Gmail Access`
   - **Client ID**: [Your Google Client ID]
   - **Client Secret**: [Your Google Client Secret]
3. Click **Connect my account**
4. **Authorize AIPA** in the Google popup
5. **Grant all Gmail permissions** (read, modify, labels)
6. Click **Save**

### 2.3 Test the Connection
1. The credential should show **✅ Connected**
2. If it shows an error, double-check your Client ID/Secret

## Step 3: Update Workflow (if needed)

The Gmail organizer workflow should automatically use your Gmail credential. If you need to manually assign it:

1. Open workflow: **AIPA - Advanced Gmail Organization & Cleanup**
2. Click each Gmail node (there are several)
3. In **Credential to connect with** dropdown, select: **AIPA Gmail Access**
4. Save the workflow

## 🔒 Security Notes

### What Permissions Are Needed
The AIPA Gmail organizer needs these permissions:
- ✅ **Read emails**: To analyze content and age
- ✅ **Modify emails**: To add labels and delete spam
- ✅ **Manage labels**: To create organization folders
- ✅ **Delete emails**: To remove confirmed spam/old emails

### Data Protection
- 🔒 **Your emails stay in Gmail** - n8n only processes them
- 🛡️ **Multiple safety checks** prevent accidental deletion
- 📊 **Audit logs** track all actions
- 🚫 **No email content is stored** - only metadata

## 🧪 Testing Your Setup

Once you've completed the credential setup:

1. **Test the credential** in n8n by clicking the test button
2. **Run the manual test**:
   ```powershell
   python test_gmail_organizer.py
   ```
3. **Check Discord** for notification in #email-alerts
4. **Verify Gmail labels** were created in your Gmail

## 📞 Troubleshooting

### "Invalid Credentials" Error
- Double-check Client ID and Client Secret
- Ensure Gmail API is enabled in Google Cloud
- Try creating new OAuth credentials

### "Insufficient Permissions" Error
- Re-authorize the credential in n8n
- Make sure you granted all requested permissions
- Check that redirect URIs are correct

### "Rate Limit Exceeded" Error
- The organizer respects Gmail's API limits
- Large inboxes may take longer to process
- This is normal and will complete eventually

### "Webhook Registration Failed" Error
- This is a known n8n issue, but doesn't affect functionality
- The workflow will still work perfectly
- Focus on Gmail API access instead

## ✅ Success Checklist

Before your first automatic run:
- [ ] Gmail API enabled in Google Cloud
- [ ] OAuth2 credentials created with correct redirect URIs
- [ ] n8n credential created and connected
- [ ] All Gmail nodes in workflow use the credential
- [ ] Manual test completed successfully
- [ ] Discord notifications working
- [ ] Gmail labels created in your account

---

## 🎉 You're Ready!

Once this setup is complete, your Gmail will be automatically organized every night at 2:00 AM with:
- 🔒 **Smart protection** for important emails
- 🗑️ **Safe cleanup** of spam and old emails  
- 📁 **Automatic labeling** and organization
- 📱 **Discord notifications** with daily reports

**Sleep peacefully knowing your inbox will be clean every morning!** 🌅