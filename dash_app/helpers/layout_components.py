from dash import html, dcc # type: ignore
import dash_bootstrap_components as dbc
import dash_leaflet as dl

def build_pie_charts(fig1, fig2, fig3):
    pie_charts = [dbc.Col(
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
    )]
    
    return pie_charts

def build_line_chart(fig):
    line_chart = dbc.Col(
        html.Div(dcc.Graph(figure=fig, id="multi_projects_line_chart")), 
        width=12,
        className='line_chart',
        id='multi_projects_line_chart_col'

    )

    return line_chart


def build_map():
    the_map = dl.Map(center=[51.505, -0.09], zoom=13, children=[
        dl.TileLayer(),
        dl.Marker(position=[51.505, -0.09], children=[
            dl.Tooltip("Hello world"),
            dl.Popup([
                html.H1("Popup"),
                html.P("This is a popup.")
            ])
        ])
    ], style={'width': '100%', 'height': '50vh'})
    
    return the_map