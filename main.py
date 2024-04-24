from dash import Dash, html, dcc,Input, Output,callback
import dash
from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.types import TypeDecorator, VARCHAR
from dateutil.parser import parse
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc
import pandas as pd

# import mysql.connector
# import yaml

####################### FLASK SQL #############################

# server = Flask(__name__)


# @server.route("/flask")
# def home():
#     return "Flask Database"
# server.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://your_db_user:your_db_password@db/your_db_name'
# server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# db = SQLAlchemy(server)


# class CustomDate(TypeDecorator):
#     impl = VARCHAR

#     def process_bind_param(self, value, dialect):
#         if isinstance(value, str):
#             # Assuming input string is in format 'dd/mm/yyyy'
#             return value
#         elif isinstance(value, datetime):
#             return value.strftime('%d/%m/%Y')
#         else:
#             raise ValueError('Invalid input format for date')

#     def process_result_value(self, value, dialect):
#         if value is not None:
#             return parse(value).date()
#         return value


# class Schedule(db.Model):
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     Date=db.Column(CustomDate,nullable=False)
#     Day=db.Column(db.String(20),nullable=False)
#     Public_Holiday=db.Column(db.String(120))
#     Employee_ID=db.Column(db.String(5),nullable=False)
#     Shift=db.Column(db.String(120),nullable=False)
#     Role=db.Column(db.String(120))
#     Hours_worked=db.Column(db.Integer)
#     Hourly_rate=db.Column(db.Integer)
#     Job_status=db.Column(db.String(120))
#     # posts=db.relationship('Post',backref='author',lazy=True) #UPDATE NULLABLE

#     # MAY NOT NEED
#     def __repr__(self) -> str:
#         return f"<Schedule(id='{self.id}', Date='{self.Date}', Day='{self.Day}', Public_Holiday='{self.Public_Holiday}', Employee_ID='{self.Employee_ID}', Shift='{self.Shift}', Role='{self.Role}', Hours_worked='{self.Hours_worked}', Hourly_rate='{self.Hourly_rate}', Job_status='{self.Job_status}')>"


# import csv
# # db.drop_all() # drop tables
# db.create_all()
# with open("final.csv") as f:
#     reader = csv.reader(f)
#     header = next(reader)
#     for i in reader:
#         kwargs = {column: value for column, value in zip(header, i)}
#         new_entry = Schedule(**kwargs)
#         db.session.add(new_entry)
#         db.session.commit()

####################### DASH APP #############################

external_css = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,dbc.icons.FONT_AWESOME,"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css,routes_pathname_prefix="/")
# auth=dash_auth.BasicAuth(app,USER_PASS_MAPPING)

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

# TO UPDATE WHEN APP HAS AUTHENTICATION
# @app.callback(
# 	Output('user-login','children'),
# 	Input()
# )


if __name__ == '__main__':
    # with server.app_context():
    #     db.create_all()
    #     schedule=Schedule()
    #     db.session.add(schedule)
    #     db.session.commit()
    #     print(Schedule.query.all())
	app.run(debug=True)