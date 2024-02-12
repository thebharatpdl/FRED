import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import csv
import time
import os
from sklearn.svm import OneClassSVM
import joblib  

########## KNN CODE ############
def euclidean_distance(v1, v2):
    """Calculate the Euclidean distance between two vectors."""
    return np.sqrt(((v1 - v2) ** 2).sum())

def knn(train, test, k=5):
    """K-nearest neighbors algorithm for classification."""
    distances = []
    for i in range(train.shape[0]):
        ix = train[i, :-1]
        iy = train[i, -1]
        d = euclidean_distance(test, ix)
        distances.append([d, iy])
    dk = sorted(distances, key=lambda x: x[0])[:k]
    labels = np.array(dk)[:, -1]
    output = np.unique(labels, return_counts=True)
    index = np.argmax(output[1])
    return output[0][index], dk[0][0]  # Return both label and distance
################################

def load_haar_cascade():
    """Load the Haar Cascade Classifier for face detection."""
    try:
        return cv2.CascadeClassifier('app/models/haarcascade_frontalface_alt.xml')
    except Exception as e:
        print(f"Error loading the Haar Cascade Classifier: {e}")
        exit()

def load_cnn_model():
    """Load the CNN model for emotion prediction."""
    try:
        return load_model('app/models/model.h5')
    except Exception as e:
        print(f"Error loading the CNN model: {e}")
        exit()

def save_svm_model(svm_model, filename='svm_model.joblib'):
    """Save the SVM model to a file using joblib."""
    try:
        joblib.dump(svm_model, filename)
        print(f"SVM model saved to {filename}")
    except Exception as e:
        print(f"Error saving SVM model: {e}")

def load_svm_model(filename='svm_model.joblib'):
    """Load the SVM model from a file using joblib."""
    try:
        return joblib.load(filename)
    except Exception as e:
        print(f"Error loading SVM model: {e}")
        exit()

def svm_model(dataset_path="./face_dataset/"):
    """Train, save, and load the SVM model for face recognition."""
    face_data = []
    labels = []
    class_id = 0
    names = {}

    # Dataset preparation
    for fx in os.listdir(dataset_path):
        if fx.endswith('.npy'):
            names[class_id] = fx[:-4]
            data_item = np.load(os.path.join(dataset_path, fx))
            face_data.append(data_item)

            target = class_id * np.ones((data_item.shape[0],))
            class_id += 1
            labels.append(target)

    face_dataset = np.concatenate(face_data, axis=0)
    face_labels = np.concatenate(labels, axis=0).reshape((-1, 1))

    trainset = np.concatenate((face_dataset, face_labels), axis=1)

    # Train a one-class SVM on the known face data
    try:
        svm = OneClassSVM(gamma='auto')
        svm.fit(face_dataset)
        # Save the trained SVM model
        # save_svm_model(svm)
    except Exception as e:
        print(f"Error training SVM: {e}")
        exit()

    # Load the SVM model
    # svm = load_svm_model()

    return svm, names, trainset

def collect_initial_distances(cap, face_classifier, trainset):
    """Collect initial distances for dynamic thresholding."""
    initial_distances = []
    for _ in range(30):  # Collect distances from the first 30 frames
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray, 1.3, 5)

            for face in faces:
                x, y, w, h = face
                offset = 5
                face_section = frame[y - offset: y + h + offset, x - offset: x + w + offset]

                # Add a check for empty face section
                if not face_section.size == 0:
                    face_section = cv2.resize(face_section, (100, 100))
                    _, distance = knn(trainset, face_section.flatten())
                    initial_distances.append(distance)

    return initial_distances

def set_dynamic_threshold(initial_distances):
    """Set dynamic threshold based on initial distances."""
    return np.median(initial_distances)


