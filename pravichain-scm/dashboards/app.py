"""Dashboard Agent with role-based views."""

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output

app = Dash(__name__)

# Sample data for demo purposes
sales_df = pd.DataFrame(
    {
        "date": pd.date_range("2023-01-01", periods=7),
        "sales": [100, 120, 90, 130, 150, 170, 160],
    }
)

inventory_df = pd.DataFrame(
    {
        "sku": ["A", "B", "C"],
        "stock": [40, 20, 15],
    }
)

routes_df = pd.DataFrame(
    {
        "route": ["R1", "R2", "R3"],
        "success_rate": [95, 88, 92],
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

app.layout = html.Div(
    [
        html.H1("PraviChain SCM Dashboard"),
        dcc.Dropdown(
            id="role-dropdown",
            options=[{"label": r, "value": r} for r in roles],
            value="Manufacturer",
            clearable=False,
        ),
        html.Div(id="role-content"),
    ]
)


@app.callback(Output("role-content", "children"), Input("role-dropdown", "value"))
def render_content(role):
    """Render role-specific dashboard content."""
    if role == "Manufacturer":
        fig = px.line(sales_df, x="date", y="sales", title="Weekly Sales Forecast")
        return dcc.Graph(figure=fig)
    if role == "CFA":
        return dash_table.DataTable(
            data=inventory_df.to_dict("records"),
            columns=[{"name": i, "id": i} for i in inventory_df.columns],
        )
    if role == "Super Stockist":
        fig = px.bar(routes_df, x="route", y="success_rate", title="Route Success Rate")
        return dcc.Graph(figure=fig)
    if role == "Stockist":
        fig = px.line(sales_df, x="date", y="sales", title="Sales Overview")
        return dcc.Graph(figure=fig)
    if role == "Auditor":
        return html.P("Audit reports will appear here.")
    # Super Admin or other roles
    return html.Ul(
        [
            html.Li("Monitor all agents"),
            html.Li("View analytics"),
            html.Li("Manage users"),
        ]
    )


if __name__ == "__main__":
    app.run(debug=True)
