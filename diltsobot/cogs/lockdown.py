from discord.ext import commands
from .defs import lockdownmodthing, client, Bot, BLANK, needs_any_role, ids
import datetime, time, discord, asyncio, logging

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Lockdown(commands.Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	lockdown = discord.SlashCommandGroup("lockdown", "Lockdown commands")

	@lockdown.command(name="server", description="Locks down the server")
	@needs_any_role()
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	@discord.option("toggle", choices=["Enable", "Disable"], description="Whether to lockdown or unlockdown the server")
	async def lockdownserver(self, ctx: discord.ApplicationContext, toggle: str):
		await ctx.response.defer()
		async for member in ctx.guild.fetch_members():
			role = ctx.guild.get_role(self.bot.ids.member_Role)
			if toggle == "Enable":
				if role in member.roles:
					await member.remove_roles(role, reason="Lockdown")
			else:
				if not role in member.roles:
					await member.add_roles(role, reason="Lockdown lifted")
		else:
			await ctx.respond("Done")
			webhook = await self.bot.channels.modlogchannel()
			await webhook.send(embed=discord.Embed(colour=BLANK, title=f"Server lockdown toggled by {ctx.user}"))


	@lockdown.command(name="staff", description="Locks down the staff team and shuts off the bot")
	@needs_any_role()
	async def lockdownstaff(self, ctx: discord.ApplicationContext):
		await ctx.defer()
		staffrole = discord.Object(ids.staff_Role)
		trialmodrole = discord.Object(ids.trial_Role)
		modrole = discord.Object(ids.mod_Role)
		devrole = discord.Object(ids.botdev_Role)
		adminrole = discord.Object(ids.admin_Role)
		ignoredrole = ctx.guild.get_role(ids.immune_Role)
		roles = {staffrole, trialmodrole, modrole, devrole, adminrole}
		for member in ctx.guild.members:
			if not ignoredrole in member.roles:
				for role in roles:
					try:
						await member.remove_roles(role, reason="Staff lockdown")
					except:
						pass
		else:
			await ctx.followup.send("Done")
			webhook = await self.bot.channels.modlogchannel()
			await webhook.send(embed=discord.Embed(colour=BLANK, title=f"Staff lockdown toggled by {ctx.author}"))
			await asyncio.sleep(5)
			await self.bot.close()

	@lockdown.command(name="mod", description="Arrests a moderator")
	@commands.has_any_role()
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def lockdownmod(self, ctx: discord.ApplicationContext, mod: discord.Option(discord.Member, description="Moderator to arrest")):
		await lockdownmodthing(bot=self.bot, mod=mod)
		await ctx.respond("Done")

def setup(bot: commands.Bot):
	bot.add_cog(Lockdown(bot))