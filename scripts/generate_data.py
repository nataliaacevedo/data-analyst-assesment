import pandas as pd, numpy as np, os, random, math
from datetime import datetime, timedelta

# Load existing deals dataset
deals_path = "/mnt/data/deals_2024onwards.csv"
deals = pd.read_csv(deals_path, parse_dates=["entered_buyer_interested", "entered_offer_submitted"])

# Create a copy to adjust
deals_adj = deals.copy()

n_total = len(deals_adj)
idx = deals_adj.index

# 1) Make 15% of deals non‑compliant: buyer_interested >= offer_submitted
noncomp_count = int(0.15 * n_total)
idx_noncomp = np.random.choice(idx, size=noncomp_count, replace=False)

for i in idx_noncomp:
    # Shift offer_submitted backwards by random 1‑10 days to break the rule
    deals_adj.at[i, "entered_buyer_interested"] = deals_adj.at[i, "entered_offer_submitted"] + timedelta(days=np.random.randint(1, 10))

# 2) Make another 5% of deals have NULL offer_submitted (still earlier stages)
remaining_idx = list(set(idx) - set(idx_noncomp))
missing_count = int(0.05 * n_total)
idx_missing = np.random.choice(remaining_idx, size=missing_count, replace=False)
deals_adj.loc[idx_missing, "entered_offer_submitted"] = pd.NaT

# Save adjusted dataset
new_path = "/mnt/data/deals_2024onwards_var.csv"
deals_adj.to_csv(new_path, index=False)

# Quick sanity check
total_offer_submitted = deals_adj["entered_offer_submitted"].notna().sum()
compliant = deals_adj["entered_offer_submitted"].notna() & (deals_adj["entered_buyer_interested"] < deals_adj["entered_offer_submitted"])
percent_compliant = compliant.sum() / total_offer_submitted * 100

summary = pd.DataFrame({
    "Total deals": [n_total],
    "Deals con Offer Submitted": [total_offer_submitted],
    "Compliant": [compliant.sum()],
    "% Compliant": [round(percent_compliant, 1)]
})