def main():
    """Main function for running the emotion and face detection system."""

    # Load Haar Cascade Classifier
    face_classifier = load_haar_cascade()

    # Load CNN model
    classifier = load_cnn_model()

    emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']

    # Display emotion labels with different colors
    emotion_colors = {'Angry': (0, 0, 255), 'Disgust': (0, 255, 0), 'Fear': (255, 0, 0),
                  'Happy': (255, 255, 0), 'Neutral': (255, 165, 0), 'Sad': (0, 255, 255),
                  'Surprise': (255, 0, 255)}

    # Specify the folder path to store CSV files
    csv_folder = 'app/static/captured_emotions_data'

    # Create the folder if it doesn't exist
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Create unknown_face folder if it doesn't exist
    unknown_faces_directory = 'unknown_faces'
    if not os.path.exists(unknown_faces_directory):
        os.makedirs(unknown_faces_directory)

    # Save the captured image in a sub-folder with the current timestamp
    image_folder = os.path.join(unknown_faces_directory, time.strftime('%Y%m%d_%H%M%S'))
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    # Initializing dictionary to store unknown face id
    known_face_ids = {}

    # Generate the CSV file name with current date and time
    csv_file_name = time.strftime('%Y%m%d_%H%M%S') + '_captured_emotions.csv'
    csv_file_path = os.path.join(csv_folder, csv_file_name)
    try:
        with open(csv_file_path, 'w', newline='') as csv_file:
            fieldnames = ['Timestamp', 'Date', 'Emotion', 'Duration','Person']
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            # Write header
            csv_writer.writeheader()

            start_time = None  # Variable to store the start time of an emotion

            # Initialize cap outside the try block
            cap = cv2.VideoCapture(0)

            # Check if VideoCapture initialization was successful
            if not cap.isOpened():
                print("Error: Could not open video capture.")
                exit()

            # Face recognition setup
            svm, names, trainset = svm_model()

            font = cv2.FONT_HERSHEY_SIMPLEX

            # Collect some initial distances for dynamic threshold calculation
            initial_distances = collect_initial_distances(cap, face_classifier, trainset)

            # Set the threshold dynamically based on the initial distances
            dynamic_threshold = set_dynamic_threshold(initial_distances)

            # Initialize an ID counter for unknown face
            id_counter = 1

            while True:
                _, frame = cap.read()
                labels = []
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_classifier.detectMultiScale(gray)
                

                for (x, y, w, h) in faces:
                    offset = 5
                    face_section = frame[y - offset: y + h + offset, x - offset: x + w + offset]

                    # Add a check for empty face section
                    if not face_section.size == 0:
                        # Use the SVM decision function to get the confidence score
                        face_section = cv2.resize(face_section, (100, 100))
                        _, distance = knn(trainset, face_section.flatten())

                        # Set the threshold dynamically based on the initial distances
                        if distance > dynamic_threshold:
                            if (x, y, w, h) not in known_face_ids:
                                unknown_face_id = f'1000_{id_counter}'
                                known_face_ids[(x, y, w, h)] = unknown_face_id
                                id_counter += 1

                                

                                image_filename = f'{unknown_face_id}_{time.strftime("%Y%m%d_%H%M%S")}.png'
                                image_path = os.path.join(image_folder, image_filename)
                                cv2.imwrite(image_path, face_section)

                            name_label = known_face_ids[(x, y, w, h)]
                        else:
                            # Perform KNN for known faces
                            out, _ = knn(trainset, face_section.flatten())
                            name_label = names[int(out)]

                        name_label_position = (x, y - 10)  #coordinates for name label near each face
                        
                        cv2.putText(frame, f"Name: {name_label}", name_label_position, cv2.FONT_HERSHEY_SIMPLEX, 1,
                                    (255, 0, 0), 2, cv2.LINE_AA)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 255), 2)

                        # Display emotion labels next to each face
                        roi_gray = gray[y:y + h, x:x + w]
                        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

                        if np.sum([roi_gray]) != 0:
                            roi = roi_gray.astype('float') / 255.0
                            roi = img_to_array(roi)
                            roi = np.expand_dims(roi, axis=0)

                            try:
                                prediction = classifier.predict(roi)[0]
                                emotion_label = emotion_labels[prediction.argmax()]

                                # Get the current timestamp with full date and time
                                timestamp = time.strftime('%Y-%m-%d %H:%M:%S.') + str(
                                    int((time.time() % 1) * 1000)).zfill(3)

                                # Get the current date
                                current_date = time.strftime('%Y-%m-%d')

                                # Store the predicted emotion label, frame number, timestamp, date, and duration in variables
                                captured_emotion = emotion_label
                                captured_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

                                if start_time is None:
                                    start_time = time.time()  # Set the start time for the first emotion
                                else:
                                    # Calculate the duration between the current and previous emotion
                                    duration = time.time() - start_time
                                    start_time = time.time()  # Update the start time for the next emotion

                                    # Write the data to the CSV file
                                    csv_writer.writerow({
                                        'Timestamp': timestamp,
                                        'Date': current_date,
                                        'Emotion': captured_emotion,
                                        'Duration': duration,
                                        'Person': name_label
                                    })

                                emotion_label_position = (x, y + h + 30)  #coordinates for emotion label next to each face
                                emotion_color = emotion_colors.get(emotion_label, (0, 255, 0))
                                cv2.putText(frame, f"Emotion: {emotion_label}", emotion_label_position,
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                                cv2.putText(frame, f"Emotion: {emotion_label}", emotion_label_position,
                                            cv2.FONT_HERSHEY_SIMPLEX, 1, emotion_color, 2)
                            except Exception as e:
                                print(f"Error predicting emotion: {e}")
                        else:
                            cv2.putText(frame, 'No Faces', (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                        # Print current emotion in the terminal
                        print("Captured Emotion:", captured_emotion)

                cv2.imshow('Emotion and Face Detector', frame)
                key_pressed = cv2.waitKey(1) & 0xFF
                if key_pressed == ord('q') or key_pressed == 27:
                    break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
