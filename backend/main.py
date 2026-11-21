from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from orchestrator import investigate_alert, load_json

# Load .env from the root proplr-sentinel folder
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="Proplr Sentinel API")

# Allow the React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvestigateRequest(BaseModel):
    alert_id: str

@app.get("/api/alerts")
def get_alerts():
    return load_json("alerts.json")

@app.post("/api/investigate")
def investigate(req: InvestigateRequest):
    try:
        return investigate_alert(req.alert_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))