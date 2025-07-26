import os
import json
from datetime import datetime
import pandas as pd

# Directory containing JSON files
WALLET_DIR = "data/wallet_data"


# Utility: convert value to ETH from wei (if applicable)
def convert_wei_to_eth(wei):
    try:
        return int(wei) / 1e18
    except:
        return 0

def extract_features_from_txns(txns):
    total_txns = len(txns)
    lending_txns = 0
    repay_txns = 0
    liquidation_txns = 0
    values = []
    borrow_amounts = []
    timestamps = []

    for txn in txns:
        method = txn.get("method", "").lower()
        values.append(convert_wei_to_eth(txn.get("value", 0)))

        # Count based on decoded method names if available
        if "deposit" in method or "supply" in method:
            lending_txns += 1
        elif "repay" in method:
            repay_txns += 1
        elif "liquidate" in method:
            liquidation_txns += 1
        elif "borrow" in method:
            borrow_amounts.append(convert_wei_to_eth(txn.get("value", 0)))

        # Collect timestamp
        if "block_signed_at" in txn:
            timestamps.append(datetime.fromisoformat(txn["block_signed_at"].replace("Z", "+00:00")))

    # Age calculations
    if timestamps:
        wallet_start = min(timestamps)
        wallet_age_months = max((datetime.now(wallet_start.tzinfo) - wallet_start).days / 30, 1)
        last_txn_days_ago = (datetime.now(max(timestamps).tzinfo) - max(timestamps)).days
    else:
        wallet_age_months = 1
        last_txn_days_ago = None

    return {
        "num_txns": total_txns,
        "num_lending_txns": lending_txns,
        "num_repay_txns": repay_txns,
        "num_liquidation_txns": liquidation_txns,
        "avg_txn_value": sum(values) / len(values) if values else 0,
        "last_txn_days_ago": last_txn_days_ago,
        "txns_per_month": total_txns / wallet_age_months,
        "max_borrowed_amount": max(borrow_amounts) if borrow_amounts else 0
    }

results = []

for file in os.listdir(WALLET_DIR):
    if file.endswith(".json"):
        wallet_id = file.replace(".json", "")
        with open(os.path.join(WALLET_DIR, file), "r") as f:
            try:
                data = json.load(f)
            except:
                continue

        features = extract_features_from_txns(data)
        features["wallet_id"] = wallet_id
        results.append(features)

# Save to CSV
df = pd.DataFrame(results)
os.makedirs("outputs", exist_ok=True)
df.to_csv("outputs/wallet_features.csv", index=False)
print("✅ Feature extraction complete. Output saved as 'wallet_features.csv'")
