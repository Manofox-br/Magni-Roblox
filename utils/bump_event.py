import discord, asyncio, config, random, datetime
from database import data

from discord import ui
class BumpView(ui.LayoutView):
  def __init__(self):
    super().__init__(timeout=None)
    container = ui.Container(accent_color=config.commands_colors["main"])

    container.add_item(ui.TextDisplay(f"<@&1528041210449494166>"))
    sessao = ui.Section(
      ui.TextDisplay(f"# OLHA O BUMPEEEEEEEEE!!!!"),
      accessory=ui.Thumbnail(media="attachment://gif_alerta.gif")
    )
    container.add_item(sessao)
    
    self.add_item(container)

class BumpClaimView(ui.LayoutView):
  def __init__(self, autor, streak, xp, money = None):
    super().__init__(timeout=None)
    container = ui.Container(accent_color=config.commands_colors["main"])

    timestamp = int(datetime.datetime.now().timestamp()) + (120 * 60)
    thumb = autor.display_avatar.url if autor.avatar.url else "attachment://gif_alerta.gif"
    
    sessao = ui.Section(
      ui.TextDisplay(f"## {autor.mention} bumpou o servidor! <a:wumpus:1528542753158467704>"),
      accessory=ui.Thumbnail(media=thumb)
    )
    container.add_item(sessao)
    
    container.add_item(ui.TextDisplay(f"""> Você ganhou {xp}
 xp e {money} dinheiro por está ação! 😉
 ### 🔥 Streak atual: {streak}"""))
    container.add_item(ui.Separator())
    container.add_item(ui.TextDisplay(f"-# <t:{timestamp}:R>"))
    
    self.add_item(container)

async def setup_bump(bot:discord.ext.commands.Bot):
  ultimo_bump = data.getServerVar("ultimo_bump_timestamp", config.guild_id)
  ultimo_bump = ultimo_bump if ultimo_bump else datetime.datetime.now().timestamp()
  if ultimo_bump:
    ultimo_bump = datetime.datetime.fromtimestamp(int(ultimo_bump))
    agora = datetime.datetime.now()
    restante = (ultimo_bump + datetime.timedelta(hours=2)) - agora
    segundos = max(restante.total_seconds(), 0)
    await asyncio.sleep(segundos)
  data.setServerVar("ultimo_bump_timestamp", str(datetime.datetime.now().timestamp()), config.guild_id)

  arquivos = [
      discord.File("imagens/gif_alerta.gif", "gif_alerta.gif")
  ]
  
  channel = await bot.fetch_channel(1528033286998462577)
  await channel.send(view=BumpView(), files=arquivos)

class checkBump:
  def __init__(self, bot:discord.ext.commands.Bot, msg:discord.Message):
    self.bot = bot
    self.msg = msg
    self.channel = None
    asyncio.create_task(self.verificar())

  async def achar_canal(self):
    self.channel = await self.bot.fetch_channel(1528033286998462577)
    
  async def achar_autor(self):
    if self.msg.interaction_metadata and self.msg.interaction_metadata.user:
      user = self.msg.interaction_metadata.user
      member = self.msg.guild.get_member(user.id)
      if user is not None:
        member = self.msg.guild.get_member(user.id) if self.msg.guild else None
        return member or user

    if self.msg.mentions:
      return self.msg.mentions[0]

    return None
  
  async def verificar(self):
    await self.achar_canal()
    arquivos = [
      discord.File("imagens/gif_alerta.gif", "gif_alerta.gif")
    ]
    if self.msg.author == 302050872383242240:
      embed = self.msg.embeds[0]
      if "Bumb done" in embed.description:
        autor = await self.achar_autor()
        arquivos = [
        discord.File("imagens/gif_alerta.gif", "gif_alerta.gif")
      ]
      
      ultimo = data.getUserVar('ultimo_bumper', config.guild_id)
      ultimo = int(ultimo) if ultimo else None
    
      if ultimo != autor.id:
        data.setUserVar("streak_bumps", "0", autor.id)
        data.setServerVar("ultimo_bumper", str(autor.id), config.guild_id)
    
        streak = data.getUserVar("streak_bumps", autor.id)
        streak = int(streak) if streak else 0
        streak += 1
        data.setUserVar("streak_bumps", str(streak), autor.id)

        xp = data.getUserVar("xp", autor.id)
        xp = int(xp) if xp else 0
        xp += random.randint(50, 125)
        data.setUserVar("xp", str(xp), autor.id)
    
        await self.channel.send(view=BumpClaimView(autor, streak, xp), files=arquivos)
        
        ultimo_bump = data.getServerVar("ultimo_bump_timestamp", config.guild_id)
        ultimo_bump = ultimo_bump if ultimo_bump else datetime.datetime.now().timestamp()
        if ultimo_bump:
          ultimo_bump = datetime.datetime.fromtimestamp(int(ultimo_bump))
          agora = datetime.datetime.now()
          restante = (ultimo_bump + datetime.timedelta(hours=2)) - agora
          segundos = max(restante.total_seconds(), 0)
          await asyncio.sleep(segundos)
        data.setServerVar("ultimo_bump_timestamp", str(datetime.datetime.now().timestamp()))

        await self.channel.send(view=BumpView(), files=arquivos)