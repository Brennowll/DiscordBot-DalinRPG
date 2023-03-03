import discord
import asyncio 
import yaml

from os import listdir
from discord.ext import commands
from decouple import config

intents=discord.Intents.default()
intents.presences=True
intents.message_content=True
intents.members=True
intents.voice_states=True

def pegar_prefixo_server(bot, message):
    with open("bancodedados/prefixos.yaml", "r") as pasta:
        prefixo = yaml.safe_load(pasta)
    return prefixo[str(message.guild.id)]

activity = discord.Game(name="/ajuda")
bot = commands.Bot(command_prefix=pegar_prefixo_server, intents=intents,  activity=activity, status=discord.Status.idle)

async def carregar():
    for pasta in listdir("./comandos"):
        if pasta.endswith(".py"):
            await bot.load_extension(f"comandos.{pasta[:-3]}")
    await bot.load_extension("gerenciador")

TOKEN_SECRETO = config("TOKEN")
async def principal():
    await carregar()
    await bot.start(f"{TOKEN_SECRETO}")

asyncio.run(principal())