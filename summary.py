from openai import OpenAI
import streamlit as st


def generate_summary_from_tickets(tickets):
    client = OpenAI(api_key=st.secrets['OPENAI_KEY'])

    # Format ticket info into a prompt
    formatted = []
    for t in tickets:
        fields = t.get("fields", {})
        key = t.get("key", "UNKNOWN")
        date = fields.get("updated", "")[:10]
        status = fields.get("status", {}).get("name", "Unknown")
        assignee = fields.get("assignee", {}).get("displayName", "Unassigned")
        summary = fields.get("summary", "No summary")
        description = fields.get("description", "")

        formatted.append(
            f"- [{date}] {key} ({status}) — {assignee}: {summary} — {description}"
        )

    ticket_log = "\n".join(formatted)

    prompt = (
        "You're a product operations assistant. Summarize the following Jira tickets "
        "into a clean weekly update for stakeholders. Group by theme if possible. "
        "Be concise and use a professional tone:\n\n"
        f"{ticket_log}"
    )

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You write clear status updates for product teams."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()
