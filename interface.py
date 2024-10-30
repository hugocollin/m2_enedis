import os
import dash
from dash import html, dash_table, dcc
from dash.dependencies import Input, Output

class DashInterface:
    def __init__(self, dataframe):
        self.df = dataframe
        self.app = dash.Dash(__name__)
        self.server = self.app.server
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout(self):
        self.app.layout = html.Div([
            dcc.Tabs(id="tabs", value='tab-1', children=[
                dcc.Tab(label='Contexte', value='tab-1', style=self.tab_style, selected_style=self.tab_selected_style),
                dcc.Tab(label='Onglet 2', value='tab-2', style=self.tab_style, selected_style=self.tab_selected_style),
                dcc.Tab(label='Onglet 3', value='tab-3', style=self.tab_style, selected_style=self.tab_selected_style),
            ]),
            html.Div(id='tabs-content')
        ], style={'fontFamily': 'Century Gothic, sans-serif'})

    @property
    def tab_style(self):
        return {
            'padding': '10px',
            'fontWeight': 'bold',
            'backgroundColor': '#f9f9f9',
            'border': '1px solid #d6d6d6',
            'borderRadius': '5px',
            'margin': '5px'
        }

    @property
    def tab_selected_style(self):
        return {
            'padding': '10px',
            'fontWeight': 'bold',
            'backgroundColor': '#007bff',
            'color': 'white',
            'border': '1px solid #d6d6d6',
            'borderRadius': '5px',
            'margin': '5px'
        }

    def setup_callbacks(self):
        @self.app.callback(Output('tabs-content', 'children'),
                           [Input('tabs', 'value')])
        def render_content(tab):
            if tab == 'tab-1':
                return html.Div([
                    html.H1('Contexte'),
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i} for i in self.df.columns],
                        data=self.df.to_dict('records'),
                        page_size=30,
                        style_table={'height': '400px', 'overflowY': 'auto'},
                        virtualization=True,
                    )
                ])
            elif tab == 'tab-2':
                return html.Div([
                    html.H1('Onglet 2'),
                    html.Div('Contenu de l\'onglet 2.')
                ])
            elif tab == 'tab-3':
                return html.Div([
                    html.H1('Onglet 3'),
                    html.Div('Contenu de l\'onglet 3.')
                ])

    def run(self):
        port = int(os.environ.get('PORT', 8050))
        self.app.run_server(debug=False, host='0.0.0.0', port=port)