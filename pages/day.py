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
customer_prediction = pd.read_csv('output/predictions.csv')
customer_prediction['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
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
    html.H2(id='event-header'),
    
    # shift tab
    # html.Div(id="shift",children=[
    #     dbc.Button("Morning\n(10am-4.30pm)", value="morn",active='exact'),
    #     dbc.Button("Night (Chinese)\n(7pm-10pm)", value="chidata",active='exact'),
    #     dbc.Button("Night (Indian)\n(8pm-10pm)", value="inddata",active='exact'),]
    # ),
    html.Br(),
    html.Div([
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
        dbc.Row([dbc.Col(html.Div(id='employee-table'),width=8),
                 dbc.Col(html.Div(id="count-table")),
                 ]),
        dbc.Row([
            dbc.Col(html.Div(id= 'histogram-container', className='histogram-container'), width = 8)
                ]),

        ], className='day-display'),


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



@callback([Output('employee-table', 'children'),Output('count-table','children'), Output('histogram-container', 'children')],
          [Input('date-picker','date'),Input("shift","value")])


def produce_output(date,shift):
    df= manpower_schedule.loc[manpower_schedule['Date'] == date]
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
                    {'name': 'Employees Working', 'id': 'Employee_ID'}
                ],
        
        data=roles_df[['Role', 'Employee_ID']].to_dict('records'),
        page_size=10,
        style_cell={"background-color": "#EDF6F9", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left",'font_family':"'Outfit', sans-serif","font-size": "16px","padding": "10px"},
        style_header={"background-color": "#83C5BE", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"}),


    count = dbc.Card(
        [dbc.CardBody(
                [
                    html.H4("Total no. of staff for this shift:", className="card-title"),
                    html.P(len(final_df), className="card-text"),
                ]
            ),
        ],
        class_name='card',
    )
    df3 = customer_prediction.loc[customer_prediction['Date']== date]
    print(df3)
    x_values = df3.columns[9:].tolist()
    print(x_values)
    y_values = df3.iloc[0, 9:].values.tolist() 
    print(y_values)
    histogram_fig = px.histogram(x = x_values, y= y_values, title="Customer demand across the day",
        labels={'x': 'Time', 'y': 'Customer Count'}, histnorm = 'density')

    histogram_fig.update_layout(
    title=dict(y=0.99, x = 0.07, font=dict(size=17)), 
    margin = dict(t = 40),
    bargap = 0, 
    plot_bgcolor='rgba(0,0,0,0)', 
    paper_bgcolor='rgba(0,0,0,0)', 
    yaxis_title = 'Customer Count',
)

    histogram_fig.add_scatter(x=x_values, y=y_values, mode='lines', line=dict(shape='spline', smoothing=1.3), showlegend = False)

    histogram_container = dcc.Graph(figure=histogram_fig)


    # # show graph of chefs
    # fig = px.histogram(final_df, x="Role")
    # fig.update_layout(
    #     title='Histogram',
    #     yaxis_title='Count',
    #     yaxis=dict(
    #         dtick=1  # Set dtick to 1 for y-axis
    #     )
    # )

    return table,count, histogram_container
