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

# Neighborhood centroid fallbacks for groups without a street address.
# Covers every neighborhood that appears in the CSV so no group is silently
# dropped from the map.
HOOD_GEO = {
    # ── City-level / generic ──────────────────────────────────────────────
    "Citywide":          [41.8781, -87.6298],  # Chicago centre
    "Chicago":           [41.8781, -87.6298],
    "Statewide":         [41.8781, -87.6298],
    "Cook County":       [41.8781, -87.6298],
    "Multiple":          [41.8781, -87.6298],
    "Varies":            [41.8781, -87.6298],
    # ── North Side ────────────────────────────────────────────────────────
    "Rogers Park":       [41.9983, -87.6630],
    "West Ridge":        [41.9977, -87.6961],
    "Uptown":            [41.9734, -87.6580],
    "Lincoln Square":    [41.9678, -87.6877],
    "North Center":      [41.9558, -87.6762],
    "Ravenswood":        [41.9734, -87.6746],
    "Lake View":         [41.9440, -87.6490],
    "Lakeview":          [41.9440, -87.6490],
    "Lincoln Park":      [41.9216, -87.6497],
    "Near North":        [41.9000, -87.6376],
    "River North":       [41.8952, -87.6337],
    "Streeterville":     [41.8924, -87.6192],
    "Gold Coast":        [41.9027, -87.6286],
    "Edgewater":         [41.9888, -87.6598],
    "Andersonville":     [41.9784, -87.6688],
    "Roscoe Village":    [41.9451, -87.6786],
    "North Shore":       [42.0800, -87.7800],
    # ── Northwest Side ────────────────────────────────────────────────────
    "Northwest Side":    [41.9600, -87.7200],
    "Jefferson Park":    [41.9703, -87.7681],
    "Edgebrook":         [41.9987, -87.7564],
    "Forest Glen":       [41.9957, -87.7444],
    "Norwood Park":      [41.9889, -87.8079],
    "Gladstone Park":    [41.9817, -87.7671],
    "Portage Park":      [41.9570, -87.7676],
    "Irving Park":       [41.9544, -87.7261],
    "Albany Park":       [41.9685, -87.7270],
    "Avondale":          [41.9426, -87.7068],
    "Logan Square":      [41.9217, -87.7070],
    "Belmont Cragin":    [41.9417, -87.7662],
    "Hermosa":           [41.9213, -87.7354],
    "Bucktown":          [41.9177, -87.6849],
    "Wicker Park":       [41.9085, -87.6793],
    "Ukrainian Village": [41.8943, -87.6747],
    "West Town":         [41.8954, -87.6716],
    "River West":        [41.8863, -87.6665],
    "Mayfair":           [41.9686, -87.7538],
    # ── West Side ─────────────────────────────────────────────────────────
    "West Side":         [41.8820, -87.7400],
    "Austin":            [41.8990, -87.7658],
    "West Garfield Park":[41.8800, -87.7400],
    "East Garfield Park":[41.8821, -87.7186],
    "Garfield Park":     [41.8820, -87.7188],
    "North Lawndale":    [41.8660, -87.7205],
    "Lawndale":          [41.8660, -87.7205],
    "South Lawndale":    [41.8551, -87.7191],
    "Little Village":    [41.8489, -87.7191],
    "Humboldt Park":     [41.9003, -87.7215],
    "West Loop":         [41.8827, -87.6467],
    "Near West Side":    [41.8781, -87.6658],
    "Pilsen":            [41.8544, -87.6623],
    "Lower West Side":   [41.8544, -87.6623],
    # ── South Side ────────────────────────────────────────────────────────
    "South Side":        [41.7600, -87.6200],
    "Loop":              [41.8827, -87.6293],
    "South Loop":        [41.8635, -87.6270],
    "Near South Side":   [41.8562, -87.6221],
    "Bridgeport":        [41.8312, -87.6508],
    "Armour Square":     [41.8479, -87.6338],
    "Chinatown":         [41.8513, -87.6326],
    "Bronzeville":       [41.8220, -87.6175],
    "Douglas":           [41.8376, -87.6175],
    "Grand Boulevard":   [41.8100, -87.6175],
    "Washington Park":   [41.7936, -87.6153],
    "Woodlawn":          [41.7747, -87.5929],
    "Hyde Park":         [41.7960, -87.5960],
    "Kenwood":           [41.8095, -87.5987],
    "Oakland":           [41.8215, -87.5971],
    "South Shore":       [41.7590, -87.5777],
    "South Chicago":     [41.7363, -87.5618],
    "Gage Park":         [41.8004, -87.7020],
    "McKinley Park":     [41.8299, -87.6731],
    "Brighton Park":     [41.8220, -87.6916],
    "Back of the Yards": [41.8047, -87.6597],
    "New City":          [41.8047, -87.6597],
    "West Englewood":    [41.7800, -87.6660],
    "Englewood":         [41.7730, -87.6460],
    "Greater Grand Crossing": [41.7644, -87.5996],
    "Auburn Gresham":    [41.7511, -87.6627],
    "Chatham":           [41.7500, -87.6060],
    "Avalon Park":       [41.7383, -87.5793],
    "Burnside":          [41.7253, -87.6017],
    "Calumet Heights":   [41.7244, -87.5853],
    "Roseland":          [41.6930, -87.6220],
    "Pullman":           [41.7069, -87.6085],
    "West Pullman":      [41.6890, -87.6436],
    "Riverdale":         [41.6449, -87.6282],
    "Altgeld Gardens":   [41.6449, -87.6282],
    "South Deering":     [41.7053, -87.5568],
    "East Side":         [41.7208, -87.5504],
    "Southeast Side":    [41.7208, -87.5504],
    "Morgan Park":       [41.6947, -87.6644],
    "Beverly":           [41.7196, -87.6744],
    "Mount Greenwood":   [41.6997, -87.7077],
    "North Lawndale / Citywide": [41.8660, -87.7205],
    # ── Southwest Side ────────────────────────────────────────────────────
    "Southwest Side":    [41.8100, -87.7000],
    "Chicago Lawn":      [41.7746, -87.6951],
    "Marquette Park":    [41.7746, -87.6951],
    # ── Suburbs ───────────────────────────────────────────────────────────
    "Chicago Suburbs":   [41.8781, -87.6298],
    "Evanston":          [42.0450, -87.6877],
    "Skokie":            [42.0334, -87.7334],
    "Oak Park":          [41.8850, -87.7845],
    "Berwyn":            [41.8506, -87.7940],
    "Cicero":            [41.8456, -87.7539],
    "Harvey":            [41.6100, -87.6469],
    "Blue Island":       [41.6558, -87.6833],
    "Robbins":           [41.6350, -87.7061],
    "South Suburbs":     [41.6558, -87.6833],
    "La Grange":         [41.8081, -87.8694],
    "Elmhurst":          [41.8995, -87.9403],
    "Schaumburg":        [42.0334, -88.0834],
    "Glenwood":          [41.5375, -87.6050],
    "Chicagoland":       [41.8781, -87.6298],
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
    """Load locations.csv, geocode any rows that are missing coordinates, and save.

    On CI (GitHub Actions) we skip live geocoding to avoid flaky network calls —
    any rows without coordinates are simply omitted from the GeoJSON and the
    neighbourhood-centroid fallback in build_geojson() picks them up instead.
    """
    loc_file = DATA_DIR / "locations.csv"
    if not loc_file.exists():
        return []

    with open(loc_file, "r", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    # Detect CI environment — skip live API calls to avoid build failures
    is_ci = os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS")
    if is_ci:
        print("  CI environment detected — skipping live geocoding, using cached coordinates only.")
        return rows

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


def load_addr_research():
    """Load address research results written by research subagents.
    Returns dict of group_id -> {street_address, city, state, zip, location_type, location_note}.
    """
    result = {}
    batch_dir = DATA_DIR / "addr_batches"
    if not batch_dir.exists():
        return result
    for path in sorted(batch_dir.glob("result_*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                entries = json.load(f)
            for e in entries:
                gid = e.get("group_id")
                if gid:
                    result[gid] = e
        except Exception as ex:
            print(f"  Warning: could not load {path.name}: {ex}")
    return result


def build_geojson(groups, locations):
    """Build a GeoJSON FeatureCollection from known locations + neighbourhood fallbacks.

    Each feature includes:
      location_type: 'EXACT' | 'ESTIMATED'
      location_note: source or reasoning for the coordinate
    """
    features = []
    mapped_ids = {loc["group_id"] for loc in locations if loc.get("latitude")}

    # Load any address research results produced by subagents
    addr_research = load_addr_research()
    print(f"  Loaded address research for {len(addr_research)} groups")

    # ── Pass 1: exact locations from locations.csv ───────────────────────
    for loc in locations:
        if not (loc.get("latitude") and loc.get("longitude")):
            continue
        g = next((g for g in groups if g["group_id"] == loc["group_id"]), {})
        research = addr_research.get(loc["group_id"], {})
        loc_note = research.get("location_note") or loc.get("location_note") or "Address from locations.csv"
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
                "location_type": "EXACT",
                "location_note": loc_note,
            },
        })

    # ── Pass 2: address research results (exact addresses found by agents) ─
    for g in groups:
        if g["group_id"] in mapped_ids:
            continue
        research = addr_research.get(g["group_id"])
        if research and research.get("location_type") == "EXACT" and research.get("street_address"):
            addr = research["street_address"]
            city = research.get("city", "Chicago")
            state = research.get("state", "IL")
            # Try geocoding the found address
            lat, lon = geocode_address(addr, city)
            if lat and lon:
                mapped_ids.add(g["group_id"])
                features.append({
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [float(lon), float(lat)],
                    },
                    "properties": {
                        "group_id": g["group_id"],
                        "name": g["name"],
                        "location_name": addr,
                        "address": f"{addr}, {city}, {state}",
                        "verification_status": g.get("verification_status", "UNCERTAIN"),
                        "category": g.get("category", ""),
                        "location_type": "EXACT",
                        "location_note": research.get("location_note", "Address found via research"),
                    },
                })

    # ── Pass 3: estimated locations — research result or neighbourhood centroid ─
    for g in groups:
        if g["group_id"] in mapped_ids:
            continue
        research = addr_research.get(g["group_id"])
        hood = re.split(r"[,/&]", g.get("neighborhood") or "")[0].strip()
        coords = next(
            (v for k, v in HOOD_GEO.items() if k.lower() in hood.lower()), None
        )
        # If research said ESTIMATED and gave a note, use that note
        if research and research.get("location_type") == "ESTIMATED":
            loc_note = research.get("location_note") or (
                f"No fixed address found. Estimated from listed neighborhood: '{hood}'."
            )
        else:
            loc_note = f"No verified address found. Pin placed at approximate centre of '{hood or 'Chicago'}' based on group's listed service area."

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
                    "location_name": "Estimated location",
                    "address": hood,
                    "verification_status": g.get("verification_status", "UNCERTAIN"),
                    "category": g.get("category", ""),
                    "location_type": "ESTIMATED",
                    "location_note": loc_note,
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

    groups_json = json.dumps(groups).replace('</', '<\\/')
    geojson_json = json.dumps(geojson).replace('</', '<\\/')
    script_block = (
        "\n<script>\n"
        "/* DATA_INJECTION_START */\n"
        "window.CHICAGO_CORPS_DATA = {\n"
        "  generated_at: '" + datetime.now().isoformat() + "',\n"
        "  groups: " + groups_json + ",\n"
        "  geojson: " + geojson_json + "\n"
        "};\n"
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
