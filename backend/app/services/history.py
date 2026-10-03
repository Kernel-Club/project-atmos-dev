from app.db.mongodb import db
from app.models.history import WeatherHistory


history_collection = db["weather_history"]


async def save_weather_history(weather: WeatherHistory) -> None:
    history_collection.insert_one(
        {
            "city": weather.city,
            "temperature": weather.temperature,
            "description": weather.description,
            "humidity": weather.humidity,
            "timestamp": weather.timestamp,
        }
    )


async def get_weather_history() -> list[dict]:
    history = history_collection.find(
        {},
        {"_id": 0},
    ).sort("timestamp", -1)

    return list(history)


async def clear_weather_history() -> None:
    history_collection.delete_many({})