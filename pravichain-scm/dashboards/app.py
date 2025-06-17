"""Dashboard Agent."""

import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('PraviChain SCM Dashboard'),
    html.P('Placeholder dashboard')
])

if __name__ == '__main__':
    app.run_server(debug=True)
