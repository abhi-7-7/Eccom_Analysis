import pandas as pd
import sqlite3

df = pd.read_csv("data/raw/Sample - Superstore.csv", encoding="latin1")
df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
df["order_date"] = pd.to_datetime(df["order_date"])
df["ship_date"] = pd.to_datetime(df["ship_date"])
df["shipping_days"] = (df["ship_date"] - df["order_date"]).dt.days

conn = sqlite3.connect("superstore.db")
df.to_sql("orders", conn, if_exists="replace", index=False)
conn.close()
print(f"Loaded {len(df)} rows into superstore.db")