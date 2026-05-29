# Chicago Corps — Operational Plan

How to move from a 77-group dataset to active volunteer-to-group matching. Covers the end-to-end workflow: finding volunteers, qualifying groups, making connections, and displaying the information publicly.

**Status:** Phase 6 — Directory Expansion & Tooling  
**Last updated:** 2026-05-29

---

## Part 1: Volunteer-to-Group Matching Workflow

### Pipeline

```
DISCOVER ──→ QUALIFY ──→ MATCH ──→ CONNECT ──→ TRACK ──→ ITERATE
```

---

### Phase A: Volunteer Discovery

**Recruitment Channels (ordered by expected yield):**

| Channel | Method | Reach | Effort |
|---|---|---|---|
| Social media | Chicago neighborhood FB groups, r/chicago, Instagram | High | Medium |
| Universities | UIC, UChicago, DePaul, Northwestern, Loyola volunteer offices | High | Low |
| Existing platforms | VolunteerMatch, Idealist, Chicago Cares, United Way, Serve Illinois | Medium | Low |
| Community boards | Flyers at libraries, coffee shops, community centers | Low-Med | High |
| Word of mouth | Ask each contacted group to share with their networks | Medium | Low |
| Local media | City Cast Chicago, Block Club, WBEZ, Chicago Reader | Medium | Medium |

**Volunteer Intake Form (→ data/volunteers.csv):**

- Name (required), Email (required), Phone (optional)
- ZIP code → auto-populated neighborhood
- Availability: weekday/weekend, morning/afternoon/evening
- Time commitment: one-time, weekly, monthly, as-needed
- Skills checkboxes: Food distribution, Driving/delivery, Tutoring/mentoring, Legal/professional, Translation, Gardening/farming, Tech/social media, Healthcare/first aid, Organizing/outreach, General
- Transportation: car, bike, CTA, walk
- Languages spoken

---

### Phase B: Group Qualification

**Priority Tiers:**

| Tier | Criteria | ~Count | Action |
|---|---|---|---|
| Tier 1 — Ready | Email/phone confirmed + volunteer page + active ≤3 months | ~10 | Contact today |
| Tier 2 — Warm | Email/phone confirmed + likely volunteers + active ≤6 months | ~15 | Contact this week |
| Tier 3 — Cold | Contact form only or no volunteer page + active ≤15 months | ~30 | Contact this month |
| Tier 4 — Needs Work | No contact info or UNCERTAIN status | ~20 | Research first |

**Group Intake Questionnaire (sent on first contact):**

1. Are you currently accepting new volunteers? [Yes / With restrictions / Not right now]
2. What volunteer roles do you need filled?
3. What is the time commitment? [One-time / Weekly / Monthly / As-needed]
4. Are there any requirements? [Age minimum, background check, training, etc.]
5. How should volunteers apply? [Link to form / Email you / Just show up / Other]
6. What languages would be helpful for volunteers to speak?
7. Do you have capacity to onboard new volunteers right now? [Yes / Strained but yes / No]
8. Is there anything else volunteers should know?

---

### Phase C: Volunteer-Group Matching

**Algorithm (priority order):**

1. **Geography** — Volunteer ZIP → groups within 3 miles (primary) or same side of city (secondary)
2. **Skills** — Volunteer's checked skills → groups' needed roles
3. **Availability** — Schedule alignment
4. **Language** — Language match where relevant

**Matching Rules:**

- Never match to more than 3 groups at once (avoid overwhelm)
- Always include at least one general mutual aid option
- Prioritize Tier 1-2 groups over Tier 3-4
- Flag if the only match is a Tier 4 group

**Match Email Template:**

```
Hi [Name],

Based on your location ([Neighborhood]) and interests ([Skills]),
here are Chicago mutual aid groups that could use your help:

1. [Group Name] — [Neighborhood] ([Distance] miles)
   What they do: [One-line description]
   They need: [Relevant roles]
   How to apply: [Link or instructions]
   Contact: [Email or phone]

2. [Group Name] ...
3. [Group Name] ...

If none of these feel right, reply and we'll find more options.
```

---

### Phase D: Connection & Follow-Up

**Schedule:**

| Day | Action |
|---|---|
| 0 | Send match email to volunteer, log in outreach_log.csv |
| 3 | Check-in email: "Did you reach out? Any questions?" |
| 7 | If no response, send one more follow-up |
| 14 | Mark "no response" if still silent; send feedback survey if connected |
| 30 | Check in with group: "Did the volunteer work out?" |
| 90 | Re-verify group for activity |

**Feedback Survey (for volunteers):**

1. Did you connect with the group we matched you with? [Yes / No]
2. If yes, how was the experience? [1-5 scale]
3. Would you like to be matched with more groups? [Yes / No]
4. What could we improve about the matching process?

---

### Phase E: System Iteration

**Monthly Maintenance:**

- Re-verify all Tier 1-2 groups (check website/social media)
- Update verification_log.csv with new evidence
- Remove or archive groups inactive for 15+ months
- Add newly discovered groups from ongoing research
- Review match success rate: connected / total matched
- Adjust matching algorithm based on feedback patterns

**Quarterly Review:**

- Neighborhood coverage gap analysis
- Category gap analysis
- Volunteer demographics review
- Group satisfaction survey
- Publish updated public directory

---

## Part 2: Information Display Plan

### Audience → Format Matrix

