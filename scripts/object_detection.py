from imageai.Detection import ObjectDetection
import os

current_directory = os.getcwd()

detector = ObjectDetection()

detector.setModelTypeAsTinyYOLOv3()

detector.setModelPath(os.path.join(current_directory , "yolo-tiny.h5"))

detector.loadModel()

detections = detector.detectObjectsFromImage(
input_image = os.path.join(current_directory, "yes.jpg"), 
output_image_path = os.path.join(current_directory , "traffic_detected.jpg")
)
for eachObject in detections:
    print(
         eachObject["name"] , " : ",
         eachObject["percentage_probability"], " : ",
         eachObject["box_points"] )
    print("--------------------------------")