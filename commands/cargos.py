import discord, config
from discord.ext import commands

from discord import ui
class CargosView(ui.LayoutView):
  def __init__(self, icon):
    super().__init__(timeout=None)
    container = ui.Container(accent_color=config.commands_colors["main"])

    sessao = ui.Section(
      ui.TextDisplay(f"# 💼 CARGOS DO SERVIDOR"),
      accessory=ui.Thumbnail(media=icon)
    )
    container.add_item(sessao)
    container.add_item(ui.Separator(spacing=discord.SeparatorSpacing.large))

    container.add_item(ui.TextDisplay(f"""- - Use o <id:customize> para personalizar alguns cargos;
- - Candita-se para staff abrindo um <#1525645057435373748> e escolhendo a opção `Candidatar para staff`;
- - Escolha uma cor para seu nome abaixo:
"""))
    opcoes = [
      discord.SelectOption(label="Nenhum", value="nenhum", emoji="🚫", default=True),
      discord.SelectOption(label="Preto", value="preto", emoji="⚫"),
      discord.SelectOption(label="Vermelho", value="vermelho", emoji="🔴"),
      discord.SelectOption(label="Laranja", value="laranja", emoji="🟠"),
      discord.SelectOption(label="Amarelo", value="amarelo", emoji="🟡"),
      discord.SelectOption(label="Verde", value="verde", emoji="🟢"),
      discord.SelectOption(label="Azul", value="azul", emoji="🔵"),
      discord.SelectOption(label="Rosa", value="rosa", emoji="🌸"),
      discord.SelectOption(label="Índigo", value="indigo", emoji="♑"),
      discord.SelectOption(label="Roxo", value="roxo", emoji="🟣"),
      discord.SelectOption(label="Branco", value="branco", emoji="⚪"),
    ]
    menu = ui.Select(placeholder="Cores", min_values=1, max_values=1, options=opcoes, custom_id="menu_cargos")
    menu.callback = self.menu_callback
    
    row1 = ui.ActionRow(menu)
    container.add_item(row1)

    self.add_item(container)

  async def menu_callback(self, interaction=discord.Interaction):
    escolha = interaction.data["values"][0]
    autor = interaction.user
    role_remover = []
    for nome, id in config.roles.items():
      role = interaction.guild.get_role(id)
      if role in autor.roles:
        role_remover.append(role)
    await autor.remove_roles(*role_remover)
    if escolha != "nenhum":
      role = interaction.guild.get_role(config.roles[escolha])
      await autor.add_roles(role)
      
      await interaction.response.send_message(f"💼│Cargo <@&{config.roles[escolha]}> concedido com êxito!", ephemeral=True)
      return
    
    await interaction.response.send_message(f"🚫│Cargos removido com sucesso!", ephemeral=True)

class Cargos(commands.Cog):
  def __init__(self, bot:commands.Bot):
    self.bot = bot

  @commands.command(name="cargos")
  @commands.has_role(config.owner_role_id)
  async def cargos_prefix(self, ctx:commands.Context):
    await ctx.send(view=CargosView(ctx.guild.icon.url))

  @discord.app_commands.command(name="cargos", description="💼 Envia o menu de cargos disponíveis")
  @discord.app_commands.guilds(discord.Object(config.guild_id))
  @discord.app_commands.checks.has_role(config.owner_role_id)
  @discord.app_commands.default_permissions(administrator=True)
  async def cargos_slash(self, interaction:discord.Interaction):
    await interaction.response.send_message(view=CargosView(interaction.guild.icon.url))

async def setup(bot:commands.Bot):
  await bot.add_cog(Cargos(bot))