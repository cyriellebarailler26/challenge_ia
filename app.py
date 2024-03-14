import asyncio
import base64
import dash, cv2
import threading
from dash import html
from dash.dependencies import Output, Input
from quart import Quart, websocket
from dash_extensions import WebSocket

from flask import jsonify


####
import mediapipe as mp
import numpy as np


mp_holistic = mp.solutions.holistic # Holistic model
mp_drawing = mp.solutions.drawing_utils # Drawing utilities


def mediapipe_detection(image, model):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
    image.flags.writeable = False                  # Image is no longer writeable
    results = model.process(image)                 # Make prediction
    image.flags.writeable = True                   # Image is now writeable 
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
    return image, results

def draw_landmarks(image, results):
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS) # Draw face connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS) # Draw pose connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

def draw_styled_landmarks(image, results):
    # Draw face connections
    mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                             mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
                             mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                             ) 
    # Draw pose connections
    mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS,
                             mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                             ) 
    # Draw left hand connections
    mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                             ) 
    # Draw right hand connections  
    mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                             mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
                             mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                             )
    
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

# Actions that we try to detect
# actions = np.array(['A', 'E', 'I', 'L', 'N', 'O', 'R', 'S', 'T', 'U'])
actions = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'])
# Label mapping
label_map = {label:num for num, label in enumerate(actions)}

from keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu', input_shape=(30,126)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(actions.shape[0], activation='softmax'))
model.load_weights('action_26L.h5')

####


class VideoCamera(object):
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        _, jpeg = cv2.imencode('.jpg', image)
        return image, jpeg.tobytes()


# Setup small Quart server for streaming via websocket.
server = Quart(__name__)
delay_between_frames = 0.05  # add delay (in seconds) if CPU usage is too high


@server.websocket("/stream")
async def stream():
    sequence = []
    threshold = 0.5

    camera = VideoCamera(0)  # zero means webcam
    pred = 'NO'
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            if delay_between_frames is not None:
                await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
            jpeg, frame = camera.get_frame()
            
            temp = frame
            # frame2 = base64.b64encode(frame).decode()
            image, results = mediapipe_detection(jpeg, holistic)
            if results.left_hand_landmarks or results.right_hand_landmarks:
            
                draw_styled_landmarks(image, results)
                _, jpeg = cv2.imencode('.jpg', image)
                
                # 2. Prediction logic
                keypoints = extract_keypoints(results)[1536:]
                sequence.append(keypoints)
                sequence = sequence[-30:]
                
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    if res[np.argmax(res)] > threshold: 
                        pred = actions[np.argmax(res)]
                
                temp = jpeg.tobytes()
            
            await websocket.send(f"{pred}||data:image/jpeg;base64, {base64.b64encode(temp).decode()}")
            
            

@server.websocket("/stream2")
async def stream2():
    sequence = []
    threshold = 0.5

    camera = VideoCamera(0)  # zero means webcam
    pred = 'NO'
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        while True:
            if delay_between_frames is not None:
                await asyncio.sleep(delay_between_frames)  # add delay if CPU usage is too high
            jpeg, frame = camera.get_frame()
            
            temp = frame
            # frame2 = base64.b64encode(frame).decode()
            image, results = mediapipe_detection(jpeg, holistic)
            if results.left_hand_landmarks or results.right_hand_landmarks:
            
                draw_styled_landmarks(image, results)
                _, jpeg = cv2.imencode('.jpg', image)
                
                # 2. Prediction logic
                keypoints = extract_keypoints(results)[1536:]
                sequence.append(keypoints)
                sequence = sequence[-30:]
                
                if len(sequence) == 30:
                    res = model.predict(np.expand_dims(sequence, axis=0))[0]
                    if res[np.argmax(res)] > threshold: 
                        pred = actions[np.argmax(res)]
                
                temp = jpeg.tobytes()
            
            await websocket.send(f"{pred}||data:image/jpeg;base64, {base64.b64encode(temp).decode()}")


# Create small Dash application for UI.
app = dash.Dash(__name__, use_pages=True, external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css'])

app.layout = html.Div(
    children=[
        dash.page_container
    ]
)

if __name__ == '__main__':
    threading.Thread(target=app.run_server).start()
    server.run()