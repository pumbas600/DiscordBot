import os
import requests
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = '!'

bot = commands.Bot(command_prefix=PREFIX)
joke_categories = {
    'random': 'random_joke',
    'programming': 'jokes/programming/random'
}


# on_ready function handles the event when the client
# establishes a connection to Discord. Essentially, it is
# called when the bot is ready for further actions
@bot.event
async def on_ready():
    print(f'{bot.user.name} has established connection to Discord!')


@bot.event
async def on_member_join(member):
    # Send the member who joined a personalised DM
    # await makes the coroutine (this method) wait until the member.create_dm() has finished.
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to the Discord server!'
    )

@bot.command(name='categories', help='Responds with the available joke categories')
async def send_joke_categories(ctx):
    categories = ', '.join(joke_categories.keys())
    await ctx.send(f'Available categories: {categories}')


@bot.command(name='joke', help='Responds with a random joke')
async def send_joke(ctx, joke_category='random'):
    if joke_category.lower() not in joke_categories.keys():
        await ctx.send(f'The category, {joke_category}, is not supported. '
                       f'To find all the supported categories, use {PREFIX}categories')
        return

    response = requests.get(f'https://official-joke-api.appspot.com/{joke_categories[joke_category.lower()]}')

    # A status code of 200 indicates the request was a success and contains content.
    if response.status_code == 200:
        json_joke = response.json()

        # When getting a category joke, a list is returned
        if isinstance(json_joke, list):
            json_joke = json_joke[0]

        await ctx.send(f'{json_joke["setup"]}\n'
                       f'{json_joke["punchline"]}')
    else:
        await ctx.send("The joke servers weren't responding to our request for your joke :sob:")


@bot.event
async def on_error(event, *args, **kwargs):
    # Opens the file error.log with the ability to append. The file will be created if
    # it doesn't exist.
    with open('error.log', 'a') as f:
        f.write(f'Error caused by event: {event}\n'
                f'Error details: {args[0]}\n')
        # Re-raise the error to make it invoke the default error behaviour
        # raise


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role to use this command.')


bot.run(TOKEN)
