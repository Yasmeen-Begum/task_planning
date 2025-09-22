# planner/enrichers/weather.py
import os
import requests

# Use environment variable if available (recommended), otherwise fallback to provided key.
OPENWEATHER_KEY = os.getenv("OPENWEATHER_KEY", "d73576703f295e340b8725848ed7b171")

def get_weather_forecast(city: str, day_offset: int = 0):
    """
    Returns a friendly string with the day-offset forecast for `city`.
    day_offset is 0-based (0 => today, 1 => tomorrow).
    Uses the 5-day/3-hour forecast endpoint and approximates daily by selecting
    the item at index min(day_offset*8, last_index).
    """
    url = "http://api.openweathermap.org/data/2.5/forecast"
    params = {"q": city, "appid": OPENWEATHER_KEY, "units": "metric"}
    try:
        resp = requests.get(url, params=params, timeout=8)
        resp.raise_for_status()
        data = resp.json()

        items = data.get("list", [])
        if not items:
            return f"Weather unavailable for {city}: no forecast data"

        # Each day ~ 8 entries (3-hourly). Compute preferred index, clamp to available.
        preferred_idx = day_offset * 8
        idx = preferred_idx if preferred_idx < len(items) else len(items) - 1
        forecast = items[idx]

        # Parse fields safely
        weather_arr = forecast.get("weather", [])
        desc = weather_arr[0].get("description") if weather_arr else "No data"
        temp = forecast.get("main", {}).get("temp")

        temp_str = f"{round(temp,2)}°C" if temp is not None else "N/A"
        return f"{desc.capitalize()}, {temp_str}"

    except requests.exceptions.RequestException as re:
        return f"Weather unavailable for {city}: network error ({re})"
    except Exception as e:
        # catch-all so UI doesn't crash; return useful message
        return f"Weather unavailable for {city}: {str(e)}"
