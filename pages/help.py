import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback, State, dash_table


dash.register_page(__name__)

layout = html.Div(
    className='',
    children=[
        html.Div(className='left-body', children=[
            html.Div(className='left-head', children=[
                html.Div(className='left-bar-content', children=[
                    html.Div(className='logo', children=[
                        html.H1('Quatrosigno')
                    ])
                ]),
                html.Div(className='nar-bar', children=[
                    html.Ul(className='nav-ul', children=[
                        html.Li(children=[
                            html.A(className='nav-item w-100', href="/courses", children=[
                                html.Img(className='nav-ico', src='https://d35aaqx5ub95lt.cloudfront.net/vendor/784035717e2ff1d448c0f6cc4efc89fb.svg', alt=''),
                                html.Span('Mes cours')
                            ])
                        ]),
                        html.Li(children=[
                            html.A(className='nav-item w-100', href="/help", children=[
                                html.Img(className='nav-ico', src='https://simg-ssl.duolingo.com/avatars/981300147/78FYzQ0V0W/xlarge', alt=''),
                                html.Span('Alphabet')
                            ])
                        ])
                        # ,
                        # html.Li(children=[
                        #     html.Button(className='nav-item w-100', children=[
                        #         html.Img(className='nav-ico', src='https://d35aaqx5ub95lt.cloudfront.net/vendor/7159c0b5d4250a5aea4f396d53f17f0c.svg', alt=''),
                        #         html.Span('Paramètres')
                        #     ])
                        # ])
                    ])
                ])
            ])
        ]),
        html.Div(className='right-body', children=[
            html.Div(className='content', children=[
                html.Div(className='middle-body', children=[
                    html.Img(src='/assets/alphabet.png', className='home-image', alt='Home Image')
                ])
            ])
        ])
    ]
)
