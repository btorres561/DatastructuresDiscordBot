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

#dictionary of misbehaving users and their offenses
badUsers = {}

#Prints a message after the bot successfully connects to Discord, Learned from ChatGpt
@bot.event
async def onReady():
    print(f'logged in as {bot.user}')
    
#bst class, a reimplementation of Lab 3 Part 2 in Python instead of Java and replaces the spellCheck() method with 2 new functions
class BinarySearchTree:
    #binary search tree constructor
    def __init__(self):
        root = None
    
    #node class
    class Node:
        #node left and right
        left = None
        right = None
        #node function taking word
        def __init__(self, key = ""):
            #key = item
            self.key = key
            #left = right = null
            self.left = None
            self.right = None
            
    #genBstFile function
    def GenBstFile(self):
        #new bst object
        bstFile = BinarySearchTree()
        #try
        try:
            #extract file and insert each word into bstFile
            with open('censored_words.txt', 'r') as file:
                badWords = file.readlines()
                print(badWords)
                for word in badWords:
                    print(word)
                    bstFile.insert(word.strip())

        #catch file not found exception
        except FileNotFoundError:
            print("Error")

        #return bstFile
        return bstFile
    
    #Scans messages sent by users for banned words and if a banned word is found a warning message is sent Big O: O(n Log n)
    async def messageMonitor(self, message):
        if message.author == bot.user: #Prevents bot from responding to itself
            return
        
        words = re.sub(r"[^a-zA-Z0-9\s]", "", message.content.lower()).split(" ")
        print(words)
        for word in words:
            if self.search(word):
                await message.channel.send(f'"{word}" is a bad word, you cant say that.')
                await self.shameUser(message)
                
        await bot.process_commands(message) #Allows bot to process commands still
    
    #Function gets called when banned words are found, add offending user to a dictionary with their message and changes their nickname
    async def shameUser(self, message):
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
    
    #node object named root
    root = None
    
    #insert function taking key Big O: O(n)
    def insert(self, key):
        self.root = self.insertRec(self.root, key)

    #insert recurive function taking root and key Big O: O(n)
    def insertRec(self, root, key):
        #if root = null
        if root is None:
            root = self.Node(key)
            return root
        
        #if key compared to root.key < 0
        if key < root.key:
            #root.left = insertRec(root.left, key)
            root.left = self.insertRec(root.left, key)
        #if key compared to root.key > 0
        elif key > root.key:
            #root.right = insertRec(root.right, key)
            root.right = self.insertRec(root.right, key)
        #return root
        return root

    #search function taking key argument Big O: O(Log n)
    def search(self, key):
        #return searchRec(root, key) != null
        tempRoot = self.searchRec(self.root, key)
        if tempRoot is not None:
            return True
        else:   
            return False
    
    #searchRec function taking root and key O(Log n)
    def searchRec(self, root, key):
        #if root = null or root.key.equals(key)
        if root is None or root.key == key:
            #return root
            return root
        #if key compared to root.key < 0
        if key < root.key:
            #return searchRec(root.left, key)
            return self.searchRec(root.left, key)
        #return searchRec(root.right, key)
        return self.searchRec(root.right, key)

#Prints a message after the bot successfully connects to Discord, Learned from ChatGpt
@bot.event
async def onReady():
    print(f'logged in as {bot.user}')

#Defines a BinarySearchTree object for on_message to utilize
bst = BinarySearchTree()
bstFile = bst.GenBstFile()

#Scans messages sent by users for banned words and if a banned word is found a warning message is sent
@bot.event
async def on_message(message):
    await bstFile.messageMonitor(message)

#Defines the hello command, when user calls $hello the bot will send a message saying Hello!, Learned from ChatGpt  
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
