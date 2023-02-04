from discord.ext import commands
import discord, yaml

class gerenciador(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Estou pronto, logado como {self.bot.user}")
        try:
            synced = await self.bot.tree.sync()
            print(f"Consegui syncar {len(synced)} commandos!")

        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("bancodedados/prefixos.yaml", "r") as pasta:
            prefixo = yaml.safe_load(pasta)
            
        prefixo[str(guild.id)] = "!"

        with open("bancodedados/prefixos.yaml", "w") as pasta:
            yaml.dump(prefixo, pasta)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("bancodedados/prefixos.yaml", "r") as pasta:
            prefixo = yaml.safe_load(pasta)

        del prefixo[str(guild.id)]

        with open("bancodedados/prefixos.yaml", "w") as pasta:
            yaml.dump(prefixo, pasta)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.mentions[0] == self.bot.user:
            with open("bancodedados/prefixos.yaml", "r") as pasta:
                prefixos = yaml.safe_load(pasta)

            pre = prefixos[str(message.guild.id)]
            
            embed = discord.Embed(title= f'Meu prefixo para este server é "{pre}"!!', color=0xdfca7f)
            await message.channel.send(embed=embed)
            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        voice_state = member.guild.voice_client
        if voice_state is not None and len(voice_state.channel.members) == 1:
            voice_state.stop()
            await voice_state.disconnect()

async def setup(bot):
    await bot.add_cog(gerenciador(bot))