from flask import Flask, request, jsonify
import os
import face_recognition
import numpy as np
import cv2
from utils.face_recognition_helper import load_known_faces
import telegram

# CONFIG
TELEGRAM_TOKEN = '7701272969:AAGmhwar1GoLKnsd_zL7248lcSvnCG05PHM'
TELEGRAM_CHAT_ID = '1159476089'
DATASET_PATH = 'dataset/'

bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Load known faces
known_face_encodings, known_face_names = load_known_faces(DATASET_PATH)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    # Convert to RGB
    rgb_img = img[:, :, ::-1]

    # Face recognition
    face_locations = face_recognition.face_locations(rgb_img)
    face_encodings = face_recognition.face_encodings(rgb_img, face_locations)

    unknown_detected = False

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)

        if not any(matches):
            unknown_detected = True
            break

    if unknown_detected:
        # Save temporary image
        temp_path = 'unknown.jpg'
        cv2.imwrite(temp_path, img)

        # Send to Telegram
        with open(temp_path, 'rb') as photo:
            bot.send_photo(chat_id=TELEGRAM_CHAT_ID, photo=photo, caption="⚠️ Wajah Tak Dikenal Terdeteksi!")

        os.remove(temp_path)

        return jsonify({'status': 'Unknown face detected, notification sent!'}), 200
    else:
        return jsonify({'status': 'All faces recognized'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
