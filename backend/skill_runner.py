import os
import json
import httpx
from pathlib import Path

SKILLS_DIR = Path(__file__).parent / "skills"

def load_skill_instructions(skill_name: str) -> str:
    skill_path = SKILLS_DIR / skill_name / "SKILL.md"
    text = skill_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            return parts[2].strip()
    return text.strip()

def run_skill(skill_name: str, payload: dict) -> dict:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or "paste-your-key" in api_key:
        raise ValueError("Missing valid OPENROUTER_API_KEY in .env file")

    system_prompt = load_skill_instructions(skill_name)
    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "openai/gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(payload)}
            ],
            "temperature": 0.1
        },
        timeout=30.0
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    # Strip markdown code fences if the model includes them
    cleaned = content.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(cleaned)