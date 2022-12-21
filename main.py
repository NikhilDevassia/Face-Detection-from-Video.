
import torch
import cv2
import numpy as np

def detection(frame, model):
    frame = [frame]
    print(f'[INFO] Detecting.....')
    results = model(frame)

    labels, coordinates = results.xyxyn[0][:, -1], results.xyxyn[0][:, :-1]

    return labels, coordinates

def plot_boxes(results, frame, classes):

    labels, cord = results
    n = len(labels)
    x_shape, y_shape = frame.shape[1], frame.shape[0]

    print(f'[INFO] Total {n} detections.....')
    print(f'[INFO] Looping through all detections.....')

    # Looping through all the detections
    for i in range(n):
        cor = cord[i]
        if cor[i] >= 0.55: # threshold value for detection 
            print(f'[INFO] Extracting BBox coordinates...')
            x1, y1, x2, y2 = int(cor[0]*x_shape), int(cor[1]*y_shape), int(cor[2]*x_shape), int(cor[3]*y_shape) # BBox coordinates
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) # BBox
            return frame
            
def main(img_path=None, vid_path=None):
    
    print(f'[info] Loading model.....')
    # loading the custom training model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path='last.pt', force_reload=True)
    Classes = model.names 


    # Detection on image and saving image
    if img_path != None:
        print(f"[INFO] Working with image: {img_path}")
        img_out_name = f"./output/result{img_path.split('/')[-1]}"

        frame = cv2.imread(img_path)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = detection(frame, model = model) # detection function

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame = plot_boxes(results, frame, Classes)

        # cv2.namedWindow('window', cv2.WINDOW_NORMAL) # creating a window to show the results

        while True:
            cv2.imshow('window', frame)

            if cv2.waitKey(5) & 0xFF == ord('q'):
                print(f'[INFO] Exiting.....')

                cv2.imwrite(f'{img_out_name}', frame) # if want to save the output
                break
    
    # for detection on video
    elif vid_path != None:
        print(f'[INFO] working with video: {vid_path}')
        vid_out_name = f"./output/result{vid_path.split('/')[-1]}"

        # reading the video 
        cap = cv2.VideoCapture(vid_path)

        # assert cap.isOpened()
        frame_no = 1

        # cv2.namedWindow('vid_out', cv2.WINDOW_NORMAL)
        while True:
            ret, frame = cap.read()
            if ret and frame_no % 1 == 0:
                print(f'[INFO] Working with frame {frame_no}')

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = detection(frame, model=model)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

                frame = plot_boxes(results, frame, classes=Classes)

                cv2.imwrite("output/result/frame%d.jpg" % frame_no, frame)
                frame_no += 1


main(vid_path='pexels-marc-espejo-6548176.mp4')



