import mediapipe as mp
import cv2

def track_hand(frame, width, height, last_tip_position):
    # Initialize MediaPipe Hand module
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()

    # Process the frame with MediaPipe Hand Tracking
    rgb_frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # Check for hand presence
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get the coordinates of the tip of the index finger
            tip_of_index_finger = (
                int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width),
                int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
            )
        return tip_of_index_finger
    else:
        return last_tip_position