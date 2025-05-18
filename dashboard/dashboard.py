import streamlit as st
import requests
import time
import pandas as pd
import matplotlib.pyplot as plt

st.title("📦 SmartEdge Inventory Monitor")

# Session state to track restocks
if 'restock_history' not in st.session_state:
    st.session_state.restock_history = []

def fetch_data():
    try:
        response = requests.get("http://localhost:5000/get_logs", timeout=3)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"HTTP {response.status_code}"}
    except requests.exceptions.RequestException as e:
        return {"status": "error", "message": str(e)}

def restock_shelves():
    try:
        response = requests.post(
            "http://localhost:5000/restock",
            json={"amount": 100}  # Refill to 100 units
        )
        if response.status_code == 200:
            st.session_state.restock_history.append(time.time())
            st.success("✅ Shelves restocked to 100 units!")
        else:
            st.error(f"Restock failed: {response.json().get('message')}")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

def display_dashboard():
    data = fetch_data()
    
    if data.get("status") == "success":
        # Current Levels Section
        st.subheader("Current Inventory Levels")
        cols = st.columns(3)
        
        if data.get("logs"):
            latest = {log['device_id']: log['inventory_level'] for log in data["logs"][-3:]}
            for i, (shelf, level) in enumerate(latest.items()):
                cols[i].metric(
                    label=shelf,
                    value=f"{level:.1f} units",
                    delta=f"{level-100:.1f}%" if level < 100 else None
                )
        else:
            st.info("No inventory data yet")

        # Restock Button
        st.button("🔄 Restock All Shelves", on_click=restock_shelves)
        
        # Historical Chart
        if data.get("logs"):
            st.subheader("Historical Inventory Data")
            df = pd.DataFrame(data["logs"])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
            
            fig, ax = plt.subplots()
            for shelf in df['device_id'].unique():
                shelf_data = df[df['device_id'] == shelf]
                ax.plot(shelf_data['timestamp'], shelf_data['inventory_level'], label=shelf)
            
            # Add vertical lines for restocks
            for restock_time in st.session_state.restock_history:
                ax.axvline(pd.to_datetime(restock_time, unit='s'), color='r', linestyle='--', alpha=0.3)
            
            ax.set_xlabel("Time")
            ax.set_ylabel("Inventory Level")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        
    else:
        st.error(f"❌ Connection failed: {data.get('message')}")

display_dashboard()