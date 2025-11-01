#!/usr/bin/env python3
"""
AIPA CrewAI Multi-Agent System
Coordinates specialized AI agents for business management
"""

import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

from crewai import Agent, Task, Crew, Process
from crewai_tools import tool
from langchain.tools import Tool
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Custom tools (will be implemented)
from tools.gmail_tools import GmailTools
from tools.database_tools import DatabaseTools
from tools.calendar_tools import CalendarTools


class AIPersonalAssistant:
    """
    Main AI PA system coordinating multiple specialized agents
    """

    def __init__(self):
        # Initialize AI models
        self.claude = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=0.3,
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
        )

        self.gemini = ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=0.1,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        # Initialize tools
        self.gmail_tools = GmailTools()
        self.db_tools = DatabaseTools()
        self.calendar_tools = CalendarTools()

        # Create agents
        self.agents = self._create_agents()

    def _create_agents(self) -> Dict[str, Agent]:
        """Create all specialized agents"""

        # ============================================
        # Executive Assistant - Main coordinator
        # ============================================
        executive_assistant = Agent(
            role='Executive Assistant',
            goal='Coordinate all business operations across multiple contexts and delegate to specialist agents',
            backstory="""You are Woody's trusted Executive Assistant with deep knowledge of his multiple businesses:
            - Woody's Creations (laser-cut gifts)
            - DJ Business (event services)
            - BMF Work (contract work)
            - Future Pub (planning phase)

            You maintain context across all areas, prioritize ruthlessly, and ensure nothing falls through the cracks.
            You're proactive, efficient, and always thinking two steps ahead.""",
            verbose=True,
            allow_delegation=True,  # Can delegate to other agents
            llm=self.claude,
            tools=[
                self.db_tools.get_tasks_tool(),
                self.db_tools.get_emails_tool(),
                self.db_tools.get_calendar_tool(),
                self.db_tools.recall_memory_tool()
            ],
            max_iter=10
        )

        # ============================================
        # Email Manager - Email triage specialist
        # ============================================
        email_manager = Agent(
            role='Email Manager',
            goal='Efficiently triage, classify, and process emails across all business contexts',
            backstory="""You're an expert at quickly understanding email content, detecting urgency,
            and routing messages appropriately. You know the patterns of each business and can
            spot opportunities, issues, and routine correspondence instantly.""",
            verbose=True,
            allow_delegation=False,
            llm=self.gemini,  # Use Gemini for cost efficiency
            tools=[
                self.gmail_tools.search_emails_tool(),
                self.gmail_tools.get_email_tool(),
                self.gmail_tools.apply_label_tool(),
                self.gmail_tools.create_draft_tool(),
                self.db_tools.save_email_tool(),
                self.db_tools.search_knowledge_tool(),
                self.db_tools.get_customer_history_tool()
            ]
        )

        # ============================================
        # Calendar Manager - Scheduling specialist
        # ============================================
        calendar_manager = Agent(
            role='Calendar Manager',
            goal='Optimize schedule across all business contexts, detect conflicts, and suggest optimal time blocks',
            backstory="""You're a scheduling genius who understands the different needs of each business:
            - DJ gigs need travel time and setup buffers
            - Woody's production needs uninterrupted blocks
            - BMF work requires focus time
            - Personal time is sacred

            You balance everything while protecting productivity.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.calendar_tools.get_events_tool(),
                self.calendar_tools.check_availability_tool(),
                self.calendar_tools.create_event_tool(),
                self.db_tools.create_task_tool()
            ]
        )

        # ============================================
        # Business Strategist - Insights & analysis
        # ============================================
        business_strategist = Agent(
            role='Business Strategist',
            goal='Analyze business performance, identify trends, spot opportunities and risks',
            backstory="""You're a strategic thinker who sees patterns across all the businesses.
            You track KPIs, notice seasonal trends, identify optimization opportunities,
            and provide actionable insights. You think long-term while staying grounded in data.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.db_tools.get_metrics_tool(),
                self.db_tools.query_database_tool(),
                self.db_tools.save_insight_tool()
            ]
        )

        # ============================================
        # Marketing Manager - Campaign & content
        # ============================================
        marketing_manager = Agent(
            role='Marketing Manager',
            goal='Create marketing strategies and content for each business with zero budget',
            backstory="""You're creative and resourceful, specializing in organic growth.
            You understand each business's unique value proposition and target audience.
            You create compelling content and campaigns that work within budget constraints.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.db_tools.get_metrics_tool(),
                self.db_tools.search_knowledge_tool(),
                self.db_tools.save_memory_tool()
            ]
        )

        # ============================================
        # DJ Booking Manager - DJ business specialist
        # ============================================
        dj_booking_manager = Agent(
            role='DJ Booking Manager',
            goal='Handle DJ booking inquiries, generate quotes, manage pipeline',
            backstory="""You're an expert in the DJ/events industry. You know standard pricing,
            what questions to ask clients, how to qualify leads, and how to close bookings.
            You can generate professional quotes and handle the full booking lifecycle.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.gmail_tools.create_draft_tool(),
                self.db_tools.create_booking_tool(),
                self.db_tools.get_customer_history_tool(),
                self.calendar_tools.check_availability_tool(),
                self.db_tools.search_knowledge_tool()  # Access DJ pricing/terms
            ]
        )

        # ============================================
        # Operations Manager - Woody's Creations
        # ============================================
        operations_manager = Agent(
            role='Operations Manager',
            goal='Manage Woody\'s Creations orders, production scheduling, and inventory',
            backstory="""You understand the production process for laser-cut products.
            You can estimate production time, check material inventory, schedule production runs,
            and ensure timely delivery. You balance quality, efficiency, and customer satisfaction.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.gmail_tools.create_draft_tool(),
                self.db_tools.create_order_tool(),
                self.db_tools.get_customer_history_tool(),
                self.calendar_tools.create_event_tool(),  # Schedule production
                self.db_tools.search_knowledge_tool()  # Access materials/pricing
            ]
        )

        # ============================================
        # Project Coordinator - BMF work tracking
        # ============================================
        project_coordinator = Agent(
            role='Project Coordinator',
            goal='Track BMF work hours, manage project deadlines, handle invoicing',
            backstory="""You're detail-oriented and organized, ensuring all work is properly logged,
            deadlines are met, and invoicing happens on time. You understand the project lifecycle
            and can provide status updates at any time.""",
            verbose=True,
            allow_delegation=False,
            llm=self.claude,
            tools=[
                self.db_tools.log_work_hours_tool(),
                self.db_tools.get_work_log_tool(),
                self.db_tools.create_task_tool(),
                self.calendar_tools.get_events_tool()
            ]
        )

        return {
            'executive': executive_assistant,
            'email': email_manager,
            'calendar': calendar_manager,
            'strategist': business_strategist,
            'marketing': marketing_manager,
            'dj': dj_booking_manager,
            'operations': operations_manager,
            'project': project_coordinator
        }

    def process_user_message(self, user_message: str, user_id: str, context: Dict = None) -> str:
        """
        Main entry point for processing user messages
        Routes to appropriate workflow based on intent
        """

        # Detect intent
        intent = self._detect_intent(user_message, context)

        # Route to appropriate workflow
        if intent == 'briefing':
            return self.generate_daily_briefing(user_id)
        elif intent == 'email_triage':
            return self.process_emails(user_id)
        elif intent == 'schedule_query':
            return self.handle_calendar_query(user_message, user_id)
        elif intent == 'dj_inquiry':
            return self.handle_dj_inquiry(user_message, context)
        elif intent == 'order_inquiry':
            return self.handle_order_inquiry(user_message, context)
        elif intent == 'task_management':
            return self.manage_tasks(user_message, user_id)
        elif intent == 'business_insights':
            return self.generate_insights(user_message, user_id)
        else:
            # General conversation - use executive assistant
            return self.general_conversation(user_message, user_id)

    def generate_daily_briefing(self, user_id: str) -> str:
        """Generate comprehensive daily briefing"""

        # Create tasks for the crew
        tasks = [
            Task(
                description=f"""Gather today's calendar events for user {user_id}.
                Include all business contexts, highlight conflicts, and identify gaps.""",
                agent=self.agents['calendar'],
                expected_output="Formatted list of today's events with analysis"
            ),
            Task(
                description=f"""Summarize unprocessed emails for user {user_id}.
                Group by business context, flag urgent items, count total by priority.""",
                agent=self.agents['email'],
                expected_output="Email summary grouped by business and priority"
            ),
            Task(
                description=f"""List top priority tasks for user {user_id}.
                Focus on urgent and high priority items due today or overdue.""",
                agent=self.agents['calendar'],
                expected_output="Prioritized task list with deadlines"
            ),
            Task(
                description="""Compile the briefing sections into a cohesive daily summary.
                Format for Telegram with emojis, be concise, highlight what needs immediate attention.""",
                agent=self.agents['executive'],
                expected_output="Complete formatted daily briefing",
                context=[0, 1, 2]  # Use outputs from previous tasks
            )
        ]

        # Create and run the crew
        crew = Crew(
            agents=[self.agents['executive'], self.agents['calendar'], self.agents['email']],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def process_emails(self, user_id: str, limit: int = 10) -> str:
        """Process and triage new emails"""

        task = Task(
            description=f"""Process the latest {limit} unread emails for user {user_id}:
            1. Classify each by business context
            2. Determine priority and action needed
            3. Apply appropriate Gmail labels
            4. Save to database with AI summary
            5. For urgent items, prepare notifications
            6. For inquiries, draft responses if confident

            Return summary of processed emails and any that need immediate attention.""",
            agent=self.agents['email'],
            expected_output="Summary of processed emails with urgent items highlighted"
        )

        crew = Crew(
            agents=[self.agents['email']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def handle_dj_inquiry(self, email_content: str, context: Dict) -> str:
        """Handle DJ booking inquiry with automated response"""

        tasks = [
            Task(
                description=f"""Analyze this DJ booking inquiry:
                {email_content}

                Extract:
                - Event date and time
                - Event type (wedding, corporate, etc.)
                - Venue and location
                - Guest count
                - Special requests

                Check calendar availability and determine if we can accommodate.""",
                agent=self.agents['dj'],
                expected_output="Structured inquiry details with availability check"
            ),
            Task(
                description="""Based on the inquiry analysis:
                1. Generate a professional quote using our pricing from knowledge base
                2. Create a personalized response draft
                3. Include our terms and deposit requirements
                4. Add a call-to-action

                The response should be warm but professional, highlighting our experience.""",
                agent=self.agents['dj'],
                expected_output="Professional quote email draft ready for review",
                context=[0]
            )
        ]

        crew = Crew(
            agents=[self.agents['dj']],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def handle_order_inquiry(self, email_content: str, context: Dict) -> str:
        """Handle Woody's Creations order inquiry"""

        tasks = [
            Task(
                description=f"""Analyze this order inquiry for Woody's Creations:
                {email_content}

                Extract:
                - Product type and description
                - Quantity
                - Material preference (oak, pine, acrylic)
                - Personalization details
                - Deadline/urgency

                Check current production capacity and estimate lead time.""",
                agent=self.agents['operations'],
                expected_output="Structured order details with production feasibility"
            ),
            Task(
                description="""Based on the order analysis:
                1. Calculate pricing based on materials and complexity
                2. Provide estimated completion date
                3. Create professional response with quote
                4. Include our terms and design process
                5. Suggest upsells if appropriate (rush service, premium materials)

                Be friendly and enthusiastic about creating their custom piece.""",
                agent=self.agents['operations'],
                expected_output="Order confirmation email draft with quote",
                context=[0]
            )
        ]

        crew = Crew(
            agents=[self.agents['operations']],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def manage_tasks(self, user_message: str, user_id: str) -> str:
        """Manage tasks - create, update, or query"""

        task = Task(
            description=f"""Handle this task management request:
            "{user_message}"

            Actions you can take:
            - Create new tasks
            - Update task status
            - Query tasks by business/priority/status
            - Suggest task priorities based on deadlines

            Respond with what was done and current task status.""",
            agent=self.agents['executive'],
            expected_output="Task management action summary"
        )

        crew = Crew(
            agents=[self.agents['executive']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def generate_insights(self, query: str, user_id: str) -> str:
        """Generate business insights and analytics"""

        task = Task(
            description=f"""Analyze business performance based on this request:
            "{query}"

            Pull relevant metrics, identify trends, and provide actionable insights.
            Compare to previous periods when possible.
            Be specific with numbers and recommendations.""",
            agent=self.agents['strategist'],
            expected_output="Business analysis with insights and recommendations"
        )

        crew = Crew(
            agents=[self.agents['strategist']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def handle_calendar_query(self, query: str, user_id: str) -> str:
        """Handle calendar-related queries"""

        task = Task(
            description=f"""Handle this calendar request:
            "{query}"

            Can include:
            - Viewing schedule for specific dates
            - Checking availability
            - Finding free time
            - Scheduling new events
            - Detecting conflicts

            Provide clear, formatted response.""",
            agent=self.agents['calendar'],
            expected_output="Calendar information and/or availability analysis"
        )

        crew = Crew(
            agents=[self.agents['calendar']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()
        return result

    def general_conversation(self, message: str, user_id: str) -> str:
        """Handle general conversation with executive assistant"""

        # Recall relevant memories
        memory_context = self._recall_relevant_memories(message, user_id)

        task = Task(
            description=f"""User says: "{message}"

            Context from memory:
            {memory_context}

            Respond helpfully and naturally. You can:
            - Answer questions about their businesses
            - Provide quick updates
            - Make suggestions
            - Clarify or ask follow-up questions

            Be conversational but efficient.""",
            agent=self.agents['executive'],
            expected_output="Natural conversational response"
        )

        crew = Crew(
            agents=[self.agents['executive']],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        result = crew.kickoff()

        # Save interaction to memory
        self._save_to_memory(message, result, user_id)

        return result

    def _detect_intent(self, message: str, context: Dict = None) -> str:
        """Detect user intent from message"""

        message_lower = message.lower()

        # Keyword matching (can be enhanced with ML later)
        if any(word in message_lower for word in ['briefing', 'summary', 'update', "what's up"]):
            return 'briefing'
        elif any(word in message_lower for word in ['email', 'inbox', 'unread']):
            return 'email_triage'
        elif any(word in message_lower for word in ['calendar', 'schedule', 'meeting', 'when']):
            return 'schedule_query'
        elif any(word in message_lower for word in ['task', 'todo', 'remind']):
            return 'task_management'
        elif any(word in message_lower for word in ['insight', 'analytics', 'performance', 'metrics', 'revenue']):
            return 'business_insights'
        elif context and context.get('email_type') == 'dj_inquiry':
            return 'dj_inquiry'
        elif context and context.get('email_type') == 'order_inquiry':
            return 'order_inquiry'
        else:
            return 'general'

    def _recall_relevant_memories(self, query: str, user_id: str) -> str:
        """Recall relevant memories for context"""
        # Implementation would query agent_memory table
        # For now, return empty
        return ""

    def _save_to_memory(self, user_message: str, assistant_response: str, user_id: str):
        """Save interaction to agent memory"""
        # Implementation would save to agent_memory table
        pass


# Autonomous background agent
class AutonomousAgent:
    """
    Background agent that runs periodic tasks without user input
    """

    def __init__(self, aipa_system: AIPersonalAssistant):
        self.aipa = aipa_system
        self.db_tools = DatabaseTools()

    def morning_routine(self, user_id: str):
        """Run every morning at configured time"""

        # Generate daily briefing
        briefing = self.aipa.generate_daily_briefing(user_id)

        # Send via Telegram (implementation needed)
        self._send_telegram_message(user_id, briefing)

        # Process overnight emails
        email_summary = self.aipa.process_emails(user_id, limit=50)

        # Check for urgent items
        urgent = self._check_urgent_items(user_id)
        if urgent:
            self._send_telegram_message(user_id, f"🔴 URGENT ITEMS:\n{urgent}")

    def check_stale_items(self, user_id: str):
        """Check for items needing follow-up"""

        # Unanswered emails > 24 hours
        stale_emails = self.db_tools.get_stale_emails(user_id, hours=24)

        if stale_emails:
            # Draft responses
            for email in stale_emails:
                # Agent drafts response
                task = Task(
                    description=f"""This email has been unanswered for 24+ hours:
                    From: {email['from']}
                    Subject: {email['subject']}
                    Summary: {email['summary']}

                    Draft a polite response or follow-up.""",
                    agent=self.aipa.agents['email'],
                    expected_output="Draft email response"
                )

                crew = Crew(agents=[self.aipa.agents['email']], tasks=[task], verbose=False)
                draft = crew.kickoff()

                # Request approval
                self._request_approval(user_id, f"Draft response for: {email['subject']}", draft)

    def detect_patterns_and_insights(self, user_id: str):
        """Proactively identify patterns and generate insights"""

        task = Task(
            description="""Analyze recent business data to identify:
            - Unusual trends (booking surges, order drops)
            - Potential issues (low inventory, overdue items)
            - Opportunities (seasonal demand, upsell potential)

            Generate proactive insights worth sharing.""",
            agent=self.aipa.agents['strategist'],
            expected_output="Proactive business insights"
        )

        crew = Crew(agents=[self.aipa.agents['strategist']], tasks=[task], verbose=False)
        insights = crew.kickoff()

        if insights:
            self._send_telegram_message(user_id, f"💡 INSIGHT:\n{insights}")

    def _send_telegram_message(self, user_id: str, message: str):
        """Send message via Telegram"""
        # Implementation needed - integrate with Telegram API
        pass

    def _request_approval(self, user_id: str, title: str, content: str):
        """Request user approval for agent action"""
        # Implementation needed - send to user with approve/reject buttons
        pass

    def _check_urgent_items(self, user_id: str) -> str:
        """Check for urgent items needing attention"""
        # Implementation - query database for urgent emails, tasks, deadlines
        return ""


if __name__ == "__main__":
    # Test the system
    aipa = AIPersonalAssistant()

    # Example: Process a message
    response = aipa.process_user_message(
        user_message="What's on my schedule today?",
        user_id="user-uuid-here"
    )

    print(response)
