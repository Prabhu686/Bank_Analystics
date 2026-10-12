import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Create directories
os.makedirs("02_EDA_and_Feature_Engineering/output_data", exist_ok=True)
os.makedirs("02_EDA_and_Feature_Engineering/figures", exist_ok=True)

sns.set_theme(style="whitegrid")

# ==========================================
# 1. LOAD DATASETS
# ==========================================
customers = pd.read_csv("customers.csv")
accounts = pd.read_csv("accounts.csv")
transactions = pd.read_csv("transactions.csv")
channels = pd.read_csv("channels.csv")
service = pd.read_csv("service.csv")

# ==========================================
# 2. DATA CLEANING & PREPROCESSING
# ==========================================

# A. Standardize Inconsistent Account Labels
accounts["account_type_clean"] = accounts["account_type"].str.strip().str.title()
accounts["account_type_clean"] = accounts["account_type_clean"].replace({
    "Savings Account": "Savings",
    "Fixed Deposit": "Fixed Deposit",
})

# B. Remove Duplicate Transactions & Cap Extreme Outlier Amounts (99th percentile)
transactions = transactions.drop_duplicates()
q99 = transactions["amount"].quantile(0.99)
transactions["amount_cleaned"] = np.where(
    transactions["amount"] > q99, q99, transactions["amount"]
)

# C. Impute Missing Channel Usage Values with Median
channels["mobile_usage_clean"] = channels["mobile_usage"].fillna(
    channels["mobile_usage"].median()
)
channels["internet_usage_clean"] = channels["internet_usage"].fillna(
    channels["internet_usage"].median()
)

# D. Service Resolution Cleaning
service["resolution_clean"] = service["resolution"].fillna(
    "Unresolved / Pending"
)

# ==========================================
# 3. FEATURE ENGINEERING & AGGREGATION
# ==========================================

# Aggregate Transactions to Customer Level
tx_acc = transactions.merge(accounts, on="account_id", how="left")
tx_summary = (
    tx_acc.groupby("customer_id")
    .agg(
        total_tx_count=("transaction_id", "count"),
        total_tx_amount=("amount_cleaned", "sum"),
        avg_tx_amount=("amount_cleaned", "mean"),
        deposit_count=(
            "transaction_type",
            lambda x: (x == "Deposit").sum(),
        ),
        withdrawal_count=(
            "transaction_type",
            lambda x: (x == "Withdrawal").sum(),
        ),
        transfer_count=(
            "transaction_type",
            lambda x: (x == "Transfer").sum(),
        ),
        payment_count=(
            "transaction_type",
            lambda x: (x == "Payment").sum(),
        ),
    )
    .reset_index()
)

# Aggregate Service Interactions & Resolution Metrics
srv_summary = (
    service.groupby("customer_id")
    .agg(
        total_complaints=("complaints", "count"),
        resolved_complaints=(
            "resolution_clean",
            lambda x: x.str.startswith("Resolved").sum(),
        ),
        unresolved_complaints=(
            "resolution_clean",
            lambda x: (~x.str.startswith("Resolved")).sum(),
        ),
    )
    .reset_index()
)

srv_summary["complaint_resolution_rate"] = np.where(
    srv_summary["total_complaints"] > 0,
    srv_summary["resolved_complaints"] / srv_summary["total_complaints"],
    1.0,
)

# Channel Interaction Ratios
channels["total_digital_usage"] = (
    channels["mobile_usage_clean"] + channels["internet_usage_clean"]
)
channels["total_physical_usage"] = (
    channels["branch_usage"] + channels["ATM_usage"]
)

# ==========================================
# 4. MASTER DATASET COMBINATION & ENCODING
# ==========================================
master_df = (
    customers.merge(
        accounts[[
            "customer_id",
            "account_id",
            "account_type_clean",
            "balance_band",
        ]],
        on="customer_id",
        how="left",
    )
    .merge(channels, on="customer_id", how="left")
    .merge(tx_summary, on="customer_id", how="left")
    .merge(srv_summary, on="customer_id", how="left")
)

