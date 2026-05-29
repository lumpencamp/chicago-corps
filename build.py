#!/usr/bin/env python3
"""
Chicago Corps — Build Script
Validates CSV files, converts to JSON, generates site data, flags stale entries.
Run: python build.py
"""

import csv
import json
import os
from datetime import datetime
from pathlib import Path

DATA_DIR = Path("data")
OUTPUT_DIR = Path("_data")

# ── Schema ─────────────────────────────────────────────────────

REQUIRED_FIELDS = {
    "groups.csv": [
        "group_id", "name", "category", "neighborhood", "description",
        "verification_status", "last_verified_date", "evidence_summary",
        "source", "last_updated"
    ],
    "contacts.csv": ["group_id", "last_updated"],
    "locations.csv": ["group_id", "location_id", "city", "last_updated"],
    "volunteer_needs.csv": ["group_id", "accepting_volunteers", "last_updated"],
    "outreach_log.csv": [
        "outreach_id", "group_id", "contact_date",
        "contact_method", "contact_address"
    ],
    "verification_log.csv": [
        "verification_id", "group_id", "verification_date",
        "status_after", "evidence_type", "evidence_url",
        "evidence_date", "evidence_summary"
    ],
    "coalitions.csv": [
        "parent_group_id", "child_group_id",
        "relationship_type", "last_updated"
    ],
}

VALID_STATUSES = {"VERIFIED", "LIKELY_ACTIVE", "UNCERTAIN", "STALE", "INACTIVE"}
VALID_CATEGORIES = {
    "Mutual Aid - General", "Food Security", "Healthcare & Wellness",
    "Social Justice", "Harm Reduction", "Legal Aid & Community Law",
    "Arts & Culture", "Housing Justice", "Domestic Violence Support",
    "Migrant & Immigrant Support", "Community Advocacy",
    "Environmental & Green Space", "Environmental Justice",
    "Prison Abolition & Solidarity", "Youth & Education",
    "Indigenous Solidarity", "Community Development",
    "Worker Co-ops & Economic Justice", "LGBTQ+ Support",
    "Senior & Elder Support",
}

STALE_THRESHOLD_DAYS = 180

errors = []
warnings = []


def validate_csv(filename):
    filepath = DATA_DIR / filename
    if not filepath.exists():
        warnings.append(f"SKIP: {filename} not found")
        return []

    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    required = REQUIRED_FIELDS.get(filename, [])
    headers = reader.fieldnames or []

    for field in required:
        if field not in headers:
            errors.append(f"MISSING FIELD: {filename} — '{field}'")

    for i, row in enumerate(rows, start=2):
        for field in required:
            if not row.get(field, "").strip():
                errors.append(f"EMPTY: {filename}:{i} — '{field}'")

        status = row.get("verification_status", "")
        if status and status not in VALID_STATUSES:
            errors.append(f"INVALID STATUS: {filename}:{i} — '{status}'")

        cat = row.get("category", "")
        if cat and cat not in VALID_CATEGORIES:
            errors.append(f"INVALID CATEGORY: {filename}:{i} — '{cat}'")

        vdate = row.get("last_verified_date", "")
        if vdate:
            try:
                vd = datetime.strptime(vdate, "%Y-%m-%d")
                age = (datetime.now() - vd).days
                if age > STALE_THRESHOLD_DAYS:
                    name = row.get("name", row.get("group_id", "?"))
                    warnings.append(f"STALE: {name} — {age} days since verification")
            except ValueError:
                pass

    return rows


def csv_to_json(filename):
    rows = validate_csv(filename)
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = OUTPUT_DIR / filename.replace(".csv", ".json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2, ensure_ascii=False)
    print(f"  {filename} → {out.name} ({len(rows)} rows)")


def generate_stats():
    try:
        with open(DATA_DIR / "groups.csv", newline="", encoding="utf-8") as f:
            groups = list(csv.DictReader(f))
    except FileNotFoundError:
        return {}

    try:
        with open(DATA_DIR / "contacts.csv", newline="", encoding="utf-8") as f:
            contacts = list(csv.DictReader(f))
    except FileNotFoundError:
        contacts = []

    try:
        with open(DATA_DIR / "volunteer_needs.csv", newline="", encoding="utf-8") as f:
            needs = list(csv.DictReader(f))
    except FileNotFoundError:
        needs = []

    statuses = {}
    categories = {}
    neighborhoods = set()

    for g in groups:
        s = g.get("verification_status", "UNKNOWN")
        statuses[s] = statuses.get(s, 0) + 1
        c = g.get("category", "Uncategorized")
        categories[c] = categories.get(c, 0) + 1
        n = g.get("neighborhood", "")
        if n and n != "Citywide":
            neighborhoods.add(n)

    emails = sum(1 for c in contacts if c.get("email", "").strip())
    phones = sum(1 for c in contacts if c.get("phone", "").strip())
    accepting = sum(
        1 for n in needs
        if n.get("accepting_volunteers", "").upper() == "TRUE"
    )

    stale_count = sum(
        1 for g in groups
        if g.get("last_verified_date") and g["last_verified_date"] != "2025-10-01"
        and (datetime.now() - datetime.strptime(g["last_verified_date"], "%Y-%m-%d")).days > STALE_THRESHOLD_DAYS
    )

    stats = {
        "generated": datetime.now().isoformat(),
        "total_groups": len(groups),
        "verified": statuses.get("VERIFIED", 0),
        "likely_active": statuses.get("LIKELY_ACTIVE", 0),
        "uncertain": statuses.get("UNCERTAIN", 0),
        "contacts_with_email": emails,
        "contacts_with_phone": phones,
        "accepting_volunteers": accepting,
        "neighborhoods_covered": len(neighborhoods),
        "stale_count": stale_count,
        "categories": dict(sorted(categories.items(), key=lambda x: -x[1])),
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_DIR / "stats.json", "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"  stats.json ({len(groups)} groups, {len(neighborhoods)} neighborhoods)")

    return stats


def generate_geojson():
    try:
        with open(DATA_DIR / "locations.csv", newline="", encoding="utf-8") as f:
            locations = list(csv.DictReader(f))
    except FileNotFoundError:
        return

    features = []
    for loc in locations:
        lat = loc.get("latitude", "").strip()
        lon = loc.get("longitude", "").strip()
        if not lat or not lon:
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [float(lon), float(lat)]},
            "properties": {
                "group_id": loc.get("group_id", ""),
                "name": loc.get("location_name", ""),
                "type": loc.get("location_type", ""),
                "address": loc.get("street_address", ""),
                "zip": loc.get("zip_code", ""),
                "community_area": loc.get("community_area", ""),
            }
        })

    geojson = {"type": "FeatureCollection", "features": features}
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(OUTPUT_DIR / "locations.geojson", "w", encoding="utf-8") as f:
        json.dump(geojson, f, indent=2, ensure_ascii=False)
    print(f"  locations.geojson ({len(features)} points)")


# ── Main ────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Chicago Corps — Build\n")

    for fname in REQUIRED_FIELDS:
        validate_csv(fname)

    if errors:
        print(f"\n{len(errors)} ERROR(S):")
        for e in errors:
            print(f"  {e}")
    if warnings:
        print(f"\n{len(warnings)} WARNING(S):")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print("\nBuild failed — fix errors above.")
        exit(1)

    print("\nConverting:")
    for fname in REQUIRED_FIELDS:
        csv_to_json(fname)

    print("\nGenerating site data:")
    generate_stats()
    generate_geojson()

    print(f"\nDone — {len(warnings)} warning(s)")
