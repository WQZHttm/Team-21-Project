import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback
import plotly.graph_objects as go
import plotly.express as px
import datetime
import numpy as np
import dash_bootstrap_components as dbc
from shared_data import customer_prediction, manpower_schedule
# from main import fetch_data


dash.register_page(__name__, path='/', name="Day 📋")

current_date = datetime.datetime.today().date()
####################### LOAD DATASET #############################
customer_prediction=customer_prediction
manpower_schedule=manpower_schedule

####################### PAGE LAYOUT #############################

layout = html.Div([
    html.Br(),
    #Day dropdown
    
    html.Span([html.I(className='bi bi-calendar4-event'),
                        html.B('Select a date: ', style={'margin-left': '5px'})]),

    # pick date
    dcc.DatePickerSingle(id='date-picker',
        min_date_allowed=datetime.datetime(2024, 1, 1),
        max_date_allowed=datetime.datetime(2024, 12, 31),
        date=current_date,
        style={'width':'200px', 'margin':'10px'}),
    html.Br(),
    # Header for Event of the Day
    html.H2(id='event-header'),
    html.Br(),
    html.Div([
    # tabs for each shift
    dcc.Tabs(id="shift", value="morn", children=[
        
        dcc.Tab(label=" Morning\n(10am-4.30pm)", value="morn",className="bi bi-sun"),
        dcc.Tab(label=" Night (Chinese)\n(7pm-10pm)", value="chidata", className='bi bi-moon'),
        dcc.Tab(label=" Night (Indian)\n(8pm-10pm)", value="inddata",className='bi bi-moon-stars'),
        ],style={"white-space": "pre"})
    ],className='shift-tab'),
    

    html.Br(),
    html.Br(),
    # day display
    html.Div([
        # Top of page
        dbc.Row([
            # table for employee schedule for the shift
            dbc.Col(html.Div(id='employee-table'), width=8),
            # table for total count of employees for the shift
            dbc.Col(html.Div(id="count-table")),
            ], className='day-middle-row'),
        # Bottom of page
        dbc.Row([
            # graph for predicted customer count throughout the day
            dbc.Col(html.Div(id= 'histogram-container', className='histogram-container'),width='auto')
                ]),
        ], className='day-display'),
])

# update event of the day
@callback(Output('event-header', 'children'),
          Input('date-picker', 'date'))
def update_event(date):
    df2=customer_prediction.loc[customer_prediction['Date']==date]
    # Update event of the day based on date selected
    if not isinstance(df2['Public_Holiday'].item(),str):
        return "Event of the Day: NA"
    else:
        return f"Event of the Day: {df2['Public_Holiday'].item()}"

# Updating all tables and graphs
@callback([Output('employee-table', 'children'),Output('count-table','children'), Output('histogram-container', 'children')],
          [Input('date-picker','date'),Input("shift","value")])


def produce_output(date,shift):
    # filtering data for date and shift selected
    df= manpower_schedule.loc[manpower_schedule['Date'] == date]
    if shift=="morn":
        final_df=df.loc[df['Shift']=='10am-4.30pm']
    elif shift=='chidata':
        final_df=df.loc[df['Shift']=='7pm-10pm']
    else: # indian buffet
        final_df=df.loc[df['Shift']=='8pm-10pm']

    # create a new df to group employees
    roles_df=final_df.pivot_table(index='Role', values='Employee_ID', aggfunc=lambda x: ', '.join(x)).reset_index()
    # Accounting for when there is no indian buffet
    if roles_df.empty:
        return None, None,html.H4('No Indian Buffet Today')
    roles_df.columns = ['Role', 'Employee_ID']
    # Table for displaying employee schedule for the shift selected
    table = dash_table.DataTable(
        id='table',
        columns=[
                    {'name': 'Role', 'id': 'Role'},
                    {'name': 'Employees Working', 'id': 'Employee_ID'}
                ],

        data=roles_df[['Role', 'Employee_ID']].to_dict('records'),
        page_size=10,
        style_data_conditional=[{
            'if':{'column_id': 'Role','filter_query': '{Role} eq "chef"'},
            'text':'Chef',
        }],
        # styling elements of the table
        style_cell={"background-color": "#fce5cd", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left",'font_family':"'Outfit', sans-serif","font-size": "16px","padding": "10px"},
        style_header={"background-color": "#fda64a", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"}),

    # Card for displaying staff count for shift selected
    count = dbc.Card(
        [dbc.CardBody(
                [
                    html.H4(f"Total number of staff for this shift:", className="card-title"),
                    html.P(len(final_df), className="card-text"),
                ]
            ),
        ],
        class_name='standard-card',
    )
    # filtering data for predicted customer count across the date selected
    df3 = customer_prediction.loc[customer_prediction['Date']== date]
    x_values = df3.columns[9:].tolist()
    y_values = df3.iloc[0, 9:].values.tolist()

    # Histogram for predicted customer count based on filtered data
    histogram_fig = px.histogram(x = x_values, y= y_values, title=f"Predicted Customer Demand on {date}",
        labels={'x': 'Time', 'y': 'Customer Count'}, histnorm = 'density')
    # Histogram styling
    histogram_fig.update_layout(
    title=dict(y=0.99, x = 0.07, font=dict(size=17)), 
    margin = dict(t = 40),
    bargap = 0, 
    plot_bgcolor='#F4F4F4', 
    paper_bgcolor='#F4F4F4', 
    yaxis_title = 'Customer Count',
)
    # Adding line graph to histogram
    histogram_fig.add_scatter(x=x_values, y=y_values, mode='lines', line=dict(shape='spline', smoothing=1.3), showlegend = False, line_color = 'black')
    # change colour of histogram
    histogram_fig.update_traces(marker_color='#b6d7a8')
    # line to indicate whether restaurant is busy
    histogram_fig.add_hline(y=50,line_color='orange',annotation_text='Busy',annotation_position="right")
    histogram_container = dcc.Graph(figure=histogram_fig)

    return table,count, histogram_container