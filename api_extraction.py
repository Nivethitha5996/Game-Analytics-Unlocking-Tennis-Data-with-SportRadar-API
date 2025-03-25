import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
import requests
import sys

# Load environment variables
load_dotenv()

# ----------------------------
# Database Connection Setup
# ----------------------------
def get_db_connection():
    """Create and return a database connection"""
    try:
        engine = create_engine(
            f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
            f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
        )
        # Test the connection with simple query
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("Database connection successful!")
        return engine
    except Exception as e:
        print(f"Failed to connect to database: {e}")
        print("\nTroubleshooting tips:")
        print("1. Verify PostgreSQL is running")
        print("2. Check your credentials in .env file")
        print("3. Ensure database 'sports_data' exists")
        print("4. Verify your PostgreSQL port (default is 5432)")
        return None

# ----------------------------
# API Data Extraction
# ----------------------------
def fetch_competitions():
    """Fetch competition data from SportRadar API"""
    API_KEY = 'BYqjI6IJX4GIONDQFKFNUz5aWxTRY3LYUjJhV6Dr'
    url = f'https://api.sportradar.com/tennis/trial/v3/en/competitions.json?api_key={API_KEY}'
    
    try:
        print("Fetching data from SportRadar API...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('competitions', [])
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return []

# ----------------------------
# Data Transformation
# ----------------------------
def prepare_competitions_data(api_data):
    """
    Transform raw API data to match database schema
    Handles missing columns with default values
    """
    if not api_data:
        return pd.DataFrame()
    
    processed_records = []
    
    for competition in api_data:
        record = {
            'competition_id': competition.get('id'),
            'competition_name': competition.get('name'),
            'parent_id': competition.get('parent_id'),
            'type': competition.get('type', 'tournament'),
            'gender': competition.get('gender', 'mixed'),
            'category_id': competition.get('category_id')
        }
        processed_records.append(record)
    
    return pd.DataFrame(processed_records)

# ----------------------------
# Database Operations
# ----------------------------
def initialize_database(engine):
    """Create tables if they don't exist"""
    with engine.begin() as conn:
        # Create Categories table if not exists
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id VARCHAR(50) PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
        )
        """))
        
        # Create Competitions table if not exists
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id VARCHAR(50) PRIMARY KEY,
            competition_name VARCHAR(100) NOT NULL,
            parent_id VARCHAR(50),
            type VARCHAR(20) NOT NULL,
            gender VARCHAR(10) NOT NULL,
            category_id VARCHAR(50),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
        """))

def insert_data(engine, df, table_name):
    """Insert data into specified table"""
    if df.empty:
        print("No data to insert")
        return False
    
    try:
        with engine.begin() as conn:
            df.to_sql(
                name=table_name,
                con=conn,
                if_exists='append',
                index=False,
                method='multi'
            )
        print(f"Successfully inserted {len(df)} rows into {table_name}")
        return True
    except Exception as e:
        print(f"Error inserting into {table_name}: {str(e)}")
        return False

# ----------------------------
# Main Execution
# ----------------------------
def main():
    # Step 1: Establish database connection
    print("Attempting to connect to database...")
    engine = get_db_connection()
    if not engine:
        sys.exit(1)  # Exit if no connection
    
    # Step 2: Initialize database tables
    print("Initializing database tables...")
    initialize_database(engine)
    
    # Step 3: Fetch data from API
    api_data = fetch_competitions()
    if not api_data:
        print("No data received from API")
        sys.exit(1)
    
    # Step 4: Transform API data
    competitions_df = prepare_competitions_data(api_data)
    print("\nSample of transformed data:")
    print(competitions_df.head())
    
    # Step 5: Insert data into database
    if not competitions_df.empty:
        if insert_data(engine, competitions_df, 'competitions'):
            print("\nData successfully loaded into database!")
        else:
            print("\nFailed to load data into database")
    else:
        print("\nNo valid data to insert")

if __name__ == "__main__":
    main()