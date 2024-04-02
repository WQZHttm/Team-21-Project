import pandas as pd
import dash
from dash import html, dash_table, dcc
import plotly.graph_objects as go
from datetime import datetime, timedelta, date

dash.register_page(__name__, path='/', name="Day 📋")

#current date

current_date = datetime.now()


####################### LOAD DATASET #############################
df = pd.read_csv("input/data.csv")

####################### PAGE LAYOUT #############################
layout = html.Div(children=[
    html.Br(),
    html.Label(children = html.B('Select a date:  ')),
    dcc.DatePickerSingle(
        min_date_allowed=date.today(), # CHECK
        max_date_allowed=datetime(2024, 12, 31),
        date=current_date,
        style={'width':'200px', 'margin':'0 auto'}),
    html.Br(),
    html.Br(),
    html.H1(children='Manpower Today'),

])