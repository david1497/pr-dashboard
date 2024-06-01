import dash
from dash import html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import os

from .helpers.data_table_styling import data_bars

print(os.getcwd())

# Sample data
df = pd.read_excel('../dash_app/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
agg_df.reset_index(inplace=True)
fig1 = px.pie(agg_df, values='Project Name', names='Prelims', title='Prelims')
fig2 = px.pie(agg_df, values='Project Name', names='Measured Works', title='Measured Works')
fig3 = px.pie(agg_df, values='Project Name', names='ToComplete Costs', title='Costs To Complete')



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


def build_nav(user_type='admin'):
    
    navbar = html.Div(
    dbc.Row(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("COSTS", href="/")),
                dbc.NavItem(dbc.NavLink("SUPPLIERS", href="overview")),
                dbc.NavItem(dbc.NavLink("LABOUR", href="#")),
                dbc.NavItem(dbc.NavLink("MATERIALS", href="#")),
                dbc.NavItem(dbc.NavLink("REPORTS", href="#")),
                dbc.NavItem(dbc.NavLink("PLACEHOLDER", href="#")),
            ],
            brand="PlattReilly",
            brand_href="#",
            color="primary",
            dark=True,
            fixed="top"
        )
    ))

    return navbar





# Define the layout of the app
layout = html.Div(children=[
    build_nav(user_type='admin'),
    dbc.Row(
        html.Div(
            dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True),
            className="mt-lg-5 col-md-10",
            style={"margin":"auto"}
        )
    ),

    dbc.Row(
        [dbc.Col(
            html.Div([
                dash_table.DataTable(
                    id='overview_table',
                    columns=[{'name':col, 'id':col} for col in df.columns],
                    data = df.to_dict('records'),
                    row_selectable='single',
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
            ]),
            width=11,
            align="center"
        )],
        align="center"
    ),

    dbc.Row(
        [
            dbc.Col(
                html.Div(dcc.Graph(figure=fig1, id="prelims")), 
                width=3
            ),
            dbc.Col(
                html.Div(dcc.Graph(figure=fig2, id="measured_works")), 
                width=3
            ),
            dbc.Col(
                html.Div(dcc.Graph(figure=fig3, id="costs_to_complete")), 
                width=3
            ),
        ]
        
    ),
])