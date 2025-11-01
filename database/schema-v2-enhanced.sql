-- =====================================================
-- AI Personal Assistant (AIPA) - Enhanced Database Schema V2
-- With Vector Search, Agent Memory, and Advanced Features
-- Version: 2.0.0
-- =====================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";  -- For semantic search
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- For fuzzy text search

-- =====================================================
-- BUSINESS CONTEXTS (Enhanced)
-- =====================================================

CREATE TABLE IF NOT EXISTS business_contexts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(20),
    emoji VARCHAR(10),
    gmail_label VARCHAR(100),
    calendar_id VARCHAR(255),
    drive_folder_id VARCHAR(255),
    is_active BOOLEAN DEFAULT true,

    -- New: Business metadata
    business_type VARCHAR(50), -- 'product', 'service', 'contract', 'personal'
    timezone VARCHAR(50) DEFAULT 'Europe/London',
    working_hours JSONB, -- {"monday": {"start": "09:00", "end": "17:00"}, ...}

    -- New: Agent configuration
    agent_config JSONB, -- AI agent settings per business
    automation_rules JSONB, -- Custom automation rules

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- USERS (Enhanced with preferences)
-- =====================================================

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    role VARCHAR(50) DEFAULT 'user',
    allowed_contexts TEXT[],
    is_active BOOLEAN DEFAULT true,

    -- New: User preferences
    preferences JSONB DEFAULT '{
        "briefing_time": "08:00",
        "notification_urgency": ["urgent", "high"],
        "work_schedule": {},
        "communication_style": "professional",
        "auto_approve_threshold": 0.95
    }'::jsonb,

    -- New: Agent memory
    long_term_memory JSONB DEFAULT '{}'::jsonb,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONVERSATIONS (Enhanced with vectors)
-- =====================================================

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL,
    intent VARCHAR(100),
    metadata JSONB,

    -- New: Vector embedding for semantic search
    embedding vector(1536),

    -- New: Agent tracking
    processing_agent VARCHAR(100), -- Which agent handled this
    agent_confidence DECIMAL(3, 2),

    -- New: Conversation threading
    thread_id UUID, -- Group related messages
    parent_message_id UUID REFERENCES conversations(id),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_context ON conversations(business_context_id);
CREATE INDEX idx_conversations_thread ON conversations(thread_id);
CREATE INDEX idx_conversations_embedding ON conversations USING ivfflat (embedding vector_cosine_ops);

-- =====================================================
-- EMAILS (Enhanced with vectors and auto-response)
-- =====================================================

