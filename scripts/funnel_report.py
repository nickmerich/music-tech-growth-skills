#!/usr/bin/env python3
"""Weekly music tech partner and revenue report.

Usage: python3 funnel_report.py orders.csv partners.csv [--as-of YYYY-MM-DD]

orders.csv:   date,order_id,amount,partner_id,refunded
partners.csv: partner_id,accepted_date,first_post_date
Sales are counted only from orders, never from clicks.
"""
import argparse
import csv
import datetime as dt
import statistics
import sys
from collections import defaultdict


def read(path, need):
    try:
        with open(path, newline="") as f:
            r = csv.DictReader(f)
            if not r.fieldnames or not set(need).issubset(r.fieldnames):
                sys.exit(f"{path} needs columns: {', '.join(need)}")
            return list(r)
    except FileNotFoundError:
        sys.exit(f"File not found: {path}")


def day(s):
    s = (s or "").strip()
    return dt.date.fromisoformat(s) if s else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("orders")
    ap.add_argument("partners")
    ap.add_argument("--as-of", default=dt.date.today().isoformat())
    a = ap.parse_args()
    as_of = dt.date.fromisoformat(a.as_of)

    orders = [o for o in read(a.orders, ["date", "order_id", "amount", "partner_id", "refunded"])
              if day(o["date"]) <= as_of]
    partners = [p for p in read(a.partners, ["partner_id", "accepted_date", "first_post_date"])
                if day(p["accepted_date"]) and day(p["accepted_date"]) <= as_of]

    gross = sum(float(o["amount"]) for o in orders)
    refunds = sum(float(o["amount"]) for o in orders if o["refunded"].strip() == "1")
    net = gross - refunds
    kept = [o for o in orders if o["refunded"].strip() != "1"]
    by_partner = defaultdict(list)
    for o in kept:
        if o["partner_id"].strip():
            by_partner[o["partner_id"].strip()].append(o)
    partner_net = sum(float(o["amount"]) for os_ in by_partner.values() for o in os_)

    print(f"Report as of {as_of}")
    print(f"Gross ${gross:,.2f} | refunds ${refunds:,.2f} | net ${net:,.2f}")
    if net:
        print(f"Partner-attributed net: ${partner_net:,.2f} ({partner_net / net:.0%})")

    posted = [p for p in partners if day(p["first_post_date"])]
    one = [p for p in partners if len(by_partner.get(p["partner_id"], [])) >= 1]
    two = [p for p in partners if len(by_partner.get(p["partner_id"], [])) >= 2]
    print(f"\nApproved {len(partners)} | posted {len(posted)} | 1+ sale {len(one)} | 2+ sales {len(two)}")

    def first_sale(pid):
        ds = [day(o["date"]) for o in by_partner.get(pid, [])]
        return min(ds) if ds else None

    cohort30 = [p for p in partners if day(p["accepted_date"]) <= as_of - dt.timedelta(days=30)]
    act = [p for p in cohort30 if first_sale(p["partner_id"]) and
           (first_sale(p["partner_id"]) - day(p["accepted_date"])).days <= 30]
    if cohort30:
        print(f"30-day activation: {len(act)}/{len(cohort30)} = {len(act) / len(cohort30):.0%}")
    gaps = [(first_sale(p["partner_id"]) - day(p["accepted_date"])).days
            for p in partners if first_sale(p["partner_id"])]
    if gaps:
        print(f"Median days to first sale: {statistics.median(gaps):g}")
    dormant = [p["partner_id"] for p in partners
               if day(p["accepted_date"]) <= as_of - dt.timedelta(days=60) and not by_partner.get(p["partner_id"])]
    print(f"Dormant at 60 days: {len(dormant)}" + (f" ({', '.join(dormant)})" if dormant else ""))

    rev = sorted((sum(float(o["amount"]) for o in os_) for os_ in by_partner.values()), reverse=True)
    if rev and partner_net:
        k = max(1, round(len(partners) * 0.1))
        print(f"Top 10% of partners ({k}) share of partner net: {sum(rev[:k]) / partner_net:.0%}")


if __name__ == "__main__":
    main()
