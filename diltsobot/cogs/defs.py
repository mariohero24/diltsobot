import discord, datetime, asyncio
import aiofiles
from discord.ext.prettyhelp import PrettyHelp
from traceback import format_exception

from randseal import Client
from discord.ext import commands
client = Client()

class Hooks:
	def __init__(self, client: discord.Client):
		channel: discord.TextChannel | None = asyncio.run(discord.utils.get_or_fetch(client, "channel", 1047613703702466622))
		self.debughook = asyncio.run(channel.fetch_message(1057416652226056203)).content
		self.loghook = asyncio.run(channel.fetch_message(1057417458232872991)).content
	

async def lockdownmodthing(bot: discord.Client, mod: discord.Member):
	"""Custom function that arrests a user"""
	staffrole = discord.Object(1015653001437909123)
	emojirole = discord.Object(1023379620348829696)
	trialmodrole = discord.Object(1020855698663411753)
	modrole = discord.Object(1000424453576073306)
	adrole = discord.Object(1016386365216272424)
	devrole = discord.Object(1047289657051840532)
	trialadminrole = discord.Object(1013266611970527253)
	adminrole = discord.Object(1008027971694633060, 1047327417338957945)
	roles = {staffrole, emojirole, trialmodrole, modrole,
			adrole, devrole, trialadminrole, adminrole}
	for role in roles:
		try:
			await mod.remove_roles(role, reason="Mod lockdown")
		except:
			pass
	else:
		duration = datetime.timedelta(days=1)
		await mod.timeout_for(duration, reason="Mod lockdown")
		hooks = Hooks(bot)
		webhook = discord.Webhook.from_url(hooks.loghook, session=client.session2)
		await webhook.send(username=bot.user.name, avatar_url=bot.user.avatar.url, embed=discord.Embed(colour=client.blank, title=f"{mod} arrested."))


class Bot(commands.Bot):
	"""Bot class cause yes"""
	def __init__(self):
		super().__init__(intents=discord.Intents.all(), command_prefix=commands.when_mentioned_or(
			"/"), help_command=PrettyHelp(color=client.blank, show_bot_perms=True, no_category="System"))
		with open('toggle.txt', 'w') as f:
			f.write("UwU")
		self.load_extensions(".cogs.lockdown", ".cogs.mass", ".cogs.core", ".cogs.managment", package="diltsobot")
		self.load_extension('jishaku')
		self.hooks = Hooks(self)

	async def on_command_error(self, ctx, error):
		pass

	async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
		if isinstance(error, commands.CommandOnCooldown):
			await ctx.respond(f"Command on cooldown, kinda sussy...", ephemeral=True)
			async with aiofiles.open('toggle.txt') as f:
				if (await f.read()) == "OwO":
					await lockdownmodthing(bot=self, mod=ctx.author)
		elif isinstance(error, commands.NotOwner):
			await ctx.respond("Only <@" + "> and <@".join(str(id) for id in self.owner_ids) + "> may use this command!", allowed_mentions=discord.AllowedMentions.none())
		elif isinstance(error, commands.MissingAnyRole):
			await ctx.respond(f"You require one of the following roles to use this command:\n<@&" + ">\n<@&".join(str(sus) for sus in error.missing_roles) + ">", allowed_mentions=discord.AllowedMentions.none())
		elif isinstance(error, discord.NotFound):
			await ctx.send(f"The bot was unable to respond in time")
		else:
			async with aiofiles.open('error.err', 'w') as f:
				await f.write(''.join(n for n in format_exception(error)))
				webhook = discord.Webhook.from_url(
					self.hooks.debughook, session=client.session2)
				await webhook.send(file=discord.File('error.err'), username=self.user.name, avatar_url=self.user.avatar.url)


class view(discord.ui.View):
	def __init__(self, **kwargs):
		super().__init__(timeout=256, **kwargs)
	@discord.ui.button(label="Stop", emoji="🛑")
	async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		await interaction.delete_original_response()