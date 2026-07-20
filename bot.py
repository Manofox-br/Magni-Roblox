import discord, os, config, datetime, ast, asyncio, itertools
from discord.ext import commands, tasks
from utils import CheckBump, SetupBump
from database import data

from discord import ui
class EntradasView(ui.LayoutView):
  def __init__(self, user:discord.Member):
    super().__init__(timeout=None)
    container = ui.Container(accent_color=config.commands_colors["main"])

    sessao = ui.Section(
      ui.TextDisplay(f"# 👋 Seja bem-vindo(a) {user.mention}"),
      accessory=ui.Thumbnail(media=user.display_avatar.url)
    )
    container.add_item(sessao)
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
    
    container.add_item(ui.TextDisplay(f"### Olá {user.name}, sinta-se em casa. Aqui você pode:"))
    container.add_item(ui.TextDisplay(f"""- 1. Conhecer novas pessoas;
- 2. Conversar sobre Roblox;
- 3. Jogar juntos em call;
- 4. Trocar ou comprar itens;
- 5. E muitas outras coisas! Aproveite.
"""))
    container.add_item(ui.TextDisplay(f"-# Não se esqueça de ler as <#1525635851676160170>"))
    container.add_item(ui.Separator())

    timestamp = int(datetime.datetime.now().timestamp())
    container.add_item(ui.TextDisplay(f"<t:{timestamp}:F>"))

    botao = ui.Button(
      url="https://discord.com/channels/1525614537930444851/1525635851676160170",
      label="REGRAS",
      style=discord.ButtonStyle.link,
      emoji="📌"
    )
    row1 = ui.ActionRow(botao)
    
    self.add_item(container)
    self.add_item(row1)

class InvitesView(ui.LayoutView):
  def __init__(self, autor_invites, invites, autor, member):
    super().__init__(timeout=None,)
    if member.bot:
      self.add_item(ui.TextDisplay(f"🤖 novo bot na parada! {member.mention}"))
      return

    guild = bot.get_guild(config.guild_id)
    if guild.get_member(autor.id):
      autor_mention = autor.mention if autor is not None else "**Usuário desconhecido**"
    else:
      autor_mention = "**O usuário não foi encontrado**"
    
    self.add_item(ui.TextDisplay(f"# 📊 • Status do convite"))
    self.add_item(ui.Separator())
    self.add_item(ui.TextDisplay(f"""🛎️ │ Pessoa que entrou: {member.mention}
📌 | Pessoa que convidou: {autor_mention}"""))
    if isinstance(autor_invites, int):
      self.add_item(ui.TextDisplay(f"✉️ | Pessoas convidadas: {autor_invites}"))
    else:
      self.add_item(ui.TextDisplay(f"✉️ | Pessoas convidadas: **indisponível**"))

    #garelia = ui.MediaGallery()
    #garelia.add_item(media=None)
    #self.add_item(galeria)

class SetupHook(commands.Bot):
  def __init__(self):
    super().__init__(
      command_prefix=config.prefix,
      intents=discord.Intents.all(),
      help_command=None
    )
    
  async def setup_hook(self):
    from commands.cargos import CargosView
    self.add_view(CargosView(None))
    
    await self.load_commands("commands")

  async def load_commands(self, folder):
    for file in os.listdir(folder):
      if file.endswith(".py"):
        try:
          await self.load_extension(f"commands.{file[:-3]}")
          print(f"📂 Comando {file[:-3]} carregado com sucesso!")
        except Exception as e:
          print(f"❌ Comando {file[:-3]} gerou um erro:\n{e}")
bot = SetupHook()
invites = {}

class MudarStatus:
  def  __init__(self):
    self.lista_atividades = [
      lambda:discord.CustomActivity(f"discord.gg/magni")
    ]
    self.atividades = itertools.cycle(self.lista_atividades)
    
    self.iniciar.start()
  
  @tasks.loop(seconds=12)
  async def iniciar(self):
    if not bot.is_closed():
      try:
        await bot.change_presence(status=discord.Status.idle, activity=next(self.activities)())
      except Exception as e:
        config.log.error(e)

async def entrar_chamada():
  guild = bot.get_guild(config.guild_id)
  voice_channel = guild.get_channel(1528120982575779920)

  await voice_channel.connect()

async def fetch_invites(member):
  channel = await bot.fetch_channel(1528030049561874472)
 
  guild = member.guild
  new_invites = await guild.invites()
  old_invites = invites[guild.id]

  for invite in old_invites:
    for new_invite in new_invites:
      if invite.code == new_invite.code and invite.uses < new_invite.uses:
        autor = invite.inviter
        user_history = ast.literal_eval(f"{data.getUserVar('user_history', autor.id)}")
        user_history = {} if user_history is None else user_history
          
        user_history[member.id] = True
        data.setUserVar("user_history", str(user_history), autor.id)

        autor_invites = data.getUserVar("invites", autor.id) if data.getUserVar("invites", autor.id) is not None else 1
        autor_invites = int(autor_invites)
        if member.id not in user_history:
          autor_invites += 1
        data.setUserVar("invites", str(autor_invites), autor.id)
        
        await channel.send(view=InvitesView(autor_invites, invite, autor, member))
        
    invites[guild.id] = new_invites

@bot.event
async def on_command_error(ctx:commands.Context, error):
  if isinstance(error, commands.MissingPermissions):
    print(f"{author.user} tentou usar o comando {command.name}.")
    return

@bot.event
async def on_member_join(member:discord.Member):
  channel = await bot.fetch_channel(1525636419572338829)
  await fetch_invites(member)
  await channel.send(view=EntradasView(member))

@bot.event
async def on_message(msg:discord.Message):
  CheckBump(bot, msg)
  if msg.author.bot:
    return
  msg.content = msg.content.lower()
  await bot.process_commands(msg)

@bot.event
async def on_ready():
  SetupBump(bot)
  for guild in bot.guilds:
    invites[guild.id] = await guild.invites()
  await entrar_chamada()
  print(f"Bot {bot.user} logado com êxito!")

bot.run(config.token)