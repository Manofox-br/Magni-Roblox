import discord, config, datetime
from discord.ext import commands

from discord import ui
class RegrasView(ui.LayoutView):
  def __init__(self, guild, author):
    super().__init__(timeout=None)
    timestamp = int(datetime.datetime.now().timestamp())
    
    container = ui.Container(accent_color=config.commands_colors["main"])
    sessao = ui.Section(
      ui.TextDisplay(f"# 📕 REGRAS DO SERVIDOR"),
      accessory=ui.Thumbnail(media=guild.icon.url)
    )
    container.add_item(sessao)
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
    galeria = ui.MediaGallery()
    galeria.add_item(media="attachment://banner_regras.png")
    container.add_item(galeria)
    container.add_item(ui.TextDisplay(f"""-# staff responsável: {author.mention}
-# última edição: <t:{timestamp}:F>
"""))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
    self.add_item(container)
    
    container2 = ui.Container(accent_color=config.commands_colors["main"])
    container2.add_item(ui.TextDisplay(f"# 📕 0. DISCORD:"))
    container2.add_item(ui.Separator())
    container2.add_item(ui.TextDisplay(f"""- 1. __**Termos de Serviço:**__ Respeite as [regras e diretrizes](https://discord.com/guidelines) do discord;
- 2. __**Idade mínima:**__ Ao permanecer, você concordar ter pelo menos 13 anos.
"""))
    container2.add_item(ui.Separator())
    botao = ui.Button(
      url="https://www.discord.com/guidelines",
      label="Regras e diretrizes do Discord",
      style=discord.ButtonStyle.link,
      emoji="🪩"
    )
    row1 = ui.ActionRow(botao)
    self.add_item(container2)
    self.add_item(row1)

    container3 = ui.Container(accent_color=config.commands_colors["main"])
    container3.add_item(ui.TextDisplay(f"# 📕 1. RESPEITO E CONVIVÊNCIA:"))
    container3.add_item(ui.Separator())
    container3.add_item(ui.TextDisplay(f"""- 1. __**Contas e Avatares:**__ Fotos de perfil, nicks ou status que contenham conteúdo ofensivo, violento ou inadequado não serão tolerados. Alts para evitar punições serão banidas também;
- 2. __**Sem Ofensas:**__ É proibido qualquer tipo de insulto, discurso de ódio, preconceito ou assédio contra membros ou membros da equipe;
- 3. __**Discussões e Conflitos:**__ Evite brigas, provocações e dramas desnecessários nos chats públicos. Caso tenha problemas com alguém, resolva no privado ou crie um <#1525645057435373748>.
"""))
    container3.add_item(ui.Separator())
    self.add_item(container3)

    container4 = ui.Container(accent_color=config.commands_colors["main"])
    container4.add_item(ui.TextDisplay(f"# 📕 2. ORGANIZAÇÃO DOS CHATS:"))
    container4.add_item(ui.Separator())
    container4.add_item(ui.TextDisplay(f"""- 1. __**Uso dos Canais:**__ Utilize cada canal para a sua respectiva finalidade (ex: comandos de bots apenas no chat de bots, trocas apenas no chat de trocas);
- 2. __**Poluição Visual (Spam/Flood):**__ Não envie a mesma mensagem repetidamente, não abuse de letras maiúsculas (CAPS LOCK) e evite marcar as pessoas de forma desnecessária.
"""))
    container4.add_item(ui.Separator())
    self.add_item(container4)

    container5 = ui.Container(accent_color=config.commands_colors["main"])
    container5.add_item(ui.TextDisplay(f"# 📕 3. DIVULGAÇÃO E COMÉRCIO:"))
    container5.add_item(ui.Separator())
    container5.add_item(ui.TextDisplay(f"""- 1. __**Divulgação Não Autorizada:**__ É proibido enviar links de outros servidores do Discord, canais do YouTube ou convites sem a autorização prévia da administração;
- 2. __**Comércio Paralelo:**__ Não é permitido realizar vendas, trocas de contas ou transações financeiras fora dos canais oficiais da loja do servidor.
"""))
    container5.add_item(ui.Separator())
    self.add_item(container5)

class ImpulsosView(ui.LayoutView):
  def __init__(self, guild, author):
    super().__init__(timeout=None)
    timestamp = int(datetime.datetime.now().timestamp())
    
    container = ui.Container(accent_color=config.commands_colors["main"])
    sessao = ui.Section(
      ui.TextDisplay(f"# 🚀 IMPULSOS DO SERVIDOR"),
      accessory=ui.Thumbnail(media=guild.icon.url)
    )
    container.add_item(sessao)
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
    galeria = ui.MediaGallery()
    galeria.add_item(media="attachment://banner_impulsos.png")
    container.add_item(galeria)
    container.add_item(ui.TextDisplay(f"""-# staff responsável: {author.mention}
-# última edição: <t:{timestamp}:F>
"""))
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))
    self.add_item(container)
    
    container2 = ui.Container(accent_color=config.commands_colors["main"])
    container2.add_item(ui.TextDisplay(f"# 🚀 BÔNUS DE IMPULSOS:"))
    container2.add_item(ui.Separator())
    container2.add_item(ui.TextDisplay(f"""### __**<@&1525665166119796896>** Impulsione o servidor **uma** vez e ganhe:__
- 2x de xp;
- Cargo personalizado;
- Chat vip.
### __**<@&1525665441911931041>** Impulsione o servidor **duas** vez e ganhe:__
- Bônus do primeiro impulso;
- Cargo personalizado;
- Desconto de 10% em compras no servidor.
"""))
    container2.add_item(ui.Separator())
    self.add_item(container2)
  
class Regras(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

  @commands.command(name="regras")
  @commands.has_role(config.owner_role_id)
  async def regras_prefix(self, ctx:commands.Context):
    banners = [
      discord.File("imagens/banner_regras.png", "banner_regras.png"),
    ]
    await ctx.send(view=RegrasView(ctx.guild, ctx.author), files=banners)

  @discord.app_commands.command(name="regras", description="📌 Envia as regras do servidor")
  @discord.app_commands.guilds(discord.Object(id=config.guild_id))
  @discord.app_commands.checks.has_role(config.owner_role_id)
  @discord.app_commands.default_permissions(administrator=True)
  async def regras_slash(self, interaction:discord.Interaction):
    banners = [
      discord.File("imagens/banner_regras.png", "banner_regras.png"),
    ]
    await interaction.response.send_message(view=RegrasView(interaction.guild, interaction.user), files=banners)

  @commands.command(name="impulsos")
  @commands.has_role(config.owner_role_id)
  async def impulsos_prefix(self, ctx:commands.Context):
    banners = [
      discord.File("imagens/banner_impulsos.png", "banner_impulsos.png")
    ]
    await ctx.send(view=ImpulsosView(ctx.guild, ctx.author), files=banners)

  @discord.app_commands.command(name="impulsos", description="🚀 Envia as informações sobre os impulsos no servidor")
  @discord.app_commands.guilds(discord.Object(id=config.guild_id))
  @discord.app_commands.checks.has_role(config.owner_role_id)
  @discord.app_commands.default_permissions(administrator=True)
  async def impulsos_slash(self, interaction:discord.Interaction):
    banners = [
      discord.File("imagens/banner_impulsos.png", "banner_impulsos.png")
    ]
    await interaction.response.send_message(view=ImpulsosView(interaction.guild, interaction.user), files=banners)

async def setup(bot:commands.Bot):
  await bot.add_cog(Regras(bot))