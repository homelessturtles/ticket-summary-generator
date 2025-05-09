import streamlit as st
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="Weekly Update Bot", layout="centered")

# Header
st.title("📋 Weekly Ticket Summary Generator")
st.subheader("Generate clean stakeholder updates from Jira activity")

# Sidebar - Inputs
st.sidebar.header("🔧 Configuration")
jira_url = st.sidebar.text_input("Jira Base URL", placeholder="https://yourcompany.atlassian.net")
api_token = st.sidebar.text_input("API Token", type="password")
email = st.sidebar.text_input("Jira Account Email")
project_key = st.sidebar.text_input("Project Key", placeholder="e.g. PROJ")

# Date range (defaults to last 7 days)
default_end = datetime.today()
default_start = default_end - timedelta(days=7)
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

# Main Action
if st.button("🚀 Generate Summary"):
    if not all([jira_url, api_token, email, project_key]):
        st.error("Please fill in all required fields in the sidebar.")
    else:
        st.info("Fetching tickets from Jira... (coming soon)")

# Output Panel Placeholder
st.markdown("---")
st.markdown("### ✍️ Summary")
st.write("GPT-generated summary will appear here.")

# Footer
st.markdown("---")
st.caption("Built with 💻 by Brian Fedelin — Build #2 of the Internal Tools Series")