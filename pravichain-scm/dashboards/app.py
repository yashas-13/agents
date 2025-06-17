"""Dashboard Agent with role-based views."""

import pandas as pd
import plotly.express as px
import numpy as np
import sqlite3
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Attempt to open the local SQLite database if available
try:
    DB_CONN = sqlite3.connect("db/scm.sqlite", check_same_thread=False)
except sqlite3.Error:
    DB_CONN = None

# Fallback sample data if the database isn't available
sales_df = pd.DataFrame(
    {
        "ds": pd.date_range("2023-01-01", periods=30),
        "yhat": np.random.randint(80, 200, size=30),
    }
)

inventory_df = pd.DataFrame(
    {
        "sku": ["A", "B", "C"],
        "stock": np.random.randint(10, 50, size=3),
        "location": ["WH1", "WH2", "WH3"],
    }
)

routes_df = pd.DataFrame(
    {
        "route": ["R1", "R2", "R3"],
        "success_rate": np.random.randint(80, 99, size=3),
    }
)


def load_db_table(query, fallback_df):
    """Utility to load a table from the SQLite DB with fallback."""
    if DB_CONN is None:
        return fallback_df
    try:
        return pd.read_sql(query, DB_CONN)
    except Exception:
        return fallback_df

roles = [
    "Super Admin",
    "Manufacturer",
    "CFA",
    "Super Stockist",
    "Stockist",
    "Auditor",
]

app.layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H1("PraviChain SCM Dashboard"))),
        dbc.Row(
            dbc.Col(
                dcc.Dropdown(
                    id="role-dropdown",
                    options=[{"label": r, "value": r} for r in roles],
                    value="Manufacturer",
                    clearable=False,
                ),
                width=4,
            )
        ),
        dbc.Row(dbc.Col(id="role-content")),
        dcc.Interval(id="interval-refresh", interval=10000, n_intervals=0),
    ],
    fluid=True,
)


@app.callback(
    Output("role-content", "children"),
    [Input("role-dropdown", "value"), Input("interval-refresh", "n_intervals")],
)
def render_content(role, _):
    """Render role-specific dashboard content with live updates."""
    global sales_df, inventory_df, routes_df

    # Load latest data from the DB if available
    sales_df = load_db_table("SELECT ds, yhat FROM forecast", sales_df)
    inventory_df = load_db_table(
        "SELECT sku, stock, location FROM inventory", inventory_df
    )
    routes_df = load_db_table(
        "SELECT id as route, 100 as success_rate FROM deliveries", routes_df
    )

    if role == "Manufacturer":
        fig = px.line(sales_df, x="ds", y="yhat", title="Weekly Sales Forecast")
        return dbc.Card(dcc.Graph(figure=fig), body=True)

    if role == "CFA":
        table = dash_table.DataTable(
            data=inventory_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in inventory_df.columns],
            sort_action="native",
            filter_action="native",
            page_size=5,
        )
        return dbc.Card(table, body=True)

    if role == "Super Stockist":
        fig = px.bar(routes_df, x="route", y="success_rate", title="Route Success Rate")
        return dbc.Card(dcc.Graph(figure=fig), body=True)

    if role == "Stockist":
        fig = px.line(sales_df, x="ds", y="yhat", title="Sales Overview")
        return dbc.Card(dcc.Graph(figure=fig), body=True)

    if role == "Auditor":
        return dbc.Alert("Audit reports will appear here.", color="info")

    # Super Admin or other roles
    items = html.Ul(
        [
            html.Li("Monitor all agents"),
            html.Li("View analytics"),
            html.Li("Manage users"),
        ]
    )
    return dbc.Card(items, body=True)


def main():
    """Entry point for the dashboard agent."""
    app.run(debug=True)


if __name__ == "__main__":
    main()
