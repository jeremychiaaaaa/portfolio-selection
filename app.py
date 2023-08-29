import dash
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import dash_core_components as dcc
import dash_html_components as html
import base64
import datetime
import io

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True, suppress_callback_exceptions=True )
app.layout = html.Div(
    dash.page_container
)




if __name__ == '__main__':
    app.run(debug=True)