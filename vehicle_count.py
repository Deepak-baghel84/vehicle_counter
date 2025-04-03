import cv2
import numpy as np
import torch
from ultralytics import YOLO
import cvzone
from sort import *

#print(cv2.getBuildInformation())
#model = torch.hub.load("ultralytics/yolov5", "yolov5s") 
print("start capturing the frames...")
vid_cap = cv2.VideoCapture("./video.mp4")
#vid_cap.set(cv2.CAP_PROP_FPS,60)

tracker = Sort(max_age=40,iou_threshold=0.3)

count_frame = 0
count_obj_l,count_obj_r = 0,0
limits_l = [55,200,230,200]
limits_r = [280,225,485,225]


store_id = []

obj_lst = [2,5,7,9]

w = int(vid_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(vid_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("width,height",w,h)

while True :
    ret, frame = vid_cap.read()

    if not ret:
        print("unable to read frame")
        break

    frame = cv2.resize(frame,(500,350))
    model = YOLO("../Yolo-Weights/yolov8s.pt")
    out_frame = model(frame)
 

    for result in out_frame:
        dimensions = np.empty((0,5))
        boxes = result.boxes
        for box in boxes:
             x1,y1,x2,y2 = box.xyxy[0]
             x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)

             conf = round(box.conf[0].item(),3)
             #confidense = conf.item()
             cls = int(box.cls[0])

             w,h = (x2-x1),(y2-y1)
             cx,cy = (x1+w//2,y1+h//2)
             #cvzone.cornerRect(frame,(x1,y1,w,h),(255,0,0))
             if cls in obj_lst and conf > 0.35 and cy > 185:
                 cvzone.cornerRect(frame,(x1,y1,w,h),l=10,t=4,rt=2,colorR=(255,10,10),colorC=(101,214,191))
                 fps = vid_cap.get(cv2.CAP_PROP_FPS)
                 #print("frame ,class,conf",fps,cls,conf)

                 track_objs = np.array([x1,y1,x2,y2,conf])
                 dimensions = np.vstack((dimensions,track_objs))

                         # center of object
                 cv2.circle(frame,(cx,cy),3,(0,0,255),2,cv2.FILLED)
             
    cv2.line(frame,(limits_l[0],limits_l[1]),(limits_l[2],limits_l[3]),(242,148,65),3)
    cv2.line(frame,(limits_r[0],limits_r[1]),(limits_r[2],limits_r[3]),(242,148,65),3)
    tracked = tracker.update(dimensions)
    for track in tracked:
        x,y,x_,y_,id = track
        x,y,x_,y_,id = int(x),int(y),int(x_),int(y_),int(id)
        #print("track is:",track)
        w,h = (x_-x),(y_-y)
        cx,cy = (x+w//2,y+h//2)
        cvzone.putTextRect(frame,f"ID:{id}",(x,y-10),scale=1,thickness=1,colorR=(136,77,232),offset=5)
        
        if 50 < cx < 235  and 195  < cy < 205  :
            if id not in store_id:
                count_obj_l += 1
                cv2.line(frame,(limits_l[0],limits_l[1]),(limits_l[2],limits_l[3]),(16,16,255),3)
                store_id.append(id)
                
                #print("left_object_count:",count_obj)
        cvzone.putTextRect(frame,f"left_vehicles: {count_obj_l}",(25,30),scale=1,thickness=2,colorR=(100,222,220),colorT = (224,29,55))

        if 275 < cx < 490  and 220 < cy < 230 :
            if id not in store_id:
                count_obj_r += 1
                cv2.line(frame,(limits_r[0],limits_r[1]),(limits_r[2],limits_r[3]),(16,16,255),3)
                store_id.append(id)
                
                #print("left_object_count:",count_obj)
        cvzone.putTextRect(frame,f"right_vehicles: {count_obj_r}",(350,30),scale=1,thickness=2,colorR=(100,222,220),colorT = (224,29,55))


    count_frame += 1
    print("count_frame",count_frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    cv2.imshow("frame", frame)

    ##cv2.imwrite("./cv_practice/updated_video.mp4",frame)
    #cv2.waitKey(1)

vid_cap.release()
cv2.destroyAllWindows() 