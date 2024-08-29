import cv2
import numpy as np

class Camera(object):

    def __init__(self, camera=1):
        # Attempt to connect to the FLIR Duo Pro R camera via OpenCV
        self.cam = cv2.VideoCapture(camera)
        self.valid = False
        try:
            if self.cam.isOpened():
                # Set properties for resolution, adjust as necessary
                self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Width for RGB stream
                self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080) # Height for RGB stream
                self.cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))  # Setting codec if necessary
                self.valid = True
                print("FLIR Duo Pro R connected and ready.")
            else:
                raise Exception("FLIR camera could not be opened.")
        except Exception as e:
            print(f"Camera initialization error: {e}")
            self.shape = None

    def get_frame(self):
        if self.valid:
            ret, frame = self.cam.read()
            if ret:
                # FLIR Duo Pro R provides RGB frames directly
                return frame
            else:
                print("Failed to capture frame from FLIR camera.")
                frame = np.ones((480, 640, 3), dtype=np.uint8)
                col = (0, 256, 256)
                cv2.putText(frame, "(Error: Frame capture failed)",
                            (65, 220), cv2.FONT_HERSHEY_PLAIN, 2, col)
                return frame
        else:
            frame = np.ones((480, 640, 3), dtype=np.uint8)
            col = (0, 256, 256)
            cv2.putText(frame, "(Error: Camera not accessible)",
                        (65, 220), cv2.FONT_HERSHEY_PLAIN, 2, col)
            return frame

    def release(self):
        if self.cam.isOpened():
            self.cam.release()
            print("FLIR camera released.")
        else:
            print("No camera to release.")
