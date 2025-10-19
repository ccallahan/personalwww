# Weather Integration for KHNZ

## ✅ Feature Complete!

Real-time weather conditions for KHNZ (Henderson Executive Airport, NC) with severe weather alert coloring.

## 🌤️ Features

### Current Weather Display
- **Temperature** in Fahrenheit
- **Conditions** (Clear, Cloudy, Rain, etc.)
- **Wind** (direction and speed in mph)
- **Location**: KHNZ (36.3611°N, 78.4636°W)

### Alert-Based Color Coding
- **🔴 RED Background** - Tornado Warning or Watch
- **🟡 YELLOW Background** - Severe Thunderstorm Warning or Watch
- **⚫ NORMAL Background** - No active alerts

### Alert Badges
- Shows prominent warning badge when severe weather is active
- "⚠️ TORNADO WARNING/WATCH" in red
- "⚠️ SEVERE THUNDERSTORM WARNING/WATCH" in yellow

## 🛠️ Technical Implementation

### Data Source
**National Weather Service (NWS) API** - Free, no API key required

### API Workflow
1. **Get Grid Point** - Query NWS for KHNZ coordinates (36.3611, -78.4636)
2. **Get Nearest Station** - Find closest weather observation station
3. **Get Latest Observation** - Fetch current temperature, conditions, wind
4. **Get Active Alerts** - Check for tornado/severe thunderstorm warnings/watches

### Temperature Conversion
- NWS provides Celsius
- Converted to Fahrenheit: `(C × 9/5) + 32`

### Wind Conversion
- NWS provides km/h
- Converted to mph: `km/h × 0.621371`

### Alert Detection
Scans active alerts for keywords:
- **Tornado**: "tornado" in event name
- **Severe Thunderstorm**: "severe thunderstorm" in event name

## 📊 State Variables

```python
weather_temp: str              # "72°F"
weather_condition: str         # "Partly Cloudy"
weather_wind: str             # "270° at 8 mph"
has_severe_thunderstorm: bool # Yellow background trigger
has_tornado: bool             # Red background trigger
weather_loaded: bool          # Display toggle
```

## 🎨 UI Design

### Normal Weather (No Alerts)
```
┌─────────────────────────────┐
│ Weather at KHNZ:            │
│ 72°F - Partly Cloudy        │
│ Wind: 270° at 8 mph         │
└─────────────────────────────┘
Background: rgba(0,0,0,0.7) - semi-transparent black
```

### Severe Thunderstorm Alert
```
┌─────────────────────────────┐
│ Weather at KHNZ:            │
│ 68°F - Thunderstorms        │
│ Wind: 180° at 15 mph        │
│ ⚠️ SEVERE THUNDERSTORM...   │
└─────────────────────────────┘
Background: rgba(139,128,0,0.8) - dark yellow/amber
```

### Tornado Alert
```
┌─────────────────────────────┐
│ Weather at KHNZ:            │
│ 65°F - Severe Storms        │
│ Wind: 230° at 25 mph        │
│ ⚠️ TORNADO WARNING/WATCH    │
└─────────────────────────────┘
Background: rgba(139,0,0,0.8) - dark red
```

## 🔄 Update Frequency

Weather data refreshes every time the page loads via `fetch_all_data()`:
- GeoIP lookup
- Ham radio logbook
- **Weather conditions**

## 🌐 API Endpoints Used

1. **Point Metadata**
   ```
   GET https://api.weather.gov/points/{lat},{lon}
   ```

2. **Observation Stations**
   ```
   GET https://api.weather.gov/points/{lat},{lon}/observationStations
   ```

3. **Latest Observation**
   ```
   GET https://api.weather.gov/stations/{stationId}/observations/latest
   ```

4. **Active Alerts**
   ```
   GET https://api.weather.gov/alerts/active?point={lat},{lon}
   ```

## 📝 Error Handling

- Graceful fallback if NWS API is unavailable
- Console logging of failures
- Card hidden if `weather_loaded = False`
- No API key rate limiting (NWS is free, public service)

## 🚀 Example Use Cases

### Aviation Weather
Perfect for pilots checking KHNZ conditions before flight

### Storm Chasing
Immediate visual alert when severe weather is detected

### General Interest
Keep tabs on local weather with at-a-glance display

## 🎯 Future Enhancements

- Add forecast (next 24-48 hours)
- Historical weather data
- Weather radar integration
- Multiple location support
- Hourly weather graph
- Ceiling/visibility for aviation
- METAR/TAF display
