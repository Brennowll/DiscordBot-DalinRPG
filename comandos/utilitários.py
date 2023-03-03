from discord.ext import commands
from random import choice
from modulos.funcoes import mandar_embed
from modulos.funcoes import pegar_posicao_str

import discord
import yaml


class utilit(commands.Cog):
    """Comandos de utilidade dentro do discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name = "calc", description = 'Calcula a expressão digitada!')
    async def calc(self, ctx, *, conta: str):
        if conta.count("x") > 0:
            conta = conta.replace("x", '*')

        try:
            resultado = eval(conta)
        except:
            resultado = None

        if resultado is None:
            mensagem = """Oops.. digite uma conta válida:
                \nExemplos:\n3x4+7 // 4/2-1 // (8+5)x4"""

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

    @commands.hybrid_command(name = "sort", description = "Sorteia algo entre Ex: a/b/c/d")
    async def sortear(self, ctx, *, entre: str):
        lista_para_sortear = list()
        barr = entre.count("/")

        if barr == 0:
            mensagem = "Atenção, os valores pra serem sorteados devem estar entre barras (Ex: 1/3/5/7)"

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        for c in range(0, barr):

            if c == 0:
                posicao_primeira_barra = entre.find("/")
                posicao_segunda_barra = entre.find("/", entre.find("/")+1)

                primeiro_valor = entre[0: posicao_primeira_barra]
                segundo_valor = entre[posicao_primeira_barra+1:posicao_segunda_barra]

                lista_para_sortear.append(primeiro_valor)
                lista_para_sortear.append(segundo_valor)

            elif c == barr - 1:
                posicao_ultima_barra = entre.rfind("/")

                ultimo_valor = entre[posicao_ultima_barra+1:]

                lista_para_sortear.append(ultimo_valor)

            else:
                posicao_barra_anterior = pegar_posicao_str(entre , "/", c+1)
                posicao_barra_posterior = pegar_posicao_str(entre, "/", c+2)

                valor_encontrado = entre[posicao_barra_anterior+1:posicao_barra_posterior]

                lista_para_sortear.append(valor_encontrado)

        sort = choice(lista_para_sortear)
        mensagem = f"sorteado: {sort}"
        descricao = f"Entre: {lista_para_sortear}"

        await mandar_embed(
            contexto= ctx,
            autor= mensagem,
            desc= descricao
        )

    @commands.hybrid_command(name = "ajuda", description = "Como funciona os comandos do Dalin!")
    async def ajuda(self, ctx):
        link_icone = "https://cdn.discordapp.com/attachments/1065414001418317865/1071041621816246352/DalinComFundo.png"

        descricao_dados = """/rolar = Rola dados na mesma frase (2d6+3d20+4d4+10)
            \n/rolarum = Rola 1 tipo de dado
            \n/rolarloop = Rola um amontoado de dados mais de uma vez
            \n/sortdado = Sorteia um tipo de dado"""

        descricao_trilha = """/criartrilha = Cadastra uma música como trilha sonora
            \n/trilha = Toca a trilha sonora cadastrada anteriormente a partir do apelido dado a ela (Em loop)
            \n/ptrilha = Para a trilha sonora que está tocando
            \n/deltrilha = Deleta uma trilha criada de escolha
            \n/deltodtrilhas = Deleta todas as trilhas que você cadastrou
            \n/vol = Altera o volume da trilha (0 - 150 limite)"""

        descricao_utilidades = """/calc = Calcula uma expressão matemática digitada (2x7+3/2)
            \n/sort = sorteia algo entre os valores divididos com barra (um/dois/nome/lugar)
            \n/mudarpref = (Somente para administradores do server) Muda o prefixo do DalinRPG para aquele server
            \n-> Pingar/Mencionar o DalinRPG no chat = Mostra qual o prefixo do DalinRPG para o server
            \n/ajuda (nome do comando) = Digitar o /ajuda com um comando mostra detalhadamente sobre um comando expecífico"""

        embed = discord.Embed(
            color = 0xdfca7f
        )
        embed.set_author(
            name = "DalinRPG",
            icon_url = link_icone
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

    @commands.hybrid_command(name = "mudarpref", description = "Muda o prefixo do DalinRPG")
    @commands.has_permissions(administrator = True)
    async def mudarpref(self, ctx, *, novoprefixo: str):

        if len(novoprefixo) > 2:
            mensagem = "Atenção, o novo prefixo digitado tem mais de 2 caracteres!"

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        elif novoprefixo.isnumeric() is True:
            mensagem = "Atenção, o novo prefixo digitado não pode ser somente números!"

            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
            )

            return

        with open("bancodedados/prefixos.yaml", "r") as pasta:
            prefixo = yaml.safe_load(pasta)

        prefixo[str(ctx.guild.id)] = novoprefixo

        with open("bancodedados/prefixos.yaml", "w") as pasta:
            yaml.dump(prefixo, pasta)

        mensagem = f"O prefixo do dalin bot agora é {novoprefixo}"

        await mandar_embed(
            contexto= ctx,
            autor= mensagem
        )

async def setup(bot):
    await bot.add_cog(utilit(bot))