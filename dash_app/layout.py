import os, dash
from dash import html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from flask_login import current_user

from .helpers.data_table_styling import data_bars
from .helpers.navbar import build_nav
from .helpers.etl import build_area_chart

# import time
# from memory_profiler import memory_usage


# Sample data
df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
agg_df.reset_index(inplace=True)
# Checking which approach is faster
# start_time = time.time()
# start_mem = memory_usage()[0]
last_date_df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx', sheet_name='LastStatePerProject_VIEW')
# last_date_idx = df.groupby('Project Name')['Date'].idxmax()
# last_date_df = df.loc[last_date_idx].reset_index(drop=True)
last_date_df = last_date_df.drop(['Date'], axis='columns')
# end_mem = memory_usage()[0]
# end_time = time.time()
# print(f'\n\n\nFinished in {end_time - start_time} and used {end_mem - start_mem}')
# Done checking

fig1 = px.pie(agg_df, values='Prelims', names='Project Name')
fig1.update_layout(title={'text': "Prelims", 'x':0.5, 'xanchor': 'center'})
fig2 = px.pie(agg_df, values='Measured Works', names='Project Name')
fig2.update_layout(title={'text': "Measured Works", 'x':0.5, 'xanchor': 'center'})
fig3 = px.pie(agg_df, values='ToComplete Costs', names='Project Name')
fig3.update_layout(title={'text': "Costs To Complete", 'x':0.5, 'xanchor': 'center'})
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



# Define the layout of the app
layout = html.Div(children=[
    dbc.Row(
        [
            dbc.Col(html.Hr())
        ],
        className="row_splitter"
    ),
    dbc.Row([
        dbc.Col([
            html.H5('Prelims'),
            dcc.Graph(
                figure=prelims_kpi, 
                id="prelims_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ],
        className='kpi_col'
        ), 
        dbc.Col([
            html.H5('Measured Works'),
            dcc.Graph(
                figure=measured_works_kpi, 
                id="measured_works_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ], 
        className='kpi_col'),
        dbc.Col([
            html.H5('Actual Costs'),
            dcc.Graph(
                figure=costs_kpi, 
                id="costs_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ], 
        className='kpi_col'),
        dbc.Col([
            html.H5('Actual Revenue'),
            dcc.Graph(
                figure=revenue_kpi, 
                id="revenue_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ], 
        className='kpi_col'),
        dbc.Col([
            html.H5('Estimated Profit'),
            dcc.Graph(
                figure=profit_kpi, 
                id="profit_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ], 
        className='kpi_col'),
        dbc.Col([
            html.H5('Margin'),
            dcc.Graph(
                figure=margin_kpi, 
                id="margin_kpi",
                animate=True,
                responsive=True,
                style={'height':'12vh'},
                config={'displayModeBar': False}
            )
        ],
        className='kpi_col'),
    ],
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
    dbc.Row(
        [
            dbc.Col(
                html.Div(dcc.Graph(
                    figure=fig1, 
                    id="prelims",
                    animate=True,
                    responsive=True)), 
                width=4,
                className='pie_chart prelims'
            ),
            dbc.Col(
                html.Div(dcc.Graph(figure=fig2, id="measured_works")), 
                width=4,
                className='pie_chart measure_works'
            ),
            dbc.Col(
                html.Div(dcc.Graph(figure=fig3, id="costs_to_complete")), 
                width=4,
                className='pie_chart costs_to_complete'
            ),
        ],
        className='second_row',        
    ),
])