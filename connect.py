import requests
import json
import base64

ANKICONNECT_URL = 'http://localhost:8765'

def browse(id = 1):
    payload = {
        "action": "guiBrowse",
        "version": 6,
        "params": {
            "query": f'nid:{id}',
        }
    }

    response = requests.post(ANKICONNECT_URL, json=payload)
    response_data = response.json()

    return response_data


def get_last_note():
    payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": 'added:1' #  all notes added today 
        }
    }
     
    response = requests.post(ANKICONNECT_URL, json=payload)
    response_data = response.json()

    note_id = max(response_data["result"]) if response_data["result"] else None

    return note_id


def add_audio_and_picture(note_id, audio_path, screenshot_path):
    # For local files we have to use base64 lol
    with open(screenshot_path, 'rb') as img_file:
        encoded_img = base64.b64encode(img_file.read())
    with open(audio_path, 'rb') as img_file:
        encoded_audio = base64.b64encode(img_file.read())
    
    # https://github.com/FooSoft/anki-connect/issues/82
    browse()


    # TODO fields name can change depending on the user...
    payload = {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": note_id,
                "fields": {},
                "audio": [{
                    "filename": "output.ogg",
                    "data": encoded_audio.decode(),
                    "fields": [
                        "SentenceAudio"
                    ]
                }],
                "picture": [{
                    "filename": "screenshot.jpg",
                    "data": encoded_img.decode(),
                    "fields": [
                        "Picture"
                    ]
                }]
            }   
        }
    }

    response = requests.post(ANKICONNECT_URL, json=payload)
    response_data = response.json()

    browse(note_id)

    return response_data


note_id = get_last_note()
audio = './output.ogg'
picture = './screenshot.jpg'

response = add_audio_and_picture(note_id, audio, picture)
print(response)