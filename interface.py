from api import API
from model import Model

import dash
from dash import html, dcc, dash_table
from dash.dependencies import Input, Output, State
import io
import os
import pandas as pd
import plotly.express as px

class DashInterface:
    """
    Interface Dash pour le projet Enedis
    """

    # Constructeur de la classe
    def __init__(self):
        self.app = dash.Dash(__name__, external_stylesheets=['/assets/style.css'])
        self.app.title = "Projet Enedis"
        self.server = self.app.server
        self.df = pd.read_csv('assets/data_69.csv', sep='|')
        self.current_fig = None
        self.setup_layout()
        self.setup_callbacks()

    # Fonction d'affichage de l'interface
    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Contexte', value='tab-1', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Modèles', value='tab-2', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Visualisations', value='tab-3', className='tab', selected_className='tab_selected'),
                dcc.Tab(label='Prédictions', value='tab-4', className='tab', selected_className='tab_selected'),
            ]),
            html.Div(id='tabs-content')
        ])
    
    # Fonction de la page "Contexte"
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
                        className='image_container',
                        children=[
                            html.Img(src='/assets/images/image_DPE.jpg', className='centered_image')
                        ]
                    ),

                html.H2("Problématique et objectifs du projet"),
                html.P("Les objectifs principaux sont de quantifier l’impact des améliorations de DPE sur les économies d’énergie, et de vérifier la fiabilité des prévisions du DPE par rapport aux données réelles. L'enjeu est d'aider les particuliers et les décideurs à mieux évaluer les bénéfices d'une rénovation énergétique."),

                html.H2("Structure de l'application"),
                html.P("L'application web comporte trois pages principales :"),
                html.Ul([
                    html.Li("Page 'Contexte', présentant les objectifs du projet et le défi proposé par Enedis."),
                    html.Li("Page 'Modèles', permettant le téléchargement des données, le chargement de nouvelles données et le réentraînement du modèle."),
                    html.Li("Page 'Visualisations', proposant des visuels interactifs pour explorer les données."),
                    html.Li("Page 'Prédictions', permettant de prédire la classe énergétique d'un logement et sa consommation d'énergie.")
                ]),

                html.H2("Équipe de projet"),
                html.P("Ce projet est réalisé par trois étudiants du Master 2 SISE : Hugo Collin, Maxence Liogier et Antoine Oruezabala.")
            ]
        )

    # Fonction de la page "Modèles"
    def render_model_page(self):
        return html.Div(
            className='model_container',
            children=[
                html.Div(
                    className='model_subcontainer',
                    children=[
                        html.H2('API de l\'Ademe'),
                        html.P("Permet de charger de nouvelles données de logements, en utilisant l'API de l'Ademe."),
                        html.P("Attention : ce bouton ne marche qu'en version locale", style={'font-style':'italic', 'color':'red'}),
                        html.Button("Actualiser les données", id="btn-refresh-data", n_clicks=0, className='ui_button'),
                        html.P(id='refresh-api-status', style={'margin-top': '10px', 'color': 'green'})
                    ]
                ),
                html.Div(
                    className='model_subcontainer',
                    children=[
                        html.H2('Réentraînement des modèles de prédiction'),
                        html.P("Permet de réentraîner les modèle de prédiction du DPE et de la consommation avec les nouvelles données."),
                        html.P("Attention : ce bouton ne marche qu'en version locale et peut prendre un certain moment.", style={'font-style':'italic', 'color':'red'}),
                        html.Button("Réentraîner les modèles de prédiction", id="btn-refresh-models", n_clicks=0, className='ui_button'),
                        html.P(id='refresh-models-status', style={'margin-top': '10px', 'color': 'green'})
                    ]
                )
            ]
        )

    # Fonction de la page "Visualisations"
    def render_visuals_page(self):
        return html.Div([
            html.Div(
                className='subtabs_container',
                children=[
                    dcc.Tabs(
                        id="visuals-subtabs",
                        value='subtab-1',
                        children=[
                            dcc.Tab(label='Tableau', value='subtab-1', className='subtab_visuals', selected_className='tab_selected'),
                            dcc.Tab(label='Statistiques', value='subtab-2', className='subtab_visuals', selected_className='tab_selected'),
                            dcc.Tab(label='Graphiques', value='subtab-3', className='subtab_visuals', selected_className='tab_selected'),
                            dcc.Tab(label='Cartographie', value='subtab-4', className='subtab_visuals', selected_className='tab_selected')
                        ],
                    )
                ]
            ),
            html.Div(id='visuals-tabs-content')
        ])
    
    # Fonction de la sous page "Tableau"
    def render_tab_page(self):
        return html.Div(
            className='visuals_container',
            children=[
                html.H2('Tableau dynamique'),
                dash_table.DataTable(
                    id='data-table',
                    columns=[{'name': col, 'id': col} for col in self.df.columns],
                    data=[],
                    page_current=0,
                    page_size=100,
                    page_action='custom',
                    virtualization=True,
                    fixed_rows={'headers': True},
                    style_as_list_view=True,
                    style_cell={
                        'width': '250px',
                        'whiteSpace': 'nowrap',
                        'textOverflow': 'ellipsis'
                    }
                ),

                html.Button("Télécharger les données", id="btn-download-data", n_clicks=0, className='ui_button'),
                dcc.Download(id="download-data")
            ]
        )
    
    #  Fonction de la sous page "Statistiques"
    def render_stats_page(self):
        return html.Div(
            className='visuals_container',
            children=[
                html.H2('Filtres'),
                html.Div(
                    className='subcontainer',
                    children=[
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Communes", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='filter-nom-commune',
                                    options=[{'label': val, 'value': val} for val in self.df['Nom commune'].unique()],
                                    multi=True,
                                    placeholder='Sélectionnez une ou plusieurs valeurs'
                                ),
                            ]
                        ),
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Type de batiments", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='filter-type-batiment',
                                    options=[
                                        {'label': 'Maison', 'value': 'maison'},
                                        {'label': 'Appartement', 'value': 'appartement'},
                                        {'label': 'Immeuble', 'value': 'immeuble'}
                                    ],
                                    multi=True,
                                    placeholder='Sélectionnez une ou plusieurs valeurs'
                                ),
                            ]
                        ),
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Type d\'énergie du chauffage", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='filter-type-energie-chauffage',
                                    options=[
                                        {'label': 'Électricité', 'value': 'Électricité'},
                                        {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                        {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                        {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                        {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                        {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                        {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                        {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                        {'label': 'GPL', 'value': 'GPL'},
                                        {'label': 'Propane', 'value': 'Propane'},
                                        {'label': 'Charbon', 'value': 'Charbon'},
                                        {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                        {'label': 'Butane', 'value': 'Butane'}
                                    ],
                                    multi=True,
                                    placeholder='Sélectionnez une ou plusieurs valeurs'
                                ),
                            ]
                        ),
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Type d\'énergie pour l\'eau chaude sanitaire", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='filter-type-energie-ecs',
                                    options=[
                                        {'label': 'Électricité', 'value': 'Électricité'},
                                        {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                        {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                        {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                        {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                        {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                        {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                        {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                        {'label': 'GPL', 'value': 'GPL'},
                                        {'label': 'Propane', 'value': 'Propane'},
                                        {'label': 'Charbon', 'value': 'Charbon'},
                                        {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                        {'label': 'Butane', 'value': 'Butane'}
                                    ],
                                    multi=True,
                                    placeholder='Sélectionnez une ou plusieurs valeurs'
                                ),
                            ]
                        ),
                    ]
                ),

                html.H2('Indicateurs clés de performance'),
                html.Div(
                    className='stats_boxes_container',
                    id='statistics-output',
                    children=[]
                )
            ]
        )
    
    # Fonction pour afficher la sous page "Graphiques"
    def render_graphs_page(self):
        return html.Div(
            className='visuals_container',
            children=[
                html.H2('Types de graphique'),
                html.Div([
                    html.Div(
                        className='option_box graph_type_option',
                        id='graph-type-histogram',
                        children=[
                            html.Img(src="/assets/images/histogramme.png", className='graph_option_image'),
                            html.Span("Histogramme", className='graph_option_text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option_box graph_type_option',
                        id='graph-type-line',
                        children=[
                            html.Img(src="/assets/images/graphique_ligne.png", className='graph_option_image'),
                            html.Span("Graphique en ligne", className='graph_option_text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option_box graph_type_option',
                        id='graph-type-scatter',
                        children=[
                            html.Img(src="/assets/images/nuage_points.png", className='graph_option_image'),
                            html.Span("Nuage de points", className='graph_option_text')
                        ],
                        n_clicks=0
                    ),
                    html.Div(
                        className='option_box graph_type_option',
                        id='graph-type-box',
                        children=[
                            html.Img(src="/assets/images/boite_moustache.png", className='graph_option_image'),
                            html.Span("Boîte à moustaches", className='graph_option_text')
                        ],
                        n_clicks=0
                    ),
                ], className='subcontainer'),
                dcc.Store(id='selected-graph-type', data='histogram'),

                html.H2('Axes du graphique'),
                html.Div(
                    className='subcontainer',
                    children=[
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Abscisse", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='x-axis',
                                    options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Étiquette DPE']],
                                    value="Période construction"
                                ),
                            ]
                        ),
                        html.Div(
                            className='option_box dropdown_item',
                            children=[
                                html.Label("Ordonnée", className='dropdown-label'),
                                dcc.Dropdown(
                                    id='y-axis',
                                    options=[{'label': col, 'value': col} for col in self.df.columns if col not in ['Étiquette DPE']],
                                    value="Surface habitable logement"
                                ),
                            ]
                        ),
                    ]
                ),

                html.H2('Filtres par étiquette DPE'),
                html.Div(
                    className='filter_container',
                    children=[
                        dcc.Checklist(
                            id='data-filter',
                            options=[
                                {
                                    'label': html.Img(src='/assets/images/A.png', className='filter_icon'),
                                    'value': 'A'
                                },
                                {
                                    'label': html.Img(src='/assets/images/B.png', className='filter_icon'),
                                    'value': 'B'
                                },
                                {
                                    'label': html.Img(src='/assets/images/C.png', className='filter_icon'),
                                    'value': 'C'
                                },
                                {
                                    'label': html.Img(src='/assets/images/D.png', className='filter_icon'),
                                    'value': 'D'
                                },
                                {
                                    'label': html.Img(src='/assets/images/E.png', className='filter_icon'),
                                    'value': 'E'
                                },
                                {
                                    'label': html.Img(src='/assets/images/F.png', className='filter_icon'),
                                    'value': 'F'
                                },
                                {
                                    'label': html.Img(src='/assets/images/G.png', className='filter_icon'),
                                    'value': 'G'
                                }
                            ],
                            value=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                            inline=True,
                            className='filter_checklist'
                        ),
                    ]
                ),
                
                html.H2('Graphique dynamique'),
                dcc.Graph(id='dynamic-plot'),

                html.Button("Télécharger le graphique", id="btn-download-graph", n_clicks=0, className='ui_button'),
                dcc.Download(id="download-graph")
            ]
        )
    
    # Fonction pour afficher la sous page "Cartographie"
    def render_carto_page(self):
        return html.Div(
            className='visuals_container',
            children=[
                html.H2('Carte dynamique de la répartition des étiquettes DPE'),
                html.P('Pour des raisons de performances au maximum 100 000 points sont affichés', style={'font-style':'italic', 'text-align':'center'}),
                html.Div([
                    dcc.Checklist(
                        id='data-filter',
                        options=[
                            {
                                'label': html.Img(src='/assets/images/A.png', className='filter_icon'),
                                'value': 'A'
                            },
                            {
                                'label': html.Img(src='/assets/images/B.png', className='filter_icon'),
                                'value': 'B'
                            },
                            {
                                'label': html.Img(src='/assets/images/C.png', className='filter_icon'),
                                'value': 'C'
                            },
                            {
                                'label': html.Img(src='/assets/images/D.png', className='filter_icon'),
                                'value': 'D'
                            },
                            {
                                'label': html.Img(src='/assets/images/E.png', className='filter_icon'),
                                'value': 'E'
                            },
                            {
                                'label': html.Img(src='/assets/images/F.png', className='filter_icon'),
                                'value': 'F'
                            },
                            {
                                'label': html.Img(src='/assets/images/G.png', className='filter_icon'),
                                'value': 'G'
                            }
                        ],
                        value=['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                        inline=True,
                        className='filter_checklist'
                    ),
                ], className='filter_container'),
                dcc.Graph(id='map-plotly')
            ]
        )

    # Fonction pour afficher la page "Prédiction"
    def render_prediction_page(self):
        return html.Div([
            html.Div(
                className='subtabs_container',
                children=[
                    dcc.Tabs(
                        id="prediction-subtabs",
                        value='subtab-1',
                        children=[
                            dcc.Tab(label='Prédiction de la classe énergétique', value='subtab-1', className='subtab_predict', selected_className='tab_selected'),
                            dcc.Tab(label='Prédiction de la consomation', value='subtab-2', className='subtab_predict', selected_className='tab_selected')
                        ],
                    )
                ]
            ),
            html.Div(id='prediction-tabs-content')
        ])
    
    # Fonction pour afficher la sous page "Prédiction de la classe énergétique"
    def render_dpe_prediction_page(self):
        return html.Div(
            className='form_container',
            children=[
                html.H2('Informations générales sur le logement'),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Code postal'),
                        dcc.Input(id='code-postal', type='text', placeholder='Code postal'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Année de construction'),
                        dcc.Input(id='annee-construction', type='number', placeholder='Année de construction'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type de logement'),
                        dcc.Dropdown(
                            id='type-batiment',
                            options=[
                                {'label': 'Maison', 'value': 'maison'},
                                {'label': 'Appartement', 'value': 'appartement'},
                                {'label': 'Immeuble', 'value': 'immeuble'}
                            ],
                            placeholder='Type de logement'
                        ),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Surface habitable (en m²)'),
                        dcc.Input(id='surface-habitable', type='number', placeholder='Surface habitable'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Nombre d\'étage(s)'),
                        dcc.Input(id='nombre-etage', type='number', placeholder='Nombre d\'étage(s)'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Hauteur sous plafond (en m)'),
                        dcc.Input(id='hauteur-plafond', type='number', placeholder='Hauteur sous plafond'),
                    ]
                ),

                html.H2('Informations de consommation du logement'),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type d\'énergie du chauffage'),
                        dcc.Dropdown(
                            id='type-energie-chauffage',
                            options=[
                                {'label': 'Électricité', 'value': 'Électricité'},
                                {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                {'label': 'GPL', 'value': 'GPL'},
                                {'label': 'Propane', 'value': 'Propane'},
                                {'label': 'Charbon', 'value': 'Charbon'},
                                {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                {'label': 'Butane', 'value': 'Butane'}
                            ],
                            placeholder='Type d\'énergie du chauffage'
                        ),
                    ]
                ),

                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type d\'énergie pour l\'eau chaude sanitaire'),
                        dcc.Dropdown(
                            id='type-energie-ecs',
                            options=[
                                {'label': 'Électricité', 'value': 'Électricité'},
                                {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                {'label': 'GPL', 'value': 'GPL'},
                                {'label': 'Propane', 'value': 'Propane'},
                                {'label': 'Charbon', 'value': 'Charbon'},
                                {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                {'label': 'Butane', 'value': 'Butane'}
                            ],
                            placeholder='Type d\'énergie pour l\'eau chaude sanitaire'
                        ),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Consommation totale sur une année (en kWh)'),
                        dcc.Input(id='conso-totale', type='number', placeholder='Consommation totale'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Consommation chauffage sur une année (en kWh)'),
                        dcc.Input(id='conso-chauffage', type='number', placeholder='Consommation chauffage'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Consommation eau chaude sanitaire sur une année (en kWh)'),
                        dcc.Input(id='conso-ecs', type='number', placeholder='Consommation eau chaude sanitaire'),
                    ]
                ),

                html.Button('Prédire la classe énergétique de mon logement', id='dpe-submit-button', n_clicks=0, className='ui_button'),

                html.Div(id='dpe-prediction-result')
            ]
        )
    
    # Fonction pour afficher la sous page "Prédiction de la consommation"
    def render_conso_prediction_page(self):
        return html.Div(
            className='form_container',
            children=[
                html.H2('Informations générales sur le logement'),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Code postal'),
                        dcc.Input(id='code-postal', type='text', placeholder='Code postal'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Année de construction'),
                        dcc.Input(id='annee-construction', type='number', placeholder='Année de construction'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type de logement'),
                        dcc.Dropdown(
                            id='type-batiment',
                            options=[
                                {'label': 'Maison', 'value': 'maison'},
                                {'label': 'Appartement', 'value': 'appartement'},
                                {'label': 'Immeuble', 'value': 'immeuble'}
                            ],
                            placeholder='Type de logement'
                        ),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Surface habitable (en m²)'),
                        dcc.Input(id='surface-habitable', type='number', placeholder='Surface habitable'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Nombre d\'étage(s)'),
                        dcc.Input(id='nombre-etage', type='number', placeholder='Nombre d\'étage(s)'),
                    ]
                ),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Hauteur sous plafond (en m)'),
                        dcc.Input(id='hauteur-plafond', type='number', placeholder='Hauteur sous plafond'),
                    ]
                ),

                html.H2('Informations énergétiques du logement'),
                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type d\'énergie du chauffage'),
                        dcc.Dropdown(
                            id='type-energie-chauffage',
                            options=[
                                {'label': 'Électricité', 'value': 'Électricité'},
                                {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                {'label': 'GPL', 'value': 'GPL'},
                                {'label': 'Propane', 'value': 'Propane'},
                                {'label': 'Charbon', 'value': 'Charbon'},
                                {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                {'label': 'Butane', 'value': 'Butane'}
                            ],
                            placeholder='Type d\'énergie du chauffage'
                        ),
                    ]
                ),

                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Type d\'énergie pour l\'eau chaude sanitaire'),
                        dcc.Dropdown(
                            id='type-energie-ecs',
                            options=[
                                {'label': 'Électricité', 'value': 'Électricité'},
                                {'label': 'Gaz naturel', 'value': 'Gaz naturel'},
                                {'label': 'Réseau de chauffage urbain', 'value': 'Réseau de Chauffage urbain'},
                                {'label': 'Fioul domestique', 'value': 'Fioul domestique'},
                                {'label': 'Bois – Bûches', 'value': 'Bois – Bûches'},
                                {'label': 'Bois – Granulés (pellets) ou briquettes', 'value': 'Bois – Granulés (pellets) ou briquettes'},
                                {'label': 'Bois – Plaquettes forestières', 'value': 'Bois – Plaquettes forestières'},
                                {'label': 'Bois – Plaquettes d’industrie', 'value': 'Bois – Plaquettes d’industrie'},
                                {'label': 'GPL', 'value': 'GPL'},
                                {'label': 'Propane', 'value': 'Propane'},
                                {'label': 'Charbon', 'value': 'Charbon'},
                                {'label': 'Électricité d\'origine renouvelable utilisée dans le bâtiment', 'value': 'Électricité d\'origine renouvelable utilisée dans le bâtiment'},
                                {'label': 'Butane', 'value': 'Butane'}
                            ],
                            placeholder='Type d\'énergie pour l\'eau chaude sanitaire'
                        ),
                    ]
                ),

                html.Div(
                    className='field_box',
                    children=[
                        html.Label('Classe énergétique'),
                        dcc.Dropdown(id='classe-energetique', options=['A', 'B', 'C', 'D', 'E', 'F', 'G'], placeholder='Classe énergétique'),
                    ]
                ),

                html.Button('Prédire la consommation de mon logement', id='conso-submit-button', n_clicks=0, className='ui_button'),

                html.Div(id='conso-prediction-result')
            ]
        )

    # Fonction pour les callbacks de l'interface
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
                return self.render_model_page()
            elif tab == 'tab-3':
                return self.render_visuals_page()
            elif tab == 'tab-4':
                return self.render_prediction_page()
            
        # Callback pour actualiser les données de l'API
        @self.app.callback(
            Output('refresh-api-status', 'children'),
            Input('btn-refresh-data', 'n_clicks'),
            prevent_initial_call=True
        )
        def refresh_data(n_clicks):
            if n_clicks:
                api = API()
                api.get_data()
                return "Données actualisées"
            return ""
        
        # Callback pour réentraîner les modèles de prédiction
        @self.app.callback(
            Output('refresh-models-status', 'children'),
            Input('btn-refresh-models', 'n_clicks'),
            prevent_initial_call=True
        )
        def refresh_models(n_clicks):
            if n_clicks:
                model = Model()
                model.train_models()
                return "Modèles réentraînés"
            return ""
        
        # Callback pour afficher le contenu de l'onglet sélectionné dans la page "Visualisations"
        @self.app.callback(
            Output('visuals-tabs-content', 'children'),
            [Input('visuals-subtabs', 'value')]
        )
        def render_visual_subtabs(subtab):
            if subtab == 'subtab-1':
                return self.render_tab_page()
            elif subtab == 'subtab-2':
                return self.render_stats_page()
            elif subtab == 'subtab-3':
                return self.render_graphs_page()
            elif subtab == 'subtab-4':
                return self.render_carto_page()
        
        # Callback pour afficher uniquement la page demandée dans le tableau
        @self.app.callback(
            Output('data-table', 'data'),
            Input('data-table', 'page_current'),
            Input('data-table', 'page_size'),
            State('data-table', 'data')
        )
        def update_table(page_current, page_size, existing_data):
            start = page_current * page_size
            end = start + page_size
            page_data = self.df.iloc[start:end].to_dict('records')

            return page_data
        
        # Callback pour télécharger les données en CSV
        @self.app.callback(
            Output("download-data", "data"),
            Input("btn-download-data", "n_clicks"),
            prevent_initial_call=True,
        )
        def download_csv(n_clicks):
            if n_clicks:
                return dcc.send_file('assets/data_69.csv')
        
        # Dictionnaire des libellés des indicateurs
        COLUMN_LABELS = {
            'Consommation totale': 'consommation totale',
            'Consommation chauffage': 'consommation du chauffage',
            'Consommation ECS': 'consommation de l\'eau chaude sanitaire'
        }

        # Callback pour mettre à jour les statistiques
        @self.app.callback(
            Output('statistics-output', 'children'),
            [
                Input('filter-nom-commune', 'value'),
                Input('filter-type-batiment', 'value'),
                Input('filter-type-energie-chauffage', 'value'),
                Input('filter-type-energie-ecs', 'value')
            ]
        )
        def update_statistics(filter_commune, filter_batiment, filter_energie_ecs, filter_energie_chauffage):
            filtered_df = self.df

            if filter_commune:
                filtered_df = filtered_df[filtered_df['Nom commune'].isin(filter_commune)]
            if filter_batiment:
                filtered_df = filtered_df[filtered_df['Type bâtiment'].isin(filter_batiment)]
            if filter_energie_chauffage:
                filtered_df = filtered_df[filtered_df['Type énergie chauffage'].isin(filter_energie_chauffage)]
            if filter_energie_ecs:
                filtered_df = filtered_df[filtered_df['Type énergie ECS'].isin(filter_energie_ecs)]

            stats = {}
            for col in COLUMN_LABELS.keys():
                stats[col] = {
                    'moyenne': filtered_df[col].mean(),
                    'écart-type': filtered_df[col].std(),
                    'somme': filtered_df[col].sum(),
                    'min': filtered_df[col].min(),
                    'max': filtered_df[col].max(),
                }

            stats_output = []
            for col, col_stats in stats.items():
                stats_output.append(html.Div(
                className='stats_box',
                children=[
                    html.H4(f"Statistiques de la {COLUMN_LABELS[col]} (en kWh/an)"),
                    html.P(f"Moyenne : {col_stats['moyenne']:.2f}"),
                    html.P(f"Écart-type : {col_stats['écart-type']:.2f}"),
                    html.P(f"Somme : {col_stats['somme']:.2f}"),
                    html.P(f"Min : {col_stats['min']:.2f}"),
                    html.P(f"Max : {col_stats['max']:.2f}")
                ]
            ))

            return stats_output
        
        # Callback pour mettre à jour le type de graphique sélectionné
        @self.app.callback(
            Output('selected-graph-type', 'data'),
            [Input('graph-type-histogram', 'n_clicks'),
            Input('graph-type-line', 'n_clicks'),
            Input('graph-type-scatter', 'n_clicks'),
            Input('graph-type-box', 'n_clicks')],
            [State('selected-graph-type', 'data')]
        )
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
        def update_dynamic_plot(x_col, y_col, graph_type, filter_values):
            if x_col and y_col:
                filtered_df = self.df

                if filter_values:  
                    filtered_df = filtered_df[filtered_df['Étiquette DPE'].isin(filter_values)]

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
                    'Étiquette DPE': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                }
                if graph_type == 'scatter':
                    fig = px.scatter(filtered_df, x=x_col, y=y_col, color='Étiquette DPE',
                                    title=f"Nuage de points ({x_col} vs {y_col}) par Étiquette DPE",
                                    color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'histogram':
                    fig = px.histogram(filtered_df, x=x_col, color='Étiquette DPE',
                                    title=f"Histogramme de {x_col} par Étiquette DPE",
                                    color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'box':
                    fig = px.box(filtered_df, x='Étiquette DPE', y=y_col,
                                title=f"Boîte à moustaches de {y_col} par Étiquette DPE",
                                color_discrete_map=color_map, category_orders=category_order)
                elif graph_type == 'line':
                    fig = px.line(filtered_df, x=x_col, y=y_col, color='Étiquette DPE',
                                title=f"Graphique en ligne ({x_col} vs {y_col}) par Étiquette DPE",
                                color_discrete_map=color_map, category_orders=category_order)

                self.current_fig = fig
                return fig
            return {}
        
        # Callback pour télécharger le graphique en PNG
        @self.app.callback(
            Output("download-graph", "data"),
            Input("btn-download-graph", "n_clicks"),
            prevent_initial_call=True,
        )
        def download_graph_as_png(n_clicks):
            if n_clicks:
                if self.current_fig:
                    buffer = io.BytesIO()
                    self.current_fig.write_image(buffer, format="png")
                    buffer.seek(0)
                    return dcc.send_bytes(buffer.read(), "graphique.png")

        # Callback pour mettre à jour la carte 
        @self.app.callback(
            Output('map-plotly', 'figure'),
            [
                Input('visuals-subtabs', 'value'),
                Input('data-filter', 'value')
            ]
        )
        def generate_map_plotly(subtabs_value, selected_dpe):
            if subtabs_value != 'subtab-4':
                return dash.no_update

            data = self.df.copy()

            if len(data) > 100000:
                data = data.sample(100000, random_state=None)

            if selected_dpe:
                data = data[data['Étiquette DPE'].isin(selected_dpe)]

            fig = px.scatter_mapbox(
                data,
                lat='Latitude',
                lon='Longitude',
                hover_name='Nom commune',
                hover_data={
                    'Code postal': True,
                    'Étiquette DPE': True,
                    'Latitude': False,
                    'Longitude': False
                },
                color='Étiquette DPE',
                color_discrete_map={
                    'A': '#479E72',
                    'B': '#6BAE5E',
                    'C': '#ADCA7D',
                    'D': '#F3E84F',
                    'E': '#E7B741',
                    'F': '#DE8647',
                    'G': '#C6362C'
                },
                category_orders={
                    'Étiquette DPE': ['A', 'B', 'C', 'D', 'E', 'F', 'G']
                },
                zoom=10,
                height=600,
            )

            fig.update_layout(
                mapbox_style="carto-positron",
                margin={"r":0,"t":50,"l":0,"b":0}
            )
            self.current_fig = fig
            return fig
        
        # Callback pour afficher le contenu de l'onglet sélectionné dans la page "Prédictions"
        @self.app.callback(
            Output('prediction-tabs-content', 'children'),
            [Input('prediction-subtabs', 'value')]
        ) 
        def render_prediction_subtabs(subtab):
            if subtab == 'subtab-1':
                return self.render_dpe_prediction_page()
            elif subtab == 'subtab-2':
                return self.render_conso_prediction_page()
        
        # Callback pour faire la prédiction de la classe énergétique
        @self.app.callback(
            Output('dpe-prediction-result', 'children'),
            Input('dpe-submit-button', 'n_clicks'),
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
        def predict_dpe(n_clicks, code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, conso_totale, conso_chauffage, conso_ecs):
            if n_clicks > 0:
                if not all([code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, conso_totale, conso_chauffage, conso_ecs]):
                    return html.H3(f"Veuillez remplir tous les champs", style={'color':'red'})
                
                data = pd.DataFrame({
                    'Code postal': [code_postal],
                    'Période construction': [annee_construction],
                    'Type bâtiment': [type_batiment],
                    'Surface habitable logement': [surface_habitable],
                    'Nombre niveau logement': [nombre_etage],
                    'Hauteur sous-plafond': [hauteur_plafond],
                    'Type énergie chauffage': [type_energie_chauffage],
                    'Type énergie ECS': [type_energie_ecs],
                    'Consommation totale': [conso_totale],
                    'Conso_chauffage': [conso_chauffage],
                    'Consommation ECS': [conso_ecs]
                })

                prediction = Model.predict_DPE(data)
                return (
                    html.H3(f"Votre logement est classé en catégorie : {prediction}"),
                    html.Div(
                        className='image_container',
                        children=[
                            html.Img(src=f'/assets/images/DPE_{prediction}.png', className='centered_image')
                        ]
                    )
                )
            
        # Callback pour faire la prédiction de la consommation
        @self.app.callback(
            Output('conso-prediction-result', 'children'),
            Input('conso-submit-button', 'n_clicks'),
            State('code-postal', 'value'),
            State('annee-construction', 'value'),
            State('type-batiment', 'value'),
            State('surface-habitable', 'value'),
            State('nombre-etage', 'value'),
            State('hauteur-plafond', 'value'),
            State('type-energie-chauffage', 'value'),
            State('type-energie-ecs', 'value'),
            State('classe-energetique', 'value')
        )
        def predict_conso(n_clicks, code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, classe_energetique):
            if n_clicks > 0:
                if not all([code_postal, annee_construction, type_batiment, surface_habitable, nombre_etage, hauteur_plafond, type_energie_chauffage, type_energie_ecs, classe_energetique]):
                    return html.H3(f"Veuillez remplir tous les champs", style={'color':'red'})
                
                data = pd.DataFrame({
                    'Code postal': [code_postal],
                    'Période construction': [annee_construction],
                    'Type bâtiment': [type_batiment],
                    'Surface habitable logement': [surface_habitable],
                    'Nombre niveau logement': [nombre_etage],
                    'Hauteur sous-plafond': [hauteur_plafond],
                    'Type énergie chauffage': [type_energie_chauffage],
                    'Type énergie ECS': [type_energie_ecs],
                    'Étiquette DPE': [classe_energetique]
                })

                prediction = Model.predict_conso(data)
                return html.H3(f"La consommation totale de votre logement est d'environ : {prediction:.2f} kWh/an")

    # Méthode pour exécuter l'interface Dash
    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)