"""Incident brief app. Run with: streamlit run app.py

Left: incoming alerts. Right: the brief for the selected alert.
The engineer on call approves or rejects it. Nothing is executed or sent.
"""

import streamlit as st

# Sample alerts. At connect time, load these from data/alerts.json instead.
ALERTS = [
    {
        "id": "ALR-001",
        "service": "payments-api",
        "message": "Requests timing out, DB connections maxed",
        "time": "2026-11-21T09:40",
    },
    {
        "id": "ALR-002",
        "service": "checkout-service",
        "message": "5xx errors at 8%",
        "time": "2026-11-21T10:30",
    },
    {
        "id": "ALR-003",
        "service": "notification-service",
        "message": "Email queue backlog, SMTP failures",
        "time": "2026-11-21T11:05",
    },
]

# Hard-coded briefs, one per demo scenario. get_brief() below replaces these.
# Teammates: make_brief() should return this same shape.
FAKE_BRIEFS = {
    "ALR-001": {
        "likely_cause": "DB connection pool exhausted on payments-api. "
        "This matches a past incident with the same symptoms (INC-0087).",
        "confidence": "High",
        "past_incidents": [
            {
                "id": "INC-0087",
                "title": "payments-api DB connection pool exhausted",
                "score": 0.82,
            },
        ],
        "recent_changes": [],
        "known_fix": {
            "runbook_id": "RB-012",
            "title": "Recover from DB connection pool exhaustion",
            "steps": [
                "Confirm active connections are at the pool limit.",
                "Find and end long-running queries.",
                "Restart payments-api pods one at a time.",
                "Watch timeouts return to normal.",
            ],
        },
    },
    "ALR-002": {
        "likely_cause": "Deploy DEP-0412 to checkout-service at 10:15, "
        "15 minutes before the errors started.",
        "confidence": "High",
        "past_incidents": [],
        "recent_changes": [
            {
                "id": "DEP-0412",
                "service": "checkout-service",
                "time": "2026-11-21T10:15",
                "summary": "Code deploy",
            },
        ],
        "known_fix": None,
    },
    "ALR-003": {
        "likely_cause": "Unknown. No past incident matches this alert.",
        "confidence": "Low",
        "past_incidents": [],
        "recent_changes": [
            {
                "id": "CHG-SAMPLE",
                "service": "notification-service",
                "time": "2026-11-20T16:00",
                "summary": "Placeholder change to check",
            },
        ],
        "known_fix": None,
    },
}


def get_brief(alert):
    """The one place to connect the real pipeline at 19:30.

    Replace the body with:
        evidence = {
            "past_incidents": tools.search_past_incidents(alert["message"]),
            "recent_changes": tools.get_recent_changes(alert["service"], alert["time"]),
        }
        return agents.make_brief(alert, evidence)
    """
    return FAKE_BRIEFS[alert["id"]]


def show_alert_list():
    st.subheader("Alerts")
    for alert in ALERTS:
        decision = st.session_state.decisions.get(alert["id"])
        mark = {"Approved": " ✅", "Rejected": " ❌"}.get(decision, "")
        selected = alert["id"] == st.session_state.selected
        if st.button(
            f"**{alert['id']}{mark}** · {alert['service']}\n\n{alert['message']}",
            key=f"alert_{alert['id']}",
            type="primary" if selected else "secondary",
            width="stretch",
        ):
            st.session_state.selected = alert["id"]
            st.rerun()


def show_past_incidents(incidents):
    st.markdown("#### Past incidents")
    if not incidents:
        st.write("No matching past incidents.")
    for incident in incidents:
        st.markdown(
            f"- **{incident['id']}**: {incident['title']} "
            f"(match {incident['score']:.2f})"
        )


def show_recent_changes(changes):
    st.markdown("#### Recent changes")
    if not changes:
        st.write("No recent changes to this service.")
    for change in changes:
        when = change["time"].replace("T", " ")
        st.markdown(
            f"- **{change['id']}**: {change['summary']} to "
            f"{change['service']} at {when}"
        )


def show_known_fix(fix):
    st.markdown("#### Known fix")
    if not fix:
        st.error("No known fix found.")
        return
    st.markdown(f"**{fix['runbook_id']}**: {fix['title']}")
    for number, step in enumerate(fix["steps"], start=1):
        st.markdown(f"{number}. {step}")


def show_decision(alert_id):
    st.divider()
    decision = st.session_state.decisions.get(alert_id)
    if decision:
        st.info(f"{decision} by the engineer on call. No fix was run.")
        if st.button("Undo", key=f"undo_{alert_id}"):
            del st.session_state.decisions[alert_id]
            st.rerun()
        return

    st.caption("You decide. Approving records your decision and runs nothing.")
    approve, reject = st.columns(2)
    if approve.button("Approve", key=f"approve_{alert_id}", type="primary", width="stretch"):
        st.session_state.decisions[alert_id] = "Approved"
        st.rerun()
    if reject.button("Reject", key=f"reject_{alert_id}", width="stretch"):
        st.session_state.decisions[alert_id] = "Rejected"
        st.rerun()


def show_brief(alert):
    brief = get_brief(alert)
    st.subheader(f"Brief for {alert['id']}")
    st.caption(
        f"{alert['service']} · {alert['message']} · {alert['time'].replace('T', ' ')}"
    )

    st.markdown("#### Likely cause")
    st.warning(f"{brief['likely_cause']}\n\nConfidence: {brief['confidence']}")

    show_past_incidents(brief["past_incidents"])
    show_recent_changes(brief["recent_changes"])
    show_known_fix(brief["known_fix"])
    show_decision(alert["id"])


def main():
    st.set_page_config(page_title="Incident Brief", page_icon="🚨", layout="wide")
    st.session_state.setdefault("selected", ALERTS[0]["id"])
    st.session_state.setdefault("decisions", {})

    st.title("Incident Brief")
    st.caption("Sample data only. The engineer on call checks the brief and decides.")

    left, right = st.columns([1, 2], gap="large")
    with left:
        show_alert_list()
    with right:
        alert = next(a for a in ALERTS if a["id"] == st.session_state.selected)
        show_brief(alert)


if __name__ == "__main__":
    main()
