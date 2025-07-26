# 🛡️ Wallet Risk Scoring from On-Chain Transactions

This project analyzes on-chain wallet activity from Compound V2/V3 using the Covalent API and assigns a **risk score (0–1000)** to each wallet based on transaction behavior.

---

## 📂 Folder Structure

wallet-risk-scoring/

├── data/

│   ├── wallets.txt              # List of 100 wallet addresses

│   └── wallet_data/             # Raw JSONs per wallet

├── outputs/

│   ├── wallet_features.csv      # Engineered features table

│   └── wallet_scores.csv        # Final wallet risk scores + risk levels

├── scripts/

│   ├── fetch_wallets.py         # Fetch transaction data via Covalent

│   ├── wallet_transaction_extraction.py  # Feature-extraction logic

│   └── wallet_risk_scoring.py   # Compute risk score & assign risk level

├── requirements.txt             # Python dependencies (e.g. pandas, scikit‑learn)

└── README.md                    # Project documentation (this file)


---

## 🧠 Problem Statement

> Retrieve on-chain transaction history for 100+ wallet addresses from the Compound protocol, extract features, and assign a **risk score** (0 to 1000) to each wallet.

---

## ✅ Steps Performed

### 1. 🔍 Data Collection

- Used [Covalent API](https://www.covalenthq.com/docs/api/) to fetch historical transactions for each wallet on Ethereum Mainnet.
- Saved results in `data/wallet_data/` as individual `.json` files.
- Script used: `scripts/fetch_wallets.py`
- Loads wallet list from `data/wallets.txt`, fetches and saves JSON data into `data/wallet_data/`.

- 
- ✅ # 🔑 Don't forget:
Open `scripts/fetch_wallets.py` and replace the value of `COVALENT_API_KEY` with your actual Covalent API key:
```bash
COVALENT_API_KEY = "ENTER_YOUR_API_KEY_HERE"
```



### 2. 🧾 Feature Engineering

Extracted the following features for each wallet:
| Feature Name           | Description |
|------------------------|-------------|
| `num_txns`             | Total number of transactions |
| `num_lending_txns`     | Count of deposit/supply operations |
| `num_repay_txns`       | Count of repayment operations |
| `num_liquidation_txns` | Number of liquidations |
| `avg_txn_value`        | Average ETH value per transaction |
| `last_txn_days_ago`    | Days since last transaction |
| `txns_per_month`       | Frequency of activity |
| `max_borrowed_amount`  | Largest borrow amount seen |

- Script used: `scripts/wallet_transaction_extraction.py`
- Output: `outputs/wallet_features.csv`


### 3. 📊 Risk Scoring (0–1000)

Assigned a normalized risk score using the following logic:

| Feature | Risk Logic |
|--------|------------|
| `num_liquidation_txns` | Higher = riskier |
| `num_repay_txns`       | Higher = safer |
| `last_txn_days_ago`    | Inactive wallets = riskier |
| `avg_txn_value`        | Very low = suspicious |
| `txns_per_month`       | Too high or low = risk outliers |
| `max_borrowed_amount`  | High borrow without repayment = risky |

- Script used: `scripts/wallet_risk_scoring.py`
- Output: `outputs/wallet_scores.csv`


🧾 Risk Level Assignment:

| Risk Score Range | Risk Level       |
| ---------------- | ---------------- |
| 0–400            | 🚨 High Risk     |
| 401–700          | ⚠️ Moderate Risk |
| 701–1000         | ✅ Low Risk      |

- Script used: 
```
scripts/wallet_risk_scoring.py
```

- Output: 
outputs/wallet_scores.csv 
---


⚙️ Setup & Execution

1. Install the Python dependencies:

```
pip install -r requirements.txt
```

Dependencies include:

pandas

requests

scikit-learn



🚀 Running the Pipeline


Make sure you're in the root folder (wallet-risk-scoring/), then run:

1. Add your wallet addresses (one per line) to data/wallets.txt.  (Already added and can be changed as per your needs)

2. Update your Covalent API key in scripts/debug_fetch_only.py.  (Optional: to check is it working or not) 

3. Update your Covalent API key in scripts/save_wallet_data.py. 

4. Run:

# Step 1: Fetch transaction data (saves to data/wallet_data/)

```
python scripts/save_wallet_data.py
```

# Step 2: Extract features (saves to outputs/wallet_features.csv)

```
python scripts/wallet_transaction_extraction.py
```

# Step 3: Score wallets (saves to outputs/wallet_scores.csv)

```
python scripts/wallet_risk_scoring.py
```


5. Final output files will appear in the outputs/ folder:

wallet_features.csv – extracted wallet features

wallet_scores.csv – scores and risk levels


🧪 Testing
Use scripts/fetch_wallets.py to test Covalent responses for sample wallets (for debugging only).


✍️ Author
Aditya Vishwakarma


📌 Notes

Stay within API rate limits when using Covalent (default delay of 1.2s is added).

💡 You can update or add wallet addresses by editing the data/wallets.txt file. Each line should contain a single wallet address (without quotes).

Only tested on Ethereum Mainnet (Chain ID: 1).

Ideal for wallet-level credit/risk scoring, DeFi fraud detection, or behavioral wallet analysis.

