# This class exports the Rasa chatbot to Discord.

import discord
import asyncio
import nest_asyncio
from typing import Dict, Text, Any
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa.core.agent import Agent

# Set up the Discord bot
intents = discord.Intents.guilds | discord.Intents.messages | discord.Intents.members | discord.Intents.guild_messages | discord.Intents.dm_messages
client = discord.Client(intents=intents)

# Set up the Rasa agent
model_path = "/Users/carolinaduarte/PycharmProjects/Chatbot-for-L2-Learning/chatbot/models/20221118-231745-external-defense.tar.gz"
agent = Agent.load(model_path)


# Define a custom action that sends messages to Discord
class ActionSendToDiscord(Action):
    def name(self):
        return "action_send_to_discord"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]):
        # Get the response from the Rasa agent
        response = tracker.latest_message.get('text')

        # Send the response back to Discord
        channel = client.get_channel(1096131946796548128)
        asyncio.run_coroutine_threadsafe(channel.send(response), client.loop)

        return []


# Define a function to handle incoming Discord messages
@client.event
async def on_message(message):
    # Ignore messages sent by the bot itself
    if message.author == client.user:
        return

    # Send the message to the Rasa agent
    response = await agent.handle_text(message.content)

    # Send the response back to Discord
    channel = message.channel
    await channel.send(response[0]['text'])

# Start the Discord bot
nest_asyncio.apply()
client.run('MTA5NTM0NjIyNzY4NTYyMTc4MA.GUbthA.990oMUyfYWIH-A7EE0tREssa6sGcUxqcmjVaB8')
