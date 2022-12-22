import torch
import cv2
import numpy as np
from . models import Model_weight

weight = Model_weight.objects.get(caption='yolov5')
weight_file_path = weight.model.path

def detection(frame, model):
    frame = [frame]
    results = model(frame)

    labels, coordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    return labels, coordinates

def plot_boxes(results, frame, classes):

    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    # Looping through all the detections
    for i in range(n):
        cor = cord[i]
        if cor[i] >= 0.55: # threshold value for detection 
            print(f'[INFO] Extracting BBox coordinates...')
            x1, y1, x2, y2 = int(cor[0]*x_shape), int(cor[1]*y_shape), int(cor[2]*x_shape), int(cor[3]*y_shape) # BBox coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # BBox
            val = [True,frame]
            return val

def main(img_path=None, vid_path=None):
    
    print(f'[info] Loading model.....')
    # loading the custom training model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=weight_file_path, force_reload=True)
    Classes = model.names 
    if vid_path != None:
        print(f'[INFO] working with video: {vid_path}')
        cap = cv2.VideoCapture(vid_path)

        frame_no = 1

        imageList = []
        while True:
            ret, frame = cap.read()
            if ret and frame_no % 1 == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = detection(frame, model=model)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                try:
                    t,frame = plot_boxes(results, frame, classes=Classes)
                except:
                    t = False

                if t:
                    cv2.imwrite("media/output/frame%d.jpg" % frame_no, frame)
                    imageList.append("media/output/frame%d.jpg" % frame_no)
                frame_no += 1
            else:
                break

    return imageList





