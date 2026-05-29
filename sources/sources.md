# Source Inventory — Chicago Corps

Every source used to discover and verify groups. Includes extraction status and notes on what remains.

---

## Fully or Substantially Extracted

| Source | Type | Groups Extracted | Status | Notes |
|---|---|---|---|---|
| ChicagoCore PDF | Baseline spreadsheet | 7 | Done | 7 orgs extracted. 2 UNCERTAIN, 2 LIKELY_ACTIVE, 3 VERIFIED. Original PDF in `chicago-corps/`. |
| Organize Directory | Web directory | ~25 of 55 | Partial | Mutual Aid Networks (14) and Social Justice (4) fully extracted. Housing Justice (5), Food Justice (8 more), Prison Abolition (3 more), Migrant Support (1 more) remain. Page is JS-rendered; full extraction needs browser tool. |
| The Love Fridge Chicago | Mutual aid network | 1 network + 25+ locations | Partial | Network entity added. Individual fridge locations (25+) not individually listed. Locations available at thelovefridge.com/find-a-fridge. |
| Borderless Magazine food pantry guide | News article | Referenced, groups cross-referenced | Partial | Nov 2025 article. ZIP-code-organized food pantry list. Article body not fully extracted (JS-rendered). |
| City Cast Chicago mutual aid explainer | Podcast/article | Referenced | Done | Referenced Market Box Chicago and mutual aid concepts. |
| Chicago Tribune / WTTW / NPR Illinois | News coverage | Referenced | Done | Used for verification evidence (naloxone newsstands, Native American Summit, etc.). |
| Illinois 211 | Resource directory | Referenced | Done | Used for verification of harm reduction and food pantry programs. |
| Cook County resource directories | Government directory | Referenced | Done | Used for legal aid and DV support verification. |

---

## Partially Extracted

| Source | Type | Estimated Remaining | Status | Notes |
|---|---|---|---|---|
| Block Club Chicago — Give Local 2025 | News article | ~40 groups | Not started | 60+ neighborhood initiatives listed. Article body is JS-rendered and was not captured. NewsBreak mirror may work. Author: Kelly Bauer. Date: Nov 25, 2025. |
| CAPS Mutual Aid Map PDF | PDF directory | Unknown | Not started | 5.6 MB PDF from Oct 2025. Contains food pantry/organization listings throughout Chicagoland. Raw binary — needs PDF text extraction or OCR. |
| Facebook — Chicagoland Mutual Aid Group List | Social media post | ~30 groups | Partial | Jan 28, 2025 post by Savannah Hinde-Seeley. Referenced 19th Ward Mutual Aid. Full list not extracted. |

---

## Not Yet Extracted

| Source | Type | Estimated Groups | Notes |
|---|---|---|---|
| LinkedIn — 122 Chicago Mutual Aid Networks | Article | ~50 not yet in dataset | Login-walled. Author: Savannah Hinde-Seeley. Described as "broad list of grassroots mutual aid, harm reduction, and solidarity-based organizations." |
| Sixty Inches From Center — 200+ Resources | Resource list | ~150 not yet extracted | "Resources Towards Solidarity, Care, and Community Defense: Chicago." JS-rendered page. Covers basic needs, solidarity, creative caretaking, organizing. |
| Organize Directory — remaining sections | Web directory | ~17 | Housing Justice (5), Food Justice (8 more), Prison Abolition (3 more), Migrant Support (1 more). |
| Community Kitchen Chicago Mutual Aid Map | Web directory | Unknown | Physical map + PDF download available. Squarespace site — JS-rendered content. |
| After School Matters Mutual Aid Map PDF | PDF directory | Unknown | Identical format to CAPS PDF. Oct 2025. May contain different listings. |
| Chicago Southsider — 10+ Food Pantries on South Side | News article | ~5 not yet in dataset | Curated list. May fill South Side food security gaps. |

---

## Source Quality Ratings

| Source | Reliability | Recency | Structured? | Notes |
|---|---|---|---|---|
| Organize Directory | High | 2025 | Yes | Actively maintained, categorized, includes descriptions and links |
| Block Club Chicago | High | Nov 2025 | No | Journalistic, verified by reporters. Free-text article format |
| CAPS Mutual Aid Map | Medium | Oct 2025 | Yes | PDF format, compiled by a nonprofit. Food-focused only |
| LinkedIn list | Medium | 2025 | Unknown | Personal compilation, not institutionally verified |
| Sixty Inches From Center | High | 2025 | Yes | Curated by arts/culture publication. Broad scope beyond mutual aid |
| Facebook group post | Low-Medium | Jan 2025 | No | Community-sourced, unverified |
| Illinois 211 | High | Ongoing | Yes | Government-maintained resource directory |

---

## Extraction Priority

1. **Organize Directory remaining** — Structured, high-quality, easy to extract. ~17 groups.
2. **Block Club Give Local 2025** — Journalistic, verified, recent. ~40 groups.
3. **CAPS + After School Matters PDFs** — Large compiled lists, but PDF extraction is technically challenging.
4. **LinkedIn 122 list** — Large, but login-walled and unverified.
5. **Sixty Inches From Center** — Largest source (200+), but JS-rendered and broad scope beyond mutual aid.

---

## How to Add a New Source

1. Add a row to the appropriate table above
2. If the source is a URL, record it
3. Note the extraction method that worked (or didn't)
4. Update the extraction status as work progresses
5. Cross-reference extracted groups against existing dataset before adding
