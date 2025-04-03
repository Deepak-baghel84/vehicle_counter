import cv2
import cvzone

class Plot():
    def __init__(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_scale = 1
        self.font_thickness = 2
        self.text_color = (255, 255, 255)  # White text
        self.bg_color = (100, 100, 100)  # Dark Grey background
        self.set_frame_text_size = False
        self.set_count_text_size = False
        self.text_size = None
        self.text_w = None
        self.text_h = None
        self.padding = 0

        self.get_text_size(f"Frame count: {10000}", type="frame")
        self.get_text_size(f"Person count: {10000}", type="person")


    def get_text_size(self, text, type="frame"):
        # Get text size
        
        if type=="frame":
            self.text_size_f, _ = cv2.getTextSize(text, self.font, self.font_scale, self.font_thickness)
            self.set_frame_text_size = True
        else : 
            self.text_size_p, _ = cv2.getTextSize(text, self.font, self.font_scale, self.font_thickness)
            self.set_count_text_size = True

            self.text_w = max(self.text_size_f[0], self.text_size_p[0])  # Width of the widest text
            self.text_h = self.text_size_f[1] + self.text_size_p[1] + 10

            self.padding = 10
            self.x, self.y = self.padding, self.padding + self.text_size_f[1]


    def plot_stats(self, frame, frame_count, person_count):
        
        text1 = f"Person count: {person_count}"
        text2 = f"Frame count: {frame_count}"
        
        #cv2.rectangle(frame, 
      #          (self.x - 5, self.y + self.text_size_p[1] + 10), 
       #         (self.x + self.text_w + 10, self.y + self.text_size_p[1] + 10), 
        #        self.bg_color, -1)
        w = (self.x + self.text_w + 10-self.x - 5)
        h = (self.y + self.text_size_p[1] + 10-self.y + self.text_size_p[1] + 10)

        cvzone.cornerRect(frame,(self.x - 5, self.y + self.text_size_p[1] + 10,w,h),l=20,rt=5,colorR=(101,214,191))
        # Draw background rectangle
        #cv2.putText(frame, text1, (self.x, self.y), self.font, self.font_scale, self.text_color, self.font_thickness, cv2.LINE_AA)
        #cv2.putText(frame, text2, (self.x, self.y + self.text_size_f[1] + 5), self.font, self.font_scale, self.text_color, self.font_thickness, cv2.LINE_AA)
        cvzone.putTextRect(frame,text1,(self.x, self.y))
        cvzone.putTextRect(frame,text2,(self.x, self.y + self.text_size_f[1] + 30))
 #,self.font_scale,self.font_thickness,colorR=(230,218,96)
 #,self.font_scale,self.font_thickness,colorR=(230,218,96)