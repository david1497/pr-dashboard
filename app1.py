import dash
from dash import html, dcc, dash_table, callback_context
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from src.helpers.data_table_styling import data_bars

# Sample data
df = pd.read_excel('src/assets/data/data_for_main_table.xlsx')
agg_df = df.groupby('Project Name').agg({'Prelims':'sum', 'Measured Works':'sum', 'ToComplete Costs':'sum'})
agg_df.reset_index(inplace=True)
fig1 = px.pie(agg_df, values='Project Name', names='Prelims', title='Prelims')
fig2 = px.pie(agg_df, values='Project Name', names='Measured Works', title='Measured Works')
fig3 = px.pie(agg_df, values='Project Name', names='ToComplete Costs', title='Costs To Complete')

# Initialize the Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app_title = "Dash project structure template"
app.title = app_title



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
app.layout = html.Div(children=[
    html.Div(
    dbc.Row(
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("COSTS", href="#")),
                dbc.NavItem(dbc.NavLink("SUPPLIERS", href="#")),
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
    )),
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


@app.callback(
    Output('redirect-link', 'href'),
    [Input('table', 'selected_rows')]
)
def update_link(selected_rows):
    if selected_rows:  # If a row is selected
        # Get the ID of the selected row
        selected_id = df.iloc[selected_rows[0]]['ID']
        # Construct the URL for redirection
        url = f'/redirect/{selected_id}'
        return url
    else:
        raise PreventUpdate  # Prevent callback from being triggered if no row is selected




# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)