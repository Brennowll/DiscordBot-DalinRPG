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

# Especificar o erro dos excepts
# Testar vc: player sem o player

lista_volume = {}
queue = {}
tocando = []

def carregar_apelidos():
    """Lê e transfere os dados do arquivo apelidos.yaml
    para uma variável, retornando os valores dessa variável

    Returns:
        (list): valores lidos do arquivo apelidos.yaml
    """

    yaml_apelidos = "bancodedados/apelidos.yaml"
    with open(yaml_apelidos, "r", encoding= "utf8") as arq:
        arquiv = yaml.safe_load(arq)

    return arquiv

def mudar_apelidos(variavel):
    """Faz um safe dump no arquivo apelidos.yaml com
    os valores de uma variável

    Args:
        variavel: valor a se escrever no arquivo apelidos.yaml
    """

    yaml_apelidos = "bancodedados/apelidos.yaml"
    with open(yaml_apelidos, "w", encoding= "utf8") as arq:
        yaml.safe_dump(variavel, arq)

def repetir(vc, ctx):

    """
    Faz o loop da trilha sonora escolhida ao usar
    o comando /trilha, executando essa função sempre
    que o audio da trilha sonora acabar.

    Args:
        vc (_type_): variável que foi definida como voice channel
        ctx (_type_): contexto de onde o comando /trilha foi usado
    """

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
            mensagem = "O apelido pode ter no máximo 20 letras!"
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

        id_autor_message = f"{ctx.author.id}"
        arquiv = carregar_apelidos()

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

        chegou_limite_mus = len(arquiv[id_autor_message]) >= 11
        if chegou_limite_mus:

            mensagem = (
                f"Eeeepa {ctx.author.name}, ",
                "você já cadastrou 10 trilhas sonoras, ",
                "esse é o máximo!"
                )
            descricao = (
                "Da uma olhadinha nesses comandos aqui:",
                "\n/listatrilhas /deltrilha /deltodas",
                "\n(Pra você liberar espaço :p )"
                )

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
                )
            return

        mudar_apelidos(arquiv)

        mensagem = (
            f"{ctx.author.name} criou uma trilha sonora!",
            f"\nApelido: {apelido}\n",
            f"Nome da música: {nomearq}"
            )
        await mandar_embed(
            contexto= ctx,
            autor= mensagem
            )

        for arquivo_mp3 in ctx.message.attachments:
            await arquivo_mp3.save(f"musicas/{nomearq}")

    @commands.hybrid_command(
        name= "trilha",
        description= "Toca uma trilha criada com /criartrilha!"
        )
    async def trilha(self, ctx, *, apelido: str):

        """
        Faz o bot entrar no canal de voz de quem usou este comando
        e faz ele tocar a trilha sonora a partir do apelido usado
        para cadastrá-la com o comando /criartrilha

        Args:
            apelido (str): apelido da trilha sonora que quer tocar
        """

        try:
            voice_channel = ctx.author.voice.channel

        # Fazer um teste de que erro
        # aparece pra poder especificar o except
        except:
            voice_channel = None

        if voice_channel is None:
            mensagem = (
                "Você precisa entrar em ",
                "um canal de voz primeiro"
                )
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        arquiv = carregar_apelidos()
        id_autor_message = f"{str(ctx.author.id)}"

        try:
            id_existe = arquiv[id_autor_message]

        # Especificar o except
        except:
            id_existe = None

        if id_existe is None:
            mensagem = (
                "Você ainda não cadastrou nenhuma trilha sonora",
                )
            descricao = (
                "[tente o comando novamente ou crie uma ",
                "trilha sonora com o comando /criartrilha]"
                )
            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
                )
            return

        apelido_n_existe = apelido not in arquiv[id_autor_message]
        if apelido_n_existe:

            mensagem = "O apelido digitado não existe!"
            descricao = (
                "[tente o comando novamente ou use ",
                "/criartrilha /listatrilhas]"
                )

            await mandar_embed(
                contexto= ctx,
                desc= descricao,
                autor= mensagem,
                esconder= True
                )
            return

        nome_canal = ctx.voice_client
        nao_conectado = nome_canal is None

        if nao_conectado:
            vc = await voice_channel.connect()
        else:
            vc = nome_canal

        vc.stop()
        tocando.append(str(ctx.guild.id))

        nomemusica = f"{arquiv[id_autor_message][apelido]}"
        queue[id_autor_message] = nomemusica

        await mandar_embed(
            contexto= ctx,
            desc= f"[{nomemusica}]",
            autor= f"Tocando agora: {apelido}"
            )

        local_mus = f"musicas/{nomemusica}"

        vc.play(
            discord.FFmpegPCMAudio(source= local_mus),
            after= lambda e: repetir(vc=vc, ctx=ctx)
            )
        vc.source = discord.PCMVolumeTransformer(
                vc.source,
                volume=1.0
                )

    @commands.hybrid_command(
        name= "ptrilha",
        description= "Para a trilha sonora que está tocando!"
        )
    async def ptrilha(self, ctx):

        """Se uma trilha sonora estiver tocando no server do ctx
        para a trilha sonora e desconecta o bot do canal que
        ele está conectado"""

        id_guilda = str(ctx.guild.id)

        nada_tocando = id_guilda not in tocando
        if nada_tocando:

            mensagem = "Não tem nenhuma trilha sonora tocando!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        tocando.remove(id_guilda)

        voice_state = ctx.guild.voice_client
        voice_state.stop()
        await voice_state.disconnect()

        mensagem = "A trilha sonora parou!"
        await mandar_embed(
            contexto= ctx,
            autor= mensagem
            )

    @commands.hybrid_command(
        name= "listatrilhas",
        description= "Lista das trilhas que você cadastrou!"
        )
    async def listatrilhas(self, ctx):

        """Manda um embed no canal que o comando foi usado
        com uma lista das trilhas sonoras cadastradas pelo
        usuário que usou o comando"""

        arquiv = carregar_apelidos()
        id_autor_message = f"{str(ctx.author.id)}"

        try:
            id_existe = arquiv[id_autor_message]
        
        # Especificar except
        except:
            id_existe = None

        if id_existe is None:
            mensagem =  "Oops.. não parece que você tem alguma trilha criada!"
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

    @commands.hybrid_command(
        name= "deltrilha",
        description= "Deleta uma trilha criada!"
        )
    async def deltrilha(self, ctx, *, apelido: str):
        
        """
        Deleta o arquivo.mp3 e os dados gravados no apelidos.yaml
        sobre uma trilha sonora criada com o comando /criartrilha

        Args:
            apelido (str): apelido da trilha sonora a se excluir
        """

        arquiv = carregar_apelidos()

        try:
            sem_dados = None
            nome_musica = arquiv[str(ctx.author.id)][apelido]

        # Especificar except
        except:
            sem_dados = True

        if sem_dados is True:
            descricao = (
                "(Tente esses comandos: ",
                "/listatrilha /criartrilha)"
                )
            mensagem = (
                "ish.. parece que essa trilha não existe ",
                "ou você não cadastrou nenhuma trilha"
                )
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

        mudar_apelidos(arquiv)

        mensagem = f"{ctx.author.name} deletou a trilha {apelido}!"
        await mandar_embed(
            contexto= ctx,
            desc= f"({musicdel})",
            autor= mensagem
            )

    @commands.hybrid_command(
        name= "deltodtrilhas",
        description= "Apaga todas as suas trilhas criadas!"
        )
    async def deltodastrilhas(self, ctx):

        """Apaga todos os arquivos.mp3 e os dados de trilha
        sonora que o autor cadastrou com o comando /criartrilha."""

        arquiv = carregar_apelidos()

        id_autor_n_cadastrado = str(ctx.author.id) not in arquiv
        if id_autor_n_cadastrado:

            descricao = (
                "(Tente esses comandos: /listatrilha /criartrilha)",
                )
            mensagem = (
                "Oops.. Você não tem nenhuma trilha criada :/"
                )

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

        mudar_apelidos(arquiv)

        mensagem = f"{ctx.author.name} deletou todas as trilhas!"
        descricao = f"({mus_para_del})"
        await mandar_embed(
            contexto= ctx,
            desc= descricao,
            autor= mensagem,
            )

    @commands.hybrid_command(
        name= "vol",
        description= "Muda o volume do DalinRPG!"
        )
    async def voice_connect(self, ctx, *, volume: int):

        """
        Muda o volume da trilha sonora que foi iniciada com
        o comando /trilha

        Args:
            volume (int): numero do volume escolhido, entre 1/150
        """

        id_guilda = str(ctx.guild.id)

        try:
            voice_channel = ctx.author.voice.channel
        except:
            voice_channel = None

        autor_n_conectado = voice_channel is None
        n_tocando_server = id_guilda not in tocando

        if autor_n_conectado or n_tocando_server:
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

        vol_invalido = volume < 0 or volume > 150
        if vol_invalido:
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

async def setup(bot):
    await bot.add_cog(Musica(bot))