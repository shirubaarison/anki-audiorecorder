from PIL import ImageGrab
import pywinctl as pwc

def screenshot():
    window = pwc.getActiveWindow()

    left, top, width, height = window.left, window.top, window.width, window.height
    
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

    screenshot.save('screenshot.jpg')

    print('Screenshot created')