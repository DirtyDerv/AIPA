#!/usr/bin/env python3
"""
Setup Supabase Database for AIPA System
This script creates the database schema and initial data
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from urllib.parse import urlparse
import sys

# Your Supabase credentials
SUPABASE_URL = "https://neoeoabqcfpopzkwvcxq.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5lb2VvYWJxY2Zwb3B6a3d2Y3hxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjIwMDY2MTAsImV4cCI6MjA3NzU4MjYxMH0.wqHy-uwc57QMOxxwJBGVupLDvnUCWQbP-eCwlXRT6Ck"

def get_db_connection():
    """Create database connection to Supabase"""
    # Parse the Supabase URL to get connection details
    parsed = urlparse(SUPABASE_URL)
    host = parsed.hostname
    
    # Supabase connection details
    # Note: For the schema setup, we need the service role key, not anon key
    # But let's try with the database URL first
    
    # Extract the project ref from URL
    project_ref = host.split('.')[0]
    
    # Supabase PostgreSQL connection
    db_host = f"db.{project_ref}.supabase.co"
    
    print(f"Connecting to: {db_host}")
    print("Note: You'll need to provide your database password")
    
    # For now, let's create the SQL file to run manually
    return None

def create_schema_file():
    """Read the schema file and prepare it for execution"""
    try:
        with open('database/schema-v2-enhanced.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("✅ Schema file read successfully")
        print(f"Schema size: {len(schema_sql)} characters")
        
        # Write a simplified setup script
        with open('supabase_setup.sql', 'w', encoding='utf-8') as f:
            f.write(schema_sql)
            
            # Add initial business contexts
            f.write("""

-- Insert initial business contexts
INSERT INTO business_contexts (name, display_name, description, color, emoji, gmail_label, business_type) VALUES
('personal', 'Personal', 'Personal tasks and communications', 'blue', '👤', 'Personal', 'personal'),
('woodys-creations', 'Woodys Creations', 'Product design and manufacturing business', 'green', '🏢', 'WoodysCreations', 'product'),
('dj-business', 'DJ Business', 'DJ services and music events', 'red', '🎵', 'DJ-Business', 'service'),
('bmf-work', 'BMF Work', 'Contract work and consulting', 'orange', '💼', 'BMF-Work', 'contract'),
('pub-future', 'Pub Management', 'Future pub business planning', 'purple', '🍺', 'Pub-Future', 'service')
ON CONFLICT (name) DO NOTHING;

""")
        
        print("✅ Setup SQL file created: supabase_setup.sql")
        return True
        
    except FileNotFoundError:
        print("❌ Schema file not found: database/schema-v2-enhanced.sql")
        return False
    except Exception as e:
        print(f"❌ Error creating schema file: {e}")
        return False

def main():
    print("🚀 AIPA Database Setup")
    print("=" * 50)
    
    # Create the setup file
    if create_schema_file():
        print("\n📋 Next Steps:")
        print("1. Go to your Supabase dashboard: https://supabase.com/dashboard")
        print("2. Open your project: neoeoabqcfpopzkwvcxq")
        print("3. Go to SQL Editor")
        print("4. Copy and paste the contents of 'supabase_setup.sql'")
        print("5. Run the SQL to create your database schema")
        print("\nOR")
        print("6. Provide your database password and I'll set it up automatically")
        
        # Try to get database password for automatic setup
        try:
            password = input("\nEnter your Supabase database password (or press Enter to skip): ").strip()
            if password:
                setup_database_automatic(password)
        except KeyboardInterrupt:
            print("\n\n✅ Manual setup files created. Follow the steps above.")
    
def setup_database_automatic(password):
    """Attempt automatic database setup with password"""
    try:
        parsed = urlparse(SUPABASE_URL)
        project_ref = parsed.hostname.split('.')[0]
        db_host = f"db.{project_ref}.supabase.co"
        
        print(f"Connecting to database: {db_host}")
        
        conn = psycopg2.connect(
            host=db_host,
            port=5432,
            database="postgres",
            user="postgres",
            password=password,
            sslmode="require"
        )
        
        cursor = conn.cursor()
        
        # Read and execute schema
        with open('supabase_setup.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("Executing schema...")
        cursor.execute(schema_sql)
        conn.commit()
        
        print("✅ Database schema created successfully!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Automatic setup failed: {e}")
        print("Please use the manual setup method instead.")

if __name__ == "__main__":
    main()