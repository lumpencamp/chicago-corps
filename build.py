#!/usr/bin/env python3
"""
Chicago Corps — Build Script

Reads chicago_mutual_aid_groups.csv, joins relational data files, geocodes
any new addresses via OpenStreetMap Nominatim (rate-limited), and injects
the compiled data directly into index.html as an inline JS block.

Also writes _data/api.json and _data/locations.geojson for external use.

Usage:
    python3 build.py
"""

import csv
import json
import os
import re
import random
import time
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("_data")
MAIN_CSV = "chicago_mutual_aid_groups.csv"

# Neighborhood centroid fallbacks for groups without a street address
HOOD_GEO = {
    "Englewood":       [41.7730, -87.6460],
    "Bridgeport":      [41.8312, -87.6508],
    "Woodlawn":        [41.7747, -87.5929],
    "Bronzeville":     [41.8220, -87.6175],
    "Logan Square":    [41.9217, -87.7070],
    "Mayfair":         [41.9686, -87.7538],
    "Lakeview":        [41.9440, -87.6490],
    "Uptown":          [41.9734, -87.6580],
    "Hyde Park":       [41.7960, -87.5960],
    "South Side":      [41.7600, -87.6200],
    "North Side":      [41.9700, -87.6600],
    "Rogers Park":     [41.9983, -87.6630],
    "Pilsen":          [41.8544, -87.6623],
    "Avondale":        [41.9426, -87.7068],
    "Edgewater":       [41.9888, -87.6598],
    "Irving Park":     [41.9544, -87.7261],
    "Albany Park":     [41.9685, -87.7270],
    "Humboldt Park":   [41.9003, -87.7215],
    "Austin":          [41.8990, -87.7658],
    "Garfield Park":   [41.8820, -87.7188],
    "Roseland":        [41.6930, -87.6220],
    "Chatham":         [41.7500, -87.6060],
    "Auburn Gresham":  [41.7511, -87.6627],
    "West Side":       [41.8820, -87.7400],
    "Southwest Side":  [41.8100, -87.7000],
    "Northwest Side":  [41.9600, -87.7200],
    "Evanston":        [42.0450, -87.6877],
}


def slugify(text):
    """Convert a group name to a URL-safe ID slug."""
    if not text:
        return ""
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]", "-", text.lower())).strip("-")


def load_csv(filename):
    """Load a CSV from the data directory. Returns empty list if file missing."""
    path = DATA_DIR / filename
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def geocode_address(address, city="Chicago"):
    """Geocode a street address via Nominatim. Sleeps 1s to respect rate limits."""
    time.sleep(1)
    query = f"{address}, {city}, IL"
    url = (
        "https://nominatim.openstreetmap.org/search"
        f"?q={urllib.parse.quote(query)}&format=json&limit=1"
    )
    req = urllib.request.Request(
        url, headers={"User-Agent": "ChicagoCorps/1.0 (github.com/lumpencamp/chicago-corps)"}
    )
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if data:
                return data[0]["lat"], data[0]["lon"]
    except Exception as e:
        print(f"  Geocoding error for {query!r}: {e}")
    return None, None


