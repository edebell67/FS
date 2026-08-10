"use client";

import { useEffect, useRef } from "react";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

interface BusinessMapProps {
  address: string;
  town: string | null;
  county: string | null;
  postcode: string | null;
  businessName: string;
  latitude?: number | null;
  longitude?: number | null;
}

/**
 * OpenStreetMap-powered map showing the business location.
 * Uses stored lat/lng coordinates from the database when available;
 * falls back to Nominatim geocoding only as a last resort.
 * Uses Leaflet (BSD-2-Clause) with OSM tiles.
 * No API keys required — all data is free and open-source (ODbL).
 *
 * The attribution line is required by the OpenStreetMap copyright policy and
 * the Leaflet license; it is rendered by Leaflet's built-in attribution control.
 */
export default function BusinessMap({
  address,
  town,
  county,
  postcode,
  businessName,
  latitude,
  longitude,
}: BusinessMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const instanceRef = useRef<L.Map | null>(null);

  /** Render the map at the given coordinates. */
  function renderMap(lat: number, lon: number, label: string) {
    if (!mapRef.current || instanceRef.current) return;

    const map = L.map(mapRef.current, {
      center: [lat, lon],
      zoom: 15,
      scrollWheelZoom: false,
      attributionControl: true,
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution:
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 19,
    }).addTo(map);

    // Red drop-pin SVG marker — no external image dependencies
    const redIcon = L.divIcon({
      html: `<svg xmlns="http://www.w3.org/2000/svg" width="32" height="42" viewBox="0 0 32 42"><path d="M16 0C7.2 0 0 7.2 0 16c0 12 16 26 16 26s16-14 16-26C32 7.2 24.8 0 16 0z" fill="#e85347"/><circle cx="16" cy="15" r="7" fill="#fff"/></svg>`,
      className: "",
      iconSize: [32, 42],
      iconAnchor: [16, 42],
      popupAnchor: [0, -42],
    });

    L.marker([lat, lon], { icon: redIcon })
      .addTo(map)
      .bindPopup(`<strong>${businessName}</strong><br>${label}`);

    instanceRef.current = map;

    // Enable scroll zoom on click/tap
    map.on("click", () => {
      if (map.scrollWheelZoom) {
        map.scrollWheelZoom.enable();
      }
    });
  }

  useEffect(() => {
    if (!mapRef.current || instanceRef.current) return;

    // 1. Use stored lat/lng from DB when available — instant, reliable, zero API calls
    if (latitude != null && longitude != null && !isNaN(latitude) && !isNaN(longitude)) {
      const label = [address, town, county, postcode].filter(Boolean).join(", ");
      renderMap(latitude, longitude, label);
      return;
    }

    // 2. Fallback: geocode the address via Nominatim (free, no API key, max 1 req/sec)
    const fullAddress = [address, town, county, postcode]
      .filter(Boolean)
      .join(", ");

    if (!fullAddress) return;

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);

    fetch(
      `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(fullAddress)}&limit=1&countrycodes=gb`,
      {
        headers: { "User-Agent": "EP047DirectoryApp/1.0 (business-map)" },
        signal: controller.signal,
      },
    )
      .then((res) => res.json())
      .then((data) => {
        clearTimeout(timeout);
        if (!Array.isArray(data) || data.length === 0) {
          // Try postcode only as last resort
          if (postcode) {
            return fetch(
              `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(postcode)}&limit=1&countrycodes=gb`,
              {
                headers: { "User-Agent": "EP047DirectoryApp/1.0 (business-map)" },
              },
            )
              .then((r) => r.json())
              .then((d2) => {
                if (Array.isArray(d2) && d2.length > 0) return d2;
                return null;
              });
          }
          return null;
        }
        return data;
      })
      .then((result) => {
        if (!result || !mapRef.current || instanceRef.current) return;
        const lat = parseFloat(result[0].lat);
        const lon = parseFloat(result[0].lon);
        if (isNaN(lat) || isNaN(lon)) return;
        renderMap(lat, lon, fullAddress);
      })
      .catch(() => {
        clearTimeout(timeout);
      });

    return () => {
      clearTimeout(timeout);
      controller.abort();
    };
  }, [address, town, county, postcode, businessName, latitude, longitude]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (instanceRef.current) {
        instanceRef.current.remove();
        instanceRef.current = null;
      }
    };
  }, []);

  const fullAddress = [address, town, county, postcode]
    .filter(Boolean)
    .join(", ");

  if (!fullAddress) return null;

  return (
    <div className="mt-6">
      <div
        ref={mapRef}
        className="h-56 w-full overflow-hidden rounded-xl border border-slate-200 sm:h-64"
        style={{ zIndex: 0 }}
        role="img"
        aria-label={`Map showing location of ${businessName} at ${fullAddress}`}
      />
    </div>
  );
}