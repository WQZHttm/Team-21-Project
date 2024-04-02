import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback
import plotly.graph_objects as go
import plotly.express as px
from dash import dash_table 
from datetime import datetime, timedelta, date

dash.register_page(__name__, path='/week', name="Week 📋")

####################### LOAD DATASET #############################
df = pd.read_csv("output/predictions.csv")
df ['Date_and_day'] = df['Date'] + ' ' + df['Day']
print(df.columns)
print((df['Date']))
df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
df['Public Holiday'] = df['Public Holiday'].fillna('')

# customer_demand = pd.read_csv('Customer_demand.csv')
manpower_schedule = pd.read_csv('output/final_schedule.csv')

#setting the date
current_date = datetime.now()
start_of_current_week = current_date - timedelta(days=current_date.weekday())
end_of_current_week = start_of_current_week + timedelta(days=6)
start_date_default = start_of_current_week.date()
end_date_default = end_of_current_week.date()


#unique identifier for the days
manpower_schedule ['Date_and_day'] = manpower_schedule['Date'] + ' ' + manpower_schedule['Day']
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

# customer_demand['Date'] = pd.to_datetime(customer_demand['Date'], format='%Y-%m-%d')
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d')


#group by 'Date_and_day' and sum the cost 
cost_group = manpower_schedule.groupby('Date_and_day')['Cost'].sum().reset_index()
#cost of hiring bar graph 
cost_hiring_fig = px.bar(data_frame = cost_group, 
	x = 'Date_and_day',
	y = 'Cost', 
	labels = {'Date_and_day': 'Days of the Week', 'Cost' : 'Cost($)'} , 
	title = 'Cost of hiring' ,
	)


#group by day and type of staffs, then counting 
staff_counts = manpower_schedule.groupby(['Date_and_day', 'Role']).size().unstack(fill_value=0).reset_index()
#staff present for the week graph
staff_present_fig = px.bar(data_frame = staff_counts,  
	x = 'Date_and_day',
	y = ['chef', 'dishwasher', 'service'],
	barmode = 'group',
	labels = {'Date_and_day': 'Days of the Week', 'value' : 'Number of Staffs'} , 
	title = 'Number of Staffs Present for Each Day' )

#logo link 
logo_link = 'https://www.mountfaberleisure.com/wp-content/uploads/2023/08/logo.png'


####################### PAGE LAYOUT #############################


layout = html.Div(children=[
    html.Br(),
    html.Div([
        html.Label( children = html.B('Select a date range: ')),
        dcc.DatePickerRange(
            id='date-picker-range',
            min_date_allowed=datetime(2024, 1, 1), # TO CHANGE
            max_date_allowed=datetime(2024, 12, 31), 
            start_date=start_date_default,
            end_date=end_date_default,
            display_format='YYYY-MM-DD',
        ),
        html.Div(id='output-container-date-picker-range'),
    ]),
    html.Br(),
    html.H1(children='Overview for the Week'),
    html.Div(children =[
        dcc.Graph(id='staff-present-fig',style= {'border':'2px solid black', 'display':'inline-block', 'width':'45%',  'margin':'5px', 'margin-right': '5%'}),
        dcc.Graph(id='cost-hiring-fig', style = {'border':'2px solid black', 'display':'inline-block' , 'width':'45%',  'margin':'5px'}),
        ], style={'background-color':'rgb(224, 255, 252)'}),
    html.Br(),
    html.Div(id='output-table'),

    ], className='row')    

@callback(
    Output('date-picker-range', 'end_date'),
    [Input('date-picker-range', 'start_date')]
)
def update_end_date(start_date):
    if start_date is not None:
        start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d').date()
        end_date = start_date + timedelta(days=6)
        return end_date.strftime('%Y-%m-%d')


# Define callback to update other graphs
@callback(
    [Output('staff-present-fig', 'figure'),
     Output('output-table', 'children'),
     Output('cost-hiring-fig', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')])

def update_graphs(start_date, end_date):
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        # Filter data based on selected date range
        mask = (manpower_schedule['Date'] >= start_date) & (manpower_schedule['Date'] <= end_date)
        filtered_data = manpower_schedule.loc[mask]
        df2 = df.loc[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

        # Recalculate cost_group and staff_counts based on filtered_data
        cost_group = filtered_data.groupby('Date_and_day')['Cost'].sum().reset_index()
        staff_counts = filtered_data.groupby(['Date_and_day', 'Role']).size().unstack(fill_value=0).reset_index()
        
        # Update figures with filtered data
        staff_present_fig = px.bar(data_frame=staff_counts,  
                                   x='Date_and_day',
                                   y=['chef', 'dishwasher', 'service'],
                                   barmode='group',
                                   labels={'Date_and_day': 'Days of the Week', 'value': 'Number of Staffs'}, 
                                   title='Number of Staffs Present for Each Day')
        print(df2)
        table = dash_table.DataTable(
            id='table',
            columns=[
                        {'name': 'Date', 'id': 'Date_and_day'},
                        {'name': 'Public Holiday', 'id': 'Public Holiday'}
                    ],
            data=df2[['Date_and_day', 'Public Holiday']].to_dict('records'),
            page_size=10,
            style_cell={"background-color": "lightgrey", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left"},
            style_header={"background-color": "dodgerblue", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"}),
        
        cost_hiring_fig = px.bar(data_frame=cost_group, 
                                  x='Date_and_day',
                                  y='Cost', 
                                  labels = {'Date_and_day': 'Days of the Week', 'Cost' : 'Cost($)'} ,
                                  title ='Cost of hiring')
        
        return staff_present_fig, table, cost_hiring_fig
    else:
        return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}
    

