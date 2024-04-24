import pandas as pd
import dash
from dash import html, dcc,Input, Output,callback
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
import dash_bootstrap_components as dbc
from shared_data import customer_prediction, manpower_schedule

dash.register_page(__name__, path='/lcp', name="Labour Cost Percentage")


current_date = datetime.today().date()

####################### LOAD DATASET #############################
customer_prediction=customer_prediction
manpower_schedule=manpower_schedule



##Baseline##
# A = ["A1", "A2", "A3", "A4", "A5"] #Chefs
# B = ["B1", "B2", "B3", "B4", "B5"] #FT
# C = ["C1", "C2"] #DW
# D = ["D1", "D2", "D3"] #PT

# Cycle Order for services and part time: B1 D1 D3 D2 B3 B4 B2 B5
## Mon = [[A1, A2, A3, A4, B3, C1, D2, D3], [A3, A4, B2, B4, B5, C1], [A2, B3, C2, D2, D3]]     A5, B1, C2, D1 on off
Mon = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 3, 3, 3, 2]), sum([6.5, 3, 2]), sum([6.5, 6.5, 2, 2])]

## Tue = [[A1, A2, A3, A5, B3, B4, C2, D2], [A2, A3, B1, B2, B5, C2, D1], [A1, B3, B4, C1, D2]]     A5, B1, C2, D1 on off
Tue = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 6.5, 3, 3, 3, 2, 2]), sum([6.5, 3, 2]), sum([6.5, 3, 2])]

## Wed = [[A1, A2, A4, A5, B2, B3, B4, C1], [A1, A2, B1, B5, C2, D1, D3], [A5, B2, B3, B4, C1]]     A3, D2 on off
Wed = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 6.5, 6.5, 3, 3, 2, 2, 2]), sum([6.5, 3, 2]), sum([3, 3])]

## Thur = [[A1, A3, A4, A5, B2, B4, B5, C2], [A1, A5, B1, C1, D1, D2, D3], [A4, B2, B4, B5, C2]]    A2, B3 on off
Thur = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 6.5, 6.5, 3, 2, 2, 2]), sum([6.5, 3, 2]), sum([3, 3, 3])]

## Fri = [[A2, A3, A4, A5, B1, B2, B5, C1], [A4, A5, B3, C2, D1, D2, D3], [A3, B1, B2, B5, C1]]     A1, B4 on off
Fri = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 6.5, 6.5, 3, 2, 2, 2]), sum([6.5, 3, 2]), sum([3, 3, 3])]

## Sat = [[A1, A2, A3, A4, B1, B5, C2, D1], [A4, A5, B3, B4, C1, D2, D3],[A3, B1, B5, C2, D1]]      B2 on off
Sat = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 6.5, 3, 3, 2, 2]), sum([6.5, 3, 2]), sum([6.5, 3, 3, 2])]

## Sun = [[A1, A2, A4, A5, B1, C1, D1, D3], [A1, A2, B2, B3, B4, C2, D2], [A3, B1, C1, D1, D3]]     B5 on off
Sun = [sum([6.5, 6.5, 6.5, 6.5, 3, 3, 2]), sum([6.5, 3, 3, 3, 2]), sum([6.5, 3, 2]), sum([6.5, 6.5, 3, 2, 2])]
Week = [Mon, Tue, Wed, Thur, Fri, Sat, Sun]


def calculate_defaults(selected_date):
    filtered_data = manpower_schedule[manpower_schedule['Date'] == selected_date]
    filtered_data1 = filtered_data[filtered_data['Shift'] == '10am-4.30pm']
    filtered_data2 = filtered_data[filtered_data['Shift'] == '7pm-10pm']
    filtered_data3 = filtered_data[filtered_data['Shift'] == '8pm-10pm']
    day = filtered_data['Day'].iloc[0]

    defaultchef1 = len(filtered_data1[filtered_data1['Role'] == 'Chef'])
    defaultservice1 = len(filtered_data1[(filtered_data1['Role'] == 'Service') & (filtered_data1['Job_status'] == 'full-time')])
    defaultdishwasher1 = len(filtered_data1[filtered_data1['Role'] == 'Dishwasher'])
    defaultpt1 = len(filtered_data1[filtered_data1['Job_status'] == 'part-time'])

    defaultchef2 = len(filtered_data2[filtered_data2['Role'] == 'Chef'])
    defaultservice2 = len(filtered_data2[(filtered_data2['Role'] == 'Service') & (filtered_data2['Job_status'] == 'full-time')])
    defaultdishwasher2 = len(filtered_data2[filtered_data2['Role'] == 'Dishwasher'])
    defaultpt2 = len(filtered_data2[filtered_data2['Job_status'] == 'part-time'])

    defaultchef3 = len(filtered_data3[filtered_data3['Role'] == 'Chef'])
    defaultservice3 = len(filtered_data3[(filtered_data3['Role'] == 'Service') & (filtered_data3['Job_status'] == 'full-time')])
    defaultdishwasher3 = len(filtered_data3[filtered_data3['Role'] == 'Dishwasher'])
    defaultpt3 = len(filtered_data3[filtered_data3['Job_status'] == 'part-time'])

    w = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in range(len(Week)):
        if w[i] == day:
            hours = Week[i]
            if not pd.isna(filtered_data['Public_Holiday'].iloc[0]):
                baselinecost = (hours[0] * 17) + (hours[1] * 16) + (hours[2] * 16) + (hours[3] * 15)
            elif filtered_data['Day'].iloc[0] == 'Saturday':
                baselinecost = (hours[0] * 16) + (hours[1] * 15) + (hours[2] * 15) + (hours[3] * 14)
            elif filtered_data['Day'].iloc[0] == 'Sunday':
                baselinecost = (hours[0] * 16) + (hours[1] * 15) + (hours[2] * 15) + (hours[3] * 14)
            else:
                baselinecost = (hours[0] * 15) + (hours[1] * 14) + (hours[2] * 14) + (hours[3] * 13)


    defaultcost = sum(filtered_data['Total Paid'])
    return defaultchef1, defaultservice1, defaultdishwasher1, defaultpt1, \
        defaultchef2, defaultservice2, defaultdishwasher2, defaultpt2, \
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, \
        defaultcost, baselinecost


