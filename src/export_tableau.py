import pandas as pd

df = pd.read_csv("data/raw/Sample - Superstore.csv", encoding="latin1")
df.columns = [c.strip().lower().replace(" ", "_").replace("-","_") for c in df.columns]


# Export clean version for Tableau direct connect
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days
df["order_date"] = df["order_date"].dt.strftime("%m/%d/%Y")
df["ship_date"] = df["ship_date"].dt.strftime("%m/%d/%Y")
df["profit_margin_pct"] = round(100 * df["profit"] / df["sales"], 2)
df["discount_band"] = pd.cut(df["discount"],
    bins=[-0.01,0,0.10,0.20,0.30,1.0],
    labels=["0%","1-10%","11-20%","21-30%","31%+"])

import os
os.makedirs("data/proccesed", exist_ok=True)
df.to_csv("data/proccesed/superstore_tableau.csv", index=False)
print("Done — connect Tableau to data/proccesed/superstore_tableau.csv")
