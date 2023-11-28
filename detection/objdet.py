from picamera2 import Picamera2
import cv2
import time
from ultralytics import YOLO

def obj_det(target_objs = [39, 75], conf_threshold = 0.5):
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
        
        result =  results[0]
        objs = result.boxes.cls.cpu().numpy()
        confs = result.boxes.conf.cpu().numpy()
        pixel_coords = result.boxes.xyxy.cpu().numpy()
        print('coordinate:', pixel_coords)
        print('conf:', confs)
        print('class:', objs)        
        end_time = time.time()        
        print(f"elapsed time: {end_time - start_time}")
        
        for index, obj in enumerate(objs):
            if obj in target_objs and confs[index] >= conf_threshold:
                return obj, confs[index], pixel_coords[index]

#Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":  
    result = obj_det()
    print(result)
