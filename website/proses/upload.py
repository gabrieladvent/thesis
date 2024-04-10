import cv2
from ultralytics import YOLO
import numpy as np
import random
import streamlit as st
import base64
from tempfile import NamedTemporaryFile


model = YOLO('best.pt', verbose=False)

def draw_boxes(image, boxes, labels):
    img = np.array(image)
    for box, label in zip(boxes, labels):
        box = [int(coord) for coord in box]
        color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 5)
        cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    
    return img


def image_classify(image):
    source = image
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
    cap = cv2.VideoCapture(video_path)
    frames = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Pastikan setiap frame memiliki ukuran yang sama
        frame = cv2.resize(frame, (240, 240))

        detections, labels = image_classify(frame)
        frame_with_boxes = draw_boxes_video(frame, detections, labels)
        frames.append(frame_with_boxes)

    cap.release()

    return frames



def draw_boxes_video(image, detections_list, labels_list):
    img = np.array(image)
    for detections, labels in zip(detections_list, labels_list):
        for box, label in zip(detections, labels):
            box = [int(coord) for coord in box]
            color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
            cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 5)
            cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
    return img


def create_video(frames):
    height, width, _ = frames[0].shape
    fps = 30.0

    # Membuat objek untuk menyimpan video dengan format MP4
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    temp_file = NamedTemporaryFile(delete=False, suffix='.mp4')
    out = cv2.VideoWriter(temp_file.name, fourcc, fps, (width, height))

    # Menyimpan setiap frame ke dalam video
    for frame in frames:
        out.write(frame)

    # Menutup file video
    out.release()

    return temp_file.name
















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