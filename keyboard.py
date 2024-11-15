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

def _drawKey(image, text, point1, point2: tuple[int, int], pressed: bool = False):
    return cv2.putText(
        cv2.rectangle(
            image, point1, point2, 
            (128, 128, 128), 1 if not pressed else -1
        ), text, 
        org=(
            point1[0] + max(20, 4*len(text)), 
            ((point1[1]+point2[1])>>1) + 10
        ),
        fontFace=cv2.FONT_HERSHEY_PLAIN, 
        fontScale=max(1.5, 4 - (len(text)/3)), 
        color=(255, 255, 255), 
        thickness=2,
        lineType=cv2.LINE_AA,
        bottomLeftOrigin=False
    )




def DrawKeyboard(image, pressed: dict[str, int]):

    X, Y = 0, 0

    height, side, _ = image.shape
    side //= 15

    Y = (height - (side * len(ROWS))) // 2

    for row in ROWS:
        for key in row:

            is_pressed = key in pressed and pressed[key]

            if not key in SIZES:
                image = _drawKey(image, key, (X, Y), (X + side, Y + side), is_pressed)
                X += side

            else:
                image = _drawKey(
                    image, key, (X, Y), 
                    (X + int(side * SIZES[key]), Y + side),
                    is_pressed
                )
                X += int(side * SIZES[key])

        X = 0
        Y += side

    return image

def KeyPress(key):
    press(key.lower())