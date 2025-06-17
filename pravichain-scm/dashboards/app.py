"""Dashboard Agent with role-based views."""

import pandas as pd
import plotly.express as px
import numpy as np
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data for demo purposes
sales_df = pd.DataFrame(
    {
        "date": pd.date_range("2023-01-01", periods=30),
        "sales": np.random.randint(80, 200, size=30),
    }
)

inventory_df = pd.DataFrame(
    {
        "sku": ["A", "B", "C"],
        "stock": np.random.randint(10, 50, size=3),
    }
)

routes_df = pd.DataFrame(
    {
        "route": ["R1", "R2", "R3"],
        "success_rate": np.random.randint(80, 99, size=3),
    }
)

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
    # Update sample data to simulate real-time changes
    sales_df["sales"] += np.random.randint(-5, 6, size=len(sales_df))
    inventory_df["stock"] += np.random.randint(-2, 3, size=len(inventory_df))
    routes_df["success_rate"] += np.random.randint(-1, 2, size=len(routes_df))

    if role == "Manufacturer":
        fig = px.line(sales_df, x="date", y="sales", title="Weekly Sales Forecast")
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
        fig = px.line(sales_df, x="date", y="sales", title="Sales Overview")
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
