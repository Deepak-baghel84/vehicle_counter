from detector import Detection

class Test():
    def __init__(self, config):
        self.detector = Detection(config)

    def run(self):
        self.detector.run()

if __name__ == "__main__":
    config = {
        "device" : "cuda:0", #cpu
        "source" : "./istockphoto-2167097544-640_adpp_is.mp4",    
        "vid_stride" : 1,
        "visualize" : True,
        "track" : False,
        "person_only" : False
    }

    test = Test(config)
    test.run()
    