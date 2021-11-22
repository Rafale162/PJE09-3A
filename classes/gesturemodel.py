import copy
import csv
import itertools
import cv2
import mediapipe as mp

from model import KeyPointClassifier
from classes.hand import Hand

class GestureModel:

    def __init__(self):
        with open('model/keypoint_classifier/keypoint_classifier_label.csv', encoding='utf-8-sig') as f:
            labels = csv.reader(f)
            self.signLabels = [row[0] for row in labels]

        with open('model/point_history_classifier/point_history_classifier_label.csv', encoding='utf-8-sig') as f:
            labels = csv.reader(f)
            self.movementlabels = [row[0] for row in labels]
        self.keyPointClassifier = KeyPointClassifier()
        self.handModel = mp.solutions.hands.Hands(
            static_image_mode = False,
            max_num_hands = 2,
            min_detection_confidence = 0.7,
            min_tracking_confidence = 0.5
        )

    def SetImageSize(self, res):
        self.width = res[0]
        self.height = res[1]

    def GetHands(self, image):
        hands = []
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        model = self.handModel.process(image)
        if model.multi_hand_landmarks is not None:
            for handedness, hand_landmarks in zip(model.multi_handedness, model.multi_hand_landmarks):
                hands.append(Hand(handedness, hand_landmarks))
        return hands

    def GetSide(self, hand):
        return hand.GetSide()

    def GetSign(self, hand):
        # Landmark calculation
        preProcessedLandmarkList = self.GetPreProcessedLandmark(hand)
        # Hand sign classification
        handSignId = self.keyPointClassifier(preProcessedLandmarkList)
        return self.signLabels[handSignId]

    def GetPoint(self, hand, id):
        landmark = hand.GetLandmarkList(self.width, self.height)
        return landmark[id]

    def GetPreProcessedLandmark(self, hand):
        landmarkPoint = []
        # Keypoint
        for _, landmark in enumerate(hand.landmarks.landmark):
            landmarkX = min(int(landmark.x * self.width), self.width - 1)
            landmarkY = min(int(landmark.y * self.height), self.height - 1)
            landmarkPoint.append([landmarkX, landmarkY])

        tempLandmarkList = copy.deepcopy(landmarkPoint)
        # Convert to relative coordinates
        baseX, baseY = 0, 0
        for index, landmarkPoint in enumerate(tempLandmarkList):
            if index == 0:
                baseX, baseY = landmarkPoint[0], landmarkPoint[1]
            tempLandmarkList[index][0] = tempLandmarkList[index][0] - baseX
            tempLandmarkList[index][1] = tempLandmarkList[index][1] - baseY
        # Convert to a one-dimensional list
        tempLandmarkList = list(
            itertools.chain.from_iterable(tempLandmarkList))
        # Normalization
        maxValue = max(list(map(abs, tempLandmarkList)))

        def Normalize(n):
            return n / maxValue

        return list(map(Normalize, tempLandmarkList))
        
    def GetPreProcessPointHistory(self, pointHistory):
        tempPointHistory = copy.deepcopy(pointHistory)
        # Convert to relative coordinates
        baseX, baseY = 0, 0
        for index, point in enumerate(tempPointHistory):
            if index == 0:
                baseX, baseY = point[0], point[1]
            tempPointHistory[index][0] = (tempPointHistory[index][0] - baseX) / self.width
            tempPointHistory[index][1] = (tempPointHistory[index][1] - baseY) / self.height

        # Convert to a one-dimensional list
        return list(itertools.chain.from_iterable(tempPointHistory))

    def SelectMode(self, key, mode):
        number = -1
        if 48 <= key <= 57:  # 0 ~ 9
            number = key - 48
        if key == 110:  # n
            mode = 0
        if key == 107:  # k
            mode = 1
        if key == 104:  # h
            mode = 2
        return number, mode