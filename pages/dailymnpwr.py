import dash
from dash import Dash, dcc, html, Input, Output, dash_table, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# Load data from CSV
df = pd.read_csv('Schedule.csv')

# Filtered dfs



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

    dcc.Tabs(id="tabs", value="morndata", children=[
        dcc.Tab(label="Day", value="morndata"),
        dcc.Tab(label="Night (Chinese)", value="chidata"),
        dcc.Tab(label="Night (Indian)", value="inddata"),
    ]),
    html.Div(id="tab_content")

])

@callback(Output("tab_content","children"),
          Input("tabs","value"))

def render_content(tab):
    if tab == "morndata":
        return html.Div([
            dcc.Graph(id="table", figure= create_table(morndata)),
            dcc.Graph(id="bar_chart", figure= create_bar_chart(morndata))
        ])

    elif tab == "chidata":
        return html.Div([
            dcc.Graph(id="table", figure= create_table(chidata)),
            dcc.Graph(id="bar_chart", figure= create_bar_chart(chidata))
        ])

    elif tab == "inddata":
        return html.Div([
            dcc.Graph(id="table", figure= create_table(inddata)),
            dcc.Graph(id="bar_chart", figure= create_bar_chart(inddata))
        ])


@callback(Output("table", "figure"), [Input("tabs","value"),], config_prevent_initial_callbacks=True)
def update_table(data):
    return create_table(data)
@callback(Output("bar_chart","figure"), [Input("tabs","value"),], config_prevent_initial_callbacks=True)
def update_bar_chart(data):
    return create_bar_chart(data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


