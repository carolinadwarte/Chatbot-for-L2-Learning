# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Dict, Text, Any, List
from rasa_sdk import Action, Tracker
from gtts import gTTS
from rasa_sdk.executor import CollectingDispatcher


# This file implements the text to speech functionality. gTTS is implemented - a Python library and CLI tool to
# interface with Google Translate’s text-to-speech API. Writes spoken mp3 data to a file, a file-like object
# (bytestring) for further audio manipulation, or stdout.


class ActionTextToSpeech(Action):
    def name(self):
        return "action_text_to_speech"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract the wildcard text from the user input
        query = tracker.latest_message['text']
        query = query.split(' ', 1)[1]

        # Generate the speech output using gTTS
        speech = gTTS(text=query, lang='pt-pt')

        # Save the speech output as an audio file
        speech_file = 'speech.mp3'
        speech.save(speech_file)

        # Send the speech output back to the user
        dispatcher.utter_audio_file(speech_file)

        # Return an empty list to update the chatbot's state
        # events that should be applied to the conversation state
        return []
