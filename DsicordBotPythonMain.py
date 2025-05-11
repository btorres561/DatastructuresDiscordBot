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
badUsers = {}

#Prints a message after the bot successfully connects to Discord, Learned from ChatGpt
@bot.event
async def onReady():
    print(f'logged in as {bot.user}')

#Scans messages sent by users for banned words and if a banned word is found a warning message is sent
@bot.event
async def on_message(message):
    if message.author == bot.user: #Prevents bot from responding to itself
        return
    
    words = re.sub(r"[^a-zA-Z0-9\s]", "", message.content.lower()).split(" ")
    print(words)
    for word in words:
        if word in bannedWords:
            await message.channel.send(f'Erm "{word}" is a bad word, you cant say that.')
            await shameUser(message)
            
    await bot.process_commands(message) #Allows bot to process commands still

async def shameUser(message):
    member = message.author
    if member.name in badUsers: 
        badUsers[member.name].append(message.content)
        
    else:
        badUsers[member.name] = [message.content]
        
    try: 
        await member.edit(nick="Rude Man")
        await message.channel.send(f'From {member.mention}: "{message.content}"\nYour name is now Rude Man.')
        
    except discord.Forbidden:
        await message.channel.send("Do not have permission to change user nickname.")
        
    except discord.HTTPException:
        await message.channel.send("Changing nickname failed.")
        
#Defines the hello command, when user calls $hello the bot will send a message saying Hello!   
@bot.command()
async def hello(ctx):
    await ctx.send('Hello!')

#Defines the badPeople command, when users call this command it sends a message containing bad users from the badUsers dictionary 
@bot.command()
async def badPeople(ctx):
    await ctx.send(badUsers)

#Defines the findBadPeople command, when users call this command and supply a user it sends a message containing the user's flagged messages
@bot.command()
async def findBadPeople(ctx, member: discord.Member):
    if member.name in badUsers.keys():
        await ctx.send(f'{member.name}: {badUsers[member.name]}')
    else:
        await ctx.send(f'{member.name} is not a bad user.')
        
#Runs the bot
bot.run(TOKEN)
