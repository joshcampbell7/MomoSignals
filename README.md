# MomoSignals

AI-powered signals for prediction markets, starting with Valorant.

The frontend does not have its own backend. It reads the Valorant API in [valorant-prediction-model](https://github.com/joshcampbell7/valorant-prediction-model).

Pasting a Valorant Polymarket link sends it to that API. The API builds the market JSON, looks up recent news on the two teams, and returns the agent's reply. The frontend logs that reply in the browser console.

## Valorant API

Local API: http://127.0.0.1:8000/

Docs: http://127.0.0.1:8000/docs

Momo Signals route:

```http
POST http://127.0.0.1:8000/momo-signals
Content-Type: application/json

{ "url": "https://polymarket.com/esports/valorant/vct/val-wol-at1-2026-10-21" }
```

Start that API from the Valorant project, not from this repo.

Notes:

- Production docs: https://valorant-prediction-model.onrender.com/docs#/

## Frontend

From the project root:

```powershell
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173/