| Audience | Need | Format |
|---|---|---|
| Volunteers | "What's near me that needs help?" | Interactive map + search |
| Groups | "List us correctly, send us volunteers" | Submission form + directory listing |
| Organizers (us) | "Where are the gaps? Who needs follow-up?" | Internal dashboard + CSVs |
| General public | "What mutual aid exists in Chicago?" | Browseable directory + printables |
| Funders/donors | "What's the landscape?" | Summary statistics + reports |

---

### Format A: Public Website (chicagocorps.org)

```
chicagocorps.org
├── / (Home) — Search bar, ZIP lookup, category browser, intake form links
├── /groups/[slug]/ — Individual group page with details + volunteer badge
├── /neighborhoods/ — Browse by community area
├── /map/ — Interactive Leaflet map with all locations
├── /volunteer/ — Intake form + how-it-works explainer
├── /about/ — Mission, methodology, contact
└── /data/ — Download CSV for researchers
```

**Tech stack (zero-cost, static, git-backed):**

- **Hosting:** GitHub Pages or Neocities (free)
- **Generator:** Jekyll or 11ty (static site)
- **Search:** Lunr.js or Fuse.js (client-side, no backend needed)
- **Map:** Leaflet.js + OpenStreetMap tiles (free, no API key)
- **Forms:** Google Forms → Sheets → CSV → committed to repo
- **Pipeline:** CSV files → build.py → JSON → Jekyll → static HTML

---

### Format B: Internal Dashboard (dashboard.html)

Single HTML file reading CSVs client-side via Papa Parse. Sections:

1. **At-a-glance stats** — total groups, verified %, volunteer-ready count
2. **Outreach pipeline** — Tier breakdown, contacted vs uncontacted
3. **Coverage heatmap** — Chicago community areas colored by group density
4. **Stale data alerts** — groups unverified in 6+ months
5. **Recent activity** — last 10 verification events + outreach attempts
6. **Gap finder** — neighborhoods with 0 groups, categories with < 3 groups

---

### Format C: Printable Resources

- **Neighborhood sheets** — one page per neighborhood with contact info for printing
- **Zine/flyer** — foldable pocket guide to Chicago mutual aid
- **Poster** — "Chicago Community Fridges" map with all 11 locations
- **QR code cards** — link to website, distributed at libraries and community centers

---

### Format D: Data Pipeline

```
data/*.csv                    ← Source of truth (human-edited)
    │
    ▼
build.py                       ← One command: `make build`
    │
    ├──→ groups.json           ← CSV → JSON for website
    ├──→ locations.geojson     ← Addresses → geocoded coordinates
    └──→ _data/                ← Jekyll data files
            │
            ▼
        jekyll build            ← Static site generator
            │
            ▼
        _site/                  ← Deploy to GitHub Pages
```

---

## Competitive Landscape

No existing platform specifically matches volunteers to grassroots Chicago mutual aid groups. Chicago Cares serves traditional nonprofits. Serve Illinois is a broad state portal. Brightest is a paid platform for organizers. Community Kitchen Chicago's map is food-only. Our niche is unfilled.

---

## Partnership Targets

| Partner | Value | Ask |
|---|---|---|
| Chicago Cares | Existing volunteer base, platform | Cross-list our verified groups |
| Block Club Chicago | Reach 200K+ readers | Cover our launch, link to directory |
| City Cast Chicago | Podcast audience, mutual aid coverage | Feature in explainer episode |
| Community Kitchen Chicago | Mutual aid map, credibility | Link exchange, data sharing |
| Serve Illinois | State platform | List our groups on Galaxy Digital |
| University volunteer offices | Student volunteer pool | Promote to students |
| Chicago Public Library | Community access points | Host printable sheets, QR cards |

---

## Implementation Timeline

| Week | Focus | Key Deliverable |
|---|---|---|
| 1-2 | Foundation | GitHub Pages + build.py + dashboard.html + Google Forms + email templates |
| 3-4 | Public Launch | Public site + directory with 77 groups + volunteer intake form + first outreach to 16 Tier-1 groups |
| 5-6 | First Matching Cycle | Process volunteer signups → run matching → send match emails → follow-ups + printable sheets |
| 7-8 | Iteration | Analyze first cycle results + re-verify stale groups + fill top 5 geographic gaps + first monthly update |
| Ongoing | Maintenance | Monthly re-verification, matching, directory updates, social media posts |

---

## Success Metrics

| Metric | Target | Source |
|---|---|---|
| Groups with confirmed contact | 50+ | contacts.csv |
| Groups accepting volunteers | 30+ | volunteer_needs.csv |
| Volunteer signups | 100+ | volunteers.csv |
| Successful matches | 50+ | outreach_log.csv |
| Neighborhood coverage | 50 of 77 CAs | locations.csv |
| Data freshness | 90% verified ≤6 months | verification_log.csv |
| Match satisfaction | 4.0+/5.0 | feedback surveys |

---

## Risk Table

| Risk | Probability | Mitigation |
|---|---|---|
| Groups don't respond | Medium | Multiple contact methods, phone follow-up, accept informality |
| Volunteers don't follow through | Medium | Tiny first step ("just send one email"), Day 3 check-in |
| Dataset goes stale | High | Monthly re-verification cycle, STALE flag, dashboard alerts |
| Someone listed without consent | Low | Public info only, removal instructions on every page |
| Burnout (maintainer) | Medium | Automate everything, keep scope small, recruit co-maintainers from matched volunteers |
| Geographic imbalance | High | Active recruitment in underserved areas per coverage/gaps.md |
