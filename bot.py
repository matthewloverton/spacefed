import discord
from discord.ext import commands
import json, sys, traceback, asyncio, random, os

config = json.load(open('config.json', 'r'))

#0 = Playing
#1 = Streaming
#2 = Listening to
#3 = Watching

#Define bot statuses.
statuses = [['a Space Federation match', 0],
            ['over the Server', 3],
            ['some lo-fi beats', 2],
            ['planets get destroyed', 3],
            ['the assembly debate', 2]]

# ============= INITIALIZE BOT CLIENT =============

# Define the prefix for the bot, tagging the bot also works. 
def get_prefix(bot, message):
    # ENV
    #prefixes = os.getenv('PREFIXES').split(' ')
    # LOCAL
    prefixes = config['discord']['prefixes']

    return commands.when_mentioned_or(*prefixes)(bot, message)

# Create an array of the cogs that need loading.
initial_extensions = []

# Set the prefix.
client = commands.Bot(command_prefix = get_prefix, description = "Space Federation bot")

# ============= FUNCTIONS =============

# Loop through the status choices.
async def status_task():
    while True:
        status = random.choice(statuses)
        await client.change_presence(activity=discord.Activity(name=status[0], type=status[1]))
        await asyncio.sleep(180)


# ============= LOAD COGS =============
if __name__ == '__main__':
    for extension in initial_extensions:
        client.load_extension(extension)

# Print information about the bot if it successfully activates.
@client.event
async def on_ready():
    print (f'\n\nLogged in as: {client.user.name} - {client.user.id}\nVersion: {discord.__version__}\n')

    # Create an asynchronous task to change the status.
    client.loop.create_task(status_task())
    print(f'Successfully logged in and running...!')

# ============= START BOT =============
# ENV
#client.run(os.getenv('BOT_TOKEN'), bot = True, reconnect = True)
# LOCAL
client.run(config['discord']['token'], bot = True, reconnect = True)