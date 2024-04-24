from dash import Dash, html
import dash
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
from dateutil.parser import parse

####################### FLASK SERVER #############################
server = Flask(__name__)

# Database connection settings
host = 'localhost'
user = 'root'
password = 'password'
database = 'trial_schema'
port = 3306

server.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{user}:{password}@{host}:{port}/{database}'
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(server)


####################### SQL INTEGRATION #############################
# with open("docker-compose.yml", "r") as file:
#     config =yaml.safe_load(file)['services']['db']['environment']


####################### DASH APP #############################

external_css = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME,"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__,server=server, routes_pathname_prefix="/", pages_folder='pages', use_pages=True, external_stylesheets=external_css)

sidebar = html.Div([
    html.Br(),
    html.Img(src='https://eber.co/wp-content/uploads/2023/08/mount-faber-logo-768x288.png', style={'height': '70px', 'margin-right': '10px','float': 'left'}),
    html.Br(),

    html.Br(), 
    html.Br(),
    html.Div([html.Span([
                    html.I(className='bi bi-person-circle'),
                    html.Span('Hao Xiang', id='user-login',style={'margin-left': '5px'})])],
             className='sidebar-user'),
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



app.layout = html.Div([
	# html.H1(datetime.datetime.now().strftime('Last updated: %Y-%m-%d %H:%M:%S'),
	# 	style={'opacity': '1','color': 'blue', 'fontSize': 15, 'position': 'absolute', 'top': '2px', 'right': '2px'}),
    # html.Br(),
    
    # side bar
    html.Div(children=dbc.Row([dbc.Col(sidebar, width=2), dbc.Col(dash.page_container)])),
])



if __name__ == '__main__':
	app.run(debug=True)