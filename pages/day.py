import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback
import plotly.graph_objects as go
import plotly.express as px
import datetime
import numpy as np
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/', name="Day 📋")

#current date

current_date = datetime.datetime.today().date()
df = pd.read_csv("output/predictions.csv") # TO REMOVE
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')


####################### LOAD DATASET #############################
manpower_schedule = pd.read_csv('output/final_schedule.csv')
manpower_schedule ['Date_and_day'] = manpower_schedule['Date'] + ' ' + manpower_schedule['Day']
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

# customer_demand['Date'] = pd.to_datetime(customer_demand['Date'], format='%Y-%m-%d')
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d')


####################### PAGE LAYOUT #############################


layout = html.Div([
   #Day dropdown
   html.Label(children = html.B('Select a date:  ')),
    dcc.DatePickerSingle(id='date-picker',
        min_date_allowed=datetime.datetime.today(), # CHECK
        max_date_allowed=datetime.datetime(2024, 12, 31),
        date=current_date,
        style={'width':'200px', 'margin':'10px'}),
    html.Br(),
    html.Br(),
    html.H2(id='event-header'),
    
    # shift tab
    # html.Div(id="shift",children=[
    #     dbc.Button("Morning\n(10am-4.30pm)", value="morn",active='exact'),
    #     dbc.Button("Night (Chinese)\n(7pm-10pm)", value="chidata",active='exact'),
    #     dbc.Button("Night (Indian)\n(8pm-10pm)", value="inddata",active='exact'),]
    # ),
    html.Div([
    dcc.Tabs(id="shift", value="morn", children=[
        dcc.Tab(label="Morning\n(10am-4.30pm)", value="morn"),
        dcc.Tab(label="Night (Chinese)\n(7pm-10pm)", value="chidata"),
        dcc.Tab(label="Night (Indian)\n(8pm-10pm)", value="inddata"),
        ],style={"white-space": "pre"})
    ],className='shift-tab'),
    

    html.Br(),
    # day display
    html.Div(
        dbc.Row([dbc.Col(html.Div(id='employee-table'),width=6),
                 dbc.Col(html.Div(id="count-table"),width=3)]),
        className='day-display')


])

# update event of the day
@callback(Output('event-header','children'),
          Input('date-picker','date'))
def update_event(date):
    df2=df.loc[df['Date']==date]
    if not isinstance(df2['Public Holiday'].item(),str):
        return "Today's Event: NA"
    else:
        return f"Today's Event: {df2['Public Holiday'].item()}"

@callback([Output('employee-table', 'children'),Output('count-table','children')],
          [Input('date-picker','date'),Input("shift","value")])

def produce_output(date,shift):
    date_picked=date
    df=manpower_schedule.loc[manpower_schedule['Date'] == date_picked]
    if shift=="morn":
        final_df=df.loc[df['Shift']=='10am-4.30pm']
    elif shift=='chidata':
        final_df=df.loc[df['Shift']=='7pm-10pm']
    else: # indian buffet
        final_df=df.loc[df['Shift']=='8pm-10pm']
    
    print('final',final_df)
    # create a new df to group employees
    roles_df=final_df.pivot_table(index='Role', values='Employee_ID', aggfunc=lambda x: ', '.join(x)).reset_index()
    if roles_df.empty:
        return None, None
    roles_df.columns = ['Role', 'Employee_ID']
    table = dash_table.DataTable(
        id='table',
        columns=[
                    {'name': 'Role', 'id': 'Role'},
                    {'name': 'Employees working', 'id': 'Employee_ID'}
                ],
        
        data=roles_df[['Role', 'Employee_ID']].to_dict('records'),
        page_size=10,
        style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
        style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"}),


    count = dbc.Card(
        [dbc.CardBody(
                [
                    html.H4("Total no. of staff for this shift", className="card-title"),
                    html.P(len(final_df), className="card-text"),
                ]
            ),
        ],
        style={"width": "18rem"},
        class_name='card',
    )
    # # show graph of chefs
    # fig = px.histogram(final_df, x="Role")
    # fig.update_layout(
    #     title='Histogram',
    #     yaxis_title='Count',
    #     yaxis=dict(
    #         dtick=1  # Set dtick to 1 for y-axis
    #     )
    # )

    return table,count
