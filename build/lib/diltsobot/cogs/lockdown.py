from discord.ext import commands
from .defs import lockdownmodthing, client, Hooks, Bot
import datetime, time, discord, asyncio, logging

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Lockdown(commands.Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")
		self.hooks = bot.hooks

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	lockdown = discord.SlashCommandGroup("lockdown", "Lockdown commands")

	@lockdown.command(name="server", description="Locks down the server")
	@commands.has_any_role(1000205572173471744, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def lockdownserver(self, ctx: discord.ApplicationContext, toggle: discord.Option(choices=["Enable", "Disable"], description="Whether to lockdown or unlockdown the server")):
		async for member in ctx.guild.fetch_members():
			role = discord.Object(1000424632882581505)
			if toggle == "Enable":
				if role in member.roles:
					await member.remove_roles(role, reason="Lockdown")
			else:
				if not role in member.roles:
					await member.add_roles(role, reason="Lockdown lifted")
		else:
			await ctx.respond("Done")
			webhook = discord.Webhook.from_url(self.hooks.loghook, session=client.session2)
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=discord.Embed(colour=client.blank, title=f"Server lockdown toggled by {ctx.author}"))


	@lockdown.command(name="staff", description="Locks down the staff team and shuts off the bot")
	@commands.is_owner()
	async def lockdownstaff(self, ctx: discord.ApplicationContext):
		await ctx.defer()
		mod = ctx
		staffrole = discord.Object(1015653001437909123)
		emojirole = discord.Object(1023379620348829696)
		trialmodrole = discord.Object(1020855698663411753)
		modrole = discord.Object(1000424453576073306)
		adrole = discord.Object(1016386365216272424)
		devrole = discord.Object(1047289657051840532)
		trialadminrole = discord.Object(1013266611970527253)
		adminrole = discord.Object(1008027971694633060, 1047327417338957945)
		ignoredrole = discord.Object(1047384386762453083)
		roles = {staffrole, emojirole, trialmodrole, modrole,
				adrole, devrole, trialadminrole, adminrole}
		async for member in ctx.guild.fetch_members(limit=ctx.guild.max_members):
			if not ignoredrole in member.roles:
				for role in roles:
					try:
						await member.remove_roles(role, reason="Staff lockdown")
					except:
						pass
		else:
			await ctx.send_followup("Done")
			webhook = discord.Webhook.from_url(self.hooks.loghook, session=client.session2)
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=discord.Embed(colour=client.blank, title=f"Staff lockdown toggled by {ctx.author}"))
			await asyncio.sleep(5)
			await self.bot.close()

	@lockdown.command(name="mod", description="Arrests a moderator")
	@commands.has_any_role(1000205572173471744, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def lockdownmod(self, ctx: discord.ApplicationContext, mod: discord.Option(discord.Member, description="Moderator to arrest")):
		await lockdownmodthing(bot=self.bot, mod=mod)
		await ctx.respond("Done")

def setup(bot: commands.Bot):
	bot.add_cog(Lockdown(bot))