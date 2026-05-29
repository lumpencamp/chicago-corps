# Data Schema — Chicago Corps

Every field, type, constraint, and example for each data file. Use this as the authoritative reference when adding or editing entries.

---

## groups.csv

The core directory. One row per organization. `group_id` is the primary key used across all files.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `group_id` | string | **Yes** | Unique, lowercase, kebab-case, stable across renames | `bridgeport-alliance` |
| 2 | `name` | string | **Yes** | Full public-facing name, including acronym in parens if commonly used | `Bridgeport Alliance` |
| 3 | `category` | string | **Yes** | Must match a category in `taxonomy.md` | `Community Advocacy` |
| 4 | `neighborhood` | string | **Yes** | Chicago community area name, neighborhood, "Citywide", or suburban municipality | `Bridgeport` |
| 5 | `description` | string | **Yes** | 1-3 sentences. What they do, who they serve, how they operate. No markdown. | `Grassroots organization of residents...` |
| 6 | `website` | string | No | Full HTTPS URL. Empty string if none. | `https://actionnetwork.org/groups/bridgeport-alliance` |
| 7 | `social_media` | string | No | Space-separated URLs for Instagram, Facebook, Twitter, Linktree, etc. | `https://www.instagram.com/bridgeportalliance/ https://linktr.ee/BridgeportAlliance` |
| 8 | `verification_status` | enum | **Yes** | `VERIFIED`, `LIKELY_ACTIVE`, `UNCERTAIN`, `STALE`, `INACTIVE` | `VERIFIED` |
| 9 | `last_verified_date` | date | **Yes** | ISO 8601 (YYYY-MM-DD). The date evidence was observed, not the date the entry was added. | `2025-11-15` |
| 10 | `evidence_url` | string | No | URL to the specific post, event page, news article, or other public artifact proving recent activity. | `https://www.instagram.com/p/example/` |
| 11 | `evidence_summary` | string | **Yes** | 1-sentence summary of what the evidence shows. | `Instagram post Nov 15 2025 advertising monthly meeting` |
| 12 | `source` | string | **Yes** | Comma-separated list of sources where this group was discovered or verified. | `Organize Directory, web_search, fetch_url` |
| 13 | `last_updated` | date | **Yes** | ISO 8601. Date this row was last modified. | `2026-05-29` |
| 14 | `priority` | enum | No | `HIGH`, `MEDIUM`, `LOW`. Based on mission alignment and volunteer need signal. | `HIGH` |
| 15 | `data_quality` | enum | No | `CLEAN`, `NEEDS_REVIEW`, `DUPLICATE_SUSPECT`, `STALE` | `CLEAN` |
| 16 | `notes` | string | No | Internal notes. Not for public consumption. | `Listed in multiple directories under slightly different names` |

### `group_id` Convention

- Lowercase, hyphen-separated
- Based on the most commonly used short name
- Stable — do not change if the group rebrands (add a `notes` entry instead)
- Examples: `bridgeport-alliance`, `love-fridge-chicago`, `uchrp`

---

## contacts.csv

Contact information. Separate from `groups.csv` so contact data can be updated independently and optionally kept private.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `group_id` | string | **Yes** | Foreign key to `groups.csv` | `bridgeport-alliance` |
| 2 | `email` | string | No | Public-facing email only. Empty if none found. | `info@example.org` |
| 3 | `phone` | string | No | Public-facing phone only. Format: `(312) 555-0100`. Empty if none. | `(312) 555-0100` |
| 4 | `contact_form_url` | string | No | URL to a web contact/volunteer form, if no direct email is available. | `https://example.org/volunteer` |
| 5 | `contact_name` | string | No | Name of a known contact person, if publicly listed. | `Andrea Yarbrough` |
| 6 | `contact_role` | string | No | Role/title of contact person if known. | `Co-founder` |
| 7 | `preferred_method` | enum | No | `email`, `phone`, `contact_form`, `social_dm`, `unknown` | `email` |
| 8 | `last_updated` | date | **Yes** | ISO 8601. | `2026-05-29` |

### Privacy note

Only publicly listed contact information should be recorded. Do not add personal emails or phone numbers obtained through private channels.

---

## locations.csv

Geographic precision. One row per physical location a group operates from. A group may have multiple rows if it operates multiple sites (e.g., The Love Fridge has 25+ fridge locations).

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `group_id` | string | **Yes** | Foreign key to `groups.csv` | `love-fridge-chicago` |
| 2 | `location_id` | string | **Yes** | Unique per location. `{group_id}-{slug}` | `love-fridge-chicago-bridgeport` |
| 3 | `location_name` | string | No | Human-readable name for this location. | `The Fridge on Marz` |
| 4 | `street_address` | string | No | Full street address if publicly listed. | `3630 S Iron St` |
| 5 | `city` | string | **Yes** | Default `Chicago`. | `Chicago` |
| 6 | `zip_code` | string | No | 5-digit ZIP. | `60609` |
| 7 | `community_area` | string | No | Official Chicago community area name (77 total). | `Bridgeport` |
| 8 | `community_area_number` | integer | No | 1-77. | `60` |
| 9 | `latitude` | float | No | Decimal degrees. | `41.8275` |
| 10 | `longitude` | float | No | Decimal degrees. | `-87.6543` |
| 11 | `location_type` | enum | No | `headquarters`, `fridge`, `pantry`, `garden`, `clinic`, `office`, `popup`, `other` | `fridge` |
| 12 | `is_primary` | boolean | No | `TRUE` if this is the main location. | `TRUE` |
| 13 | `last_updated` | date | **Yes** | ISO 8601. | `2026-05-29` |

