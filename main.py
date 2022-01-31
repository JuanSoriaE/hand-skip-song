import pyautogui
import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
mpHands = mp.solutions.hands
index = 9
initialFlag = False

def click():
    location = pyautogui.locateOnScreen('next.png')
    if location is not None:
        x, y = pyautogui.center(location)
        pyautogui.click(x, y)
    else:
        print('[-] Button not found.')

def positionChange(width, x):
    #If x starts before 20% and finishes after 70%
    global initialFlag
    if x < width*0.2:
        initialFlag = True
    if x > width*0.7 and initialFlag == True:
        print('[+] Position changed!')
        click()
        initialFlag = False

with mpHands.Hands(
    model_complexity = 0,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
) as hands:
    while cap.isOpened():
        succes, image = cap.read()

        if not succes:
            print('Ignoring empty camera frame.')
            continue

        height, width, _ = image.shape
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks: 
                x = int(hand_landmarks.landmark[index].x * width)
                y = int(hand_landmarks.landmark[index].y * height)

                cv2.circle(image, (x, y), 2, (0, 255, 255), 2)
                cv2.circle(image, (x, y), 1, (128, 0, 250), 2)
            positionChange(width, x)
                
        cv2.imshow('Skip song', cv2.flip(image, 1))
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()