from dash import Dash, html, dcc
import dash
import plotly.express as px
import datetime
import dash_bootstrap_components as dbc



#setting the date
current_date = datetime.datetime.now()
start_of_current_week = current_date - datetime.timedelta(days=current_date.weekday())
end_of_current_week = start_of_current_week + datetime.timedelta(days=6)
start_date_default = start_of_current_week.date()
end_date_default = end_of_current_week.date()

# LAYOUT
px.defaults.template = "ggplot2"

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css", ]

app = Dash(__name__, pages_folder='pages', use_pages=True, external_stylesheets=external_css)

app.layout = html.Div([
	html.Br(),
    html.Img(src='https://www.mountfaberleisure.com/wp-content/uploads/2023/08/logo.png', style={'height': '50px', 'margin-right': '10px','float': 'left'}),
	html.Br(),
	html.Br(),	
	html.H1(datetime.datetime.now().strftime('Last updated: %Y-%m-%d %H:%M:%S'),
		style={'opacity': '1','color': 'blue', 'fontSize': 15, 'position': 'absolute', 'top': '2px', 'right': '2px'}),
    html.Br(),
    html.Div(children=[
	    dcc.Link(page['name'], href=page["relative_path"], className="btn btn-dark m-2 fs-5")\
			  for page in dash.page_registry.values()], style={'height': '50px', 'margin-right': '10px'}
	),
    html.Br(),
	dash.page_container
], className="col-8 mx-auto")

if __name__ == '__main__':
	app.run(debug=True)