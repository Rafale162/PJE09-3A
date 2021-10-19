import cv2
import mediapipe as mp
import time
#from classes.camera import *

class HandCapture:

    def __init__(self):      
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.5)
        self.cam = cv2.VideoCapture(0)#Camera(0)

    def DrawAnnotations(self, image, results):
        im = image.copy()
        im.flags.writeable = True
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    im,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())   
        return im

    def ShowImage(self, image):
        cv2.imshow('MediaPipe Hands', image)

    def ProcessImage(self, image):
        return self.hands.process(image)

    def Run(self):
        self.CamInit(0)
        start_time = time.time()
        x = 2 # affichage des FPS toutes les x secondes
        counter = 0
        while self.cap.isOpened():
            image = self.GetImage()
            results = self.ProcessImage(image)
            annoted = self.DrawAnnotations(image, results)
            self.ShowImage(annoted)

            if cv2.waitKey(1) & 0xFF == 27:
                break
            counter+=1
            if (time.time() - start_time) > x :
                print("FPS: ", counter / (time.time() - start_time))
                counter = 0
                start_time = time.time()
                if results.multi_handedness != None:
                    for hand in results.multi_handedness:
                        print(hand.classification[0].label)
        self.CamStop()

    def Pos(self, results, el):
        if results.multi_hand_landmarks == None:
            return None
        return results.multi_hand_landmarks[0].landmark[el]
        
    def CaptureDataset(self, file):
        f = open(file, "a")
        self.CamInit(0)
        while self.cap.isOpened():
            image = self.GetImage()
            results = self.ProcessImage(image)
            annoted = self.DrawAnnotations(image, results)
            self.ShowImage(annoted)
            if cv2.waitKey(5) & 0xFF == 27:
                break
            if cv2.waitKey(5) & 0xFF == 32:
                pos = self.Pos(results, self.mp_hands.HandLandmark.INDEX_FINGER_TIP)
                print(pos)
                data = ""
                for lm in results.multi_hand_landmarks[0].landmark:
                    data += str(lm.x) + ";"+ str(lm.y) +";"
                print(data)
                f.write(data + "\n")
        f.close()
        self.CamStop()

