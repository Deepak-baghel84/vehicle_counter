import cv2

def open_webcam(source):
    cap = cv2.VideoCapture(source)  # Open the default webcam (0)
    # cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)

    try :
        camera_fps = int(cap.get(cv2.CAP_PROP_FPS))
    except :
        print(f"Issue with camera fps, not able to access video capture object properly. Setting camera fps to 15.")
        camera_fps = 15
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return None
    return cap, camera_fps