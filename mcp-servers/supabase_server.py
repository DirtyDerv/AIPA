#!/usr/bin/env python3
"""
Supabase MCP Server
Provides database access tools for Claude Desktop via Model Context Protocol
"""

import asyncio
import json
import os
from typing import Any, Sequence

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Database imports
import psycopg2
from psycopg2.extras import RealDictCursor
import psycopg2.pool


class SupabaseMCPServer:
    def __init__(self):
        self.server = Server("supabase-server")
        self.db_pool = None
        self._setup_handlers()

    def _get_db_connection(self):
        """Get database connection from pool"""
        if not self.db_pool:
            # Load from environment or config
            db_config = {
                'host': os.getenv('SUPABASE_HOST'),
                'port': os.getenv('SUPABASE_PORT', 5432),
                'database': os.getenv('SUPABASE_DB', 'postgres'),
                'user': os.getenv('SUPABASE_USER', 'postgres'),
                'password': os.getenv('SUPABASE_PASSWORD'),
                'sslmode': 'require'
            }

            self.db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, **db_config)

        return self.db_pool.getconn()

    def _setup_handlers(self):
        """Setup MCP tool handlers"""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="query_database",
                    description="Execute a SELECT query on the database. Returns results as JSON array.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "SQL SELECT query to execute"
                            },
                            "params": {
                                "type": "array",
                                "description": "Optional query parameters for prepared statement",
                                "items": {"type": ["string", "number", "boolean", "null"]}
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="get_tasks",
                    description="Get tasks filtered by status, business context, or priority",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_context": {
                                "type": "string",
                                "description": "Filter by business context name"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed", "cancelled"],
                                "description": "Filter by task status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["urgent", "high", "medium", "low"],
                                "description": "Filter by priority"
                            },
                            "limit": {
                                "type": "number",
                                "default": 20,
                                "description": "Maximum number of tasks to return"
                            }
                        }
                    }
                ),
                Tool(
                    name="create_task",
                    description="Create a new task",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Task title"
                            },
                            "description": {
                                "type": "string",
                                "description": "Task description"
                            },
                            "business_context": {
                                "type": "string",
                                "description": "Business context name (e.g., 'woodys-creations', 'dj-business')"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["urgent", "high", "medium", "low"],
                                "default": "medium"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Due date in ISO format (YYYY-MM-DD)"
                            }
                        },
                        "required": ["title", "business_context"]
                    }
                ),
                Tool(
                    name="update_task",
                    description="Update task status or details",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "string",
                                "description": "Task UUID"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "in_progress", "completed", "cancelled"]
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["urgent", "high", "medium", "low"]
                            }
                        },
                        "required": ["task_id"]
                    }
                ),
                Tool(
                    name="get_emails",
                    description="Get emails filtered by business context, priority, or processed status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_context": {
                                "type": "string",
                                "description": "Filter by business context"
                            },
                            "is_processed": {
                                "type": "boolean",
                                "description": "Filter by processed status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["urgent", "high", "medium", "low"]
                            },
                            "limit": {
                                "type": "number",
                                "default": 20
                            }
                        }
                    }
                ),
                Tool(
                    name="get_calendar_events",
                    description="Get calendar events for a date range",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "start_date": {
                                "type": "string",
                                "description": "Start date (YYYY-MM-DD)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date (YYYY-MM-DD)"
                            },
                            "business_context": {
                                "type": "string",
                                "description": "Optional filter by business context"
                            }
                        },
                        "required": ["start_date", "end_date"]
                    }
                ),
                Tool(
                    name="search_knowledge_base",
                    description="Search the knowledge base using semantic search (if embeddings exist) or text search",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            },
                            "business_context": {
                                "type": "string",
                                "description": "Optional filter by business context"
                            },
                            "limit": {
                                "type": "number",
                                "default": 5
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="save_agent_memory",
                    description="Save a memory/fact for the agent to remember",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Name of the agent"
                            },
                            "content": {
                                "type": "string",
                                "description": "Memory content to save"
                            },
                            "memory_type": {
                                "type": "string",
                                "enum": ["fact", "preference", "pattern", "instruction"],
                                "default": "fact"
                            },
                            "importance": {
                                "type": "number",
                                "description": "Importance score 1-10",
                                "default": 5
                            }
                        },
                        "required": ["agent_name", "content"]
                    }
                ),
                Tool(
                    name="recall_agent_memory",
                    description="Recall relevant memories for the agent",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Name of the agent"
                            },
                            "query": {
                                "type": "string",
                                "description": "What to recall about"
                            },
                            "limit": {
                                "type": "number",
                                "default": 10
                            }
                        },
                        "required": ["agent_name"]
                    }
                ),
                Tool(
                    name="get_customer_history",
                    description="Get customer history including past orders, bookings, emails",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "customer_email": {
                                "type": "string",
                                "description": "Customer email address"
                            },
                            "customer_id": {
                                "type": "string",
                                "description": "Customer UUID (if known)"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_business_metrics",
                    description="Get business metrics for a specific period",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "business_context": {
                                "type": "string",
                                "description": "Business context name"
                            },
                            "metric_type": {
                                "type": "string",
                                "description": "Type of metric (revenue, bookings, orders, hours_worked)"
                            },
                            "start_date": {
                                "type": "string",
                                "description": "Start date (YYYY-MM-DD)"
                            },
                            "end_date": {
                                "type": "string",
                                "description": "End date (YYYY-MM-DD)"
                            }
                        },
                        "required": ["business_context", "start_date", "end_date"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent]:
            """Handle tool calls"""

            conn = self._get_db_connection()
            try:
                cursor = conn.cursor(cursor_factory=RealDictCursor)

                if name == "query_database":
                    query = arguments["query"]
                    params = arguments.get("params", [])

                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "get_tasks":
                    filters = []
                    params = []

                    if "business_context" in arguments:
                        filters.append("bc.name = %s")
                        params.append(arguments["business_context"])

                    if "status" in arguments:
                        filters.append("t.status = %s")
                        params.append(arguments["status"])

                    if "priority" in arguments:
                        filters.append("t.priority = %s")
                        params.append(arguments["priority"])

                    where_clause = " AND ".join(filters) if filters else "1=1"
                    limit = arguments.get("limit", 20)

                    query = f"""
                        SELECT
                            t.id,
                            t.title,
                            t.description,
                            t.priority,
                            t.status,
                            t.due_date,
                            bc.display_name as business,
                            bc.emoji
                        FROM tasks t
                        JOIN business_contexts bc ON t.business_context_id = bc.id
                        WHERE {where_clause}
                        ORDER BY
                            CASE t.priority
                                WHEN 'urgent' THEN 1
                                WHEN 'high' THEN 2
                                WHEN 'medium' THEN 3
                                ELSE 4
                            END,
                            t.due_date ASC NULLS LAST
                        LIMIT %s
                    """

                    params.append(limit)
                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "create_task":
                    # Get business context ID
                    cursor.execute(
                        "SELECT id FROM business_contexts WHERE name = %s",
                        [arguments["business_context"]]
                    )
                    context = cursor.fetchone()

                    if not context:
                        return [TextContent(
                            type="text",
                            text=f"Error: Business context '{arguments['business_context']}' not found"
                        )]

                    # Create task
                    cursor.execute("""
                        INSERT INTO tasks (business_context_id, title, description, priority, due_date, created_by_ai)
                        VALUES (%s, %s, %s, %s, %s, true)
                        RETURNING id, title
                    """, [
                        context['id'],
                        arguments["title"],
                        arguments.get("description"),
                        arguments.get("priority", "medium"),
                        arguments.get("due_date")
                    ])

                    result = cursor.fetchone()
                    conn.commit()

                    return [TextContent(
                        type="text",
                        text=f"Task created: {result['title']} (ID: {result['id']})"
                    )]

                elif name == "update_task":
                    updates = []
                    params = []

                    if "status" in arguments:
                        updates.append("status = %s")
                        params.append(arguments["status"])

                        if arguments["status"] == "completed":
                            updates.append("completed_at = NOW()")

                    if "priority" in arguments:
                        updates.append("priority = %s")
                        params.append(arguments["priority"])

                    if not updates:
                        return [TextContent(
                            type="text",
                            text="Error: No updates specified"
                        )]

                    params.append(arguments["task_id"])

                    query = f"""
                        UPDATE tasks
                        SET {', '.join(updates)}
                        WHERE id = %s
                        RETURNING id, title, status
                    """

                    cursor.execute(query, params)
                    result = cursor.fetchone()
                    conn.commit()

                    if result:
                        return [TextContent(
                            type="text",
                            text=f"Task updated: {result['title']} -> {result['status']}"
                        )]
                    else:
                        return [TextContent(
                            type="text",
                            text=f"Error: Task not found"
                        )]

                elif name == "get_emails":
                    filters = []
                    params = []

                    if "business_context" in arguments:
                        filters.append("bc.name = %s")
                        params.append(arguments["business_context"])

                    if "is_processed" in arguments:
                        filters.append("e.is_processed = %s")
                        params.append(arguments["is_processed"])

                    if "priority" in arguments:
                        filters.append("e.priority = %s")
                        params.append(arguments["priority"])

                    where_clause = " AND ".join(filters) if filters else "1=1"
                    limit = arguments.get("limit", 20)

                    query = f"""
                        SELECT
                            e.id,
                            e.subject,
                            e.from_email,
                            e.from_name,
                            e.received_at,
                            e.priority,
                            e.action_needed,
                            e.ai_summary,
                            bc.display_name as business,
                            bc.emoji
                        FROM emails e
                        JOIN business_contexts bc ON e.business_context_id = bc.id
                        WHERE {where_clause}
                        ORDER BY e.received_at DESC
                        LIMIT %s
                    """

                    params.append(limit)
                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "get_calendar_events":
                    filters = ["ce.start_time BETWEEN %s AND %s"]
                    params = [arguments["start_date"], arguments["end_date"]]

                    if "business_context" in arguments:
                        filters.append("bc.name = %s")
                        params.append(arguments["business_context"])

                    where_clause = " AND ".join(filters)

                    query = f"""
                        SELECT
                            ce.id,
                            ce.title,
                            ce.start_time,
                            ce.end_time,
                            ce.location,
                            ce.description,
                            bc.display_name as business,
                            bc.emoji
                        FROM calendar_events ce
                        JOIN business_contexts bc ON ce.business_context_id = bc.id
                        WHERE {where_clause}
                        ORDER BY ce.start_time
                    """

                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "search_knowledge_base":
                    query = """
                        SELECT
                            kb.id,
                            kb.title,
                            kb.content,
                            kb.content_type,
                            kb.category,
                            bc.display_name as business
                        FROM knowledge_base kb
                        LEFT JOIN business_contexts bc ON kb.business_context_id = bc.id
                        WHERE kb.is_active = true
                          AND kb.content ILIKE %s
                    """

                    params = [f"%{arguments['query']}%"]

                    if "business_context" in arguments:
                        query += " AND bc.name = %s"
                        params.append(arguments["business_context"])

                    query += f" LIMIT %s"
                    params.append(arguments.get("limit", 5))

                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "save_agent_memory":
                    cursor.execute("""
                        INSERT INTO agent_memory (agent_name, content, memory_type, importance_score)
                        VALUES (%s, %s, %s, %s)
                        RETURNING id
                    """, [
                        arguments["agent_name"],
                        arguments["content"],
                        arguments.get("memory_type", "fact"),
                        arguments.get("importance", 5)
                    ])

                    result = cursor.fetchone()
                    conn.commit()

                    return [TextContent(
                        type="text",
                        text=f"Memory saved (ID: {result['id']})"
                    )]

                elif name == "recall_agent_memory":
                    query = """
                        SELECT content, memory_type, importance_score, created_at
                        FROM agent_memory
                        WHERE agent_name = %s
                          AND is_active = true
                    """

                    params = [arguments["agent_name"]]

                    if "query" in arguments:
                        query += " AND content ILIKE %s"
                        params.append(f"%{arguments['query']}%")

                    query += """
                        ORDER BY importance_score DESC, access_count DESC, created_at DESC
                        LIMIT %s
                    """

                    params.append(arguments.get("limit", 10))

                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    # Update access count
                    for row in results:
                        cursor.execute("""
                            UPDATE agent_memory
                            SET access_count = access_count + 1,
                                last_accessed = NOW()
                            WHERE agent_name = %s AND content = %s
                        """, [arguments["agent_name"], row['content']])

                    conn.commit()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                elif name == "get_customer_history":
                    # Find customer
                    if "customer_id" in arguments:
                        cursor.execute("SELECT * FROM customers WHERE id = %s", [arguments["customer_id"]])
                    elif "customer_email" in arguments:
                        cursor.execute("SELECT * FROM customers WHERE email = %s", [arguments["customer_email"]])
                    else:
                        return [TextContent(type="text", text="Error: No customer identifier provided")]

                    customer = cursor.fetchone()

                    if not customer:
                        return [TextContent(type="text", text="Customer not found")]

                    # Get orders
                    cursor.execute("""
                        SELECT order_reference, status, order_date, quoted_price
                        FROM woodys_orders
                        WHERE customer_id = %s
                        ORDER BY order_date DESC
                    """, [customer['id']])
                    orders = cursor.fetchall()

                    # Get bookings
                    cursor.execute("""
                        SELECT booking_reference, status, event_date, quoted_price
                        FROM dj_bookings
                        WHERE customer_id = %s
                        ORDER BY event_date DESC
                    """, [customer['id']])
                    bookings = cursor.fetchall()

                    history = {
                        "customer": dict(customer),
                        "orders": [dict(row) for row in orders],
                        "bookings": [dict(row) for row in bookings]
                    }

                    return [TextContent(
                        type="text",
                        text=json.dumps(history, indent=2, default=str)
                    )]

                elif name == "get_business_metrics":
                    cursor.execute("""
                        SELECT
                            bc.id
                        FROM business_contexts bc
                        WHERE bc.name = %s
                    """, [arguments["business_context"]])

                    context = cursor.fetchone()

                    if not context:
                        return [TextContent(type="text", text="Business context not found")]

                    query = """
                        SELECT
                            metric_date,
                            metric_type,
                            metric_value,
                            metric_unit,
                            comparison_previous_period
                        FROM business_metrics
                        WHERE business_context_id = %s
                          AND metric_date BETWEEN %s AND %s
                    """

                    params = [context['id'], arguments["start_date"], arguments["end_date"]]

                    if "metric_type" in arguments:
                        query += " AND metric_type = %s"
                        params.append(arguments["metric_type"])

                    query += " ORDER BY metric_date DESC"

                    cursor.execute(query, params)
                    results = cursor.fetchall()

                    return [TextContent(
                        type="text",
                        text=json.dumps([dict(row) for row in results], indent=2, default=str)
                    )]

                else:
                    return [TextContent(
                        type="text",
                        text=f"Unknown tool: {name}"
                    )]

            except Exception as e:
                conn.rollback()
                return [TextContent(
                    type="text",
                    text=f"Database error: {str(e)}"
                )]
            finally:
                cursor.close()
                self.db_pool.putconn(conn)

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
    server = SupabaseMCPServer()
    asyncio.run(server.run())


if __name__ == "__main__":
    main()
