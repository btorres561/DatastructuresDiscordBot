import discord
from discord.ext import commands
import os
from dotenv import load_dotenv    

#Retrieving the discord Bot Token, Learned from ChatGpt
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

#Allow the bot to read messages, Learned my friend Mitchel
intents = discord.Intents.default()
intents.message_content = True

#Allows bot commands, specifies the character required to call commands, Learned from ChatGpt
bot = commands.Bot(command_prefix='$', intents=intents)

#Prints a message after the bot successfully connects to Discord, Learned from ChatGpt
@bot.event
async def onReady():
    print(f'logged in as {bot.user}')
    
#Defines the commands for the bot, Learned from ChatGpt
@bot.command()
async def hello(ctx): #Defines the hello command, when user calls $hello the bot will send a message saying Hello!
    await ctx.send('Hello!')

#Runs the bot
bot.run(TOKEN)