CREATE TABLE IF NOT EXISTS emails (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gmail_id VARCHAR(255) UNIQUE NOT NULL,
    gmail_thread_id VARCHAR(255),
    business_context_id UUID REFERENCES business_contexts(id),
    subject TEXT,
    from_email VARCHAR(255),
    from_name VARCHAR(255),
    to_email VARCHAR(255),
    received_at TIMESTAMP WITH TIME ZONE,
    priority VARCHAR(20),
    ai_summary TEXT,
    action_needed VARCHAR(50),
    sentiment VARCHAR(20),
    key_points JSONB,
    is_processed BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,

    -- New: Vector embedding for semantic search
    embedding vector(1536),

    -- New: Structured data extraction
    extracted_data JSONB, -- Dates, amounts, contacts, etc.
    entity_mentions JSONB, -- People, companies, products mentioned

    -- New: Auto-response tracking
    auto_response_suggested BOOLEAN DEFAULT false,
    auto_response_sent BOOLEAN DEFAULT false,
    auto_response_draft TEXT,
    auto_response_confidence DECIMAL(3, 2),
    requires_approval BOOLEAN DEFAULT true,

    -- New: Customer tracking
    customer_id UUID, -- Link to customer record
    related_order_id UUID, -- Link to order if applicable
    related_booking_id UUID, -- Link to booking if applicable

    -- New: Similar emails
    similar_email_ids UUID[], -- IDs of similar past emails

    user_action_taken VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_emails_gmail_id ON emails(gmail_id);
CREATE INDEX idx_emails_context ON emails(business_context_id);
CREATE INDEX idx_emails_embedding ON emails USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_emails_from ON emails(from_email);
CREATE INDEX idx_emails_customer ON emails(customer_id);

-- =====================================================
-- CUSTOMERS (New - Unified customer database)
-- =====================================================

CREATE TABLE IF NOT EXISTS customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Contact info
    email VARCHAR(255),
    phone VARCHAR(50),
    name VARCHAR(255) NOT NULL,
    company VARCHAR(255),

    -- Classification
    customer_type VARCHAR(50), -- 'lead', 'customer', 'repeat', 'vip'
    source VARCHAR(100), -- 'email', 'referral', 'website', etc.

    -- History
    first_contact_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_contact_date TIMESTAMP WITH TIME ZONE,
    total_orders INTEGER DEFAULT 0,
    total_bookings INTEGER DEFAULT 0,
    total_revenue DECIMAL(12, 2) DEFAULT 0,

    -- Preferences
    preferences JSONB,
    notes TEXT,
    tags TEXT[],

    -- Vector for similarity matching
    profile_embedding vector(1536),

    -- Status
    is_active BOOLEAN DEFAULT true,
    blacklisted BOOLEAN DEFAULT false,
    blacklist_reason TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_customers_email ON customers(email);
CREATE INDEX idx_customers_business ON customers(business_context_id);
CREATE INDEX idx_customers_type ON customers(customer_type);

-- =====================================================
-- AGENT MEMORY (New - Persistent agent memory)
-- =====================================================

CREATE TABLE IF NOT EXISTS agent_memory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    agent_name VARCHAR(100) NOT NULL,
    memory_type VARCHAR(50), -- 'fact', 'preference', 'pattern', 'instruction'

    -- Memory content
    content TEXT NOT NULL,
    embedding vector(1536),

    -- Context
    business_context_id UUID REFERENCES business_contexts(id),
    related_entity_type VARCHAR(50), -- 'customer', 'order', 'task', etc.
    related_entity_id UUID,

    -- Metadata
    confidence DECIMAL(3, 2),
    importance_score INTEGER DEFAULT 5, -- 1-10
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE,

    -- Lifecycle
    expires_at TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT true,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_agent_memory_user ON agent_memory(user_id);
CREATE INDEX idx_agent_memory_agent ON agent_memory(agent_name);
CREATE INDEX idx_agent_memory_embedding ON agent_memory USING ivfflat (embedding vector_cosine_ops);

-- =====================================================
-- KNOWLEDGE BASE (New - RAG system)
-- =====================================================

CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Content
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50), -- 'policy', 'faq', 'template', 'procedure', 'price'

    -- Vector for RAG
    embedding vector(1536),

    -- Metadata
    category VARCHAR(100),
    tags TEXT[],
    language VARCHAR(10) DEFAULT 'en',

    -- Source
    source_type VARCHAR(50), -- 'manual', 'learned', 'imported'
    source_url TEXT,

    -- Usage tracking
    access_count INTEGER DEFAULT 0,
    last_accessed TIMESTAMP WITH TIME ZONE,

    -- Versioning
    version INTEGER DEFAULT 1,
    is_latest BOOLEAN DEFAULT true,
    supersedes_id UUID REFERENCES knowledge_base(id),

    -- Status
    is_active BOOLEAN DEFAULT true,
    requires_review BOOLEAN DEFAULT false,

    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_knowledge_business ON knowledge_base(business_context_id);
CREATE INDEX idx_knowledge_type ON knowledge_base(content_type);
CREATE INDEX idx_knowledge_embedding ON knowledge_base USING ivfflat (embedding vector_cosine_ops);

-- =====================================================
-- TASKS (Enhanced with agent automation)
-- =====================================================

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium',
    status VARCHAR(20) DEFAULT 'pending',
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,

    -- New: Agent automation
    created_by_ai BOOLEAN DEFAULT false,
    ai_suggested_reason TEXT,
    can_auto_complete BOOLEAN DEFAULT false,
    auto_complete_conditions JSONB,

    -- New: Dependencies
    depends_on_tasks UUID[],
    blocks_tasks UUID[],

    -- New: Recurrence
    is_recurring BOOLEAN DEFAULT false,
    recurrence_rule JSONB, -- {"frequency": "weekly", "interval": 1, ...}
    parent_recurring_task_id UUID REFERENCES tasks(id),

    -- New: Time tracking
    estimated_duration_minutes INTEGER,
    actual_duration_minutes INTEGER,
    started_at TIMESTAMP WITH TIME ZONE,

    -- Links
    parent_task_id UUID REFERENCES tasks(id),
    related_email_id UUID REFERENCES emails(id),
    related_customer_id UUID REFERENCES customers(id),

    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_context ON tasks(business_context_id);
