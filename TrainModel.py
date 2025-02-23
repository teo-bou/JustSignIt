import mediapipe as mp
import cv2
import numpy as np
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


folders = ['A', 'B', 'C', 'D']
classes = ['A', 'B', 'C', 'D']


def process(image_rgb, results):
    # Process the image and find hands
    hand_landmarks_list = []
    skip = False
    # Draw bounding box if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            if skip:
                break
            skip = True
            # Get the bounding box coordinates
            x_min = min([lm.x for lm in hand_landmarks.landmark])
            y_min = min([lm.y for lm in hand_landmarks.landmark])
            x_max = max([lm.x for lm in hand_landmarks.landmark])
            y_max = max([lm.y for lm in hand_landmarks.landmark])
            
            # Convert normalized coordinates to pixel values
            h, w, _ = image_rgb.shape
            x_min = int(x_min * w)
            y_min = int(y_min * h)
            x_max = int(x_max * w)
            y_max = int(y_max * h)
        
            # Draw the bounding box
            for landmark in hand_landmarks.landmark:
                normalized_x = (landmark.x - x_min / w) / ((x_max - x_min) / w)
                normalized_y = (landmark.y - y_min / h) / ((y_max - y_min) / h)
                hand_landmarks_list.extend([normalized_x, normalized_y, landmark.z])

        # Convert the list to a numpy array
        hand_landmarks_array = np.array(hand_landmarks_list)
        return hand_landmarks_array




def read_and_process_images(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        if filename.endswith('.png') or filename.endswith('.jpg'):
            filepath = os.path.join(folder, filename)
            image = cv2.imread(filepath)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            hand_landmarks_array = process(image_rgb, results)
            if hand_landmarks_array is not None:
                images.append(hand_landmarks_array)
                labels.append(label)
    return images, labels


def load_model():
    # Load the trained model
    model = joblib.load('model.pkl')
    return model

def predict_sign(model, image, results):
    return model.predict(process(image, results).reshape(1, -1))[0]


if __name__ == '__main__':
    
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=True)

    all_images = []
    all_labels = []
    for folder in folders:
        images, labels = read_and_process_images(folder, label=folders.index(folder))
        all_images.extend(images)
        all_labels.extend(labels)



    # Convert to numpy arrays
    all_images = np.array(all_images)
    all_labels = np.array(all_labels)


    # Flatten the images for the model
    n_samples, n_features = all_images.shape[0], all_images.shape[1]
    all_images_flattened = all_images.reshape(n_samples, n_features)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(all_images_flattened, all_labels, test_size=0.2, random_state=42, shuffle=True)

    # Create a RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Train the model
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate the accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model accuracy: {accuracy * 100:.2f}%")
    print("Model trained successfully")
    # Save the model
    joblib.dump(model, 'model.pkl')
    print("Model saved successfully")