"""Incident brief app. Run with: streamlit run app.py

Left: incoming alerts. Right: the brief for the selected alert.
The engineer on call approves or rejects it. Nothing is executed or sent.

Trust rule: past incidents, changes and runbooks are shown straight from the
records. The AI only writes the likely cause, its confidence and the evidence.
If the AI fails, a plain brief is built from the same records.
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "backend"))
load_dotenv(ROOT / ".env")

import orchestrator  # noqa: E402
from skill_runner import run_skill  # noqa: E402

LIKELY_CAUSE_WINDOW = timedelta(hours=2)
REQUIRED_AI_KEYS = ("probable_root_cause", "confidence", "evidence")
ID_PATTERN = re.compile(r"\b(?:INC|DEP|CHG|RB|ALT)-\d+\b")


def parse_time(value):
    return datetime.fromisoformat(value)


def format_time(value):
    return parse_time(value).strftime("%Y-%m-%d %H:%M UTC")


def latest_change_before_alert(alert, changes):
    """The newest change close enough to the alert to suspect it, if any."""
    alert_time = parse_time(alert["timestamp"])
    candidates = [
        change
        for change in changes
        if timedelta(0) <= alert_time - parse_time(change["timestamp"]) <= LIKELY_CAUSE_WINDOW
    ]
    return max(candidates, key=lambda c: parse_time(c["timestamp"]), default=None)


def minutes_before(alert, change):
    gap = parse_time(alert["timestamp"]) - parse_time(change["timestamp"])
    return int(gap.total_seconds() // 60)


def build_fallback_brief(evidence):
    """A brief built only from the records, used when the AI is unavailable."""
    alert = evidence["alert"]
    history = evidence["history_matches"]
    runbooks = evidence["runbooks"]
    suspect = latest_change_before_alert(alert, evidence["recent_changes"])
    facts = [f"Log: {log['message']}" for log in evidence["log_anomalies"]]

    if suspect:
        suspect_text = (
            f"{suspect['deployment_id']} ({suspect['summary']}) was deployed "
            f"{minutes_before(alert, suspect)} minutes before this alert."
        )
        facts.append(suspect_text)

    if history and runbooks:
        match = history[0]
        cause = f"Possible repeat of {match['incident_id']}: {match['root_cause']}."
        if suspect:
            cause += f" Check {suspect['deployment_id']} first."
        confidence = "Medium"
    elif suspect:
        cause = f"Possibly caused by a recent release. {suspect_text}"
        confidence = "Medium"
    else:
        cause = "Unknown. No past incident matches this alert. Check the recent changes below."
        confidence = "Low"

    return {
        "probable_root_cause": cause,
        "confidence": confidence,
        "evidence": facts,
        "next_steps_if_unknown": [
            "Read the latest error logs for this service.",
            "Check for configuration or infrastructure changes outside the deploy history.",
            "Check the status pages of outside providers this service depends on.",
        ],
        "source": "fallback",
    }


def invented_ids(brief, evidence):
    """IDs the AI cited that do not appear in the evidence it was given."""
    return set(ID_PATTERN.findall(json.dumps(brief))) - set(
        ID_PATTERN.findall(json.dumps(evidence))
    )


def run_skill_safely(skill_name, payload):
    """Calls the AI without the scenario label, and falls back if it fails."""
    alert = {k: v for k, v in payload["alert"].items() if k != "scenario_label"}
    clean_payload = {**payload, "alert": alert}
    try:
        brief = run_skill(skill_name, clean_payload)
        if not all(brief.get(key) for key in REQUIRED_AI_KEYS):
            raise ValueError("AI reply is missing required fields")
        if invented_ids(brief, clean_payload):
            raise ValueError("AI reply cited an ID that is not in the evidence")
    except Exception as error:
        # Only the error type is logged, so a key can never reach the console.
        print(f"AI brief failed for {alert['alert_id']}: {type(error).__name__}")
        return build_fallback_brief(payload)
    return {**brief, "source": "ai"}


orchestrator.run_skill = run_skill_safely


def get_investigation(alert_id):
    """Runs once per alert, because Streamlit reruns this file on every click."""
    investigations = st.session_state.investigations
    if alert_id not in investigations:
        with st.spinner("Gathering evidence and writing the brief..."):
            investigations[alert_id] = orchestrator.investigate_alert(alert_id)
    return investigations[alert_id]


def show_alert_list(alerts):
    st.subheader("Alerts")
    for alert in alerts:
        alert_id = alert["alert_id"]
        decision = st.session_state.decisions.get(alert_id)
        mark = {"Approved": " ✅", "Rejected": " ❌"}.get(decision, "")
        selected = alert_id == st.session_state.selected
        if st.button(
            f"**{alert_id}{mark}** · {alert['service']}\n\n{alert['message']}",
            key=f"alert_{alert_id}",
            type="primary" if selected else "secondary",
            width="stretch",
        ):
            st.session_state.selected = alert_id
            st.rerun()


def show_likely_cause(brief):
    st.markdown("#### Likely cause")
    st.warning(f"{brief['probable_root_cause']}\n\nConfidence: {brief['confidence']}")
    if brief["evidence"]:
        st.markdown("**Why**")
        for fact in brief["evidence"]:
            st.markdown(f"- {fact}")


def show_past_incidents(incidents):
    st.markdown("#### Past incidents")
    if not incidents:
        st.write("No matching past incidents.")
    for incident in incidents:
        st.markdown(
            f"- **{incident['incident_id']}** ({incident['date']}, "
            f"{incident['score']:.0%} match): {incident['symptom']}\n"
            f"  - Cause: {incident['root_cause']}\n"
            f"  - Resolution: {incident['resolution']}"
        )


def show_recent_changes(alert, changes):
    st.markdown("#### Recent changes")
    if not changes:
        st.write("No recent changes on record for this service.")
    for change in changes:
        gap = minutes_before(alert, change)
        timing = f"{gap} min before alert" if gap >= 0 else "after the alert"
        st.markdown(
            f"- **{change['deployment_id']}**: {change['summary']} "
            f"({change['author']}, {format_time(change['timestamp'])}, {timing})"
        )


def show_known_fix(runbooks, brief):
    st.markdown("#### Known fix")
    if not runbooks:
        st.error("No known fix found.")
        steps = brief.get("next_steps_if_unknown") or []
        if steps:
            st.markdown("**What to check next**")
            for step in steps:
                st.markdown(f"- {step}")
        return
    for runbook in runbooks:
        st.markdown(f"**{runbook['runbook_id']}**: {runbook['title']}")
        for step in runbook["steps"]:
            st.markdown(step)


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


def show_brief(alert_id):
    result = get_investigation(alert_id)
    alert, findings, brief = result["alert"], result["agent_findings"], result["brief"]

    st.subheader(f"Brief for {alert_id}")
    st.caption(
        f"{alert['service']} · {alert['severity']} · {alert['message']} · "
        f"{format_time(alert['timestamp'])}"
    )

    if brief["source"] == "fallback":
        st.info("AI unavailable. This brief was built directly from the records.")
        if st.button("Try AI again", key=f"retry_{alert_id}"):
            del st.session_state.investigations[alert_id]
            st.rerun()

    show_likely_cause(brief)
    show_past_incidents(findings["history_matches"])
    show_recent_changes(alert, findings["recent_changes"])
    show_known_fix(findings["runbooks"], brief)
    show_decision(alert_id)


def main():
    st.set_page_config(page_title="Incident Brief", page_icon="🚨", layout="wide")
    alerts = orchestrator.load_json("alerts.json")
    st.session_state.setdefault("selected", alerts[0]["alert_id"])
    st.session_state.setdefault("decisions", {})
    st.session_state.setdefault("investigations", {})

    st.title("Incident Brief")
    st.caption("Sample data only. The engineer on call checks the brief and decides.")

    left, right = st.columns([1, 2], gap="large")
    with left:
        show_alert_list(alerts)
    with right:
        show_brief(st.session_state.selected)


if __name__ == "__main__":
    main()