# Fill nulls for customers without transaction or complaint activity
master_df["total_tx_count"] = master_df["total_tx_count"].fillna(0)
master_df["total_tx_amount"] = master_df["total_tx_amount"].fillna(0)
master_df["avg_tx_amount"] = master_df["avg_tx_amount"].fillna(0)
master_df["total_complaints"] = master_df["total_complaints"].fillna(0)

# Ordinal Categorical Encodings
balance_map = {
    "Low (<$1k)": 1,
    "Medium ($1k-$10k)": 2,
    "High ($10k-$50k)": 3,
    "VHNW (>$50k)": 4,
}
age_map = {"18-25": 1, "26-35": 2, "36-50": 3, "51-65": 4, "65+": 5}

master_df["balance_band_code"] = master_df["balance_band"].map(balance_map)
master_df["age_band_code"] = master_df["age_band"].map(age_map)

# Export cleaned CSV file
master_df.to_csv(
    "02_EDA_and_Feature_Engineering/output_data/cleaned_trustwave_bank_data.csv",
    index=False,
)
print("Master dataset saved successfully!")

# ==========================================
# 5. VISUALIZATIONS & EDA
# ==========================================

# Figure 1: Channel Usage Comparison
plt.figure(figsize=(8, 5))
channel_totals = pd.Series({
    "Mobile Usage": master_df["mobile_usage_clean"].sum(),
    "Internet Usage": master_df["internet_usage_clean"].sum(),
    "ATM Usage": master_df["ATM_usage"].sum(),
    "Branch Usage": master_df["branch_usage"].sum(),
})
ax1 = sns.barplot(
    x=channel_totals.index,
    y=channel_totals.values,
    palette=sns.color_palette("Blues_r", len(channel_totals)),
)
plt.title("Total Usage Across Banking Channels", fontsize=14, fontweight="bold")
plt.ylabel("Total Monthly Interactions", fontsize=12)
for p in ax1.patches:
  ax1.annotate(
      f"{int(p.get_height()):,}",
      (p.get_x() + p.get_width() / 2.0, p.get_height()),
      ha="center",
      va="bottom",
      fontsize=10,
      xytext=(0, 3),
      textcoords="offset points",
  )
plt.tight_layout()
plt.savefig(
    "02_EDA_and_Feature_Engineering/figures/fig1_channel_usage.png", dpi=300
)
plt.close()

# Figure 2: Channel Usage by Age Band
age_channel = (
    master_df.groupby("age_band")[[
        "mobile_usage_clean",
        "internet_usage_clean",
        "ATM_usage",
        "branch_usage",
    ]]
    .mean()
    .reset_index()
)
age_channel_melted = age_channel.melt(
    id_vars="age_band", var_name="Channel", value_name="Avg_Monthly_Usage"
)
age_channel_melted["Channel"] = (
    age_channel_melted["Channel"]
    .str.replace("_clean", "")
    .str.replace("_usage", "")
    .str.title()
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=age_channel_melted,
    x="age_band",
    y="Avg_Monthly_Usage",
    hue="Channel",
    palette="viridis",
)
plt.title("Average Channel Usage by Age Band", fontsize=14, fontweight="bold")
plt.xlabel("Age Band", fontsize=12)
plt.ylabel("Average Monthly Interactions", fontsize=12)
plt.tight_layout()
plt.savefig(
    "02_EDA_and_Feature_Engineering/figures/fig2_channel_by_age.png", dpi=300
)
plt.close()

# Figure 3: Regional Complaint Distribution
plt.figure(figsize=(8, 5))
region_complaints = master_df.groupby("region")["total_complaints"].sum().sort_values(ascending=False)
ax3 = sns.barplot(
    x=region_complaints.index, y=region_complaints.values, palette="Reds_r"
)
plt.title("Total Customer Complaints by Region", fontsize=14, fontweight="bold")
plt.xlabel("Region", fontsize=12)
plt.ylabel("Complaint Count", fontsize=12)
for p in ax3.patches:
  ax3.annotate(
      f"{int(p.get_height()):,}",
      (p.get_x() + p.get_width() / 2.0, p.get_height()),
      ha="center",
      va="bottom",
      fontsize=10,
      xytext=(0, 3),
      textcoords="offset points",
  )
plt.tight_layout()
plt.savefig(
    "02_EDA_and_Feature_Engineering/figures/fig3_regional_complaints.png",
    dpi=300,
)
plt.close()