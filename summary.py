import openai
import streamlit as st


def generate_summary_from_tickets(tickets):
    client = openai.OpenAI(api_key=st.secrets["OPENAI_KEY"])

    formatted = []
    for t in tickets:
        fields = t.get("fields", {})
        key = t.get("key", "UNKNOWN")
        date = fields.get("updated", "")[:10]
        status = fields.get("status", {}).get("name", "Unknown")

        assignee_obj = fields.get("assignee")
        assignee = assignee_obj.get(
            "displayName") if assignee_obj else "Unassigned"

        summary = fields.get("summary", "No summary")
        description = fields.get("description", "")

        formatted.append(
            f"- [{date}] {key} ({status}) — {assignee}: {summary} — {description}"
        )

    ticket_log = "\n".join(formatted)

    prompt = (
        "You're a product operations assistant helping a product team stay informed.\n"
        "Write a clean, professional weekly summary of Jira tickets grouped by theme.\n\n"
        "For each ticket, include:\n"
        "- Key updates (what changed)\n"
        "- Status (In Progress, Blocked, etc.)\n"
        "- Who it's assigned to (if available)\n"
        "- Any risks, blockers, or delays\n\n"
        "Summarize in a way that's useful for product managers and cross-functional stakeholders.\n"
        "Format the output using bullet points under each theme. Be brief but informative.\n\n"
        "Here are the tickets:\n\n"
        f"{ticket_log}"
    )

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