def process_locations():
    """Load locations.csv, geocode any rows that are missing coordinates, and save."""
    loc_file = DATA_DIR / "locations.csv"
    if not loc_file.exists():
        return []

    with open(loc_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    updated = False
    for row in rows:
        if row.get("street_address") and not (row.get("latitude") and row.get("longitude")):
            print(f"  Geocoding: {row['street_address']}…")
            lat, lon = geocode_address(row["street_address"], row.get("city") or "Chicago")
            if lat and lon:
                row["latitude"] = lat
                row["longitude"] = lon
                updated = True

    if updated:
        with open(loc_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    return rows


def build_geojson(groups, locations):
    """Build a GeoJSON FeatureCollection from known locations + neighborhood fallbacks."""
    features = []
    mapped_ids = {loc["group_id"] for loc in locations if loc.get("latitude")}

    # Precise locations first
    for loc in locations:
        if not (loc.get("latitude") and loc.get("longitude")):
            continue
        g = next((g for g in groups if g["group_id"] == loc["group_id"]), {})
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [float(loc["longitude"]), float(loc["latitude"])],
            },
            "properties": {
                "group_id": loc["group_id"],
                "name": g.get("name", loc["group_id"]),
                "location_name": loc.get("location_name", ""),
                "address": loc.get("street_address", ""),
                "verification_status": g.get("verification_status", "UNCERTAIN"),
                "category": g.get("category", ""),
            },
        })

    # Neighbourhood centroid fallbacks (with jitter so markers don't stack)
    for g in groups:
        if g["group_id"] in mapped_ids:
            continue
        hood = (g.get("neighborhood") or "").split(",")[0].strip()
        coords = next(
            (v for k, v in HOOD_GEO.items() if k.lower() in hood.lower()), None
        )
        if coords:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        coords[1] + (random.random() - 0.5) * 0.005,
                        coords[0] + (random.random() - 0.5) * 0.005,
                    ],
                },
                "properties": {
                    "group_id": g["group_id"],
                    "name": g["name"],
                    "location_name": "Neighbourhood Centroid",
                    "address": hood,
                    "verification_status": g.get("verification_status", "UNCERTAIN"),
                    "category": g.get("category", ""),
                },
            })

    return {"type": "FeatureCollection", "features": features}


def inject_into_html(groups, geojson):
    """Inject compiled data as an inline <script> block into index.html."""
    html_file = Path("index.html")
    if not html_file.exists():
        print("  index.html not found, skipping injection")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Remove any previous injection
    html = re.sub(
        r"\n<script>\s*/\* DATA_INJECTION_START \*/.*?/\* DATA_INJECTION_END \*/\s*</script>\n",
        "",
        html,
        flags=re.DOTALL,
    )

    script_block = (
        "\n<script>\n"
        "/* DATA_INJECTION_START */\n"
        f"window.CHICAGO_CORPS_DATA = {{\n"
        f"  generated_at: '{datetime.now().isoformat()}',\n"
        f"  groups: {json.dumps(groups).replace('</', '<\\/')},\n"
        f"  geojson: {json.dumps(geojson).replace('</', '<\\/')}\n"
        "}};\n"
        "/* DATA_INJECTION_END */\n"
        "</script>\n"
    )

    # Insert BEFORE the first inline <script> block so data is ready when init() runs
    match = re.search(r"\n<script>(?!\s*src)", html)
    if match:
        html = html[: match.start()] + script_block + html[match.start():]
    else:
        html = html.replace("</body>", script_block + "</body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)


def build():
    print("Chicago Corps — Build\n")

    # Load and slug main CSV
    with open(MAIN_CSV, "r", encoding="utf-8") as f:
        groups = list(csv.DictReader(f))
    for g in groups:
        g["group_id"] = slugify(g["name"])

    # Load relational tables
    urgent_map = {
        r["group_id"]: r
        for r in load_csv("urgent_needs.csv")
        if r.get("urgent_need") == "TRUE"
    }
    donations_map: dict[str, list] = {}
    for r in load_csv("donation_needs.csv"):
        donations_map.setdefault(r["group_id"], []).append(r)
    lang_map = {r["group_id"]: r for r in load_csv("languages.csv")}

    # Enrich each group
    for g in groups:
        gid = g["group_id"]
        g["is_urgent"] = gid in urgent_map
        g["urgent_description"] = urgent_map[gid].get("urgent_need_description") if gid in urgent_map else None
        g["donation_needs"] = [d["item"] for d in donations_map.get(gid, []) if d.get("item")]
        served = [l.strip() for l in lang_map.get(gid, {}).get("languages_served", "").split(",") if l.strip()]
        g["languages"] = served or ["English"]

    # Geocode and build GeoJSON
    print("Checking locations…")
    locations = process_locations()
    geojson = build_geojson(groups, locations)

    # Write outputs
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_DIR / "api.json", "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.now().isoformat(), "groups": groups}, f, indent=2)
    with open(OUTPUT_DIR / "locations.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)

    inject_into_html(groups, geojson)

    print(f"\nDone — {len(groups)} groups · {len(geojson['features'])} map features")


if __name__ == "__main__":
    build()
