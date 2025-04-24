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
            # Ensure all leads have a visible field and filter invisible ones
            visible_leads = []
            for lead in data.get("leads", []):
                if "visible" not in lead:
                    lead["visible"] = True
                if lead.get("visible", True):
                    visible_leads.append(lead)
            data["leads"] = visible_leads
            return data
    return {"leads": []}

# Function to save data to YAML file
def save_data(data):
    # Ensure all leads have a visible field before saving
    for lead in data.get("leads", []):
        if "visible" not in lead:
            lead["visible"] = True
    with open("db.yaml", "w") as file:
        yaml.dump(data, file)

# Custom CSS with explicit text color settings
st.markdown("""
<style>
    # /* Base text color enforcement */
    # * {
    #     color: black;
    # }
    
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
        color: black;
    }
    
    .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: black;
    }
    
    .status-draftready {
        background-color: #A0A0A0;
        color: black;
    }
    
    .status-contacted {
        background-color: #3498DB;
        color: black;
    }
    
    .status-inconversation {
        background-color: #5DADE2;
        color: black;
    }
    
    .status-leadidentified {
        background-color: #9B59B6;
        color: black;
    }
    
    .status-notfit {
        background-color: #E74C3C;
        color: black;
    }
    
    .status-qualifiedlead {
        background-color: #1ABC9C;
        color: black;
    }
    
    .status-handedtohuman {
        background-color: #E67E22;
        color: black;
    }
    
    .status-meetingproposed {
        background-color: #F1C40F;
        color: black;
    }
    
    .status-meetingbooked {
        background-color: #2ECC71;
        color: black;
    }
    
    .conversation-expanded {
        padding: 10px;
        background-color: #f9f9f9;
        border-radius: 5px;
        margin: 5px 0;
        color: black;
    }
    
    .conversation-expanded p {
        color: black;
    }
    
    .conversation-expanded b {
        color: black;
    }
    
    /* Stage styling - force black text */
    .stage-indicator {
        padding: 5px;
        border-radius: 3px;
        color: black;
    }
    
    .stage-indicator b {
        color: black;
    }
    
    .stage-indicator span {
        color: black !important;
    }
    
    p, 
    span,
    label {
        color: black !important;
    }
    
    /* Even more forceful override for the expander header text */
    [data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] + div {
    color: black !important;
}
    /* Target Streamlit expander headers more precisely */
    [data-testid="stExpander"] > div:first-child, 
    [data-testid="stExpander"] > div:first-child p,
    [data-testid="stExpander"] > div:first-child span,
    .stExpander label, 
    .stExpander div p,
    div[role="button"] p {
        color: black !important;
    }

    /* Force all text in expanders to be black */
    [data-testid="stExpander"] {
        color: black !important;
    }

    /* Direct targeting of expander header text */
    button[kind="secondary"] p,
    .stExpanderToggleIcon + div,
    .stExpanderToggleIcon ~ div p {
        color: black !important;
    }
    
    /* Header text color override */
    .header-text {
        color: black;
        font-weight: bold;
    }
    
    /* Delete button styling */
    .stButton > button {
        background-color: #D3D3D3;
        color: black;
    }
    
    /* Date and message labels */
    .date-label, .message-label {
        color: black;
        font-weight: bold;
    }
    
    /* Message content */
    .message-content {
        color: black;
    }
    
    /* Stage text */
    .stage-text {
        color: black;
        font-weight: bold;
    }
    
    /* Stage value */
    .stage-value {
        color: black;
    }
    
    /* Override for the white text in status labels */
    div[class*="status-"] * {
        color: black;
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

# ─── Stateful toggle for "show_filter" ────────────────────────────────────────
# ─── Build dropdown options ──────────────────────────────────────────────────
status_options = [
    "All connections",
    "Draft Ready",
    "Contacted",
    "In-conversation",
    "Lead Identified",
    "Not fit Lead",
    "Qualified Lead",
    "Handed to Human",
    "Meeting Proposed",
    "Meeting Booked",
]

# ─── HEADER ROW: Title + Icon Button ────────────────────────────────────────
# ─── CONDITIONAL DROPDOWN ────────────────────────────────────────────────────
# ─── FILTER LEADS ────────────────────────────────────────────────────────
# ─── ADD THIS: Sort control ────────────────────────────────────────────────────

# Calculate statistics
total_leads = len(data["leads"])
contacted = sum(1 for lead in data["leads"] if lead["stage"] == "Contacted")
in_conversation = sum(1 for lead in data["leads"] if lead["stage"] == "In-conversation")
booked_calls = sum(1 for lead in data["leads"] if lead["stage"] in ("Meeting Proposed","Meeting Booked"))

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
    # ─── Inline filters next to table headings ────────────────────────────────────

    # 1) Initialize toggles in session_state
    if "show_stage_filter" not in st.session_state:
        st.session_state.show_stage_filter = False
    if "show_date_sort" not in st.session_state:
        st.session_state.show_date_sort = False

    # 2) Table HEADER with embedded filter/sort icons
    header_cols = st.columns([3, 6, 3, 2, 1])
    header_cols[0].markdown("<span class='header-text'>Company</span>", unsafe_allow_html=True)
    header_cols[1].markdown("<span class='header-text'>Conversation Snippet</span>", unsafe_allow_html=True)

    # ─ Stage ─────────────────────────────────────────────────────────────────────
    with header_cols[2]:
        ic, tc = st.columns([1, 9])
        if ic.button("🔽", key="toggle_stage_filter"):
            st.session_state.show_stage_filter = not st.session_state.show_stage_filter
        tc.markdown("<span class='header-text'>Stage</span>", unsafe_allow_html=True)

    # ─ Last Updated ──────────────────────────────────────────────────────────────
    with header_cols[3]:
        ic, tc = st.columns([1, 9])
        if ic.button("🔽", key="toggle_date_sort"):
            st.session_state.show_date_sort = not st.session_state.show_date_sort
        tc.markdown("<span class='header-text'>Last Updated</span>", unsafe_allow_html=True)

    # ─ Delete (blank) ────────────────────────────────────────────────────────────
    header_cols[4].markdown("", unsafe_allow_html=True)

    # 3) INLINE FILTER ROW (conditionally shown under the header)
    # 3a) Status filter dropdown
    if st.session_state.show_stage_filter:
        filter_cols = st.columns([3, 6, 3, 2, 1])
        with filter_cols[2]:
            st.selectbox(
                "",                        # no label
                options=status_options, 
                key="status_filter_key"
            )

    # 3b) Date sort dropdown
    if st.session_state.show_date_sort:
        sort_cols = st.columns([3, 6, 3, 2, 1])
        with sort_cols[3]:
            st.selectbox(
                "", 
                options=["Latest first", "Earliest first"], 
                key="date_sort_key"
            )

    # 4) APPLY FILTERS & SORTING
    # 4a) Stage / status filter
    sel_status = st.session_state.get("status_filter_key", "All connections")
    if sel_status == "All connections":
        stage_filtered = data["leads"]
    else:
        stage_filtered = [
            lead for lead in data["leads"]
            if lead["stage"] == sel_status
        ]

    # 4b) Date sorting
    sort_pref = st.session_state.get("date_sort_key", "Latest first")
    def get_last_date(lead):
        if not lead["conversations"]:
            return ""
        return max(c["date"] for c in lead["conversations"])

    leads_sorted = sorted(
        stage_filtered,
        key=lambda ld: get_last_date(ld),
        reverse=(sort_pref == "Latest first")
    )

    # 5) RENDER ROWS using `leads_sorted`
    for i, lead in enumerate(leads_sorted):
        row_cols = st.columns([3, 6, 3, 2, 1])
        # Company name
        row_cols[0].markdown(f"<span class='header-text'>{lead['company']}</span>", unsafe_allow_html=True)
        
        # Conversation Snippet (collapsible)
        with row_cols[1].expander(lead["conversations"][-1]["message"][:100] + "..." if len(lead["conversations"][-1]["message"]) > 100 else lead["conversations"][-1]["message"], expanded=False):
            for convo in lead["conversations"]:
                st.markdown(f"""
                <div class="conversation-expanded" style="border: 1px solid #e0e0e0; margin: 5px 0; padding: 10px; border-radius: 5px;">
                    <p><span class="date-label">Date:</span> <span class="message-content">{convo['date']}</span></p>
                    <p><span class="message-label">Message:</span> <span class="message-content">{convo['message']}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Stage with appropriate styling
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
        
        row_cols[2].markdown(f"""
        <div class="stage-indicator {stage_class}">
            <span class="stage-value">{lead["stage"]}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Last Updated date
        latest_date = max([convo['date'] for convo in lead["conversations"]]) if lead["conversations"] else "No conversations"
        row_cols[3].markdown(f"<span class='date-label'>{latest_date}</span>", unsafe_allow_html=True)
        
        # Delete button
        if row_cols[4].button("Delete", key=f"delete_{lead['company']}"):
            # Reload the full data to ensure we have all leads
            full_data = yaml.safe_load(open("db.yaml", "r"))
            # Update the specific lead's visibility
            for idx, l in enumerate(full_data["leads"]):
                if l["company"] == lead["company"]:
                    full_data["leads"][idx]["visible"] = False
                    break
            # Save the updated data
            with open("db.yaml", "w") as file:
                yaml.dump(full_data, file)
            st.rerun()