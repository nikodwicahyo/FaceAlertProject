import face_recognition
import os

def load_known_faces(dataset_path):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(dataset_path):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(dataset_path, filename)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)

            if encoding:
                known_face_encodings.append(encoding[0])
                name = os.path.splitext(filename)[0]
                known_face_names.append(name)

    return known_face_encodings, known_face_names
