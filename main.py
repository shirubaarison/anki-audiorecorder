import wave
import os
import pyaudio
import sys 
import threading

from pynput import keyboard
from pydub import AudioSegment

CHUNK = 8192
SAMPLE_FORMAT = pyaudio.paInt16
FS = 44100
filename = 'output.wav'

p = pyaudio.PyAudio()

# TODO select device id automatically
device_id = 0
device_info = p.get_device_info_by_index(device_id)
CHANNELS = device_info["maxInputChannels"] if (device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]
SAMPLE_RATE = int(device_info["defaultSampleRate"])

is_recording = False
frames = []

def record_audio():
    global is_recording
    global frames
    global device_info
    global CHANNELS

    stream = p.open(format=SAMPLE_FORMAT,
                    channels=CHANNELS,
                    rate=SAMPLE_RATE,
                    frames_per_buffer=CHUNK,
                    input=True,
                    input_device_index=device_info["index"],
                    )

    print('recording...')
    is_recording = True

    while is_recording:
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    print('Finished recording!', end=' ')


def stop_recording():
    global is_recording
    is_recording = False


def save_file():    
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(frames))
        wf.close()

    audio_data = AudioSegment.from_wav(filename)
    audio_data.export('output.ogg', format='ogg')

    os.remove('output.wav')
    print('and converted to .ogg :)')


def on_press(key):
    global p
    if key == keyboard.Key.ctrl_l and not is_recording:
        threading.Thread(target=record_audio).start()
    elif key == keyboard.Key.ctrl_l and is_recording:
        stop_recording()
        save_file()
    elif key == keyboard.Key.esc and not is_recording:
        p.terminate()
        sys.exit(0)


with keyboard.Listener(on_press=on_press) as listener:
    listener.join()