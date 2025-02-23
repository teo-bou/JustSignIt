from flask import Flask, request, jsonify, Response, send_file
import mediapipe as mp
import cv2
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os
from TrainModel import predict_sign, load_model, process, classes
import json



import time
import cv2
import json
from flask import Flask, jsonify

app = Flask(__name__)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True)
mp_drawing = mp.solutions.drawing_utils

# Load the trained model
model = load_model()

# Global variables
video_position = 0
user_score = 0

# Load JSON file with expected predictions
with open('labels.json', 'r') as f:
    video_positions = json.load(f)

@app.route('/predict')
def prediction():
    global user_score, video_position
    cap = cv2.VideoCapture(0)
    timestamp = 0  # Initialize a timestamp variable

    if not cap.isOpened():
        return jsonify({'error': 'Could not access webcam'}), 500

    success, frame = cap.read()
    if not success:
        cap.release()
        return jsonify({'error': 'Could not read frame'}), 500

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)

    # Convert to RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Increment the timestamp for each frame
    timestamp += 1

    # Override MediaPipe's default timestamp behavior
    
    results = hands.process(image_rgb)
    

    if results.multi_hand_landmarks:
        hand_landmarks_array = process(image_rgb, results)
        if hand_landmarks_array is not None:
            prediction = predict_sign(model, image_rgb, results)
            predicted_class = classes[prediction]

            # Check if the current video position is within expected positions
            for position in video_positions:
                start_position = position['start_position']
                end_position = position['end_position']
                expected_prediction = position['expected_prediction']

                # Ensure user hasn't already received points for this position
                if start_position <= video_position <= end_position and not position.get('scored', False):
                    if predicted_class == expected_prediction:
                        user_score += 10
                        position['scored'] = True  # Mark this position as scored
                    break

            cap.release()
            return jsonify({'prediction': predicted_class, 'score': user_score})

    cap.release()
    return jsonify({'error': 'No hand detected'})


def gen():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        
@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')




@app.route('/video_started', methods=['POST'])
def video_started():
    global video_position
    video_position = 0
    return jsonify({'status': 'Video started'})

@app.route('/update_position', methods=['POST'])
def update_position():
    global video_position
    data = request.get_json()
    video_position = data.get('position', 0)
    return jsonify({'status': 'Position updated', 'position': video_position})

@app.route('/get_position', methods=['GET'])
def get_position():
    global video_position
    return jsonify({'position': video_position})

if __name__ == '__main__':
    app.run(debug=True)
