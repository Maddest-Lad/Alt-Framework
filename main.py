import time
import random
import json
from pathlib import Path

import discord
from discord import Option
from Modules.utils import *

# Initialize Classes
bot = discord.Bot()

# Server Scope (Ensures Bot Commands Are Updated Quickly)
scope = [] # This Can be Gathered by Right Clicking on a Server and Hitting "Copy Server ID"

# Startup
@bot.event
async def on_ready():
    print(f"{bot.user} Has Started Up Successfully")

# Example 1 - Simple Response
@bot.slash_command(guilds=scope)
async def d6(ctx):
    await ctx.respond(f"You Rolled a {random.randint(1,6)}")
    
    # You can Also Send Replies / Follow Ups; Also Spoilers
    await ctx.respond("What a Pro Gamer", spoiler=True) 
    
    
# Example 2 - Send a File
@bot.slash_command(guilds=scope)
async def rickroll(ctx):
    # You Don't Necessairly Need Both "content" and "file" though, but you can use both at the same time 
    await ctx.send(content="Ha Get Rick Rolled", file=discord.File("Resources/rickroll.gif"))


# Example 3 - Getting Around Time Limitations
@bot.slash_command(guilds=scope)
async def lengthy_task(ctx):
    # This Allows us to Ignore the 3-5 Second Time Limit
    await ctx.defer() 
    
    # Some Long Task (Think Stable Diffusion Image Generation)
    time.sleep(10)
    
    # Finally Send the Reply
    await ctx.followup.send("10 Seconds Have Passed")

# Example 4 - User Input and Other Fun
@bot.slash_command(guilds=scope)
async def set_status(ctx, status: Option(str, "the status to be set", required=True),
                     status_type: Option(str, "The Type of Custom Status", choices=["Game", "Streaming", "Watching", "Listening"], required=True),
                     url: Option(str, "The Streaming Url (If Streaming Status Type)", default="")):
    match status_type:
        case "Game":  
            await bot.change_presence(activity=discord.Game(name=status)) # Playing <status>
        case "Streaming":  
            await bot.change_presence(activity=discord.Streaming(name="status", url=url)) # Streaming <status>
        case "Listening":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=status)) # Listening to <status>
        case "Watching":
            await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status)) # Watching <status>

    # Only the Sender Can See This Response
    await ctx.respond("Status Set", ephemeral=True)  
    log(status)

# Example 5 - Just What the Fuck is ctx (context)
# See https://docs.pycord.dev/en/stable/_modules/discord/commands/context.html
@bot.slash_command(guilds=scope)
async def log_data(ctx, all_fields: Option(bool, "All Fields", required=False, default=False)):
    data = {}
    
    data = {
        'guild'        : ctx.guild,
        'channel'      : ctx.channel,
        'user'         : ctx.user,
        'perms'        : ctx.app_permissions    
    }
    
    if all_fields:
        data.update(vars(ctx))  
        
    # User Friendly
    formatted = '\n'.join([key + " : " + str(value) for key, value in data.items()])
    await ctx.respond(f"Data Dump:```{formatted}```")
    log(data)

if __name__ == '__main__':

    # Initialize Logs
    Path("Logs").mkdir(exist_ok=True)

    # Token Don't Share
    try:
        bot.run(open("token.secret", "r").read())
    except FileNotFoundError:
        print("Token Not Found, Please Generate a Token on https://discord.com/developers/applications, and then place it in a file Named \"token.secret\"")
