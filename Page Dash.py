from api import API
import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# Application Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout principal
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H2("Enedis Dashboard", className="display-4"),
            html.Hr(),
            html.Label("Entrez le numéro du département :"),
            dcc.Input(id='county-input', type='text', value='69', placeholder='Ex: 69'),
            html.Button('Charger les données', id='load-data', n_clicks=0),
            html.Hr(),
            html.Label("Choisissez la variable cible :"),
            dcc.Dropdown(id='target-selector', placeholder="Sélectionnez la variable cible"),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Visualisation des données", href="/", active="exact"),
                    dbc.NavLink("Graphiques", href="/graphs", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
        ], width=2),
        dbc.Col([
            dcc.Location(id='url'),
            html.Div(id='page-content')
        ], width=10)
    ])
], fluid=True)

# Variable pour stocker les données
df = pd.DataFrame()

@app.callback(
    [Output('page-content', 'children'),
     Output('target-selector', 'options')],
    [Input('load-data', 'n_clicks'),
     Input('url', 'pathname')],
    [State('county-input', 'value')]
)
def update_page(n_clicks, pathname, county):
    global df  # Utiliser une variable globale pour stocker le DataFrame

    if n_clicks > 0:
        # Charger les données à partir de l'API
        api = API(f"https://data.ademe.fr/data-fair/api/v1/datasets/dpe-v2-logements-existants/lines?size=10000&q={county}&q_fields=N%C2%B0_d%C3%A9partement_%28BAN%29&select=Ann%C3%A9e_construction%2CSurface_habitable_logement%2CNombre_niveau_logement%2CType_b%C3%A2timent%2CHauteur_sous-plafond%2CType_%C3%A9nergie_principale_chauffage%2CType_%C3%A9nergie_principale_ECS%2CConso_5_usages_%C3%A9_finale%2CConso_chauffage_%C3%A9_finale%2CConso_ECS_%C3%A9_finale%2CClasse_altitude%2CEtiquette_DPE%2CAdresse_(BAN)%2CNom__commune_(BAN)%2CCode_postal_(BAN)%2C_geopoint")
        all_data = api.get_all_data()
        df = pd.DataFrame(all_data)

        # Options pour la variable cible
        target_options = [{'label': col, 'value': col} for col in df.columns]

    # Gestion de la navigation
    if pathname == "/graphs":
        return render_graphs_page(), target_options
    else:
        return render_data_table(), target_options

# Page 1 : Visualisation des données
def render_data_table():
    return html.Div([
        html.H3('Visualisation des données Enedis'),
        dcc.Dropdown(
            id='filter',
            options=[{'label': name, 'value': name} for name in df['Etiquette_DPE'].unique()],
            multi=True,
            placeholder="Filtrer par ..."
        ),
        html.Br(),
        html.Div(id='data-table', children=[]),
    ])

@app.callback(
    Output('data-table', 'children'),
    [Input('filter', 'value')]
)
def update_table(selected):
    if selected:
        filtered_df = df[df['Etiquette_DPE'].isin(selected)]
    else:
        filtered_df = df
    return dbc.Table.from_dataframe(filtered_df, striped=True, bordered=True, hover=True)

# Page 2 : Graphiques
def render_graphs_page():
    return html.Div([
        html.H3('Graphiques interactifs'),
        dcc.Dropdown(
            id='graph-type',
            options=[
                {'label': 'Nuage de points', 'value': 'scatter'},
                {'label': 'Histogramme', 'value': 'histogram'},
                {'label': 'Boîte à moustaches', 'value': 'box'},
                {'label': 'Graphique en barres', 'value': 'bar'},
            ],
            value='scatter',
            placeholder="Choisir le type de graphique"
        ),
        dcc.Dropdown(
            id='x-axis',
            options=[{'label': col, 'value': col} for col in df.columns if col not in ['target', 'Etiquette_DPE']],
            value=df.columns[0] if not df.empty else None,
            placeholder="Choisir l'axe des X"
        ),
        dcc.Dropdown(
            id='y-axis',
            options=[{'label': col, 'value': col} for col in df.columns if col not in ['target', 'Etiquette_DPE']],
            value=df.columns[1] if len(df.columns) > 1 else None,
            placeholder="Choisir l'axe des Y"
        ),
        dcc.Graph(id='dynamic-plot')
    ])

@app.callback(
    Output('dynamic-plot', 'figure'),
    [Input('x-axis', 'value'), Input('y-axis', 'value'), Input('graph-type', 'value'), Input('target-selector', 'value')]
)
def update_dynamic_plot(x_col, y_col, graph_type, target_col):
    if x_col and y_col and target_col:
        if graph_type == 'scatter':
            fig = px.scatter(df, x=x_col, y=y_col, color=target_col,
                             title=f"Nuage de points ({x_col} vs {y_col}) par {target_col}")
        elif graph_type == 'histogram':
            fig = px.histogram(df, x=x_col, color=target_col,
                               title=f"Histogramme de {x_col} par {target_col}")
        elif graph_type == 'box':
            fig = px.box(df, x=target_col, y=y_col,
                         title=f"Boîte à moustaches de {y_col} par {target_col}")
        elif graph_type == 'bar':  
            fig = px.bar(df, x=x_col, y=y_col, color=target_col,
                         title=f"Graphique en barres ({x_col} vs {y_col}) par {target_col}")
        return fig
    return {}

# Lancer le serveur
if __name__ == '__main__':
    app.run_server(debug=True)
