import cv2
import mediapipe as mp
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import time
from comtypes import CLSCTX_ALL
import ctypes

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

def toggle_audio_playback():
    ctypes.windll.user32.keybd_event(0xB3, 0, 0, 0)  

cap = cv2.VideoCapture(0)
capturing = False  

pinch_count = 0  
pinch_in_progress = False  
audio_paused = False  

frame_count = 0  
reset_interval = 150  

def get_distance_between_fingers(landmarks, w, h, finger1, finger2):
    x1, y1 = int(landmarks.landmark[finger1].x * w), int(landmarks.landmark[finger1].y * h)
    x2, y2 = int(landmarks.landmark[finger2].x * w), int(landmarks.landmark[finger2].y * h)
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    results = hands.process(rgb_frame)  

    h, w, _ = frame.shape  

    key = cv2.waitKey(1) & 0xFF
    if key == ord('5'):
        capturing = not capturing  
        if capturing:
            print("Captura ativada.")
        else:
            print("Captura desativada.")
        time.sleep(0.5)  

    if capturing:
        if results.multi_hand_landmarks:  
            for hand_landmarks in results.multi_hand_landmarks:

                thumb_index_distance = get_distance_between_fingers(hand_landmarks, w, h, mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP)

                pinching_threshold = 40  

                if thumb_index_distance < pinching_threshold:
                    if not pinch_in_progress:
                        pinch_in_progress = True
                        pinch_count += 1
                        print(f"Pinça detectada, contagem: {pinch_count}")

                else:
                    if pinch_in_progress:
                        pinch_in_progress = False

                if pinch_count == 5:
                    toggle_audio_playback()  
                    audio_paused = not audio_paused  
                    print("Controle de áudio pausado ou retomado.")
                    pinch_count = 0  

                if frame_count >= reset_interval:
                    pinch_count = 0
                    print("Contagem de pinças resetada.")
                    frame_count = 0  

                if not audio_paused:

                    if thumb_index_distance < 20:
                        current_volume = volume.GetMasterVolumeLevelScalar()
                        new_volume = max(0, min(1, current_volume - 0.05))  
                        volume.SetMasterVolumeLevelScalar(new_volume, None)
                        print(f"Diminuindo volume: {new_volume}")

                    elif thumb_index_distance > 35:
                        current_volume = volume.GetMasterVolumeLevelScalar()
                        new_volume = max(0, min(1, current_volume + 0.05))  
                        volume.SetMasterVolumeLevelScalar(new_volume, None)
                        print(f"Aumentando volume: {new_volume}")

    frame_count += 1  

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for landmark in hand_landmarks.landmark:
                x, y = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (x, y), 5, (255, 255, 255), -1)

    cv2.imshow("Controle de Mídia com Mão", frame)

    if key == ord('q'):
        break

cap.release()  
cv2.destroyAllWindows()  