def calculate_selected(selectedchef, selectedservice, selecteddishwasher, selectedpt, selecteddate, shift):
    filtered_data = manpower_schedule[manpower_schedule['Date'] == selecteddate]
    hours = [6.5,3,2]
    if not pd.isna(filtered_data['Public_Holiday'].iloc[0]):
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
    html.Span([html.I(className='bi bi-calendar4-event'),
                        html.B('Select a date: ', style={'margin-left': '5px'})]),    dcc.DatePickerSingle(
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
                dbc.Card([
                    html.H5("Morning Shift", className='slidertitle'),
                    html.Br(),
                    html.H6("No. of Chefs:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-chef1', className='slider'),
                    html.Br(),
                    html.H6("No. of Full-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-service1', className='slider'),
                    html.Br(),
                    html.H6("No. of Part-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0,10,1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-pt1', className='slider'),
                    html.Br(),
                    html.H6("No. of Dishwashers:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-dishwasher1', className='slider'),
                    html.Br(),
                    html.Div(id = 'selected-cost-output1', className='costtabletext')
                ], className = 'lcp-card')
            ], width = 4),
            dbc.Col([
                dbc.Card([
                    html.H5("Night (Chinese Buffet)", className='slidertitle'),
                    html.Br(),
                    html.H6("No. of Chefs:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-chef2', className='slider'),
                    html.Br(),
                    html.H6("No. of Full-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-service2', className='slider'),
                    html.Br(),
                    html.H6("No. of Part-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0,10,1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-pt2', className='slider'),
                    html.Br(),
                    html.H6("No. of Dishwashers:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-dishwasher2', className='slider'),
                    html.Br(),
                    html.Div(id = 'selected-cost-output2', className='costtabletext')
                ], className = 'lcp-card')
            ], width = 4),
            dbc.Col([
                dbc.Card([
                    html.H5("Night (Indian Buffet)", className='slidertitle'),
                    html.Br(),
                    html.H6("No. of Chefs:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-chef3', className='slider'),
                    html.Br(),
                    html.H6("No. of Full-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-service3', className='slider'),
                    html.Br(),
                    html.H6("No. of Part-Time Service Staff:", className='slidertext'),
                    dcc.Slider(0,10,1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-pt3', className='slider'),
                    html.Br(),
                    html.H6("No. of Dishwashers:", className='slidertext'),
                    dcc.Slider(0, 10, 1,
                               value=0,
                               tooltip={"placement": 'bottom', "always_visible": True},
                               id = 'slider-dishwasher3', className='slider'),
                    html.Br(),
                    html.Div(id = 'selected-cost-output3', className='costtabletext')
                ], className = 'lcp-card')
            ], width = 4),
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col([
                html.Br(),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Labour Cost for the day: ", className= "slidertitle"),
                        html.Div(id = 'baseline-cost', className='costtabletext'),
                        html.H6("(Manual Scheduling without Optimisation)", style= {"font-weight": "250"}),
                        html.Div(id = 'total-cost-output', className='costtabletext'),
                        html.H6("(Suggested Scheduling using Optimisation)", style= {"font-weight": "250"}),
                        html.Div(id = 'selected-total', className='costtabletext'),
                        html.H6("(Custom Scheduling based on selected sliders)", style= {"font-weight": "250"}),
                    ])
                ], className = 'costtable',
                ),
            ], width = 4),
            dbc.Col([
                html.Div(id = 'graph',className='lcp-chart')
            ]),

        ], style={'position':'relative'})


    ]),
])

## DEFAULTS ##
@callback(
    Output('total-cost-output', 'children'),
    Output('baseline-cost', 'children'),
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
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, total_cost, baselinecost = calculate_defaults(selected_date)
    return (f"Optimised Cost: ${total_cost}",
            f"Baseline Cost: ${baselinecost}",
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
        defaultchef3, defaultservice3, defaultdishwasher3, defaultpt3, total_cost, baselinecost = calculate_defaults(selecteddate)



    graphdata = [
        go.Bar(
            y=['Selected', 'Optimised', 'Baseline'],
            x=[selectedtotal,total_cost, baselinecost],
            text=[f'${selectedtotal}', f'${total_cost}', f'${baselinecost}'],
            marker=dict(color=['#fda64a','#93c47d','#93d1e0']),
            orientation='h'
        )
    ]
    graphlayout = go.Layout(
        title = dict(text='Total Labour Cost Comparison', x=0.5, y=0.95, font=dict(size=16, color='black')),
        margin=dict(l=50, r=50, t=40, b=60),
        width= 800,
        height = 380
        
    )
    
    
    # px.bar
    
    
    figure = go.Figure(data=graphdata, layout=graphlayout)
    graph = dcc.Graph(figure = figure)

    return f"Selected Labour Cost: ${selectedtotal}",  graph
