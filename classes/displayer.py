import copy
import numpy as np
import cv2 as cv

class Displayer:

    def __init__(self):
        self.image = None

    def ResetImage(self, image):
        self.image = copy.deepcopy(image)

    def Show(self, image):
        cv.imshow('Flux video', image)

    def AnnoteHand(self, hand, gestureModel):
        brect = self.CalcBoundingRect(hand.GetLandmarks())
        self.DrawBoundingRect(brect)
        self.DrawLandmarks(hand)
        self.DrawInfoText(brect, hand.GetHandedness(), gestureModel.GetSign(hand))

    def ShowAnnoted(self, fps, mode, number):
        self.DrawInfo(fps, mode, number)
        cv.imshow('Flux video', self.image)

    def CalcBoundingRect(self, landmarks):
        imageWidth, imageHeight = self.image.shape[1], self.image.shape[0]
        landmarkArray = np.empty((0, 2), int)
        for _, landmark in enumerate(landmarks.landmark):
            landmarkX = min(int(landmark.x * imageWidth), imageWidth - 1)
            landmarkY = min(int(landmark.y * imageHeight), imageHeight - 1)
            landmarkPoint = [np.array((landmarkX, landmarkY))]
            landmarkArray = np.append(landmarkArray, landmarkPoint, axis=0)
        x, y, w, h = cv.boundingRect(landmarkArray)
        return [x, y, x + w, y + h]

    def DrawLandmarks(self, hand):
        lmp = hand.GetLandmarkList(self.image)
        if len(lmp) > 0:
            # Thumb
            self.DrawLandmarkLine(lmp, 2, 3)
            self.DrawLandmarkLine(lmp, 3, 4)

            # Index finger
            self.DrawLandmarkLine(lmp, 5, 6)
            self.DrawLandmarkLine(lmp, 6, 7)
            self.DrawLandmarkLine(lmp, 7, 8)

            # Middle finger
            self.DrawLandmarkLine(lmp, 9, 10)
            self.DrawLandmarkLine(lmp, 10, 11)
            self.DrawLandmarkLine(lmp, 11, 12)

            # Ring finger
            self.DrawLandmarkLine(lmp, 13, 14)
            self.DrawLandmarkLine(lmp, 14, 15)
            self.DrawLandmarkLine(lmp, 15, 16)

            # Little finger
            self.DrawLandmarkLine(lmp, 17, 18)
            self.DrawLandmarkLine(lmp, 18, 19)
            self.DrawLandmarkLine(lmp, 19, 20)

            # Palm
            self.DrawLandmarkLine(lmp, 0, 1)
            self.DrawLandmarkLine(lmp, 1, 2)
            self.DrawLandmarkLine(lmp, 2, 5)
            self.DrawLandmarkLine(lmp, 5, 9)
            self.DrawLandmarkLine(lmp, 9, 13)
            self.DrawLandmarkLine(lmp, 13, 17)
            self.DrawLandmarkLine(lmp, 17, 0)

        # Key Points
        for index, landmark in enumerate(lmp):
            if index != 0 & index % 4 == 0:
                a = 8
            else:
                a =  5
            if index >= 0 and index <= 20:
                cv.circle(self.image, (landmark[0], landmark[1]), a, (255, 255, 255), -1)
                cv.circle(self.image, (landmark[0], landmark[1]), a, (0, 0, 0), 1)

    def DrawLandmarkLine(self, l, a, b):
        cv.line(self.image, tuple(l[a]), tuple(l[b]), (0, 0, 0), 6)
        cv.line(self.image, tuple(l[a]), tuple(l[b]), (255, 255, 255), 2)

    def DrawBoundingRect(self, brect):
        cv.rectangle(self.image, (brect[0], brect[1]), (brect[2], brect[3]), (0, 0, 0), 1)

    def DrawInfoText(self, brect, handedness, handSignText):
        cv.rectangle(self.image, (brect[0], brect[1]), (brect[2], brect[1] - 22), (0, 0, 0), -1)

        infoText = handedness.classification[0].label[0:]
        if handSignText != "":
            infoText = infoText + ':' + handSignText
        cv.putText(self.image, infoText, (brect[0] + 5, brect[1] - 4),
                cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)

    def DrawPointHistory(self, pointHistory):
        for index, point in enumerate(pointHistory):
            if point[0] != 0 and point[1] != 0:
                cv.circle(self.image, (point[0], point[1]), 1 + int(index / 2), (152, 251, 152), 2)

    def DrawInfo(self, fps, mode, number):
        cv.putText(self.image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv.LINE_AA)
        cv.putText(self.image, "FPS:" + str(fps), (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv.LINE_AA)

        modeString = ['Logging Key Point', 'Logging Point History']
        if 1 <= mode <= 2:
            cv.putText(self.image, "MODE:" + modeString[mode - 1], (10, 90), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
            if 0 <= number <= 9:
                cv.putText(self.image, "NUM:" + str(number), (10, 110), cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv.LINE_AA)
