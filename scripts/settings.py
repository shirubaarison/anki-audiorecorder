import pyaudio

# TODO: read a config file idk

# PYAUDIO CONFIG
CHUNK = 1024
SAMPLE_FORMAT = pyaudio.paInt16
FS = 44100
RATE = 44100
CHANNELS = 2

# VIRTUALSINK NAME
VIRTUALSINK = 'vsink'

# SCREENSHOT
HEIGHT = 400

# ANKICONNECT
ANKICONNECT_URL = 'http://localhost:8765'
DECK_NAME = '日本語::メディア'
AUDIO_FIELD = 'SentenceAudio'
IMAGE_FIELD = 'Picture'