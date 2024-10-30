# Importation des librairies nécessaires
import os
import dash
from dash import html, dash_table

class DashInterface:
    def __init__(self, dataframe):
        self.df = dataframe
        self.app = dash.Dash(__name__)
        self.server = self.app.server
        self.setup_layout()

    def setup_layout(self):
        self.app.layout = html.Div(children=[
            html.H1(children='Résultats de Machine Learning'),

            html.Div(children='''
                Visualisation des données récupérées.
            '''),

            # dash_table.DataTable(
            #     id='table',
            #     columns=[{"name": i, "id": i} for i in self.df.columns],
            #     data=self.df.to_dict('records'),
            # )
        ])

    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)