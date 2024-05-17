import wave
import os
import pyaudio
import sys 
import threading

from pynput import keyboard
from pydub import AudioSegment

from scripts.settings import CHUNK, SAMPLE_FORMAT, FS, RATE, CHANNELS, VIRTUALSINK
from scripts.ankiconnect import add_audio_and_picture, get_last_note, check_connection
from scripts.setup import verify_virtual_sink, create_virtual_sink
from scripts.screenshot import screenshot

p = pyaudio.PyAudio()

is_recording = False
frames = []

def record_audio():
    global is_recording
    global frames
    global CHANNELS
    
    screenshot()

    stream = p.open(format=SAMPLE_FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    frames_per_buffer=CHUNK,
                    input=True)

    print('recording...')
    print('press right shift to stop recording')
    is_recording = True

    while is_recording:
        data = stream.read(CHUNK, exception_on_overflow=False) # so many overflows that i had to disable exception
        frames.append(data)

    stream.stop_stream()
    stream.close()

    print('Finished recording!')
    print('\007')


def stop_recording():
    global is_recording
    
    is_recording = False


def save_file():    
    # pyAudio only works with .wav files, so I have to convert to .ogg afterwards
    with wave.open('output.wav', 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(SAMPLE_FORMAT))
        wf.setframerate(FS)
        wf.writeframes(b''.join(frames))
        wf.close()

    audio_data = AudioSegment.from_wav('output.wav')
    audio_data.export('output.ogg', format='ogg')

    os.remove('output.wav')
    print('output.ogg created')


def connect():
    note_id = get_last_note()
    
    audio = './output.ogg'
    picture = './screenshot.webp'

    add_audio_and_picture(note_id, audio, picture)


def on_press(key):
    global p
    
    if key == keyboard.Key.shift_r and not is_recording:
        threading.Thread(target=record_audio, daemon=True).start()
    elif key == keyboard.Key.shift_r and is_recording:
        stop_recording()
        save_file()
        connect()
    elif key == keyboard.Key.esc and not is_recording:
        p.terminate()
        return False


def setup():
    global p
    
    # clear screen after PyAudio initialization
    os.system('clear')
    print('PyAudio initialized')

    if not verify_virtual_sink(VIRTUALSINK):
        print("Create virtual sink? (Y/n)", end=" ")
        answer = str(input())
        if answer == 'N' or answer == 'n' or answer == 'no':
            return
        create_virtual_sink(VIRTUALSINK)
    
    if not check_connection():
        p.terminate()
        sys.exit(1)


if __name__ == '__main__':
    setup()
    print()
    print('Press RIGHT shift to start recording')
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    print('\nBye')