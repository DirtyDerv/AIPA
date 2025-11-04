-- =====================================================
-- AI Personal Assistant (AIPA) - Database Schema V2 (Supabase Compatible)
-- Simplified version for initial setup
-- =====================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- BUSINESS CONTEXTS
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
    business_type VARCHAR(50),
    timezone VARCHAR(50) DEFAULT 'Europe/London',
    working_hours JSONB,
    agent_config JSONB,
    automation_rules JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- USERS
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
    preferences JSONB DEFAULT '{
        "briefing_time": "08:00",
        "notification_urgency": ["urgent", "high"],
        "work_schedule": {},
        "communication_style": "professional",
        "auto_approve_threshold": 0.95
    }'::jsonb,
    long_term_memory JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CONVERSATIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    message_text TEXT NOT NULL,
    message_type VARCHAR(20) NOT NULL,
    intent VARCHAR(100),
    metadata JSONB,
    processing_agent VARCHAR(100),
    agent_confidence DECIMAL(3, 2),
    thread_id UUID,
    parent_message_id UUID REFERENCES conversations(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TASKS
-- =====================================================

CREATE TABLE IF NOT EXISTS tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority VARCHAR(20) DEFAULT 'medium',
    due_date TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    estimated_duration INTEGER,
    tags TEXT[],
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- EMAILS
-- =====================================================

CREATE TABLE IF NOT EXISTS emails (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    gmail_message_id VARCHAR(255) UNIQUE NOT NULL,
    gmail_thread_id VARCHAR(255),
    subject TEXT,
    sender_email VARCHAR(255),
    sender_name VARCHAR(255),
    body_text TEXT,
    body_html TEXT,
    received_at TIMESTAMP WITH TIME ZONE,
    classification JSONB,
    labels TEXT[],
    is_processed BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- CALENDAR EVENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS calendar_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    google_event_id VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(200),
    description TEXT,
    start_time TIMESTAMP WITH TIME ZONE,
    end_time TIMESTAMP WITH TIME ZONE,
    location VARCHAR(255),
    attendees JSONB,
    event_type VARCHAR(50),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- BOOKINGS
-- =====================================================

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    client_name VARCHAR(200),
    client_email VARCHAR(255),
    client_phone VARCHAR(50),
    event_date DATE,
    event_time TIME,
    event_duration INTEGER,
    venue_name VARCHAR(200),
    venue_address TEXT,
    booking_type VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pending',
    total_amount DECIMAL(10, 2),
    deposit_amount DECIMAL(10, 2),
    deposit_paid BOOLEAN DEFAULT false,
    special_requests TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- ORDERS
-- =====================================================

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    business_context_id UUID REFERENCES business_contexts(id),
    order_number VARCHAR(50) UNIQUE,
    customer_name VARCHAR(200),
    customer_email VARCHAR(255),
    customer_phone VARCHAR(50),
    product_details JSONB,
    total_amount DECIMAL(10, 2),
    status VARCHAR(50) DEFAULT 'pending',
    payment_status VARCHAR(50) DEFAULT 'pending',
    delivery_address TEXT,
    special_instructions TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- KNOWLEDGE BASE
-- =====================================================

CREATE TABLE IF NOT EXISTS knowledge_base (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    content_type VARCHAR(50),
    category VARCHAR(100),
    tags TEXT[],
    is_active BOOLEAN DEFAULT true,
    access_level VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- BUSINESS METRICS
-- =====================================================

CREATE TABLE IF NOT EXISTS business_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_context_id UUID REFERENCES business_contexts(id),
    metric_name VARCHAR(100) NOT NULL,
    metric_value DECIMAL(15, 4),
    metric_unit VARCHAR(50),
    period_start DATE,
    period_end DATE,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- SYSTEM SETTINGS
-- =====================================================

CREATE TABLE IF NOT EXISTS system_settings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    setting_key VARCHAR(100) UNIQUE NOT NULL,
    setting_value JSONB,
    description TEXT,
    is_encrypted BOOLEAN DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_conversations_context ON conversations(business_context_id);
CREATE INDEX IF NOT EXISTS idx_conversations_thread ON conversations(thread_id);
CREATE INDEX IF NOT EXISTS idx_tasks_user ON tasks(user_id);
CREATE INDEX IF NOT EXISTS idx_tasks_context ON tasks(business_context_id);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_emails_user ON emails(user_id);
CREATE INDEX IF NOT EXISTS idx_emails_context ON emails(business_context_id);
CREATE INDEX IF NOT EXISTS idx_emails_processed ON emails(is_processed);

-- =====================================================
-- SEED DEFAULT DATA
-- =====================================================

-- Insert business contexts
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

-- Insert some initial knowledge base entries
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
    'Product Categories',
    'Main products: House signs (oak/slate), garden signs, wedding gifts, Christmas decorations. Custom laser engraving available. Materials: Oak, birch plywood, acrylic, slate.',
    'product',
    'catalog'
);

-- Success message
SELECT 'AIPA Database Schema Created Successfully!' as status;