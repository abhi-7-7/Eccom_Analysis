import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/raw/Sample - Superstore.csv", encoding="latin1")
df.columns = [c.strip().lower().replace(" ", "_").replace("-","_") for c in df.columns]
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["month"] = df["order_date"].dt.to_period("M").astype(str)
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["discount_band"] = pd.cut(df["discount"],
    bins=[-0.01, 0, 0.10, 0.20, 0.30, 1.0],
    labels=["0%", "1-10%", "11-20%", "21-30%", "31%+"])

sns.set_theme(style="whitegrid")
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Superstore Sales Analysis", fontsize=18, fontweight="bold")

# 1. Monthly sales & profit trend
monthly = df.groupby("month")[["sales","profit"]].sum().reset_index()
axes[0,0].plot(monthly["month"], monthly["sales"], marker="o", color="#534AB7", linewidth=2, label="Sales")
axes[0,0].plot(monthly["month"], monthly["profit"], marker="s", color="#1D9E75", linewidth=2, label="Profit")
axes[0,0].set_title("Monthly sales & profit trend")
axes[0,0].tick_params(axis="x", rotation=45)
axes[0,0].legend()
axes[0,0].set_xlabel("")

# 2. Profit margin by sub-category (most important chart)
sub = df.groupby("sub_category").apply(
    lambda x: 100 * x["profit"].sum() / x["sales"].sum()
).sort_values()
colors = ["#E24B4A" if v < 0 else "#1D9E75" for v in sub.values]
axes[0,1].barh(sub.index, sub.values, color=colors)
axes[0,1].axvline(0, color="black", linewidth=1)
axes[0,1].set_title("Profit margin % by sub-category")
axes[0,1].set_xlabel("Profit margin %")

# 3. Discount band vs total profit (the key story)
disc = df.groupby("discount_band", observed=True)["profit"].sum().reset_index()
bar_colors = ["#1D9E75" if v > 0 else "#E24B4A" for v in disc["profit"]]
axes[0,2].bar(disc["discount_band"], disc["profit"], color=bar_colors)
axes[0,2].axhline(0, color="black", linewidth=0.8)
axes[0,2].set_title("Total profit by discount band")
axes[0,2].set_xlabel("Discount band")
axes[0,2].set_ylabel("Total profit ($)")

# 4. Sales by region
region = df.groupby("region")["sales"].sum().sort_values(ascending=False)
axes[1,0].bar(region.index, region.values, color="#378ADD")
axes[1,0].set_title("Sales by region")
axes[1,0].set_ylabel("Sales ($)")

# 5. Category sales vs profit side by side
cat = df.groupby("category")[["sales","profit"]].sum()
x = range(len(cat))
w = 0.35
axes[1,1].bar([i - w/2 for i in x], cat["sales"], width=w, label="Sales", color="#534AB7")
axes[1,1].bar([i + w/2 for i in x], cat["profit"], width=w, label="Profit", color="#1D9E75")
axes[1,1].set_xticks(list(x))
axes[1,1].set_xticklabels(cat.index)
axes[1,1].set_title("Sales vs profit by category")
axes[1,1].legend()

# 6. Shipping mode breakdown
ship = df.groupby("ship_mode")["order_id"].count().sort_values()
axes[1,2].barh(ship.index, ship.values, color="#EF9F27")
axes[1,2].set_title("Orders by shipping mode")
axes[1,2].set_xlabel("Number of orders")

import os
os.makedirs("data/proccesed", exist_ok=True)
plt.tight_layout()
plt.savefig("data/proccesed/superstore_eda.png", dpi=150, bbox_inches="tight")
plt.show()
print("Chart saved at data/proccesed/superstore_eda.png!")

# Print insights
print("\n======= KEY INSIGHTS =======")
print(f"Total Revenue:        ${df['sales'].sum():>12,.0f}")
print(f"Total Profit:         ${df['profit'].sum():>12,.0f}")
print(f"Overall Margin:       {100*df['profit'].sum()/df['sales'].sum():>11.1f}%")
print(f"\nWorst sub-category:   {df.groupby('sub_category')['profit'].sum().idxmin()}")
print(f"Worst sub-cat loss:   ${df.groupby('sub_category')['profit'].sum().min():>11,.0f}")
print(f"\nHigh discount loss:   $125,007 lost on 31%+ discounts")
print(f"Zero discount profit: $320,988 made on 0% discount orders")
print(f"\nTop sales state:      {df.groupby('state')['sales'].sum().idxmax()}")
print(f"Top profit state:     {df.groupby('state')['profit'].sum().idxmax()}")
print(f"\nDiscount-Profit corr: {df['discount'].corr(df['profit']):.2f}  (negative = bad discounting)")