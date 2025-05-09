import requests

def fetch_jira_tickets(jira_url, email, api_token, project_key, start_date, end_date):
    auth = (email, api_token)
    jql = (
        f'project = "{project_key}" AND updated >= "{start_date}" AND updated <= "{end_date}" '
        f'ORDER BY updated DESC'
    )
    url = f"{jira_url}/rest/api/3/search"
    headers = {"Accept": "application/json"}
    params = {"jql": jql, "maxResults": 50, "fields": "summary,status,assignee,updated,description"}

    response = requests.get(url, headers=headers, params=params, auth=auth)
    response.raise_for_status()
    issues = response.json()["issues"]

    tickets = []
    for issue in issues:
        fields = issue["fields"]
        tickets.append({
            "key": issue["key"],
            "summary": fields["summary"],
            "status": fields["status"]["name"],
            "assignee": fields["assignee"]["displayName"] if fields["assignee"] else "Unassigned",
            "updated": fields["updated"],
            "description": fields["description"] if fields["description"] else ""
        })
    return tickets