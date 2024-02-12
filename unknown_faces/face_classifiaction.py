import os
import dlib
import shutil
import numpy as np

def euclidean_distance(vec1, vec2):
    return np.linalg.norm(np.array(vec1) - np.array(vec2))

def organize_images(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    #HOG face detector
    face_detector = dlib.get_frontal_face_detector()

    #face recognition model
    shape_predictor = dlib.shape_predictor("unknown_faces/shape_predictor_68_face_landmarks.dat")
    face_recognizer = dlib.face_recognition_model_v1("unknown_faces/dlib_face_recognition_resnet_model_v1.dat")

    # Load images from the input folder
    image_files = [f for f in os.listdir(input_folder) if f.endswith(('.jpg', '.png'))]
    image_paths = [os.path.join(input_folder, f) for f in image_files]

    known_encodings = []
    known_persons = []

    for image_path in image_paths:
        # Load the image
        image = dlib.load_rgb_image(image_path)

        # Detect faces in the image
        faces = face_detector(image)

        if len(faces) > 0:
            # Use the first face found for simplicity
            shape = shape_predictor(image, faces[0])
            face_encoding = face_recognizer.compute_face_descriptor(image, shape)
            known_encodings.append(face_encoding)
            known_persons.append(image_path)  # Store the image path for later association

    unique_persons = {}  # Dictionary to store unique persons and their associated images
    for i, face_encoding in enumerate(known_encodings):
        matched = False

        for j in range(i + 1, len(known_encodings)):
            # Compare face encodings
            distance = euclidean_distance(face_encoding, known_encodings[j])

            if distance < 0.6:  #threshold value
                matched = True

                # Mark both images' persons as same
                unique_persons.setdefault(known_persons[i], []).append(known_persons[j])

        # If no match found, mark the person as unique
        if not matched:
            unique_persons.setdefault(known_persons[i], [])

    # Create folders and move images
    for person, associated_images in unique_persons.items():
        person_folder = os.path.join(output_folder, f'Person_{list(unique_persons.keys()).index(person)}')
        os.makedirs(person_folder, exist_ok=True)
        shutil.copy(person, person_folder)
        for image in associated_images:
            shutil.copy(image, person_folder)

input_folder_path = 'unknown_faces/20240205_222200'
output_folder_path = 'unknown_faces/folder'

organize_images(input_folder_path, output_folder_path)
