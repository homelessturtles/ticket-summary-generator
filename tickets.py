import requests
import base64
import streamlit as st
import base64


def fetch_jira_tickets(jira_url, email, api_token, project_key, start_date, end_date, verbose=False):
    jql = f"project={project_key} AND updated >= '{start_date}' AND updated <= '{end_date}' ORDER BY updated DESC"
    encoded_auth = base64.b64encode(f"{email}:{api_token}".encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_auth}",
        "Accept": "application/json"
    }

    params = {
        "jql": jql,
        "maxResults": 50,
        "fields": "summary,status,assignee,updated,description"
    }

    url = f"{jira_url}/rest/api/3/search"

    if verbose:
        st.markdown("#### 🛠 Debug Logs")
        st.write("📄 JQL:", jql)
        st.write("🔗 Full URL:", url)
        st.write("📦 Params:", params)
        st.write("📫 Headers:", {k: headers[k]
                 for k in headers if k != "Authorization"})

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        if verbose:
            st.success("✅ Jira API request successful.")
            st.json(data)

        return data.get("issues", [])

    except requests.exceptions.RequestException as e:
        if verbose:
            st.error("❌ Jira API request failed.")
            st.exception(e)
        raise e
