import cv2
import sys
from utils import CvFpsCalc
from threading import Thread
from classes.camera import Camera
from classes.gesturemodel import GestureModel
from classes.displayer import Displayer
from classes.scenario import Scenario

class Main:

    def Setup(self):

        self.exit = False
        self.mode = 0
        self.camera = Camera(0)
        self.gestureModel = GestureModel()
        self.displayer = Displayer()
        self.gestureModel.SetImageSize(self.camera.GetResolution())
        self.scenario = Scenario()

    def Run(self):

        self.cvFpsCalc = CvFpsCalc(buffer_len=10)
        self.shared = type('', (), {})()
        self.shared.hands = []

        self.captureThread = Thread(target = self.Capture, args = (self.shared,))
        self.scenarioThread = Thread(target = self.scenario.Run, args = (self, self.shared,))
        
        self.captureThread.start()
        self.scenarioThread.start()

    def Stop(self):
        self.exit = True
        sys.exit()

    def Capture(self, resources):
        while self.camera.IsOpen() and not self.exit:
            fps = self.cvFpsCalc.get()
            image = self.camera.GetImage()
            hands = self.gestureModel.GetHands(image)
            resources.hands = hands
            self.displayer.ResetImage(image)

            for hand in hands:
                self.displayer.AnnoteHand(hand, self.gestureModel)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

            number, self.mode = self.gestureModel.SelectMode(key, self.mode)
            self.displayer.ShowAnnoted(fps, self.mode, number)

        self.camera.Stop()

if __name__ == '__main__':
    app = Main()
    app.Setup()
    app.Run()