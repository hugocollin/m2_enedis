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
    Interface Dash pour le projet Enedis
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
                dcc.Tab(label='Contexte', value='tab-1', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Données', value='tab-2', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Visualisations', value='tab-3', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Prédiction', value='tab-4', className='tab', selected_className='tab_selected'),
            ]),
            html.Div(id='tabs-content')
        ])
    
    # Méthode pour afficher la page "Contexte"
    def render_context_page(self):
        return html.Div(
            className='container',
            children=[
                html.H2("Introduction au défi"),
                html.P("Ce projet s'inscrit dans le cadre du défi proposé par Enedis, et vise à montrer le lien entre les diagnostics de performance énergétique (DPE) et les consommations réelles d'électricité des logements."),

                html.H2("Présentation du DPE"),
                html.P([
                    "Face aux défis du changement climatique et de la hausse des prix de l’énergie, la sobriété énergétique devient une priorité. Le DPE, outil central pour l'évaluation de l'efficacité énergétique des bâtiments, classe les logements de A (excellentes performances) à G (passoires énergétiques). Cette classification vise à sensibiliser les occupants et propriétaires sur les performances énergétiques et sur les travaux de rénovation nécessaires.",
                    html.Br(),
                    "De plus, certaines restrictions légales encadrent désormais la location des logements les plus énergivores (classes F et G).",
                    html.Br(),
                    "Le DPE est un outil simple permettant également d'informer les futurs locataires / acheteurs des performances énergétiques du logement et ainsi donner une indication quant aux coûts énergétiques qui lui sont associés."
                ]),

                html.Div(
                        className='image-container',
                        children=[
                            html.Img(src='/assets/images/image_DPE.jpg', className='centered-image')
                        ]
                    ),

                html.H2("Problématique et objectifs du projet"),
                html.P("Les objectifs principaux sont de quantifier l’impact des améliorations de DPE sur les économies d’énergie, et de vérifier la fiabilité des prévisions du DPE par rapport aux données réelles. L'enjeu est d'aider les particuliers et les décideurs à mieux évaluer les bénéfices d'une rénovation énergétique."),

                html.H2("Structure de l'application"),
                html.P("L'application web comporte trois pages principales :"),
                html.Ul([
                    html.Li("Page 'Contexte', présentant les objectifs du projet et le défi proposé par Enedis."),
                    html.Li("Page 'Graphiques', où l'utilisateur peut construire des graphiques interactifs pour explorer les données."),
                    html.Li("Page 'Prédiction', permettant de réaliser une prédiction de la classe DPE d'un logement en fonction d'un panel de critères.")
                ]),

                html.H2("Équipe de projet"),
                html.P("Ce projet est réalisé par trois étudiants du Master 2 SISE : Hugo Collin, Maxence Liogier et Antoine Oruezabala.")
            ]
        )

    # Méthode pour afficher la page "Données"
    def render_donnees_page(self):
        return html.Div(
            className='container',
            children=[
                html.H2('Téléchargement des données'),
                html.P("Vous pouvez télécharger les données utilisées pour ce projet en cliquant sur le bouton ci-dessous. Ces données contiennent les informations sur les logements du département du Rhône."),
                html.Button("Télécharger les données au format CSV", id="export-csv-context", n_clicks=0),
                dcc.Download(id="download-dataframe-csv-context")
            ]
        )

    # Méthode pour afficher la page "Visualisations"
    def render_visuals_page(self):
        return html.Div([
            dcc.Tabs(id="visuals-subtabs", value='subtab-1', children=[
                dcc.Tab(label='Graphiques', value='subtab-1', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Cartographie', value='subtab-2', className='tab', selected_className='tab_selected')
            ]),
            html.Div(id='visuals-tabs-content')
        ])
    
    # Méthode pour afficher la page "Graphiques"
    def render_graphs_page(self):
        return html.Div(
            className='graph_container',
            children=[
                html.H2('Types de graphique'),
                html.Div([
                    html.Div(
                        className='option-box graph-type-option',
                        id='graph-type-histogram',
                        children=[
                            html.Img(src="/assets/images/histogramme.png", className='graph-option-image'),
                            html.Span("Histogramme", className='graph-option-text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option-box graph-type-option',
                        id='graph-type-line',
                        children=[
                            html.Img(src="/assets/images/graphique_ligne.png", className='graph-option-image'),
                            html.Span("Graphique en ligne", className='graph-option-text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option-box graph-type-option',
                        id='graph-type-scatter',
                        children=[
                            html.Img(src="/assets/images/nuage_points.png", className='graph-option-image'),
                            html.Span("Nuage de points", className='graph-option-text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option-box graph-type-option',
                        id='graph-type-box',
                        children=[
                            html.Img(src="/assets/images/boite_moustache.png", className='graph-option-image'),
                            html.Span("Boîte à moustaches", className='graph-option-text')
                        ],
                        n_clicks=0
                    ),
                ], className='graph-type-container'),
                dcc.Store(id='selected-graph-type', data='histogram'),

                html.H2('Axes du graphique'),
                html.Div(
                    className='axes-container',
                    children=[
                        html.Div(
                            className='option-box dropdown-item',
                            children=[
                                html.Label("Abscisse", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='x-axis',
                                    options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Etiquette_DPE']],
                                    value="Période_construction"
                                ),
                            ]
                        ),
                        html.Div(
                            className='option-box dropdown-item',
                            children=[
                                html.Label("Ordonnée", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='y-axis',
                                    options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Etiquette_DPE']],
                                    value="Surface_habitable_logement"
                                ),
                            ]
                        ),
                    ]
                ),

                html.H2('Filtres par étiquette DPE'),
                html.Div(
                    className='filter-container',
                    children=[
                        dcc.Checklist(
                            id='data-filter',
                            options=[
                                {
                                    'label': html.Img(src='/assets/images/A.png', className='filter-icon'),
                                    'value': 'A'
                                },
                                {
                                    'label': html.Img(src='/assets/images/B.png', className='filter-icon'),
                                    'value': 'B'
                                },
                                {
                                    'label': html.Img(src='/assets/images/C.png', className='filter-icon'),
                                    'value': 'C'
                                },
                                {
                                    'label': html.Img(src='/assets/images/D.png', className='filter-icon'),
                                    'value': 'D'
                                },
                                {
                                    'label': html.Img(src='/assets/images/E.png', className='filter-icon'),
                                    'value': 'E'
                                },
                                {
                                    'label': html.Img(src='/assets/images/F.png', className='filter-icon'),
                                    'value': 'F'
                                },
                                {
                                    'label': html.Img(src='/assets/images/G.png', className='filter-icon'),
                                    'value': 'G'
                                }
                            ],
                            value=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                            inline=True,
                            className='filter-checklist'
                        ),
                    ]
                ),
                
                html.H2('Graphique dynamique'),
                dcc.Graph(id='dynamic-plot'),

                html.Button("Exporter en PNG", id="export-png", n_clicks=0),
                html.A(id="download-link", download="graph.png", children="")
            ]
        )
    
    # Méthode pour afficher la page "Cartographie"
    def render_carto_page(self):
        return html.Div(
            className='container',
            children=[
                html.P('⌛ La cartographie interactive sera disponible prochainement ⌛', style={'font-style':'italic', 'text-align':'center'}),
            ]
        )

    # Méthode pour afficher la page "Prédiction"
    def render_prediction_page(self):
        return html.Div([
            dcc.Tabs(id="prediction-subtabs", value='subtab-1', children=[
                dcc.Tab(label='Prédiction du DPE', value='subtab-1', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Prédiction de la consomation', value='subtab-2', className='tab', selected_className='tab_selected')
            ]),
            html.Div(id='prediction-tabs-content')
        ])
    
    # Méthode pour afficher la page "Prédiction du DPE"
    def render_prediction_page_dpe(self):
        return html.Div(
            className='container',
            children=[
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
                    html.Label('Consommation totale sur une année (en kW)'),
                    dcc.Input(id='conso-totale', type='number', placeholder='Consommation totale'),
                ]),
                html.Div([
                    html.Label('Consommation chauffage sur une année (en kW)'),
                    dcc.Input(id='conso-chauffage', type='number', placeholder='Consommation chauffage'),
                ]),
                html.Div([
                    html.Label('Consommation eau chaude sanitaire sur une année (en kW)'),
                    dcc.Input(id='conso-ecs', type='number', placeholder='Consommation eau chaude sanitaire'),
                ]),
                html.Button('Prédire la classe énergétique de mon logement', id='submit-button', n_clicks=0),
                html.Div(id='prediction-result')
            ]
        )
    
    # Méthode pour afficher la page "Prédiction de la consommation"
    def render_prediction_page_conso(self):
        return html.Div(
            className='container',
            children=[
                html.P('⌛ La prédiction de la consommation sera disponible prochainement ⌛', style={'font-style':'italic', 'text-align':'center'}),
            ]
        )

    # Méthode pour initialiser les callbacks
    def setup_callbacks(self):

        # Callback pour afficher le contenu de l'onglet sélectionné
        @self.app.callback(
            Output('tabs-content', 'children'),
            [Input('tabs', 'value')]
        )
        # Méthode pour afficher le contenu de l'onglet sélectionné
        def render_content(tab):
            if tab == 'tab-1':
                return self.render_context_page()
            elif tab == 'tab-2':
                return self.render_donnees_page()
            elif tab == 'tab-3':
                return self.render_visuals_page()
            elif tab == 'tab-4':
                return self.render_prediction_page()
            
        # Callback pour télécharger les données en CSV
        @self.app.callback(
            Output("download-dataframe-csv-context", "data"),
            Input("export-csv-context", "n_clicks"),
            prevent_initial_call=True,
        )
        # Méthode pour télécharger les données en CSV
        def download_csv_context(n_clicks):
            return dcc.send_data_frame(self.df.to_csv, f"data/data_69.csv", index=False)
        
        # Callback pour mettre à jour le type de graphique sélectionné
        @self.app.callback(
            Output('selected-graph-type', 'data'),
            [Input('graph-type-histogram', 'n_clicks'),
            Input('graph-type-line', 'n_clicks'),
            Input('graph-type-scatter', 'n_clicks'),
            Input('graph-type-box', 'n_clicks')],
            [State('selected-graph-type', 'data')]
        )
        # Méthode pour mettre à jour le type de graphique sélectionné
        def update_graph_type(n_hist, n_line, n_scatter, n_box, current_type):
            ctx = dash.callback_context

            if not ctx.triggered:
                return current_type
            else:
                button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                if button_id == 'graph-type-histogram':
                    return 'histogram'
                elif button_id == 'graph-type-line':
                    return 'line'
                elif button_id == 'graph-type-scatter':
                    return 'scatter'
                elif button_id == 'graph-type-box':
                    return 'box'
            return current_type

        # Callback pour mettre à jour le graphique dynamique
        @self.app.callback(
            Output('dynamic-plot', 'figure'),
            [
                Input('x-axis', 'value'), 
                Input('y-axis', 'value'), 
                Input('selected-graph-type', 'data'), 
                Input('data-filter', 'value'),
            ]
        )
        # Méthode pour mettre à jour le graphique dynamique
        def update_dynamic_plot(x_col, y_col, graph_type, filter_values):
            if x_col and y_col:
                filtered_df = self.df

                if filter_values:  
                    filtered_df = filtered_df[filtered_df['Etiquette_DPE'].isin(filter_values)]

                filtered_df = filtered_df.sort_values(by=x_col, ascending=True)
                
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
                elif graph_type == 'line':
                    fig = px.line(filtered_df, x=x_col, y=y_col, color='Etiquette_DPE',
                                title=f"Graphique en ligne ({x_col} vs {y_col}) par Etiquette DPE",
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
        # Méthode pour télécharger le graphique en PNG
        def download_png(n_clicks):
            if self.current_fig:
                # Convertit la figure en PNG
                img_bytes = pio.to_image(self.current_fig, format="png")
                encoded_image = base64.b64encode(img_bytes).decode()  
                return f"data:image/png;base64,{encoded_image}"
            return ""
        
        # Callback pour afficher le contenu de l'onglet sélectionné dans la page "Visualisations"
        @self.app.callback(
            Output('visuals-tabs-content', 'children'),
            [Input('visuals-subtabs', 'value')]
        )
        # Méthode pour afficher le contenu de l'onglet sélectionné dans la page "Visualisations"
        def render_visual_subtabs(subtab):
            if subtab == 'subtab-1':
                return self.render_graphs_page()
            elif subtab == 'subtab-2':
                return self.render_carto_page()
        
        # Callback pour afficher le contenu de l'onglet sélectionné dans la page "Prédictions"
        @self.app.callback(
            Output('prediction-tabs-content', 'children'),
            [Input('prediction-subtabs', 'value')]
        )
        # Méthode pour afficher le contenu de l'onglet sélectionné dans la page "Prédictions" 
        def render_prediction_subtabs(subtab):
            if subtab == 'subtab-1':
                return self.render_prediction_page_dpe()
            elif subtab == 'subtab-2':
                return self.render_prediction_page_conso()
        
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
        # Méthode pour faire une prédiction
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
                    'Conso_ECS_é_finale': [conso_ecs]
                })

                prediction = Model.predict(data)
                return (
                    html.H3(f"Votre logement est classé en catégorie : {prediction}"),
                    html.Div(
                        className='image-container',
                        children=[
                            html.Img(src=f'/assets/images/DPE_{prediction}.png', className='centered-image')
                        ]
                    )
                )

    # Méthode pour exécuter l'interface Dash
    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)