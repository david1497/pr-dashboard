from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from flask_login import current_user
from dash import html
import requests
from .layout_costs import layout_costs
from .layout_suppliers import layout_suppliers
from .layout_labour import layout_labour
from .layout_materials import layout_materials
from .layout_reports import layout_reports
from .layout import layout


def register_callbacks(dash_app):
    # define other callbacks below this one.
    @dash_app.callback(
        Output('username-store', 'data'),
        [Input('username_nav_item', 'id')]
    )
    def update_username(_):
        return {'username': current_user.username if current_user.is_authenticated else 'Guest'}


    @dash_app.callback(
        Output('username_nav_item', 'children'),
        Input('username-store', 'data')
    )
    def display_username(data):
        return dbc.NavLink(data['username'], href="#")
    

    @dash_app.callback(Output('page-content', 'children'),
                       [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/costs':
            return layout_costs
        elif pathname == '/suppliers':
            return layout_suppliers
        elif pathname == '/materials':
            return layout_materials
        elif pathname == '/reports':
            return layout_reports
        elif pathname == '/labour':
            return layout_labour
        elif pathname == '/overview':
            return layout
        else:
            return layout
        
    
    # Add callback for the slider
    @dash_app.callback(
        Output('slider-output-container', 'children'),
        [Input('footer-slider', 'value')]
    )
    def update_output(value):
        return f'You have selected {value}'
    

    @dash_app.callback(Output("output", "children"), [Input("radios", "value")])
    def get_horizontal_pos(value):
        return value
    

    @dash_app.callback(Output("output1", "children"), [Input("side_slider", "value")])
    def get_vertical_pos(value, checklist_value, switches_value):
        return value