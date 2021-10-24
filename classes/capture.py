import copy
import cv2
from classes.camera import Camera
from classes.cvfpscalc import CvFpsCalc
from classes.displayer import Displayer
from classes.gesturemodel import GestureModel

class Capture:

    def Run(self, mainPipe, scenarioPipe):
        self.mainPipe = mainPipe
        self.scenarioPipe = scenarioPipe

        self.mode = 0
        self.camera = Camera(0)
        self.gestureModel = GestureModel()
        self.displayer = Displayer()
        self.gestureModel.SetImageSize(self.camera.GetResolution())
        self.cvFpsCalc = CvFpsCalc(buffer_len=10)
        self.scenarioPipe.send(self.camera.GetResolution())
        text = ""
        
        while self.camera.IsOpen():
            if self.mainPipe.poll(0):
                if self.mainPipe.recv() == "exit":
                    break

            if self.scenarioPipe.poll(0):
                received = self.scenarioPipe.recv()
                if isinstance(received, list) and len(received) == 1:
                    text = received[0]

            fps = self.cvFpsCalc.get()
            image = self.camera.GetImage()
            hands = self.gestureModel.GetHands(image)
            self.scenarioPipe.send(hands)

            self.displayer.ResetImage(image)
            for hand in hands:
                self.displayer.AnnoteHand(hand, self.gestureModel)

            key = cv2.waitKey(1)
            if key == 27:  # ESC
                break

            number, self.mode = self.gestureModel.SelectMode(key, self.mode)
            self.displayer.WriteText(text)
            self.displayer.ShowAnnoted(fps, self.mode, number)

        scenarioPipe.send("exit")
        self.camera.Stop()