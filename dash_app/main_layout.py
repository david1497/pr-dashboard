from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

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
main_layout = html.Div(children=[
    build_nav(user_type='admin'),
    dbc.Row([
        dbc.Col([
            html.Div([
                html.H3('Overview page', className='page-title', id='page-title')
            ])
         ])
    ],
    className='title_row'),
    html.Div(id='main-page-content'),
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
])