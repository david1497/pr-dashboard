from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from .callbacks import register_callbacks

def create_dash_app(flask_app):
    dash_app = Dash(
        __name__,
        server=flask_app,
        url_base_pathname='/',
        external_stylesheets=[dbc.themes.BOOTSTRAP, 
                              dbc.icons.BOOTSTRAP, 
                              dbc.icons.FONT_AWESOME,
                              'overview.css', 
                              'footer.css', 
                              "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"],
        external_scripts=['/assets/swipe.js', 
                          '/assets/scroll.js',
                          "https://cdnjs.cloudflare.com/ajax/libs/hammer.js/2.0.8/hammer.min.js"],
        suppress_callback_exceptions=True
    )

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content')
    ])
    
    # layout
    register_callbacks(dash_app)

    return dash_app