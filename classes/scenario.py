import time
from classes.gesturemodel import GestureModel

class Scenario:
    def Run(self, mainPipe, capturePipe):
        self.mainPipe = mainPipe
        self.capturePipe = capturePipe

        received = capturePipe.recv()
        self.gestureModel = GestureModel()
        self.gestureModel.SetImageSize(received)

        self.PrintOnScreen("Ouvrez la main gauche")
        self.WaitFor("Left", "Open")
        self.PrintOnScreen("OK")

        self.Wait(2)

        self.PrintOnScreen("Fermez la main gauche")
        self.WaitFor("Left", "Close")
        self.PrintOnScreen("OK")

        self.Wait(2)

        self.PrintOnScreen("Pouce droit en l'air")
        self.WaitFor("Right", "ThumbUp")
        self.PrintOnScreen("OK")

        mainPipe.send("exit")
        capturePipe.recv()

    def Wait(self, timeout):
        start = time.time()
        while time.time() < start + timeout:
            if self.capturePipe.poll(0):
                self.capturePipe.recv()

    def WaitFor(self, side, sign):
        keep = True
        while keep:
            received = self.capturePipe.recv()
            if received == "exit":
                break
            if received is not None and received != []:
                for hand in received:
                    if hand.GetSide() == side:
                        if self.gestureModel.GetSign(hand) == sign:
                            keep = False
    
    def PrintOnScreen(self, msg):
        self.capturePipe.send([msg])
            