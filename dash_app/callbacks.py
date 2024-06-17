from dash.dependencies import Input, Output # type: ignore
import dash # type: ignore
from dash import callback_context # type: ignore
import dash_bootstrap_components as dbc # type: ignore
from flask_login import current_user # type: ignore
import pandas as pd
from .main_layout import main_layout
from .layout_costs import layout_costs
from .layout_suppliers import layout_suppliers
from .layout_labour import layout_labour
from .layout_materials import layout_materials
from .layout_reports import layout_reports
from .layout import layout
from .helpers.etl import build_area_chart
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
    

    @dash_app.callback([Output("prelims_kpi", "figure"), Output("measured_works_kpi", "figure"),
                        Output("costs_kpi", "figure"), Output("revenue_kpi", "figure"),
                        Output("profit_kpi", "figure"), Output("margin_kpi", "figure")                        ], 
                       [Input("overview_table", "selected_rows"), Input("overview_table", "data")])
    def update_kpi_charts(selected_rows, data):
        selected_projects = []
        if selected_rows != None:
            for sr in selected_rows:
                selected_projects.append(data[sr]['Project Name'])
            df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
            df = df[df['Project Name'].isin(selected_projects)]

        else:
            df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')

        prelims_kpi = build_area_chart(df, 'Prelims', lc='rgba(39, 19, 190, 0.96)', fc='rgba(149, 142, 202, 0.64)')
        measured_works_kpi = build_area_chart(df, 'Measured Works', lc='rgba(25, 130, 58, 0.94)', fc='rgba(83, 233, 130, 0.45)')
        costs_kpi = build_area_chart(df, 'Act. Costs', lc='rgba(211, 118, 60, 0.95)', fc='rgba(242, 161, 21, 0.35)')
        revenue_kpi = build_area_chart(df, 'Act. Revenue', lc='rgba(20, 51, 137, 1)', fc='rgba(89, 167, 255, 0.53)')
        profit_kpi = build_area_chart(df, 'Est. Profit', lc='rgba(199, 181, 35, 1)', fc='rgba(255, 232, 138, 0.44)')
        margin_kpi = build_area_chart(df, 'Margin (%)', lc='rgba(233, 89, 145, 0.94)', fc='rgba(245, 130, 145, 0.28)')

        return prelims_kpi, measured_works_kpi, costs_kpi, revenue_kpi, profit_kpi, margin_kpi
    


    @dash_app.callback(Output('page-content', 'children'),
                       [Input('url', 'pathname')])
    def display_page(pathname):
        if pathname == '/costs' or pathname == '/costs/':
            return main_layout
        elif pathname == '/suppliers' or pathname == '/suppliers/':
            return main_layout #layout_suppliers
        elif pathname == '/materials' or pathname == '/materials/':
            return main_layout #layout_materials
        elif pathname == '/reports' or pathname == '/reports/':
            return main_layout #layout_reports
        elif pathname == '/labour' or pathname == '/labour/':
            return main_layout #layout_labour
        elif pathname == '/overview' or pathname == '/overview/':
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
    

    # @dash_app.callback(Output("output", "children"), [Input("bottom_slider", "value")])
    # def get_horizontal_pos(value):
    #     return value
    

    # @dash_app.callback(Output("output1", "children"), [Input("side_slider", "value")])
    # def get_vertical_pos(value):
    #     return value
    

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
        [Output('main-page-content', 'children'), Output('page-title', 'children')],
        [Input('url', 'pathname')]
    )
    def display_page(pathname):
        
        ctx = callback_context
        if not ctx.triggered:
            print("No callback triggered")
        else:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback triggered by: {triggered_input}")

        if pathname == '/overview' or pathname == '/overview/':
            return layout, "Overview page"
        elif pathname == '/costs' or pathname == '/costs/':
            return layout_costs, "Costs page"
        elif pathname == '/materials' or pathname == '/materials/':
            return layout_materials, "Materials page"
        elif pathname == '/labour' or pathname == '/labour/':
            return layout_labour, "Labour page"
        elif pathname == '/suppliers' or pathname == '/suppliers/':
            return layout_suppliers, "Suppliers page"
        elif pathname == '/reports' or pathname == '/reports/':
            return layout_reports, "Reports page"
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
        if pathname == '/costs' or pathname == '/costs/':
            classes[0] += ' active'
        elif pathname == '/suppliers' or pathname == '/suppliers/':
            classes[1] += ' active'
        elif pathname == '/labour' or pathname == '/labour/':
            classes[2] += ' active'
        elif pathname == '/materials' or pathname == '/materials/':
            classes[3] += ' active'
        elif pathname == '/reports' or pathname == '/reports/':
            classes[4] += ' active'
        return classes