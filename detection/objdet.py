from picamera2 import Picamera2
import cv2
import time
import os
import matplotlib.pyplot as plt
from ultralytics import YOLO
import random
import numpy as np

def save_img(image, pixel_coords, confs, objs, cls, chosen_index, output_path):
    print(cls)
    for i, coords in enumerate(pixel_coords):
        thickness = 1 if i != chosen_index else 3
        color = (0,255,0) if i== chosen_index else (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        cv2.rectangle(image, (int(coords[0]), int(coords[1])), (int(coords[2]), int(coords[3])), color, thickness)
        cv2.putText(image, f'{str(int(objs[i]))} {cls[i]}: {str(round(confs[i], 2))}', (int(coords[0]), int(coords[1]) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    
    cv2.imwrite(output_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

def obj_det(
        target_objs = [39, 75], 
        conf_threshold = 0.3,
        folder = 'runs',
        ):
    #Get all target objs that is 39 (bottle) or 75 (vase)
    model = YOLO("yolov8n.pt")  # load a pretrained model

    picam2 = Picamera2()
    picam2.start()
    time.sleep(1)
    
    done = False
    while not done:
        start_time = time.time()
        image = picam2.capture_image("main")
        print(f"Image size: {image.size}")
        # from ndarray
        results = model.predict(source=image, device = 'cpu', \
            verbose = True, save=False, save_txt=False)  # save predictions as labels
            
        cls_names = model.names
        result =  results[0]
        
        objs = result.boxes.cls.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        pixel_coords = result.boxes.xyxy.cpu().numpy()
        cls = [cls_names[int(index)] for index in result.boxes.cls.cpu()]
        print('coordinate:', pixel_coords)
        print('conf:', confs)
        print('class:', objs)      
        print('cls_name: ', cls)  
        end_time = time.time()        
        print(f"elapsed time: {end_time - start_time}")
        
        for index, obj in enumerate(objs):
            print(obj, confs[index], target_objs )
            if obj in target_objs and confs[index] >= conf_threshold:
                save_img(np.array(image),pixel_coords= pixel_coords, confs = confs, objs = objs, cls = cls, chosen_index = index, output_path = os.path.join(folder, 'captured.png'))
                return obj, confs[index], pixel_coords[index], cls[index]

#Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":  
    result = obj_det()
    print(result)
