import dash_bootstrap_components as dbc
from dash import html, dcc


def build_nav(user_type='admin'):
    
    navbar = html.Div([
        dcc.Store(id='username-store', data={'username': ''}),
        dbc.Row(
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem(dbc.NavLink("COSTS", href="costs", id='costs-link')),
                    dbc.NavItem(dbc.NavLink("SUPPLIERS", href="suppliers", id='suppliers-link')),
                    dbc.NavItem(dbc.NavLink("LABOUR", href="labour", id='labour-link')),
                    dbc.NavItem(dbc.NavLink("MATERIALS", href="materials", id='materials-link')),
                    dbc.NavItem(dbc.NavLink("REPORTS", href="reports", id='reports-link')),
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