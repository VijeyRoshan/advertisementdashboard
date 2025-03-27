import cv2
import os
from face_detection import FaceAnalyzer
from ad_display import AdManager

def main():
    # Initialize the face analyzer with the correct models path
    face_analyzer = FaceAnalyzer(base_path='models')
    
    # Initialize the ad manager with the correct ads path
    ad_manager = AdManager(ads_base_path='ads')
    
    # Initialize video capture with PC webcam (index 0)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not connect to PC webcam.")
        print("Please make sure your webcam is properly connected.")
        return

    print("Smart Advertisement System Started...")
    print("Press 'q' to quit")

    # Capture one frame and detect
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame from PC webcam")
        return

    # Release the camera immediately after capturing one frame
    cap.release()

    # Detect faces in the frame
    face_boxes = face_analyzer.detect_faces(frame)
    
    if not face_boxes:
        print("No face detected. Please try running the program again.")
        return

    # Process the first detected face
    face_box = face_boxes[0]  # Take first detected face
    gender, age = face_analyzer.analyze_face(frame, face_box)
    print(f"Detected: {gender}, Age: {age}")

    # Select and display ad until user quits
    ad_path = ad_manager.select_ad(gender, age)
    if ad_path:
        print(f"Displaying ad for {gender}, age {age}")
        print("Close the window or press 'q' to quit")
        ad_manager.display_ad(ad_path)  # Will display until window is closed
    else:
        print("No suitable ad found")

    # Cleanup
    ad_manager.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
