import dash
import calendar
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

def show_plot(gauge_id):
	data = pd.read_csv(f"https://raw.githubusercontent.com/BlinovArtemii/group11/refs/heads/master/ai360_climateviz/lvl_obs/{gauge_id}.csv")

	data['date'] = pd.to_datetime(data['date'])
	data['day_of_year'] = data['date'].dt.dayofyear
	data_1=data.groupby(["day_of_year"])["lvl_sm"].describe()["mean"]
	data_2=data_1.reset_index()
	data=data_2

	fig = px.line(data, x="day_of_year", y="mean", title=f"Уровень воды за прошлые годы")
	return fig

	# app = dash.Dash(name="my_first_dash_app")
	# app.layout = html.Div(children=[
	# 	html.H1(children='Уровень воды'),

	# 	html.Div(children='''
	# 		Река N1 за все время исследования
	# 	'''),
	# 	dcc.Dropdown(
	# 		id='month-list',
	# 		options=[{'label': month, 'value': month} for month in data['month'].unique()],
	# 		value=1,
	# 		placeholder="Выберите месяц"
	# ),
	# 	dcc.Graph(
	# 		id='example-graph',
	# 	)
	# ])
	# @app.callback(
	# 	Output('example-graph', 'figure'),
	# 	Input('month-list', 'value'),
	# )
	# def update_graph(selected_month):
	# 	filtered_data = data[data['month'] == selected_month]#нет ошибки т.к. по умолчанию выбран январь

	# 	fig = px.line(filtered_data, x="day", y="mean", title=f"Уровень воды за {selected_month}")
		
	# if __name__ == '__main__':
   # app.run_server(debug=True)
	# return True
# Show_plot("19016")