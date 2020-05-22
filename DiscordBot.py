import os
import discord

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'

client = discord.Client()


# on_ready function handles the event when the client
# establishes a connection to Discord. Essentially, it is
# called when the bot is ready for further actions
@client.event
async def on_ready():
    print(f'{client.user} has establised connection to Discord!')


@client.event
async def on_member_join(member):
    # Send the member who joined a personalised DM
    # await makes the coroutine (this method) wait until the member.create_dm() has finished.
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Discord server!'
    )


@client.event
async def on_message(message):
    # Ignore messages sent by the bot.
    if message.author == client.user:
        return

    if message[0] == PREFIX:
        # Pass the message without the prefix
        determine_message(message[1:])


def determine_message(message):
    return 'Hey'

client.run(TOKEN)