---

## volunteer_needs.csv

Tracks which groups actively seek volunteers and what the process looks like.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `group_id` | string | **Yes** | Foreign key to `groups.csv` | `urban-growers-collective` |
| 2 | `accepting_volunteers` | boolean | **Yes** | `TRUE`, `FALSE`, or empty if unknown | `TRUE` |
| 3 | `volunteer_url` | string | No | Direct link to volunteer signup page or form. | `https://www.urbangrowerscollective.org/volunteer` |
| 4 | `application_process` | string | No | How to apply: `online_form`, `email_inquiry`, `show_up`, `training_required`, `application_required` | `online_form` |
| 5 | `requirements` | string | No | Background check, age minimum, training, skills needed. | `Must be 18+. Orientation required.` |
| 6 | `time_commitment` | string | No | Expected commitment. | `2-4 hours/week, 3-month minimum` |
| 7 | `roles_available` | string | No | Types of volunteer roles. | `Farm work, food distribution, youth mentoring` |
| 8 | `remote_available` | boolean | No | `TRUE` if remote/virtual volunteering is possible. | `FALSE` |
| 9 | `last_confirmed` | date | No | Date this information was last confirmed with the group. | `2026-05-15` |
| 10 | `last_updated` | date | **Yes** | ISO 8601. | `2026-05-29` |

---

## outreach_log.csv

Contact attempt tracking. One row per contact attempt. Multiple rows per group allowed.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `outreach_id` | string | **Yes** | Unique. `{group_id}-{iso_date}-{attempt_number}` | `bridgeport-alliance-2026-05-29-1` |
| 2 | `group_id` | string | **Yes** | Foreign key to `groups.csv` | `bridgeport-alliance` |
| 3 | `contact_date` | date | **Yes** | Date contact was attempted. | `2026-05-29` |
| 4 | `contact_method` | enum | **Yes** | `email`, `phone`, `contact_form`, `social_dm`, `in_person` | `email` |
| 5 | `contact_address` | string | **Yes** | The email/phone/handle used. | `info@example.org` |
| 6 | `outcome` | enum | No | `sent`, `delivered`, `opened`, `replied`, `bounced`, `no_response`, `declined`, `interested`, `scheduled` | `replied` |
| 7 | `response_summary` | string | No | Brief summary of response if any. | `Replied same day. Interested in volunteers. Asked us to fill out their form.` |
| 8 | `follow_up_needed` | boolean | No | `TRUE` if follow-up is required. | `TRUE` |
| 9 | `follow_up_date` | date | No | Date to follow up if no response. | `2026-06-12` |
| 10 | `notes` | string | No | Internal notes. | `Email bounced. Try contact form next.` |

---

## verification_log.csv

Verification event tracking. One row per verification check. Supports re-verification over time.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `verification_id` | string | **Yes** | Unique. `{group_id}-{iso_date}` | `bridgeport-alliance-2026-05-29` |
| 2 | `group_id` | string | **Yes** | Foreign key to `groups.csv` | `bridgeport-alliance` |
| 3 | `verification_date` | date | **Yes** | Date the verification was performed. | `2026-05-29` |
| 4 | `status_after` | enum | **Yes** | The status assigned after this check. | `VERIFIED` |
| 5 | `evidence_type` | enum | **Yes** | `social_media_post`, `website_live`, `news_article`, `event_listing`, `directory_listing`, `direct_contact`, `other` | `social_media_post` |
| 6 | `evidence_url` | string | **Yes** | Direct URL to the evidence artifact. | `https://www.instagram.com/p/example/` |
| 7 | `evidence_date` | date | **Yes** | The date on the evidence itself (post date, article date). | `2025-11-15` |
| 8 | `evidence_summary` | string | **Yes** | 1-sentence description. | `Instagram post advertising monthly community meeting` |
| 9 | `verification_method` | string | No | How the verification was done. | `fetch_url + web_search` |

---

## coalitions.csv

Models parent/child relationships between groups. Used when a coalition contains member organizations that are also listed individually.

| # | Field | Type | Required | Constraints | Example |
|---|---|---|---|---|---|
| 1 | `parent_group_id` | string | **Yes** | Foreign key to `groups.csv`. The coalition or umbrella. | `chicago-housing-justice-coalition` |
| 2 | `child_group_id` | string | **Yes** | Foreign key to `groups.csv`. The member organization. | `chicago-tenants-movement` |
| 3 | `relationship_type` | enum | **Yes** | `coalition_member`, `fiscal_sponsor`, `chapter_of`, `network_partner` | `coalition_member` |
| 4 | `last_updated` | date | **Yes** | ISO 8601. | `2026-05-29` |

---

## Field Type Reference

| Type | Format | Example |
|---|---|---|
| `string` | Free text, no commas (CSV-safe) | `Bridgeport` |
| `enum` | One of a fixed set of values | `VERIFIED` |
| `boolean` | `TRUE` or `FALSE` | `TRUE` |
| `date` | ISO 8601 `YYYY-MM-DD` | `2026-05-29` |
| `integer` | Whole number | `60` |
| `float` | Decimal number | `41.8275` |

---

## CSV Encoding Rules

- UTF-8 encoding
- Fields containing commas must be double-quoted
- Double quotes within fields must be escaped as `""`
- No trailing whitespace
- Header row required on line 1
- Empty optional fields: leave blank (no placeholder like `N/A`)
- URLs: full `https://` prefix required
- Dates: always `YYYY-MM-DD`, never `MM/DD/YYYY`
