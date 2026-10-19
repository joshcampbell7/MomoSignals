# MomoSignals

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
