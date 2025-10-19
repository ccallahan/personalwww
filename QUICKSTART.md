# Star Map Background - Quick Start

## What Was Built

✅ **GeoIP Location Detection** (`personalwww/personalwww.py`)
- Automatically detects user's location via ipapi.co API
- Falls back to a default location if API fails
- Async implementation using httpx

✅ **Custom d3-celestial Component** (`personalwww/starmap.py`)
- Wraps d3-celestial JavaScript library as a Reflex component
- Loads library from CDN (no npm install needed)
- Displays stars, constellations, and Milky Way
- Positioned as a fixed full-page background

✅ **Updated Main Page** (`personalwww/personalwww.py`)
- Integrated star map background
- Content overlay with improved styling (white text, shadows)
- Fetches location on page mount

✅ **Dependencies** (`requirements.txt`)
- Added httpx for async HTTP requests

## To Run

```bash
# Install dependencies (if not already done)
pip install -r requirements.txt

# Start the development server
reflex run

# Open browser to http://localhost:3000
```

## Features

- **Accurate Sky View**: Shows stars as they appear from user's geographic location
- **Interactive**: Pan and zoom the star map
- **Beautiful**: Constellation lines, star colors, Milky Way overlay
- **Responsive**: Full-page background that adapts to window size
- **Fast**: Loads d3-celestial from CDN (no build step required)

## Customization

### Change Star Visibility
Edit `personalwww/starmap.py` line ~84:
```javascript
limit: 6,  // Change to 4 for brighter stars only, or 8 for dimmer stars
```

### Toggle Constellation Names
Edit `personalwww/starmap.py` line ~97:
```javascript
names: true,  // Change to true to show constellation names
```

### Change Background Gradient
Edit `personalwww/starmap.py` line ~147:
```javascript
background: 'linear-gradient(to bottom, #000428, #004e92)',  // Customize colors
```

### Change Fallback Location
Edit `personalwww/personalwww.py` line ~31-32 (currently set to your area):
```python
self.latitude = 36.44   # Your latitude
self.longitude = 78.19  # Your longitude (positive = East, negative = West)
```

## How It Works

1. Page loads → `on_mount` triggers `State.fetch_location()`
2. Backend calls ipapi.co → gets lat/lon
3. `location_loaded` becomes True → star map renders
4. d3-celestial loads from CDN → renders accurate sky view for that location
5. User sees stars/constellations visible from their position

## Technical Notes

- No JavaScript build required (uses CDN)
- No API key needed for ipapi.co (free tier: 1k requests/day)
- Star data loaded once per session
- Python lint warnings about JS line length are normal/harmless
