from ultralytics import YOLO
import cv2
import time
import numpy as np

class ObjectDetector:
    def __init__(self):
        self.model_path = "best.pt"
        self.model = YOLO(self.model_path)
        self.cam = cv2.VideoCapture(0)
        if not self.cam.isOpened():
            raise Exception("No camera")
        self.frame_count = 0

    def run_realtime_detection(self):
        while True:
            ret, image = self.cam.read()
            if not ret:
                break

            self.frame_count += 1
            if self.frame_count % 5 == 0:
                _time_mulai = time.time()

                results = self.model.predict(image, show=False)[0]

                highest_score = 0
                best_box = None
                for box in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = box
                    if score > highest_score:
                        highest_score = score
                        best_box = box

                mask = np.ones_like(image, dtype=np.float32)
                if best_box is not None:
                    x1, y1, x2, y2, score, class_id = best_box
                    image[:, :int(x1), :] = (image[:, :int(x1), :].astype(np.float32) * 0.7).astype(np.uint8)  
                    image[:, int(x2):, :] = (image[:, int(x2):, :].astype(np.float32) * 0.7).astype(np.uint8)  
                    image[:int(y1), :, :] = (image[:int(y1), :, :].astype(np.float32) * 0.7).astype(np.uint8)  
                    image[int(y2):, :, :] = (image[int(y2):, :, :].astype(np.float32) * 0.7).astype(np.uint8)  

                    cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    cv2.putText(image, results.names[int(class_id)], (int(x1), int(y1 - 10)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                cv2.imshow("Deteksi Objek", image)
                print("Waktu deteksi:", time.time()-_time_mulai)

            _key = cv2.waitKey(1)
            if _key == ord('q'):
                break

        self.cam.release()
        cv2.destroyAllWindows()