CREATE INDEX idx_tasks_user ON tasks(user_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due ON tasks(due_date);
CREATE INDEX idx_tasks_recurring ON tasks(is_recurring, parent_recurring_task_id);

-- =====================================================
-- CALENDAR EVENTS (Enhanced)
-- =====================================================

CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    google_event_id VARCHAR(255) UNIQUE NOT NULL,
    business_context_id UUID REFERENCES business_contexts(id),
    calendar_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    location VARCHAR(500),
    start_time TIMESTAMP WITH TIME ZONE NOT NULL,
    end_time TIMESTAMP WITH TIME ZONE NOT NULL,
    is_all_day BOOLEAN DEFAULT false,
    attendees JSONB,

    -- New: AI enhancements
    ai_notes TEXT,
    ai_prep_checklist JSONB,
    ai_follow_up TEXT,
    auto_generated BOOLEAN DEFAULT false,

    -- New: Links
    related_task_id UUID REFERENCES tasks(id),
    related_booking_id UUID,
    related_order_id UUID,

    -- Reminders
    reminder_sent BOOLEAN DEFAULT false,
    prep_reminder_sent BOOLEAN DEFAULT false,

    status VARCHAR(20) DEFAULT 'confirmed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_calendar_google_id ON calendar_events(google_event_id);
CREATE INDEX idx_calendar_time_range ON calendar_events(start_time, end_time);

-- =====================================================
-- DJ BOOKINGS (Enhanced with automation)
-- =====================================================

CREATE TABLE IF NOT EXISTS dj_bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),

    -- Event details
    event_type VARCHAR(100),
    event_date DATE NOT NULL,
    event_start_time TIME,
    event_end_time TIME,
    venue_name VARCHAR(255),
    venue_address TEXT,
    guest_count INTEGER,

    -- Status pipeline
    status VARCHAR(50) DEFAULT 'inquiry',
    status_history JSONB, -- Track status changes with timestamps

    -- Pricing
    quoted_price DECIMAL(10, 2),
    final_price DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_paid_date DATE,
    balance_amount DECIMAL(10, 2),
    balance_paid_date DATE,
    discount_applied DECIMAL(10, 2) DEFAULT 0,
    discount_reason VARCHAR(255),

    -- Requirements
    equipment_needed TEXT[],
    special_requests TEXT,
    music_preferences TEXT,
    must_play_songs TEXT[],
    do_not_play_songs TEXT[],

    -- Documents
    contract_sent BOOLEAN DEFAULT false,
    contract_signed BOOLEAN DEFAULT false,
    contract_url TEXT,
    invoice_url TEXT,

    -- New: Auto-response
    inquiry_email_id UUID REFERENCES emails(id),
    quote_auto_generated BOOLEAN DEFAULT false,
    quote_sent_at TIMESTAMP WITH TIME ZONE,
    quote_approved_by UUID REFERENCES users(id),

    -- Links
    calendar_event_id UUID REFERENCES calendar_events(id),

    -- Source
    source VARCHAR(100),
    referral_source VARCHAR(255),

    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_dj_bookings_customer ON dj_bookings(customer_id);
CREATE INDEX idx_dj_bookings_status ON dj_bookings(status);
CREATE INDEX idx_dj_bookings_date ON dj_bookings(event_date);

-- =====================================================
-- WOODY'S ORDERS (Enhanced with automation)
-- =====================================================

