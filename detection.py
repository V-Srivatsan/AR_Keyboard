import cv2
import mediapipe
import numpy

from keyboard import DrawKeyboard, ROWS, SIZES, ALIASES

from win32api import GetSystemMetrics
WIDTH, HEIGHT = int(cv2.CAP_PROP_FRAME_WIDTH * GetSystemMetrics(0) / 7), int(cv2.CAP_PROP_FRAME_HEIGHT * GetSystemMetrics(1) / 7)
KEY_SIDE = WIDTH // 15
START = (HEIGHT - (KEY_SIDE * len(ROWS))) // 2

MP_HANDS = mediapipe.solutions.hands
MP_DRAWING = mediapipe.solutions.drawing_utils
MP_DRAWING_STYLES = mediapipe.solutions.drawing_styles

POINTS = [
    # MP_HANDS.HandLandmark.THUMB_TIP,
    MP_HANDS.HandLandmark.INDEX_FINGER_TIP,
    MP_HANDS.HandLandmark.MIDDLE_FINGER_TIP,
    MP_HANDS.HandLandmark.RING_FINGER_TIP,
    # MP_HANDS.HandLandmark.PINKY_TIP,
]

THRESHOLDS = {
    MP_HANDS.HandLandmark.THUMB_TIP: -0.13,
    MP_HANDS.HandLandmark.INDEX_FINGER_TIP: -0.15,
    MP_HANDS.HandLandmark.MIDDLE_FINGER_TIP: -0.17,
    MP_HANDS.HandLandmark.RING_FINGER_TIP: -0.16,
    MP_HANDS.HandLandmark.PINKY_TIP: -0.14,
}

TIMEOUT = {}
EXCLUDED = ['Backspace']
TIMEOUT_FRAMES = cv2.CAP_PROP_FPS

HANDS = MP_HANDS.Hands(
        model_complexity=0,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )



def _getKey(coords):

    if coords[1] < START:
        return None

    row = int(((coords[1] - START) // KEY_SIDE))
    if row >= 0 and row < len(ROWS):

        KEY_END = 0
        for i in range(len(ROWS[row])):
            key = ROWS[row][i]

            if coords[0] >= KEY_END:
                if (key in SIZES and coords[0] <= KEY_END + (SIZES[key] * KEY_SIDE)) \
                    or coords[0] <= KEY_END + KEY_SIDE:
                        return key

                if key in SIZES: KEY_END += (SIZES[key] * KEY_SIDE)
                else: KEY_END += KEY_SIDE

    return None
                    


def ProcessImage(image, calc):
    pressed = set()

    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.flip(cv2.resize(image, (WIDTH, HEIGHT)), 1)
    results = HANDS.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    frame = numpy.zeros((HEIGHT, WIDTH, 3), numpy.uint8)
    frame[:, : WIDTH] = (3, 3, 3)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            MP_DRAWING.draw_landmarks(
                frame,
                hand_landmarks,
                MP_HANDS.HAND_CONNECTIONS,
                MP_DRAWING_STYLES.get_default_hand_landmarks_style(),
                MP_DRAWING_STYLES.get_default_hand_connections_style())
            
            if (calc):
                for point in POINTS:
                    landmark = hand_landmarks.landmark[point]
                    x, y, z = float(landmark.x * WIDTH), float(landmark.y * HEIGHT), landmark.z

                    if z <= THRESHOLDS[point]:
                        key = _getKey((x, y))
                        if key:
                            if key not in EXCLUDED and key in TIMEOUT and TIMEOUT[key] != 0: continue
                            
                            else:
                                if key in ALIASES:
                                    pressed.add(ALIASES[key])
                                else:
                                    pressed.add(key.lower())
                                TIMEOUT[key] = TIMEOUT_FRAMES

    for key in TIMEOUT: TIMEOUT[key] = max(TIMEOUT[key]-1, 0)

    return DrawKeyboard(frame, TIMEOUT), pressed
    
