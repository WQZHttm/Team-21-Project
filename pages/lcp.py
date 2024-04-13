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
    filtered_data1 = filtered_data[filtered_data['Shift'] == '10am-4.30pm']
    filtered_data2 = filtered_data[filtered_data['Shift'] == '7pm-10pm']
    filtered_data3 = filtered_data[filtered_data['Shift'] == '8pm-10pm']

    defaultchef1 = len(filtered_data1[filtered_data1['Role'] == 'chef'])
    defaultservice1 = len(filtered_data1[(filtered_data1['Role'] == 'service') & (filtered_data1['Job_status'] == 'full-time')])
    defaultdishwasher1 = len(filtered_data1[filtered_data1['Role'] == 'dishwasher'])
    defaultpt1 = len(filtered_data1[filtered_data1['Job_status'] == 'part-time'])

    defaultchef2 = len(filtered_data2[filtered_data2['Role'] == 'chef'])
    defaultservice2 = len(filtered_data2[(filtered_data2['Role'] == 'service') & (filtered_data2['Job_status'] == 'full-time')])
    defaultdishwasher2 = len(filtered_data2[filtered_data2['Role'] == 'dishwasher'])
    defaultpt2 = len(filtered_data2[filtered_data2['Job_status'] == 'part-time'])

    defaultchef3 = len(filtered_data3[filtered_data3['Role'] == 'chef'])
    defaultservice3 = len(filtered_data3[(filtered_data3['Role'] == 'service') & (filtered_data3['Job_status'] == 'full-time')])
    defaultdishwasher3 = len(filtered_data3[filtered_data3['Role'] == 'dishwasher'])
    defaultpt3 = len(filtered_data3[filtered_data3['Job_status'] == 'part-time'])

    defaultcost = sum(filtered_data['Total Paid'])
    return defaultchef1, defaultservice1, defaultdishwasher1, defaultpt1, \
        defaultchef2, defaultservice2, defaultdishwasher2, defaultpt2, \
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, \
        defaultcost


def calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate, shift):
    filtered_data = manpower_schedule[manpower_schedule['Date'] == selecteddate]
    hours = [6.5,3,2]
    if not pd.isna(filtered_data['Public Holiday'].iloc[0]):
        selectedcost = (selectedchef * 17 * hours[shift]) + (selectedservice * 16 * hours[shift]) + (selecteddishwasher * 16 * hours[shift]) + (selectedpt * 15 * hours[shift])
    elif filtered_data['Day'].iloc[0] == 'Saturday':
        selectedcost = (selectedchef * 16 * hours[shift]) + (selectedservice * 15 * hours[shift]) + (selecteddishwasher * 15 * hours[shift]) + (selectedpt * 14 * hours[shift])
    elif filtered_data['Day'].iloc[0] == 'Sunday':
        selectedcost = (selectedchef * 16 * hours[shift]) + (selectedservice * 15 * hours[shift]) + (selecteddishwasher * 15 * hours[shift]) + (selectedpt * 14 * hours[shift])
    else:
        selectedcost = (selectedchef * 15 * hours[shift]) + (selectedservice * 14 * hours[shift]) + (selecteddishwasher * 14 * hours[shift]) + (selectedpt * 13 * hours[shift])
    return selectedcost

def calculate_total(selectedchef1, selectedservice1, selecteddishwasher1, selectedpt1,
                    selectedchef2, selectedservice2, selecteddishwasher2, selectedpt2,
                    selectedchef3, selectedservice3, selecteddishwasher3, selectedpt3,
                    selecteddate):
    selectedcost1 = calculate_selected(selectedchef1, selectedservice1, selecteddishwasher1, selectedpt1, selecteddate, 0)
    selectedcost2 = calculate_selected(selectedchef2, selectedservice2, selecteddishwasher2, selectedpt2, selecteddate, 1)
    selectedcost3 = calculate_selected(selectedchef3, selectedservice3, selecteddishwasher3, selectedpt3, selecteddate, 2)
    total = selectedcost1 + selectedcost2 + selectedcost3

    return total


