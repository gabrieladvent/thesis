import os
from ultralytics import YOLO
import cv2
import numpy as np

video_path = 'set/vid5.mp4'
video_path_out = '{}_outmodel3.mp4'.format(video_path)

cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

if ret:
    H, W, _ = frame.shape
    out = cv2.VideoWriter(video_path_out, cv2.VideoWriter_fourcc(*'MP4V'), int(cap.get(cv2.CAP_PROP_FPS)), (W, H))

    model_path = os.path.join('testingFromLaptopFull/MODEL 2/TRAIN/best.pt')
    model = YOLO(model_path)

    threshold = 0.5

    while ret:
        results = model(frame)[0]

        mask = np.ones_like(frame, dtype=np.float32)
        for result in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = result

            if score > threshold:
                mask[int(y1):int(y2), int(x1):int(x2), :] = 0.7

                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv2.putText(frame, results.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)

        # Apply the mask to the frame
        frame = frame.astype(np.float32) * mask

        out.write(frame.astype(np.uint8))
        ret, frame = cap.read()

    cap.release()
    out.release()
    cv2.destroyAllWindows()
else:
    print("Failed to read video")
