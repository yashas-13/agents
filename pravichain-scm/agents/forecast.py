"""Demand Forecast Agent."""

from datetime import datetime
import pandas as pd
from prophet import Prophet
import psycopg2


def fetch_sales_data(conn):
    """Fetch sales data from PostgreSQL."""
    query = "SELECT date, sku, quantity FROM sales_data;"
    return pd.read_sql(query, conn)


def train_forecast_model(df):
    """Train Prophet model."""
    df = df.rename(columns={'date': 'ds', 'quantity': 'y'})
    model = Prophet()
    model.fit(df)
    return model


def generate_forecast(model, periods=30):
    future = model.make_future_dataframe(periods=periods)
    return model.predict(future)


def store_forecast(conn, forecast_df):
    forecast_df[['ds', 'yhat']].to_sql('forecast', conn, if_exists='replace')


def main():
    conn = psycopg2.connect(dbname='scm', user='user', password='pass', host='localhost')
    df = fetch_sales_data(conn)
    model = train_forecast_model(df)
    forecast = generate_forecast(model)
    store_forecast(conn, forecast)
    print("Forecast generated at", datetime.now())


if __name__ == "__main__":
    main()
