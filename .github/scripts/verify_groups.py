#!/usr/bin/env python3
"""
Verification script for Chicago Corps.
- Checks staleness (groups unverified for 6+ months)
- Pings websites to check if they're still live
- Generates a stale_report.json
- Flags groups whose websites return non-200
"""

import csv
import json
import os
import urllib.request
import urllib.error
import ssl
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path("data")
REPORTS_DIR = Path("_reports")
CSV_PATH = Path("chicago_mutual_aid_groups.csv")
STALE_THRESHOLD_DAYS = 180

os.makedirs(REPORTS_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def check_website(url, timeout=15):
    """Ping a URL; return (status_code, error_msg)."""
    if not url or not url.startswith("http"):
        return None, "no URL"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ChicagoCorps-Verifier/1.0"})
        resp = urllib.request.urlopen(req, timeout=timeout, context=ctx)
        return resp.status, None
    except urllib.error.HTTPError as e:
        return e.code, f"HTTP {e.code}"
    except Exception as e:
        return None, str(e)[:120]


def main():
    groups = []
    if CSV_PATH.exists():
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            groups = list(reader)

    stale_groups = []
    site_issues = []
    today = datetime.now()

    for i, g in enumerate(groups):
        name = g.get("name", f"row-{i+2}")
        vdate_str = g.get("last_verified_activity", "")
        website = g.get("website", "").strip()

        # Check staleness
        if vdate_str:
            try:
                vdate = datetime.strptime(vdate_str, "%Y-%m-%d")
                age = (today - vdate).days
                if age > STALE_THRESHOLD_DAYS:
                    stale_groups.append({
                        "name": name,
                        "last_verified": vdate_str,
                        "days_since": age,
                        "status": g.get("verification_status", "UNKNOWN"),
                        "neighborhood": g.get("neighborhood", ""),
                        "website": website,
                    })
            except ValueError:
                pass

        # Check website health
        if website and website.startswith("http"):
            code, err = check_website(website)
            if code and code >= 400:
                site_issues.append({
                    "name": name,
                    "website": website,
                    "status_code": code,
                    "error": err,
                })
            elif code is None and err:
                site_issues.append({
                    "name": name,
                    "website": website,
                    "status_code": None,
                    "error": err,
                })

    report = {
        "generated": today.isoformat(),
        "total_groups": len(groups),
        "stale_count": len(stale_groups),
        "stale_threshold_days": STALE_THRESHOLD_DAYS,
        "site_issue_count": len(site_issues),
        "stale_groups": stale_groups,
        "site_issues": site_issues,
    }

    with open(REPORTS_DIR / "stale_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Total groups: {len(groups)}")
    print(f"Stale (> {STALE_THRESHOLD_DAYS}d): {len(stale_groups)}")
    print(f"Site issues: {len(site_issues)}")

    for sg in stale_groups:
        print(f"  STALE: {sg['name']} — {sg['days_since']}d since {sg['last_verified']}")

    for si in site_issues:
        print(f"  SITE ISSUE: {si['name']} — {si['website']}: {si['error'] or si['status_code']}")

    if stale_groups or site_issues:
        exit(1)  # Signal attention needed


if __name__ == "__main__":
    main()
