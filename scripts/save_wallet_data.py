import json
import os
import time
import requests

# --- Configuration ---
CHAIN_ID = "1"  # Ethereum Mainnet
COVALENT_API_KEY = "cqt_rQtBwVV3BGDM6CCwyCvHHRvKTdJ9"

# Load wallets from file
wallets_file_path = os.path.join("data", "wallets.txt")
with open(wallets_file_path, "r", encoding="utf-8-sig") as f:
    WALLETS = [line.strip().replace('\ufeff', '').replace('﻿', '') for line in f]

# ✅ Correct output directory
output_folder = os.path.join("data", "wallet_data")
os.makedirs(output_folder, exist_ok=True)

# Fetch function
def fetch_wallet_transactions(wallet_address):
    url = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address/{wallet_address}/transactions_v2/"
    params = {"key": COVALENT_API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()["data"]["items"]
    else:
        print(f"❌ Failed for {wallet_address}: {response.status_code}")
        return []

# Save transactions to correct folder
for wallet in WALLETS:
    txns = fetch_wallet_transactions(wallet)
    filepath = os.path.join(output_folder, f"{wallet}.json")
    with open(filepath, "w") as f:
        json.dump(txns, f)
    print(f"✅ Saved {len(txns)} txns for {wallet}")
    time.sleep(1.2)
