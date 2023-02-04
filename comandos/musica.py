from os import remove
from discord.ext import commands
import discord
import yaml

def repetir(vc, ctx):
    """Função que coloca a música em loop"""

    global lista_volume

    vc.play(discord.FFmpegPCMAudio(source=f"musicas/{str(queue[0])}"), after=lambda e: repetir(vc=vc, ctx=ctx))
    vc.source = discord.PCMVolumeTransformer(vc.source, volume=lista_volume[f"{ctx.author.id}"])
    vc.is_playing()


class musica(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="criartrilha", description='Cadastra uma música como triha sonora')
    async def criartrilha(self, ctx, *, apelido: str, arquivo_mp3: discord.Attachment):
        nomearq = arquivo_mp3.filename
        try:
            if arquivo_mp3.size > 15000000:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O arquivo.mp3 precisa ter 15mb ou menos!")
                await ctx.send(embed=embed, ephemeral=True)
            else:
                if len(apelido) > 20:
                    embed = discord.Embed(color=0xdfca7f)
                    embed.set_author(name=f"O apelido pode ter no máximo 20 letras!")
                    await ctx.send(embed=embed, ephemeral=True)

                else:
                    if nomearq.endswith(".mp3"):
                        with open("bancodedados/apelidos.yaml", "r") as arq:
                            arquiv = yaml.safe_load(arq)

                        try:
                            remove(f"musicas/{arquiv[str(ctx.author.id)][f'{apelido}']}")
                        except:
                            pass

                        try:
                            arquiv[str(ctx.author.id)][f"{apelido}"] = f"{nomearq}"
                        except:
                            arquiv[str(ctx.author.id)] = {f"{apelido}": f"{nomearq}"}

                        if len(arquiv[str(ctx.author.id)]) >= 11:
                            embed = discord.Embed(description=f"Da uma olhadinha nesses comandos aqui:\n/listatrilhas /deltrilha /deltodas\n(Pra você liberar espaço :p )",color=0xdfca7f)
                            embed.set_author(name=f"Eeeepa {ctx.author.name}, você já cadastrou 10 trilhas sonoras, esse é o máximo!")
                            await ctx.send(embed=embed, ephemeral=True)

                        else:
                            with open("bancodedados/apelidos.yaml", "w") as arq:
                                yaml.dump(arquiv, arq)

                            embed = discord.Embed(color=0xdfca7f)
                            embed.set_author(name=f"{ctx.author.name} criou uma trilha sonora!\nApelido: {apelido}\nNome da música: {nomearq}")
                            await ctx.send(embed=embed)

                            for arquivo_mp3 in ctx.message.attachments:
                                await arquivo_mp3.save(f"musicas/{nomearq}")

                    else:
                        embed = discord.Embed(color=0xdfca7f)
                        embed.set_author(name=f"O arquivo precisa ser .mp3!")
                        await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)

    @commands.hybrid_command(name="trilha", description="Toca a trilha criada com /criartrilha!")
    async def trilha(self, ctx, *, apelido: str):
        try:
            global queue

            try:
                voice_channel = ctx.author.voice.channel
            except:
                voice_channel = None

            if voice_channel != None:
                try:
                    vc = await voice_channel.connect()
                except:
                    vc: player = ctx.voice_client

                vc.stop()

                with open("bancodedados/apelidos.yaml", "r") as arq:
                        arquiv = yaml.safe_load(arq)

                try:
                    del(queue[0])
                except:
                    pass

                try:
                    nomemusica = arquiv[str(ctx.author.id)][apelido]
                except:
                    embed = discord.Embed(description=f"[tente o comando novamente ou crie uma trilha sonora com o /criartrilha]", color=0xdfca7f)
                    embed.set_author(name=f"O apelido digitado não existe!")
                    await ctx.send(embed=embed, ephemeral=True)

                    await vc.disconnect()

                try:
                    queue.append(nomemusica)

                    embed = discord.Embed(description=f"[{nomemusica}]", color=0xdfca7f)
                    embed.set_author(name=f"Tocando agora: {apelido}")
                    await ctx.send(embed=embed)

                    print

                    # executable="C:/PATH_Programs/ffmpeg.exe", 
                    vc.play(discord.FFmpegPCMAudio(source=f"musicas/{str(queue[0])}"), after=lambda e: repetir(vc=vc, ctx=ctx))
                    vc.source = discord.PCMVolumeTransformer(vc.source, volume=1.0)
                except:
                    pass
                
            else:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"Você precisa entrar em um canal de voz primeiro")
                await ctx.send(embed=embed, ephemeral=True)
        except Exception as e:
            print(e)

    @commands.hybrid_command(name="ptrilha", description="Para a trilha sonora que está tocando!")
    async def ptrilha(self, ctx):
        try:
            voice_state = ctx.guild.voice_client
            voice_state.stop()
            await voice_state.disconnect()

            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"A trilha sonora parou!")
            await ctx.send(embed=embed)
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Não tem nenhuma trilha sonora tocando? ué")
            await ctx.send(embed=embed, ephemeral=True)
    
    @commands.hybrid_command(name="listatrilhas", description="Lista das trilhas que você cadastrou!")
    async def listatrilhas(self, ctx):
        with open("bancodedados/apelidos.yaml", "r") as pasta:
            arquiv = yaml.safe_load(pasta)

        try:
            lista = str(arquiv[str(ctx.author.id)])
            listab = lista.replace("mp3',", "mp3'\n \n")
            listac = listab.replace("'", "")
            listad = listac.replace("{", "")

            embed = discord.Embed(description=f"{listad}",color=0xdfca7f)
            embed.set_author(name=f"Lista de trilhas {ctx.author.name}:")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description=f"(Tente o comando /criartrilha)",color=0xdfca7f)
            embed.set_author(name=f"Oops.. não parece que você tem alguma trilha criada!")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="deltrilha", description="Deleta uma trilha criada!")
    async def deltrilha(self, ctx, *, apelido: str):
        try:
            with open("bancodedados/apelidos.yaml", "r") as arq:
                arquiv = yaml.safe_load(arq)

            musicdel = arquiv[str(ctx.author.id)][apelido]
            remove(f"musicas/{arquiv[str(ctx.author.id)][apelido]}")
            del arquiv[str(ctx.author.id)][apelido] 

            with open("bancodedados/apelidos.yaml", "w") as arq:
                yaml.dump(arquiv, arq)

            embed = discord.Embed(description=f"({musicdel})",color=0xdfca7f)
            embed.set_author(name=f"{ctx.author.name} deletou a trilha {apelido}!")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description=f"(Tente esses comandos: /listatrilha /criartrilha)",color=0xdfca7f)
            embed.set_author(name=f"ish.. parece que essa trilha não existe ou você não cadastrou nenhuma trilha")
            await ctx.send(embed=embed, ephemeral=True)

    @commands.hybrid_command(name="deltodtrilhas", description="Apaga todas as suas trilhas criadas!")
    async def deltodastrilhas(self, ctx):
        try:
            with open("bancodedados/apelidos.yaml", "r") as arq:
                arquiv = yaml.safe_load(arq)

            musicasdel = arquiv[str(ctx.author.id)]
            for mus in musicasdel:
                remove(f"musicas/{arquiv[str(ctx.author.id)][mus]}")
            del arquiv[str(ctx.author.id)]

            with open("bancodedados/apelidos.yaml", "w") as arq:
                yaml.dump(arquiv, arq)

            embed = discord.Embed(description=f"({musicasdel})",color=0xdfca7f)
            embed.set_author(name=f"{ctx.author.name} deletou todas as trilhas!")
            await ctx.send(embed=embed)

        except:
            embed = discord.Embed(description=f"(Tente esses comandos: /listatrilha /criartrilha)",color=0xdfca7f)
            embed.set_author(name=f"Oops.. Você não tem nenhuma trilha criada :/")
            await ctx.send(embed=embed, ephemeral=True)
    
    @commands.hybrid_command(name="vol", description="Muda o volume do DalinRPG!")
    async def voice_connect(self, ctx, *, volume: int):
        global lista_volume

        try:
            vc: player = ctx.voice_client

            if 0 <= volume <= 150:
                novovol = volume / 100
                lista_volume[f"{ctx.author.id}"] = novovol
                vc.source.volume = novovol

                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O volume foi alterado para: {volume}%")
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0xdfca7f)
                embed.set_author(name=f"O volume precisa estar entre 0/150!")
                await ctx.send(embed=embed, ephemeral=True)
        except:
            embed = discord.Embed(color=0xdfca7f)
            embed.set_author(name=f"Você precisa estar em um canal com uma trilha sonora tocando pra mudar o volume né! :/")
            await ctx.send(embed=embed, ephemeral=True)

lista_volume = {}            
queue = []

async def setup(bot):
    await bot.add_cog(musica(bot))