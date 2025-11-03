# Configuration Files

## Files
- `requirements.txt` - Python dependencies
- `CREDENTIALS.md` - All system credentials (create manually)
- `credential_ids.json` - n8n credential mappings

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Create `CREDENTIALS.md` with your actual credentials
3. Configure n8n credentials using the credential IDs

## Security
⚠️ Never commit actual credentials to git
✅ Use placeholder values in uploaded files
🔒 Store real credentials in local `CREDENTIALS.md`