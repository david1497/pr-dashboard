from dash.dependencies import Input, Output, State # type: ignore
import dash # type: ignore
from dash import callback_context, html # type: ignore
import dash_bootstrap_components as dbc # type: ignore
from flask_login import current_user # type: ignore
import pandas as pd
import plotly.express as px # type: ignore
from .main_layout import main_layout
from .layout_costs import layout_costs
from .layout_suppliers import layout_suppliers
from .layout_labour import layout_labour
from .layout_materials import layout_materials
from .layout_reports import layout_reports
from .layout import layout
from .helpers.etl import build_area_chart, get_nth_value_column, get_change_direction
from .helpers.data_importer import agg_df #, agg_df_t
from .helpers.layout_components import build_pie_charts, build_line_chart
# from flask_app.errors import not_found_error

agg_df_t = px.data.gapminder().query("continent=='Oceania'")

fig1 = px.pie(agg_df, values='Prelims', names='Project Name')
fig1.update_layout(title={'text': "Prelims", 'x':0.5, 'xanchor': 'center'})
fig2 = px.pie(agg_df, values='Measured Works', names='Project Name')
fig2.update_layout(title={'text': "Measured Works", 'x':0.5, 'xanchor': 'center'})
fig3 = px.pie(agg_df, values='ToComplete Costs', names='Project Name')
fig3.update_layout(title={'text': "Costs To Complete", 'x':0.5, 'xanchor': 'center'})
line_chart_fig = px.line(agg_df_t, x="year", y="lifeExp", color='country')




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
        """display_username

        Args:
            data (user_data): data containing the user details

        Returns:
            dbc.NavLink: the numb link with the username
        """
        return dbc.NavLink(data['username'], href="#")
    

    @dash_app.callback(
            [Output('filtered-data-store', 'data'), Output('selected-projects-store', 'data')],
            [Input("overview_table", "selected_rows")],
            State('overview_table', 'data'))
    def slice_data_main_table(selected_rows, data):
        """slice_data_main_table
        This callback will slice the dataframe behind the visuals in the main page based on the user selections in the main table.
        The sliced data will be passed to other callbacks using the dcc.Store object from the layout.py

        Args:
            selected_rows (_type_): _description_
            data (_type_): _description_
        """
        df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
        selected_projects = []
        if selected_rows != None:
            for sr in selected_rows:
                selected_projects.append(data[sr]['Project Name'])
            if len(selected_projects) > 0:
                df = df[df['Project Name'].isin(selected_projects)]

        return df.to_dict(), selected_projects


    kpis = ['prelims', 'measured_works', 'costs', 'revenue', 'profit', 'margin']


    update_kpi_charts_outputs = []
    for kpi in kpis:
        update_kpi_charts_outputs.append(Output(f'{kpi}_kpi', 'figure'))

    @dash_app.callback(
            update_kpi_charts_outputs,
            [Input('filtered-data-store', 'data')])
    def update_kpi_charts(df):
        """update_kpi_charts

        Reads the data from the excel file and based on the user interactions slices the dataframe and returns the kpi charts for the main page.

        Args:
            df (dict): the data as a dictionary which is transformed in a pd dataframe later.

        Returns:
            line_charts: Line charts for the kpi's pannel on the overview page.
        """

        df = pd.DataFrame(df)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
        prelims_kpi_fig = build_area_chart(df, 'Prelims', lc='rgba(39, 19, 190, 0.96)', fc='rgba(149, 142, 202, 0.64)')
        measured_works_kpi_fig = build_area_chart(df, 'Measured Works', lc='rgba(25, 130, 58, 0.94)', fc='rgba(83, 233, 130, 0.45)')
        costs_kpi_fig = build_area_chart(df, 'Act. Costs', lc='rgba(211, 118, 60, 0.95)', fc='rgba(242, 161, 21, 0.35)')
        revenue_kpi_fig = build_area_chart(df, 'Act. Revenue', lc='rgba(20, 51, 137, 1)', fc='rgba(89, 167, 255, 0.53)')
        profit_kpi_fig = build_area_chart(df, 'Est. Profit', lc='rgba(199, 181, 35, 1)', fc='rgba(255, 232, 138, 0.44)')
        margin_kpi_fig = build_area_chart(df, 'Margin (%)', lc='rgba(233, 89, 145, 0.94)', fc='rgba(245, 130, 145, 0.28)')

        return prelims_kpi_fig, measured_works_kpi_fig, costs_kpi_fig, revenue_kpi_fig, profit_kpi_fig, margin_kpi_fig
    

    update_kpi_latest_value_outputs = []
    for kpi in kpis:
        update_kpi_latest_value_outputs.append(Output(f'{kpi}_kpi_current_value', 'children'))

    @dash_app.callback(
            update_kpi_latest_value_outputs,
            [Input('filtered-data-store', 'data'), Input('selected-projects-store', 'data')])
    def update_kpi_latest_value(df, selected_projects):
        """update_kpi_latest_value

        This callback takes the sliced data and adjusts the latest value of the KPIs

        Args:
            data (dict): Dictionary with the data about the projects based on the user selections.

        Returns:
            ints: integer values representing the latest value of each kpis from the main page. 
        """
        df = pd.DataFrame(df)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')

        prelims_kpi_latest_value = get_nth_value_column(df, col_name='Prelims', selected_projects=selected_projects)
        measured_works_kpi_latest_value = get_nth_value_column(df, col_name='Measured Works', selected_projects=selected_projects)
        costs_kpi_latest_value = get_nth_value_column(df, col_name='Act. Costs', selected_projects=selected_projects)
        revenue_kpi_latest_value = get_nth_value_column(df, col_name='Act. Revenue', selected_projects=selected_projects)
        profit_kpi_latest_value = get_nth_value_column(df, col_name='Est. Profit', selected_projects=selected_projects)
        margin_kpi_latest_value = get_nth_value_column(df, col_name='Margin (%)', selected_projects=selected_projects)

        return prelims_kpi_latest_value, measured_works_kpi_latest_value, costs_kpi_latest_value, revenue_kpi_latest_value, profit_kpi_latest_value, margin_kpi_latest_value


    update_kpi_change_icon_outputs = []
    for kpi in kpis:
        update_kpi_change_icon_outputs.append(Output(f'{kpi}_kpi_change_icon', 'children'))

    @dash_app.callback(
            update_kpi_change_icon_outputs,
            [Input('filtered-data-store', 'data'), Input('selected-projects-store', 'data')])
    def update_kpi_change_icon(df, selected_projects):
        """update_kpi_change_icon

        This callback takes the sliced data and adjusts the icon depending on the change of the KPI

        Args:
            data (dict): dictionary with the data selected by the user.

        Returns:
            html.icon: changes the value of the triangle from the kpis section.
        """
        df = pd.DataFrame(df)
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')


        prelims_kpi_change = get_change_direction(df, col_name='Prelims', selected_projects=selected_projects)
        measured_works_kpi_change = get_change_direction(df, col_name='Measured Works', selected_projects=selected_projects)
        costs_kpi_change = get_change_direction(df, col_name='Act. Costs', selected_projects=selected_projects)
        revenue_kpi_change = get_change_direction(df, col_name='Act. Revenue', selected_projects=selected_projects)
        profit_kpi_change = get_change_direction(df, col_name='Est. Profit', selected_projects=selected_projects)
        margin_kpi_change = get_change_direction(df, col_name='Margin (%)', selected_projects=selected_projects)

        up = "fa-solid fa-caret-up"
        down = "fa-solid fa-caret-down"
        stable = "fa-solid fa-stop"

        prelims_kpi_change_icon = html.I(
            className=up if prelims_kpi_change > 0 else (down if prelims_kpi_change < 0 else stable), 
            style={'color':'green'} if prelims_kpi_change > 0 else ({'color':'#c51212'} if prelims_kpi_change < 0 else {'color':'#bfe2f3'}))
        measured_works_kpi_change_icon = html.I(
            className=up if measured_works_kpi_change > 0 else (down if measured_works_kpi_change < 0 else stable), 
            style={'color':'green'} if measured_works_kpi_change > 0 else ({'color':'#c51212'} if measured_works_kpi_change < 0 else {'color':'#bfe2f3'}))
        costs_kpi_change_icon = html.I(
            className=up if costs_kpi_change > 0 else (down if costs_kpi_change < 0 else stable), 
            style={'color':'green'} if costs_kpi_change > 0 else ({'color':'#c51212'} if costs_kpi_change < 0 else {'color':'#bfe2f3'}))
        revenue_kpi_change_icon = html.I(
            className=up if revenue_kpi_change > 0 else (down if revenue_kpi_change < 0 else stable), 
            style={'color':'green'} if revenue_kpi_change > 0 else ({'color':'#c51212'} if revenue_kpi_change < 0 else {'color':'#bfe2f3'}))
        profit_kpi_change_icon = html.I(
            className=up if profit_kpi_change > 0 else (down if profit_kpi_change < 0 else stable), 
            style={'color':'green'} if profit_kpi_change > 0 else ({'color':'#c51212'} if profit_kpi_change < 0 else {'color':'#bfe2f3'}))
        margin_kpi_change_icon = html.I(
            className=up if margin_kpi_change > 0 else (down if margin_kpi_change < 0 else stable), 
            style={'color':'green'} if margin_kpi_change > 0 else ({'color':'#c51212'} if margin_kpi_change < 0 else {'color':'#bfe2f3'}))


        return prelims_kpi_change_icon, measured_works_kpi_change_icon, costs_kpi_change_icon, revenue_kpi_change_icon, profit_kpi_change_icon, margin_kpi_change_icon
    
    
