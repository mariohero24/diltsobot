from discord.ext import commands
from .defs import client, Hooks, Bot
import datetime, time, discord, logging

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

now = datetime.datetime.now()
description = ""
hexa = f"<t:{(time.mktime(now.timetuple()))}:R>".replace(".0", "")



class Mass(commands.Cog):
	def __init__(self, bot: Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")
		self.hooks = bot.hooks

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	mass = discord.SlashCommandGroup("mass", "Mass punishment commands")


	@mass.command(name="kick", description="Mass kicks members")
	@commands.has_any_role(1000205572173471744, 1000424453576073306, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def masskick(self, ctx: discord.ApplicationContext, ids: discord.Option(description="IDs to kick"), reason: discord.Option(description="Reason for kicks") = "None"):
		for id in ids.split():
			idint = int(id)
			member = await ctx.guild.fetch_member(idint)
			await ctx.guild.kick(member, reason=reason)
		else:
			webhook = discord.Webhook.from_url(self.hooks.loghook, session=client.session2)
			await ctx.respond(f"{len(ids.split())} members kicked.")
			embed = discord.Embed(colour=client.blank, title="Members masskicked", description=f"{len(ids.split())} members kicked by <@{ctx.author.id}>.")
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=embed)


	@mass.command(name="ban", description="Mass bans members")
	@commands.has_any_role(1000205572173471744, 1000424453576073306, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def massban(self, ctx: discord.ApplicationContext, ids: discord.Option(description="IDs to ban"), reason: discord.Option(description="Reason for bans") = "None"):
		for id in ids.split():
			idint = int(id)
			member = await ctx.guild.fetch_member(idint)
			await ctx.guild.ban(member, reason=reason)
		else:
			webhook = discord.Webhook.from_url(self.hooks.loghook, session=client.session2)
			await ctx.respond(f"{len(ids.split())} members banned.")
			embed = discord.Embed(colour=client.blank, title="Members massbanned", description=f"{len(ids.split())} members banned by <@{ctx.author.id}>.")
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=embed)

	add = mass.create_subgroup("add")
	@add.command(description="Adds a role to several members")
	@commands.has_any_role(1000205572173471744, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def role(self, ctx: discord.ApplicationContext, role: discord.Option(discord.Role, description="Role to add"), ids: discord.Option(description="IDs to add the role to")):
		for idstr in ids.split():
			idint = int(idstr)
			member = await ctx.guild.fetch_member(idint)
			await member.add_roles(role, reason=f"Requested by {ctx.author}")
		else:
			await ctx.respond("Done")

	
	@mass.command(description="Purges a channel or member")
	@commands.has_any_role(1000205572173471744, 1000424453576073306, 1008027971694633060, 1047327417338957945)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def purge(self, ctx: discord.ApplicationContext, count: discord.Option(int, min_value=2, max_value=50, description="How many messages to purge")):
		await ctx.defer()
		await ctx.channel.purge(limit=count)
		await ctx.send_followup("Done")
		webhook = discord.Webhook.from_url(self.hooks.loghook, session=client.session2)
		await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=discord.Embed(colour=client.blank, title=f"{count} messages purged by {ctx.author}."))



def setup(bot: commands.Bot):
	bot.add_cog(Mass(bot))