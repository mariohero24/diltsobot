from discord.ext import commands
from .defs import lockdownmodthing, client, Hooks, Bot
import datetime, time, discord, asyncio, logging, os

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Managment(commands.Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	@discord.slash_command(description="Reloads all the cogs")
	@needs_any_role()
	async def reload_cogs(self, ctx: discord.ApplicationContext):
		for cog in {".cogs.mass", ".cogs.core", ".cogs.lockdown"}:
			self.bot.reload_extension(cog, package='diltsobot')
		else:
			await ctx.respond("Done")