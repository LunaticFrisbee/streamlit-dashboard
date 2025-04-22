import streamlit as st
import yaml
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="AI Sales Agent Dashboard", layout="wide", initial_sidebar_state="expanded")

# Function to load data from YAML file
def load_data():
    if os.path.exists("db.yaml"):
        with open("db.yaml", "r") as file:
            data = yaml.safe_load(file)
            # Filter out invisible leads
            data["leads"] = [lead for lead in data["leads"] if lead.get("visible", True)]
            return data
    return {"leads": []}

# Function to save data to YAML file
def save_data(data):
    with open("db.yaml", "w") as file:
        yaml.dump(data, file)

# Custom CSS with explicit text color settings
st.markdown("""
<style>
    /* Base text color enforcement */
    * {
        color: black;
    }
    
    .title {
        font-size: 36px;
        color: #4a6ea9 !important;
        text-align: center;
        margin-bottom: 30px;
    }
    
    .stat-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 30px;
    }
    
    .stat-box {
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        width: 22%;
    }
    
    .stat-box-blue {
        background-color: #e6f0ff;
        border: 1px solid #99c2ff;
    }
    
    .stat-box-yellow {
        background-color: #fff9e6;
        border: 1px solid #ffe680;
    }
    
    .stat-box-orange {
        background-color: #fff0e6;
        border: 1px solid #ffcc99;
    }
    
    .stat-box-green {
        background-color: #e6ffe6;
        border: 1px solid #99ff99;
    }
    
    .stat-label {
        font-size: 18px;
        margin-bottom: 5px;
        color: black !important;
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: black !important;
    }
    
    .status-draftready {
        background-color: #A0A0A0;
        color: black !important;
    }
    
    .status-contacted {
        background-color: #3498DB;
        color: black !important;
    }
    
    .status-inconversation {
        background-color: #5DADE2;
        color: black !important;
    }
    
    .status-leadidentified {
        background-color: #9B59B6;
        color: black !important;
    }
    
    .status-notfit {
        background-color: #E74C3C;
        color: black !important;
    }
    
    .status-qualifiedlead {
        background-color: #1ABC9C;
        color: black !important;
    }
    
    .status-handedtohuman {
        background-color: #E67E22;
        color: black !important;
    }
    
    .status-meetingproposed {
        background-color: #F1C40F;
        color: black !important;
    }
    
    .status-meetingbooked {
        background-color: #2ECC71;
        color: black !important;
    }
    
    .conversation-expanded {
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin: 5px 0;
        color: black !important;
    }
    
    .conversation-expanded p {
        color: black !important;
    }
    
    .conversation-expanded b {
        color: black !important;
    }
    
    /* Stage styling - force black text */
    .stage-indicator {
        padding: 5px;
        border-radius: 3px;
        color: black !important;
    }
    
    .stage-indicator b {
        color: black !important;
    }
    
    .stage-indicator span {
        color: black !important;
    }
    
    /* Force expander label text to be black */
    .streamlit-expanderHeader p {
        color: black !important;
    }
    
    /* Header text color override */
    .header-text {
        color: black !important;
        font-weight: bold;
    }
    
    /* Delete button styling */
    .stButton > button {
        background-color: #D3D3D3 !important;
        color: black !important;
    }
    
    /* Date and message labels */
    .date-label, .message-label {
        color: black !important;
        font-weight: bold;
    }
    
    /* Message content */
    .message-content {
        color: black !important;
    }
    
    /* Stage text */
    .stage-text {
        color: black !important;
        font-weight: bold;
    }
    
    /* Stage value */
    .stage-value {
        color: black !important;
    }
    
    /* Override for the white text in status labels */
    div[class*="status-"] * {
        color: black !important;
    }
</style>
""", unsafe_allow_html=True)

