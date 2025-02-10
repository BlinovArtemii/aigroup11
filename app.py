import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json
import requests
from map_tiffs_points import map_fig
from test_plot import show_plot

# Загрузка GeoJSON данных России
url_russia = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/russia.geojson"
response_russia = requests.get(url_russia)
russia_geojson = json.loads(response_russia.text)

# Загрузка GeoJSON данных с точками
# Замените URL на ваш реальный URL или путь к файлу
response = requests.get("https://raw.githubusercontent.com/BlinovArtemii/aigroup11/refs/heads/master/ai360_climateviz/gauge_stations.geojson")
points_geojson = json.loads(response.text)

# Инициализация приложения Dash
app = dash.Dash(__name__)

# Определение layout приложения
app.layout = html.Div([
    html.Div([
        dcc.Graph(id='map', figure=map_fig(russia_geojson, points_geojson))
    ]),
    html.Div(children=[
        dcc.Graph(
            id='graph'
        )
    ])
])


# Callback для обработки кликов
@app.callback(
    Output('graph', 'figure'),
    Input('map', 'clickData')
)
def display_click_data(clickData):
    if clickData is None:
        return show_plot("70620", "р.Евда - Евда, Станция №70620")
    else:
        point_data = clickData['points'][0]
        print(point_data)
        if 'id' in point_data:
            return show_plot(point_data['id'], ", ".join(point_data['hovertext'].split('<br>')))
        else:
            return show_plot("70620", "р.Евда - Евда, Станция №70620")


# Запуск приложения
if __name__ == '__main__':
    app.run_server(debug=True)