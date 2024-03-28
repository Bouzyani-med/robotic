import cv2
import serial
import time

# Set the serial port and baud rate
ser = serial.Serial('COM11', 9600, timeout=1)
time.sleep(2)  # Allow time for Arduino to reset

# Initialize face cascade from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    if len(faces) > 0:
        print("Face detected!")
        ser.write(b'1')  # Send '1' to Arduino to turn servo
    else:
        print("No face detected.")
        ser.write(b'0')  # Send '0' to Arduino to return servo to initial position

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
ser.close()
