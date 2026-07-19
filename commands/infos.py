import discord, config
from discord.ext import commands
from database import data

class Infos(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

  @commands.command(name="invites")
  async def invites_prefix(self, ctx: commands.Context, member:discord.Member):
    invites = data.getUserVar("invites", member.id)
    invites = invites if invites is not None else 0

    await ctx.reply(f"O usuário {member.mention} tem {invites} pessoas convidadas.")

  @discord.app_commands.command(name="invites", description="📬 Mostra quantas pessoas um usuário convidou")
  @discord.app_commands.describe(member="Usuário que será mostrados os convites")
  async def invites_slash(self, interaction:discord.Interaction, member:discord.Member):
    invites = data.getUserVar("invites", member.id)
    invites = invites if invites is not None else 0

    await interaction.response.send_message(f"O usuário {member.mention} tem {invites} pessoas convidadas.")

async def setup(bot:commands.Bot):
  await bot.add_cog(Infos(bot))