#--------------------------------------------------------------------
#---------------- Start of Navigation callbacks ---------------------
#--------------------------------------------------------------------    
    @dash_app.callback(
            Output('page-content', 'children'),
            Input('url', 'pathname'))
    def display_page(pathname):
        
        ctx = callback_context
        if ctx.triggered:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback display_page triggered by: {triggered_input}")

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
        

    
     # Callback to display the page content based on URL
    @dash_app.callback(
            [Output('main-page-content', 'children'), Output('page-title', 'children')],
            Input('url', 'pathname'))
    def display_page1(pathname):
        
        ctx = callback_context
        if ctx.triggered:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback display_page1 triggered by: {triggered_input}")

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
            return layout, "Overview page"
    

    #=========================== start of sliders' navigation ===================================
    @dash_app.callback(
            [Output('side_slider', 'value'), Output('bottom_slider', 'value')],
            Input('url', 'pathname'))
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
    #=========================== end of sliders' navigation ======================================


    @dash_app.callback(
            Output('url', 'pathname'),
            [Input('side_slider', 'value'), Input('bottom_slider', 'value')])
    def update_url(side_slider, bottom_slider):

        ctx = callback_context
        if ctx.triggered:
            triggered_input = ctx.triggered[0]['prop_id'].split('.')[0]
            print(f"Callback update_url triggered by: {triggered_input}")

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
        return '/overview/'
    

    # =========================== Start of callbacks that highlights the active link in the navbar ===========================
    @dash_app.callback(
            [Output('costs-link', 'className'), Output('suppliers-link', 'className'),
             Output('labour-link', 'className'), Output('materials-link', 'className'),
             Output('reports-link', 'className')],
             Input('url', 'pathname'))
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
    # =========================== End of callbacks that highlights the active link in the navbar ===========================
    
