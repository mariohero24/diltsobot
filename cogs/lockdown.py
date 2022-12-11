from discord.ext import commands
from stuff.defs import lockdownmodthing, client, rolecheck, debughook, loghook
import datetime, time, discord, asyncio, logging

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Lockdown(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	lockdown = discord.SlashCommandGroup("lockdown", "Lockdown commands")

	@lockdown.command(name="server", description="Locks down the server")
	@rolecheck(1000205572173471744, 1008027971694633060)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def lockdownserver(self, ctx: discord.ApplicationContext, toggle: discord.Option(choices=["Enable", "Disable"], description="Whether to lockdown or unlockdown the server")):
		async for member in ctx.guild.fetch_members():
			role = await client.fetchrole(context=ctx, id=1000424632882581505)
			if toggle == "Enable":
				if role in member.roles:
					await member.remove_roles(role, reason="Lockdown")
			else:
				if not role in member.roles:
					await member.add_roles(role, reason="Lockdown lifted")
		else:
			await ctx.respond("Done")
			webhook = discord.Webhook.from_url(loghook.url, session=client.session2)
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=discord.Embed(colour=client.blank, title=f"Server lockdown toggled by {ctx.author}"))


	@lockdown.command(name="staff", description="Locks down the staff team and shuts off the bot")
	@commands.is_owner()
	async def lockdownstaff(self, ctx: discord.ApplicationContext):
		await ctx.defer()
		mod = ctx
		staffrole = await client.fetchrole(context=mod, id=1015653001437909123)
		emojirole = await client.fetchrole(context=mod, id=1023379620348829696)
		trialmodrole = await client.fetchrole(context=mod, id=1020855698663411753)
		modrole = await client.fetchrole(context=mod, id=1000424453576073306)
		adrole = await client.fetchrole(context=mod, id=1016386365216272424)
		devrole = await client.fetchrole(context=mod, id=1047289657051840532)
		trialadminrole = await client.fetchrole(context=mod, id=1013266611970527253)
		adminrole = await client.fetchrole(context=mod, id=1008027971694633060)
		ignoredrole = await client.fetchrole(context=mod, id=1047384386762453083)
		roles = [staffrole, emojirole, trialmodrole, modrole,
				adrole, devrole, trialadminrole, adminrole]
		async for member in ctx.guild.fetch_members():
			if not ignoredrole in member.roles:
				for role in roles:
					try:
						await member.remove_roles(role, reason="Staff lockdown")
					except:
						pass
		else:
			await ctx.send_followup("Done")
			webhook = discord.Webhook.from_url(loghook.url, session=client.session2)
			await webhook.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url,  embed=discord.Embed(colour=client.blank, title=f"Staff lockdown toggled by {ctx.author}"))
			await asyncio.sleep(5)
			await self.bot.close()

	@lockdown.command(name="mod", description="Arrests a moderator")
	@rolecheck(1000205572173471744, 1008027971694633060)
	@commands.cooldown(rate=1, per=60, type=commands.cooldowns.BucketType.user)
	async def lockdownmod(self, ctx: discord.ApplicationContext, mod: discord.Option(discord.Member, description="Moderator to arrest")):
		await lockdownmodthing(bot=self.bot, mod=mod)
		await ctx.respond("Done")

def setup(bot):
	bot.add_cog(Lockdown(bot))