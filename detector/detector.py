from ultralytics import YOLO
import threading
import time
import cv2
import numpy as np
from collections import deque

from cam_utils import open_webcam
from plot_utils import Plot

class Detection:
    def __init__(self, config):
        self.model = YOLO("yolov8m.pt")
        self.device = 'cuda:0' if config['device'].lower() == 'gpu' else 'cpu'
        self.visualize = config['visualize']
        self.conf = 0.3
        self.imgsz = 320
        self.classes = None  # Detect only 'Person' class
        self.source = config['source']
        self.vid_stride = config.get('vid_stride', 1)  # Default: process every frame
        self.running = True
        self.track = config['track']
        self.person_only = config['person_only']
        self.unique_person = set()
        self.plot = Plot()
        self.frame_idx = 0
        self.skip_count = 0

        if self.person_only:
            self.classes = 0
        # Open camera stream
        self.cap = cv2.VideoCapture(self.source)
        # self.cap, _ = open_webcam(self.source)
        assert self.cap.isOpened(), f"❌ Failed to open webcam {self.source}"

        # Get video properties
        self.w = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30  # Default to 30 FPS

        print(f"🎥 Camera FPS: {self.fps}")

        # Frame storage
        self.frames_queue = deque(maxlen=2)  # Store only 2 latest frames
        self.lock = threading.Lock()
        self.last_processed_frame = 0

        # Start video thread
        self.thread = threading.Thread(target=self.update, daemon=True)
        self.thread.start()

    def update(self):
        """Continuously grabs frames from the webcam and updates queue based on vid_stride."""
        frame_idx = 0
        print("🟢 Video thread started...")

        while self.running:
            success, frame = self.cap.read()  # Read frame directly instead of grab
            #frame = cv2.resize(frame,(720, 420))    
            if not success:
                print("⚠️ Webcam issue detected, resetting...")
                self.cap.release()
                time.sleep(1)  # Pause before reopening
                self.cap = cv2.VideoCapture(self.source)
                # self.cap, _ = open_webcam(self.source)
                continue  # Skip this iteration
                
            
            frame_idx += 1
            if frame_idx % self.vid_stride == 0:  # Process every `vid_stride` frame
                with self.lock:
                    self.frames_queue.clear()
                    self.frames_queue.append((frame_idx, frame))

            time.sleep(0.01)  # Reduce CPU load

    def process_result(self, results):
        """Processes detection results."""
        detections = []
        for result in results:
            if result.boxes:
                for box in result.boxes:
                    xywhn = box.xywhn[0].cpu().numpy().tolist()
                    confidence = box.conf.item()
                    class_id = int(box.cls.item())
                    detection = {"box": xywhn, "confidence": confidence, "class_id": class_id}
                    if self.track:
                        track_id = box.id.int().cpu().tolist()
                        detection['track_ids'] = track_id
                        self.unique_person.add(track_id[0])
                    detections.append(detection)
            else:
                detection = {"box": None, "confidence": None, "class_id": None}
                detections.append(detection)
            print(detections)

    def run(self):
        skip_count = 0
        """Runs YOLO detection loop with fresh frames from queue."""
        print("🚀 Detection loop started...")
        while self.running:
            if not self.thread.is_alive():
                print("❌ Video thread stopped unexpectedly! Restarting...")
                skip_count += 1
                if skip_count >= 5:     
                    break                      # stop threading after 5 unsuccessful attmpts
                self.thread = threading.Thread(target=self.update, daemon=True)
                self.thread.start()

            with self.lock:
                if self.frames_queue:
                    self.frame_idx, frame = self.frames_queue.popleft()  # Get latest frame
                    if self.frame_idx == self.last_processed_frame:
                        pass
                       # continue  # Skip repeated frames
                    self.last_processed_frame = self.frame_idx
                #else:
                   # continue  # Skip processing if no new frame

            print(f"🔄 Processing Frame No: {self.frame_idx}")

            # Run YOLO inference

            if self.track:
                results = self.model.track(source=frame, 
                    conf=self.conf, 
                    iou=0.5,
                    tracker="bytetrack.yaml", 
                    classes=self.classes,
                    show=False,
                    verbose=False)
                # frame = results[0].plot()
            else:
                results = self.model.predict(
                source=frame, 
                save=False, 
                imgsz=self.imgsz, 
                conf=self.conf, 
                classes=self.classes, 
                device=self.device, 
                verbose=False
            )

            frame = results[0].plot()

            self.process_result(results)

            # Display the webcam feed
            if self.visualize:
                self.plot.plot_stats(frame=frame, frame_count=self.frame_idx, person_count=len(self.unique_person))
                cv2.imshow("Webcam Feed", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.running = False
                    break
                
                    
                    

        self.cap.release()
        cv2.destroyAllWindows()
