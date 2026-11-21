# Proplr Sentinel — Frontend

A demo-ready React + TypeScript frontend for the Brampton AI Innovator Challenge 4. It shows three synthetic IT alerts and an evidence-backed investigation view.

## Requirements

- Node.js 20.19+ (Node 22 LTS or newer is recommended)
- npm
- VS Code (recommended)

## Run locally

Open the project in VS Code, open Terminal → New Terminal, then:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL printed by Vite (usually http://localhost:5173).

## Build check

```bash
cd frontend
npm run build
```

Vite writes the production build to `frontend/dist/`.

## Demo scenarios

- **ALR-001 / payments-api:** historical match `INC-0087`, runbook `RB-012`, known fix guidance.
- **ALR-002 / checkout-service:** deployment `DEP-0412` at 10:15, alert at 10:30; deployment is described as a possible cause, not proof.
- **ALR-003 / notification-service:** no known historical match or fix; shows a recent SMTP configuration change to investigate.

All data is synthetic and stored in `src/data/demo.ts`.

## Backend integration

The frontend runs independently with demo data. When the backend is ready:

1. In `frontend/`, copy `.env.example` to `.env`. This is separate from the Gemini key's `.env` in the project root.
2. Set `VITE_API_BASE_URL` to the backend URL (for example `http://localhost:8000`).
3. Implement `GET /api/investigations/:alertId` returning an object matching `src/types.ts`.
4. Restart the Vite dev server.

The API adapter is in `src/lib/api.ts`. Adjust the endpoint or map the backend response there if the backend contract differs.

## Dependencies

Runtime:
- `react`, `react-dom`
- `lucide-react` — icons
- `axios` — backend HTTP requests

Development:
- `vite`, `typescript`, `@vitejs/plugin-react`
- `@types/react`, `@types/react-dom`

No Tailwind setup is required; the UI uses regular CSS in `src/styles.css`.

## Notes for reviewers

- No live client data or infrastructure connections.
- No remediation scripts or automatic fixes.
- Confidence is a demo field, not a calibrated production score.
- All actions are illustrative UI interactions only.
