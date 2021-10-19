import cv2

class Camera:

    def __init__(self, id):
        self.cam = cv2.VideoCapture(id)
        self.SetResolution(1280, 720)

    def SetResolution(self, width, height):
        self.width = width
        self.height = height
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def GetResolution(self):
        return self.width, self.height

    def IsOpen(self):
        return self.cam.isOpened()

    def Stop(self):
        self.cam.release()
        cv2.destroyAllWindows()

    def GetImage(self):
        if self.cam.isOpened():
            success, image = self.cam.read()
            if not success:
                print("[ERREUR] Flux vidéo vide")
                return False
            image = cv2.flip(image, 1)
            return image
        print("[ERREUR] Flux vidéo non ouvert")
        return False