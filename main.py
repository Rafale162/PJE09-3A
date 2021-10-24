import copy
import cv2
import sys
from multiprocessing import Process, Pipe
from classes.capture import Capture
from classes.scenario import Scenario

class Main:

    def Setup(self):

        self.exit = False
        self.mode = 0
        self.capture = Capture()
        self.scenario = Scenario()

    def Run(self):
        self.captureMainPipe, mcCapturePipe = Pipe()
        self.scenarioMainPipe, msScenarioPipe = Pipe()
        scScenarioPipe, scCapturePipe = Pipe()

        self.captureProcess = Process(target = self.capture.Run, args = (mcCapturePipe, scCapturePipe))
        self.scenarioProcess = Process(target = self.scenario.Run, args = (msScenarioPipe, scScenarioPipe))
        
        self.captureProcess.start()
        self.scenarioProcess.start()

        while True:
            received = self.scenarioMainPipe.recv()
            if received == "exit":
                self.Stop()
                break
        

    def Stop(self):
        self.captureMainPipe.send("exit")
        self.captureProcess.join()
        self.scenarioProcess.join()

if __name__ == '__main__':
    app = Main()
    app.Setup()
    app.Run()