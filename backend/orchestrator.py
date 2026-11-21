import json
from datetime import datetime, timedelta
from pathlib import Path
from matching import search_past_incidents
from skill_runner import run_skill

DATA_DIR = Path(__file__).parent / "data"
CHANGE_WINDOW = timedelta(hours=24)
LOG_WINDOW = timedelta(hours=1)

def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def in_window(timestamp: str, alert_time: datetime, window: timedelta) -> bool:
    gap = alert_time - datetime.fromisoformat(timestamp)
    return timedelta(0) <= gap <= window

def investigate_alert(alert_id: str) -> dict:
    alerts = load_json("alerts.json")
    alert = next((a for a in alerts if a["alert_id"] == alert_id), None)
    if not alert:
        raise ValueError(f"Alert {alert_id} not found")

    service = alert["service"]
    alert_time = datetime.fromisoformat(alert["timestamp"])

    # 4 investigation lookups across historical incidents, deployments, logs, and runbooks
    history_matches = search_past_incidents(alert["message"], load_json("incidents.json"))
    recent_changes = sorted(
        (
            d for d in load_json("deployments.json")
            if d["service"] == service and in_window(d["timestamp"], alert_time, CHANGE_WINDOW)
        ),
        key=lambda d: d["timestamp"],
        reverse=True,
    )
    log_anomalies = [
        l for l in load_json("logs.json")
        if l["service"] == service and in_window(l["timestamp"], alert_time, LOG_WINDOW)
    ]
    # A runbook counts only when a matching past incident links to it
    matched_runbook_ids = {i["runbook_id"] for i in history_matches if i.get("runbook_id")}
    runbooks = [r for r in load_json("runbooks.json") if r["runbook_id"] in matched_runbook_ids]

    evidence_bundle = {
        "alert": alert,
        "history_matches": history_matches,
        "recent_changes": recent_changes,
        "log_anomalies": log_anomalies,
        "runbooks": runbooks
    }

    # Root Cause Analysis Agent synthesizes the evidence into an Incident Brief
    brief = run_skill("root-cause-agent", evidence_bundle)

    return {
        "alert": alert,
        "agent_findings": {
            "history_matches": history_matches,
            "recent_changes": recent_changes,
            "log_anomalies": log_anomalies,
            "runbooks": runbooks
        },
        "brief": brief
    }
