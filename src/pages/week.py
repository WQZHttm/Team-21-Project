import pandas as pd
import dash
from dash import html,dcc,Input, Output,callback
import plotly.express as px
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from shared_data import manpower_schedule,customer_prediction


dash.register_page(__name__, path='/week', name="Week 📋")

####################### LOAD DATASET #############################
df=customer_prediction
manpower_schedule=manpower_schedule
#setting the date
current_date = datetime.now()
start_of_current_week = current_date - timedelta(days=current_date.weekday())
end_of_current_week = start_of_current_week + timedelta(days=6)
start_date_default = start_of_current_week.date()
end_date_default = end_of_current_week.date()



####################### PAGE LAYOUT #############################

#Layout of the page (Date picker range and texts)
headers_week=html.Div(
        children = [html.Span([
                        html.I(className='bi bi-calendar4-range'),
                        html.B('Select a date range: ', style={'margin-left': '5px'})]),
                    dcc.DatePickerRange(
                        id='date-picker-range',
                        min_date_allowed=datetime(2024, 1, 1),
                        max_date_allowed=datetime(2024, 12, 31), 
                        start_date=start_date_default,
                        end_date=end_date_default,
                        display_format='YYYY-MM-DD',
                        className='date-picker'),
                    html.Div("(Select Monday as the start date in the highlighted box)", style={'color': 'black', 'fontSize': 12, 'padding': 0, 'margin': 0}),
                    html.Br(),
                    html.H1(children='Overview for the Week'),

])

#Layout of page
layout = html.Div(children=[
    html.Br(),
    html.Div([
        dbc.Row([dbc.Col(headers_week),
                dbc.Col(html.Div(id='output-table'),width=4)])]),
    html.Br(),
    html.Div(children =[
        dbc.Row([dbc.Col(dcc.Graph(id='staff-present-fig'), className='chart'),
                 (dbc.Col(dcc.Graph(id='cost-hiring-fig'),className='chart'))])],
                 style={'position':'relative'}),


    html.Br()])

#Changing the date picker range to always select Monday as the start date 
@callback(
    Output('date-picker-range', 'start_date'),
    Input('date-picker-range', 'start_date')
)
def update_start_date(start_date):
    if start_date is not None:
        selected_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        # Check if the selected date is Monday (0 is Monday, 6 is Sunday)
        if selected_date.weekday() != 0:
            # Find the previous Monday
            previous_monday = selected_date - timedelta(days=selected_date.weekday())
            return previous_monday
    return start_date

@callback(
    Output('date-picker-range', 'end_date'),
    [Input('date-picker-range', 'start_date')]
)

#Ensuring the end date is the last day of the week 
def update_end_date(start_date):
    if start_date is not None:
        start_date = datetime.strptime(start_date.split(' ')[0], '%Y-%m-%d').date()
        end_date = start_date + timedelta(days=6)
        return end_date.strftime('%Y-%m-%d')
    



# Define callback by taking in date picker range parameters to update staff and cost graph 
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
        print(filtered_data)
        cost_group = filtered_data.groupby('Date_and_day')['Cost'].sum().reset_index()
        staff_counts=filtered_data.groupby(['Date_and_day', 'Role']).size().reset_index()
        print(staff_counts)
        print('sc',staff_counts.columns)
        staff_counts.columns = ['Date_and_day', 'Role', 'Counts']
        print(staff_counts)
        # Update figures with filtered data
        staff_present_fig = px.bar(data_frame=staff_counts,  
                                x='Date_and_day',
                                y=['Counts'],
                                color='Role',
                                # barmode='stack',
                                labels={'Date_and_day': 'Days of the Week', 'value': 'Number of Staffs'}, 
                                title='Number of Staffs Present for Each Day',
                                text=staff_counts['Counts'].apply(lambda x: '{0:.0f}'.format(x)),
                                color_discrete_map={'chef': '#fda64a', 'dishwasher': '#93c47d', 'service': '#93d1e0'},  # Map roles to colors
) 
        staff_present_fig.update_traces(textangle = 0)
        staff_present_fig.update_layout(legend=dict(
            # orientation="h",
            # yanchor="bottom",
            # y=1,
            xanchor="right",
            x=1.5
        ))

        cost_hiring_fig = px.bar(data_frame=cost_group, 
                                  x='Date_and_day',
                                  y='Cost', 
                                  labels = {'Date_and_day': 'Days of the Week', 'Cost' : 'Cost($)'} ,
                                  title ='Cost of Hiring')
        
        cost_hiring_fig.update_traces(marker_color='#fda64a')



        if (df2 ['Public_Holiday'] != '').any():
            filtered_df2 = df2[df2['Public_Holiday'] != '']

            ph_obj = filtered_df2[['Date_and_day','Public_Holiday']].apply(lambda row: ':\n'.join(map(str, row)), axis=1)

            ph_text=''
            for string_row in ph_obj:
                ph_text+=(string_row+'\n')
            table = dbc.Card(
                [dbc.CardBody(
                        [
                            html.H4(" Events",className='bi bi-calendar-event'),
                            html.P(ph_text,className='event-text'),
                        ]
                    ),
                ],
                style={'background-color': '#b6d7a8'},
            )


            return staff_present_fig, table, cost_hiring_fig
        else:
            return staff_present_fig, html.Div(), cost_hiring_fig

    else:
        return {'data': [], 'layout': {}}, {'data': [], 'layout': {}}
    

