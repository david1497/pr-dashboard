from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from .layout import layout
from .layout_costs import layout_costs
from .callbacks import register_callbacks

def create_dash_app(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/',
        external_stylesheets=[dbc.themes.BOOTSTRAP, 'overview.css']
    )
    
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    
    # layout
    register_callbacks(dash_app)

    return dash_app