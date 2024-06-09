from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from urllib.parse import parse_qs, urlparse
from flask_login import current_user
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
    

    @dash_app.callback(Output("output", "children"), [Input("bottom_slider", "value")])
    def get_horizontal_pos(value):
        return value
    

    @dash_app.callback(Output("output1", "children"), [Input("side_slider", "value")])
    def get_vertical_pos(value):
        return value
    


    # Update layout based on URL parameters
    @dash_app.callback(
        Output('bottom_slider', 'value'),
        Output('side_slider', 'value'),
        [Input('url', 'search')]
    )
    def update_radio_values(search):
        parsed = parse_qs(urlparse(search).query)
        bottom_slider_value = parsed.get('bottom_slider', ['left'])[0]
        side_slider_value = parsed.get('side_slider', ['1'])[0]
        return bottom_slider_value, side_slider_value




    @dash_app.callback(
        Output('url', 'href'),
        [Input('side_slider', 'value'), Input('bottom_slider', 'value')]
    )
    def update_url(side_slider_value, bottom_slider_value):
        base_url = '/'
        if bottom_slider_value == 'left' and side_slider_value == "1":
            # return '/overview'
            return f'{base_url}overview?radio1={side_slider_value}&radio2={bottom_slider_value}'
        elif bottom_slider_value == 'left' and side_slider_value == "2":
            # return '/costs'    
            return f'{base_url}costs?radio1={side_slider_value}&radio2={bottom_slider_value}'             
        elif bottom_slider_value == 'left' and side_slider_value == "3":
            # return '/labour'
            return f'{base_url}labour?radio1={side_slider_value}&radio2={bottom_slider_value}'
        elif bottom_slider_value == 'right' and side_slider_value == "1":
            # return '/materials'
            return f'{base_url}materials?radio1={side_slider_value}&radio2={bottom_slider_value}'
        elif bottom_slider_value == 'right' and side_slider_value == "2":
            # return '/suppliers'
            return f'{base_url}suppliers?radio1={side_slider_value}&radio2={bottom_slider_value}'
        elif bottom_slider_value == 'right' and side_slider_value == "3":
            # return '/reports'
            return f'{base_url}reports?radio1={side_slider_value}&radio2={bottom_slider_value}'
        return '/'