from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.config import OPENWEATHER_API_KEY
from app.services.weather import get_weather

app = FastAPI(
    title="Project Atmos API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config-check")
async def config_check() -> dict[str, bool]:
    return {"openweather_configured": bool(OPENWEATHER_API_KEY)}

@app.get("/weather/{city}")
async def weather(city: str):
    try:
        return await get_weather(city)
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )