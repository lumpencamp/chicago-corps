# Coverage Gap Analysis — Chicago Corps

Which Chicago neighborhoods and suburbs have zero groups in the dataset, and what that means for the project.

---

## Methodology

Groups were assigned to neighborhoods based on their `neighborhood` field in `groups.csv`. Groups marked "Citywide" (23) were counted separately and not assigned to a specific neighborhood. For the purposes of this analysis, a neighborhood is "covered" if at least one group lists it as its primary service area.

---

## Chicago Community Areas — 77 Total

### Covered (at least one group): ~30 community areas

**North Side (7 of ~12):** Rogers Park, Edgewater, Uptown, Lakeview, Lincoln Park, North Center, Avondale

**Northwest Side (7 of ~12):** Albany Park, Irving Park, Mayfair, Logan Square, Humboldt Park, West Town, Ukrainian Village (subset)

**West Side (5 of ~12):** Austin, East Garfield Park, West Garfield Park, North Lawndale, Pilsen

**South Side (7 of ~20):** Englewood, Woodlawn, Bronzeville, Bridgeport, Hyde Park, South Shore, Chatham

**Southwest Side (4 of ~10):** Mount Greenwood, Morgan Park, Beverly, West Lawn

**Central:** Near North Side, Loop, Near South Side (covered by citywide orgs)

### Uncovered (zero groups): ~30 community areas

#### Far North Side
- **Edison Park** (CA #9) — Far northwest, low density, more suburban character
- **Norwood Park** (CA #10) — Similar to Edison Park
- **Jefferson Park** (CA #11) — Major transit hub, diverse population
- **Forest Glen** (CA #12) — Residential, higher income
- **North Park** (CA #13) — Diverse, home to North Park University

#### Far Northwest Side
- **Portage Park** (CA #15) — Large, family-oriented, diverse
- **Dunning** (CA #17) — Includes former state hospital grounds
- **Montclare** (CA #18) — Small, residential
- **Belmont Cragin** (CA #19) — Large, predominantly Latino, working class
- **Hermosa** (CA #20) — Industrial/residential mix (Westside CDC covers this but not as primary)

#### West Side
- **Humboldt Park** (CA #23) — Covered by HP Solidarity Network, but only one group for large area
- **West Garfield Park** (CA #26) — Covered by Westside Mutual Aid (multi-neighborhood)
- **Near West Side** (CA #28) — Includes UIC area, medical district

#### Southwest Side
- **Archer Heights** (CA #57) — Working class, predominantly Latino
- **Garfield Ridge** (CA #56) — Residential, near Midway Airport
- **Clearing** (CA #64) — Residential, near Midway
- **West Elsdon** (CA #62) — Residential
- **Gage Park** (CA #60) — Working class, predominantly Latino
- **Chicago Lawn** (CA #63) — Includes Marquette Park area
- **Ashburn** (CA #70) — Large, diverse middle-class area
- **Auburn Gresham** (CA #71) — Predominantly Black, active community organizations likely exist

#### Far South Side
- **Roseland** (CA #49) — Large, predominantly Black, significant need
- **Pullman** (CA #50) — Historic district, mixed-income
- **South Deering** (CA #51) — Includes industrial areas
- **East Side** (CA #52) — Predominantly Latino, near Indiana border
- **West Pullman** (CA #53) — Large, predominantly Black
- **Riverdale** (CA #54) — Includes Altgeld Gardens, significant need
- **Hegewisch** (CA #55) — Isolated, working class
- **Washington Heights** (CA #73) — Predominantly Black
- **Morgan Park** (CA #75) — Covered by 19th Ward MA
- **Beverly** (CA #72) — Covered by 19th Ward MA
- **Mount Greenwood** (CA #74) — Covered by 19th Ward MA

---

## Suburban Coverage

| Suburb | Population | Status | Notes |
|---|---|---|---|
| Evanston | ~78,000 | Covered | Evanston Community Fridges |
| Berwyn | ~56,000 | Covered | Berwyn Cicero Mutual Aid |
| Cicero | ~83,000 | Covered | Berwyn Cicero Mutual Aid |
| Elgin | ~114,000 | Covered | Elgin in Solidarity with BLM |
| Oak Park | ~52,000 | **Uncovered** | No direct group found. CEDA serves area. |
| Skokie | ~64,000 | **Uncovered** | Large, diverse suburb |
| Des Plaines | ~60,000 | **Uncovered** | No groups found |
| Harvey | ~20,000 | **Uncovered** | Significant need, South Suburbs |
| Blue Island | ~23,000 | **Uncovered** | Working class, South Suburbs |
| Calumet City | ~36,000 | **Uncovered** | South Suburbs |
| Dolton | ~23,000 | **Uncovered** | South Suburbs |
| Maywood | ~23,000 | **Uncovered** | Near West Suburbs |
| Bellwood | ~19,000 | **Uncovered** | Near West Suburbs |

---

## Priority Gaps for Phase 4 Fill

### Tier 1 — High Need, No Coverage
These are areas with significant socioeconomic need and zero groups in the dataset.

1. **Roseland / West Pullman / Riverdale** — Far South Side. High poverty, food deserts, Altgeld Gardens. Critical gap.
2. **Auburn Gresham** — South Side. Active community organizations known to exist but not yet discovered.
3. **Belmont Cragin** — Northwest Side. Large, working-class Latino community.
4. **Gage Park / Chicago Lawn** — Southwest Side. Working-class, predominantly Latino.

### Tier 2 — Moderate Need, No Coverage
5. **Portage Park / Jefferson Park** — Far Northwest. Large population, aging demographic.
6. **Archer Heights / Garfield Ridge** — Southwest. Near Midway Airport.
7. **Harvey / Dolton / Calumet City** — South Suburbs. High need, active community organizations likely exist.
8. **Skokie** — North Suburb. Large, diverse. Likely has groups not yet discovered.

### Tier 3 — Lower Need or Adjacent to Coverage
9. **Edison Park / Norwood Park** — Far Northwest. Higher income, lower density. Adjacent to suburban groups.
10. **Oak Park** — Near West. Higher income but progressive community. Adjacent to Austin and Berwyn groups.

---

## Recommended Search Strategy for Gap Fill

For each uncovered area, search:
- `"[neighborhood name]" mutual aid Chicago`
- `"[neighborhood name]" food pantry Chicago`
- `"[neighborhood name]" community organization Chicago`
- Check the Greater Chicago Food Depository locator for pantries in each ZIP code
- Check Organize Directory and Sixty Inches From Center for neighborhood-specific entries
- Search Facebook groups for `"[neighborhood]" mutual aid`
