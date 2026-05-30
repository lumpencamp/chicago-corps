# Chicago Corps

A verified directory of mutual aid and community support groups in the Chicago area. Built to match volunteers with organizations that need them.

**115 groups** across **20 categories** covering 61+ neighborhoods across Chicago and suburbs.  
**50 groups** have contact info on file. **24 locations** geocoded for the interactive map.

🌐 **[View the directory →](https://lumpencamp.github.io/chicago-corps/)**

---

## Quick Start

### Browse the data

Open `chicago_mutual_aid_groups.csv` in any spreadsheet app. Filter by `neighborhood` to find groups near you, or by `category` to find groups doing work you care about.

### Build the site

```bash
python build.py       # Geocode locations, generate JSON, inject data into index.html
open index.html       # View locally
```

No server required — everything is baked into a single static HTML file. The interactive map uses Leaflet with CARTO dark tiles.

### Contribute

To add a group:

1. Add a row to `chicago_mutual_aid_groups.csv`
2. Optionally add contact info to `data/contacts.csv` with a matching group_id
3. Optionally add location data to `data/locations.csv`
4. Run `python build.py` to geocode, regenerate, and inject the data
5. Commit and push — the GitHub Pages site rebuilds automatically

See `schema.md` for the full data model, `taxonomy.md` for category definitions, and `coverage/gaps.md` for neighborhood coverage analysis.

---

## Project Structure

```
├── index.html                  # The site — self-contained, data baked in at build time
├── chicago_mutual_aid_groups.csv # Canonical group data (115 groups)
├── build.py                    # Build script: geocodes, injects data into index.html
├── dashboard.html              # Internal pipeline dashboard (reads CSVs client-side)
│
├── data/
│   ├── groups.csv              # Structured group data (alternate format)
│   ├── contacts.csv            # Email, phone, contact forms — 50 entries
│   ├── locations.csv           # Addresses + community areas — 24 geocoded locations
│   ├── volunteer_needs.csv     # Groups accepting volunteers — 16 confirmed
│   ├── donation_needs.csv      # In-kind donation needs tracking
│   ├── urgent_needs.csv        # Time-sensitive volunteer/donation alerts
│   ├── events.csv              # One-time volunteer event listings
│   ├── languages.csv           # Languages served and needed by volunteers
│   ├── volunteers.csv          # Volunteer intake schema
│   ├── outreach_log.csv        # Contact tracking
│   ├── verification_log.csv    # Evidence trail
│   └── coalitions.csv          # Parent/child relationships
│
├── _data/                      # Auto-generated build output (api.json, locations.geojson)
├── .github/workflows/
│   ├── deploy.yml              # Auto-builds on CSV changes
│   └── verify.yml              # CI validation
│
├── coverage/gaps.md            # Neighborhood gap analysis
├── sources/sources.md          # Source inventory
├── schema.md                   # Data model reference
├── taxonomy.md                 # Category definitions and counts
└── OPERATIONAL_PLAN.md         # Volunteer-to-group matching strategy
```

---

## How It Works

### Source data
- **`chicago_mutual_aid_groups.csv`** — 115 groups with name, category, neighborhood, description, website, social media, verification status, evidence, and source
- **`data/locations.csv`** — 24 street addresses with group IDs (for precise map placement)
- **`data/contacts.csv`** — 50 email/phone entries

### Build step — `python build.py`

**Geocoding.** For any address in `locations.csv` missing latitude/longitude, Nominatim (OpenStreetMap) resolves it — e.g. `13300 S Baltimore Ave` → `41.667, -87.544`. Geocoded coordinates are saved back to the CSV so subsequent builds skip the lookup.

**GeoJSON generation.** Two passes produce map features:
- *Precise markers* — every location with coordinates becomes a GeoJSON `Point` feature carrying `group_id`, name, verification status, and category
- *Neighborhood fallbacks* — groups without a physical address are placed at their neighborhood's centroid with small random jitter so overlapping dots don't stack

Result: a `FeatureCollection` with 61 features covering all 115 groups.

**HTML injection.** The script opens `index.html`, strips any previous data block, and inserts a `<script>` tag before the main JavaScript:

```javascript
window.CHICAGO_CORPS_DATA = {
  generated_at: '2026-05-30T...',
  groups: [ /* 115 groups as JSON */ ],
  geojson: { "type": "FeatureCollection", "features": [ /* 61 points */ ] }
};
```

### Browser — static single-page app

**`index.html`** is fully self-contained: CSS, HTML, data, and JavaScript in one file. No API calls, no build server, no Jekyll. On load:

1. Leaflet creates the map centered on Chicago with CARTO dark tiles
2. `window.CHICAGO_CORPS_DATA.groups` populates the searchable card grid
3. `window.CHICAGO_CORPS_DATA.geojson.features` draws 61 color-coded dots

**Map markers** are color-coded by verification status: green (VERIFIED), yellow (LIKELY_ACTIVE), orange (UNCERTAIN), red (STALE). Clicking a dot opens a popup with the group name, category, and links. "View details ↓" scrolls to the matching card.

**Search and filters** run client-side — no network requests. The search bar matches against name, category, neighborhood, and description. Category and neighborhood dropdowns narrow results. The 🙋 Volunteers toggle shows only groups accepting volunteers.

### Deployment

Push to `main` → GitHub Pages serves `index.html` directly (`.nojekyll` skips Jekyll processing). The deploy workflow in `.github/workflows/deploy.yml` auto-rebuilds on CSV changes, but a manual Pages rebuild trigger is occasionally needed to unstick the deployment queue.

---

## Data Freshness

Every group has a `verification_status` and `last_verified_activity` date. Groups without verification evidence in 6+ months are flagged as STALE. The `build.py` script surfaces stale entries automatically.

---

## Deployment

```bash
# Site is live at:
https://lumpencamp.github.io/chicago-corps/

# To deploy changes:
git add -A
git commit -m "Update data"
git push origin main
```

GitHub Pages is configured to deploy from the `main` branch (`/` root). The `.nojekyll` file tells Pages to serve files as-is without Jekyll processing. For automated builds on CSV changes, see `.github/workflows/deploy.yml`.

---

## License

This project shares publicly available information about community organizations. All data is sourced from public websites, directories, and news coverage. If you represent a listed organization and would like your information updated or removed, please open an issue.
