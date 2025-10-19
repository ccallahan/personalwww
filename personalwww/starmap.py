"""Custom d3-celestial star map component for Reflex."""

import reflex as rx
from typing import Any


class StarMap(rx.Component):
    """A d3-celestial based star map component."""

    tag = "StarMap"

    # Props
    latitude: rx.Var[float]
    longitude: rx.Var[float]
    width: rx.Var[str] = "100%"
    height: rx.Var[str] = "100vh"

    def _get_imports(self):
        return {
            "react": [
                rx.ImportVar(tag="useEffect"),
                rx.ImportVar(tag="useRef"),
            ],
        }

    def _get_custom_code(self) -> str:
        return """
// Load d3-celestial from CDN
const loadScript = (src) => {
  return new Promise((resolve, reject) => {
    if (document.querySelector(`script[src="${src}"]`)) {
      resolve();
      return;
    }
    const script = document.createElement('script');
    script.src = src;
    script.onload = () => {
      console.log(`Loaded: ${src}`);
      resolve();
    };
    script.onerror = reject;
    document.head.appendChild(script);
  });
};

const loadStyle = (href) => {
  if (document.querySelector(`link[href="${href}"]`)) {
    return;
  }
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = href;
  document.head.appendChild(link);
};

function StarMap({ latitude = 0, longitude = 0, width = '100%', height = '100vh' }) {
  const containerRef = useRef(null);
  const mapRef = useRef(null);

  useEffect(() => {
    let mounted = true;
    let resizeHandler = null;

    const initMap = async () => {
      try {
        // Load d3 v3 (d3-celestial was built for v3)
        if (!window.d3) {
          await loadScript('https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.17/d3.min.js');
          // Give d3 time to initialize
          await new Promise(resolve => setTimeout(resolve, 500));
        }
        
        // Double check d3 is available
        if (!window.d3) {
          console.error('d3 failed to load');
          return;
        }
        
        console.log('d3 loaded, version:', window.d3.version);
        
        // Load d3-celestial if not already loaded
        if (!window.Celestial) {
          loadStyle('https://cdn.jsdelivr.net/npm/d3-celestial@0.7.2/celestial.min.css');
          await loadScript('https://cdn.jsdelivr.net/npm/d3-celestial@0.7.2/celestial.min.js');
          // Wait for Celestial to be fully initialized
          await new Promise(resolve => setTimeout(resolve, 500));
        }

        if (!mounted || !containerRef.current || !window.Celestial) {
          console.log('Missing dependencies:', {
            mounted,
            container: !!containerRef.current,
            Celestial: !!window.Celestial,
            d3: !!window.d3
          });
          return;
        }

        console.log('Initializing Celestial map...');

        // Properly clear any previous instance
        if (mapRef.current && mapRef.current.clear) {
          try {
            mapRef.current.clear();
          } catch (e) {
            console.log('Error clearing previous map:', e);
          }
        }
        
        // Clear container
        if (containerRef.current) {
          containerRef.current.innerHTML = '';
        }
        
        // Create a specific div for the map
        const mapDiv = document.createElement('div');
        mapDiv.id = 'celestial-map';
        mapDiv.style.width = '100vw';
        mapDiv.style.height = '100vh';
        mapDiv.style.position = 'absolute';
        mapDiv.style.top = '50%';
        mapDiv.style.left = '50%';
        mapDiv.style.transform = 'translate(-50%, -50%) scale(1.2)';
        mapDiv.style.display = 'flex';
        mapDiv.style.alignItems = 'center';
        mapDiv.style.justifyContent = 'center';
        containerRef.current.appendChild(mapDiv);

        // Calculate size to fill screen
        const size = Math.max(window.innerWidth, window.innerHeight);

        const config = {
          width: size, // Use larger dimension to ensure full coverage
          projection: 'stereographic',
          transform: 'equatorial',
          center: [0, 0],
          orientationfixed: false,
          geopos: [longitude, latitude],
          follow: 'zenith',
          adaptable: true,
          interactive: true,
          form: false,
          location: false,
          controls: false,
          container: 'celestial-map',
          datapath: 'https://cdn.jsdelivr.net/npm/d3-celestial@0.7.2/data/',
          stars: {
            show: true,
            limit: 6,
            colors: true,
            style: { fill: '#ffffff', opacity: 1 },
            designation: false,
            designationLimit: 2.5,
            propername: false,
            propernameLimit: 1.5,
            size: 7,
            exponent: -0.28,
            data: 'stars.6.json'
          },
          dsos: {
            show: false,
          },
          constellations: {
            show: true,
            names: false,
            desig: false,
            namestyle: { fill: '#cccc99', align: 'center', baseline: 'middle', opacity: 0.8 },
            lines: true,
            linestyle: { stroke: '#cccccc', width: 1, opacity: 0.4 },
            bounds: false,
            boundstyle: { stroke: '#cccc00', width: 0.5, opacity: 0.8, dash: [2, 4] }
          },
          mw: {
            show: true,
            style: { fill: '#ffffff', opacity: 0.15 }
          },
          lines: {
            graticule: { show: true, stroke: '#cccccc', width: 0.6, opacity: 0.2 },
            equatorial: { show: false },
            ecliptic: { show: false },
            galactic: { show: false },
            supergalactic: { show: false }
          },
          background: { fill: 'transparent', opacity: 1, stroke: 'transparent', width: 0 },
          horizon: { show: false }
        };

        window.Celestial.display(config);
        mapRef.current = window.Celestial;

        // Handle window resize
        resizeHandler = () => {
          if (mapRef.current && mapRef.current.resize) {
            const size = Math.max(window.innerWidth, window.innerHeight);
            mapRef.current.resize({ width: size });
          }
        };
        
        window.addEventListener('resize', resizeHandler);
        
        // Initial resize to ensure proper sizing
        setTimeout(resizeHandler, 100);

      } catch (error) {
        console.error('Failed to load d3-celestial:', error);
      }
    };

    initMap();

    return () => {
      mounted = false;
      
      // Clean up resize handler
      if (resizeHandler) {
        window.removeEventListener('resize', resizeHandler);
      }
      
      // Clean up celestial map
      if (mapRef.current && mapRef.current.clear) {
        try {
          mapRef.current.clear();
          mapRef.current = null;
        } catch (e) {
          console.log('Error during cleanup:', e);
        }
      }
      
      // Clear container
      if (containerRef.current) {
        containerRef.current.innerHTML = '';
      }
    };
  }, [latitude, longitude]);

  return (
    <div
      ref={containerRef}
      style={{
        width: '100vw',
        height: '100vh',
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        margin: 0,
        padding: 0,
        zIndex: -1,
        overflow: 'hidden',
        background: 'linear-gradient(to bottom, #000428, #004e92)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    />
  );
}"""

    def get_event_triggers(self) -> dict[str, Any]:
        return {}


starmap = StarMap.create
