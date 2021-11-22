class Hand:
    def __init__(self, handedness, landmarks):
        self.handedness = handedness
        self.landmarks = landmarks
    
    def __del__(self):
        del(self.handedness)
        del(self.landmarks)

    def GetSide(self):
        return self.handedness.classification[0].label[0:]

    def GetLandmarks(self):
        return self.landmarks

    def GetHandedness(self):
        return self.handedness

    def GetLandmarkList(self, imageWidth, imageHeight):
        landmarkPoint = []
        for _, landmark in enumerate(self.landmarks.landmark):
            landmarkX = min(int(landmark.x * imageWidth), imageWidth - 1)
            landmarkY = min(int(landmark.y * imageHeight), imageHeight - 1)
            landmarkPoint.append([landmarkX, landmarkY])
        return landmarkPoint