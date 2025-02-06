import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import json
import requests


def map_fig(russia_geojson, points_geojson):
    # Создание фигуры
    fig = go.Figure()

    # Добавление хороплета России
    fig.add_trace(go.Choroplethmapbox(
        geojson=russia_geojson,
        locations=[feat['properties']['name'] for feat in russia_geojson['features']],
        z=[1]*len(russia_geojson['features']),
        colorscale=[[0, 'lightblue'], [1, 'lightblue']],
        showscale=False,
        marker_opacity=0.5,
        marker_line_width=0
    ))

    # Извлечение координат и свойств точек из GeoJSON
    lats, lons, gauge_ids, descriptions = [], [], [], []
    for feature in points_geojson['features']:
        if feature['geometry']['type'] == 'Point':
            lon, lat = feature['geometry']['coordinates']
            lons.append(lon)
            lats.append(lat)
            # desc = "<br>".join([f"{k}: {v}" for k, v in feature['properties'].items()])
            desc = "<br>".join([feature['properties']['name_ru'],
                                "Станция №" + str(feature['properties']['gauge_id'])
                                ])      
            descriptions.append(desc)
            gauge_ids.append(feature['properties']['gauge_id'])

    # Добавление точек из GeoJSON
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lons,
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='red',
        ),
        hovertext=descriptions,
        ids=gauge_ids,
        hoverinfo='text'
    ))

    # Настройка макета
    fig.update_layout(
        mapbox_style="carto-positron",
        mapbox=dict(
            center=dict(lat=65, lon=105),
            zoom=2
        ),
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    return fig
