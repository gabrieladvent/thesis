import cv2
import os
from tqdm import tqdm

dataset_path = 'data'
save_path = 'result'
os.makedirs(save_path, exist_ok=True)

files = os.listdir(dataset_path)
for file in tqdm(files, desc='Processing images', unit='image'):
    image = cv2.imread(os.path.join(dataset_path, file))
    resized_image = cv2.resize(image, (416, 416))
    cv2.imwrite(os.path.join(save_path, file.split('.')[0] + '_resized.jpg'), resized_image)
    
    rows, cols, _ = resized_image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), 10, 1)
    rotated_image = cv2.warpAffine(resized_image, M, (cols, rows))
    cv2.imwrite(os.path.join(save_path, file.split('.')[0] + '_rotated.jpg'), rotated_image)
    
    greyscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(save_path, file.split('.')[0] + '_greyscale.jpg'), greyscale_image)
    
    exposure_adjusted_image = cv2.convertScaleAbs(resized_image, alpha=1.5, beta=0)
    cv2.imwrite(os.path.join(save_path, file.split('.')[0] + '_exposure.jpg'), exposure_adjusted_image)
