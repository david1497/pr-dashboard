from dash import Dash
import dash_bootstrap_components as dbc
from .layout import layout
from .callbacks import register_callbacks

def create_dash_app(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/overview/',
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )
    dash_app.layout = layout
    register_callbacks(dash_app)

    return dash_app