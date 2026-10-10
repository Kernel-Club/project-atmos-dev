from datetime import UTC, datetime

from app.clients.openweather import get_current_weather
from app.db.redis import client as redis_client
from app.models.history import WeatherHistory
from app.models.weather import WeatherResponse
from app.services.history import save_weather_history


async def get_weather(city: str) -> WeatherResponse:
    cache_key = f"weather:{city.lower()}"

    cached_weather = await redis_client.get(cache_key)

    if cached_weather:
        weather = WeatherResponse.model_validate_json(cached_weather)
    else:
        data = await get_current_weather(city)

        weather = WeatherResponse(
            city=data["name"],
            temperature=round(data["main"]["temp"]),
            description=data["weather"][0]["description"],
            humidity=data["main"]["humidity"],
        )

        await redis_client.set(
            cache_key,
            weather.model_dump_json(),
            ex=600,
        )

    await save_weather_history(
        WeatherHistory(
            city=weather.city,
            temperature=weather.temperature,
            description=weather.description,
            humidity=weather.humidity,
            timestamp=datetime.now(UTC),
        )
    )

    return weather