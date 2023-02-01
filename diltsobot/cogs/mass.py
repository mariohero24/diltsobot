from discord.ext import commands
from . import defs
import datetime, time, discord, logging

now = datetime.datetime.now()
description = ""
hexa = f"<t:{(time.mktime(now.timetuple()))}:R>".replace(".0", "")



class Mass(commands.Cog):
	def __init__(self, bot: defs.Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	mass = discord.SlashCommandGroup("mass", "Mass punishment commands")


	@mass.command(name="kick", description="Mass kicks members")
	@commands.has_any_role(defs.ids.mod_Role)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	@discord.option("ids", description="IDs to kick")
	@discord.option("reason", description="Reason for kicks")
	async def masskick(self, ctx: discord.ApplicationContext, ids: str, reason: str):
		for id in ids.split():
			idint = int(id)
			member = await ctx.guild.fetch_member(idint)
			await ctx.guild.kick(member, reason=reason)
		else:
			webhook = await self.bot.channels.modlogchannel()
			await ctx.respond(f"{len(ids.split())} members kicked.")
			embed = discord.Embed(colour=defs.BLANK, title="Members masskicked", description=f"{len(ids.split())} members kicked by <@{ctx.author.id}>.")
			await webhook.send(embed=embed)


	@mass.command(name="ban", description="Mass bans members")
	@commands.has_any_role(defs.ids.admin_Role)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	@discord.option("ids", description="IDs to kick")
	@discord.option("reason", description="Reason for kicks")
	async def massban(self, ctx: discord.ApplicationContext, ids: str, reason: str):
		for id in ids.split():
			idint = int(id)
			member = await ctx.guild.fetch_member(idint)
			await ctx.guild.ban(member, reason=reason)
		else:
			webhook = await self.bot.channels.modlogchannel()
			await ctx.respond(f"{len(ids.split())} members banned.")
			embed = discord.Embed(colour=defs.BLANK, title="Members massbanned", description=f"{len(ids.split())} members banned by <@{ctx.author.id}>.")
			await webhook.send(embed=embed)

	add = mass.create_subgroup("add")
	@add.command(description="Adds a role to several members")
	@commands.has_any_role(defs.ids.admin_Role)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	@discord.option("role", discord.Role, description="Role to add")
	@discord.option("ids", description="IDs to add the role to")
	async def role(self, ctx: discord.ApplicationContext, role: discord.Role, ids: str):
		for idstr in ids.split():
			idint = int(idstr)
			member = await ctx.guild.fetch_member(idint)
			await member.add_roles(role, reason=f"Requested by {ctx.author}")
		else:
			await ctx.respond("Done")

	
	@mass.command(description="Purges a channel or member")
	@commands.has_any_role(defs.ids.mod_Role)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def purge(self, ctx: discord.ApplicationContext, count: discord.Option(int, min_value=2, max_value=50, description="How many messages to purge")):
		await ctx.defer()
		await ctx.channel.purge(limit=count)
		await ctx.send_followup("Done")
		webhook = await self.bot.channels.modlogchannel()
		await webhook.send(embed=discord.Embed(colour=defs.BLANK, title=f"{count} messages purged by {ctx.author}."))



def setup(bot: commands.Bot):
	bot.add_cog(Mass(bot))