layout = html.Div([
    html.Br(),
    html.Label(html.B('Select a date: ')),
    dcc.DatePickerSingle(
        id = 'date-picker',
        min_date_allowed = datetime.today(),
        max_date_allowed = datetime(2024, 12, 31),
        date = current_date,
        style = {'width' : '200px', 'margin' : '10px'}
    ),
    html.Br(),
    html.H2('Labour Cost Percentage'),
    html.Br(),
    html.Div([
        dbc.Row([
            dbc.Col([
                html.H3("Morning Shift", className='slidertitle'),
                html.Br(),
                html.H4("No. of Chefs:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-chef1', className='slider'),
                html.Br(),
                html.H4("No. of Full-Time Service Staff:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-service1', className='slider'),
                html.Br(),
                html.H4("No. of Dishwashers:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-dishwasher1', className='slider'),
                html.Br(),
                html.H4("No. of Part-Timers:"),
                dcc.Slider(0,10,1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-pt1', className='slider'),
                html.Br(),
                html.Div(id = 'selected-cost-output1', className='costtabletext')

            ], className = 'bordered-col'),
            dbc.Col([
                html.H3("Night (Chinese Buffet)", className='slidertitle'),
                html.Br(),
                html.H4("No. of Chefs:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-chef2', className='slider'),
                html.Br(),
                html.H4("No. of Full-Time Service Staff:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-service2', className='slider'),
                html.Br(),
                html.H4("No. of Dishwashers:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-dishwasher2', className='slider'),
                html.Br(),
                html.H4("No. of Part-Timers:"),
                dcc.Slider(0,10,1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-pt2', className='slider'),
                html.Br(),
                html.Div(id = 'selected-cost-output2', className='costtabletext')

            ], className = 'bordered-col'),
            dbc.Col([
                html.H3("Night (Indian Buffet)", className='slidertitle'),
                html.Br(),
                html.H4("No. of Chefs:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-chef3', className='slider'),
                html.Br(),
                html.H4("No. of Full-Time Service Staff:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-service3', className='slider'),
                html.Br(),
                html.H4("No. of Dishwashers:"),
                dcc.Slider(0, 10, 1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-dishwasher3', className='slider'),
                html.Br(),
                html.H4("No. of Part-Timers:"),
                dcc.Slider(0,10,1,
                           value=0,
                           tooltip={"placement": 'bottom', "always_visible": True},
                           id = 'slider-pt3', className='slider'),
                html.Br(),
                html.Div(id = 'selected-cost-output3', className='costtabletext')

            ], className = 'bordered-col'),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Br(),
                        html.H2("Labour Cost for the day: ", className= "costtabletitle"),
                        html.Br(),
                        html.Br(),
                        html.Div(id = 'total-cost-output', className='costtabletext'),
                        html.Br(),
                        html.Div(id = 'selected-total', className='costtabletext')
                    ])
                ], className = 'costtable',
                ),
            ], width = 6),
            dbc.Col([
                html.Div(id = 'graph')
            ], width = 5),

        ])


    ]),
])

## DEFAULTS ##
@callback(
    Output('total-cost-output', 'children'),
    Output('slider-chef1', 'value'),
    Output('slider-service1', 'value'),
    Output('slider-dishwasher1', 'value'),
    Output('slider-pt1', 'value'),
    Output('slider-chef2', 'value'),
    Output('slider-service2', 'value'),
    Output('slider-dishwasher2', 'value'),
    Output('slider-pt2', 'value'),
    Output('slider-chef3', 'value'),
    Output('slider-service3', 'value'),
    Output('slider-dishwasher3', 'value'),
    Output('slider-pt3', 'value'),
    Input('date-picker', 'date')
)

def update_defaults(selected_date):
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d')
    defaultchef1, defaultservice1, defaultdishwasher1, defaultpt1, \
        defaultchef2, defaultservice2, defaultdishwasher2, defaultpt2, \
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, total_cost = calculate_defaults(selected_date)
    return (f"Optimised Cost: ${total_cost}",
            defaultchef1, defaultservice1, defaultdishwasher1, defaultpt1,
            defaultchef2, defaultservice2, defaultdishwasher2, defaultpt2,
            defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3,
            )

## MORNING ##
@callback(
    Output('selected-cost-output1', 'children'),
    Input('slider-chef1', 'value'),
    Input('slider-service1', 'value'),
    Input('slider-dishwasher1', 'value'),
    Input('slider-pt1', 'value'),
    Input('date-picker', 'date')
)

def update_selected1(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate):
    selectedcost = calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate, 0)
    return f"Selected Labour Cost: ${selectedcost}"

## NIGHT CHINESE ##
@callback(
    Output('selected-cost-output2', 'children'),
    Input('slider-chef2', 'value'),
    Input('slider-service2', 'value'),
    Input('slider-dishwasher2', 'value'),
    Input('slider-pt2', 'value'),
    Input('date-picker', 'date')
)

def update_selected2(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate):
    selectedcost = calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate, 1)
    return f"Selected Labour Cost: ${selectedcost}"

## NIGHT INDIAN ##
@callback(
    Output('selected-cost-output3', 'children'),
    Input('slider-chef3', 'value'),
    Input('slider-service3', 'value'),
    Input('slider-dishwasher3', 'value'),
    Input('slider-pt3', 'value'),
    Input('date-picker', 'date')
)

def update_selected3(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate):
    selectedcost = calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate, 2)
    return f"Selected Labour Cost: ${selectedcost}"

## LABOUR COST ##

@callback(
    Output('selected-total', 'children'),
    Output('graph', 'children'),
    Input('slider-chef1', 'value'),
    Input('slider-service1', 'value'),
    Input('slider-dishwasher1', 'value'),
    Input('slider-pt1', 'value'),
    Input('slider-chef2', 'value'),
    Input('slider-service2', 'value'),
    Input('slider-dishwasher2', 'value'),
    Input('slider-pt2', 'value'),
    Input('slider-chef3', 'value'),
    Input('slider-service3', 'value'),
    Input('slider-dishwasher3', 'value'),
    Input('slider-pt3', 'value'),
    Input('date-picker', 'date')
)

def update_selected_total(selectedchef1, selectedservice1, selecteddishwasher1, selectedpt1,
                          selectedchef2, selectedservice2, selecteddishwasher2, selectedpt2,
                          selectedchef3, selectedservice3, selecteddishwasher3, selectedpt3,
                          selecteddate):
    selectedtotal = calculate_total(selectedchef1, selectedservice1, selecteddishwasher1, selectedpt1,
                                    selectedchef2, selectedservice2, selecteddishwasher2, selectedpt2,
                                    selectedchef3, selectedservice3, selecteddishwasher3, selectedpt3,
                                    selecteddate)
    defaultchef1, defaultservice1, defaultdishwasher1, defaultpt1, \
        defaultchef2, defaultservice2, defaultdishwasher2, defaultpt2, \
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, total_cost = calculate_defaults(selecteddate)


    graphdata = [
        go.Bar(
            x=['Optimised', 'Selected'],
            y=[total_cost, selectedtotal],
            text=[f'${total_cost}', f'${selectedtotal}'],
            marker=dict(color=['blue','green']),
        )
    ]
    graphlayout = go.Layout(
        title = dict(text='Total Labour Cost Comparison', x=0.5, y=0.95, font=dict(size=20, color='black')),
        margin=dict(l=50, r=50, t=50, b=60)
    )
    figure = go.Figure(data=graphdata, layout=graphlayout)
    graph = dcc.Graph(figure = figure)

    return f"Total Selected Labour Cost: ${selectedtotal}", graph

if __name__ == '__main__':
    app.run(debug=True)