import aiofiles
from discord.ext.prettyhelp import PrettyHelp
from discord.ext import commands
from .cogs.defs import lockdownmodthing, client, debughook
import discord
from traceback import format_exception
from importlib import resources

class Bot(commands.Bot):
	"""Bot class cause yes"""
	def __init__(self):
		super().__init__(intents=discord.Intents.all(), command_prefix=commands.when_mentioned_or(
			"/"), help_command=PrettyHelp(color=client.blank, show_bot_perms=True, no_category="System"))
		with open('toggle.txt', 'w') as f:
			f.write("UwU")
		self.load_extensions(".cogs.lockdown", ".cogs.mass", ".cogs.core", package="diltsobot")
		self.load_extension('jishaku')

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
					debughook.url, session=client.session2)
				await webhook.send(file=discord.File('error.err'), username=self.user.name, avatar_url=self.user.avatar.url)