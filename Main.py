"""Arquivo pricipal que carrega as cogs dos arquivos
que armazenam as classes com os comandos do bot"""

from os import listdir
import asyncio
import discord
import yaml
from discord.ext import commands
from decouple import config

intents=discord.Intents.default()
intents.presences=True
intents.message_content=True
intents.members=True
intents.voice_states=True

def pegar_prefixo_server(bot, message):

    """
    Acha o prefixo que o server em específico usa

    Args:
        message (_type_): mensagem no canal de texto
        para extrair o id do server em que foi mandada
    """

    db_prefixos = "bancodedados/prefixos.yaml"
    with open(db_prefixos, "r", encoding= "utf8") as pasta:
        prefixo = yaml.safe_load(pasta)
    return prefixo[str(message.guild.id)]

activity = discord.Game(
    name= "/ajuda"
    )
bot = commands.Bot(
    command_prefix= pegar_prefixo_server,
    intents= intents,
    activity= activity,
    status= discord.Status.idle
    )

async def carregar():

    """Carrega as commands.cogs dos arquivos dentro da
    pasta 'comandos' """

    for pasta in listdir("./comandos"):
        if pasta.endswith(".py"):
            await bot.load_extension(f"comandos.{pasta[:-3]}")

TOKEN_SECRETO = str(config("TOKEN"))
async def principal():

    """Executa a função de carregamento das cogs e inicializa
    o bot a partir do token especificado no arquivo.env"""

    await carregar()
    await bot.start(TOKEN_SECRETO)

asyncio.run(principal())
