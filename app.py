import streamlit as st
import yaml
import pandas as pd
import os
from datetime import datetime

# Set page configuration
st.set_page_config(page_title="AI Sales Agent Dashboard", layout="wide", initial_sidebar_state="expanded")

# ─── At the very top of your file, inject a tiny CSS tweak to shrink only the toggle buttons ───
st.markdown(
    """
    <style>
      /* Shrink all st.buttons slightly (affects toggle‐icons & delete buttons) */
      .stButton > button {
        font-size: 14px !important;
        min-width: 24px !important;
        height: 24px    !important;
        padding: 0 4px  !important;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to load data from YAML file
def load_data():
    if os.path.exists("db.yaml"):
        with open("db.yaml", "r") as file:
            data = yaml.safe_load(file)
            # Now we're looking for 'companies' instead of 'leads'
            visible_companies = []
            for company in data.get("companies", []):
                if company.get("lead_status", {}).get("visible", True):
                    visible_companies.append(company)
            return {"companies": visible_companies}
    return {"companies": []}

# Function to save data to YAML file
def save_data(data):
    # Ensure all companies have a visible field before saving
    for company in data.get("companies", []):
        if "lead_status" not in company:
            company["lead_status"] = {}
        if "visible" not in company["lead_status"]:
            company["lead_status"]["visible"] = True
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
    "prospecting",
    "contacted",
    "meeting_proposed",
    "in_conversation",
    "qualified",
    "closed"
]

# ─── HEADER ROW: Title + Icon Button ────────────────────────────────────────
# ─── CONDITIONAL DROPDOWN ────────────────────────────────────────────────────
# ─── FILTER LEADS ────────────────────────────────────────────────────────
# ─── ADD THIS: Sort control ────────────────────────────────────────────────────

# Calculate statistics
total_leads = len(data["companies"])
contacted = sum(1 for company in data["companies"] if company["lead_status"]["stage"] == "contacted")
in_conversation = sum(1 for company in data["companies"] if company["lead_status"]["stage"] == "in_conversation")
booked_calls = sum(1 for company in data["companies"] 
                  if company["lead_status"]["stage"] in ("meeting_proposed", "closed"))

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

    # ─── Stage Header + Toggle Icon on the RIGHT ────────────────────────────────────────────
    with header_cols[2]:
        text_col, icon_col = st.columns([9, 1])
        # 1) First render the header text …
        text_col.markdown("<span class='header-text'>Stage</span>", unsafe_allow_html=True)
        # 2) … then the toggle button
        if icon_col.button("🔽", key="toggle_stage_filter"):
            st.session_state.show_stage_filter = not st.session_state.show_stage_filter

    # ─── Last Updated Header + Toggle Icon on the RIGHT ───────────────────────────────────
    with header_cols[3]:
        text_col, icon_col = st.columns([9, 1])
        text_col.markdown("<span class='header-text'>Last Updated</span>", unsafe_allow_html=True)
        if icon_col.button("🔽", key="toggle_date_sort"):
            st.session_state.show_date_sort = not st.session_state.show_date_sort

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
        stage_filtered = data["companies"]
    else:
        stage_filtered = [
            company for company in data["companies"]
            if company["lead_status"]["stage"] == sel_status
        ]

    # 4b) Date sorting
    sort_pref = st.session_state.get("date_sort_key", "Latest first")
    def get_last_date(company):
        return company["lead_status"]["last_updated"] if company["lead_status"].get("last_updated") else ""

    companies_sorted = sorted(
        stage_filtered,
        key=lambda c: get_last_date(c),
        reverse=(sort_pref == "Latest first")
    )

    # 5) RENDER ROWS using `companies_sorted`
    for i, company in enumerate(companies_sorted):
        row_cols = st.columns([3, 6, 3, 2, 1])
        # Company name
        row_cols[0].markdown(f"<span class='header-text'>{company['name']}</span>", unsafe_allow_html=True)
        
        # Conversation Snippet (collapsible)
        latest_conversation = company["conversations"][-1] if company["conversations"] else {"message": "No messages"}
        snippet = latest_conversation["message"][:100] + "..." if len(latest_conversation["message"]) > 100 else latest_conversation["message"]
        
        with row_cols[1].expander(snippet, expanded=False):
            for convo in company["conversations"]:
                st.markdown(f"""
                <div class="conversation-expanded">
                    <p><span class="date-label">Date:</span> <span class="message-content">{convo['date']}</span></p>
                    <p><span class="message-label">Message:</span> <span class="message-content">{convo['message']}</span></p>
                </div>
                """, unsafe_allow_html=True)
        
        # Stage with appropriate styling
        stage = company["lead_status"]["stage"]
        stage_class = f"status-{stage.replace('_', '').lower()}"
        
        row_cols[2].markdown(f"""
        <div class="stage-indicator {stage_class}">
            <span class="stage-value">{stage.replace('_', ' ').title()}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Last Updated date
        latest_date = company["lead_status"]["last_updated"]
        row_cols[3].markdown(f"<span class='date-label'>{latest_date}</span>", unsafe_allow_html=True)
        
        # Delete button
        if row_cols[4].button("Delete", key=f"delete_{company['id']}"):
            # Reload the full data to ensure we have all companies
            full_data = yaml.safe_load(open("db.yaml", "r"))
            # Update the specific company's visibility
            for idx, c in enumerate(full_data["companies"]):
                if c["id"] == company["id"]:
                    full_data["companies"][idx]["lead_status"]["visible"] = False
                    break
            # Save the updated data
            with open("db.yaml", "w") as file:
                yaml.dump(full_data, file)
            st.rerun()