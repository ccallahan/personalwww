# Personal Website Features

## ✨ Current Features

### 🌟 Interactive Star Map Background
- **Real-time sky visualization** using d3-celestial (d3 v3)
- **GeoIP location detection** via ipapi.co
- Shows accurate star positions, constellations, and Milky Way
- Automatically adapts to visitor's geographic location
- Beautiful gradient background with constellation overlays

### 📻 Ham Radio Logbook Integration
- **Live logbook scraping** from https://hamlog.chancecallahan.com
- Displays most recent contact information:
  - Callsign contacted
  - Country/location
  - Date of contact
  - Mode (e.g., FT8, SSB, CW)
  - Band (e.g., 40m, 20m)
- Automatic updates on page load
- Beautiful card display with color-coded badges

## 🛠 Technical Stack

- **Backend**: Reflex (Python web framework)
- **HTTP Client**: httpx (async HTTP requests)
- **HTML Parsing**: BeautifulSoup4 + lxml
- **Sky Rendering**: d3-celestial v0.7.2 + d3 v3.5.17
- **Location**: ipapi.co GeoIP API (free tier)

## 🚀 How It Works

### On Page Load:
1. `fetch_all_data()` is called via `on_mount`
2. **GeoIP Lookup**: Fetches visitor's lat/lon from ipapi.co
3. **Logbook Scraping**: Parses HTML table from Cloudlog logbook
4. **Star Map Renders**: d3-celestial displays accurate sky for that location
5. **Contact Info Shows**: Last QSO displayed in a card overlay

### Star Map Initialization:
1. Loads d3 v3.5.17 from CDN
2. Loads d3-celestial v0.7.2 from CDN
3. Waits for libraries to initialize (500ms each)
4. Creates dedicated div with ID for map container
5. Configures celestial with visitor's coordinates
6. Renders stars, constellations, Milky Way, graticule

### Logbook Parser:
1. Fetches HTML from Cloudlog visitor page
2. Parses table rows with BeautifulSoup
3. Extracts first data row (most recent contact)
4. Populates state with callsign, country, date, mode, band

## 📊 Data Sources

- **GeoIP**: ipapi.co (1k requests/day free)
- **Logbook**: Cloudlog self-hosted instance
- **Star Data**: d3-celestial CDN (stars, constellations, Milky Way)
- **Map Library**: d3 v3 + d3-celestial from CDN (no build needed)

## 🎨 UI Components

- **Star Map**: Full-page fixed background with gradient
- **Hero Section**: Name and bio with text shadows for readability
- **Last Contact Card**: Semi-transparent card with:
  - Heading
  - Contact details
  - Color-coded badges (date=blue, mode=green, band=orange)
- **Dark Mode Toggle**: Top-right corner button

## 🔧 Customization

### Change Star Map Settings
Edit `personalwww/starmap.py`:
- Star brightness limit (magnitude)
- Constellation visibility
- Milky Way opacity
- Background gradient colors

### Change Fallback Location
Edit `personalwww/personalwww.py`:
```python
self.latitude = 36.44   # Your latitude
self.longitude = 78.19  # Your longitude
```

### Modify Logbook Display
Edit the card section in `index()` function to add/remove fields or change styling.

## 📝 Dependencies

```
reflex==0.8.15
httpx
beautifulsoup4
lxml
```

## 🐛 Known Issues

- Type linter shows warning on `on_mount=State.fetch_all_data` (works fine at runtime)
- Some JavaScript line length lint warnings in embedded code (cosmetic)

## 🎯 Future Enhancements

- Cache logbook data to reduce scraping frequency
- Add loading spinner while fetching data
- Show more logbook stats (total QSOs, countries worked, etc.)
- Add time-based star map updates
- Add click handlers to explore different sky regions
- Parse additional contact details (power, frequency, grid square)
