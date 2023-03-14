"""
Módulo para armazenar a categoria de comandos do
bot relacionados a utilidade e geral.

Contém:\n
    class Utilidades: (commands.cog)\n
        Classe de cogs para a categoria rolagem de dados do DiscordBOT\n
    class setup: (bot/client)\n
        Classe para inicializar a cog de comandos
        'Utilidades' no arquivo Main.py
"""


from random import choice
import discord
import yaml
from discord.ext import commands
from sympy import sympify
from sympy import SympifyError
from modulos.funcoes import mandar_embed


class Utilidades(commands.Cog):

    """
    Classe cog para exportar hybrid commands
    da categoria de comandos 'utilidades'

    Hybrid commands:\n
        calc = calcula uma expressão matemática\n
        sort = sorteia valores entre barras '/'\n
        ajuda = descrição dos comandos do bot\n
        mudarpref = muda o prefixo do  bot
        para o server específico server
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name= "calc",
        description= 'Calcula a expressão digitada!'
        )
    async def calc(self, ctx, *, conta: str):

        """
        hybrid command, faz o calculo de uma expressão
        matemática simples e mostra o resultado

        Args:
            ctx (autodefinido): contexto do comando
            conta (str): expressão matemática p/ calcular
        """

        tem_x_conta = conta.count("x") > 0
        if tem_x_conta:
            conta = conta.replace("x", '*')

        try:
            resultado = int(sympify(conta))
        except (SympifyError, TypeError):
            resultado = None

        if resultado is None:
            mensagem = "Oops.. digite uma conta válida:"\
                "\nExemplos:\n3x4+7 // 4/2-1 // (8+5)x4"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        mensagem =  f"Resultado: {resultado}"
        descricao = f"[{conta}]"
        await mandar_embed(
            contexto = ctx,
            titulo = mensagem,
            desc = descricao
            )

    @commands.hybrid_command(
        name= "sort",
        description= "Sorteia algo entre Ex: a/b/c/d"
        )
    async def sortear(self, ctx, *, entre: str):

        """
        hybrid command, sorteia um valor entre
        os valores passados no arg 'variável'

        Args:
            ctx (autodefinido): contexto do comando
            entre (str): valores a serem sorteados
            divididos por '/'
        """

        n_existe_barra = entre.count("/") == 0
        if n_existe_barra:

            mensagem = "Atenção, os valores pra serem "\
                "sorteados devem estar entre barras (Ex: 1/3/5/7)"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        lista_para_sortear = entre.split("/")
        sort = choice(lista_para_sortear)

        mensagem = f"sorteado: {sort}"
        descricao = f"Entre: {lista_para_sortear}"
        await mandar_embed(
            contexto= ctx,
            autor= mensagem,
            desc= descricao
            )

    @commands.hybrid_command(
        name= "ajuda",
        description= "Como funciona os comandos do Dalin!"
        )
    async def ajuda(self, ctx):

        """hybrid command, manda um embed no canal que o comando
        foi usado, com a lista de comandos do bot e sua descrição
        para uso dos usuários do discord"""

        descricao_dados = \
            "/rolar = Rola dados na mesma frase (2d6+3d20+4d4+10)"\
            "\n/rolarum = Rola 1 tipo de dado"\
            "\n/rolarloop = Rola um amontoado de dados mais de uma vez"\
            "\n/sortdado = Sorteia um tipo de dado"
        descricao_trilha = \
            "/criartrilha = Cadastra uma música como trilha sonora"\
            "\n/trilha = Toca a trilha sonora cadastrada anteriormente"\
            "a partir do apelido dado a ela (Em loop)"\
            "\n/ptrilha = Para a trilha sonora que está tocando"\
            "\n/deltrilha = Deleta uma trilha criada de escolha"\
            "\n/deltodtrilhas = Deleta todas as trilhas que você cadastrou"\
            "\n/vol = Altera o volume da trilha (0 - 150 limite)"
        descricao_utilidades = \
            "/calc = Calcula uma expressão matemática digitada (2x7+3/2)"\
            "\n/sort = sorteia algo entre os valores divididos com barra"\
            "(um/dois/nome/lugar)"\
            "\n/mudarpref = (Somente para administradores do server)"\
            "Muda o prefixo do DalinRPG para aquele server"\
            "\n-> Pingar/Mencionar o DalinRPG no chat ="\
            "Mostra qual o prefixo do DalinRPG para o server"\
            "\n/ajuda (nome do comando) = Digitar o /ajuda com um comando"\
            "mostra detalhadamente sobre um comando expecífico"

        embed = discord.Embed(
            color = 0xdfca7f
            )
        embed.set_author(
            name = "DalinRPG"
            )
        embed.add_field(
            name = "Rolagem de dados:",
            value = descricao_dados,
            )
        embed.add_field(
            name = "Trilha Sonora:",
            value = descricao_trilha,
            inline = False
            )
        embed.add_field(
            name = "Utilidades:",
            value = descricao_utilidades,
            inline = False
            )

        await ctx.send(
            embed = embed,
            ephemeral = True
            )

    @commands.hybrid_command(
        name= "mudarpref",
        description= "Muda o prefixo do DalinRPG"
        )
    @commands.has_permissions(
        administrator = True
        )
    async def mudarpref(self, ctx, *, novoprefixo: str):

        """
        hybrid command, muda o prefixo do bot para o
        server que o comando foi executado

        Args:
            ctx (autodefinido): contexto da mensagem
            novoprefixo (str): novo prefixo escolhido
        """

        pref_muito_grande = len(novoprefixo) > 2
        if pref_muito_grande:
            mensagem = "Atenção, o novo prefixo digitado tem "\
                "mais de 2 caracteres!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        pref_somente_num = novoprefixo.isnumeric() is True
        if pref_somente_num:
            mensagem = "Atenção, o novo prefixo digitado não "\
                "pode ser somente números!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        yaml_prefixos = "bancodedados/prefixos.yaml"

        with open(yaml_prefixos, "r", encoding= "utf8") as pasta:
            prefixo = yaml.safe_load(pasta)

        prefixo[str(ctx.guild.id)] = novoprefixo

        with open(yaml_prefixos, "w", encoding= "utf8") as pasta:
            yaml.dump(prefixo, pasta)

        mensagem = f"O prefixo do dalin bot agora é {novoprefixo}"
        await mandar_embed(
            contexto= ctx,
            autor= mensagem
            )

async def setup(bot):

    """
    Função assíncrona que executa a cog
    Utilidades no arquivo Main.py

    Args:
        bot: client ou bot do arquivo Main.py
    """

    await bot.add_cog(Utilidades(bot))
