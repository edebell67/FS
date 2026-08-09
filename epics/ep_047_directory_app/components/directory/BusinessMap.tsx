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
}

/**
 * OpenStreetMap-powered map showing the business location.
 * Uses Leaflet (BSD-2-Clause) with OSM tiles and Nominatim geocoding.
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
}: BusinessMapProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const instanceRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (!mapRef.current || instanceRef.current) return;

    const fullAddress = [address, town, county, postcode]
      .filter(Boolean)
      .join(", ");

    // Geocode via Nominatim (free, no API key, usage: max 1 req/sec)
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
          // Fallback: try postcode only
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

        L.marker([lat, lon])
          .addTo(map)
          .bindPopup(`<strong>${businessName}</strong><br>${fullAddress}`);

        instanceRef.current = map;

        // Enable scroll zoom on click/tap
        map.on("click", () => {
          if (map.scrollWheelZoom) {
            map.scrollWheelZoom.enable();
          }
        });
      })
      .catch(() => {
        clearTimeout(timeout);
      });

    return () => {
      clearTimeout(timeout);
      controller.abort();
    };
  }, [address, town, county, postcode, businessName]);

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