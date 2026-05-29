# Chicago Corps

A verified directory of mutual aid and community support groups in the Chicago area. Built to match volunteers with organizations that need them.

**77 groups** across **20 categories** covering North, South, West, Southwest sides + suburbs.  
**38 groups** have verified contact information. **16 groups** are confirmed accepting volunteers.

🌐 **[View the directory →](https://lumpencamp.github.io/chicago-corps/)**

---

## Quick Start

### Browse the data

Open `chicago_mutual_aid_groups.csv` in any spreadsheet app. Filter by `neighborhood` to find groups near you, or by `category` to find groups doing work you care about.

### Run the dashboard

```bash
open dashboard.html
```

A self-contained HTML page that reads the CSV files and displays live stats, a coverage map, stale data alerts, and category breakdowns. No server required.

### Build the site

```bash
python build.py       # Validate CSVs + generate JSON + stats + GeoJSON
jekyll serve           # Run locally at http://localhost:4000
```

### Contribute

See `schema.md` for the data model. To add a group:

1. Add a row to `data/groups.csv` with a unique `group_id`
2. Add contact info to `data/contacts.csv` using the same `group_id`
3. Add location data to `data/locations.csv`
4. Add a verification event to `data/verification_log.csv`
5. Run `python build.py` to validate

---

## Project Structure

```
├── _config.yml                # Jekyll config for GitHub Pages
├── build.py                   # CSV validation + JSON conversion + stats
├── dashboard.html             # Internal pipeline dashboard
├── data/
│   ├── groups.csv             # Core directory — 77 groups
│   ├── contacts.csv           # Email, phone, contact forms — 38 entries
│   ├── locations.csv          # Addresses + community areas — 22 locations
│   ├── volunteer_needs.csv    # Groups accepting volunteers — 16 confirmed
│   ├── volunteers.csv         # Volunteer intake schema
│   ├── outreach_log.csv       # Contact tracking
│   ├── verification_log.csv   # Evidence trail
│   └── coalitions.csv         # Parent/child relationships
├── coverage/gaps.md           # Neighborhood gap analysis
└── sources/sources.md         # Source inventory
```

---

## Data Freshness

Every group has a `verification_status` and `last_verified_date`. Groups unverified for 6+ months are flagged as STALE and hidden from volunteer matching. The `build.py` script surfaces stale entries automatically.

---

## License

This project shares publicly available information about community organizations. All data is sourced from public websites, directories, and news coverage. If you represent a listed organization and would like your information updated or removed, please open an issue or contact us.

---

## Deployment

This site is designed for **GitHub Pages** with Jekyll:

```bash
# First time
git init
git add .
git commit -m "Initial commit: Chicago Corps directory"
git branch -M main
git remote add origin git@github.com:USERNAME/chicago-corps.git
git push -u origin main

# Enable GitHub Pages in repo Settings → Pages → Source: GitHub Actions (Jekyll)
```

The site will be live at `https://lumpencamp.github.io/chicago-corps/`.

To use a custom domain (e.g. chicagocorps.org), add a `CNAME` file containing the domain name and configure DNS with your provider.
