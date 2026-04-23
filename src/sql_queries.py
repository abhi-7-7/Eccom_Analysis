import sqlite3
import pandas as pd

conn = sqlite3.connect("superstore.db")

queries = {}

# 1. Monthly revenue + profit trend with MoM growth
queries["monthly_trend"] = """
SELECT
    strftime('%Y-%m', order_date) AS month,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS profit_margin_pct,
    ROUND(SUM(sales) - LAG(SUM(sales)) OVER (ORDER BY strftime('%Y-%m', order_date)), 2) AS mom_sales_change
FROM orders
GROUP BY month
ORDER BY month;
"""

# 2. Sales + profit by category and sub-category
queries["category_breakdown"] = """
SELECT
    category,
    sub_category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS profit_margin_pct,
    ROUND(AVG(discount), 2) AS avg_discount
FROM orders
GROUP BY category, sub_category
ORDER BY total_sales DESC;
"""

# 3. Regional performance
queries["regional_performance"] = """
SELECT
    region,
    state,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(100.0 * SUM(profit) / SUM(sales), 1) AS profit_margin_pct
FROM orders
GROUP BY region, state
ORDER BY total_profit DESC;
"""

# 4. Shipping performance by ship mode
queries["shipping_analysis"] = """
SELECT
    ship_mode,
    COUNT(*) AS total_orders,
    ROUND(AVG(shipping_days), 1) AS avg_shipping_days,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_of_orders
FROM orders
GROUP BY ship_mode
ORDER BY avg_shipping_days;
"""

# 5. Top 10 customers by revenue with rank
queries["top_customers"] = """
SELECT
    customer_name,
    customer_id,
    segment,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS lifetime_sales,
    ROUND(SUM(profit), 2) AS lifetime_profit,
    RANK() OVER (ORDER BY SUM(sales) DESC) AS sales_rank
FROM orders
GROUP BY customer_id, customer_name, segment, region
ORDER BY lifetime_sales DESC
LIMIT 10;
"""

# 6. Discount impact on profit (key business insight)
queries["discount_vs_profit"] = """
SELECT
    CASE
        WHEN discount = 0 THEN '0% discount'
        WHEN discount <= 0.1 THEN '1-10%'
        WHEN discount <= 0.2 THEN '11-20%'
        WHEN discount <= 0.3 THEN '21-30%'
        ELSE '31%+'
    END AS discount_band,
    COUNT(*) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(AVG(profit), 2) AS avg_profit_per_order
FROM orders
GROUP BY discount_band
ORDER BY discount_band;
"""

import os
os.makedirs("data/proccesed", exist_ok=True)
for name, sql in queries.items():
    df_result = pd.read_sql_query(sql, conn)
    df_result.to_csv(f"data/proccesed/{name}.csv", index=False)
    print(f"\n--- {name} ---")
    print(df_result.head())

conn.close()
print("\nAll CSVs exported — ready for Tableau!")