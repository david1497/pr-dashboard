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

# Sample data
df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
agg_df.reset_index(inplace=True)
fig1 = px.pie(agg_df, values='Prelims', names='Project Name')
fig1.update_layout(title={'text': "Prelims", 'x':0.5, 'xanchor': 'center'})
fig2 = px.pie(agg_df, values='Measured Works', names='Project Name')
fig2.update_layout(title={'text': "Measured Works", 'x':0.5, 'xanchor': 'center'})
fig3 = px.pie(agg_df, values='ToComplete Costs', names='Project Name')
fig3.update_layout(title={'text': "Costs To Complete", 'x':0.5, 'xanchor': 'center'})



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
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
        ], 
        className='kpi_col'),
        dbc.Col([
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
        ], 
        className='kpi_col'),
        dbc.Col([
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
        ], 
        className='kpi_col'),
        dbc.Col([
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
        ], 
        className='kpi_col'),
        dbc.Col([
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
        ], 
        className='kpi_col'),
        dbc.Col([
            html.Div([
                html.H5('Overview page'),
                html.H2('1 000 520')
            ])
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
                    columns=[{'name':col, 'id':col} for col in df.columns],
                    data = df.to_dict('records'),
                    row_selectable='multiple',
                    page_size=10,
                    style_data_conditional=(
                        data_bars(df, 'Complete (%)')
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