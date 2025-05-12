import streamlit as st
from datetime import datetime, timedelta
from summary import generate_summary_from_tickets
from tickets import fetch_jira_tickets

# Page Config
st.set_page_config(page_title="Weekly Update Bot", layout="centered")

# Header
st.title("📋 Weekly Ticket Summary Generator")
st.subheader("Generate clean stakeholder updates from Jira activity")

# Sidebar - Inputs
st.sidebar.header("🔧 Configuration")
jira_url = st.sidebar.text_input(
    "Jira Base URL", placeholder="https://yourcompany.atlassian.net")
api_token = st.sidebar.text_input("API Token", type="password")
email = st.sidebar.text_input("Jira Account Email")
project_key = st.sidebar.text_input("Project Key", placeholder="e.g. PROJ")
# verbose = st.sidebar.checkbox("Show API Debug Logs")

# Date range (defaults to last 7 days)
default_end = datetime.today()
default_start = default_end - timedelta(days=7)
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", default_end)

# Button logic
if st.button("🚀 Generate Summary"):
    if not all([jira_url, email, api_token, project_key]):
        st.error("Please fill in all required fields in the sidebar.")
    else:
        try:
            with st.spinner("Fetching Jira tickets..."):
                tickets = fetch_jira_tickets(
                    jira_url=jira_url,
                    email=email,
                    api_token=api_token,
                    project_key=project_key,
                    start_date=start_date.strftime("%Y-%m-%d"),
                    end_date=end_date.strftime("%Y-%m-%d"),
                    verbose=verbose
                )

            if not tickets:
                st.warning("No tickets found in that range.")
            else:
                with st.spinner("Generating summary..."):
                    summary = generate_summary_from_tickets(tickets)
                st.markdown("### ✍️ Summary")
                st.markdown(summary)

        except Exception as e:
            st.exception(e)

# Footer
st.markdown("---")
st.caption("Built with 💻 by Brian Fedelin — Build #2 of the Internal Tools Series")