CREATE TABLE IF NOT EXISTS woodys_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_reference VARCHAR(50) UNIQUE NOT NULL,
    customer_id UUID REFERENCES customers(id),

    -- Product details
    product_type VARCHAR(100),
    product_description TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    design_file_url TEXT,
    material VARCHAR(100),
    dimensions VARCHAR(100),

    -- Customization
    personalization_text TEXT,
    color_finish VARCHAR(100),
    additional_options JSONB,

    -- Status pipeline
    status VARCHAR(50) DEFAULT 'received',
    status_history JSONB,

    -- Pricing
    quoted_price DECIMAL(10, 2),
    final_price DECIMAL(10, 2),
    material_cost DECIMAL(10, 2),
    labor_cost DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_paid_date DATE,
    balance_amount DECIMAL(10, 2),
    balance_paid_date DATE,

    -- Timeline
    order_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    production_date DATE,
    completion_date DATE,
    shipped_date DATE,
    delivered_date DATE,

    -- Production
    estimated_production_hours DECIMAL(5, 2),
    actual_production_hours DECIMAL(5, 2),
    production_notes TEXT,
    quality_check_passed BOOLEAN,

    -- Delivery
    delivery_method VARCHAR(50),
    delivery_address TEXT,
    tracking_number VARCHAR(100),

    -- New: Auto-confirmation
    inquiry_email_id UUID REFERENCES emails(id),
    confirmation_auto_generated BOOLEAN DEFAULT false,
    confirmation_sent_at TIMESTAMP WITH TIME ZONE,

    -- Links
    calendar_event_id UUID REFERENCES calendar_events(id),

    source VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_woodys_orders_customer ON woodys_orders(customer_id);
CREATE INDEX idx_woodys_orders_status ON woodys_orders(status);
CREATE INDEX idx_woodys_orders_due ON woodys_orders(due_date);

-- =====================================================
-- BMF WORK LOG (Enhanced)
-- =====================================================

CREATE TABLE IF NOT EXISTS bmf_work_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    work_date DATE NOT NULL,
    hours_worked DECIMAL(4, 2) NOT NULL,
    project_name VARCHAR(255),
    project_code VARCHAR(50),
    task_description TEXT NOT NULL,
    deliverables TEXT,

    -- Status
    status VARCHAR(50) DEFAULT 'logged',

    -- Invoicing
    invoice_reference VARCHAR(50),
    invoice_date DATE,
    invoice_amount DECIMAL(10, 2),
    hourly_rate DECIMAL(10, 2),
    paid_date DATE,

    -- New: Time tracking
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    break_minutes INTEGER DEFAULT 0,

    -- New: Auto-log from calendar
    auto_logged_from_calendar BOOLEAN DEFAULT false,
    calendar_event_id UUID REFERENCES calendar_events(id),

    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bmf_work_date ON bmf_work_log(work_date DESC);
CREATE INDEX idx_bmf_status ON bmf_work_log(status);
CREATE INDEX idx_bmf_project ON bmf_work_log(project_name);

-- =====================================================
-- AI DECISIONS LOG (Enhanced with feedback loop)
-- =====================================================

CREATE TABLE IF NOT EXISTS ai_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Agent info
    agent_role VARCHAR(100) NOT NULL,
    agent_version VARCHAR(20),

    -- Decision
    decision_type VARCHAR(100) NOT NULL,
    input_data JSONB,
    ai_model VARCHAR(50),
    ai_output TEXT,
    confidence_score DECIMAL(3, 2),

    -- Tools used
    tools_called JSONB, -- List of tools/functions called

    -- User feedback
    user_approved BOOLEAN,
    user_feedback TEXT,
    user_correction TEXT,

    -- New: Learning
    was_correct BOOLEAN,
    improvement_suggestion TEXT,
    added_to_training BOOLEAN DEFAULT false,

    -- Performance
    execution_time_ms INTEGER,
    api_tokens_used INTEGER,
    api_cost_estimate DECIMAL(10, 6),

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ai_decisions_agent ON ai_decisions(agent_role);
CREATE INDEX idx_ai_decisions_type ON ai_decisions(decision_type);
CREATE INDEX idx_ai_decisions_feedback ON ai_decisions(user_approved, was_correct);

-- =====================================================
-- AGENT TASKS (New - Background agent tasks)
-- =====================================================

