# Personal Website with Star Map Background

A Reflex web application featuring an interactive celestial star map background that displays the stars and constellations visible from the user's approximate geographic location.

## Features

- **GeoIP Location Detection**: Automatically detects the user's approximate location using the ipapi.co API
- **d3-celestial Integration**: Renders an accurate star map with constellations based on the user's location
- **Real-time Sky View**: Shows stars, constellations, and the Milky Way as they appear from the user's position
- **Responsive Design**: Full-page star map background with content overlay

## Technical Stack

- **Reflex**: Python web framework
- **d3-celestial**: JavaScript library for astronomical visualizations (loaded via CDN)
- **httpx**: Async HTTP client for GeoIP lookups
- **ipapi.co**: Free GeoIP service

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   reflex run
   ```

3. Open your browser to `http://localhost:3000`

## How It Works

1. **Location Detection**: When the page loads, the `State.fetch_location()` method calls the ipapi.co API to get the user's latitude and longitude
2. **Star Map Rendering**: The custom `starmap` component loads d3-celestial from CDN and renders the star map with:
   - Stars up to magnitude 6 (visible to naked eye)
   - Constellation lines and boundaries
   - The Milky Way
   - Equatorial grid
3. **Background Integration**: The star map is positioned as a fixed background with content overlaid on top

## Customization

### Star Map Settings

Edit `personalwww/starmap.py` to customize the star map appearance:

- `stars.limit`: Maximum star magnitude to display (6 = visible to naked eye)
- `stars.colors`: Show stars in their actual colors
- `constellations.show`: Toggle constellation lines
- `mw.show`: Toggle Milky Way display
- `projection`: Change sky projection (stereographic, aitoff, mercator, etc.)

### Fallback Location

If GeoIP lookup fails, the app defaults to Greenwich, UK (51.4779°N, 0.0015°W). Edit the fallback in `personalwww/personalwww.py`:

```python
self.latitude = 51.4779  # Change to your preferred latitude
self.longitude = -0.0015  # Change to your preferred longitude
```

## API Usage

This app uses the free tier of ipapi.co (no API key required). The free tier allows:
- 1,000 requests per day
- 30,000 requests per month

For production use with higher traffic, consider:
- Caching user locations
- Using ipapi.co's paid tier
- Switching to an alternative GeoIP service

## Development Notes

- The d3-celestial library is loaded from CDN, so no npm installation is needed
- Star data is fetched from the d3-celestial CDN on first render
- The component uses React hooks (useEffect, useRef) within the custom Reflex component
- Python lint warnings about line length in embedded JavaScript can be ignored

## License

This project template is provided as-is for personal use.

d3-celestial is licensed under the BSD-3-Clause License.
