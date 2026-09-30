const API_URL = 'http://127.0.0.1:8000'

export async function getWeather(city) {
  const response = await fetch(`${API_URL}/weather/${encodeURIComponent(city)}`)

  if (!response.ok) {
    const error = await response.json().catch(() => ({}))

    throw new Error(
      error.detail || 'Failed to fetch weather data'
    )
  }

  return response.json()
}