import pandas as pd
import dash
from dash import html, dash_table, dcc,Input, Output,callback
import plotly.graph_objects as go
import plotly.express as px
from dash import dash_table 
from datetime import datetime, timedelta, date

dash.register_page(__name__, path='/employee_details', name="Employee Details👬")

#Load data from CSV

manpower_schedule = pd.read_csv('output/final_schedule.csv')


# Calculate current week's start and end date
current_date = datetime.now()
start_of_current_week = current_date - timedelta(days=current_date.weekday())
end_of_current_week = start_of_current_week + timedelta(days=6)

layout = html.Div([
    html.Br(),
    html.Label('Select Date Range:', style={'textDecoration': 'underline', 'fontWeight': 'bold', 'fontSize': '25px'},className='date-picker'),
    dcc.DatePickerRange(
        id='date-picker-range',
        start_date_placeholder_text='Start Date',
        end_date_placeholder_text='End Date',
        start_date=start_of_current_week.date(),
        end_date=end_of_current_week.date(),
        display_format='YYYY-MM-DD'
    ),
    html.Br(),
    html.Br(),
    html.Label('Enter Employee Name:', style={'textDecoration': 'underline', 'fontWeight': 'bold', 'fontSize': '25px'}, className='date-picker'),
    dcc.Input(id='employee-name-input', type='text', placeholder='Enter Employee Name'),
    html.Br(),
    html.Br(),
    html.Div(id='employee-info-output')
])

# Callback to update employee information based on selected date range and employee ID
@callback(
    Output('employee-info-output', 'children'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('employee-name-input', 'value')]
)
def update_employee_info(start_date, end_date, employee_id):
    if start_date and end_date and employee_id:
        # Filter DataFrame based on selected date range and employee ID
        filtered_manpower_schedule = manpower_schedule[(manpower_schedule['Date'] >= start_date) & (manpower_schedule['Date'] <= end_date) & (manpower_schedule['Employee_ID'] == employee_id)]
        
        if not filtered_manpower_schedule.empty:
            # Aggregate hours worked and calculate salary
            total_hours_worked = filtered_manpower_schedule['Hours_worked'].sum()
            hourly_rate = filtered_manpower_schedule['Hourly_rate'].iloc[0]  # Assuming hourly rate is consistent for the employee
            
            # Calculate salary
            total_salary = total_hours_worked * hourly_rate
            
            # Extract employee information
            role = filtered_manpower_schedule['Role'].iloc[0]
            job_status = filtered_manpower_schedule['Job_status'].iloc[0]
            
            # Create table to display employee information
            employee_info_table = html.Table([
                html.Tr([html.Th('Role:'), html.Td(role)]),
                html.Tr([html.Th('Job Status:'), html.Td(job_status)]),
                html.Tr([html.Th('Total Hours Worked:'), html.Td(f"{total_hours_worked} hours")]),
                html.Tr([html.Th('Rate:'), html.Td(f"${hourly_rate}/ hr")]),
                html.Tr([html.Th('Total Salary ($):'), html.Td(f"${total_salary}")])
            ], style={'fontSize': '18px'})
            return employee_info_table
        else:
            return html.P('No data available for the selected date range and employee name.', style={'fontWeight': 'bold', 'fontSize': '20px'})
    else:
        return html.P('Please select a date range and enter an employee name.', style={'fontWeight': 'bold', 'fontSize': '20px'})