from dash.dependencies import Input, Output # type: ignore
import dash # type: ignore
from dash import callback_context # type: ignore
import dash_bootstrap_components as dbc # type: ignore
from flask_login import current_user # type: ignore
from .main_layout import main_layout
from .layout_costs import layout_costs
from .layout_suppliers import layout_suppliers
from .layout_labour import layout_labour
from .layout_materials import layout_materials
from .layout_reports import layout_reports
from .layout import layout
# from flask_app.errors import not_found_error


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
    
    
    # # Callback to update the URL based on swipe events
    # @dash_app.callback(
    #     Output('url', 'pathname'),
    #     [Input('swipe-event', 'children'), [Input('url', 'pathname')]]
    # )
    # def handle_swipe(swipe_event, url):

    #     ctx = callback_context
    #     if not ctx.triggered:
    #         print("No callback triggered")
    #     else:
    #         triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
    #         print(f"Callback triggered by: {triggered_input}")

    #     if swipe_event == 'left':
    #         # Handle left swipe (e.g., navigate to the next page)
    #         print("Swiped left")
    #         # return '/page-2'  # Example, change this to the appropriate page
    #     elif swipe_event == 'right':
    #         # Handle right swipe (e.g., navigate to the previous page)
    #         print("Swiped right")
    #         # return '/page-1'  # Example, change this to the appropriate page
    #     return dash.no_update


    @dash_app.callback(Output('page-content', 'children'),
                       [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/costs':
            return main_layout
        elif pathname == '/suppliers':
            return main_layout #layout_suppliers
        elif pathname == '/materials':
            return main_layout #layout_materials
        elif pathname == '/reports':
            return main_layout #layout_reports
        elif pathname == '/labour':
            return main_layout #layout_labour
        elif pathname == '/overview':
            return main_layout #layout
        else:
            return main_layout #layout
        
    
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
    

    @dash_app.callback(
        [Output('side_slider', 'value'), Output('bottom_slider', 'value')],
        [Input('url', 'pathname')]
    )
    def update_radios(pathname):
        page_map = {
            '/overview': ('1', 'left'),
            '/costs': ('1', 'right'),
            '/materials': ('2', 'left'),
            '/labour': ('2', 'right'),
            '/suppliers': ('3', 'left'),
            '/reports': ('3', 'right'),
        }
        if pathname in page_map:
            return page_map[pathname]
        return '1', 'left'


    @dash_app.callback(Output('url', 'pathname'),
    [Input('side_slider', 'value'), Input('bottom_slider', 'value')]
    )
    def update_url(side_slider, bottom_slider):

        ctx = callback_context
        if not ctx.triggered:
            print("No callback triggered")
        else:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback triggered by: {triggered_input}")

        if side_slider and bottom_slider:
            # Map the combination of radio buttons to specific pages
            page_map = {
                ('1', 'left'): '/overview',
                ('1', 'right'): '/costs',
                ('2', 'left'): '/materials',
                ('2', 'right'): '/labour',
                ('3', 'left'): '/suppliers',
                ('3', 'right'): '/reports',
            }
            return page_map[(side_slider, bottom_slider)]
        return '/overview'
    

    # Callback to display the page content based on URL
    @dash_app.callback(
        Output('main-page-content', 'children'),
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        
        ctx = callback_context
        if not ctx.triggered:
            print("No callback triggered")
        else:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback triggered by: {triggered_input}")

        if pathname == '/overview':
            return layout
        elif pathname == '/costs':
            return layout_costs
        elif pathname == '/materials':
            return layout_materials
        elif pathname == '/labour':
            return layout_labour
        elif pathname == '/suppliers':
            return layout_suppliers
        elif pathname == '/reports':
            return layout_reports
        else:
            pass


    @dash_app.callback(
    [Output('costs-link', 'className'),
     Output('suppliers-link', 'className'),
     Output('labour-link', 'className'),
     Output('materials-link', 'className'),
     Output('reports-link', 'className')],
    [Input('url', 'pathname')]
    )
    def update_active_link(pathname):
        # Default class for all links
        classes = ['nav-link'] * 5
        # Highlight the active link
        if pathname == '/costs':
            classes[0] += ' active'
        elif pathname == '/suppliers':
            classes[1] += ' active'
        elif pathname == '/labour':
            classes[2] += ' active'
        elif pathname == '/materials':
            classes[3] += ' active'
        elif pathname == '/reports':
            classes[4] += ' active'
        return classes