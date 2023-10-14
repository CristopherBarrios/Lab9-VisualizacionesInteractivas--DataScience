import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Carga tus datos
importaciones = pd.read_excel('./data2/IMPORTACION-VOLUMEN-2023-05.xlsx', skiprows=6)
consumo = pd.read_excel('./data2/CONSUMO-2023-05.xlsx', skiprows=6)
precios_2023 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=0, skiprows=7)
precios_2022 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=1, skiprows=6)
precios_2021 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=2, skiprows=6)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño del cuadro de mando
app.layout = html.Div([
    html.H1("Cuadro de Mando Interactivo"),
    
    # Selector de datos
    dcc.Dropdown(
        id='data-selector',
        options=[
            {'label': 'Importaciones', 'value': 'importaciones'},
            {'label': 'Consumo', 'value': 'consumo'},
            {'label': 'Precios 2023', 'value': 'precios_2023'},
            {'label': 'Precios 2022', 'value': 'precios_2022'},
            {'label': 'Precios 2021', 'value': 'precios_2021'}
        ],
        value='importaciones'
    ),

    # Gráfico de datos
    dcc.Graph(id='data-graph')
])

# Callback para actualizar los gráficos en función de la selección del usuario
@app.callback(
    Output('data-graph', 'figure'),
    Input('data-selector', 'value')
)
def update_data_graph(selected_data):
    data = None
    if selected_data == 'importaciones':
        data = importaciones
    elif selected_data == 'consumo':
        data = consumo
    elif selected_data == 'precios_2023':
        data = precios_2023
    elif selected_data == 'precios_2022':
        data = precios_2022
    elif selected_data == 'precios_2021':
        data = precios_2021

    if data is not None:
        # Usa Plotly Express para crear figuras interactivas
        fig = px.histogram(data, x=data.columns[1])
        return fig
    else:
        return {}

if __name__ == '__main__':
    app.run_server(debug=True)
