import dash
import os
from dash_extensions import WebSocket
from dash import html, Input, Output, clientside_callback

dash.register_page(__name__)

students = os.listdir("assets/etudiants/")[:5]

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
                        html.Div(className='webcam-div', children=[
                            html.Img(style={'width': '100%'}, id="video2"),
                            WebSocket(url=f"ws://127.0.0.1:5000/stream2", id="ws2")
                        ])]+[
                        html.Div(className='steps', children=[
                            html.Div(className='step', id=f'question-{i}', children=[
                                html.H1(children=[
                                    html.Span('Écrivez le nom de cette personne :')
                                ]),
                                html.Div(className='exo-content', children=[
                                    html.Img(className='image-to-write', src=f'/assets/etudiants/{letter}'),
                                    html.Div(className='write-place', children=[
                                        html.Div(className='write-line', children=[
                                            html.Span(className='btn-letter', children=[c])
                                            for c in letter.split('.')[0]
                                        ])
                                    ])
                                ]),
                            ]) for i, letter in enumerate(students)
                        ])
                        #
                    ])
                ])
            ])
        ]),
        html.Div(className='main-footer', children=[
            html.Div(className='container start-form d-flex justify-content-between', children=[
                html.Div(className='form-group', children=[
                    html.Button('', className='btn-continue prev w-100 p-0')
                ]),
                html.Div(className='form-group', children=[
                    html.Button('Continuer', className='nexter btn-continue disabled w-100')
                ])
            ])
        ])
    ]
)


clientside_callback(
    """
    function(m){
        const letters = document.querySelector('.step.active .write-line .btn-letter.current');
        
        const currentLetter = letters.innerHTML;
        const predLetter = m.data.split("||")[0];
        
        console.log(currentLetter, predLetter);
        
        if(predLetter == currentLetter) {
            if(!!letters.nextSibling) {
                letters.nextSibling.classList.add('current')
                letters.classList.remove('current')
            } else {
                document.querySelector('.nexter.btn-continue').classList.remove('disabled')
            }
        }
        return m? m.data.split("||")[1] : '';
    }
    """,
    Output(f"video2", "src"),
    Input(f"ws2", "message")
)