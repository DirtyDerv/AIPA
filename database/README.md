# Database Schema

## Files
- `supabase_schema.sql` - Complete database schema for AIPA system
- `supabase_setup.sql` - Additional setup scripts (if exists)

## Overview
The AIPA database supports multiple business contexts with the following main tables:

### Core Tables
- **business_contexts** - Business context definitions (Personal, Woody's Creations, DJ, BMF, etc.)
- **users** - User accounts and preferences
- **conversations** - All chat interactions and messages
- **tasks** - Task management across all contexts
- **emails** - Gmail integration and processing
- **calendar_events** - Google Calendar integration

### Business-Specific Tables
- **bookings** - DJ business booking management
- **orders** - Woody's Creations order processing
- **knowledge_base** - Context-specific information storage
- **business_metrics** - Performance tracking
- **system_settings** - Configuration storage

## Setup
1. Create new Supabase project
2. Run `supabase_schema.sql` in SQL editor
3. Configure Row Level Security policies as needed
4. Update connection details in `config/CREDENTIALS.md`

## Features
- UUID primary keys for all tables
- JSONB fields for flexible metadata storage
- Proper foreign key relationships
- Indexed columns for performance
- Pre-seeded business contexts and knowledge base