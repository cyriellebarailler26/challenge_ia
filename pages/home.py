import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input


dash.register_page(__name__)


layout = html.Div(
    children=[
        html.Div(className='home-container', children=[
            html.Div(className='main-head', children=[
                html.Div(className='container', children=[
                    html.Div(className='logo', children=[
                        html.H1('Quatrosigno')
                    ])
                ])
            ]),
            html.Div(className='main-body', children=[
                html.Div(className='container', children=[
                    html.Div(className='main-body-content', children=[
                        html.Div(className='main-left-body', children=[
                            html.Img(src='/assets/home-image.png', className='home-image', alt='Home Image')
                        ]),
                        html.Div(className='main-right-body', children=[
                            html.P(children=[
                                    html.H1("Bienvenue sur QuatroSigno", className="welcome-msg"),
                                    "Votre compagnon pour apprendre la langue des signes d'une manière amusante, interactive et accessible à tous. QuatroSigno est une application de reconnaissance de la langue des signes conçue pour vous aider à maîtriser cette forme unique de communication. Plongeons dans les fonctionnalités et les détails de cette application innovante."
                                ]),
                            html.Form(className='start-form', action='/courses', children=[
                                html.Div(className='form-group mb-3', children=[
                                    dcc.Input(type='text', id="swap", className='name-input w-100', name='nom', placeholder='Veuillez saisir votre nom'),
                                    dcc.Input(type='text', id="swapout", className='d-none')
                                ]),
                                html.Div(className='form-group', children=[
                                    html.Button('Continuer', className='btn-continue w-100')
                                ])
                            ])
                        ])
                    ])
                ])
            ]),
            html.Div(className='main-footer', children=[
                html.H2('SISE - 2024')
            ])
        ])
    ]
)


@callback(
    Output('swapout', 'value'),
    Input('swap', 'value')
)
def update_pie_local(value):
    print(value)
    # return value