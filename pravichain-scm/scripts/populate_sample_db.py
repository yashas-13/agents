import sqlite3
import pandas as pd
import os

os.makedirs('db', exist_ok=True)
conn = sqlite3.connect('db/scm.sqlite')

conn.execute("CREATE TABLE IF NOT EXISTS sales_data (date TEXT, sku TEXT, quantity INTEGER)")
conn.execute("CREATE TABLE IF NOT EXISTS inventory (sku TEXT, location TEXT, stock INTEGER, lead_time INTEGER)")
conn.execute("CREATE TABLE IF NOT EXISTS deliveries (id INTEGER PRIMARY KEY, address_lat REAL, address_lon REAL, status TEXT)")
conn.execute("CREATE TABLE IF NOT EXISTS invoices (id INTEGER PRIMARY KEY, vendor TEXT, amount REAL)")

sales = pd.DataFrame({
    'date': pd.date_range('2023-01-01', periods=10).astype(str),
    'sku': ['A'] * 10,
    'quantity': list(range(10, 20))
})
sales.to_sql('sales_data', conn, if_exists='replace', index=False)

inventory = pd.DataFrame({
    'sku': ['A', 'B'],
    'location': ['WH1', 'WH2'],
    'stock': [100, 150],
    'lead_time': [2, 3]
})
inventory.to_sql('inventory', conn, if_exists='replace', index=False)

deliveries = pd.DataFrame({
    'id': [1, 2],
    'address_lat': [12.9716, 12.2958],
    'address_lon': [77.5946, 76.6394],
    'status': ['pending', 'pending']
})
deliveries.to_sql('deliveries', conn, if_exists='replace', index=False)

invoices = pd.DataFrame({
    'id': [1],
    'vendor': ['ACME'],
    'amount': [100.0]
})
invoices.to_sql('invoices', conn, if_exists='replace', index=False)

conn.commit()
conn.close()
print('Sample database created.')
