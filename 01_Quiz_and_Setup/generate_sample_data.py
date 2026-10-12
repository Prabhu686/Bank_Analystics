import os
import random
import numpy as np
import pandas as pd

# Create raw_data directory
os.makedirs("raw_data", exist_ok=True)
np.random.seed(42)

n_customers = 500

# 1. customers.csv
regions = ["North", "South", "East", "West", "Central"]
age_bands = ["18-25", "26-35", "36-50", "51-65", "65+"]

customers = pd.DataFrame(
    {
        "customer_id": [f"CUST_{1000+i}" for i in range(n_customers)],
        "age_band": np.random.choice(age_bands, n_customers, p=[0.2, 0.3, 0.25, 0.15, 0.1]),
        "region": np.random.choice(regions, n_customers),
        "relationship_length_years": np.random.randint(1, 15, n_customers),
    }
)
customers.to_csv("raw_data/customers.csv", index=False)

# 2. accounts.csv (Quality issue: Inconsistent account labels)
account_types_messy = [
    "Savings",
    "savings",
    "SAVINGS",
    "Checking",
    "checking",
    "Current",
    "CURRENT",
    "Fixed Deposit",
]
balance_bands = ["Low (<$1k)", "Medium ($1k-$10k)", "High ($10k-$50k)", "VHNW (>$50k)"]

accounts = pd.DataFrame(
    {
        "account_id": [f"ACC_{2000+i}" for i in range(n_customers)],
        "customer_id": customers["customer_id"],
        "account_type": np.random.choice(account_types_messy, n_customers),
        "balance_band": np.random.choice(balance_bands, n_customers, p=[0.3, 0.4, 0.2, 0.1]),
    }
)
accounts.to_csv("raw_data/accounts.csv", index=False)

# 3. transactions.csv (Quality issues: Extreme amounts & duplicate records)
tx_types = ["Deposit", "Withdrawal", "Transfer", "Payment"]
dates = pd.date_range(start="2025-01-01", periods=180, freq="D")

tx_list = []
for acc in accounts["account_id"].sample(300):
    for _ in range(np.random.randint(3, 10)):
        tx_list.append(
            {
                "transaction_id": f"TX_{random.randint(100000, 999999)}",
                "account_id": acc,
                "date": np.random.choice(dates).strftime("%Y-%m-%d"),
                "amount": round(np.random.exponential(scale=150) + 10, 2),
                "transaction_type": np.random.choice(tx_types),
            }
        )

tx_df = pd.DataFrame(tx_list)

# Inject extreme amounts (outliers)
tx_df.loc[tx_df.sample(10).index, "amount"] = [99999.00, 500000.00, 150000.00] + list(
    np.random.uniform(50000, 200000, 7)
)

# Inject duplicate records
duplicates = tx_df.sample(25)
tx_df = pd.concat([tx_df, duplicates], ignore_index=True)
tx_df.to_csv("raw_data/transactions.csv", index=False)

# 4. channels.csv (Quality issue: Missing values)
channels = pd.DataFrame(
    {
        "customer_id": customers["customer_id"],
        "branch_visits_pm": np.random.poisson(lam=1.5, size=n_customers),
        "atm_usage_pm": np.random.poisson(lam=3.0, size=n_customers),
        "mobile_usage_pm": np.random.poisson(lam=12.0, size=n_customers),
        "internet_usage_pm": np.random.poisson(lam=5.0, size=n_customers),
    }
)

# Inject missing values (NaN)
channels.loc[channels.sample(40).index, "mobile_usage_pm"] = np.nan
channels.loc[channels.sample(30).index, "internet_usage_pm"] = np.nan
channels.to_csv("raw_data/channels.csv", index=False)

# 5. service.csv (Quality issue: Incomplete complaint records)
request_types = [
    "Address Change",
    "Card Replacement",
    "Password Reset",
    "Fee Dispute",
    "Loan Query",
]
complaint_types = [
    "Long Wait Time",
    "Failed Transaction",
    "Incorrect Charges",
    "App Crash",
    "Unauthorized Transaction",
]
resolutions = ["Resolved - Satisfied", "Resolved - Refunded", "Escalated", np.nan]

service_list = []
for cust in customers["customer_id"].sample(200):
    service_list.append(
        {
            "service_id": f"SRV_{random.randint(10000, 99999)}",
            "customer_id": cust,
            "request_type": np.random.choice(request_types),
            "complaint_type": np.random.choice(complaint_types, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
            "resolution": np.random.choice(resolutions, p=[0.5, 0.2, 0.1, 0.2]),
        }
    )

service_df = pd.DataFrame(service_list)
service_df.to_csv("raw_data/service.csv", index=False)

print("All sample datasets successfully generated in '01_Quiz_and_Setup/raw_data/'!")