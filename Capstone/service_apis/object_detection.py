import os
import uuid
import cv2
import subprocess
from collections import Counter
from ultralytics import YOLO
from django.conf import settings
BASE_DIR = settings.BASE_DIR
MODEL_NAME = "yolov8m.pt"
TRAINED_MODEL_NAME = "trained_model_v1_5cls.pt"


model_path = os.path.join(BASE_DIR, MODEL_NAME)
model = YOLO(model_path)  # Detection model path
class_names = model.names
img_resolution = 640
confidence = 0.6

trained_model_path = os.path.join(BASE_DIR, TRAINED_MODEL_NAME)
trained_model = YOLO(trained_model_path)  # Detection model path
trained_class_names = trained_model.names


def counter(classes): 
	counts = dict(Counter(classes))
	duplicates = {key:value for key, value in counts.items() if value > 0}
	return duplicates

def detect(img):
	base_model_flag = False
	trained_model_flag = False
	cal = []
	results = model.predict(source=img, 
							imgsz=img_resolution, 
							conf=0.8,
							save=False
							)  # predict on an images
	tensor_list = results[0].boxes.data
	detection = tensor_list.tolist()
	total_products = len(detection)
	if total_products > 0:
		print('total_products from base model: ', total_products)
		for det in detection:
			x,y,w,h,_,cls = [int(d) for d in det]
			cal.append(str(class_names[int(cls)]))
			# add detected images 
			# if SAVE:
			img = cv2.rectangle(img,(x,y),(w,h), (0,0,255), 2)
			cv2.putText(img, str(class_names[int(cls)]), (x, y-10), 4, 0.6, (255,125,120), 1)
			base_model_flag = True
	else:
		base_model_flag = False
		print('No products detected from base model')
	
	trained_results = trained_model.predict(source=img, 
							imgsz=img_resolution, 
							conf=confidence,
							save=False
							)  # predict on an images
	trained_tensor_list = trained_results[0].boxes.data
	trained_detection = trained_tensor_list.tolist()
	trained_total_products = len(trained_detection)
	if trained_total_products > 0:
		print('total_products from trained model: ', trained_total_products)
		for det in trained_detection:
			x,y,w,h,_,cls = [int(d) for d in det]
			cal.append(str(trained_class_names[int(cls)]))
			# add detected images 
			# if SAVE:
			img = cv2.rectangle(img,(x,y),(w,h), (0,0,255), 2)
			cv2.putText(img, str(trained_class_names[int(cls)]), (x, y-10), 4, 0.6, (255,125,120), 1)
			trained_model_flag = True
	else:
		trained_model_flag = False
		print('No products detected from trained model')
	

	# filename = f"{uuid.uuid4().hex}.jpg"
	# savepath = os.path.join(ROOT, filename)
	# subprocess.run(f"rm -rf {ROOT}/*.jpg".split())
	# cv2.imwrite(savepath, img)
	if base_model_flag or trained_model_flag:
		sum_of_products = total_products + trained_total_products
		product_count = dict(sorted((counter(cal)).items()))
		return product_count, sum_of_products
	else:
		return {}, 0
