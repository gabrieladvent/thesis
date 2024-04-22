import cv2
import numpy as np
import random
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self):
        self.model = YOLO('best.pt')

    def draw_boxes_video(self, image, detections_list, labels_list):
        img = np.array(image)
        for detections, labels in zip(detections_list, labels_list):
            for box, label in zip(detections, labels):
                box = [int(coord) for coord in box]
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), color, 5)
                cv2.putText(img, label, (box[0], box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
        
        return img

    def image_classify(self, image):
        source = image
        results = self.model(source, stream=True)
        
        boxes = []
        labels = []
        for result in results:
            box = result.boxes.xyxy
            boxes.append(box)
            for cls_idx in result.boxes.cls.tolist():
                label = self.model.names[cls_idx]
                labels.append(label)
        
        return boxes, labels

    def video_classify(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
    
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
    
            detections, labels = self.image_classify(frame)
            frame_with_boxes = self.draw_boxes_video(frame, detections, labels)
            frames.append(frame_with_boxes)
    
        cap.release()
    
        return frames

# Membuat objek dari class ObjectDetector
detector = ObjectDetector()

# Memanggil metode video_classify untuk memproses video
video_frames = detector.video_classify('G:/SKRIPSI/tempvid.mp4')

# Mendefinisikan properti video seperti lebar, tinggi, dan frame rate
height, width, _ = video_frames[0].shape
fps = 30.0

# Membuat objek untuk menyimpan video dengan format MP4
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('output.mp4', fourcc, fps, (width, height))

# Menyimpan setiap frame ke dalam video
for frame in video_frames:
    out.write(frame)

# Menutup file video
out.release()
