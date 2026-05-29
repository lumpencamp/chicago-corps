# Chicago Corps

> A verified, living directory of mutual aid and community support groups across the Chicago area.

**77 groups** · **21 categories** · **40+ neighborhoods** · **72 verified active**

🌐 **[lumpencamp.github.io/chicago-corps](https://lumpencamp.github.io/chicago-corps/)**

---

## What is this?

Chicago Corps is an open-data directory built to make it easier to find and connect with mutual aid organizations, community support groups, food pantries, legal aid clinics, harm reduction programs, and solidarity networks in and around Chicago.

Every entry has a `verification_status` backed by evidence — a live website check, recent social media activity, news coverage, or direct outreach. No stale lists from 2020.

---

## Features

- 🔍 **Live search** — filter by name, neighborhood, category, or keyword
- 🗂️ **Category filter** — 21 categories from Food Security to Prison Abolition
- 📍 **Neighborhood filter** — 40+ Chicago neighborhoods and suburbs
- 🙋 **Volunteer filter** — shows the 16 groups confirmed to be accepting volunteers
- 🗺️ **Interactive map** — all groups plotted on a dark map with color-coded verification status markers
- 📊 **Verification status** — every group rated VERIFIED / LIKELY_ACTIVE / UNCERTAIN / STALE

---

## Data

The core dataset is [`chicago_mutual_aid_groups.csv`](chicago_mutual_aid_groups.csv) — open it in any spreadsheet app to browse, filter, and sort.

| File | Description |
|------|-------------|
| `chicago_mutual_aid_groups.csv` | 77 groups — name, category, neighborhood, description, website, social, verification status |
| `data/contacts.csv` | Email, phone, contact forms — 38 entries |
| `data/locations.csv` | Street addresses + community areas — 22 locations |
| `data/volunteer_needs.csv` | 16 groups confirmed accepting volunteers with roles and requirements |
| `data/verification_log.csv` | Evidence trail for each verification decision |
| `data/outreach_log.csv` | Direct contact attempts log |
| `data/coalitions.csv` | Coalition and umbrella organization relationships |

### Verification statuses

| Status | Meaning |
|--------|---------|
| `VERIFIED` | Active within 6 months, confirmed by direct evidence |
| `LIKELY_ACTIVE` | Website or social present, no recent direct confirmation |
| `UNCERTAIN` | Referenced in directories but hard to verify independently |
| `STALE` | No activity found in 6+ months |
| `INACTIVE` | Confirmed dissolved or inactive |

---

## Contributing

### Add or update a group

1. Open a [GitHub Issue](https://github.com/lumpencamp/chicago-corps/issues) with the group name and any links
2. Or fork the repo, edit `chicago_mutual_aid_groups.csv`, and open a pull request

### Validate data locally

```bash
python build.py
```

Checks required fields, validates status/category values, and flags stale entries (>180 days since last verification).

### Run the site locally

The site is a single self-contained `index.html` — no build step needed:

```bash
open index.html
# or: python -m http.server 8000
```

---

## Project Structure

```
chicago-corps/
├── index.html                     # The live directory site
├── chicago_mutual_aid_groups.csv  # Core dataset — 77 groups
├── build.py                       # CSV validation + stats + GeoJSON generator
├── .nojekyll                      # Tells GitHub Pages to serve static HTML directly
├── data/
│   ├── contacts.csv
│   ├── locations.csv
│   ├── volunteer_needs.csv
│   ├── outreach_log.csv
│   ├── verification_log.csv
│   └── coalitions.csv
├── schema.md                      # Full data schema documentation
├── taxonomy.md                    # Category and tag taxonomy
├── sources/sources.md             # Source inventory
└── coverage/gaps.md               # Neighborhood gap analysis
```

---

## Deployment

Hosted on GitHub Pages as a static site (no Jekyll, no build step):

- Push to `main` → GitHub Actions automatically deploys
- Live at: `https://lumpencamp.github.io/chicago-corps/`

To use a custom domain, add a `CNAME` file with the domain and configure DNS with your provider.

---

## License

Data in this repository is sourced from public websites, directories, and news coverage. It is shared for community use under the spirit of mutual aid — freely available, freely improvable.

If you represent a listed organization and would like your information updated or removed, please [open an issue](https://github.com/lumpencamp/chicago-corps/issues) and we'll take care of it promptly.
