import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback
import plotly.graph_objects as go
import plotly.express as px
from dash import dash_table 
from datetime import datetime, timedelta, date
import dash_bootstrap_components as dbc
from urllib.parse import quote
from shared_data import manpower_schedule

dash.register_page(__name__, path='/employee_details', name="Employee Details👬")

#Load data from CSV

manpower_schedule = manpower_schedule
# define employee image mapping 

employee_image_mapping = {'A2': '/assets/A2.jpeg' , 'A1': '/assets/A1.jpg' }


# Calculate current week's start and end date
current_date = datetime.now()
start_of_current_week = current_date - timedelta(days=current_date.weekday())
end_of_current_week = start_of_current_week + timedelta(days=6)



# headers 
header = html.Div([
    dbc.Row([
        dbc.Col(html.Div([
            html.Span([
                        html.I(className='bi bi-calendar4-range'),
                        html.B('Select a date range: ', style={'margin-left': '5px'})]),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date_placeholder_text='Start Date',
                end_date_placeholder_text='End Date',
                start_date=start_of_current_week.date(),
                end_date=end_of_current_week.date(),
                display_format='YYYY-MM-DD',
                style = {'margin' : '10px'}
            ),
            html.Div("(Select Monday as the start date in the highlighted box)", style={'color': 'black', 'fontSize': 12, 'padding': 0, 'margin': 0})
        ]), width={'size': 6}),
        dbc.Col(html.Div([
                html.Span([html.I(className='bi bi-person-badge'),
                        html.B('Enter an employee name:  ', style={'margin-left': '5px'})]),
            dcc.Input(id='employee-name-input', type='text', placeholder='Enter Employee Name', style = {'margin': '10px'})
        ]), width={'size': 6})
    ]),

])




#first row

first_row = html.Div([
    dbc.Row([
        dbc.Col(html.Div(id='employee-info-output',className='employee-table'), width=7),
        dbc.Col([html.Div(id='employee-card'),html.Div(id='whatsapp')], width = 5)
        
        
    ])],className='ed-first')


#second row 

second_row = html.Div([
    dbc.Row([
        dbc.Col(html.Div(id= 'work-schedule-output'), width = {'size': 9})
        ])
    ])

layout = html.Div([
    html.Br(),
    header,
    html.Br(),
    first_row,
    html.Br(),
    html.Br(),
    html.Div(id='employee-schedule-heading'),
    html.Br(),
    second_row

    ])


@callback(
    Output('employee-schedule-heading', 'children'),
    [Input('employee-name-input', 'value')]
)
def update_employee_schedule_heading(employee_name):
    if employee_name and employee_name in manpower_schedule['Employee_ID'].unique():
        return html.B(f"{employee_name}'s Schedule", style={'font-size': '20px'})
    else:
        return ""

# Callback to update employee information based on selected date range and employee ID
@callback(
    [Output('employee-info-output', 'children'),
     Output('employee-card', 'children'),
     Output('whatsapp','children')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('employee-name-input', 'value')]
)
def update_employee_info(start_date, end_date, employee_name):
    if start_date and end_date and employee_name:
        filtered_manpower_schedule = manpower_schedule[(manpower_schedule['Date'] >= start_date) & (manpower_schedule['Date'] <= end_date) & (manpower_schedule['Employee_ID'] == employee_name)]
        
        if not filtered_manpower_schedule.empty:
            # Extract employee information
            role = filtered_manpower_schedule['Role'].iloc[0]
            job_status = filtered_manpower_schedule['Job_status'].iloc[0]
            total_hours_worked = filtered_manpower_schedule['Hours_worked'].sum()
            hourly_rate = filtered_manpower_schedule['Hourly_rate'].iloc[0]  # Assuming hourly rate is consistent for the employee
            total_salary = total_hours_worked * hourly_rate
            
            # Create DataTable for employee information
            employee_info_table = dash_table.DataTable(
                id='employee',
                columns=[{'name': ' Employee Information ', 'id': 'Attribute'}, {'name': ' ', 'id': 'Value'}],
                data=[
                    {'Attribute': 'Role', 'Value': role},
                    {'Attribute': 'Job status', 'Value': job_status},
                    {'Attribute': 'Rate', 'Value': f"${hourly_rate}/ hr"},
                    {'Attribute': 'Total hours worked for the week', 'Value': f"{total_hours_worked} hours"},
                    {'Attribute': 'Total salary for the week ($) ', 'Value': f"${total_salary}"}
                ],
                style_table={'overflowY': 'auto'},
                style_cell={"background-color": "#fce5cd", "border": "solid 1px white", "color": "black", "font-size": "11px", "text-align": "left",'font_family':"'Outfit', sans-serif","font-size": "16px","padding": "10px"},
                style_header={"background-color": "#fda64a", "font-weight": "bold", "color": "white", "padding": "10px", "font-size": "18px"},
                style_data_conditional=[
                    {'if': {'column_id': 'Attribute'},'color': '#000000'},
                    {'if': {'column_id': 'Value'},'color': 'black'}
                    ]

            )
            
            # UPDATE EMPLOYEE CARD
            employee_image_path = employee_image_mapping.get(employee_name)
            if not employee_image_path:
                employee_image_path=''
            employee_card=html.Div([html.Img(src=employee_image_path,className='employee-image'),
                                        # html.H4(employee_name),
                                        # html.H6(role),
                                        html.Br(),
                                        html.Br(),
                                        
                                    ],
                                    className='employee-card')
            whatsapp_button=html.A("WhatsApp Message",
                        href=f"https://wa.me/6585224420/?text={quote('Hello, please be informed that...')}",
                        target="_blank",
                        style={
                            'display': 'inline-block',
                            'background-color': '#547047',
                            'color': 'white',
                            'padding': '5px 10px',
                            'border-radius': '5px',
                            'text-decoration': 'none',
                        },
                        className='bi bi-whatsapp')
            if employee_name is None:
                return None         
            return employee_info_table, employee_card, whatsapp_button
        else:
            return html.P('No data available for the selected date range and employee name.', style={'fontWeight': 'bold', 'fontSize': '20px'}), None, None
    else:
        return [], None, None


    











