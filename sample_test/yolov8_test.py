from ultralytics import YOLO
import cv2


# Load a model
# model = YOLO("yolov8n.yaml")  # build a new model from scratch
model = YOLO("yolov8n.pt")  # load a pretrained model (recommended for training)

# path = model.export(format="onnx")  # export the model to ONNX format

# from ndarray
im2 = cv2.imread("in/sample.png")
results = model.predict(source=im2, save=False, save_txt=False)  # save predictions as labels

result =  results[0]
print('coordinate:', result.boxes.xyxy.cpu().numpy())
print('conf:', result.boxes.conf.cpu().numpy())
print('class:', result.boxes.cls.cpu().numpy())