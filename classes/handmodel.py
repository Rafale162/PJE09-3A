from classes.hand import Hand

class HandModel:

    def __init__(self, model):
        self.model = model

    def GetHands(self):
        hands = []
        if self.model.multi_hand_landmarks is not None:
            for handedness, hand_landmarks in zip(self.model.multi_handedness, self.model.multi_hand_landmarks):
                hands.append(Hand(handedness, hand_landmarks))
        return hands