#!/usr/bin/env python3
"""
Gmail MCP Server
Provides Gmail access tools for Claude Desktop via Model Context Protocol
"""

import asyncio
import json
import os
from typing import Any, Sequence
from datetime import datetime, timedelta

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Google API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for Gmail access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/gmail.labels',
    'https://www.googleapis.com/auth/gmail.send'
]

class GmailMCPServer:
    def __init__(self):
        self.server = Server("gmail-server")
        self.gmail_service = None
        self._setup_handlers()

    def _get_gmail_service(self):
        """Get authenticated Gmail service"""
        if self.gmail_service:
            return self.gmail_service

        creds = None
        token_path = os.path.expanduser('~/.aipa/gmail_token.json')
        creds_path = os.path.expanduser('~/.aipa/gmail_credentials.json')

        # Load existing token
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        # If no valid creds, login
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
                creds = flow.run_local_server(port=0)

            # Save token
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        self.gmail_service = build('gmail', 'v1', credentials=creds)
        return self.gmail_service

    def _setup_handlers(self):
        """Setup MCP tool handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="search_emails",
                    description="Search Gmail for emails matching query. Returns list of emails with id, subject, from, date, snippet.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Gmail search query (e.g., 'from:someone@example.com subject:order is:unread')"
                            },
                            "max_results": {
                                "type": "number",
                                "description": "Maximum number of emails to return (default: 10)",
                                "default": 10
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_email",
                    description="Get full content of a specific email by ID",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            }
                        },
                        "required": ["email_id"]
                    }
                ),
                Tool(
                    name="send_email",
                    description="Send an email",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient email address"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject"
                            },
                            "body": {
                                "type": "string",
                                "description": "Email body (plain text)"
                            },
                            "cc": {
                                "type": "string",
                                "description": "CC recipients (comma-separated)"
                            }
                        },
                        "required": ["to", "subject", "body"]
                    }
                ),
                Tool(
                    name="apply_label",
                    description="Apply a label to an email",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email_id": {
                                "type": "string",
                                "description": "Gmail message ID"
                            },
                            "label_name": {
                                "type": "string",
                                "description": "Label name (e.g., 'WoodysCreations', 'DJ-Business')"
                            }
                        },
                        "required": ["email_id", "label_name"]
                    }
                ),
                Tool(
                    name="create_draft",
                    description="Create a draft email for review before sending",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "to": {
                                "type": "string",
                                "description": "Recipient email address"
                            },
                            "subject": {
                                "type": "string",
                                "description": "Email subject"
                            },
                            "body": {
                                "type": "string",
                                "description": "Email body"
                            }
                        },
                        "required": ["to", "subject", "body"]
                    }
                ),
                Tool(
                    name="mark_as_read",
                    description="Mark email(s) as read",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "email_ids": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of Gmail message IDs to mark as read"
                            }
                        },
                        "required": ["email_ids"]
                    }
                ),
                Tool(
                    name="get_unread_count",
                    description="Get count of unread emails, optionally filtered by label/query",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Optional Gmail search query",
                                "default": "is:unread"
                            }
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
            """Handle tool calls"""

            service = self._get_gmail_service()

            try:
                if name == "search_emails":
                    query = arguments.get("query", "")
                    max_results = arguments.get("max_results", 10)

                    results = service.users().messages().list(
                        userId='me',
                        q=query,
                        maxResults=max_results
                    ).execute()

                    messages = results.get('messages', [])

                    email_list = []
                    for msg in messages:
                        # Get full message
                        full_msg = service.users().messages().get(
                            userId='me',
                            id=msg['id'],
                            format='metadata',
                            metadataHeaders=['From', 'Subject', 'Date']
                        ).execute()

                        headers = {h['name']: h['value'] for h in full_msg['payload']['headers']}

                        email_list.append({
                            'id': msg['id'],
                            'threadId': msg['threadId'],
                            'from': headers.get('From', ''),
                            'subject': headers.get('Subject', ''),
                            'date': headers.get('Date', ''),
                            'snippet': full_msg.get('snippet', '')
                        })

                    return [TextContent(
                        type="text",
                        text=json.dumps(email_list, indent=2)
                    )]

                elif name == "get_email":
                    email_id = arguments["email_id"]

                    message = service.users().messages().get(
                        userId='me',
                        id=email_id,
                        format='full'
                    ).execute()

                    # Extract headers
                    headers = {h['name']: h['value'] for h in message['payload']['headers']}

                    # Extract body
                    body = ""
                    if 'parts' in message['payload']:
                        for part in message['payload']['parts']:
                            if part['mimeType'] == 'text/plain':
                                import base64
                                body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                                break
                    elif 'body' in message['payload'] and 'data' in message['payload']['body']:
                        import base64
                        body = base64.urlsafe_b64decode(message['payload']['body']['data']).decode('utf-8')

                    email_data = {
                        'id': email_id,
                        'threadId': message['threadId'],
                        'from': headers.get('From', ''),
                        'to': headers.get('To', ''),
                        'subject': headers.get('Subject', ''),
                        'date': headers.get('Date', ''),
                        'body': body
                    }

                    return [TextContent(
                        type="text",
                        text=json.dumps(email_data, indent=2)
                    )]

                elif name == "send_email":
                    import base64
                    from email.mime.text import MIMEText

                    message = MIMEText(arguments["body"])
                    message['to'] = arguments["to"]
                    message['subject'] = arguments["subject"]
                    if arguments.get("cc"):
                        message['cc'] = arguments["cc"]

                    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

                    sent_message = service.users().messages().send(
                        userId='me',
                        body={'raw': raw}
                    ).execute()

                    return [TextContent(
                        type="text",
                        text=f"Email sent successfully. Message ID: {sent_message['id']}"
                    )]

                elif name == "apply_label":
                    email_id = arguments["email_id"]
                    label_name = arguments["label_name"]

                    # Get label ID
                    labels = service.users().labels().list(userId='me').execute()
                    label_id = None
                    for label in labels.get('labels', []):
                        if label['name'] == label_name:
                            label_id = label['id']
                            break

                    if not label_id:
                        return [TextContent(
                            type="text",
                            text=f"Error: Label '{label_name}' not found"
                        )]

                    service.users().messages().modify(
                        userId='me',
                        id=email_id,
                        body={'addLabelIds': [label_id]}
                    ).execute()

                    return [TextContent(
                        type="text",
                        text=f"Label '{label_name}' applied to email {email_id}"
                    )]

                elif name == "create_draft":
                    import base64
                    from email.mime.text import MIMEText

                    message = MIMEText(arguments["body"])
                    message['to'] = arguments["to"]
                    message['subject'] = arguments["subject"]

                    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

                    draft = service.users().drafts().create(
                        userId='me',
                        body={'message': {'raw': raw}}
                    ).execute()

                    return [TextContent(
                        type="text",
                        text=f"Draft created successfully. Draft ID: {draft['id']}"
                    )]

                elif name == "mark_as_read":
                    email_ids = arguments["email_ids"]

                    for email_id in email_ids:
                        service.users().messages().modify(
                            userId='me',
                            id=email_id,
                            body={'removeLabelIds': ['UNREAD']}
                        ).execute()

                    return [TextContent(
                        type="text",
                        text=f"Marked {len(email_ids)} email(s) as read"
                    )]

                elif name == "get_unread_count":
                    query = arguments.get("query", "is:unread")

                    results = service.users().messages().list(
                        userId='me',
                        q=query
                    ).execute()

                    count = results.get('resultSizeEstimate', 0)

                    return [TextContent(
                        type="text",
                        text=f"Unread count: {count}"
                    )]

                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]

            except HttpError as error:
                return [TextContent(
                    type="text",
                    text=f"Gmail API error: {error}"
                )]
            except Exception as e:
                return [TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )]

    async def run(self):
        """Run the MCP server"""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


def main():
    """Main entry point"""
    server = GmailMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
