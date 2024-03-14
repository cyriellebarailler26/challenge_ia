import dash
from dash import html, Input, Output, clientside_callback
from dash_extensions import WebSocket

dash.register_page(__name__)

import random
letters = random.sample(['A', 'B', 'C', 'E', 'I', 'H', 'L', 'V', 'M'], 5)

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
                    html.Div(className='mn-body w-75 position-relative', children=[
                        html.Div(className='webcam-div', children=[
                            html.Img(style={'width': '100%'}, id="video"),
                            WebSocket(url=f"ws://127.0.0.1:5000/stream", id="ws")
                        ])]+[
                        html.Div(className='steps', children=[
                            html.Div(className='step', id=f'question-{i}', children=[
                                html.H1(children=[
                                    html.Span('Faites le signe correspondant à cette lettre')
                                ]),
                                html.Div(className='exo-content', children=[
                                    html.Span(letter, className='letter')
                                ]),
                            ]) for i, letter in enumerate(letters)
                        ])
                        #
                    ])
                ])
            ])
        ]),
        html.Div(className='main-footer', children=[
            html.Div(className='container start-form d-flex justify-content-between', children=[
                html.Div(className='form-group', children=[
                    html.Button('', className='btn-continue w-100 p-0')
                ]),
                html.Div(className='form-group', children=[
                    html.Button('Continuer', id="continuer", className='nexter btn-continue disabled w-100')
                ])
            ])
        ])
    ]
)



clientside_callback(
    """
    function(m){
        const currentLetter = document.querySelector('.step.active .letter').innerHTML
        const predLetter = m.data.split("||")[0]

        console.log(predLetter);
        
        if(currentLetter == predLetter) {
            document.querySelector('.nexter.btn-continue').classList.remove('disabled')
            document.querySelector('.main-footer').classList.remove('success')
        }
        
        return m? m.data.split("||")[1] : '';
    }
    """,
    Output(f"video", "src"),
    Input(f"ws", "message")
)