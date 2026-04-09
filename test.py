# from protocol import *
#
# # === Load reference image ===
# reference_image_path = """C:\\Users\\Gabi\\Desktop\\family_photos\\gaya.jpeg"""  # <-- change this to your image path
#
# reference_image = face_recognition.load_image_file(reference_image_path)
# reference_encodings = face_recognition.face_encodings(reference_image)
#
# if len(reference_encodings) == 0:
#     print("No face found in the reference image!")
#     exit()
#
# reference_encoding = reference_encodings[0]
#
# video_capture = cv2.VideoCapture(0)
#
# print("Press 'q' to quit.")
#
# while True:
#     ret, frame = video_capture.read()
#     if not ret:
#         break
#
#     # Convert BGR (OpenCV) to RGB (face_recognition)
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#
#     face_locations = face_recognition.face_locations(rgb_frame, model= "hog") # Detects face from camera
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations) # Encodes the face
#
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # Compare with reference
#         matches = face_recognition.compare_faces([reference_encoding], face_encoding)
#
#         match_text = "Unknown"
#
#         if matches[0]:
#             match_text = "MATCH!"
#             color = (0, 255, 0)
#         else:
#             match_text = "NOT MATCH"
#             color = (0, 0, 255)
#
#
#         # Draw rectangle around face
#         cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#
#         # Display result
#         cv2.putText(frame, match_text, (left, top - 10),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
#
#     # Show frame
#     cv2.imshow('Face Recognition', frame)
#
#     # Exit on 'q'
#     key = cv2.waitKey(1)
#     if key == ord('q'):
#         break
#
# # Cleanup
# video_capture.release()
# cv2.destroyAllWindows()
#
