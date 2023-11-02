from picamera2 import Picamera2
import cv2
import time
from ultralytics import YOLO
    
#Below determines the size of the live feed window that will be displayed on the Raspberry Pi OS
if __name__ == "__main__":
    model = YOLO("yolov8n.pt")  # load a pretrained model

    picam2 = Picamera2()
    picam2.start()
    time.sleep(1)
    
    done = 0
    while done < 10:
        start_time = time.time()
        image = picam2.capture_image("main")

        # from ndarray
        results = model.predict(source=image, device = 'cpu', \
            verbose = True, save=False, save_txt=False)  # save predictions as labels
        
        result =  results[0]
        print('coordinate:', result.boxes.xyxy.cpu().numpy())
        print('conf:', result.boxes.conf.cpu().numpy())
        print('class:', result.boxes.cls.cpu().numpy())        
        end_time = time.time()        
        print(f"elapsed time: {end_time - start_time}")
        
        done+= 1
