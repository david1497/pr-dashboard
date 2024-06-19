import os, dash
from dash import html, dcc, dash_table #, callback_context
# from dash.dependencies import Input, Output
# from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
# from flask_login import current_user
from .helpers.data_importer import df, last_date_df

from .helpers.data_table_styling import data_bars
from .helpers.navbar import build_nav
from .helpers.etl import build_area_chart
from .helpers.layout_components import build_map


prelims_kpi = build_area_chart(df, 'Prelims', lc='rgba(39, 19, 190, 0.96)', fc='rgba(149, 142, 202, 0.64)')
measured_works_kpi = build_area_chart(df, 'Measured Works', lc='rgba(25, 130, 58, 0.94)', fc='rgba(83, 233, 130, 0.45)')
costs_kpi = build_area_chart(df, 'Act. Costs', lc='rgba(211, 118, 60, 0.95)', fc='rgba(242, 161, 21, 0.35)')
revenue_kpi = build_area_chart(df, 'Act. Revenue', lc='rgba(20, 51, 137, 1)', fc='rgba(89, 167, 255, 0.53)')
profit_kpi = build_area_chart(df, 'Est. Profit', lc='rgba(199, 181, 35, 1)', fc='rgba(255, 232, 138, 0.44)')
margin_kpi = build_area_chart(df, 'Margin (%)', lc='rgba(233, 89, 145, 0.94)', fc='rgba(245, 130, 145, 0.28)')


# Define progress bar template
def progress_bar_template(per):
    return html.Div(
        [
            html.Div(
                style={"width": "{}%".format(str(per))},
                className="progress-bar progress-bar-striped progress-bar-animated",
                children=[],
            )
        ],
        className="progress",
    )


# Format function for the Percentage column
def format_percentage(percentage):
    return progress_bar_template(percentage) if isinstance(percentage, int) else percentage


def build_kpi_column(kpi_name, kpi_title, kpi_figure):
    kpi_col = dbc.Col([
        html.Div([
            html.H5(kpi_title),
            html.H6('', id=f'{kpi_name}_kpi_change_value'), # make it as percentage
            html.H6('', id=f'{kpi_name}_kpi_change_icon')
        ]),
        html.Div([
            dcc.Graph(
                figure=kpi_figure, 
                id=f"{kpi_name}_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            ),
            html.H6('', id=f'{kpi_name}_kpi_current_value')
        ])
    ],
    className='kpi_col'),

    return kpi_col 

kpi_dict = {
    'prelims': [prelims_kpi, 'Prelims'],
    'measured_works': [measured_works_kpi, 'Measured Works'],
    'costs': [costs_kpi, 'Actual Costs'],
    'revenue': [revenue_kpi, 'Actual Revenue'],
    'profit': [profit_kpi, 'Estimated Profit'],
    'margin': [margin_kpi, 'Margin'],
}


# Define the layout of the app
layout = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(html.Hr())
        ],
        className="row_splitter"
    ),
    dcc.Store(id='filtered-data-store', storage_type='memory'),  # Store for filtered data
    dcc.Store(id='selected-projects-store', storage_type='memory'),  # Store for filtered data selected-projects-store
    dbc.Row(
        [build_kpi_column(k, v[1], v[0])[0] for k,v in kpi_dict.items()],
        className='kpi_row'
    ),
    dbc.Row(
        [
            dbc.Col(html.Hr())
        ],
        className="row_splitter"
    ),
    dbc.Row(
        [dbc.Col(
            html.Div([
                dash_table.DataTable(
                    id='overview_table',
                    columns=[{'name':col, 'id':col} for col in last_date_df.columns],
                    data = last_date_df.to_dict('records'),
                    row_selectable='multiple',
                    page_size=10,
                    style_data_conditional=(
                        data_bars(last_date_df, 'Complete (%)')
                    ),
                    sort_action='native',
                ),
                dcc.Link(
                    id='redirect-link',
                    children=html.Div(id='dummy-div'),
                    href='https://plotly.com/python/pie-charts/',
                    style={'display':'none'}
                )
            ],
            className="main_table"
            ),
            width=12,
        )],
        className='first_row'
    ),
    dbc.Row(
        [
            dbc.Col(html.Hr())
        ],
        className="row_splitter"
    ),
    dbc.Row(children=[],
        className='second_row', 
        id='pie_charts_row'      
    ),
    dbc.Row([
        dbc.Button(
            "Open Charts",
            color="primary",
            id="open_charts_collapse_btn",
            className="me-1",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Row(
                id='pie_charts_row',
                # width=12     
            ),
            id='pie_charts_collapse',
            is_open=True,
        )],
        className='second_row', 
    ),
    dbc.Col(html.Hr()),
    dbc.Row([
        dbc.Button(
            "Open Map",
            color="primary",
            id="open_map_collapse_btn",
            className="me-1",
            n_clicks=0,
        ),
        dbc.Collapse(
            build_map(),
            id='maps_collapse',
            is_open=True,
        )],
        className='second_row', 
        id='maps_row'      
    ),
])