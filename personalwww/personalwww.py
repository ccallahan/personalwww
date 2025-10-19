"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
import httpx
from bs4 import BeautifulSoup
from .starmap import starmap


class State(rx.State):
    """The app state."""

    latitude: float = 0.0
    longitude: float = 0.0
    location_loaded: bool = False

    # Ham radio logbook data
    last_contact_callsign: str = ""
    last_contact_country: str = ""
    last_contact_date: str = ""
    last_contact_mode: str = ""
    last_contact_band: str = ""
    logbook_loaded: bool = False

    # Weather data for KHNZ
    weather_temp: str = ""
    weather_condition: str = ""
    weather_wind: str = ""
    has_severe_thunderstorm: bool = False
    has_tornado: bool = False
    weather_loaded: bool = False

    async def fetch_location(self):
        """Fetch user's approximate location using GeoIP."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://ipapi.co/json/", timeout=5.0
                )
                if response.status_code == 200:
                    data = response.json()
                    self.latitude = float(data.get("latitude", 0.0))
                    self.longitude = float(data.get("longitude", 0.0))
                    self.location_loaded = True
        except Exception as e:
            # Fallback to default location (e.g., Greenwich)
            print(f"GeoIP lookup failed: {e}")
            self.latitude = 36.44
            self.longitude = 78.19
            self.location_loaded = True

    async def fetch_logbook(self):
        """Fetch and parse ham radio logbook for last contact."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://hamlog.chancecallahan.com/index.php/"
                    "visitor/master",
                    timeout=10.0,
                )
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "lxml")

                    # Find the table with logbook entries
                    # Looking for table rows with contact data
                    rows = soup.find_all("tr")

                    # Skip header row, get first data row (most recent)
                    for row in rows:
                        cells = row.find_all("td")
                        if len(cells) >= 7:  # Valid contact row
                            self.last_contact_date = cells[0].text.strip()
                            self.last_contact_country = (
                                cells[1].text.strip()
                            )
                            self.last_contact_callsign = (
                                cells[2].text.strip()
                            )
                            self.last_contact_mode = cells[3].text.strip()
                            self.last_contact_band = cells[6].text.strip()
                            self.logbook_loaded = True
                            break
        except Exception as e:
            print(f"Logbook fetch failed: {e}")
            self.logbook_loaded = False

    async def fetch_weather(self):
        """Fetch weather for KHNZ from National Weather Service API."""
        try:
            async with httpx.AsyncClient() as client:
                # KHNZ coordinates: 36.3611, -78.4636
                # Get weather station and forecast from NWS
                headers = {"User-Agent": "(Personal Website, chance1callahan@gmail.com)"}
                
                # Get grid point data for KHNZ location
                point_response = await client.get(
                    "https://api.weather.gov/points/36.3611,-78.4636",
                    headers=headers,
                    timeout=10.0,
                )
                
                if point_response.status_code == 200:
                    point_data = point_response.json()
                    
                    # Get current observations from nearest station
                    stations_url = point_data["properties"]["observationStations"]
                    stations_response = await client.get(
                        stations_url,
                        headers=headers,
                        timeout=10.0,
                    )
                    
                    if stations_response.status_code == 200:
                        stations_data = stations_response.json()
                        station_id = stations_data["features"][0]["properties"]["stationIdentifier"]
                        
                        # Get latest observation
                        obs_response = await client.get(
                            f"https://api.weather.gov/stations/{station_id}/observations/latest",
                            headers=headers,
                            timeout=10.0,
                        )
                        
                        if obs_response.status_code == 200:
                            obs_data = obs_response.json()
                            props = obs_data["properties"]
                            
                            # Extract temperature (convert C to F)
                            temp_c = props.get("temperature", {}).get("value")
                            if temp_c:
                                temp_f = (temp_c * 9/5) + 32
                                self.weather_temp = f"{temp_f:.0f}°F"
                            
                            # Extract condition
                            self.weather_condition = props.get("textDescription", "N/A")
                            
                            # Extract wind
                            wind_speed = props.get("windSpeed", {}).get("value")
                            wind_dir = props.get("windDirection", {}).get("value")
                            if wind_speed and wind_dir:
                                wind_mph = wind_speed * 0.621371  # km/h to mph
                                self.weather_wind = f"{wind_dir:.0f}° at {wind_mph:.0f} mph"
                    
                    # Check for active alerts
                    alerts_response = await client.get(
                        f"https://api.weather.gov/alerts/active?point=36.3611,-78.4636",
                        headers=headers,
                        timeout=10.0,
                    )
                    
                    if alerts_response.status_code == 200:
                        alerts_data = alerts_response.json()
                        self.has_severe_thunderstorm = False
                        self.has_tornado = False
                        
                        for feature in alerts_data.get("features", []):
                            event = feature["properties"]["event"].lower()
                            if "tornado" in event:
                                self.has_tornado = True
                            elif "severe thunderstorm" in event:
                                self.has_severe_thunderstorm = True
                    
                    self.weather_loaded = True
                    
        except Exception as e:
            print(f"Weather fetch failed: {e}")
            self.weather_loaded = False

    async def fetch_all_data(self):
        """Fetch location, logbook, and weather data."""
        await self.fetch_location()
        await self.fetch_logbook()
        await self.fetch_weather()


