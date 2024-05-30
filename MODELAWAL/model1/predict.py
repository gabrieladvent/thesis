
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('best.pt')
data = '../vali/test.mp4'

# Run inference on 'bus.jpg' with arguments
model.predict(data, save=True, imgsz=320, conf=0.5)