CREATE TABLE IF NOT EXISTS agent_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name VARCHAR(100) NOT NULL,
    task_type VARCHAR(100) NOT NULL, -- 'draft_email', 'schedule_reminder', 'analyze_trends'

    -- Task details
    description TEXT,
    input_data JSONB,

    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'failed', 'requires_approval'

    -- Execution
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    result_data JSONB,
    error_message TEXT,

    -- Approval workflow
    requires_approval BOOLEAN DEFAULT true,
    approved_by UUID REFERENCES users(id),
    approved_at TIMESTAMP WITH TIME ZONE,
    approval_status VARCHAR(20), -- 'pending', 'approved', 'rejected'

    -- Priority
    priority INTEGER DEFAULT 5, -- 1-10
    scheduled_for TIMESTAMP WITH TIME ZONE,

    -- Retry logic
    retry_count INTEGER DEFAULT 0,
    max_retries INTEGER DEFAULT 3,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_agent_tasks_status ON agent_tasks(status);
CREATE INDEX idx_agent_tasks_agent ON agent_tasks(agent_name);
CREATE INDEX idx_agent_tasks_scheduled ON agent_tasks(scheduled_for);

-- =====================================================
-- EMAIL TEMPLATES (New - For auto-responses)
-- =====================================================

CREATE TABLE IF NOT EXISTS email_templates (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Template info
    name VARCHAR(255) NOT NULL,
    template_type VARCHAR(100), -- 'dj_inquiry', 'order_confirmation', 'quote', etc.

    -- Content
    subject_template TEXT,
    body_template TEXT,
    variables JSONB, -- List of variables: {name, description, default}

    -- Usage
    usage_count INTEGER DEFAULT 0,
    last_used TIMESTAMP WITH TIME ZONE,

    -- Conditions for auto-use
    auto_use_conditions JSONB,
    requires_approval BOOLEAN DEFAULT true,

    -- Version control
    version INTEGER DEFAULT 1,
    is_active BOOLEAN DEFAULT true,

    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_email_templates_business ON email_templates(business_context_id);
CREATE INDEX idx_email_templates_type ON email_templates(template_type);

-- =====================================================
-- BUSINESS METRICS (Enhanced with predictions)
-- =====================================================

CREATE TABLE IF NOT EXISTS business_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    metric_date DATE NOT NULL,
    metric_type VARCHAR(100) NOT NULL,
    metric_value DECIMAL(12, 2),
    metric_unit VARCHAR(50),

    -- Comparisons
    comparison_previous_period DECIMAL(12, 2),
    comparison_same_period_last_year DECIMAL(12, 2),

    -- New: Predictions
    predicted_next_period DECIMAL(12, 2),
    prediction_confidence DECIMAL(3, 2),

    -- Aggregation level
    aggregation_period VARCHAR(20), -- 'daily', 'weekly', 'monthly', 'quarterly', 'yearly'

    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_business_metrics_business ON business_metrics(business_context_id);
CREATE INDEX idx_business_metrics_date ON business_metrics(metric_date DESC);
CREATE INDEX idx_business_metrics_type ON business_metrics(metric_type);
CREATE UNIQUE INDEX idx_business_metrics_unique ON business_metrics(business_context_id, metric_date, metric_type, aggregation_period);

-- =====================================================
-- INSIGHTS (New - AI-generated insights)
-- =====================================================

CREATE TABLE IF NOT EXISTS insights (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Insight details
    insight_type VARCHAR(100), -- 'trend', 'anomaly', 'opportunity', 'risk', 'recommendation'
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,

    -- Severity/importance
    importance_score INTEGER, -- 1-10
    impact_level VARCHAR(20), -- 'low', 'medium', 'high', 'critical'

    -- Supporting data
    supporting_data JSONB,
    related_metrics JSONB,

    -- Actions
    suggested_actions JSONB, -- Array of suggested actions
    action_taken TEXT,
    action_taken_at TIMESTAMP WITH TIME ZONE,

    -- Lifecycle
    status VARCHAR(50) DEFAULT 'new', -- 'new', 'acknowledged', 'acted_on', 'dismissed'
    dismissed_reason TEXT,

    -- User interaction
    viewed_by UUID[] DEFAULT '{}',
    acknowledged_by UUID REFERENCES users(id),
    acknowledged_at TIMESTAMP WITH TIME ZONE,

    -- Timing
    valid_from TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    valid_until TIMESTAMP WITH TIME ZONE,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_insights_business ON insights(business_context_id);
CREATE INDEX idx_insights_status ON insights(status);
CREATE INDEX idx_insights_importance ON insights(importance_score DESC);

-- =====================================================
-- VOICE MESSAGES (New - For voice interface)
-- =====================================================

CREATE TABLE IF NOT EXISTS voice_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),

    -- Telegram file
    telegram_file_id VARCHAR(255),
    file_url TEXT,
    duration_seconds INTEGER,

    -- Transcription
    transcript TEXT,
    transcription_confidence DECIMAL(3, 2),
    language VARCHAR(10),

    -- Processing
    intent VARCHAR(100),
    business_context_id UUID REFERENCES business_contexts(id),

    -- Response
    response_text TEXT,
    response_voice_url TEXT,

    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_voice_messages_user ON voice_messages(user_id);

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply to all relevant tables
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN
        SELECT table_name
        FROM information_schema.columns
        WHERE column_name = 'updated_at'
        AND table_schema = 'public'
    LOOP
        EXECUTE format('
            DROP TRIGGER IF EXISTS update_%I_updated_at ON %I;
            CREATE TRIGGER update_%I_updated_at
                BEFORE UPDATE ON %I
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
        ', t, t, t, t);
    END LOOP;
END;
$$;

-- Auto-generate order references
CREATE OR REPLACE FUNCTION generate_order_reference()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_reference IS NULL THEN
        NEW.order_reference := 'WC' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('woodys_order_seq')::TEXT, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE IF NOT EXISTS woodys_order_seq START 1;

DROP TRIGGER IF EXISTS generate_woodys_order_reference ON woodys_orders;
CREATE TRIGGER generate_woodys_order_reference
    BEFORE INSERT ON woodys_orders
    FOR EACH ROW
    EXECUTE FUNCTION generate_order_reference();

-- Auto-generate booking references
CREATE OR REPLACE FUNCTION generate_booking_reference()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.booking_reference IS NULL THEN
        NEW.booking_reference := 'DJ' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('dj_booking_seq')::TEXT, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE IF NOT EXISTS dj_booking_seq START 1;

DROP TRIGGER IF EXISTS generate_dj_booking_reference ON dj_bookings;
CREATE TRIGGER generate_dj_booking_reference
    BEFORE INSERT ON dj_bookings
    FOR EACH ROW
    EXECUTE FUNCTION generate_booking_reference();

-- Track customer activity
CREATE OR REPLACE FUNCTION update_customer_last_contact()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE customers
    SET last_contact_date = NOW()
    WHERE id = NEW.customer_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_customer_contact_dj ON dj_bookings;
CREATE TRIGGER update_customer_contact_dj
    AFTER INSERT OR UPDATE ON dj_bookings
    FOR EACH ROW
    WHEN (NEW.customer_id IS NOT NULL)
    EXECUTE FUNCTION update_customer_last_contact();

DROP TRIGGER IF EXISTS update_customer_contact_woodys ON woodys_orders;
CREATE TRIGGER update_customer_contact_woodys
    AFTER INSERT OR UPDATE ON woodys_orders
    FOR EACH ROW
    WHEN (NEW.customer_id IS NOT NULL)
    EXECUTE FUNCTION update_customer_last_contact();

-- =====================================================
-- USEFUL VIEWS
-- =====================================================

-- Active pipeline overview
CREATE OR REPLACE VIEW active_pipeline AS
SELECT
    'DJ Booking' as item_type,
    bc.display_name as business,
    dj.booking_reference as reference,
    dj.status,
    dj.event_date::text as key_date,
    dj.quoted_price as value,
    c.name as customer_name
FROM dj_bookings dj
JOIN business_contexts bc ON bc.name = 'dj-business'
LEFT JOIN customers c ON dj.customer_id = c.id
WHERE dj.status NOT IN ('completed', 'cancelled')
UNION ALL
SELECT
    'Woodys Order' as item_type,
    bc.display_name as business,
    wo.order_reference as reference,
    wo.status,
    wo.due_date::text as key_date,
    wo.quoted_price as value,
    c.name as customer_name
FROM woodys_orders wo
JOIN business_contexts bc ON bc.name = 'woodys-creations'
LEFT JOIN customers c ON wo.customer_id = c.id
WHERE wo.status NOT IN ('delivered', 'cancelled')
ORDER BY key_date ASC;

-- Today's action items
CREATE OR REPLACE VIEW todays_actions AS
SELECT
    'Email' as action_type,
    bc.emoji || ' ' || e.subject as title,
    e.action_needed as action,
    e.priority,
    bc.display_name as business
FROM emails e
JOIN business_contexts bc ON e.business_context_id = bc.id
WHERE e.is_processed = false
UNION ALL
SELECT
    'Task' as action_type,
    bc.emoji || ' ' || t.title as title,
    t.status as action,
    t.priority,
    bc.display_name as business
FROM tasks t
JOIN business_contexts bc ON t.business_context_id = bc.id
WHERE t.status IN ('pending', 'in_progress')
  AND (t.due_date IS NULL OR DATE(t.due_date) <= CURRENT_DATE + INTERVAL '7 days')
ORDER BY
    CASE priority
        WHEN 'urgent' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        ELSE 4
    END;

-- =====================================================
-- SEED DEFAULT DATA
-- =====================================================

-- Insert/update business contexts with enhanced data
INSERT INTO business_contexts (name, display_name, description, color, emoji, gmail_label, business_type) VALUES
    ('personal', 'Personal', 'Personal life management', 'blue', '👤', 'Personal', 'personal'),
    ('woodys-creations', 'Woody''s Creations UK', 'Laser-cut gifts and signs manufacturing', 'green', '🏢', 'WoodysCreations', 'product'),
    ('dj-business', 'DJ Business', 'Event DJ services', 'red', '🎵', 'DJ-Business', 'service'),
    ('bmf-work', 'BMF Work', 'Contract work for Brian Farmer', 'orange', '💼', 'BMF-Work', 'contract'),
    ('pub-future', 'Pub', 'Future pub landlord duties', 'purple', '🍺', 'Pub-Future', 'service')
ON CONFLICT (name) DO UPDATE SET
    display_name = EXCLUDED.display_name,
    description = EXCLUDED.description,
    business_type = EXCLUDED.business_type;

-- Insert default knowledge base entries
INSERT INTO knowledge_base (business_context_id, title, content, content_type, category) VALUES
(
    (SELECT id FROM business_contexts WHERE name = 'dj-business'),
    'Standard DJ Pricing',
    'Standard rates: £300 for 4 hours, £500 for full evening (8 hours). Wedding premium: +£100. Equipment included: CDJ setup, speakers, basic lighting. Travel over 30 miles: +£50.',
    'price',
    'pricing'
),
(
    (SELECT id FROM business_contexts WHERE name = 'dj-business'),
    'Booking Terms',
    'Deposit: 25% upfront to secure booking. Balance due 1 week before event. Cancellation: Full refund if cancelled 30+ days before. 50% refund if 14-29 days. No refund within 14 days.',
    'policy',
    'terms'
),
(
    (SELECT id FROM business_contexts WHERE name = 'woodys-creations'),
    'Production Lead Times',
    'Standard signs: 5-7 business days. Complex/large orders: 10-14 days. Rush orders: +50% fee for 2-3 day turnaround (if capacity allows).',
    'procedure',
    'production'
),
(
    (SELECT id FROM business_contexts WHERE name = 'woodys-creations'),
    'Materials and Pricing',
    'Oak: Premium option, £X per item base. Pine: Standard option, £Y per item base. Acrylic: Modern option, £Z per item base. Price includes design, cutting, finishing.',
    'price',
    'materials'
);

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Enhanced AIPA Database Schema V2 created successfully!';
    RAISE NOTICE '';
    RAISE NOTICE 'New features:';
    RAISE NOTICE '✅ Vector search enabled (pgvector)';
    RAISE NOTICE '✅ Agent memory system';
    RAISE NOTICE '✅ RAG knowledge base';
    RAISE NOTICE '✅ Customer database';
    RAISE NOTICE '✅ Auto-response tracking';
    RAISE NOTICE '✅ Background agent tasks';
    RAISE NOTICE '✅ Email templates';
    RAISE NOTICE '✅ Business insights';
    RAISE NOTICE '✅ Voice message support';
    RAISE NOTICE '';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Enable pgvector extension in Supabase';
    RAISE NOTICE '2. Generate embeddings for existing data';
    RAISE NOTICE '3. Deploy MCP servers';
    RAISE NOTICE '4. Set up CrewAI agents';
END $$;
