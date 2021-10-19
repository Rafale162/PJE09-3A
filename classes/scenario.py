from time import sleep

class Scenario:

    def Run(self, app, shared):
        hands = shared.hands

        print("Ouvrez la main gauche")
        self.WaitFor(app, shared, "Left", "Open")
        print("OK")

        print("Fermez la main gauche")
        self.WaitFor(app, shared, "Left", "Close")
        print("OK")

        print("Pouce droit en l'air")
        self.WaitFor(app, shared, "Right", "ThumbUp")
        print("OK")

        app.Stop()

    def WaitFor(self, app, shared, side, sign):
        class EndLoop(Exception): pass
        loop = True
        try:
            while loop:
                if app.exit:
                    raise EndLoop
                for hand in shared.hands:
                    if hand.GetSide() == side:
                        if app.gestureModel.GetSign(hand) == sign:
                            loop = False
                sleep(.5)
        except EndLoop:
            pass
            