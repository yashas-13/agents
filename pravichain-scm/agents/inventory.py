"""Inventory Optimization Agent."""

import numpy as np
import pandas as pd
import pulp as pl
import psycopg2


def fetch_stock_levels(conn):
    query = "SELECT sku, location, stock, lead_time FROM inventory;"
    return pd.read_sql(query, conn)


def optimize_reorder(df):
    """Simple EOQ-based optimization placeholder."""
    results = []
    for _, row in df.iterrows():
        demand = max(row['stock'], 1)
        order_cost = 50
        holding_cost = 2
        eoq = np.sqrt((2 * demand * order_cost) / holding_cost)
        results.append({'sku': row['sku'], 'location': row['location'], 'eoq': eoq})
    return pd.DataFrame(results)


def store_reorder_plan(conn, plan_df):
    plan_df.to_sql('reorder_plan', conn, if_exists='replace')


def main():
    conn = psycopg2.connect(dbname='scm', user='user', password='pass', host='localhost')
    df = fetch_stock_levels(conn)
    plan = optimize_reorder(df)
    store_reorder_plan(conn, plan)
    print('Reorder plan generated')


if __name__ == '__main__':
    main()
