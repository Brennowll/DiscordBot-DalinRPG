"""
Módulo para armazenar a categoria de comandos do
bot relacionados a dados e rolagem de dados.

Contém\n
    class Rolardados: (commands.cog)\n
        Classe de cogs para a categoria rolagem de dados do DiscordBOT\n
    class setup: (bot/client)\n
        Classe para inicializar a cog de comandos
        'Rolar dados' no arquivo Main.py
"""


from random import randint, choice
from discord.ext import commands
import discord
from modulos.funcoes import mandar_embed


class RolarDados(commands.Cog):

    """
    Classe de cogs para exportar hybrid commands
    da categoria de comandos 'Rolagem de dados'

    Hybrid Commands:\n
        rolarum = faz a rolagem de um dado\n
        rolar = rolagem multiplos dados em uma str\n
        rolarloop = faz um loop da função 'rolarum'\n
        sortdado = sorteia um tipo de dado
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name= "rolarum",
        description= "Rola UM dado de sua escolha!"
        )
    async def rolarum(self, ctx, *, quant: int, lados: int):

        """
        hybrid command, rola um dado a partir da
        quantidade de dados e de quantos lados o dado tem

        Args:
            ctx (_type_): contexto do comando executado
            quant (int): quantidade de dados para rolar
            lados (int): tipo de dado, quantos lados tem
        """

        lista_dados_validos = [4, 6, 8, 10, 12, 20, 100]
        verificar_dados = lados in lista_dados_validos

        if not verificar_dados:
            mensagem = "O dado que você digitou não existe!!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        dados_rolados = [
            randint(1, lados)
            for _ in range (0, quant)
            ]
        soma_todas_rolagens = sum(dados_rolados)

        descricao = f"Soma das rolagens: {soma_todas_rolagens}"
        mensagem = f"Resultado: {dados_rolados}"
        await mandar_embed(
            contexto= ctx,
            desc= descricao,
            autor= mensagem
            )

    @commands.hybrid_command(
        name= "rolar",
        description= "Rola dados! (Ex: 1d8+3d6+2d12+20)"
        )
    async def rolar(self, ctx, *, dado: str):

        """
        hybrid command, faz a rolagem de multiplos dados a
        partir da string passada Ex: '2d6+3d8+5'

        Args:
            ctx (_type_): contexto do comando
            dado (str): valor completo para rolagem dos dados
        """

        contagem_d = dado.count("d")
        rolagem_invalida = contagem_d == 0

        if rolagem_invalida:
            mensagem = "Digite uma rolagem de dados válida!"
            descricao = "Exemplos: 2d20+3d12 / 3d100 / 1d10+5"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                desc= descricao,
                esconder= True
                )
            return

        quantidades_a_rolar = []
        tipo_dados_p_rolar = []

        dados_separados = dado.split(sep= "+")
        valor_para_somar = 0

        for strdado in dados_separados:

            soma_da_rolagem = strdado.count("d") == 0
            if soma_da_rolagem:
                valor_para_somar = int(strdado)
                break

            separar = strdado.split(sep= "d")

            quantidades_a_rolar.append(int(separar[0]))
            tipo_dados_p_rolar.append(int(separar[1]))

        lista_dados_validos = [4, 6, 8, 10, 12, 20, 100]
        dados_invalidos = [
            valor
            for valor in tipo_dados_p_rolar
            if valor not in lista_dados_validos
            ]
        verificar_tipos_dados = len(dados_invalidos) == 0

        if not verificar_tipos_dados:
            mensagem = "Um dos dados que você digitou não existe!"
            descricao = "dados existentes: (4, 6, 8, 10, 12, 20, 100)"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                desc= descricao,
                esconder= True
                )
            return

        dados_sorteados = [
            randint(1, tipo_dados_p_rolar[pos])
            for pos in range(0, len(quantidades_a_rolar))
            for _ in range(0, quantidades_a_rolar[pos])
            ]

        som_quantidades = 0
        lista_organizada = []

        for valor in quantidades_a_rolar:
            som_final = som_quantidades + valor

            rolagem = list(dados_sorteados[som_quantidades: som_final])
            lista_organizada.append(rolagem)

            som_quantidades += valor

        soma_todas_rolagens = sum(dados_sorteados) + valor_para_somar
        mensagem_titulo = f"Resultado (Soma): {soma_todas_rolagens}"

        embed = discord.Embed(
            title= mensagem_titulo,
            color= 0xdfca7f
            )

        posicao = 0
        for valor in tipo_dados_p_rolar:
            titulo_field = f"d{valor}'s"
            descricao_field = str(lista_organizada[posicao])

            posicao += 1

            embed.add_field(
                name= titulo_field,
                value= descricao_field
                )

        await ctx.send(
            embed= embed
            )

    @commands.hybrid_command(
        name= "rolarloop",
        description= "Rola um amontoado de dados mais de uma vez"
        )
    async def rolarloop(
        self, ctx, *,
        quant: int, lados: int,
        soma: int, vezes: int
        ):

        """
        hybrid command, faz a rolagem de um dado em loop
        Ex: Um RPG player tem 3 ações e quer atacar em todas

        Args:
            ctx (_type_): contexto do comando
            quant (int): quantidade de dados a rolar
            lados (int): tipo de dado a rolar
            soma (int): valor a se somar no final dos loops
            vezes (int): quantos loops irão ser feitos
        """

        lista_dados_validos = [4, 6, 8, 10, 12, 20, 100]
        dados_validados = lados in lista_dados_validos

        if not dados_validados:
            mensagem = "O dado que você digitou não existe!!"
            await mandar_embed(
                contexto= ctx,
                autor= mensagem,
                esconder= True
                )
            return

        dados = []
        lista_somas = []
        temp = []

        for _ in range(0, vezes):
            temp = [
                randint(1, lados)
                for _ in range (0, quant)
                ]

            dados.append([*temp])
            temp.clear()

        for lista in dados:
            lista_somas.append(sum(lista))

        embed = discord.Embed(
            title= "Resultados:",
            color=0xdfca7f
            )

        for loop_rolagem in range(0, vezes):
            
            mensagem = f"{loop_rolagem+1}º:"
            sub_mensagem = f"{dados[loop_rolagem]}"\
                f"\nSoma: {lista_somas[loop_rolagem]+soma}"

            embed.add_field(
                name= mensagem,
                value= sub_mensagem
                )

        await ctx.send(embed=embed)

    @commands.hybrid_command(
        name= "sortdado",
        description= 'Sorteia um tipo de dado!'
        )
    async def sortdado(self, ctx):

        """
        hybrid command, sorteia um tipo de dado
        dos 7 tipos clássicos [d4 a d100]

        Args:
            ctx (_type_): contexto do comando
        """

        tipos = [
            "d4", "d6", "d8",
            "d10", "d12", "d20",
            'd100'
            ]
        sort = choice(tipos)

        mensagem = f"{ctx.author.name},"\
            f" o tipo de dado sorteado foi: {sort}"
        await mandar_embed(
            contexto= ctx,
            autor= mensagem
            )

async def setup(bot):

    """
    Função assíncrona que faz o executa a cog
    desse arquivo no Main.py

    Args:
        bot: client ou bot do arquivo Main.py
    """

    await bot.add_cog(RolarDados(bot))
