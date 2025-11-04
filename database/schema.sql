-- =====================================================
-- AI Personal Assistant (AIPA) - Database Schema
-- Supabase PostgreSQL Database
-- Version: 1.0.0
-- =====================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- BUSINESS CONTEXTS TABLE
-- Stores the different business/personal contexts
-- =====================================================

CREATE TABLE business_contexts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    display_name VARCHAR(100) NOT NULL,
    description TEXT,
    color VARCHAR(20), -- For calendar color coding
    emoji VARCHAR(10), -- For Telegram display
    gmail_label VARCHAR(100), -- Gmail label name
    calendar_id VARCHAR(255), -- Google Calendar ID
    drive_folder_id VARCHAR(255), -- Google Drive folder ID
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default business contexts
INSERT INTO business_contexts (name, display_name, description, color, emoji, gmail_label) VALUES
    ('personal', 'Personal', 'Personal life management', 'blue', '👤', 'Personal'),
    ('woodys-creations', 'Woody''s Creations UK', 'Laser-cut gifts and signs manufacturing', 'green', '🏢', 'WoodysCreations'),
    ('dj-business', 'DJ Business', 'Event DJ services', 'red', '🎵', 'DJ-Business'),
    ('bmf-work', 'BMF Work', 'Contract work for Brian Farmer', 'orange', '💼', 'BMF-Work'),
    ('pub-future', 'Pub', 'Future pub landlord duties', 'purple', '🍺', 'Pub-Future');

-- =====================================================
-- USERS TABLE
-- Stores system users (Woody, Angie, etc.)
-- =====================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    telegram_id BIGINT UNIQUE NOT NULL,
    telegram_username VARCHAR(100),
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    role VARCHAR(50) DEFAULT 'user', -- 'admin', 'user', 'viewer'
    allowed_contexts TEXT[], -- Array of context IDs user can access
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONVERSATIONS TABLE
-- Stores conversation history for context awareness
-- =====================================================

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL, -- 'user', 'assistant', 'system'
    intent VARCHAR(100), -- Detected user intent
    metadata JSONB, -- Additional data (attachments, buttons clicked, etc.)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_context ON conversations(business_context_id);
CREATE INDEX idx_conversations_created ON conversations(created_at DESC);

-- =====================================================
-- TASKS TABLE
-- Manages tasks and todos across all contexts
-- =====================================================

CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    user_id UUID REFERENCES users(id),
    title VARCHAR(255) NOT NULL,
    description TEXT,
    priority VARCHAR(20) DEFAULT 'medium', -- 'low', 'medium', 'high', 'urgent'
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'in_progress', 'completed', 'cancelled'
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_by_ai BOOLEAN DEFAULT false,
    ai_suggested_reason TEXT, -- Why AI suggested this task
    parent_task_id UUID REFERENCES tasks(id), -- For subtasks
    metadata JSONB, -- Tags, links, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_tasks_context ON tasks(business_context_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_tasks_priority ON tasks(priority);

-- =====================================================
-- EMAILS TABLE
-- Processed emails with AI analysis
-- =====================================================

CREATE TABLE emails (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    gmail_id VARCHAR(255) UNIQUE NOT NULL,
    gmail_thread_id VARCHAR(255),
    business_context_id UUID REFERENCES business_contexts(id),
    subject TEXT,
    from_email VARCHAR(255),
    from_name VARCHAR(255),
    to_email VARCHAR(255),
    received_at TIMESTAMP WITH TIME ZONE,
    priority VARCHAR(20), -- 'low', 'medium', 'high', 'urgent'
    ai_summary TEXT, -- AI-generated summary
    action_needed VARCHAR(50), -- 'reply', 'schedule', 'file', 'none', 'forward'
    sentiment VARCHAR(20), -- 'positive', 'neutral', 'negative', 'complaint'
    key_points JSONB, -- Extracted key information
    is_processed BOOLEAN DEFAULT false,
    is_archived BOOLEAN DEFAULT false,
    user_action_taken VARCHAR(100), -- What user did with this email
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_emails_gmail_id ON emails(gmail_id);
CREATE INDEX idx_emails_context ON emails(business_context_id);
CREATE INDEX idx_emails_processed ON emails(is_processed);
CREATE INDEX idx_emails_priority ON emails(priority);
CREATE INDEX idx_emails_received ON emails(received_at DESC);

-- =====================================================
-- CALENDAR EVENTS TABLE
-- Synced calendar events with AI enhancements
-- =====================================================

CREATE TABLE calendar_events (
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
    attendees JSONB, -- Array of attendee objects
    ai_notes TEXT, -- AI-generated prep notes
    ai_follow_up TEXT, -- AI-suggested follow-up actions
    reminder_sent BOOLEAN DEFAULT false,
    status VARCHAR(20) DEFAULT 'confirmed', -- 'confirmed', 'tentative', 'cancelled'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_calendar_google_id ON calendar_events(google_event_id);
CREATE INDEX idx_calendar_context ON calendar_events(business_context_id);
CREATE INDEX idx_calendar_start ON calendar_events(start_time);
CREATE INDEX idx_calendar_end ON calendar_events(end_time);

-- =====================================================
-- DJ BOOKINGS TABLE
-- DJ business specific booking pipeline
-- =====================================================

CREATE TABLE dj_bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    booking_reference VARCHAR(50) UNIQUE NOT NULL,
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    client_phone VARCHAR(50),
    event_type VARCHAR(100), -- 'wedding', 'corporate', 'birthday', 'club', 'other'
    event_date DATE NOT NULL,
    event_start_time TIME,
    event_end_time TIME,
    venue_name VARCHAR(255),
    venue_address TEXT,
    status VARCHAR(50) DEFAULT 'inquiry', -- 'inquiry', 'quoted', 'confirmed', 'deposit_paid', 'completed', 'cancelled'
    quoted_price DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_paid_date DATE,
    balance_amount DECIMAL(10, 2),
    balance_paid_date DATE,
    equipment_needed TEXT[], -- Array of equipment
    special_requests TEXT,
    music_preferences TEXT,
    contract_sent BOOLEAN DEFAULT false,
    contract_signed BOOLEAN DEFAULT false,
    calendar_event_id UUID REFERENCES calendar_events(id),
    notes TEXT,
    source VARCHAR(100), -- 'email', 'phone', 'referral', 'website', 'social_media'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_dj_bookings_status ON dj_bookings(status);
CREATE INDEX idx_dj_bookings_event_date ON dj_bookings(event_date);
CREATE INDEX idx_dj_bookings_client ON dj_bookings(client_name);

-- =====================================================
-- WOODY'S CREATIONS ORDERS TABLE
-- Order management for laser-cut products
-- =====================================================

CREATE TABLE woodys_orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_reference VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(255) NOT NULL,
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    product_type VARCHAR(100), -- 'sign', 'gift', 'custom', 'bulk'
    product_description TEXT NOT NULL,
    quantity INTEGER DEFAULT 1,
    design_file_url TEXT, -- Google Drive link
    material VARCHAR(100), -- 'oak', 'pine', 'acrylic', etc.
    dimensions VARCHAR(100), -- e.g., "30cm x 20cm"
    status VARCHAR(50) DEFAULT 'received', -- 'received', 'in_design', 'approved', 'in_production', 'completed', 'shipped', 'delivered', 'cancelled'
    quoted_price DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_paid_date DATE,
    balance_amount DECIMAL(10, 2),
    balance_paid_date DATE,
    order_date DATE DEFAULT CURRENT_DATE,
    due_date DATE,
    production_date DATE, -- When production scheduled
    completion_date DATE, -- When actually completed
    delivery_method VARCHAR(50), -- 'pickup', 'delivery', 'shipping'
    delivery_address TEXT,
    tracking_number VARCHAR(100),
    calendar_event_id UUID REFERENCES calendar_events(id), -- Link to production time block
    notes TEXT,
    source VARCHAR(100), -- 'email', 'phone', 'etsy', 'facebook', 'website'
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_woodys_orders_status ON woodys_orders(status);
CREATE INDEX idx_woodys_orders_due_date ON woodys_orders(due_date);
CREATE INDEX idx_woodys_orders_customer ON woodys_orders(customer_name);

-- =====================================================
-- BMF WORK LOG TABLE
-- Timesheet and project tracking for BMF contract work
-- =====================================================

CREATE TABLE bmf_work_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    work_date DATE NOT NULL,
    hours_worked DECIMAL(4, 2) NOT NULL,
    project_name VARCHAR(255),
    project_code VARCHAR(50),
    task_description TEXT NOT NULL,
    deliverables TEXT,
    status VARCHAR(50) DEFAULT 'logged', -- 'logged', 'invoiced', 'paid'
    invoice_reference VARCHAR(50),
    invoice_date DATE,
    invoice_amount DECIMAL(10, 2),
    paid_date DATE,
    notes TEXT,
    calendar_event_id UUID REFERENCES calendar_events(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_bmf_work_date ON bmf_work_log(work_date DESC);
CREATE INDEX idx_bmf_status ON bmf_work_log(status);
CREATE INDEX idx_bmf_project ON bmf_work_log(project_name);

-- =====================================================
-- AI DECISIONS LOG TABLE
-- Tracks all AI decisions for transparency and learning
-- =====================================================

CREATE TABLE ai_decisions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    business_context_id UUID REFERENCES business_contexts(id),
    agent_role VARCHAR(100) NOT NULL, -- 'executive_assistant', 'strategist', etc.
    decision_type VARCHAR(100) NOT NULL, -- 'email_classification', 'task_creation', 'calendar_suggestion', etc.
    input_data JSONB, -- What was provided to AI
    ai_model VARCHAR(50), -- 'claude', 'gemini'
    ai_output TEXT, -- AI's response
    confidence_score DECIMAL(3, 2), -- 0.00 to 1.00
    user_approved BOOLEAN, -- Did user approve/accept?
    user_feedback TEXT, -- User's correction or feedback
    execution_time_ms INTEGER, -- How long it took
    api_tokens_used INTEGER, -- Token count for cost tracking
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_ai_decisions_user ON ai_decisions(user_id);
CREATE INDEX idx_ai_decisions_agent ON ai_decisions(agent_role);
CREATE INDEX idx_ai_decisions_type ON ai_decisions(decision_type);
CREATE INDEX idx_ai_decisions_created ON ai_decisions(created_at DESC);

-- =====================================================
-- API USAGE TRACKING TABLE
-- Monitor API usage to stay within free tier limits
-- =====================================================

CREATE TABLE api_usage (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_name VARCHAR(50) NOT NULL, -- 'claude', 'gemini', 'google_calendar', etc.
    endpoint VARCHAR(255),
    request_type VARCHAR(100),
    tokens_used INTEGER,
    cost_estimate DECIMAL(10, 6), -- Estimated cost if applicable
    response_time_ms INTEGER,
    status VARCHAR(20), -- 'success', 'error', 'rate_limited'
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_api_usage_name ON api_usage(api_name);
CREATE INDEX idx_api_usage_date ON api_usage(created_at DESC);

-- View for daily API usage summary
CREATE VIEW daily_api_usage AS
SELECT
    DATE(created_at) as usage_date,
    api_name,
    COUNT(*) as request_count,
    SUM(tokens_used) as total_tokens,
    AVG(response_time_ms) as avg_response_time,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as error_count
FROM api_usage
GROUP BY DATE(created_at), api_name
ORDER BY usage_date DESC, api_name;

-- =====================================================
-- NOTIFICATIONS TABLE
-- Queue for sending notifications to users
-- =====================================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    notification_type VARCHAR(50) NOT NULL, -- 'task_reminder', 'email_urgent', 'calendar_reminder', 'weekly_report'
    priority VARCHAR(20) DEFAULT 'normal', -- 'low', 'normal', 'high', 'urgent'
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    action_buttons JSONB, -- Telegram inline keyboard buttons
    related_entity_type VARCHAR(50), -- 'task', 'email', 'calendar', etc.
    related_entity_id UUID,
    is_sent BOOLEAN DEFAULT false,
    sent_at TIMESTAMP WITH TIME ZONE,
    is_read BOOLEAN DEFAULT false,
    read_at TIMESTAMP WITH TIME ZONE,
    scheduled_for TIMESTAMP WITH TIME ZONE, -- When to send
    expires_at TIMESTAMP WITH TIME ZONE, -- Don't send after this time
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_sent ON notifications(is_sent);
CREATE INDEX idx_notifications_scheduled ON notifications(scheduled_for);

-- =====================================================
-- BUSINESS METRICS TABLE
-- Store calculated business metrics for reporting
-- =====================================================

CREATE TABLE business_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    metric_date DATE NOT NULL,
    metric_type VARCHAR(100) NOT NULL, -- 'revenue', 'bookings', 'orders', 'hours_worked', etc.
    metric_value DECIMAL(12, 2),
    metric_unit VARCHAR(50), -- 'gbp', 'count', 'hours', etc.
    comparison_previous_period DECIMAL(12, 2), -- Percentage change
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_business_metrics_context ON business_metrics(business_context_id);
CREATE INDEX idx_business_metrics_date ON business_metrics(metric_date DESC);
CREATE INDEX idx_business_metrics_type ON business_metrics(metric_type);

-- =====================================================
-- SYSTEM SETTINGS TABLE
-- Configuration and preferences
-- =====================================================

CREATE TABLE system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value TEXT NOT NULL,
    setting_type VARCHAR(50), -- 'string', 'number', 'boolean', 'json'
    description TEXT,
    is_sensitive BOOLEAN DEFAULT false, -- Don't log if true
    updated_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Insert default settings
INSERT INTO system_settings (setting_key, setting_value, setting_type, description) VALUES
    ('daily_briefing_time', '08:00', 'string', 'Time to send daily briefing (HH:MM format)'),
    ('weekly_report_day', 'Sunday', 'string', 'Day of week for weekly business report'),
    ('weekly_report_time', '18:00', 'string', 'Time to send weekly report'),
    ('email_check_interval', '15', 'number', 'Minutes between email checks'),
    ('ai_default_model', 'gemini', 'string', 'Default AI model for simple tasks'),
    ('api_usage_warning_threshold', '80', 'number', 'Percentage of limit to trigger warning'),
    ('conversation_history_days', '90', 'number', 'Days to keep conversation history'),
    ('timezone', 'Europe/London', 'string', 'System timezone');

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply update triggers to relevant tables
CREATE TRIGGER update_business_contexts_updated_at BEFORE UPDATE ON business_contexts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_emails_updated_at BEFORE UPDATE ON emails
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_calendar_events_updated_at BEFORE UPDATE ON calendar_events
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_dj_bookings_updated_at BEFORE UPDATE ON dj_bookings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_woodys_orders_updated_at BEFORE UPDATE ON woodys_orders
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bmf_work_log_updated_at BEFORE UPDATE ON bmf_work_log
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_system_settings_updated_at BEFORE UPDATE ON system_settings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to auto-generate order references
CREATE OR REPLACE FUNCTION generate_order_reference()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.order_reference IS NULL THEN
        NEW.order_reference := 'WC' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('woodys_order_seq')::TEXT, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE woodys_order_seq START 1;

CREATE TRIGGER generate_woodys_order_reference BEFORE INSERT ON woodys_orders
    FOR EACH ROW EXECUTE FUNCTION generate_order_reference();

-- Function to auto-generate booking references
CREATE OR REPLACE FUNCTION generate_booking_reference()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.booking_reference IS NULL THEN
        NEW.booking_reference := 'DJ' || TO_CHAR(NOW(), 'YYYYMMDD') || '-' || LPAD(NEXTVAL('dj_booking_seq')::TEXT, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE SEQUENCE dj_booking_seq START 1;

CREATE TRIGGER generate_dj_booking_reference BEFORE INSERT ON dj_bookings
    FOR EACH ROW EXECUTE FUNCTION generate_booking_reference();

-- =====================================================
-- USEFUL VIEWS FOR REPORTING
-- =====================================================

-- View: Pending tasks by business context
CREATE VIEW pending_tasks_summary AS
SELECT
    bc.display_name as business,
    COUNT(*) as pending_count,
    SUM(CASE WHEN t.priority = 'urgent' THEN 1 ELSE 0 END) as urgent_count,
    SUM(CASE WHEN t.due_date < NOW() THEN 1 ELSE 0 END) as overdue_count
FROM tasks t
JOIN business_contexts bc ON t.business_context_id = bc.id
WHERE t.status IN ('pending', 'in_progress')
GROUP BY bc.display_name
ORDER BY urgent_count DESC, pending_count DESC;

-- View: Unprocessed emails by context
CREATE VIEW unprocessed_emails_summary AS
SELECT
    bc.display_name as business,
    COUNT(*) as unprocessed_count,
    SUM(CASE WHEN e.priority = 'urgent' THEN 1 ELSE 0 END) as urgent_count,
    MAX(e.received_at) as latest_email
FROM emails e
JOIN business_contexts bc ON e.business_context_id = bc.id
WHERE e.is_processed = false
GROUP BY bc.display_name
ORDER BY urgent_count DESC, unprocessed_count DESC;

-- View: Today's calendar events
CREATE VIEW todays_calendar AS
SELECT
    bc.display_name as business,
    bc.emoji,
    ce.title,
    ce.start_time,
    ce.end_time,
    ce.location,
    ce.ai_notes
FROM calendar_events ce
JOIN business_contexts bc ON ce.business_context_id = bc.id
WHERE DATE(ce.start_time) = CURRENT_DATE
    AND ce.status = 'confirmed'
ORDER BY ce.start_time;

-- View: DJ bookings pipeline
CREATE VIEW dj_pipeline_summary AS
SELECT
    status,
    COUNT(*) as count,
    SUM(quoted_price) as total_value,
    SUM(deposit_amount) as total_deposits,
    SUM(balance_amount) as total_balance
FROM dj_bookings
WHERE status != 'cancelled'
GROUP BY status
ORDER BY
    CASE status
        WHEN 'inquiry' THEN 1
        WHEN 'quoted' THEN 2
        WHEN 'confirmed' THEN 3
        WHEN 'deposit_paid' THEN 4
        WHEN 'completed' THEN 5
    END;

-- View: Woody's orders pipeline
CREATE VIEW woodys_pipeline_summary AS
SELECT
    status,
    COUNT(*) as count,
    SUM(quoted_price) as total_value,
    AVG(EXTRACT(DAY FROM (due_date - order_date))) as avg_lead_time_days
FROM woodys_orders
WHERE status != 'cancelled'
GROUP BY status
ORDER BY
    CASE status
        WHEN 'received' THEN 1
        WHEN 'in_design' THEN 2
        WHEN 'approved' THEN 3
        WHEN 'in_production' THEN 4
        WHEN 'completed' THEN 5
        WHEN 'shipped' THEN 6
        WHEN 'delivered' THEN 7
    END;

-- View: BMF monthly hours and invoicing
CREATE VIEW bmf_monthly_summary AS
SELECT
    TO_CHAR(work_date, 'YYYY-MM') as month,
    SUM(hours_worked) as total_hours,
    COUNT(DISTINCT work_date) as days_worked,
    SUM(CASE WHEN status = 'invoiced' OR status = 'paid' THEN invoice_amount ELSE 0 END) as invoiced_amount,
    SUM(CASE WHEN status = 'paid' THEN invoice_amount ELSE 0 END) as paid_amount
FROM bmf_work_log
GROUP BY TO_CHAR(work_date, 'YYYY-MM')
ORDER BY month DESC;

-- =====================================================
-- PERMISSIONS (Supabase RLS)
-- =====================================================
-- Note: In Supabase dashboard, enable Row Level Security
-- and create policies based on user roles

-- Enable RLS on all tables
ALTER TABLE business_contexts ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE tasks ENABLE ROW LEVEL SECURITY;
ALTER TABLE emails ENABLE ROW LEVEL SECURITY;
ALTER TABLE calendar_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE dj_bookings ENABLE ROW LEVEL SECURITY;
ALTER TABLE woodys_orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE bmf_work_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_decisions ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- =====================================================
-- END OF SCHEMA
-- =====================================================

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'AIPA Database Schema created successfully!';
    RAISE NOTICE 'Next steps:';
    RAISE NOTICE '1. Configure Row Level Security policies in Supabase dashboard';
    RAISE NOTICE '2. Run seed-data.sql to add test data (optional)';
    RAISE NOTICE '3. Note your Supabase URL and API key for n8n configuration';
END $$;
