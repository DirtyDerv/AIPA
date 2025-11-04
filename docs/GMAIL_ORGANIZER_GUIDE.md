# AIPA Advanced Gmail Organization System

## 🎯 Overview
The AIPA Advanced Gmail Organization System is an intelligent email management solution that automatically sorts, protects, and cleans up your Gmail inbox while safeguarding important credentials and receipts.

## ✅ Installation Complete
- **Workflow ID**: `qAobPItoZSgelYHn`
- **Status**: ✅ Active and Ready
- **Schedule**: Daily at 2:00 AM
- **Next Execution**: Automatically every night

## 🛡️ What It Protects (Never Deletes)

### 🔑 Login & Credentials
- Password reset emails
- Two-factor authentication codes
- Login notifications
- Security alerts
- API keys and tokens
- Account verification emails

### 💰 Receipts & Financial
- Purchase receipts
- Invoices and billing
- Payment confirmations
- Bank statements
- Tax documents (W-2, 1099)
- Subscription renewals
- PayPal, Stripe, and payment processor emails

### 🔒 Legal & Important
- Contracts and agreements
- Terms of service updates
- Legal notices
- Copyright and licensing
- Insurance documents
- Compliance notifications

## 🗑️ What It Cleans Up

### Automatic Deletion
- ✅ Emails older than 1 year (with protection checks)
- ✅ Confirmed spam and junk
- ✅ Marketing emails with unsubscribe links
- ✅ Promotional content
- ✅ Newsletter backlog

### Safety Features
- 🔒 **Triple Safety Check**: Multiple layers prevent accidental deletion
- 🔍 **Smart Content Analysis**: AI-powered classification
- 📊 **Detailed Logging**: Complete audit trail
- 🚨 **Emergency Protection**: Critical keyword detection

## 📁 Gmail Labels Created

Your Gmail will automatically get these organized labels:

### 🔑 Login & Credentials
All password-related and authentication emails

### 💰 Receipts & Financial  
All purchase, billing, and financial documents

### 🔒 AIPA Protected
Legal documents and other important items

## 🚀 Required Setup Steps

### 1. Gmail API Authentication
You need to set up Gmail API access in n8n:

1. **Open n8n**: Go to http://192.168.0.14:5678
2. **Navigate to Credentials**
3. **Add Gmail OAuth2 Credential**:
   - Name: `AIPA Gmail Access`
   - Follow OAuth2 setup wizard
   - Grant Gmail access permissions

### 2. Supabase Database Setup
Execute this SQL in your Supabase dashboard:

```sql
CREATE TABLE IF NOT EXISTS email_organization_logs (
    id SERIAL PRIMARY KEY,
    operation_type VARCHAR(50) NOT NULL,
    emails_processed INTEGER DEFAULT 0,
    protected_count INTEGER DEFAULT 0,
    deleted_count INTEGER DEFAULT 0,
    safety_saves INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    details JSONB
);
```

### 3. First Run Test
To test the system before it runs automatically:

1. Open n8n workflow: `AIPA - Advanced Gmail Organization & Cleanup`
2. Click **"Execute Workflow"** 
3. Monitor results in Discord #email-alerts channel

## 📊 Monitoring & Reports

### Discord Notifications
Every cleanup operation sends a report to your Discord #email-alerts channel with:
- 📧 Total emails processed
- 🔒 Number of emails protected
- 🗑️ Number of emails cleaned up
- ✅ Safety saves (emails protected from deletion)

### Database Logs
All operations are logged to Supabase with detailed information for audit purposes.

## ⚙️ Workflow Details

### Daily Schedule
- **Time**: 2:00 AM daily
- **Duration**: ~5-15 minutes (depending on inbox size)
- **Process**: Fully automated

### Processing Steps
1. **Scan**: Retrieve emails older than 1 year and spam
2. **Classify**: AI-powered content analysis
3. **Protect**: Move important emails to protected labels
4. **Safety Check**: Final verification before cleanup
5. **Execute**: Safe deletion of confirmed junk
6. **Report**: Send notifications and log results

## 🔧 Customization Options

### Modify Protection Patterns
To adjust what gets protected, edit the workflow's classification code:

```javascript
// Add your custom protection patterns here
const protectionPatterns = {
  passwords: ['your', 'custom', 'keywords'],
  receipts: ['receipt', 'invoice', 'purchase'],
  // ... add more categories
};
```

### Change Schedule
To modify when the cleanup runs:
1. Open n8n workflow
2. Edit the "Daily Email Cleanup Schedule" node
3. Modify the cron expression (currently: `0 2 * * *`)

### Adjust Age Threshold
To change the 1-year deletion threshold:
1. Edit the "Get Old Emails" node
2. Modify the query from `older_than:1y` to your preference

## 🚨 Emergency Controls

### Pause Cleanup
If you need to stop the automatic cleanup:
1. Go to n8n: http://192.168.0.14:5678
2. Find "AIPA - Advanced Gmail Organization & Cleanup"
3. Click "Deactivate"

### Manual Review
Before any deletion, the system generates detailed logs. You can review these in:
- Discord #email-alerts channel
- Supabase email_organization_logs table

## 📱 Usage Tips

### Best Practices
- 🔍 **Review first run**: Check the initial cleanup results
- 📊 **Monitor reports**: Keep an eye on Discord notifications
- 🔒 **Trust the protection**: The system is designed with multiple safety layers
- 📁 **Use labels**: Organized emails are easier to find

### Finding Protected Emails
Use Gmail's label filters:
- Search: `label:"🔑 Login & Credentials"`
- Search: `label:"💰 Receipts & Financial"`
- Search: `label:"🔒 AIPA Protected"`

## 🆘 Troubleshooting

### Workflow Not Running
1. Check n8n workflow is activated
2. Verify Gmail API credentials
3. Check Discord webhook connectivity

### Emails Not Being Protected
1. Review protection patterns in workflow
2. Check classification logs in Supabase
3. Add custom keywords if needed

### Missing Notifications
1. Verify Discord webhook URLs
2. Check #email-alerts channel permissions
3. Test webhook manually

## 📞 Support

If you need help:
1. Check workflow execution logs in n8n
2. Review Discord #email-alerts for error messages  
3. Check Supabase logs for detailed error information

---

## 🎉 Success!

Your Gmail is now protected by an intelligent organization system that will:
- ✅ Keep your important emails safe
- ✅ Clean up junk and old emails
- ✅ Organize everything with clear labels  
- ✅ Provide detailed reports
- ✅ Run automatically every day

**Sleep peacefully knowing your inbox will be clean and organized every morning!** 🌅