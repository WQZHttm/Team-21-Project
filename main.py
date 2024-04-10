from dash import Dash, html, dcc
import dash
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc
import dash_auth

# auth login details {user:password}
USER_PASS_MAPPING={
	'admin1':'admin1',
	'admin123':'admin123',
	'admin456':'admin456'
}

external_css = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)
# auth=dash_auth.BasicAuth(app,USER_PASS_MAPPING)

sidebar = html.Div([
    html.Br(),
    html.Img(src='https://eber.co/wp-content/uploads/2023/08/mount-faber-logo-768x288.png', style={'height': '70px', 'margin-right': '10px','float': 'left'}),
    html.Br(),
    html.Br(), 
    html.Hr(),
    html.Div([html.Span([
                    html.I(className='bi bi-person-circle'),
                    html.Span('Hao Xiang', id='user-login',style={'margin-left': '5px'})])],
             className='sidebar-user'),
    dbc.Nav(
        [
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-cloud'),
                    html.Span('Daily', style={'margin-left': '5px'})]), href='/', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-cloud'),
                    html.Span('Week', style={'margin-left': '5px'})]), href='/week', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-cloud'),
                    html.Span('Employee Details', style={'margin-left': '5px'})]), href='/employee_details', active='exact',className='sidebar-list-item'),
            dbc.NavLink(html.Span([
                    html.I(className='bi bi-cloud'),
                    html.Span('Labour Cost Percentage', style={'margin-left': '5px'})]), href='/lcp', active='exact',className='sidebar-list-item'),
    
        ],
        vertical=True,
        pills=True,
    ),
], className='sidebar')



app.layout = html.Div([
	# html.H1(datetime.datetime.now().strftime('Last updated: %Y-%m-%d %H:%M:%S'),
	# 	style={'opacity': '1','color': 'blue', 'fontSize': 15, 'position': 'absolute', 'top': '2px', 'right': '2px'}),
    # html.Br(),
    
    # side bar
    html.Div(children=dbc.Row([dbc.Col(sidebar, width=2), dbc.Col(dash.page_container)])),
])

if __name__ == '__main__':
	app.run(debug=True)