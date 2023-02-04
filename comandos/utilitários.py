from discord.ext import commands
from random import choice
import discord
import yaml

def pegarpos(string, subs, n):
    start = string.find(subs)
    while start >= 0 and n > 1:
        start = string.find(subs, start+1)
        n -= 1
    return start

class utilit(commands.Cog):
    """Comandos de utilidade dentro do discord"""

    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="calc", description='Calcula a expressão digitada!')
    async def calc(self, ctx, *, conta: str):
        try:
            if conta.count("x") > 0:
                conta = conta.replace("x", '*')
            
            embed = discord.Embed(title=f"Resultado: {eval(conta)}", 
                description=f"[{conta}]",
                color=0xdfca7f)
            await ctx.send(embed=embed)
        
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Oops.. digite uma conta válida:\n3x4+7 // 4/2-1 // (8+5)x4")
            await ctx.send(embed=embed, ephemeral=True)
    
    @commands.hybrid_command(name="sort", description="Sorteia algo entre Ex: a/b/c/d")
    async def sortear(self, ctx, *, entre: str):
        lis= list()
        barr = entre.count("/")

        if barr == 0:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Atenção, os valores pra serem sorteados devem estar entre barras (Ex: 1/3/5/7)")
            await ctx.send(embed=embed, ephemeral=True)

        else:
            for c in range(0, barr):
                if c == 0:
                    lis.append(entre[0: entre.find("/")])
                    lis.append(entre[entre.find("/")+1:entre.find("/", entre.find("/")+1)])
                elif c == barr - 1:
                    lis.append(entre[entre.rfind("/")+1:])
                else:
                    lis.append(entre[pegarpos(entre , "/", c+1)+1:pegarpos(entre, "/", c+2)])
            sort = choice(lis)

            embed = discord.Embed(title=f"sorteado: {sort}",
                description=f"Entre: {lis}",
                color=0xdfca7f)
            await ctx.send(embed=embed)

    @commands.hybrid_command(name="ajuda", description= "Como funciona os comandos do Dalin!")
    async def ajuda(self, ctx):
        embed = discord.Embed(color=0xdfca7f)
        embed.set_author(name="DalinRPG", icon_url="https://cdn.discordapp.com/attachments/1065414001418317865/1071041621816246352/DalinComFundo.png")
        embed.add_field(name="Rolagem de dados:", 
            value="""/rolar = Rola dados na mesma frase (2d6+3d20+4d4+10)
            \n/rolarum = Rola 1 tipo de dado
            \n/rolarloop = Rola um amontoado de dados mais de uma vez
            \n/sortdado = Sorteia um tipo de dado""",)
        embed.add_field(name="Trilha Sonora:", 
            value="""/criartrilha = Cadastra uma música como trilha sonora
            \n/trilha = Toca a trilha sonora cadastrada anteriormente a partir do apelido dado a ela (Em loop)
            \n/ptrilha = Para a trilha sonora que está tocando
            \n/deltrilha = Deleta uma trilha criada de escolha
            \n/deltodtrilhas = Deleta todas as trilhas que você cadastrou
            \n/vol = Altera o volume da trilha (0 - 150 limite)""",
            inline=False)
        embed.add_field(name="Utilidades:", 
            value="""/calc = Calcula uma expressão matemática digitada (2x7+3/2)
            \n/sort = sorteia algo entre os valores divididos com barra (um/dois/nome/lugar)
            \n/mudarpref = (Somente para administradores do server) Muda o prefixo do DalinRPG para aquele server
            \n-> Pingar/Mencionar o DalinRPG no chat = Mostra qual o prefixo do DalinRPG para o server
            \n/ajuda (nome do comando) = Digitar o /ajuda com um comando mostra detalhadamente sobre um comando expecífico""",
            inline=False)
        await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="mudarpref", description="Muda o prefixo do DalinRPG")
    @commands.has_permissions(administrator=True)
    async def mudarpref(self, ctx, *, novoprefixo: str):
        if len(novoprefixo) > 2:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Atenção, o novo prefixo digitado tem mais de 2 caracteres!")
            await ctx.send(embed=embed, ephemeral=True)

        elif novoprefixo.isnumeric() == True:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Atenção, o novo prefixo digitado não pode ser somente números!")
            await ctx.send(embed=embed, ephemeral=True)

        else:
            with open("bancodedados/prefixos.yaml", "r") as pasta:
                prefixo = yaml.safe_load(pasta)

            prefixo[str(ctx.guild.id)] = novoprefixo

            with open("bancodedados/prefixos.yaml", "w") as pasta:
                yaml.dump(prefixo, pasta)

            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"O prefixo do dalin bot agora é {novoprefixo}")
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(utilit(bot))