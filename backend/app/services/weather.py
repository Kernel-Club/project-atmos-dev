from app.clients.openweather import get_current_weather
from app.models.weather import WeatherResponse


async def get_weather(city: str) -> WeatherResponse:
    data = await get_current_weather(city)

    return WeatherResponse(
        city=data["name"],
        temperature=round(data["main"]["temp"]),
        description=data["weather"][0]["description"],
        humidity=data["main"]["humidity"],
    )