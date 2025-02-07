import base64
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import requests
import rasterio
import numpy as np


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

    # with rasterio.open('geopandas/ai360_climateviz/lvl_pred_maps/19016/2024-10_7.17_depth.tiff') as src:
    #     # Чтение данных
    #     raster = src.read()  # Предполагаем, что у нас один канал
        
    #     # Получение координат
    #     height = src.height
    #     width = src.width
    #     cols, rows = np.meshgrid(np.arange(width), np.arange(height))
    #     xs, ys = rasterio.transform.xy(src.transform, rows, cols)
        
    #     # Создание DataFrame
    #     df = pd.DataFrame({
    #         'x': xs.ravel(),
    #         'y': ys.ravel(),
    #         'value': raster.ravel()
    #     })

    # fig.add_trace(px.density_mapbox(df, 
    #     lat='x', 
    #     lon='y', 
    #     z='value', 
    #     radius=10,
    #     center=dict(lat=df['x'].mean(), lon=df['y'].mean()), 
    #     zoom=10,
    #     mapbox_style="open-street-map"))

    
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
