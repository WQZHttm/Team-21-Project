import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback, State
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np
import dash_bootstrap_components as dbc



dash.register_page(__name__, path='/lcp', name="Labour Cost Percentage")


#current date

current_date = datetime.today().date()
df = pd.read_csv("output/predictions.csv") # TO REMOVE
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')

####################### LOAD DATASET #############################
manpower_schedule = pd.read_csv('output/final_schedule.csv')
manpower_schedule ['Date_and_day'] = manpower_schedule['Date'] + ' ' + manpower_schedule['Day']
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

# customer_demand['Date'] = pd.to_datetime(customer_demand['Date'], format='%Y-%m-%d')
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d')

manpower_schedule['Total Paid'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']


def calculate_defaults(selected_date):
    filtered_data = manpower_schedule[manpower_schedule['Date'] == selected_date]
    defaultchef = len(filtered_data[filtered_data['Role'] == 'chef'])
    defaultservice = len(filtered_data[(filtered_data['Role'] == 'service') & (filtered_data['Job_status'] == 'full-time')])
    defaultdishwasher = len(filtered_data[filtered_data['Role'] == 'dishwasher'])
    defaultpt = len(filtered_data[filtered_data['Job_status'] == 'part-time'])
    defaultcost = sum(filtered_data['Total Paid'])
    return defaultchef, defaultservice, defaultdishwasher, defaultpt, defaultcost


def calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate):
    filtered_data = manpower_schedule[manpower_schedule['Date'] == selecteddate]
    if not pd.isna(filtered_data['Public Holiday'].iloc[0]):
        selectedcost = (selectedchef * 17 * 4) + (selectedservice * 16 * 5.5) + (selecteddishwasher * 16 * 4) + (selectedpt * 15 * 5)
    elif filtered_data['Day'].iloc[0] == 'Saturday':
        selectedcost = (selectedchef * 16 * 4) + (selectedservice * 15 * 5.5) + (selecteddishwasher * 15 * 4) + (selectedpt * 14 * 5)
    elif filtered_data['Day'].iloc[0] == 'Sunday':
        selectedcost = (selectedchef * 16 * 4) + (selectedservice * 15 * 5.5) + (selecteddishwasher * 15 * 4) + (selectedpt * 14 * 5)
    else:
        selectedcost = (selectedchef * 15 * 4) + (selectedservice * 14 * 5.5) + (selecteddishwasher * 14 * 4) + (selectedpt * 13 * 5)
    return selectedcost


layout = html.Div([
    html.Label(html.B('Select a date: ')),
    dcc.DatePickerSingle(
        id = 'date-picker',
        min_date_allowed = datetime.today(),
        max_date_allowed = datetime(2024, 12, 31),
        date = current_date,
        style = {'width' : '200px', 'margin' : '10px'}
    ),
    html.Br(),
    html.H1('Labour Cost Percentage'),
    html.Br(),
    html.Br(),
    html.Div(
        dbc.Row([
            dbc.Col([
                html.H4("No. of Chefs:"),
                dcc.Slider(0, 20, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-chef', className='slider'),
                html.Div(id= 'slider-chef-output', className='sliderdefault'),
                html.Br(),
                html.H4("No. of Full-Time Service Staff:"),
                dcc.Slider(0, 20, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-service', className='slider'),
                html.Div(id= 'slider-service-output', className='sliderdefault'),
                html.Br(),
                html.H4("No. of Dishwashers:"),
                dcc.Slider(0, 20, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-dishwasher', className='slider'),
                html.Div(id= 'slider-dishwasher-output', className='sliderdefault'),
                html.Br(),
                html.H4("No. of Part-Timers:"),
                dcc.Slider(0,20,1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-pt', className='slider'),
                html.Div(id= 'slider-pt-output', className='sliderdefault'),

            ], className = 'bordered-col'),
            dbc.Col(
                dbc.Card([
                    dbc.CardBody([
                        html.H2("Labour Cost for the day: ", className= "costtabletitle"),
                        html.Br(),
                        html.Div(id = 'total-cost-output', className='costtabletext'),
                        html.Div(id = 'selected-cost-output', className='costtabletext'),
                        html.Br(),
                        html.Div(id = 'cost-diff', className='costtabletext')
                    ])
                ], className = 'costtable',
                ), className = 'bordered-col'
            ),
        ])
    ),
])

@callback(
    Output('slider-chef-output', 'children'),
    Output('slider-service-output', 'children'),
    Output('slider-dishwasher-output', 'children'),
    Output('slider-pt-output', 'children'),
    Output('total-cost-output', 'children'),
    Output('slider-chef', 'value'),
    Output('slider-service', 'value'),
    Output('slider-dishwasher', 'value'),
    Output('slider-pt', 'value'),
    Input('date-picker', 'date'),


)
def update_defaults(selected_date):
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
    defaultchef, defaultservice, defaultdishwasher, defaultpt, total_cost = calculate_defaults(selected_date)
    return (f'Default = {defaultchef}', \
            f'Default = {defaultservice}', \
            f'Default = {defaultdishwasher}', \
            f'Default = {defaultpt}', \
            f"Default Cost: ${total_cost}",
            defaultchef,
            defaultservice,
            defaultdishwasher,
            defaultpt
            )

@callback(
    Output('selected-cost-output', 'children'),
    Output('cost-diff', 'children'),
    Input('slider-chef', 'value'),
    Input('slider-service', 'value'),
    Input('slider-dishwasher', 'value'),
    Input('slider-pt', 'value'),
    Input('date-picker', 'date')
)
def update_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate):
    selectedcost = calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate)
    defaultchef, defaultservice, defaultdishwasher, defaultpt, total_cost = calculate_defaults(selecteddate)
    costdiff = selectedcost - total_cost
    sign = "-" if costdiff < 0 else ""
    return (f"Selected Cost: ~${selectedcost} (Estimate)",
            f'Change in Labour Cost: {sign}${abs(costdiff)}'
            )


if __name__ == '__main__':
    app.run(debug=True)