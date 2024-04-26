from dash import Dash, html
import dash
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc
import pandas as pd
from sqlalchemy.types import TypeDecorator, VARCHAR
from dateutil.parser import parse
from db_server import server


####################### DASH APP #############################

# styling (icons, using css to customise colours & layout)
external_css = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME,"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

# Dash app using Flask server; routes_pathname_prefix="/" means Dash app will be shown when they first open the local webpage
app = Dash(__name__,server=server, routes_pathname_prefix="/", pages_folder='pages', use_pages=True, external_stylesheets=external_css)

# sidebar layout
sidebar = html.Div([
    html.Br(),
    # logo of Mount Faber
    html.Img(src='https://eber.co/wp-content/uploads/2023/08/mount-faber-logo-768x288.png', style={'height': '70px', 'margin-right': '10px','float': 'left'}),
   
    # spacing between logo and user 
    html.Br(),
    html.Br(), 
    html.Br(),
    
    # shows user
    html.Div([html.Span([
                    html.I(className='bi bi-person-circle'),
                    html.Span('Hao Xiang', id='user-login',style={'margin-left': '5px'})])],
             className='sidebar-user'),
    
    # buttons that lead to their respective pages
    dbc.Nav(
        [
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-cloud'),
                    html.Span('Daily', style={'margin-left': '5px'})]), href='/', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-collection'),
                    html.Span('Weekly', style={'margin-left': '5px'})]), href='/week', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-card-list'),
                    html.Span('Employee Details', style={'margin-left': '5px'})]), href='/employee_details', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-percent'),
                    html.Span('Labour Cost Percentage', style={'margin-left': '5px'})]), href='/lcp', active='exact',className='sidebar-list-item'),
    
        ],
        vertical=True,
        pills=True,
    ),
], className='sidebar')


# overall layout of app
app.layout = html.Div([   
    # side bar
    html.Div(children=dbc.Row([dbc.Col(sidebar, width=2), dbc.Col(dash.page_container)])),
])

if __name__ == '__main__':
    # run Dash app
    # (host='0.0.0.0') means server accessible from any IP address on the machine, connected to port 8050
    # debug=True means no error messages will be shown to users (deployment mode)
	app.run_server(host='0.0.0.0', port=8050, debug=False)