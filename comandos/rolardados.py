import discord
from discord.ext import commands
from random import randint, choice


class Rolardados(commands.Cog):
    """Rola dados de todos os tipos"""

    def __init__(self, bot):
        self.bot = bot
    
    @commands.hybrid_command(name="rolarum", description="Rola UM dado de sua escolha!")
    async def rolarum(self, ctx, *, quant: int, lados: int):
        try:
            if lados != 4 and lados != 6 and lados != 8 and lados != 10 and lados != 12 and lados !=20 and lados != 100:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O dado que você digitou não existe!!",)
                await ctx.send(embed=embed, ephemeral=True)
            else:
                dados = list()
                som = 0

                for c in range(0, quant):
                    dados.append(randint(1, lados))
                
                for d in range(0, quant):
                    num = dados[d]
                    som += num
                
                embed = discord.Embed(description= f"Soma das rolagens: {som}", color=0xdfca7f)
                embed.set_author(name=f"Resultado: {dados}",)
                await ctx.send(embed=embed)
                dados.clear()
            
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Oops.. use o /rolarum para este comando!\n..é mais estável :)")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="rolar", description="Rola dados! (Ex: 1d8+3d6+2d12+20)")
    async def rolar(self, ctx, *, dado: str):
        quant1 = quant2 = quant3 = 0
        lados1 = lados2 = lados3 = 4
        somar = 0
        tipo = dado.count("d")
        mais = dado.count("+")

        try:
            quant1 = int(dado[0:dado.find("d")])
            if tipo == 1 and mais == 0:
                lados1 = int(dado[dado.find("d")+1:])
            elif tipo == 1 and mais == 1:
                lados1 = int(dado[dado.find("d")+1:dado.find("+")])
                somar = int(dado[dado.find("+")+1:])

            elif tipo == 2 and mais == 1:
                lados1 = int(dado[dado.find("d")+1:dado.find("+")])
                quant2 = int(dado[dado.find("+")+1:dado.find("d", 3)])
                lados2 = int(dado[dado.find("d", 3)+1:])
            elif tipo == 2 and mais == 2:
                lados1 = int(dado[dado.find("d")+1:dado.find("+")])
                quant2 = int(dado[dado.find("+")+1:dado.find("d", 3)])
                lados2 = int(dado[dado.find("d", 3)+1:dado.rfind("+")])
                somar = int(dado[dado.rfind("+")+1:])

            elif tipo == 3 and mais == 2:
                lados1 = int(dado[dado.find("d")+1:dado.find("+")])
                quant2 = int(dado[dado.find("+")+1:dado.find("d", 3)])
                lados2 = int(dado[dado.find("d", 3)+1:dado.rfind("+")])
                quant3 = int(dado[dado.rfind("+")+1:dado.rfind("d")])
                lados3 = int(dado[dado.rfind("d")+1:])
            elif tipo == 3 and mais == 3:
                lados1 = int(dado[dado.find("d")+1:dado.find("+")])
                quant2 = int(dado[dado.find("+")+1:dado.find("d", 3)])
                lados2 = int(dado[dado.find("d", 3)+1:dado.find("+", 7)])
                quant3 = int(dado[dado.find("+", 7)+1:dado.rfind("d")])
                lados3 = int(dado[dado.rfind("d")+1:dado.rfind("+")])
                somar = int(dado[dado.rfind("+")+1:])
            
            if lados1 != 4 and lados1 != 6 and lados1 != 8 and lados1 != 10 and lados1 != 12 and lados1 !=20 and lados1 != 100:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O 1º dado que você digitou não existe!")
                await ctx.send(embed=embed, ephemeral=True)
            elif lados2 != 4 and lados2 != 6 and lados2 != 8 and lados2 != 10 and lados2 != 12 and lados2 !=20 and lados2 != 100:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O 2º dado que você digitou não existe!")
                await ctx.send(embed=embed, ephemeral=True)
            elif lados3 != 4 and lados3 != 6 and lados3 != 8 and lados3 != 10 and lados3 != 12 and lados3 !=20 and lados3 != 100:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O 3º dado que você digitou não existe!")
                await ctx.send(embed=embed, ephemeral=True)
            else:
                dados = list()
                temp = list()
                quanttot = quant1+quant2+quant3
                som = 0

                for e in range(0, tipo):
                    e += 1
                    if e == 1:
                        for c in range(0, quant1):
                            dados.append(randint(1, lados1))
                    elif e == 2:
                        for c in range(0, quant2):
                            dados.append(randint(1, lados2))
                    elif e == 3:
                        for c in range(0, quant3):
                            dados.append(randint(1, lados3))

                for h in range(0, quanttot):
                    som += dados[h]
                som += somar

                embed = discord.Embed(title= f"Resultado (Soma): {som}", color=0xdfca7f)
                if tipo == 1:
                    embed.add_field(name=f"d{lados1}'s:", value=f"{dados}")
                elif tipo == 2:
                    embed.add_field(name=f"d{lados1}'s:", value=f"{dados[0: quant1]}")
                    embed.add_field(name=f"d{lados2}'s:", value=f"{dados[quant1:]}")
                elif tipo == 3:
                    embed.add_field(name=f"d{lados1}'s:", value=f"{dados[0: quant1]}")
                    embed.add_field(name=f"d{lados2}'s:", value=f"{dados[quant1:quant1+quant2]}")
                    embed.add_field(name=f"d{lados3}'s:", value=f"{dados[quant1+quant2:]}")
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Oops.. use uma rolagem válida!\nEx: 2d20+10 // 10d8+2d4\nUse o /ajuda para entender melhor")
            await ctx.send(embed=embed, ephemeral=True)
        
    @commands.hybrid_command(name="rolarloop", description="Rola um amontoado de dados mais de uma vez")
    async def rolarloop(self, ctx, *, quant: int, lados: int, soma: int, vezes: int):
        try:
            if lados != 4 and lados != 6 and lados != 8 and lados != 10 and lados != 12 and lados !=20 and lados != 100:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O dado que você digitou não existe!!")
                await ctx.send(embed=embed, ephemeral=True)
            else:
                dados = list()
                somlist = list()
                temp = list()
                som = 0

                for e in range(0, vezes):
                    for c in range(0, quant):
                        temp.append(randint(1, lados))
                    dados.append(temp[:])
                    temp.clear()

                for h in range(0, vezes):
                    for f in range(0, quant):
                        som += dados[h][f]
                    somlist.append(som)
                    som = 0

                embed = discord.Embed(title= "Resultados:", color=0xdfca7f)
                for d in range(0, vezes):
                    embed.add_field(name=f"{d+1}º:", value=f"{dados[d]}\nSoma: {somlist[d]+soma}")
                await ctx.send(embed=embed)
                temp.clear()
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Oops.. use o /rolarloop para este comando!\n..é mais estável :)")
            await ctx.send(embed=embed, ephemeral=True)
            
    @commands.hybrid_command(name="sortdado", description='Sorteia um tipo de dado!')
    async def sortdado(self, ctx):
        tipos = ["d4", "d6", "d8", "d10", "d12", "d20", 'd100']
        sort = choice(tipos)
        
        embed = discord.Embed(color=0xdfca7f)
        embed.set_author(name=f"{ctx.author.name}, o tipo de dado sorteado foi: {sort}")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Rolardados(bot))