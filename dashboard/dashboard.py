import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Page configuration
st.set_page_config(layout="wide")
st.title("📊 SmartEdge Inventory Monitor")

def fetch_data():
    try:
        response = requests.get("http://localhost:5000/get_logs", timeout=3)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def create_historical_chart(df):
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Color palette for sensors
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    
    # Plot each sensor's data
    for i, device_id in enumerate(df['device_id'].unique()):
        device_data = df[df['device_id'] == device_id]
        ax.plot(
            device_data['timestamp'], 
            device_data['inventory_level'], 
            label=device_id,
            color=colors[i % len(colors)],
            linewidth=2
        )
    
    # Chart formatting
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Inventory Level", fontsize=12)
    ax.set_title("Inventory History", fontsize=14)
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    return fig

# Main dashboard layout
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Current Levels")
    data = fetch_data()
    
    if data.get("status") == "success" and data.get("logs"):
        # Get latest reading for each sensor
        latest_readings = {}
        for log in reversed(data["logs"]):
            if log["device_id"].startswith("Sensor") and log["device_id"] not in latest_readings:
                latest_readings[log["device_id"]] = log["inventory_level"]
        
        # Display metrics
        for device_id, level in latest_readings.items():
            st.metric(
                label=device_id,
                value=f"{level:.1f} units",
                delta=f"{level-100:.1f}%" if level < 100 else None
            )
    else:
        st.warning("Waiting for sensor data...")

with col2:
    st.header("Historical Trends")
    if data.get("status") == "success" and data.get("logs"):
        df = pd.DataFrame(data["logs"])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df = df[df['device_id'].str.startswith('Sensor')]  # Filter out system messages
        st.pyplot(create_historical_chart(df))
    else:
        st.info("No historical data available yet")

# Auto-refresh every 5 seconds
time.sleep(5)
st.rerun()