import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# .env file se environment variables load karna
load_dotenv()

# Token ko environment variable se hasil karna
TOKEN = os.getenv('DISCORD_TOKEN')

# Intents ko define karna
intents = discord.Intents.default()
intents.presences = True  # Presence events ke liye
intents.members = True    # Member events ke liye
intents.message_content = True  # Message content access karne ke liye

# Bot ka prefix aur intents set karna
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot ready hone par message
@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')
    print("✅ Commands loaded:", bot.commands)  # Debugging ke liye

# Debugging: Check karo ke bot messages receive kar raha hai ya nahi
@bot.event
async def on_message(message):
    print(f" Message received: {message.content}")  # Console me message print karega
    await bot.process_commands(message)  # Ye zaroori hai taake commands kaam karein

# Simple command
@bot.command()
async def hello(ctx):
    print(f"🔹 !hello command used by {ctx.author}")  # Console me print karega
    await ctx.send("Hello, World!")

# Bot ko run karna
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN environment variable not found!")
