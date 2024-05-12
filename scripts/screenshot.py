from PIL import Image, ImageGrab
import pywinctl as pwc

from scripts.constants import HEIGHT

def resize_keep_aspect_ratio(image, new_height):
    width, height = image.size
    aspect_ratio = width / height

    new_width = int(aspect_ratio * new_height)

    resized_image = image.resize((new_width, new_height), Image.LANCZOS)

    return resized_image


def screenshot():
    window = pwc.getActiveWindow()

    left, top, width, height = window.left, window.top, window.width, window.height
    
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

    resized_screenshot = resize_keep_aspect_ratio(screenshot, HEIGHT)

    resized_screenshot.save('screenshot.webp', 'webp', optimize = True, quality = 80)

    print('Screenshot created')