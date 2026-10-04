from datetime import datetime

from pydantic import BaseModel


class WeatherHistory(BaseModel):
    city: str
    temperature: int
    description: str
    humidity: int
    timestamp: datetime