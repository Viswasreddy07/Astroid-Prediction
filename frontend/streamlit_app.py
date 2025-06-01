import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import pandas as pd
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="🛰 Asteroid Threat Analysis",
    page_icon="🛰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .stButton>button {
        background-color: #FF4B4B;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #FF6B6B;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 75, 75, 0.4);
    }
    .css-1d391kg {
        background-color: #1E1E1E;
    }
    .stMetric {
        background-color: #262730;
        padding: 15px;
        border-radius: 5px;
        animation: glow 1.5s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from {
            box-shadow: 0 0 5px #fff, 0 0 10px #fff, 0 0 15px #FF4B4B;
        }
        to {
            box-shadow: 0 0 10px #fff, 0 0 20px #fff, 0 0 30px #FF4B4B;
        }
    }
    .title-container {
        background: linear-gradient(45deg, #1E1E1E, #2E2E2E);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 30px;
        text-align: center;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.01); }
        100% { transform: scale(1); }
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("""
<div class="title-container">
    <h1>🛰 Asteroid Threat Analysis System</h1>
    <p>Real-time analysis and prediction of potentially hazardous asteroids using NASA data and machine learning</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")
    
    # API Configuration
    st.markdown("### 🔌 API Settings")
    api_url = st.text_input("API URL", value="http://localhost:8000")

# Main layout
col1, col2, col3 = st.columns(3)

# Metrics
with col1:
    st.metric(label="Active Asteroids", value="42", delta="5 new", delta_color="inverse")
with col2:
    st.metric(label="Highest Risk Score", value="0.85", delta="0.12 ↑")
with col3:
    st.metric(label="Next Close Approach", value="2d 5h", delta="-3 hours")

# Top Risks Section
st.markdown("## 🎯 Top Risk Analysis")

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_top_risks():
    try:
        response = requests.get(f"{api_url}/top_risks")
        return response.json()
    except:
        # Return sample data if API is not available
        return [
            {"name": "Sample Asteroid 1", "risk_score": 0.85, "diameter": "1.2-2.5 km"},
            {"name": "Sample Asteroid 2", "risk_score": 0.75, "diameter": "0.8-1.5 km"},
        ]

# Fetch and display top risks
risks = fetch_top_risks()
risk_df = pd.DataFrame(risks)

# Create animated bar chart
fig = go.Figure(data=[
    go.Bar(
        x=risk_df['risk_score'],
        y=risk_df['name'],
        orientation='h',
        marker=dict(
            color=risk_df['risk_score'],
            colorscale='Viridis',
            showscale=True
        )
    )
])

fig.update_layout(
    title="Top 10 Potentially Hazardous Asteroids",
    xaxis_title="Risk Score",
    yaxis_title="Asteroid Name",
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# Risk Prediction Form
st.markdown("## 🔮 Risk Prediction")
with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Asteroid Name", "Unknown Asteroid")
        diameter_min = st.number_input("Minimum Diameter (km)", 0.0, 100.0, 1.0)
        diameter_max = st.number_input("Maximum Diameter (km)", 0.0, 100.0, 2.0)
    
    with col2:
        velocity = st.number_input("Velocity (km/s)", 0.0, 100.0, 20.0)
        miss_distance = st.number_input("Miss Distance (AU)", 0.0, 1.0, 0.1)
        close_approach_date = st.date_input("Close Approach Date")
    
    submitted = st.form_submit_button("Predict Threat Level")
    
    if submitted:
        with st.spinner("Analyzing threat level..."):
            try:
                response = requests.post(
                    f"{api_url}/predict",
                    json={
                        "name": name,
                        "diameter_min": diameter_min,
                        "diameter_max": diameter_max,
                        "velocity": velocity,
                        "miss_distance": miss_distance,
                        "close_approach_date": close_approach_date.strftime("%Y-%m-%d")
                    }
                )
                result = response.json()
                
                # Display result with animation
                time.sleep(1)  # Add suspense
                
                if result["is_hazardous"]:
                    st.error(f"⚠️ High Risk Detected! Risk Score: {result['risk_score']:.2f}")
                else:
                    st.success(f"✅ Low Risk Level. Risk Score: {result['risk_score']:.2f}")
                
                # Display details
                st.json(result["details"])
                
            except Exception as e:
                st.error(f"Error making prediction: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>Powered by NASA NeoWs API and Machine Learning</p>
    <p>🛰 Asteroid Threat Analysis System v1.0</p>
</div>
""", unsafe_allow_html=True) 