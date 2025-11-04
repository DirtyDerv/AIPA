#!/usr/bin/env python3
"""
n8n MCP Server
Provides n8n workflow management tools for Claude Desktop via Model Context Protocol
"""

import asyncio
import json
import os
import requests
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class N8nMCPServer:
    def __init__(self):
        self.server = Server("n8n-server")
        self.n8n_url = os.getenv('N8N_API_URL', 'http://localhost:5678')
        self.api_key = os.getenv('N8N_API_KEY')
        self._setup_handlers()

    def _get_headers(self):
        """Get authentication headers for n8n API"""
        return {
            'X-N8N-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }

    def _make_request(self, method: str, endpoint: str, data: dict = None) -> dict:
        """Make authenticated request to n8n API"""
        url = f"{self.n8n_url}/rest{endpoint}"
        headers = self._get_headers()

        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                return {'error': f'Unsupported method: {method}'}

            if response.status_code >= 200 and response.status_code < 300:
                return response.json() if response.content else {'success': True}
            else:
                return {
                    'error': f'HTTP {response.status_code}',
                    'message': response.text
                }

        except requests.exceptions.RequestException as e:
            return {'error': f'Request failed: {str(e)}'}

    def _setup_handlers(self):
        """Setup MCP tool handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="list_workflows",
                    description="List all n8n workflows with their status and metadata",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "active_only": {
                                "type": "boolean",
                                "description": "Only show active workflows",
                                "default": False
                            }
                        }
                    }
                ),
                Tool(
                    name="get_workflow",
                    description="Get detailed information about a specific workflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "workflow_id": {
                                "type": "string",
                                "description": "The workflow ID to retrieve"
                            }
                        },
                        "required": ["workflow_id"]
                    }
                ),
                Tool(
                    name="create_workflow",
                    description="Create a new n8n workflow from JSON",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": "Name of the workflow"
                            },
                            "workflow_json": {
                                "type": "string",
                                "description": "JSON string of the workflow definition"
                            },
                            "activate": {
                                "type": "boolean",
                                "description": "Whether to activate the workflow after creation",
                                "default": False
                            }
                        },
                        "required": ["name", "workflow_json"]
                    }
                ),
                Tool(
                    name="update_workflow",
                    description="Update an existing workflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "workflow_id": {
                                "type": "string",
                                "description": "The workflow ID to update"
                            },
                            "workflow_json": {
                                "type": "string",
                                "description": "Updated JSON string of the workflow"
                            },
                            "activate": {
                                "type": "boolean",
                                "description": "Whether to activate after update",
                                "default": False
                            }
                        },
                        "required": ["workflow_id", "workflow_json"]
                    }
                ),
                Tool(
                    name="activate_workflow",
                    description="Activate or deactivate a workflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "workflow_id": {
                                "type": "string",
                                "description": "The workflow ID to activate/deactivate"
                            },
                            "active": {
                                "type": "boolean",
                                "description": "Whether to activate (true) or deactivate (false)",
                                "default": True
                            }
                        },
                        "required": ["workflow_id"]
                    }
                ),
                Tool(
                    name="delete_workflow",
                    description="Delete a workflow",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "workflow_id": {
                                "type": "string",
                                "description": "The workflow ID to delete"
                            }
                        },
                        "required": ["workflow_id"]
                    }
                ),
                Tool(
                    name="test_webhook",
                    description="Test a webhook endpoint",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "webhook_path": {
                                "type": "string",
                                "description": "The webhook path to test (e.g., 'discord-nlp')"
                            },
                            "test_data": {
                                "type": "string",
                                "description": "JSON test data to send",
                                "default": "{}"
                            }
                        },
                        "required": ["webhook_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
            if name == "list_workflows":
                active_only = arguments.get('active_only', False)
                result = self._make_request('GET', '/workflows')

                if 'error' in result:
                    return [TextContent(type="text", text=f"Error listing workflows: {result['error']}")]

                workflows = result.get('data', [])
                if active_only:
                    workflows = [w for w in workflows if w.get('active', False)]

                response = f"Found {len(workflows)} workflow{'s' if len(workflows) != 1 else ''}"
                if active_only:
                    response += " (active only)"
                response += ":\n\n"

                for workflow in workflows:
                    status = "🟢 ACTIVE" if workflow.get('active', False) else "🔴 INACTIVE"
                    response += f"• **{workflow['name']}** (ID: {workflow['id']}) - {status}\n"

                return [TextContent(type="text", text=response)]

            elif name == "get_workflow":
                workflow_id = arguments['workflow_id']
                result = self._make_request('GET', f'/workflows/{workflow_id}')

                if 'error' in result:
                    return [TextContent(type="text", text=f"Error getting workflow: {result['error']}")]

                workflow = result
                response = f"**Workflow: {workflow['name']}**\n"
                response += f"**ID:** {workflow['id']}\n"
                response += f"**Status:** {'🟢 ACTIVE' if workflow.get('active', False) else '🔴 INACTIVE'}\n"
                response += f"**Created:** {workflow.get('createdAt', 'Unknown')}\n"
                response += f"**Updated:** {workflow.get('updatedAt', 'Unknown')}\n"
                response += f"**Nodes:** {len(workflow.get('nodes', []))}\n"
                response += f"**Connections:** {len(workflow.get('connections', []))}\n\n"

                # Show nodes
                if workflow.get('nodes'):
                    response += "**Nodes:**\n"
                    for node in workflow['nodes']:
                        response += f"• {node['type']} ({node['name']})\n"

                return [TextContent(type="text", text=response)]

            elif name == "create_workflow":
                name = arguments['name']
                workflow_json = arguments['workflow_json']
                activate = arguments.get('activate', False)

                try:
                    workflow_data = json.loads(workflow_json)
                    workflow_data['name'] = name

                    result = self._make_request('POST', '/workflows', workflow_data)

                    if 'error' in result:
                        return [TextContent(type="text", text=f"Error creating workflow: {result['error']}")]

                    workflow_id = result.get('id')
                    response = f"✅ **Workflow created successfully!**\n"
                    response += f"**Name:** {name}\n"
                    response += f"**ID:** {workflow_id}\n"

                    if activate:
                        # Activate the workflow
                        activate_result = self._make_request('PUT', f'/workflows/{workflow_id}/activate', {})
                        if 'error' not in activate_result:
                            response += "**Status:** 🟢 ACTIVATED\n"
                        else:
                            response += "**Status:** Created (activation failed)\n"

                    return [TextContent(type="text", text=response)]

                except json.JSONDecodeError as e:
                    return [TextContent(type="text", text=f"Invalid JSON in workflow_json: {str(e)}")]

            elif name == "update_workflow":
                workflow_id = arguments['workflow_id']
                workflow_json = arguments['workflow_json']
                activate = arguments.get('activate', False)

                try:
                    workflow_data = json.loads(workflow_json)

                    result = self._make_request('PUT', f'/workflows/{workflow_id}', workflow_data)

                    if 'error' in result:
                        return [TextContent(type="text", text=f"Error updating workflow: {result['error']}")]

                    response = f"✅ **Workflow updated successfully!**\n"
                    response += f"**ID:** {workflow_id}\n"

                    if activate:
                        activate_result = self._make_request('PUT', f'/workflows/{workflow_id}/activate', {})
                        if 'error' not in activate_result:
                            response += "**Status:** 🟢 ACTIVATED\n"
                        else:
                            response += "**Status:** Updated (activation failed)\n"

                    return [TextContent(type="text", text=response)]

                except json.JSONDecodeError as e:
                    return [TextContent(type="text", text=f"Invalid JSON in workflow_json: {str(e)}")]

            elif name == "activate_workflow":
                workflow_id = arguments['workflow_id']
                active = arguments.get('active', True)

                endpoint = 'activate' if active else 'deactivate'
                result = self._make_request('PUT', f'/workflows/{workflow_id}/{endpoint}', {})

                if 'error' in result:
                    return [TextContent(type="text", text=f"Error {'activating' if active else 'deactivating'} workflow: {result['error']}")]

                status = "🟢 ACTIVATED" if active else "🔴 DEACTIVATED"
                return [TextContent(type="text", text=f"✅ **Workflow {status}**\n**ID:** {workflow_id}")]

            elif name == "delete_workflow":
                workflow_id = arguments['workflow_id']

                result = self._make_request('DELETE', f'/workflows/{workflow_id}')

                if 'error' in result:
                    return [TextContent(type="text", text=f"Error deleting workflow: {result['error']}")]

                return [TextContent(type="text", text=f"✅ **Workflow deleted successfully**\n**ID:** {workflow_id}")]

            elif name == "test_webhook":
                webhook_path = arguments['webhook_path']
                test_data = arguments.get('test_data', '{}')

                try:
                    test_payload = json.loads(test_data)
                except json.JSONDecodeError:
                    return [TextContent(type="text", text="Invalid JSON in test_data")]

                # Test the webhook
                webhook_url = f"{self.n8n_url}/webhook/{webhook_path}"
                headers = {'Content-Type': 'application/json'}

                try:
                    response = requests.post(webhook_url, headers=headers, json=test_payload, timeout=10)

                    result = f"🧪 **Webhook Test Results**\n"
                    result += f"**URL:** {webhook_url}\n"
                    result += f"**Status:** {response.status_code}\n"
                    result += f"**Response:** {response.text[:500]}{'...' if len(response.text) > 500 else ''}\n"

                    if response.status_code >= 200 and response.status_code < 300:
                        result += "✅ **Test PASSED**"
                    else:
                        result += "❌ **Test FAILED**"

                    return [TextContent(type="text", text=result)]

                except requests.exceptions.RequestException as e:
                    return [TextContent(type="text", text=f"❌ **Webhook test failed:** {str(e)}")]

            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    """Main entry point"""
    server = N8nMCPServer()
    async with stdio_server() as (read_stream, write_stream):
        await server.server.run(
            read_stream,
            write_stream,
            server.server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())