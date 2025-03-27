import cv2
import numpy as np
import os

class FaceAnalyzer:
    def __init__(self, base_path='models'):
        # Construct full paths to model files with correct filenames
        faceProto = os.path.join(base_path, 'opency_face_detector.pbtxt')
        faceModel = os.path.join(base_path, 'opency_face_detector_uint8.pb')
        ageProto = os.path.join(base_path, 'age_deploy.prototxt')
        ageModel = os.path.join(base_path, 'age_net.caffemodel')
        genderProto = os.path.join(base_path, 'gender_deploy.prototxt')
        genderModel = os.path.join(base_path, 'gender_net.caffemodel')

        # Verify file existence
        self._verify_file_exists(faceProto, 'Face Prototype')
        self._verify_file_exists(faceModel, 'Face Model')
        self._verify_file_exists(ageProto, 'Age Prototype')
        self._verify_file_exists(ageModel, 'Age Model')
        self._verify_file_exists(genderProto, 'Gender Prototype')
        self._verify_file_exists(genderModel, 'Gender Model')

        # Load networks
        self.faceNet = cv2.dnn.readNet(faceModel, faceProto)
        self.ageNet = cv2.dnn.readNet(ageModel, ageProto)
        self.genderNet = cv2.dnn.readNet(genderModel, genderProto)

        # Define age and gender lists
        self.ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
        self.genderList = ['Male', 'Female']

    def _verify_file_exists(self, file_path, file_description):
        """Verify that a file exists, raise an informative error if not"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"{file_description} file not found at {file_path}")

    def detect_faces(self, frame):
        """Detect faces in the input frame"""
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], True, False)

        self.faceNet.setInput(blob)
        detections = self.faceNet.forward()
        
        faceBoxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.7:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                faceBoxes.append([x1, y1, x2, y2])

        return faceBoxes

    def analyze_face(self, frame, faceBox):
        """Analyze face for age and gender"""
        x1, y1, x2, y2 = faceBox
        face = frame[y1:y2, x1:x2]

        # Prepare blob for age and gender networks
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)

        # Predict gender
        self.genderNet.setInput(blob)
        genderPreds = self.genderNet.forward()
        gender = self.genderList[genderPreds[0].argmax()]

        # Predict age
        self.ageNet.setInput(blob)
        agePreds = self.ageNet.forward()
        age = self.ageList[agePreds[0].argmax()]

        return gender, age

# Optional: Add a simple test if script is run directly
if __name__ == "__main__":
    print("Face Detection module loaded successfully.")