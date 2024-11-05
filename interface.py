from model import Model

import base64
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio

class DashInterface:
    """
    Interface Dash pour visualiser les données et faire des prédictions
    """

    # Constructeur de la classe
    def __init__(self, dataframe):
        self.app = dash.Dash(__name__, external_stylesheets=['/assets/style.css'])
        self.app.title = "Projet Enedis"
        self.server = self.app.server
        self.df = dataframe
        self.current_fig = None
        self.setup_layout()
        self.setup_callbacks()

    # Méthode pour initialiser l'interface
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Contexte', value='tab-1', className='tab', selected_className='tab selected'),
                dcc.Tab(label='Graphiques', value='tab-2', className='tab', selected_className='tab selected'),
                dcc.Tab(label='Prédiction', value='tab-3', className='tab', selected_className='tab selected'),
            ]),
            html.Div(id='tabs-content')
        ])
    
    # Méthode pour afficher la page "Contexte"
    def render_context_page(self):
        return html.Div([
            html.H1('Contexte'),
            html.P("Cliquez sur le bouton ci-dessous pour télécharger les données en CSV :"),
            html.Button("Télécharger les données CSV", id="export-csv-context", n_clicks=0),
            dcc.Download(id="download-dataframe-csv-context")
        ])

    # Méthode pour afficher la page "Graphiques"
    def render_graphs_page(self):
        return html.Div([
            html.H1('Graphiques interactifs'),
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
                options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Etiquette_DPE']],
                value=self.df.columns[0] if not self.df.empty else None,
                placeholder="Choisir l'axe des X"
            ),
            dcc.Dropdown(
                id='y-axis',
                options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Etiquette_DPE']],
                value=self.df.columns[1] if len(self.df.columns) > 1 else None,
                placeholder="Choisir l'axe des Y"
            ),
            dcc.Dropdown(
                id='data-filter',
                options=[{'label': label, 'value': label} for label in self.df['Etiquette_DPE'].unique()],
                multi=True,
                placeholder="Filtrer par Etiquette DPE"
            ),
            dcc.Graph(id='dynamic-plot'),
            html.Button("Exporter en PNG", id="export-png", n_clicks=0),
            html.A(id="download-link", download="graph.png", children="")  
        ])
    
    # Méthode pour afficher la page "Prédiction"
    def render_prediction_page(self):
        return html.Div([
            html.H1('Remplissez les champs ci-dessous pour obtenir une prédiction de la classe énergétique de votre logement :'),
            html.H2('Informations générales sur le logement'),
            html.Div([
                html.Label('Code postal'),
                dcc.Input(id='code-postal', type='text', placeholder='Code postal'),
            ]),
            html.Div([
                html.Label('Année de construction'),
                dcc.Input(id='annee-construction', type='number', placeholder='Année de construction'),
            ]),
            html.Div([
                html.Label('Type de logement'),
                dcc.Dropdown(
                    id='type-batiment',
                    options=[{'label': 'Maison', 'value': 'Maison'}, {'label': 'Appartement', 'value': 'Appartement'}, {'label': 'Immeuble', 'value': 'Immeuble'}],
                    placeholder='Type de logement'
                ),
            ]),
            html.Div([
                html.Label('Surface habitable (en m²)'),
                dcc.Input(id='surface-habitable', type='number', placeholder='Surface habitable'),
            ]),
            html.Div([
                html.Label('Nombre d\'étage(s)'),
                dcc.Input(id='nombre-etage', type='number', placeholder='Nombre d\'étage(s)'),
            ]),
            html.Div([
                html.Label('Hauteur sous plafond (en m)'),
                dcc.Input(id='hauteur-plafond', type='number', placeholder='Hauteur sous plafond'),
            ]),
            html.H2('Informations de consommation du logement'),
            html.Div([
                html.Label('Type d\'énergie du chauffage'),
                dcc.Dropdown(
                    id='type-energie-chauffage',
                    options=[{'label': 'Électricité', 'value': 'Électricité'}, {'label': 'Gaz naturel', 'value': 'Gaz naturel'}, {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'}, {'label': 'Fioul domestique', 'value': 'Fioul domestique'}, {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'}, {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'}, {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'}, {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'}, {'label': 'GPL', 'value': 'GPL'}, {'label': 'Propane', 'value': 'Propane'}, {'label': 'Charbon', 'value': 'Charbon'}, {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'}, {'label': 'Butane', 'value': 'Butane'}],
                    placeholder='Type d\'énergie du chauffage'
                ),
            ]),
            html.Div([
                html.Label('Type d\'énergie pour l\'eau chaude sanitaire'),
                dcc.Dropdown(
                    id='type-energie-ecs',
                    options=[{'label': 'Électricité', 'value': 'Électricité'}, {'label': 'Gaz naturel', 'value': 'Gaz naturel'}, {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'}, {'label': 'Fioul domestique', 'value': 'Fioul domestique'}, {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'}, {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'}, {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'}, {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'}, {'label': 'GPL', 'value': 'GPL'}, {'label': 'Propane', 'value': 'Propane'}, {'label': 'Charbon', 'value': 'Charbon'}, {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'}, {'label': 'Butane', 'value': 'Butane'}],
                    placeholder='Type d\'énergie pour l\'eau chaude sanitaire'
                ),
            ]),
            html.Div([
                html.Label('Consommation totale sur une année (en kWh)'),
                dcc.Input(id='conso-totale', type='number', placeholder='Consommation totale'),
            ]),
            html.Div([
                html.Label('Consommation chauffage sur une année (en kWh)'),
                dcc.Input(id='conso-chauffage', type='number', placeholder='Consommation chauffage'),
            ]),
            html.Div([
                html.Label('Consommation eau chaude sanitaire sur une année (en kWh)'),
                dcc.Input(id='conso-ecs', type='number', placeholder='Consommation eau chaude sanitaire'),
            ]),
            html.Button('Prédire la classe énergétique de mon logement', id='submit-button', n_clicks=0),
            html.Div(id='prediction-result')
        ])

    # Méthode pour initialiser les callbacks
    def setup_callbacks(self):

        # Callback pour afficher le contenu de l'onglet sélectionné
        @self.app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs', 'value')]
        )
        def render_content(tab):
            if tab == 'tab-1':
                return self.render_context_page()
            elif tab == 'tab-2':
                return self.render_graphs_page()
            elif tab == 'tab-3':
                return self.render_prediction_page()

        # Callback pour mettre à jour le graphique dynamique
        @self.app.callback(
            Output('dynamic-plot', 'figure'),
            [Input('x-axis', 'value'), Input('y-axis', 'value'), Input('graph-type', 'value'), Input('data-filter', 'value')]
        )
        def update_dynamic_plot(x_col, y_col, graph_type, filter_values):
            if x_col and y_col:
                filtered_df = self.df

                if filter_values:  
                    filtered_df = filtered_df[filtered_df['Etiquette_DPE'].isin(filter_values)]
                
                color_map = {
                    'A': '#479E72',
                    'B': '#6BAE5E',
                    'C': '#ADCA7D',
                    'D': '#F3E84F',
                    'E': '#E7B741',
                    'F': '#DE8647',
                    'G': '#C6362C'
                }
                category_order = {
                    'Etiquette_DPE': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                }
                if graph_type == 'scatter':
                    fig = px.scatter(filtered_df, x=x_col, y=y_col, color='Etiquette_DPE',
                                    title=f"Nuage de points ({x_col} vs {y_col}) par Etiquette DPE",
                                    color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'histogram':
                    fig = px.histogram(filtered_df, x=x_col, color='Etiquette_DPE',
                                    title=f"Histogramme de {x_col} par Etiquette DPE",
                                    color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'box':
                    fig = px.box(filtered_df, x='Etiquette_DPE', y=y_col,
                                title=f"Boîte à moustaches de {y_col} par Etiquette DPE",
                                color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'bar':
                    fig = px.bar(filtered_df, x=x_col, y=y_col, color='Etiquette_DPE',
                                title=f"Graphique en barres ({x_col} vs {y_col}) par Etiquette DPE",
                                color_discrete_map=color_map, category_orders=category_order)
                
                self.current_fig = fig  
                return fig
            return {}

        # Callback pour télécharger le graphique en PNG
        @self.app.callback(
            Output("download-link", "href"),
            Input("export-png", "n_clicks"),
            prevent_initial_call=True
        )
        def download_png(n_clicks):
            if self.current_fig:
                # Convertit la figure en PNG
                img_bytes = pio.to_image(self.current_fig, format="png")
                encoded_image = base64.b64encode(img_bytes).decode()  
                return f"data:image/png;base64,{encoded_image}"
            return ""

        # Callback pour télécharger les données en CSV
        @self.app.callback(
            Output("download-dataframe-csv-context", "data"),
            Input("export-csv-context", "n_clicks"),
            prevent_initial_call=True,
        )
        def download_csv_context(n_clicks):
            return dcc.send_data_frame(self.df.to_csv, f"data/data_69.csv", index=False)
        
        # Callback pour faire une prédiction
        @self.app.callback(
            Output('prediction-result', 'children'),
            Input('submit-button', 'n_clicks'),
            State('code-postal', 'value'),
            State('annee-construction', 'value'),
            State('type-batiment', 'value'),
            State('surface-habitable', 'value'),
            State('nombre-etage', 'value'),
            State('hauteur-plafond', 'value'),
            State('type-energie-chauffage', 'value'),
            State('type-energie-ecs', 'value'),
            State('conso-totale', 'value'),
            State('conso-chauffage', 'value'),
            State('conso-ecs', 'value')
        )
        def predict(n_clicks, code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, conso_totale, conso_chauffage, conso_ecs):
            if n_clicks > 0:
                if not all([code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, conso_totale, conso_chauffage, conso_ecs]):
                    return html.H3(f"Veuillez remplir tous les champs")
                
                data = pd.DataFrame({
                    'Code_postal_(BAN)': [code_postal],
                    'Période_construction': [annee_construction],
                    'Type_bâtiment': [type_batiment],
                    'Surface_habitable_logement': [surface_habitable],
                    'Nombre_niveau_logement': [nombre_etage],
                    'Hauteur_sous_plafond': [hauteur_plafond],
                    'Type_énergie_principale_chauffage': [type_energie_chauffage],
                    'Type_énergie_principale_ECS': [type_energie_ecs],
                    'Conso_5_usages_é_finale': [conso_totale],
                    'Conso_chauffage': [conso_chauffage],
                    'Conso_ECS_é_finale': [conso_ecs],
                    'Classe_altitude': ['inférieur à 400m'] # [TEMP] À changer par des données réelles
                })

                prediction = Model.predict(data)
                return html.H3(f"Votre logement est classé en catégorie : {prediction}"), html.Img(src=f'/assets/DPE_{prediction}.png', style={'width': '10%'})

    # Méthode pour exécuter l'interface Dash
    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)