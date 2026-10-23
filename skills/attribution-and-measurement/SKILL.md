---
name: attribution-and-measurement
description: Sets up and audits measurement for music tech growth, including UTM conventions, tracked links vs discount codes and which wins, affiliate platform reports, refunds and chargebacks, trial-to-paid, mobile and app-store gaps, and a weekly funnel and partner report from order and partner exports using a script. Use for "where are sales coming from", "is the affiliate tracking working", "weekly growth report", "set up UTMs", or "reconcile partner sales".
metadata:
  library: music-tech-growth-skills
  version: "1.0"
---

# Attribution and Measurement

## Conventions

- UTMs: `utm_source` = platform, `utm_medium` = organic, partner, email, or paid, `utm_campaign` = launch or program name, `utm_content` = creator or asset id.
- One tracked link per partner with the discount built in where possible.
- Publish the precedence rule when link and code disagree.
- Test every partner link end to end (click → discount applied → order attributed) before the partner posts, on desktop and mobile.

## Truth hierarchy

Paid orders after refunds (store or payment processor) > affiliate platform conversions > analytics conversions > clicks > views. Report each separately. Never call clicks "sales."

## Known gaps

Mobile in-app browsers drop cookies, people buy days later on another device, codes get shared on coupon sites. Note gaps; don't fill them with guesses.

## Weekly report

```bash
python3 scripts/funnel_report.py orders.csv partners.csv --as-of YYYY-MM-DD
```

`orders.csv`: `date,order_id,amount,partner_id,refunded` (partner_id blank if none; refunded 1/0).
`partners.csv`: `partner_id,accepted_date,first_post_date` (first_post_date blank if none).

Outputs: gross, refunds, net, partner share of net, approved partners, posted, 1+ and 2+ sales, 30-day activation, median days to first sale, dormant at 60 days, top-10% revenue share.

## Privacy

Aggregate where you can. Don't share customer data with partners.
