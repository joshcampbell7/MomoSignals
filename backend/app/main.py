from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.polymarket import LinkError, build_market_body

app = FastAPI(title="MomoSignals API")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "MomoSignals API"}


@app.get("/health")
def health():
    return {"status": "ok"}


class MarketLink(BaseModel):
    url: str


@app.post("/markets")
def read_market(link: MarketLink):
    try:
        return build_market_body(link.url)
    except LinkError as error:
        raise HTTPException(status_code=error.status_code, detail=error.message) from error
