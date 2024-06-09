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


df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
agg_df.reset_index(inplace=True)
fig1 = px.pie(agg_df, values='Prelims', names='Project Name')
fig1.update_layout(title={'text': "Prelims", 'x':0.5, 'xanchor': 'center'})
fig2 = px.pie(agg_df, values='Measured Works', names='Project Name')
fig2.update_layout(title={'text': "Measured Works", 'x':0.5, 'xanchor': 'center'})
fig3 = px.pie(agg_df, values='ToComplete Costs', names='Project Name')
fig3.update_layout(title={'text': "Costs To Complete Costs", 'x':0.5, 'xanchor': 'center'})



# Define the layout of the app
layout_costs = html.Div(children=[
    build_nav(user_type='admin'),
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
                html.Div(dcc.Graph(figure=fig1, id="prelims")), 
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
    dbc.RadioItems(
        id="bottom_slider",
        className="btn-group footer_slider",
        inputClassName="btn-check",
        labelClassName="btn btn-outline-primary",
        labelCheckedClassName="active",
        options=[
            {"label": "LEFT", "value": 'left'},
            {"label": "RIGHT", "value": 'right'}
        ],
        value='left',
    ),
    dbc.RadioItems(
            id="side_slider",
            className="side_slider",
            options=[
                {"label": "", "value": "1"},
                {"label": "", "value": "2"},
                {"label": "", "value": "3"},
            ],
            value="1",
        ),
], 
id='page-content')