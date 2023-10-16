import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import dash_table

# Carga tus datos
importaciones = pd.read_excel('./data2/IMPORTACION-VOLUMEN-2023-05.xlsx', skiprows=6)
consumo = pd.read_excel('./data2/CONSUMO-2023-05.xlsx', skiprows=6)
precios_2023 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=0, skiprows=7)
precios_2022 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=1, skiprows=6)
precios_2021 = pd.read_excel('./data2/Precios-Promedio-Nacionales-Diarios-2023.xlsx', sheet_name=2, skiprows=6)

# Ruta donde se encuentran los archivos Excel exportados
ruta_exportacion = 'dataLimpia/'

# Importar datos de importaciones desde el archivo Excel
importas = pd.read_excel(f'{ruta_exportacion}importaciones.xlsx')

# Importar datos de consumo desde el archivo Excel
consumas = pd.read_excel(f'{ruta_exportacion}consumo.xlsx')

# Importar datos de precios desde el archivo Excel
preciosas = pd.read_excel(f'{ruta_exportacion}precios.xlsx')


# Colores personalizados para el control deslizante
custom_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# Tipos de gráfico disponibles
chart_types = ['scatter', 'bar', 'line', 'histogram']

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
        {'label': 'Precios', 'value': 'precios'}
        ],
        value='importaciones'
    ),

    # Selector de tipo de gráfico
    dcc.Dropdown(
        id='chart-type',
        options=[
            {'label': 'Scatter', 'value': 'scatter'},
            {'label': 'Bar', 'value': 'bar'},
            {'label': 'Line', 'value': 'line'},
            {'label': 'Histogram', 'value': 'histogram'}
        ],
        value='scatter'
    ),

    # Control deslizante para cambiar el color del gráfico
    dcc.Slider(
        id='color-slider',
        min=0,
        max=len(custom_colors) - 1,
        step=1,
        value=0,
        marks={i: str(i) for i in range(len(custom_colors))}
    ),

    # Gráfico de datos
    dcc.Graph(id='data-graph'),

    # Leyenda para mostrar la descripción del conjunto de datos
    html.Div(id='data-description'),

    # Contenedor para gráficos Seaborn
    html.Div(id='seaborn-plot-container'),


    # Botón para mostrar/ocultar la tabla
    html.Button('Mostrar/Ocultar Tabla', id='toggle-button'),

    # Tabla para mostrar datos subyacentes
    html.Div(dash_table.DataTable(id='data-table'), id='table-container', style={'display': 'none'})
])

# Callback para mostrar/ocultar la tabla
@app.callback(
    Output('table-container', 'style'),
    Output('toggle-button', 'children'),
    [Input('toggle-button', 'n_clicks')],
    State('table-container', 'style')
)
def toggle_table(n_clicks, current_style):
    if n_clicks is None:
        return current_style, 'Mostrar Tabla'
    if current_style.get('display') == 'none':
        return {'display': 'block'}, 'Ocultar Tabla'
    return {'display': 'none'}, 'Mostrar Tabla'



# Callback para actualizar los gráficos, descripción y tabla de datos
@app.callback(
    [Output('data-graph', 'figure'), Output('data-description', 'children'), Output('data-table', 'columns'), Output('data-table', 'data')],
    [Input('data-selector', 'value'), Input('chart-type', 'value'), Input('color-slider', 'value')]
)
def update_data(selected_data, chart_type, color_value):
    data = None
    description = ""
    table_columns = []
    table_data = []
    if selected_data == 'importaciones':
        data = importas
        description = "Datos de importaciones"
    elif selected_data == 'consumo':
        data = consumas
        description = "Datos de consumo"
    elif selected_data == 'precios':
        data = preciosas
        description = "Datos de precios"
  
    if data is not None:
        if chart_type == 'scatter':
            fig = px.scatter(data, x=data.columns[0], y=data.columns[1])

            # Escala de color en función de la posición relativa en el eje Y
            fig.update_traces(marker=dict(color=data.index, colorscale='Viridis'))
        elif chart_type == 'bar':
            fig = px.bar(data, x=data.columns[0], y=data.columns[1])
        elif chart_type == 'line':
            fig = px.line(data, x=data.columns[0], y=data.columns[1])
        elif chart_type == 'histogram':
            fig = px.histogram(data, x=data.columns[1])

        # Aplicar el color seleccionado del control deslizante
        selected_color = custom_colors[color_value]
        fig.update_traces(marker=dict(color=selected_color))

        # Configurar las columnas y datos para la tabla
        table_columns = [{'name': col, 'id': col} for col in data.columns]
        table_data = data.to_dict('records')

        return fig, description, table_columns, table_data
    else:
        return {}, "", [], []
    


if __name__ == '__main__':
    app.run_server(debug=True)