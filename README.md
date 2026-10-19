# MomoSignals

AI-powered signals for prediction markets, starting with Valorant.

A signal is a judgment about a market, not the price itself. Polymarket already states a probability. MomoSignals reads that market, and later compares it with match and player data, so it can say when the two disagree by enough to matter.

Right now, pasting a Valorant Polymarket link builds one JSON body and logs it. The body includes the sport, teams, each market's outcomes, prices, bids and asks, spread, volume, liquidity, and whether the book is tradable. Match pages and other Valorant markets, such as roster markets, both work. Other esports are rejected until they are added. The `sport` field is there so that expansion stays a small change.

## Next steps

- Use an AI library that makes it easy to create agents.
- Add helper functions that worker agents can call when they evaluate a market and produce a signal. Start with two:
  - The backend Valorant API, so an agent can read the market body for a pasted Polymarket link.
  - Web search, so an agent can make basic web queries while it evaluates the market.

## Frontend

From the project root:

```powershell
cd frontend
npm install
npm run dev
```

Opens at http://localhost:5173/

## Backend

From the project root. The virtual environment only needs to be created the first time.

```powershell
cd backend
py -3.10 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

After the first setup, start it with:

```powershell
cd backend
.\.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: http://127.0.0.1:8000/

Docs: http://127.0.0.1:8000/docs
