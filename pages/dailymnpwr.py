import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import datetime

# Load data from CSV
manpower_schedule = pd.read_csv('../output/final_schedule.csv')
manpower_schedule ['Date_and_day'] = manpower_schedule['Date'] + ' ' + manpower_schedule['Day']
#tabulating the cost
manpower_schedule ['Cost'] = manpower_schedule['Hours_worked'] * manpower_schedule['Hourly_rate']

# customer_demand['Date'] = pd.to_datetime(customer_demand['Date'], format='%Y-%m-%d')
manpower_schedule['Date'] = pd.to_datetime(manpower_schedule['Date'], format='%Y-%m-%d')


# GENERATE THE NEXT 6 DAYS (DEFAULT=CURRENT DAY) -- WORK WITH DATE FIRST
# Get the first day of the week (Monday) based on the current date
start_of_week = datetime.datetime.today() - datetime.timedelta(days=datetime.datetime.today().weekday())

# Define days of the week starting from Monday
days_of_week = [(start_of_week + datetime.timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]

# Ordering for role
custom_order = {"chef": 1, "service": 2, "dishwasher" :3}

# Graphs
def create_table(data):
    fig = go.Figure(data=[go.Table(
        header=dict(values = [["Roles"], ["Employee ID"]]),
        cells=dict(values = [["Chef","Service","Dishwasher"], data.groupby("Role")["Employee_ID"].apply(list).loc[custom_order.keys()].tolist()]))
    ])
    return fig

def create_bar_chart(data):
    fig = px.histogram(data_frame=data, x="Role",
                       histfunc="count", barmode="group", height = 600)
    fig = fig.update_layout(bargap=0.5)
    return fig



# Initialize Dash app
app = dash.Dash(__name__)


# Define app layout
app.layout = html.Div([
    html.H1('Mount Faber Leisure Group'),
    html.P("MANPOWER"),

    #Day dropdown
    dcc.Dropdown(id='date',
    options=[{'label': day, 'value': day} for day in days_of_week], # can add for the other questions
    value=days_of_week[0], clearable=False),
    html.Br(),
    dcc.Tabs(id="shift", value="morn", children=[
        dcc.Tab(label="Morning", value="morn"),
        dcc.Tab(label="Night (Chinese)", value="chidata"),
        dcc.Tab(label="Night (Indian)", value="inddata"),
    ]),
    html.Br(),
    html.Div(id='employee-table'),
    html.Br(),
    dcc.Graph(id="graph"),

])

@callback([Output('employee-table', 'children'),Output('graph','figure')],
          [Input('date','value'),Input("shift","value")])





def produce_output(date,shift):
    print(date, shift)
    df=manpower_schedule.loc[manpower_schedule['Date'] == date]
    print(df)
    if shift=="morn":
        final_df=df.loc[df['Shift']=='10am-4.30pm']
    elif shift=='chidata':
        final_df=df.loc[df['Shift']=='7pm-10pm']
    else: # indian buffet
        final_df=df.loc[df['Shift']=='8pm-10pm']
    
    print('final',final_df)
    
    # create a new df to group employees
    roles_df=final_df.pivot_table(index='Role', values='Employee_ID', aggfunc=lambda x: ', '.join(x)).reset_index()
    roles_df.columns = ['Role', 'Employee_ID']
    print(roles_df)
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

    # show graph of chefs
    fig = px.histogram(final_df, x="Role")
    fig.update_layout(
        title='Histogram',
        yaxis_title='Count',
        yaxis=dict(
            dtick=1  # Set dtick to 1 for y-axis
        )
    )
    return table,fig



# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


