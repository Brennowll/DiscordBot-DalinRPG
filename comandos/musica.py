"""
Módulo para armazenar a categoria de comandos do
bot relacionados a música e trilha sonora.

Contém:
    class Musica: (commands.cog)
        Classe de cogs para a categoria 'Musica' do DiscordBOT
    class setup: (bot/client)
        Classe para inicializar a cog de comandos
        'Rolar dados' no arquivo Main.py
"""

from os import remove

from discord.ext import commands
import yaml
import discord

from modulos.funcoes import mandar_embed

def repetir(vc, ctx):
    """Função que coloca a música em loop"""

    global lista_volume
    id_autor_message = f"{ctx.author.id}"
    nome_musica = queue[id_autor_message]
    local_music = f"musicas/{nome_musica}"

    vc.play(
        discord.FFmpegPCMAudio(
            source = local_music
            ),
        after = lambda e: repetir(vc=vc, ctx=ctx)
        )
    vc.source = discord.PCMVolumeTransformer(
        vc.source,
        volume=lista_volume[f"{ctx.author.id}"]
        )
    vc.is_playing()


class Musica(commands.Cog):
    """
    Classe de cogs para exportar hybrid commands
    da categoria de comandos 'Musica e trilha sonora'

    Hybrid Commands:\n
        criartrilha = cadastra uma música como trilha sonora\n
        trilha = toca uma trilha sonora já cadastrada\n
        ptrilha = para a trilha que esta tocando\n
        listatrilhas = mostra a lista de trilhas cadastradas
        do usuário\n
        deltrilha = deleta uma trilha cadastrada pelo usuário\n
        deltodtrilhas = deleta todas as trilhas cadastradas
        pelo usuário\n
        vol = muda o volume da trilha sonora que esta tocando
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name= "criartrilha",
        description= 'Cadastra uma música como triha sonora'
        )
    async def criartrilha(
        self, ctx, *,
        apelido: str, arquivo_mp3: discord.Attachment
        ):
        """
        Salva o arquivo da musica na pasta 'musicas'
        e salva o apelido dado a trilha sonora no 
        arquivo apelidos.yaml

        Args:\n
            ctx (autodefinido): contexto do comando
            apelido (str): apelido para dar play na musica
            arquivo_mp3 (discord.Attachment): arquivo.mp3 da
            trilha sonora que vai ser salva
        """

        nomearq = arquivo_mp3.filename
        
        mb_15 = 15000000
        arq_maior_15mb = arquivo_mp3.size > mb_15
        
        if arq_maior_15mb:
            mensagem = "O arquivo.mp3 precisa ter 15mb ou menos!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        apelido_mt_grande = len(apelido) > 20
        if apelido_mt_grande:
            mensagem = f"O apelido pode ter no máximo 20 letras!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        tipo_arq_invalido = nomearq.endswith(".mp3") is False
        if tipo_arq_invalido:
            mensagem = "O arquivo precisa ser .mp3!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        yaml_apelidos = "bancodedados/apelidos.yaml"
        id_autor_message = f"{ctx.author.id}"

        with open(yaml_apelidos, "r", encoding= "utf8") as arq:
            arquiv = yaml.safe_load(arq)

        id_ja_cadastrado = id_autor_message in arquiv
        if id_ja_cadastrado :
            
            apelido_ja_cadastrado = apelido in arquiv[id_autor_message]
            if apelido_ja_cadastrado:
                
                nome_mus_substituida = arquiv[id_autor_message][apelido]
                mus_substituida = f"musicas/{nome_mus_substituida}"
                remove(mus_substituida)

            arquiv[id_autor_message][f"{apelido}"] = f"{nomearq}"

        else:
            arquiv[id_autor_message] = {apelido: f"{nomearq}"}

        if len(arquiv[id_autor_message]) >= 11:
            mensagem = f"Eeeepa {ctx.author.name}, você já cadastrou 10 trilhas sonoras, esse é o máximo!"
            descricao = f"Da uma olhadinha nesses comandos aqui:\n/listatrilhas /deltrilha /deltodas\n(Pra você liberar espaço :p )"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        with open(yaml_apelidos, "w", encoding= "utf8") as arq:
            yaml.dump(arquiv, arq)

        mensagem = f"{ctx.author.name} criou uma trilha sonora!\nApelido: {apelido}\nNome da música: {nomearq}"

        await mandar_embed(
            contexto= ctx,
            autor= mensagem
        )

        for arquivo_mp3 in ctx.message.attachments:
            await arquivo_mp3.save(f"musicas/{nomearq}")

    @commands.hybrid_command(name = "trilha", description = "Toca a trilha criada com /criartrilha!")
    async def trilha(self, ctx, *, apelido: str):
        global queue
        global tocando

        try:
            voice_channel = ctx.author.voice.channel
        except:
            voice_channel = None

        if voice_channel == None:
            mensagem = f"Você precisa entrar em um canal de voz primeiro"

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        with open("bancodedados/apelidos.yaml", "r") as arq:
            arquiv = yaml.safe_load(arq)

        id_autor_message = f"{str(ctx.author.id)}"

        try:
            id_existe = arquiv[id_autor_message]
        except:
            id_existe = None

        if id_existe == None:
            mensagem = "Você ainda não cadastrou nenhuma trilha sonora"
            descricao = "[tente o comando novamente ou crie uma trilha sonora com o /criartrilha]"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        if apelido not in arquiv[id_autor_message]:
            mensagem = "O apelido digitado não existe!"
            descricao = "[tente o comando novamente ou use /criartrilha /listatrilhas]"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        nome_canal = ctx.voice_client
        nao_conectado = nome_canal == None

        vc = await voice_channel.connect() if nao_conectado else nome_canal

        vc.stop()
        tocando.append(str(ctx.guild.id))

        nomemusica = f"{arquiv[id_autor_message][apelido]}"
        queue[id_autor_message] = nomemusica

        await mandar_embed(
            contexto= ctx,
            desc= f"[{nomemusica}]",
            autor= f"Tocando agora: {apelido}"
        )

        vc.play(
            discord.FFmpegPCMAudio(source = f"musicas/{nomemusica}"),
            after = lambda e: repetir(vc=vc, ctx=ctx)
        )
        vc.source = discord.PCMVolumeTransformer(
            vc.source,
            volume=1.0
        )

    @commands.hybrid_command(name = "ptrilha", description = "Para a trilha sonora que está tocando!")
    async def ptrilha(self, ctx):
        global tocando
        id_guilda = str(ctx.guild.id)

        if id_guilda not in tocando:
            mensagem = f"Não tem nenhuma trilha sonora tocando? ué"

            embed = discord.Embed(color = 0xdfca7f)
            embed.set_author(name = mensagem)
            await ctx.send(
                embed = embed,
                ephemeral = True
            )

            return

        tocando.remove(id_guilda)

        voice_state = ctx.guild.voice_client
        voice_state.stop()
        await voice_state.disconnect()

        mensagem = f"A trilha sonora parou!"

        await mandar_embed(
            contexto= ctx,
            autor= mensagem
        )

    @commands.hybrid_command(name = "listatrilhas", description = "Lista das trilhas que você cadastrou!")
    async def listatrilhas(self, ctx):
        with open("bancodedados/apelidos.yaml", "r") as pasta:
            arquiv = yaml.safe_load(pasta)

        id_autor_message = f"{str(ctx.author.id)}"

        try:
            id_existe = arquiv[id_autor_message]
        except:
            id_existe = None

        if id_existe == None:
            mensagem = "Oops.. não parece que você tem alguma trilha criada!"
            descricao = "(Tente o comando /criartrilha)"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        lista = str(arquiv[str(ctx.author.id)])
        listab = lista.replace("mp3',", "mp3'\n \n")
        listac = listab.replace("'", "")
        listad = listac.replace("{", "")

        mensagem = f"Lista de trilhas {ctx.author.name}:"

        await mandar_embed(
            contexto= ctx,
            desc= f"{listad}",
            autor= mensagem
        )

    @commands.hybrid_command(name = "deltrilha", description = "Deleta uma trilha criada!")
    async def deltrilha(self, ctx, *, apelido: str):
        with open("bancodedados/apelidos.yaml", "r") as arq:
                arquiv = yaml.safe_load(arq)

        try:
            sem_dados = None
            id_autor_dados = arquiv[str(ctx.author.id)]
            nome_musica = arquiv[str(ctx.author.id)][apelido]
        except:
            sem_dados = True

        if sem_dados == True:
            descricao = "(Tente esses comandos: /listatrilha /criartrilha)"
            mensagem = "ish.. parece que essa trilha não existe ou você não cadastrou nenhuma trilha"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        musicdel = nome_musica
        remove(f"musicas/{nome_musica}")
        del arquiv[str(ctx.author.id)][apelido]

        with open("bancodedados/apelidos.yaml", "w") as arq:
            yaml.dump(arquiv, arq)

        mensagem = f"{ctx.author.name} deletou a trilha {apelido}!"

        await mandar_embed(
            contexto= ctx,
            desc= f"({musicdel})",
            autor= mensagem
        )

    @commands.hybrid_command(name = "deltodtrilhas", description = "Apaga todas as suas trilhas criadas!")
    async def deltodastrilhas(self, ctx):

        with open("bancodedados/apelidos.yaml", "r") as arq:
            arquiv = yaml.safe_load(arq)

        if str(ctx.author.id) not in arquiv:
            descricao = "(Tente esses comandos: /listatrilha /criartrilha)"
            mensagem = "Oops.. Você não tem nenhuma trilha criada :/"

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
            )

            return

        mus_para_del = arquiv[str(ctx.author.id)]

        for mus in mus_para_del:
            remove(f"musicas/{arquiv[str(ctx.author.id)][mus]}")

        del arquiv[str(ctx.author.id)]

        with open("bancodedados/apelidos.yaml", "w") as arq:
            yaml.dump(arquiv, arq)

        mensagem = f"{ctx.author.name} deletou todas as trilhas!"
        descricao = f"({mus_para_del})"

        await mandar_embed(
            contexto= ctx,
            desc= descricao,
            autor= mensagem,
        )

    @commands.hybrid_command(name = "vol", description = "Muda o volume do DalinRPG!")
    async def voice_connect(self, ctx, *, volume: int):
        global lista_volume
        global tocando

        id_guilda = str(ctx.guild.id)

        try:
            voice_channel = ctx.author.voice.channel
        except:
            voice_channel = None

        if voice_channel == None or id_guilda not in tocando:
            mensagem = (
                "Você precisa entrar em um canal de voz ",
                "que esteja tocando uma trilha sonora primeiro"
            )

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        if volume < 0 or volume > 150:
            mensagem = "O volume precisa estar entre 0/150!"

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        vc: player = ctx.voice_client

        novovol = volume / 100
        lista_volume[f"{ctx.author.id}"] = novovol
        vc.source.volume = novovol

        mensagem = f"O volume foi alterado para: {volume}%"

        await mandar_embed(
            contexto= ctx,
            autor= mensagem
        )

lista_volume = {}
queue = {}
tocando = []

async def setup(bot):
    await bot.add_cog(Musica(bot))