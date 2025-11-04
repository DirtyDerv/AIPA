# Workflow Errors Report

Generated: 2025-11-02

## Summary

**Active Workflows**: 4/8
**Total Executions**: 34
**Failed Executions**: 32 (94% error rate)
**Successful Executions**: 2

## Errors by Workflow

### 1. AIPA - Telegram Main Interface (DRuQZOp9tM79Sf6D) - ACTIVE
**Status**: Has errors
**Error**: Missing node to start execution
**Node**: Trigger Reports Workflow
**Issue**: The workflow being called doesn't have an Execute Workflow Trigger node
**Fix Required**: Add Execute Workflow Trigger node to the target workflow

### 2. AIPA - Multi-Business Calendar Management (JG4cI6JJErOgPenc) - ACTIVE
**Status**: Has errors
**Error**: Could not get parameter
**Node**: Check for Conflicts
**Issue**: Missing or incorrectly configured parameter
**Fix Required**: Review node configuration and fix parameter references

### 3. AIPA - Email Processing with AI (dsYFoJPM2wUqZaK3) - ACTIVE
**Status**: Has errors
**Error**: Unknown (need to check)
**Fix Required**: Investigate execution errors

### 4. AIPA - Business Intelligence & Reports (l4fNYmAfBcN2t4YQ) - ACTIVE
**Status**: No recent executions found
**Fix Required**: Test workflow

### 5. AIPA - Woody's Creations Order Processing (dXRNts8WNKGOaXRW) - INACTIVE
**Status**: Cannot activate (rate limited)
**Fix Required**: Wait and retry activation, check for configuration issues

### 6. AIPA - Marketing Campaign Automation (e5sxJhHN1p8I4aUX) - INACTIVE
**Status**: Cannot activate (rate limited)
**Fix Required**: Wait and retry activation, check for configuration issues

### 7. AIPA - DJ Booking Automation (s0dI6JlJ1iNRMxSu) - INACTIVE
**Status**: Cannot activate (rate limited)
**Fix Required**: Wait and retry activation, check for configuration issues

### 8. AIPA - BMF Work Logging (udPdDxTRVWWWP67Tx) - INACTIVE
**Status**: Has errors (when was active)
**Error**: Could not get parameter
**Node**: Save Hours to Database
**Issue**: Missing or incorrectly configured parameter
**Fix Required**: Review node configuration and fix parameter references

## Next Steps

1. Fix "Could not get parameter" errors in Calendar Management and BMF Work Logging
2. Fix "Missing node to start execution" in Telegram Main Interface
3. Investigate Email Processing errors
4. Wait for rate limit to reset and activate remaining workflows
5. Test all workflows after fixes
