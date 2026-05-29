#!/usr/bin/env python3
"""
Chicago Corps — Build Script
Validates flat CSV, joins relational data, geocodes addresses, generates JSON/GeoJSON for the frontend.
"""

import csv
import json
import os
import time
import random
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("_data")
MAIN_CSV = "chicago_mutual_aid_groups.csv"

def slugify(text):
    if not text:
        return ""
    return "".join(c.lower() if c.isalnum() else "-" for c in text).replace("--", "-").strip("-")

def geocode_address(address, city="Chicago"):
    # Wait 1 second to respect Nominatim usage policy
    time.sleep(1)
    query = f"{address}, {city}, IL"
    url = f"https://nominatim.openstreetmap.org/search?q={urllib.parse.quote(query)}&format=json&limit=1"
    
    req = urllib.request.Request(url, headers={'User-Agent': 'ChicagoCorps/1.0 (contact via GitHub)'})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data:
                return data[0]['lat'], data[0]['lon']
    except Exception as e:
        print(f"  Geocoding error for {query}: {e}")
    return None, None

def process_locations():
    loc_file = DATA_DIR / "locations.csv"
    if not loc_file.exists():
        return []
    
    with open(loc_file, "r", encoding="utf-8") as f:
        reader = list(csv.DictReader(f))
        fieldnames = reader[0].keys() if reader else []
    
    updated = False
    for row in reader:
        if row.get("street_address") and (not row.get("latitude") or not row.get("longitude")):
            print(f"Geocoding: {row['street_address']}...")
            lat, lon = geocode_address(row["street_address"], row.get("city") or "Chicago")
            if lat and lon:
                row["latitude"] = lat
                row["longitude"] = lon
                updated = True
                
    if updated:
        with open(loc_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(reader)
            
    return reader

def build_data():
    # 1. Load main groups
    with open(MAIN_CSV, "r", encoding="utf-8") as f:
        groups = list(csv.DictReader(f))
        
    for g in groups:
        g["group_id"] = slugify(g["name"])
        
    # 2. Load relational data
    def load_rel(filename):
        path = DATA_DIR / filename
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                return list(csv.DictReader(f))
        return []
        
    urgent_needs = load_rel("urgent_needs.csv")
    donation_needs = load_rel("donation_needs.csv")
    languages = load_rel("languages.csv")
    locations = process_locations()
    
    # 3. Join data
    urgent_map = {r["group_id"]: r for r in urgent_needs if r.get("urgent_need") == "TRUE"}
    donations_map = {}
    for r in donation_needs:
        donations_map.setdefault(r["group_id"], []).append(r)
    lang_map = {r["group_id"]: r for r in languages}
    
    for g in groups:
        gid = g["group_id"]
        g["is_urgent"] = gid in urgent_map
        g["urgent_description"] = urgent_map[gid]["urgent_need_description"] if gid in urgent_map else None
        g["donation_needs"] = [d["item"] for d in donations_map.get(gid, []) if d["item"]]
        
        langs = lang_map.get(gid, {})
        served = [l.strip() for l in langs.get("languages_served", "").split(",") if l.strip()]
        g["languages"] = served if served else ["English"] # Default to English if blank
        
    # 4. Generate JSON output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_DIR / "api.json", "w", encoding="utf-8") as f:
        json.dump({"generated_at": datetime.now().isoformat(), "groups": groups}, f, indent=2)
        
    # 5. Generate GeoJSON
    features = []
    mapped_groups = {loc["group_id"] for loc in locations if loc.get("latitude")}
    
    for loc in locations:
        if loc.get("latitude") and loc.get("longitude"):
            gname = next((g["name"] for g in groups if g["group_id"] == loc["group_id"]), "Unknown Group")
            gstatus = next((g["verification_status"] for g in groups if g["group_id"] == loc["group_id"]), "UNCERTAIN")
            gcat = next((g["category"] for g in groups if g["group_id"] == loc["group_id"]), "")
            
            features.append({
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [float(loc["longitude"]), float(loc["latitude"])]},
                "properties": {
                    "group_id": loc["group_id"],
                    "name": gname,
                    "location_name": loc.get("location_name", ""),
                    "address": loc.get("street_address", ""),
                    "verification_status": gstatus,
                    "category": gcat
                }
            })
            
    # Map neighborhood centroids for unmapped groups
    HOOD_GEO = {
        'Englewood':          [41.7730, -87.6460],
        'Bridgeport':         [41.8312, -87.6508],
        'Woodlawn':           [41.7747, -87.5929],
        'Bronzeville':        [41.8220, -87.6175],
        'Logan Square':       [41.9217, -87.7070],
        'Mayfair':            [41.9686, -87.7538],
        'Lakeview':           [41.9440, -87.6490],
        'Uptown':             [41.9734, -87.6580],
        'Hyde Park':          [41.7960, -87.5960],
        'South Side':         [41.7600, -87.6200],
        'North Side':         [41.9700, -87.6600],
        'Rogers Park':        [41.9983, -87.6630],
        'Pilsen':             [41.8544, -87.6623],
        'Avondale':           [41.9426, -87.7068],
        'Edgewater':          [41.9888, -87.6598],
        'Irving Park':        [41.9544, -87.7261],
        'Albany Park':        [41.9685, -87.7270],
        'Humboldt Park':      [41.9003, -87.7215],
        'Austin':             [41.8990, -87.7658],
        'Garfield Park':      [41.8820, -87.7188],
        'Roseland':           [41.6930, -87.6220],
        'Chatham':            [41.7500, -87.6060],
        'Auburn Gresham':     [41.7511, -87.6627],
        'West Side':          [41.8820, -87.7400],
        'Southwest Side':     [41.8100, -87.7000],
        'Northwest Side':     [41.9600, -87.7200],
        'Evanston':           [42.0450, -87.6877],
    }
    
    for g in groups:
        if g["group_id"] not in mapped_groups:
            hood = (g.get("neighborhood") or "").split(',')[0].strip()
            coords = None
            for key, val in HOOD_GEO.items():
                if key.lower() in hood.lower():
                    coords = val
                    break
            
            if coords:
                jitter_lat = (random.random() - 0.5) * 0.005
                jitter_lon = (random.random() - 0.5) * 0.005
                features.append({
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [coords[1] + jitter_lon, coords[0] + jitter_lat]},
                    "properties": {
                        "group_id": g["group_id"],
                        "name": g["name"],
                        "location_name": "Neighborhood Centroid",
                        "address": hood,
                        "verification_status": g.get("verification_status", "UNCERTAIN"),
                        "category": g.get("category", "")
                    }
                })
            
    geojson = {"type": "FeatureCollection", "features": features}
    with open(OUTPUT_DIR / "locations.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2)
        
    print(f"Built api.json ({len(groups)} groups)")
    print(f"Built locations.geojson ({len(features)} locations)")

    # 6. Inject data inline into index.html so no fetch() is needed (works on GitHub Pages with no backend)
    inject_into_html(groups, geojson)
    print("Injected data into index.html")


def inject_into_html(groups, geojson):
    import re
    html_file = Path("index.html")
    if not html_file.exists():
        print("  index.html not found, skipping injection")
        return

    with open(html_file, "r", encoding="utf-8") as f:
        html = f.read()

    # Strip any existing injected data block (the whole <script> tag we added)
    html = re.sub(
        r'\n<script>\s*/\* DATA_INJECTION_START \*/.*?/\* DATA_INJECTION_END \*/\s*</script>\n',
        '',
        html,
        flags=re.DOTALL
    )

    groups_json = json.dumps(groups, ensure_ascii=False)
    geojson_str = json.dumps(geojson, ensure_ascii=False)
    generated = datetime.now().isoformat()

    script_block = (
        "\n<script>\n"
        "/* DATA_INJECTION_START */\n"
        f"window.CHICAGO_CORPS_DATA = {{\n"
        f"  generated_at: '{generated}',\n"
        f"  groups: {groups_json},\n"
        f"  geojson: {geojson_str}\n"
        f"}};\n"
        "/* DATA_INJECTION_END */\n"
        "</script>\n"
    )

    # Insert BEFORE the first inline <script> tag (no src=) so data exists when init() runs
    match = re.search(r'\n<script>(?!\s*src)', html)
    if match:
        pos = match.start()
        html = html[:pos] + script_block + html[pos:]
    else:
        html = html.replace("</body>", script_block + "</body>")

    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html)




if __name__ == "__main__":
    build_data()
