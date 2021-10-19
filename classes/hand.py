class Hand:
    def __init__(self, handedness, landmarks):
        self.handedness = handedness
        self.landmarks = landmarks
    
    def __del__(self):
        del(self.handedness)
        del(self.landmarks)

    def GetSide(self):
        return self.handedness.classification[0].label[0:]

    def GetPoint(self, id):
        return self.landmarks[id]

    def GetLandmarks(self):
        return self.landmarks

    def GetHandedness(self):
        return self.handedness

    def GetLandmarkList(self, image):
        imageWidth, imageHeight = image.shape[1], image.shape[0]
        landmarkPoint = []
        for _, landmark in enumerate(self.landmarks.landmark):
            landmarkX = min(int(landmark.x * imageWidth), imageWidth - 1)
            landmarkY = min(int(landmark.y * imageHeight), imageHeight - 1)
            # landmark_z = landmark.z
            landmarkPoint.append([landmarkX, landmarkY])
        return landmarkPoint