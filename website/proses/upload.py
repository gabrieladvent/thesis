import cv2
from ultralytics import YOLO
import numpy as np
import random
import streamlit as st
import base64


model = YOLO('best.pt')

def draw_boxes(image, boxes, labels):
    img = np.array(image)
    for box, label in zip(boxes, labels):
        box = [int(coord) for coord in box]
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 5)
        cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    return img


def image_classify(image):
    model = YOLO('best.pt')
    source = image

    # Run inference on the source
    results = model(source, stream=True)
    
    boxes = []
    labels = []
    for result in results:
        box = result.boxes.xyxy
        boxes.append(box)
        for cls_idx in result.boxes.cls.tolist():
            label = model.names[cls_idx]
            labels.append(label)
    
    return boxes, labels




def video_classify(video_path):
    # convert image to (224, 224)

    # convert image to numpy array

    # normalize image

    # set model input
    
    # make prediction
    
    # index = np.argmax(prediction)

    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Detect objects
        detections = image_classify(frame, model)

        # Draw bounding boxes
        for det in detections:
            x1, y1, x2, y2 = map(int, det)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# def set_background(image_file):
#     with open(image_file, "rb") as f:
#         img_data = f.read()
#     b64_encoded = base64.b64encode(img_data).decode()
#     style = f"""
#         <style>
#         .stApp {{
#             background-image: url(data:image/png;base64,{b64_encoded});
#             background-size: cover;
#         }}
#         </style>
#     """
#     st.markdown(style, unsafe_allow_html=True)

def set_background(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            height: 100vh; /* Ukuran tinggi 100% dari viewport */
            width: 100vw; /* Ukuran lebar 100% dari viewport */
            margin: 0; /* Menghilangkan margin */
            padding: 0; /* Menghilangkan padding */
            overflow: hidden; /* Menghilangkan scroll jika konten melebihi ukuran */
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)