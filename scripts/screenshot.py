import pyautogui
from PIL import ImageGrab

def screenshot():
    # TODO: Screenshot only the focus window
    
    x, y = pyautogui.size()
    x /= 2
    y /= 2

    screenshot = ImageGrab.grab()

    region_size = 500
    left = max(0, x - region_size)
    top = max(0, y - region_size)
    right = min(x + region_size, 1920)
    bottom = min(y + region_size, 1080)

    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))

    screenshot.save('screenshot.jpg')

    print('Screenshot created')
