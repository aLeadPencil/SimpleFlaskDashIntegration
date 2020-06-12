from flask import Flask, render_template, redirect
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_table
from dash.dependencies import Input, Output, State
import pickle
import pandas as pd
import numpy as np



# Load In Data #
df = pd.read_csv('https://raw.githubusercontent.com/aLeadPencil/SimpleFlaskDashIntegration/master/Iris.csv?token=AKXMDUQVY5XI7KHWI2ZGS3K62P6HY')
model = pickle.load(open('logistic_regression_model.pkl', 'rb'))
column_names = df.columns.to_list()[1:-1]



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

iris_classification = dash.Dash(
    __name__,
    server = server,
    url_base_pathname = '/classification/',
    external_stylesheets = [dbc.themes.COSMO]
)



# Create Flask Routes #
@server.route('/')
def index():
    return render_template('home.html')

@server.route('/iris/')
def iris():
    return redirect('/iris/')

@server.route('/classification/')
def classification():
    return redirect('/classification/')



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

        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand('Data Visualization', className = 'ml-2'))
                ],
                align = 'center',
                no_gutters = True
            ),
            href = '/iris/'
        ),

        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand('Classification', className = 'ml-2'))
                ],
                align = 'center',
                no_gutters = True
            ),
            href = '/classification'
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
    ], 
    style = {'width': '20%', 'display': 'inline-block'}
)

classification_jumbotron = dbc.Jumbotron(
    [
        html.H2('This page is used to showcase prediction of the data according to values inputted by the user.'),
        html.P('Since this demo is created for the sake of demonstrating a simple example, only logistic regression will be used to classify the data.'),
        html.P('Adjust the sliders and the predictions will update in real time.')
    ]
)

data_sliders = html.Div(
    [
        html.Label('Sepal Length (CM)'),
        dcc.Slider(
            id = 'sepal_length_slider',
            min = 4,
            max = 8,
            value = 6,
            step = 0.01,
            marks = {
                4: '4',
                5: '5',
                6: '6',
                7: '7',
                8: '8'
            },
            updatemode = 'drag'
        ),

        dcc.Slider(
            id = 'sepal_width_slider',
            min = 2,
            max = 4.5,
            value = 3.25,
            step = 0.01,
            marks = {
                2: '2',
                2.625: '2.625',
                3.25: '3.25',
                3.875: '3.875',
                4.5: '4.5'
            },
            updatemode = 'drag'
        ),

        dcc.Slider(
            id = 'petal_length_slider',
            min = 1,
            max = 7,
            value = 4,
            step = 0.01,
            marks = {
                1: '1',
                2.5: '2.5',
                4: '4',
                5.5: '5.5',
                7: '7'
            },
            updatemode = 'drag'
        ),

        dcc.Slider(
            id = 'petal_width_slider',
            min = 0,
            max = 2.5,
            value = 1.25,
            step = 0.01,
            marks = {
                0: '0',
                0.625: '0.625',
                1.25: '1.25',
                1.875: '1.875',
                2.5: '2.5'
            },
            updatemode = 'drag'
        ),
    ],
)

# Callback functions for Interactivity #
# Navbar Collapsibility Callback
@iris_dash.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse_visualization(n, is_open):
    if n:
        return not is_open
    return is_open

@iris_classification.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse_classification(n, is_open):
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
            },
            hovermode = 'closest',
            title = 'Scatterplot of Iris Data'
        )
    }

# Slider Callback For Classification
@iris_classification.callback(
    Output('data-info', 'children'),
    [
        Input('sepal_length_slider', 'value'),
        Input('sepal_width_slider', 'value'),
        Input('petal_length_slider', 'value'),
        Input('petal_width_slider', 'value')
    ]
)
def update_jumbotron(sepal_length, sepal_width, petal_length, petal_width):
    data_values = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, 4)
    prediction = model.predict(data_values)[0]

    message1 = html.P('Sepal Length: {}'.format(sepal_length))
    message2 = html.P('Sepal Width: {}'.format(sepal_width))
    message3 = html.P('Petal Length: {}'.format(petal_length))
    message4 = html.P('Petal Width: {}'.format(petal_width))
    prediction_message = html.H2('Based on the values selected, the species is determined to be {}'.format(prediction))

    return message1, message2, message3, message4, prediction_message



# Initialize the Dash Apps #
# Initialize App 1 For Data Visualization
iris_dash.layout = html.Div(
    children = [
        navbar,
        html.Hr(),
        scatter1_dropdown,
        dcc.Graph(id = 'scatterplot-1'),
        html.Hr(),
        html.H1('Table of Iris Data', style = {'textAlign': 'center'}),
        generate_table(df)
    ],
    
    style = {
        'background': '#ADD8E6',
        'padding': '50px'
    }
)

# Initialize App 2 For Classification
iris_classification.layout = html.Div(
    children = [
        navbar,
        html.Hr(),
        html.H1('Classification Based On Data', style = {'textAlign': 'center'}),
        html.Br(),
        classification_jumbotron,
        data_sliders,
        html.Hr(),
        dbc.Jumbotron(id = 'data-info'),
    ],

    style = {
        'background': '#ADD8E6',
        'padding': '50px'
    }
)



# Run App #
if __name__ == "__main__":
    server.run(debug = True)