# Set light theme
st.markdown("""
    <style>
        .stApp {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Load data
data = load_data()

# Display title
st.markdown('<div class="title">AI Sales Agent Dashboard</div>', unsafe_allow_html=True)

# Calculate statistics
total_leads = len(data["leads"])
contacted = sum(1 for lead in data["leads"] if lead["stage"] == "Contacted")
in_conversation = sum(1 for lead in data["leads"] if lead["stage"] == "In-conversation")
booked_calls = sum(1 for lead in data["leads"] if lead["stage"] == "Meeting Proposed" or lead["stage"] == "Booked Call")

# Display statistics
st.markdown(f"""
<div class="stat-container">
    <div class="stat-box stat-box-blue">
        <div class="stat-label">Leads generated</div>
        <div class="stat-value">{total_leads}</div>
    </div>
    <div class="stat-box stat-box-yellow">
        <div class="stat-label">Contacted</div>
        <div class="stat-value">{contacted}</div>
    </div>
    <div class="stat-box stat-box-orange">
        <div class="stat-label">In-conversation</div>
        <div class="stat-value">{in_conversation}</div>
    </div>
    <div class="stat-box stat-box-green">
        <div class="stat-label">Booked Calls</div>
        <div class="stat-value">{booked_calls}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Create a container for the table
table_container = st.container()

with table_container:
    # Create columns for the table header
    cols = st.columns([3, 6, 3, 2, 1])
    cols[0].markdown("<span class='header-text'>Company</span>", unsafe_allow_html=True)
    cols[1].markdown("<span class='header-text'>Conversation</span>", unsafe_allow_html=True)
    cols[2].markdown("<span class='header-text'>Stage</span>", unsafe_allow_html=True)
    cols[3].markdown("<span class='header-text'>Last Updated</span>", unsafe_allow_html=True)
    cols[4].markdown("", unsafe_allow_html=True)
    
    # Display data rows
    for i, lead in enumerate(data["leads"]):
        # Create a unique key for each lead
        lead_key = f"lead_{i}"
        
        # Create an expander for the company with black text
        with st.expander(lead['company'], expanded=False):
            # Show company info in the header
            st.markdown(f"<span class='header-text'>{lead['company']}</span>", unsafe_allow_html=True)
            
            # Display latest conversation date
            latest_date = max([convo['date'] for convo in lead["conversations"]]) if lead["conversations"] else "No conversations"
            st.markdown(f"""
            <div class="conversation-expanded">
                <p><span class="date-label">Latest Update:</span> <span class="message-content">{latest_date}</span></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display conversations
            for j, convo in enumerate(lead["conversations"]):
                st.markdown(f"""
                <div class="conversation-expanded">
                    <p><span class="date-label">Date:</span> <span class="message-content">{convo['date']}</span></p>
                    <p><span class="message-label">Message:</span> <span class="message-content">{convo['message']}</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Display stage with appropriate styling and forced black text
            stage_class = ""
            if lead["stage"] == "Draft Ready":
                stage_class = "status-draftready"
            elif lead["stage"] == "Contacted":
                stage_class = "status-contacted"
            elif lead["stage"] == "In-conversation":
                stage_class = "status-inconversation"
            elif lead["stage"] == "Lead Identified":
                stage_class = "status-leadidentified"
            elif lead["stage"] == "Not fit Lead":
                stage_class = "status-notfit"
            elif lead["stage"] == "Qualified Lead":
                stage_class = "status-qualifiedlead"
            elif lead["stage"] == "Handed to Human":
                stage_class = "status-handedtohuman"
            elif lead["stage"] == "Meeting Proposed":
                stage_class = "status-meetingproposed"
            elif lead["stage"] == "Meeting Booked":
                stage_class = "status-meetingbooked"
            
            st.markdown(f"""
            <div class="stage-indicator {stage_class}">
                <span class="stage-text">Stage:</span> <span class="stage-value">{lead["stage"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Add delete button
            if st.button("Delete", key=f"delete_{lead_key}"):
                # Instead of removing the lead, set visible to false
                data["leads"][i]["visible"] = False
                save_data(data)
                st.rerun()