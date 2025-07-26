import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Load extracted features
df = pd.read_csv("outputs/wallet_features.csv") # <- make sure this file exists in the root!

# Fill missing values
df["last_txn_days_ago"].fillna(df["last_txn_days_ago"].max(), inplace=True)

# Feature columns
features = [
    "num_liquidation_txns",
    "num_repay_txns",
    "last_txn_days_ago",
    "avg_txn_value",
    "txns_per_month",
    "max_borrowed_amount"
]

# Normalize
scaler = MinMaxScaler()
df_scaled = pd.DataFrame(scaler.fit_transform(df[features]), columns=features)

# Weighted scoring
df['risk_score'] = (
    df_scaled['num_liquidation_txns'] * 0.35 +
    (1 - df_scaled['num_repay_txns']) * 0.2 +
    df_scaled['last_txn_days_ago'] * 0.15 +
    (1 - df_scaled['avg_txn_value']) * 0.1 +
    (1 - df_scaled['txns_per_month']) * 0.1 +
    df_scaled['max_borrowed_amount'] * 0.1
)

# Normalize risk_score to 0–1000
df['risk_score'] = (
    (df['risk_score'] - df['risk_score'].min()) /
    (df['risk_score'].max() - df['risk_score'].min())
) * 1000
df['risk_score'] = df['risk_score'].round(2)

# Add risk_level label
def assign_level(score):
    if score <= 400:
        return "🚨 High Risk"
    elif score <= 700:
        return "⚠️ Moderate"
    else:
        return "✅ Low Risk"

df['risk_level'] = df['risk_score'].apply(assign_level)

# Save results
df[['wallet_id', 'risk_score', 'risk_level']].to_csv("outputs/wallet_scores.csv", index=False)
print("✅ Risk scoring complete. Saved to 'outputs/wallet_scores.csv'")
