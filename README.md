🎾 Tennis Analytics Dashboard with SportRadar API
Tennis Analytics Dashboard Preview
![Tennis app](https://github.com/user-attachments/assets/9b540707-fccf-4b69-92dd-49e21903945f)


🌟 Overview
A powerful analytics platform that transforms raw tennis data into actionable insights using SportRadar's API, PostgreSQL for robust data storage, and Streamlit for beautiful visualizations.

Key Features
⚡ Real-time Data Fetching - Direct connection to SportRadar's comprehensive tennis API

📊 Interactive Visualizations - Dynamic charts and player performance metrics

🗃️ PostgreSQL Backend - Efficient data storage and lightning-fast queries

📱 Responsive Design - Seamless experience across all devices

🔍 Advanced Filtering - Drill down into specific players, tournaments, and time periods

🛠️ Technology Stack
Python 3.8+ - Core analytics engine

PostgreSQL 12+ - Relational database

Streamlit - Interactive web dashboard

SportRadar API - Authoritative tennis data source

Pandas - Data manipulation powerhouse

Plotly - Beautiful, interactive visualizations

🚀 Quick Start Guide
Prerequisites
Python 3.8+

PostgreSQL 12+

SportRadar API key (free tier available)

Installation
bash
Copy
# Clone the repository
git clone https://github.com/yourusername/tennis-analytics.git
cd tennis-analytics

# Set up virtual environment (recommended)
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Configuration
Rename .env.example to .env

Update with your credentials:

SPORTRADAR_API_KEY="your_api_key_here"
DB_USER=postgres
DB_PASSWORD="your_password"
DB_HOST=localhost
DB_PORT=5432
DB_NAME=sports_data

Launch the Application:

streamlit run app.py
# Or specify Python path if needed
"C:\Path\To\Python\python.exe" -m streamlit run app.py
➔ Access your dashboard at: http://localhost:8501

📊 Dashboard Features
Player Performance Analysis: Track stats across tournaments

Head-to-Head Comparisons: Compare any two players

Trend Visualization: See performance over time

Custom Reporting: Generate tailored analytics reports
