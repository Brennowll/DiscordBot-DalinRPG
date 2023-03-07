"""
Módulo para armazenar a categoria de comandos do
bot relacionados a eventos e gerenciamento do bot.

Contém:
    class Gerenciador: (commands.cog)
        Classe de cogs para a categoria 'gerenciamento' do DiscordBOT
    class setup: (bot/client)
        Classe para inicializar a cog de comandos
        'Gerenciador' no arquivo Main.py
"""

from discord.ext import commands
import discord
import yaml

# Testar se consigo dar nomes pras funções listener

class Gerenciador(commands.Cog):

    """
    Classe de Cogs para exportar listener commands
    da categoria 'eventos e gerenciamento'

    Listener Commands:\n
        on_ready: Mostra uma mensagem no terminal quando o
        bot for inicializado\n
        on_guild_join: Armazena o prefixo padrão para o
        server que o bot entrou no arquivo prefixos.yaml\n
        on_guild_remove: Deleta o prefixo armazenado no arquivo
        prefixos.yaml do server que o bot saiu\n
        on_message: Manda o prefixo para o server que o usuário
        marcou o nome do bot\n
        on_voice_state_update: Disconecta o bot do canal de voz
        se ele for o único conectado no mesmo
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):

        """Mostra uma mensagem de aviso quando o bot for totalmente
        inicializado e faz a sincronização dos comandos, mostrando
        quantos comandos foram sincronizados no terminal"""

        print(f"Estou pronto, logado como {self.bot.user}")
        try:
            synced = await self.bot.tree.sync()
            print(f"Consegui syncar {len(synced)} commandos!")

        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):

        """Cadastra o id do server que o bot entrou no arquivo
        prefixos.yaml com o prefixo padrão '!'"""

        db_prefixos = "bancodedados/prefixos.yaml"

        with open(db_prefixos, "r", encoding= "utf8") as pasta:
            prefixo = yaml.safe_load(pasta)

        prefixo[str(guild.id)] = "!"

        with open(db_prefixos, "w", encoding= "utf8") as pasta:
            yaml.dump(prefixo, pasta)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        """Exclui o id da guilda do arquivo prefixos.yaml"""

        db_prefixos = "bancodedados/prefixos.yaml"

        with open(db_prefixos, "r", encoding= "utf8") as pasta:
            prefixo = yaml.safe_load(pasta)

        del prefixo[str(guild.id)]

        with open(db_prefixos, "w", encoding= "utf8") as pasta:
            yaml.dump(prefixo, pasta)

    @commands.Cog.listener()
    async def on_message(self, message):

        """Verifica se a mensagem mandada é uma marcação do
        user do bot, se sim, manda o prefixo do bot para o
        server em que foi marcado"""

        if message.mentions[0] == self.bot.user:

            db_prefixos = "bancodedados/prefixos.yaml"
            with open(db_prefixos, "r", encoding= "utf8") as pasta:
                prefixos = yaml.safe_load(pasta)

            pre = prefixos[str(message.guild.id)]
            mensagem = f'Meu prefixo para este server é "{pre}"!!'

            embed = discord.Embed(title= mensagem, color=0xdfca7f)
            await message.channel.send(embed=embed)
            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member):

        """Verifica se o bot é o único no canal de voz,
        se for para a música que está tocando e disconecta
        o bot do canal de voz"""

        voice_state = member.guild.voice_client
        estado_voz_existe = voice_state is not None
        somente_bot_conectado = len(voice_state.channel.members) == 1

        if estado_voz_existe and somente_bot_conectado:
            voice_state.stop()
            await voice_state.disconnect()

async def setup(bot):

    """
    Função assíncrona que faz o executa a cog
    desse arquivo no Main.py

    Args:
        bot: client ou bot do arquivo Main.py
    """

    await bot.add_cog(Gerenciador(bot))