import dash
from dash import html

dash.register_page(__name__)

letters = ['A', 'Z', 'E', 'R', 'T']

layout = html.Div(
    className='exo_ct home-container',
    children=[
        html.Div(className='main-head', children=[
            html.Div(className='container', children=[
                html.Div(className='top-content', children=[
                    html.A(className='closer', href='/courses', children=[
                        html.I(className='fa-solid fa-xmark')
                    ]),
                    html.Div(className='progress w-100', children=[
                        html.Div(className='progress-bar', role='progressbar', style={'width': '25%'})
                    ])
                ])
            ])
        ]),
        html.Div(className='main-body', children=[
            html.Div(className='container', children=[
                html.Div(className='mn-content d-flex justify-content-center', children=[
                    html.Div(className='mn-body w-75', children=[
                        #
                        html.Div(className='steps', children=[
                            html.Div(className='step', children=[
                                html.H1(children=[
                                    html.Span('Écrivez la lettre manquante :')
                                ]),
                                html.Div(className='exo-content', children=[
                                    'Ceci ',
                            html.Span('...', className='btn-letter'),
                            html.Span('st', className='ms-0 btn-letter uncomplete'),
                            ' un test'
                                ]),
                            ]) for letter in letters
                        ])
                        #
                    ])
                ])
            ])
        ]),
        html.Div(className='main-footer', children=[
            html.Div(className='container start-form d-flex justify-content-between', children=[
                html.Div(className='form-group', children=[
                    html.Button('Passer', className='btn-continue w-100')
                ]),
                html.Div(className='form-group', children=[
                    html.Button('Continuer', className='nexter btn-continue w-100')
                ])
            ])
        ])
    ]
)