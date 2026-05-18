import json
import urllib.parse
import urllib.request
from langchain_core.tools import tool

NWS_API_BASE = "https://api.weather.gov"
_NWS_HEADERS = {"User-Agent": "agent-ollama/1.0", "Accept": "application/geo+json"}


def _nws_get(url: str) -> dict | None:
    req = urllib.request.Request(url, headers=_NWS_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


@tool
def add(a: int, b: int) -> int:
    """Adds two numbers together."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies two numbers together."""
    return a * b

@tool
def get_coordinates(location: str) -> str:
    """Get the latitude and longitude for a given location name.

    Args:
        location: A place name, city, address, or region (e.g. 'New York City', 'Paris, France').
    """
    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={urllib.parse.quote(location)}&format=json&limit=1"
    )
    req = urllib.request.Request(url, headers={"User-Agent": "agent-ollama/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            results = json.loads(resp.read())
    except Exception:
        return f"Unable to geocode '{location}'."
    if not results:
        return f"No coordinates found for '{location}'."
    lat = float(results[0]["lat"])
    lon = float(results[0]["lon"])
    display = results[0].get("display_name", location)
    return f"{display}\nLatitude: {lat}\nLongitude: {lon}"


@tool
def get_weather_alerts(state: str) -> str:
    """Get active weather alerts for a US state.

    Args:
        state: Two-letter US state code (e.g. CA, NY).
    """
    data = _nws_get(f"{NWS_API_BASE}/alerts/active/area/{state}")
    if not data or "features" not in data:
        return "Unable to fetch alerts or no alerts found."
    if not data["features"]:
        return f"No active alerts for {state}."
    parts = []
    for f in data["features"]:
        p = f["properties"]
        parts.append(
            f"Event: {p.get('event', 'Unknown')}\n"
            f"Area: {p.get('areaDesc', 'Unknown')}\n"
            f"Severity: {p.get('severity', 'Unknown')}\n"
            f"Description: {p.get('description', 'N/A')}\n"
            f"Instructions: {p.get('instruction', 'None')}"
        )
    return "\n---\n".join(parts)

@tool
def get_weather_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location using its latitude and longitude.

    Args:
        latitude: Latitude of the location.
        longitude: Longitude of the location.
    """
    points = _nws_get(f"{NWS_API_BASE}/points/{latitude},{longitude}")
    if not points:
        return "Unable to fetch forecast data for this location."
    forecast_url = points["properties"]["forecast"]
    forecast = _nws_get(forecast_url)
    if not forecast:
        return "Unable to fetch detailed forecast."
    periods = forecast["properties"]["periods"]
    parts = []
    for period in periods[:5]:
        parts.append(
            f"{period['name']}:\n"
            f"Temperature: {period['temperature']}°{period['temperatureUnit']}\n"
            f"Wind: {period['windSpeed']} {period['windDirection']}\n"
            f"Forecast: {period['detailedForecast']}"
        )
    return "\n---\n".join(parts)

tools = [add, multiply, get_coordinates, get_weather_alerts, get_weather_forecast]
