import cv2
from protocol import *

# === Load reference image ===
reference_image_path = r"C:\Users\User\Documents\GitHub\Cyber-Project\Images\gabi.png"

reference_image = face_recognition.load_image_file(reference_image_path)
reference_encodings = face_recognition.face_encodings(reference_image)

if len(reference_encodings) == 0:
    print("No face found in the reference image!")
    exit()

reference_encoding = reference_encodings[0]

# Use DSHOW backend on Windows — much faster to initialize
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Lower resolution = faster startup & processing
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Reduce internal buffer to avoid stale frames
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

print("Press 'q' to quit.")

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces([reference_encoding], face_encoding)

        if matches[0]:
            match_text = "MATCH!"
            color = (0, 255, 0)
        else:
            match_text = "NOT MATCH"
            color = (0, 0, 255)

        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, match_text, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

    cv2.imshow('Face Recognition', frame)

    if cv2.waitKey(1) == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()