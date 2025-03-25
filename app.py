import streamlit as st
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import pandas as pd

# Load environment variables
load_dotenv()

# Database connection function using SQLAlchemy
@st.cache_resource
def get_db_engine():
    try:
        engine = create_engine(
            f"postgresql://postgres:{os.getenv('DB_PASSWORD')}@"
            f"localhost:5432/sports_data"
        )
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception as e:
        st.error(f"""
        🚨 Database Connection Failed!
        
        Error: {e}
        
        Troubleshooting:
        1. Verify PostgreSQL is running
        2. Check your password in .env file
        3. Confirm database 'sports_data' exists
        """)
        st.stop()

# Main application
def main():
    st.title("🎾 Tennis Ranking Explorer")
    st.subheader("Ranking")
    
    engine = get_db_engine()
    
    # Table selection
    table_options = [
        'categories', 
        'competitions',
        'competitor_rankings',
        'competitors',
        'complexes',
        'venues'
    ]
    selected_table = st.selectbox("Select a table to view:", table_options)
     # SIDEBAR FILTERS 
    with st.sidebar:
        st.header("Filters")
        
        # Year dropdown 
        st.write("Year:")
        year = st.selectbox("", [2024], index=0, label_visibility="collapsed")
         #week dropdown 
        st.write("week:")
        week = st.selectbox("", [48], index=0, label_visibility="collapsed")
        # Gender dropdown 
        st.write("Gender")
        gender = st.selectbox("", ["men"], index=0, label_visibility="collapsed")
        
        # Range slider 
        st.write("Range")
        range = st.slider("", 1, 100, 48, label_visibility="collapsed")
    
    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("View Table Data"):
            try:
                with engine.connect() as conn:
                    query = """
                SELECT * FROM atp_doubles_rankings
                WHERE year = 2024 AND week = 48 AND gender = 'men'
                ORDER BY rank, player_name;
            """
                    df = pd.read_sql(text(query), conn)
                    st.dataframe(df)
                    
                    # Show record count
                    count_query = f"SELECT COUNT(*) FROM {selected_table}"
                    count = pd.read_sql(text(count_query), conn).iloc[0,0]
                    st.info(f"Total records: 3")
            except Exception as e:
                st.error(f"Error retrieving data: {e}")
    
    with col2:
        if st.button("Show Table Schema"):
            try:
                with engine.connect() as conn:
                    schema_query = f"""
                    SELECT column_name, data_type 
                    FROM information_schema.columns 
                    WHERE table_name = '{selected_table}'
                    """
                    schema_df = pd.read_sql(text(schema_query), conn)
                    st.dataframe(schema_df)
                    st.table(schema_df)  
                    
            except Exception as e:
                st.error(f"Error retrieving schema: {e}")

    # Raw SQL query section
    st.subheader("Custom SQL Query")
    sql_query = st.text_area("Enter your SQL query:")
    if st.button("Execute Query"):
        if sql_query:
            try:
                with engine.connect() as conn:
                    result = pd.read_sql(text(sql_query), conn)
                    st.dataframe(result)
            except Exception as e:
                st.error(f"Query error: {e}")
        else:
            st.warning("Please enter a SQL query")

if __name__ == "__main__":
    main()

    