@callback(
    Output('work-schedule-output', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('employee-name-input', 'value')]
    )
def employee_schedule(start_date,end_date,employee_name):
    if start_date and end_date and employee_name:
        filtered_manpower_schedule = manpower_schedule[(manpower_schedule['Date'] >= start_date) & (manpower_schedule['Date'] <= end_date) & (manpower_schedule['Employee_ID'] == employee_name)]

        if not filtered_manpower_schedule.empty:

            filtered_manpower_schedule['☀️ Morning (10am-4.30pm)'] = filtered_manpower_schedule.apply(lambda x: x['Employee_ID'] if x['Shift'] == '10am-4.30pm' else '', axis=1)
            filtered_manpower_schedule['🌙 Night-Chinese (7pm-10pm)'] = filtered_manpower_schedule.apply(lambda x: x['Employee_ID'] if x['Shift'] == '7pm-10pm' else '', axis=1)
            filtered_manpower_schedule['🌕 Night-Indian (8pm-10pm)'] = filtered_manpower_schedule.apply(lambda x: x['Employee_ID'] if x['Shift'] == '8pm-10pm' else '', axis=1)

            # Aggregating the data to remove duplicates
            filtered_manpower_schedule = filtered_manpower_schedule.groupby('Date').agg({
                '☀️ Morning (10am-4.30pm)': ' '.join,
                '🌙 Night-Chinese (7pm-10pm)': ' '.join,
                '🌕 Night-Indian (8pm-10pm)': ' '.join
            }).reset_index()
            filtered_manpower_schedule['Date'] = filtered_manpower_schedule['Date'].dt.strftime('%Y-%m-%d')

            # Convert non-empty employee IDs to ticks and store them in new columns
            for col in ['☀️ Morning (10am-4.30pm)', '🌙 Night-Chinese (7pm-10pm)', '🌕 Night-Indian (8pm-10pm)']:
                filtered_manpower_schedule[col] = filtered_manpower_schedule[col].apply(lambda x: '✓' if x.strip() != '' else '')
            
            work_schedule_table=dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in filtered_manpower_schedule.columns],
                    data=filtered_manpower_schedule.to_dict('records'),
                    style_cell={"background-color": "#b6d7a8", "border": "solid 1px black", "color": "black", "font-size": "11px", "text-align": "left",'font_family':"'Outfit', sans-serif","font-size": "16px","padding": "10px"},
                    style_header={'backgroundColor': '#547047','color': 'white','fontWeight': 'bold','padding': '10px','fontSize': '18px'},
                    style_data_conditional=[
                        {
                            'if': {'column_id': col},
                            'backgroundColor': '#b6d7a8',
                            # 'color': 'white'
                        } for col in filtered_manpower_schedule.columns[1:] if filtered_manpower_schedule[col].str.contains('✓').any()
                    ] + [
                        {
                            'if': {'column_id': col, 'filter_query': '{{{0}}} is blank'.format(col)},
                            'backgroundColor': 'white',
                            'color': 'black'
                        } for col in filtered_manpower_schedule.columns[1:]
                    ],
                )            
            return work_schedule_table
        else:
            return []
    else:
        return []

