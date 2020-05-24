from flask import Flask, render_template, redirect
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd

# Load In Data #
df = pd.read_csv('https://raw.githubusercontent.com/aLeadPencil/SimpleFlaskDashIntegration/master/Iris.csv?token=AKXMDUQVY5XI7KHWI2ZGS3K62P6HY')
column_names = df.columns.to_list()[1:-1]
available_indicators = df['Species'].unique()

print(column_names)


# Define a Function For Generating DataFrame #
def generate_table(dataframe):
    generated_table = dash_table.DataTable(
        id = 'table',
        columns = [{'name': i, 'id': i} for i in df.columns],
        page_size = 25,
        data = df.to_dict('rows'),
    )

    return generated_table


# Initialize Flask and Dash #
server = Flask(__name__)

iris_dash = dash.Dash(
    __name__,
    server = server,
    url_base_pathname = '/iris/',
    external_stylesheets = [dbc.themes.COSMO]
)


# Create Flask Routes #
@server.route('/')
def index():
    return render_template('home.html')

@server.route('/iris/')
def iris():
    return redirect('/iris/')


# Create Iris Dashboard Elements #
# About Drop Down Menu
navbar_dropdown = dbc.DropdownMenu(
    label = 'Menu',
    className = "ml-2",
    children = [
        dbc.DropdownMenuItem('LinkedIn', href = 'https://www.linkedin.com/in/kvn-chu/'),
        dbc.DropdownMenuItem('GitHub', href = 'https://github.com/aLeadPencil'),
        dbc.DropdownMenuItem('Email Me', href = 'mailto:kchu8150@gmail.com')
    ]
)

#Nav Bar
navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Home", className="ml-2")),
                ],
                align = "center",
                no_gutters = True,
            ),
            href="/",
        ),

        dbc.Button(
            'About',
            id = 'collapse-button',
            className = 'ml-auto ml-2'
        ), 

        dbc.Collapse(
            dbc.Card(
                children = [
                    dbc.CardHeader('App Description'),
                    dbc.CardBody('A simple integration of flask and dash to showcase interactive visualization using python.'),
                ],
                color = 'dark',
                inverse = True
            ),
            id = 'collapse',
        ),
    ],
    color="dark",
    dark=True,
)

scatter1_dropdown = html.Div(
    [
        dcc.Dropdown(
            id = 'xaxis-column',
            options = [{'label': i, 'value': i} for i in column_names],
            value = 'SepalLengthCm'
        ),

        dcc.Dropdown(
            id = 'yaxis-column',
            options = [{'label': i, 'value': i} for i in column_names],
            value = 'SepalWidthCm'
        ),
    ], style = {'width': '20%', 'display': 'inline-block'}
)


# Callback functions for Interactivity #
# Navbar Collapsibility Callback
@iris_dash.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Scatter Plot 1 Callback
@iris_dash.callback(
    Output('scatterplot-1', 'figure'),
    [
        Input('xaxis-column', 'value'),
        Input('yaxis-column', 'value')
    ]
)
def update_graph(xaxis_column_name, yaxis_column_name):
    traces = []
    for i in df['Species'].unique():
        df_each_species = df[df['Species'] == i]
        traces.append(
            dict(
                x = df_each_species[xaxis_column_name],
                y = df_each_species[yaxis_column_name],
                mode = 'markers',
                name = i
            )
        )

    return {
        'data': traces,

        'layout': dict(
            xaxis = {
                'title': xaxis_column_name
            },
            yaxis = {
                'title': yaxis_column_name
            }
        )
    }


# Initialize the Dash App #
iris_dash.layout = html.Div(
    children = [
        navbar,
        html.Hr(),
        scatter1_dropdown,
        dcc.Graph(id = 'scatterplot-1'),
        html.Hr(),
        generate_table(df)
    ],
    
    style = {
        'background': '#ADD8E6',
        # 'background': '#112D32',
        'padding': '50px'
    }
)

# Run App #
if __name__ == "__main__":
    server.run()