import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import re

#Retrieving the discord Bot Token, Learned from ChatGpt
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

#Allow the bot to read messages, Learned my friend Mitchel
intents = discord.Intents.default()
intents.message_content = True

#Allows bot commands, specifies the character required to call commands, Learned from ChatGpt
bot = commands.Bot(command_prefix='$', intents=intents)

#Defines list of banned words
bannedWords = ['hi', 'what', 'guh',]

#dictionary of misbehaving users and their offenses
badUser = {}

#Defines the bots functions in response to events
@bot.event
async def onReady(): #Prints a message after the bot successfully connects to Discord, Learned from ChatGpt
    print(f'logged in as {bot.user}')

@bot.event
async def on_message(message): #Scans messages sent by users for banned words and if a banned word is found a warning message is sent
    if message.author == bot.user: #Prevents bot from responding to itself
        return
    
    words = re.sub(r"[^a-zA-Z0-9\s]", "", message.content.lower()).split(" ")
    
    for word in words:
        if word in bannedWords:
            await message.channel.send(f'erm "{word}" is a bad word, you cant say that.')
    await bot.process_commands(message) #Allows bot to process commands still

    
#Defines the commands for the bot, Learned from ChatGpt
@bot.command()
async def hello(ctx): #Defines the hello command, when user calls $hello the bot will send a message saying Hello!
    await ctx.send('Hello!')

#Runs the bot
bot.run(TOKEN)
