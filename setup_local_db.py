"""
Setup Local Database

Creates the finishing_labs_erp database and runs the initial schema migration.
Run this once to set up your local development database.
"""
import psycopg
import getpass
import sys
from pathlib import Path


def setup_database():
    """Create database and run initial schema"""
    print("=== Local Database Setup ===\n")
    
    # Get PostgreSQL credentials
    user = input("PostgreSQL username (default: postgres): ").strip() or "postgres"
    password = getpass.getpass("PostgreSQL password: ")
    host = input("PostgreSQL host (default: localhost): ").strip() or "localhost"
    port = input("PostgreSQL port (default: 5432): ").strip() or "5432"
    
    db_name = "finishing_labs_erp"
    
    try:
        # Connect to postgres database to create our database
        print(f"\nConnecting to PostgreSQL...")
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/postgres"
        conn = psycopg.connect(conn_string, autocommit=True)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", [db_name])
        exists = cursor.fetchone()
        
        if exists:
            print(f"✓ Database '{db_name}' already exists")
            recreate = input("Do you want to drop and recreate it? (y/N): ").strip().lower()
            if recreate == 'y':
                cursor.execute(f"DROP DATABASE {db_name}")
                print(f"✓ Dropped existing database")
                cursor.execute(f"CREATE DATABASE {db_name}")
                print(f"✓ Created database '{db_name}'")
            else:
                print("Skipping database creation...")
        else:
            cursor.execute(f"CREATE DATABASE {db_name}")
            print(f"✓ Created database '{db_name}'")
        
        cursor.close()
        conn.close()
        
        # Connect to new database and run migration
        print(f"\nRunning initial schema migration...")
        conn_string = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
        conn = psycopg.connect(conn_string)
        cursor = conn.cursor()
        
        # Read and execute migration
        migration_file = Path(__file__).parent / "migrations" / "001_initial_schema.sql"
        if not migration_file.exists():
            print(f"✗ Migration file not found: {migration_file}")
            sys.exit(1)
        
        sql = migration_file.read_text()
        cursor.execute(sql)
        conn.commit()
        
        print("✓ Schema migration completed")
        
        # Verify tables created
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cursor.fetchall()
        
        print(f"\n✓ Created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        cursor.close()
        conn.close()
        
        print(f"\n✅ Local database setup complete!")
        print(f"\nConnection details for .env file:")
        print(f"  DB_NAME={db_name}")
        print(f"  DB_USER={user}")
        print(f"  DB_PASSWORD={password}")
        print(f"  DB_HOST={host}")
        print(f"  DB_PORT={port}")
        
    except psycopg.OperationalError as e:
        print(f"\n✗ Connection failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Is PostgreSQL running?")
        print("  2. Are your credentials correct?")
        print("  3. Does the user have permission to create databases?")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    setup_database()
