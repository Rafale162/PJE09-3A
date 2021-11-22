import time
from classes.gesturemodel import GestureModel

class Scenario:
    def Run(self, mainPipe, capturePipe):
        self.mainPipe = mainPipe
        self.capturePipe = capturePipe

        self.lastLeft = None
        self.lastRight = None

        received = capturePipe.recv()
        self.gestureModel = GestureModel()
        self.gestureModel.SetImageSize(received)

        # Début scénario

        mode = "left"
        while True:
            r = self.Receive()
            if r == -1:
                break
            else:
                if self.CheckSigns(r, [["Left", "Rock"], ["Right", "Rock"]]):
                    break
                # Gauche
                if mode == "left":
                    msg = ["Gaucher simple"]
                    if self.CheckSigns(r, [["Left", "Pointer"]]) or self.CheckSigns(r, [["Left", "Write"]]):
                        point = self.GetHandPoint("Left", 8)
                        msg.append("Ecriture - x:" + str(point[0]) + " / y:" + str(point[1]))
                    msg.append("")

                    msg.append("Droite/Pouce en l'air : Mode droitier")
                    if self.CheckSigns(r, [["Right", "ThumbUp"]]):
                        mode = "right"

                    msg.append("Droite/Pouce en bas : Mode gaucher mixte")
                    if self.CheckSigns(r, [["Right", "ThumbDown"]]):
                        mode = "left-mixed"

                # Gauche Mixte
                if mode == "left-mixed":
                    msg = ["Gaucher mixte"]
                    if self.CheckSigns(r, [["Right", "Pointer"]]):
                        point = self.GetHandPoint("Left", 8)
                        msg.append("Ecriture - x:" + str(point[0]) + " / y:" + str(point[1]))
                    msg.append("")

                    msg.append("Droite/Pouce en l'air : Mode droitier")
                    if self.CheckSigns(r, [["Right", "ThumbUp"]]):
                        mode = "right"

                    msg.append("Droite/Rock : Mode gaucher simple")
                    if self.CheckSigns(r, [["Right", "Rock"]]):
                        mode = "left"

                # Droite
                if mode == "right":
                    msg = ["Droitier simple"]
                    if self.CheckSigns(r, [["Right", "Pointer"]]) or self.CheckSigns(r, [["Right", "Write"]]):
                        point = self.GetHandPoint("Right", 8)
                        msg.append("Ecriture - x:" + str(point[0]) + " / y:" + str(point[1]))
                    msg.append("")

                    msg.append("Gauche/Pouce en l'air : Mode gaucher")
                    if self.CheckSigns(r, [["Left", "ThumbUp"]]):
                        mode = "left"

                    msg.append("Gauche/Pouce en bas : Mode droitier mixte")
                    if self.CheckSigns(r, [["Left", "ThumbDown"]]):
                        mode = "right-mixed"

                # Droitier Mixte
                if mode == "right-mixed":
                    msg = ["Droitier mixte"]
                    if self.CheckSigns(r, [["Left", "Pointer"]]):
                        point = self.GetHandPoint("Right", 8)
                        msg.append("Ecriture - x:" + str(point[0]) + " / y:" + str(point[1]))
                    msg.append("")

                    msg.append("Gauche/Pouce en l'air : Mode gaucher")
                    if self.CheckSigns(r, [["Left", "ThumbUp"]]):
                        mode = "left"

                    msg.append("Gauche/Rock : Mode droitier simple")
                    if self.CheckSigns(r, [["Left", "Rock"]]):
                        mode = "right"

                self.PrintOnScreen(msg)

        # Fin scénario

        mainPipe.send("exit")
        capturePipe.recv()

    def Wait(self, timeout):
        start = time.time()
        while time.time() < start + timeout:
            if self.capturePipe.poll(0):
                self.capturePipe.recv()

    def Receive(self):
        received = self.capturePipe.recv()
        if received == "exit":
            return -1
        elif received is not None and received != []:
            rList = []
            for hand in received:
                rList.append([hand.GetSide(), self.gestureModel.GetSign(hand)])
                if hand.GetSide() == "Left":
                    self.lastLeft = hand
                if hand.GetSide() == "Right":
                    self.lastRight = hand
            return rList

    def GetHandPoint(self, side, id):
        if side == "Left":
            return self.gestureModel.GetPoint(self.lastLeft, id)
        if side == "Right":
            return self.gestureModel.GetPoint(self.lastRight, id)
        return []

    def CheckSigns(self, toCheck, conditionList):
        if toCheck == None:
            return False
        for cond in conditionList:
            if cond not in toCheck:
                return False
        return True

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
            