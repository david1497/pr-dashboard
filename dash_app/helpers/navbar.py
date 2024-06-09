import dash_bootstrap_components as dbc
from dash import html, dcc


def build_nav(user_type='admin'):
    
    navbar = html.Div([
        dcc.Store(id='username-store', data={'username': ''}),
        dbc.Row(
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("COSTS", href="costs")),
                    dbc.NavItem(dbc.NavLink("SUPPLIERS", href="suppliers")),
                    dbc.NavItem(dbc.NavLink("LABOUR", href="labour")),
                    dbc.NavItem(dbc.NavLink("MATERIALS", href="materials")),
                    dbc.NavItem(dbc.NavLink("REPORTS", href="reports")),
                    dbc.NavItem(id='username_nav_item', children=dbc.NavLink("", href="#")),
                    dbc.NavItem(id='output'),
                    dbc.NavItem(id='output1'),
                ],
                brand="PlattReilly",
                brand_href="overview",
                color="primary",
                dark=True,
                fixed="top"
            )
        )
    ])

    return navbar