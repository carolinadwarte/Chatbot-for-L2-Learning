import logging

import telegram.ext
from gtts import gTTS
from telegram import Update, Voice
from telegram.ext import ApplicationBuilder, MessageHandler
from telegram.ext import filters
from rasa.core.agent import Agent
from chatbot.actions import actions

AUDIO_FILE_PATH = "speech.mp3"
VOICE_NOTE_TRIGGER = "Here is the pronunciation for:"
voice_note_counter = 0

# Loading the models
agent = Agent.load('./models')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def greet(update: Update, context: telegram.ext.CallbackContext):
    global voice_note_counter
    user_input = update.message.text
    response = await agent.handle_text(user_input)

    if VOICE_NOTE_TRIGGER in response[0]["text"]:
        # do the voice note
        # Remove command from user input
        #user_input = user_input.replace("Repeat this out loud:", "")
        colon_point = user_input.find(":")
        user_readable = user_input[colon_point:]
        print(f"[System] sending gTTS: {user_readable}")
        text_to_speach(user_readable)
        #this_voice = Voice(AUDIO_FILE_PATH, f"voice-{voice_note_counter}.mp3", 30)
        voice_note_counter += 1
        with open(AUDIO_FILE_PATH, 'rb') as voice_file:
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice_file)
    else:
        try:
            bot_response = response[0]["text"]
        except IndexError:
            print(f"[ERROR] No response given for input: {user_input}")
            bot_response = "Sorry, I'm having trouble with that one"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)


# async def voice_note(update: Update, context: telegram.ext.CallbackContext):
#     user_input = update.message.text
#
#     text_to_speach(user_input)
#
#     await context.bot.send_voice(chat_id=update.effective_chat.id, voice='speech.mp3')


def text_to_speach(query):
    print(f"[Bot] Running gtts...", end="")
    # Generate the speech output using gTTS
    speech = gTTS(text=query, lang='pt', tld='pt')
    # Save the speech output as an audio file
    speech_file = 'speech.mp3'
    speech.save(speech_file)
    print("Saved")


if __name__ == '__main__':
    application = ApplicationBuilder().token('6202311476:AAHDk9oIW6fLFjZB9dJqIGIGPLliysK21Yk').build()

    greeting_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), greet)
    application.add_handler(greeting_handler)

    speech_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), voice_note)
    application.add_handler(speech_handler)

    application.run_polling()