def index() -> rx.Component:
    # Welcome Page (Index) with star map background
    return rx.box(
        # Star map background
        rx.cond(
            State.location_loaded,
            starmap(
                latitude=State.latitude,
                longitude=State.longitude,
            ),
            rx.box(),  # Empty box while loading
        ),
        # Content overlay
        rx.container(
            rx.vstack(
                rx.heading(
                    "Chance Callahan",
                    size="9",
                    color="white",
                    text_shadow="0 0 10px rgba(0,0,0,0.8)",
                ),
                rx.text(
                    "Amateur Radio Operator, Human Spaceflight "
                    "Enthusiast, Weather Nerd, Tech Lover, "
                    "and System Administrator.",
                    size="5",
                    color="white",
                    text_shadow="0 0 10px rgba(0,0,0,0.8)",
                    text_align="center",
                ),
                # Last contact info
                rx.cond(
                    State.logbook_loaded,
                    rx.card(
                        rx.vstack(
                            rx.heading(
                                "Last on the air:",
                                size="5",
                                color="white",
                            ),
                            rx.text(
                                f"Contacted {State.last_contact_callsign} "
                                f"in {State.last_contact_country}",
                                color="white",
                                size="4",
                            ),
                            rx.hstack(
                                rx.badge(
                                    State.last_contact_date,
                                    color_scheme="blue",
                                ),
                                rx.badge(
                                    State.last_contact_mode,
                                    color_scheme="green",
                                ),
                                rx.badge(
                                    State.last_contact_band,
                                    color_scheme="orange",
                                ),
                                spacing="2",
                            ),
                            spacing="3",
                        ),
                        background="rgba(0,0,0,0.7)",
                        padding="4",
                        border_radius="lg",
                    ),
                    rx.box(),  # Empty when not loaded
                ),
                # Weather info with alert coloring
                rx.cond(
                    State.weather_loaded,
                    rx.card(
                        rx.vstack(
                            rx.heading(
                                "Weather at KHNZ:",
                                size="5",
                                color="white",
                            ),
                            rx.text(
                                f"{State.weather_temp} - "
                                f"{State.weather_condition}",
                                color="white",
                                size="4",
                                font_weight="bold",
                            ),
                            rx.text(
                                f"Wind: {State.weather_wind}",
                                color="white",
                                size="3",
                            ),
                            rx.cond(
                                State.has_tornado,
                                rx.badge(
                                    "⚠️ TORNADO WARNING/WATCH",
                                    color_scheme="red",
                                    size="3",
                                ),
                                rx.cond(
                                    State.has_severe_thunderstorm,
                                    rx.badge(
                                        "⚠️ SEVERE THUNDERSTORM WARNING/WATCH",
                                        color_scheme="yellow",
                                        size="3",
                                    ),
                                    rx.box(),
                                ),
                            ),
                            spacing="3",
                        ),
                        background=rx.cond(
                            State.has_tornado,
                            "rgba(139, 0, 0, 0.8)",  # Dark red
                            rx.cond(
                                State.has_severe_thunderstorm,
                                "rgba(139, 128, 0, 0.8)",  # Dark yellow
                                "rgba(0,0,0,0.7)",  # Normal
                            ),
                        ),
                        padding="4",
                        border_radius="lg",
                    ),
                    rx.box(),  # Empty when not loaded
                ),
                spacing="5",
                justify="center",
                align="center",
                min_height="85vh",
            ),
            position="relative",
            z_index="1",
        ),
        on_mount=State.fetch_all_data,
    )


app = rx.App()
app.add_page(index)
