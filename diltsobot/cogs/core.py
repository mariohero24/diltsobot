from discord.ext import commands, pages
import datetime, time, discord, asyncio, logging
import aiofiles, os
from importlib import resources
from . import defs

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Core(commands.Cog):
	def __init__(self, bot: defs.Bot):
		self.bot = bot
		logging.info(f"{__name__} cog loaded")

	def cog_unload(self):
		logging.info(f"{__name__} cog unloaded")

	@commands.Cog.listener('on_ready')
	async def ready(self):
		print("Online")
		q = await self.bot.channels.botlogchannel()
		await self.bot.change_presence(activity=discord.Game(name="with frogs"))
		logging.info(f"Logged in")
		mess = await defs.get_or_fetch_message(q, self.bot.ids.outputlog_Message)
		await mess.edit(content="", attachments=[], file=discord.File(fp='output.log', filename="log.py"))
		await q.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url, content="Online")
	
	admin = discord.SlashCommandGroup("admin", "Admin commands")
	owner = discord.SlashCommandGroup("bot", "Advanced bot commands")

	@admin.command(description="Makes the bot say something")
	@defs.needs_any_role(defs.ids.admin_Role)
	@discord.option("message", description="Message to send", default = "")
	@discord.option("media", discord.Attachment, default = None, description = "Media to send with message")
	@discord.option("channel", discord.TextChannel, description="Channel to send the message to", default = None)
	@discord.option("delete_after", float, description="How long (in seconds) you want the message to delete after", default=...)
	async def say(self,
					ctx: discord.ApplicationContext,
					message: str,
					media: discord.Attachment,
					channel: discord.TextChannel,
					delete_after: float
					):
		await ctx.response.defer(ephemeral=True)
		if channel == None:
			if media != None:
				file = await media.to_file()
				await ctx.send(message, allowed_mentions=discord.AllowedMentions.none(), file=file, delete_after=delete_after)
			else:
				await ctx.send(message, allowed_mentions=discord.AllowedMentions.none(), delete_after=delete_after)
			await ctx.followup.send(f"Command executed.")
		else:
			if media != None:
				file = await media.to_file()
				await channel.send(message, allowed_mentions=discord.AllowedMentions.none(), file=file, delete_after=delete_after)
			else:
				await channel.send(message, allowed_mentions=discord.AllowedMentions.none(), delete_after=delete_after)
			await ctx.followup.send("Sent whatever you wanted me to...")


	flag = discord.SlashCommandGroup("flag", "Flagging commands")
	@flag.command(description="Sets whether you want moderators to be arrested for doing more than 1 mod action per minute")
	@defs.needs_any_role()
	@discord.option("toggle", description="Figure it out yourself", choices=[discord.OptionChoice("Enable", "OwO"), discord.OptionChoice("Disable", "UwU")])
	async def toggle(self, ctx: discord.ApplicationContext, toggle: str):
		async with aiofiles.open('toggle.txt', 'w') as f:
			await f.write(toggle)
		await ctx.respond("Done")


	@owner.command(description="Shows basic bot information")
	@defs.needs_any_role()
	async def debug(self, ctx: discord.ApplicationContext):
		await ctx.respond(f"Bot last restarted {hexa}.\nOwners:\n<@" + ">\n<@".join(str(owner) for owner in self.bot.owner_ids) + f">\n{len(self.bot.cogs)}/4 cogs loaded.", file=await defs.client.File(discord.File), allowed_mentions=discord.AllowedMentions.none())


	@owner.command(description="Puts something in output.log")
	@defs.needs_any_role()
	@discord.option("message", description="Log message to put in output.log")
	async def log(self, ctx: discord.ApplicationContext, message: str):
		await ctx.response.defer(ephemeral=True)
		logging.info(message)
		await asyncio.sleep(1)
		await ctx.respond(file=discord.File('output.log', filename="log.py"))

	@owner.command(description="Manages the bot's systems")
	@defs.needs_any_role()
	@discord.option("action", int, description="What to do", choices=[discord.OptionChoice("Shutdown", 1), discord.OptionChoice("Clear cache", 2)])
	async def manage(self, ctx: discord.ApplicationContext, action: int):
		await ctx.response.defer()
		q = await self.bot.channels.botlogchannel()
		mess = await defs.get_or_fetch_message(q, self.bot.ids.outputlog_Message)
		await mess.edit(content=None, attachments=[], file=discord.File(fp='output.log', filename="log.py"), )
		if action == 1:
			await q.send(content=f"Shut down by {ctx.author}")
			await ctx.followup.send("Shutting down...")
			logging.info("Shutting down...")
			await asyncio.sleep(7)
			await self.bot.close()
		elif action == 2:
			await q.send(content=f"Cache cleared by {ctx.user}")
			await ctx.followup.send("Clearing...")
			logging.info("Clearing cache...")
			await self.bot.clear()
		else:
			await ctx.followup.send("how")

	@owner.command(description="Shows info of every member")
	@defs.needs_any_role(defs.ids.trial_Role)
	async def servers(self, ctx: discord.ApplicationContext):
		e = []
		async for user in ctx.guild.fetch_members():
			date_format = "%a, %d %b %Y %I:%M %p"
			embed = discord.Embed(colour=user.colour if user.colour != discord.Colour.default() else defs.BLANK, description=user.mention)
			embed.set_author(name=user.__str__(), icon_url=user.display_avatar.url)
			embed.set_thumbnail(url=user.display_avatar.url)
			embed.add_field(
				name="Joined", value=f"{user.joined_at.strftime(date_format)} (<t:{(time.mktime(user.joined_at.timetuple()))}:R>)".replace(".0", ""))
			members: list[discord.Member] = sorted(ctx.guild.members, key=lambda m: m.joined_at)
			embed.add_field(name="Join position",
							value=str(members.index(user) + 1))
			embed.add_field(name="Registered",
							value=f"{user.created_at.strftime(date_format)} (<t:{(time.mktime(user.created_at.timetuple()))}:R>)".replace(".0", ""))
			if len(user.roles) > 1:
				role_string = " ".join([r.mention for r in user.roles][1:])
				embed.add_field(
					name=f"Roles [{len(user.roles) - 1}]",
					value=role_string,
					inline=False,
				)
			perm_string = ", ".join(
				[
					str(p[0]).replace("_", " ").title()
					for p in user.guild_permissions
					if p[1]
				]
			)
			embed.add_field(name="Guild permissions",
							value=perm_string, inline=False)
			embed.set_footer(text="ID: " + str(user.id))
			e.append(embed)
		else:
			pag = pages.Paginator(e, loop_pages=True, custom_view=defs.view())
			await pag.respond(ctx.interaction, ephemeral=True)


def setup(bot: commands.Bot):
	bot.add_cog(Core(bot))