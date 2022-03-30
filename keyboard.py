import cv2
from pyautogui import press

ROWS = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
    ['Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'Return'],
    ['LShift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'RShift'],
    ['Ctrl', 'WIN', 'Alt', 'Space', 'Alt', 'WIN', 'Ctrl']
]

SIZES = {
    'Backspace': 2,
    'Tab': 1.5,
    '\\': 1.5,
    'Caps': 1.5,
    'Return': 2.5,
    'LShift': 2.5,
    'RShift': 2.5,
    'Ctrl': 1.5,
    'WIN': 1.5,
    'Alt': 1.5,
    'Space': 6
}

ALIASES = {
    'LShift': 'shiftleft',
    'RShift': 'shiftright',
    'Caps': 'capslock',
}

def _drawKey(image, text, point1, point2: tuple[int, int]):
    return cv2.rectangle(
        cv2.putText(
            image, text, (point1[0] + 7, point1[1] + 15),
            cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1,
            cv2.LINE_AA,
            False
        ),
        point1, point2, (255, 255, 255), 1
    )

def DrawKeyboard(image):

    X, Y = 0, 0

    height, side, _ = image.shape
    side //= 15

    Y = (height - (side * len(ROWS))) // 2

    for row in ROWS:
        for key in row:

            if not key in SIZES:
                image = _drawKey(image, key, (X, Y), (X + side, Y + side))
                X += side

            else:
                image = _drawKey(
                    image, key, (X, Y), 
                    (X + int(side * SIZES[key]), Y + side)
                )
                X += int(side * SIZES[key])

        X = 0
        Y += side

    return image

def KeyPress(key):
    press(key.lower())