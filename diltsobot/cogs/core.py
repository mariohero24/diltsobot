from discord.ext import commands
from .defs import client, rolecheck, debughook
import datetime, time, discord, asyncio, logging
import aiofiles

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

description = ""
hexa = f"<t:{(time.mktime(datetime.datetime.now().timetuple()))}:R>".replace(".0", "")


class Core(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener('on_ready')
	async def ready(self):
		print("Online")
		q = discord.Webhook.from_url(debughook.url, session=client.session2)
		await self.bot.change_presence(activity=discord.Game(name="with frogs"))
		logging.info(f"Logged in!")
		async with aiofiles.open("output.log") as f:
			await q.edit_message(message_id=1047667970555519036, content="", attachments=[], file=discord.File(fp=f.name, filename="log.py"))
			await q.send(username=self.bot.user.name, avatar_url=self.bot.user.avatar.url, content="Online")
	
	admin = discord.SlashCommandGroup("admin", "Admin commands")
	owner = discord.SlashCommandGroup("bot", "Advanced bot commands")
	@admin.command(description="Makes the bot say something")
	@rolecheck(1000205572173471744, 1008027971694633060)
	async def say(self,
					ctx: discord.ApplicationContext,
					message: discord.Option(description="Message to send") = "",
					media: discord.Option(discord.Attachment) = None,
					channel: discord.Option(discord.TextChannel, description="Channel to send the message to"
											) = None,
					delete_after: discord.Option(float, description="How long (in seconds) you want the message to delete after")=100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000.0
					):
		if channel == None:
			if media != None:
				file = await media.to_file()
				await ctx.send(message, allowed_mentions=discord.AllowedMentions.none(), file=file, delete_after=delete_after)
			else:
				await ctx.send(message, allowed_mentions=discord.AllowedMentions.none(), delete_after=delete_after)
			await ctx.respond(f"Command executed.", ephemeral=True)
		else:
			if media != None:
				file = await media.to_file()
				await channel.send(message, allowed_mentions=discord.AllowedMentions.none(), file=file, delete_after=delete_after)
			else:
				await channel.send(message, allowed_mentions=discord.AllowedMentions.none(), delete_after=delete_after)
			await ctx.respond("Sent whatever you wanted me to...")


	flag = discord.SlashCommandGroup("flag")
	@flag.command(description="Sets whether you want moderators to be arrested for doing more than 1 mod action per minute")
	@commands.is_owner()
	async def toggle(self, ctx: discord.ApplicationContext, uwu: discord.Option(name="toggle", description="Figure it out yourself", choices=[discord.OptionChoice("Enable", "OwO"), discord.OptionChoice("Disable", "UwU")])):
		self.toggle = uwu
		await ctx.respond("Done")


	@owner.command(description="Shows basic bot information")
	@commands.is_owner()
	async def debug(self, ctx: discord.ApplicationContext):
		await ctx.respond(f"Bot last restarted {hexa}.\nOwners:\n<@" + ">\n<@".join(str(owner) for owner in self.bot.owner_ids) + f">\n{len(self.bot.cogs)}/3 cogs loaded.", file=await client.asyncFile(), allowed_mentions=discord.AllowedMentions.none())


	@owner.command(description="Puts something in output.log")
	@commands.is_owner()
	async def log(self, ctx: discord.ApplicationContext, message: discord.Option(description="Log message to put in output.log")):
		logging.info(message)
		await asyncio.sleep(1)
		async with aiofiles.open("output.log") as f:
			await ctx.respond(file=discord.File(f.name, filename="log.py"), ephemeral=True)

def setup(bot: commands.Bot):
	bot.add_cog(Core(bot))