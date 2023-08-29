import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback
import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go

dash.register_page(__name__,'/')

layout = html.Div(style={
        'backgroundColor':'white',
        'margin':'10px',

    },
    children=[
    html.H1(
        style={
            'color':'black'
        },
        children='Welcome to Portfolio Selection'
    ),
    html.Span(
        style={
            'width':'80%'
        },
        children='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
    ),

    html.H3(
        children='Please input your portfolio in a CSV / Excel file:'
    ),
    html.H5(children='**Please only include a Month and Monthly Returns columns. Thanks!',
        style={
            'fontSize':'12px',

        }
    ),
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload')
    
])



def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values(by='Date', inplace=True)
    df['Change %'] = df['Change %'].apply(lambda x: x.replace("%","")).astype(float)    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=df['Change %'],line=go.scatter.Line(color="gray")))
    
    print(fig)
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
      
        html.Hr(),  # horizontal line

        # plot the graph for the monthly returns
       
        dcc.Graph(figure=fig)
       
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]

        return children
