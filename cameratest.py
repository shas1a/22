import cv2

class Camera(object):
    def __init__(self):
        # Initialize the camera; 0 is the default camera
        self.video_source = 0  # Change this if you have multiple cameras
        self.vid = cv2.VideoCapture(self.video_source)

        if not self.vid.isOpened():
            raise Exception("Could not open video device")

    def __del__(self):
        # Release the camera when the object is destroyed
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        # Capture a frame from the camera
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Encode the frame as JPEG
                _, jpeg = cv2.imencode('.jpg', frame)
                return jpeg.tobytes()
        return None
