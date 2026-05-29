# Contributing to Chicago Corps

> A verified, living directory of mutual aid and community support groups across the Chicago area.
> Live at **[lumpencamp.github.io/chicago-corps](https://lumpencamp.github.io/chicago-corps/)**

---

## How to Add or Update a Group

The easiest way is to [open an issue](https://github.com/lumpencamp/chicago-corps/issues/new) with the group's name, website, neighborhood, and any notes.

If you're comfortable with GitHub, you can also edit [`chicago_mutual_aid_groups.csv`](./chicago_mutual_aid_groups.csv) directly and submit a pull request.

### CSV Fields

| Field | Description |
|---|---|
| `name` | Full name of the group |
| `category` | One of the [valid categories](#categories) below |
| `neighborhood` | Chicago neighborhood(s), or `Citywide` |
| `description` | 1–3 sentence description |
| `website` | Full URL including `https://` |
| `social_media` | URL to primary social account |
| `contact_info` | Name, email, or phone (if public) |
| `verification_status` | See [status guide](#verification-status) below |
| `last_verified_activity` | YYYY-MM-DD of most recent confirmed activity |
| `verification_evidence` | Brief note on how the status was confirmed |
| `source` | Where the information came from |

---

## Verification Status

| Status | Meaning |
|---|---|
| `VERIFIED` | Confirmed active within ~6 months via website, social, or news |
| `LIKELY_ACTIVE` | Strong signals of activity but not fully confirmed |
| `UNCERTAIN` | Mixed signals — needs more research |
| `STALE` | No confirmed activity in 6+ months |
| `INACTIVE` | Confirmed closed or no longer operating |

---

## Categories

```
Mutual Aid - General
Food Security
Healthcare & Wellness
Social Justice
Harm Reduction
Legal Aid & Community Law
Arts & Culture
Housing Justice
Domestic Violence Support
Migrant & Immigrant Support
Community Advocacy
Environmental & Green Space
Environmental Justice
Prison Abolition & Solidarity
Youth & Education
Indigenous Solidarity
Community Development
Worker Co-ops & Economic Justice
LGBTQ+ Support
Senior & Elder Support
```

---

## Relational Data Files

Additional context is tracked in `data/`:

| File | Contents |
|---|---|
| `locations.csv` | Street addresses and geocoded lat/lon for physical locations |
| `contacts.csv` | Verified contact emails and forms by `group_id` |
| `donation_needs.csv` | Specific items or funds groups are currently seeking |
| `urgent_needs.csv` | Groups with critical or time-sensitive needs |
| `languages.csv` | Languages served and languages needed |
| `volunteer_needs.csv` | Groups accepting volunteers and their requirements |
| `coalitions.csv` | Coalition and partnership relationships between groups |
| `verification_log.csv` | History of verification checks |

Groups are linked across files using a `group_id` slug auto-generated from the group name (e.g., `cooperation-racine`).

---

## Build Process

The site is a static HTML page with data baked in at build time.

```bash
python3 build.py
```

This reads `chicago_mutual_aid_groups.csv` and the `data/` files, geocodes any new addresses (via OpenStreetMap Nominatim), and injects all data inline into `index.html`. No server or fetch calls needed.

The build runs automatically via GitHub Actions whenever `chicago_mutual_aid_groups.csv` or any `data/` file is pushed.

---

## Local Dev

Just open `index.html` in a browser — no build step required for viewing, since the data is already baked in.
