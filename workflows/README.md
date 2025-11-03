# AIPA Project Workflows

## n8n Workflow Files

This directory contains backup copies of the n8n workflows that power the AIPA system.

### Core Workflows
- Gmail Organization & Cleanup (Daily at 2 AM)
- Discord Voice Processing (Gemini AI)
- BMF Work Logging
- Discord Message Processing
- Business Intelligence & Reports
- Calendar Management
- Email Processing with AI

### Usage
1. Import workflows into n8n server (192.168.0.14:5678)
2. Configure credentials for each workflow
3. Activate workflows after testing

### Active Workflows Status
- **Total Active**: 20 workflows
- **Total Inactive**: 0 (cleaned up)
- **Key Workflow IDs**:
  - Gmail Organizer: `wnvzXLgk0W75yC4j`
  - Discord Voice: `YXFT5s6U3HD5qarc`
  - BMF Logging: Multiple implementations

### Backup
Workflow files should be exported regularly for backup purposes.
All sensitive credentials are stored separately in n8n credential store.