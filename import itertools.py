import itertools
import pandas as pd

optimizer_list = ['AdamW', 'Adam']
lr_list = [0.0001]
yolov8_list = ['n', 's', 'm', 'l', 'x']
size_list = [240, 256, 480]
batch_list = [16, 32, 64]
decay_list = [0.0005]
momentum_list = [0.937, 0.8]

results = []

for optimizer, lr, yolov8, imgsz, batch, decay, momentum in itertools.product(optimizer_list, lr_list, yolov8_list, size_list, batch_list, decay_list, momentum_list):
    command = f" model=yolov8{yolov8}.pt epochs=200 imgsz='{imgsz}' optimizer='{optimizer}' lr0='{lr}' batch='{batch}' decay='{decay}' momentum='{momentum}'"
    results.append({'Optimizer': optimizer, 'Learning Rate': lr, 'YOLOv8': yolov8, 'Image Size': imgsz, 'Batch Size': batch, 'Decay': decay, 'Momentum': momentum})

df = pd.DataFrame(results)
df.to_excel('results.xlsx', index=False)