#----------------------------------------------------------------------
#------------------ End of Navigation callbacks -----------------------
#----------------------------------------------------------------------
    
    @dash_app.callback(
            [Output('pie_charts_row', 'children')],
            [Input('selected-projects-store', 'data')])
    def populate_pie_charts_row(selected_projects):
        """populate_pie_charts_row

        If one project is selected - displaying the pie charts, if several or none - displaying the line_chart
        Args:
            selected_projects (list): list of selected projects

        Returns:
            list: objects to be displayed beneath the main table in the overview tab
        """
        if len(selected_projects) == 1:
            a, b, c = build_pie_charts(fig1, fig2, fig3)
            to_display = [a, b, c]
            # Building the piecharts for the selected_projects
        else:
            to_display = build_line_chart(line_chart_fig)
            # Building the line chart for the selected_projects
        return [to_display]


    @dash_app.callback(
            Output("pie_charts_collapse", "is_open"),
            [Input("open_charts_collapse_btn", "n_clicks")],
            [State("pie_charts_collapse", "is_open")])
    def toggle_pie_charts(n_left, is_open):
        # If the pie charts/line chart should be displayed or not. 
        if n_left:
            return not is_open
        return is_open


    @dash_app.callback(
            Output("maps_collapse", "is_open"),
            [Input("open_map_collapse_btn", "n_clicks")],
            [State("maps_collapse", "is_open")])
    def toggle_maps(n_right, is_open):
        # If the map should be displayed or not.
        if n_right:
            return not is_open
        return is_open