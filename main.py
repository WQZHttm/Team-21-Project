from dash import Dash, html, dcc
import dash
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc


external_css = [dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP,"https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)

sidebar=html.Div([
	dbc.Nav(
		[dbc.NavLink('Daily',href='/',active='exact'),
   		dbc.NavLink('Week',href='/week',active='exact')],
	vertical=True,
	pills=True,
	)
])






app.layout = html.Div([
	html.Br(),
    html.Img(src='https://www.mountfaberleisure.com/wp-content/uploads/2023/08/logo.png', style={'height': '50px', 'margin-right': '10px','float': 'left'}),
	html.Br(),
	html.Br(),	
	html.H1(datetime.datetime.now().strftime('Last updated: %Y-%m-%d %H:%M:%S'),
		style={'opacity': '1','color': 'blue', 'fontSize': 15, 'position': 'absolute', 'top': '2px', 'right': '2px'}),
    html.Br(),
    
    # side bar
    html.Div(dbc.Row([dbc.Col(sidebar, width=2), dbc.Col(dash.page_container, width=10)])),
    html.Br(),
])

if __name__ == '__main__':
	app.run(debug=True)