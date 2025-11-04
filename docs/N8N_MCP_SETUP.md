# n8n MCP Server Setup for Claude Code

**Date:** November 2, 2025
**Status:** ✅ Configured - Requires Restart

---

## What is n8n-MCP?

The n8n-MCP server is a Model Context Protocol bridge that gives Claude access to:
- **541 n8n node documentation** with full schemas
- **99% property coverage** for all n8n nodes
- **2,646 real-world workflow examples**
- **2,709 workflow templates** with metadata
- **Direct n8n API access** for workflow management

This means Claude can now:
- Help you build n8n workflows with expert knowledge
- Explain any n8n node and its properties
- Suggest workflow patterns based on real examples
- Create, update, and manage workflows via API
- Validate workflow configurations

---

## Configuration Method: npx (Recommended)

**Why npx instead of Docker?**
- ✅ Simpler integration with Claude Code
- ✅ Automatic updates (always latest version)
- ✅ No port conflicts
- ✅ Direct stdio communication (faster)
- ✅ No container management needed

**Previous Docker setup** (running on port 3000) can be stopped:
```bash
docker stop linear-mcp
docker stop serene_lovelace  # n8n-mcp container
```

---

## Configuration File Created

**Location:** `C:\Users\woody\.claude\claude_desktop_config.json`

**Contents:**
```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "npx",
      "args": ["n8n-mcp"],
      "env": {
        "MCP_MODE": "stdio",
        "N8N_API_URL": "http://192.168.0.14:5678",
        "N8N_API_KEY": "eyJhbGci...5o",
        "LOG_LEVEL": "error",
        "DISABLE_CONSOLE_OUTPUT": "true",
        "N8N_MCP_TELEMETRY_DISABLED": "true"
      }
    }
  }
}
```

---

## Environment Variables Explained

| Variable | Value | Purpose |
|----------|-------|---------|
| `MCP_MODE` | `stdio` | **Required** - Enables proper JSON-RPC communication |
| `N8N_API_URL` | `http://192.168.0.14:5678` | Your local n8n server |
| `N8N_API_KEY` | `eyJhbGci...` | Your n8n API key (from CREDENTIALS.md) |
| `LOG_LEVEL` | `error` | Only show errors (keeps output clean) |
| `DISABLE_CONSOLE_OUTPUT` | `true` | Prevent debug logs in Claude |
| `N8N_MCP_TELEMETRY_DISABLED` | `true` | Disable anonymous usage stats |

---

## Next Steps: RESTART REQUIRED

**⚠️ IMPORTANT:** You must restart Claude Code completely for the MCP server to activate.

### How to Restart Claude Code:

1. **Close all Claude Code windows/sessions**
2. **Fully exit the application**
3. **Restart Claude Code**
4. **Wait for initialization** (may take 10-20 seconds on first run)

On first run, npx will download the n8n-mcp package (~few MB).

---

## Verifying the Setup

After restart, you can verify the MCP is working by asking Claude:

```
"What n8n nodes are available for Telegram?"
"Show me examples of email automation workflows"
"Help me build a workflow that triggers on webhook"
```

Claude should now have detailed knowledge of n8n nodes and can help build workflows!

---

## What Claude Can Now Do

### With MCP Active:

1. **Node Documentation**
   - Explain any n8n node in detail
   - Show all properties and options
   - Provide configuration examples

2. **Workflow Building**
   - Suggest nodes for your use case
   - Provide real-world workflow examples
   - Validate workflow structure

3. **Direct API Management** (via your API key)
   - List your workflows
   - Create new workflows
   - Update existing workflows
   - Activate/deactivate workflows
   - Check execution status

4. **Best Practices**
   - Recommend workflow patterns
   - Suggest error handling
   - Optimize workflow structure

---

## Troubleshooting

### If MCP doesn't load after restart:

1. **Check the config file exists:**
   ```bash
   cat "C:\Users\woody\.claude\claude_desktop_config.json"
   ```

2. **Verify Node.js is installed:**
   ```bash
   node --version
   npx --version
   ```

3. **Test npx manually:**
   ```bash
   npx n8n-mcp
   ```
   (Should hang waiting for input - press Ctrl+C to exit)

4. **Check Claude Code logs:**
   - Look in `C:\Users\woody\.claude\debug\` for error logs

### If you get "command not found" errors:

Make sure Node.js is in your PATH and accessible from the terminal.

---

## Updating the MCP Server

Since we're using npx, updates are automatic! npx always fetches the latest version.

To force an update:
```bash
npm cache clean --force
```

Then restart Claude Code.

---

## Alternative: Docker Setup (Not Recommended)

If you prefer Docker instead of npx, use this configuration:

```json
{
  "mcpServers": {
    "n8n-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--init",
        "-e", "MCP_MODE=stdio",
        "-e", "N8N_API_URL=http://host.docker.internal:5678",
        "-e", "N8N_API_KEY=eyJhbGci...5o",
        "-e", "LOG_LEVEL=error",
        "-e", "DISABLE_CONSOLE_OUTPUT=true",
        "-e", "N8N_MCP_TELEMETRY_DISABLED=true",
        "ghcr.io/czlonkowski/n8n-mcp:latest"
      ]
    }
  }
}
```

**Note:** Docker requires `-i` (interactive) and `--init` flags for proper operation.

---

## Resources

- **GitHub:** https://github.com/czlonkowski/n8n-mcp
- **n8n Docs:** https://docs.n8n.io
- **Your n8n Instance:** http://192.168.0.14:5678
- **API Documentation:** See `N8N_API_DOCUMENTATION.md`

---

## Summary

✅ **Configuration created** at `C:\Users\woody\.claude\claude_desktop_config.json`
✅ **Using npx method** (automatic updates, simpler than Docker)
✅ **API credentials configured** (full n8n access)
✅ **Telemetry disabled**

**Action Required:** Restart Claude Code completely to activate the n8n MCP server!

After restart, I'll have expert-level n8n knowledge and can help you build, manage, and optimize your workflows! 🚀
