#!/usr/bin/env python3

import boto3
from pydub import AudioSegment
from pydub.playback import play
import io
import random

available_directions = {
    'north': [360, 360],
    'south': [180, 180],
    'west': [270, 270],
    'east': [90, 90],
    'north-east': [1, 89],
    'south-east': [91, 179],
    'south-west': [181, 269],
    'north-west': [271, 359]
}
phonetic_numbers = {
    '0': 'zero',
    '1': 'one',
    '2': 'two',
    '3': 'tree',
    '4': 'four',
    '5': 'five',
    '6': 'six',
    '7': 'seven',
    '8': 'eight',
    '9': 'niner',
}
available_vors = ['OSI', 'OAK', 'SJC', 'SFO', 'SGD', 'PYE']
client = boto3.client('polly', region_name='us-west-2')


def choose_hold():
    hold_direction = random.choice(list(available_directions.keys()))
    if hold_direction not in ['north', 'south', 'west', 'east']:
        radial = random.randrange(available_directions[hold_direction][0], available_directions[hold_direction][1])
    else:
        radial = available_directions[hold_direction][0]
    spoken_radial = ' '.join([phonetic_numbers[i] for i in str(radial).zfill(3)])
    selected_vor = random.choice(available_vors)

    return_text = "<speak>November <say-as interpret-as='characters'>1234</say-as>, " \
                  f"hold <break time='1ms' /> {hold_direction} of the " \
                  f"<say-as interpret-as='characters'>{selected_vor}</say-as> " \
                  f"<say-as interpret-as='characters'>VOR</say-as>" \
                  f"<break time='1ms' />on the {spoken_radial} radial"
    if random.choice([0, 1]):
        return_text += "<break time='75ms' /> left turns"
    return_text += " at 5000 feet <break time='50ms' /><say-as interpret-as='characters'>efc</say-as> soon</speak>"
    return return_text


def speak(text):
    response = client.synthesize_speech(Engine='neural', LanguageCode='en-US', OutputFormat='mp3', Text=text, TextType='ssml', VoiceId='Matthew')
    song = AudioSegment.from_file(io.BytesIO(response.get('AudioStream').read()), format="mp3")
    play(song)


if __name__ == "__main__":
    while True:
        hold = choose_hold()
        speak(hold)
        input("Press Enter for next")
