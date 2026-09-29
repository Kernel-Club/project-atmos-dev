from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: int
    description: str
    humidity: int