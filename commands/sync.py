import discord, config
from discord.ext import commands

class Sync(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot
  @commands.command(name="sync")
  @commands.has_role(config.owner_role_id)
  async def sync_prefix(self, ctx:commands.Context):
    server = discord.Object(id=config.guild_id)
    syncs = await self.bot.tree.sync(guild=server)
    await ctx.reply(f"{ctx.author.mention} sincronizou {len(syncs)} comandos de barra.", delete_after=5)
    print(f"{ctx.author.name} sincronizou {len(syncs)} comandos de barra.")

async def setup(bot:commands.Bot):
  await bot.add_cog(Sync(bot))