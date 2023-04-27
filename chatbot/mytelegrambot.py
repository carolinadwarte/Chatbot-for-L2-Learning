import csv
import logging
import translators as ts
import telegram.ext
from gtts import gTTS
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler
from telegram.ext import filters
from rasa.core.agent import Agent

AUDIO_FILE_PATH = "speech.mp3"
VOICE_NOTE_TRIGGER = "Here is the pronunciation for:"
voice_note_counter = 0
chat_log = {}
TRANSLATION_TRIGGER = "Translate this:"

# Loading the models
agent = Agent.load('./models')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def greet(update: Update, context: telegram.ext.CallbackContext):
    global voice_note_counter
    user_input = update.message.text
    print(f"User says: {user_input}")
    response = await agent.handle_text(user_input)
    response_text = response[0]["text"]

    if VOICE_NOTE_TRIGGER in response[0]["text"]:
        # Remove command from user input
        colon_point = user_input.find(":")
        user_readable = user_input[colon_point+1:]
        print(f"Sending user readable to gTTS: {user_readable}")
        # Call TTS function with input
        text_to_speach(user_readable)
        voice_note_counter += 1
        bot_response = f"Voice note: {user_readable}"
        with open(AUDIO_FILE_PATH, 'rb') as voice_file:
            # Send response to chatbot
            await context.bot.send_voice(chat_id=update.effective_chat.id, voice=voice_file)
    elif TRANSLATION_TRIGGER in response[0]["text"]:
        # Remove command from user
        colon_point = user_input.find(":")
        user_readable = user_input[colon_point+1:]
        print(f"Sending translation: {user_readable}")
        # Call translation function with input
        bot_response = translation(user_readable)
        # Send response to chatbots
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)
    else:
        try:
            bot_response = response[0]["text"]
        except IndexError:
            print(f"ERROR No response given for input: {user_input}")
            bot_response = "Sorry, I'm having trouble with that one."
        # Send response to chatbot
        print(f"Bot responds with: {bot_response}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=bot_response)

    chat_log[user_input] = bot_response
def translation(query):
    print(f"[Bot] Running gtts...", end="")
    # Call API to generate translation
    translated_text = ts.translate_text(query, 'google', 'en', 'pt')
    print("Saved")
    return translated_text


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
    try:
        application.run_polling()
    except KeyboardInterrupt:
        print("Saving chat log ...")

        with open("ChatLog.csv", "w") as log:
            writer = csv.DictWriter(log, fieldnames=("User Input", "Bot Response"))
            writer.writeheader()
            for user_input, bot_response in chat_log.items():
                writer.writerow((user_input, bot_response))


