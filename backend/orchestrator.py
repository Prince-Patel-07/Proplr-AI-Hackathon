import json
from pathlib import Path
from skill_runner import run_skill

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename: str):
    with open(DATA_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)

def investigate_alert(alert_id: str) -> dict:
    alerts = load_json("alerts.json")
    alert = next((a for a in alerts if a["alert_id"] == alert_id), None)
    if not alert:
        raise ValueError(f"Alert {alert_id} not found")

    service = alert["service"]

    # 4 investigation lookups across historical incidents, deployments, logs, and runbooks
    history_matches = [i for i in load_json("incidents.json") if i["service"] == service]
    recent_changes = [d for d in load_json("deployments.json") if d["service"] == service]
    log_anomalies = [l for l in load_json("logs.json") if l["service"] == service]
    runbooks = [r for r in load_json("runbooks.json") if r["service"] == service]

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