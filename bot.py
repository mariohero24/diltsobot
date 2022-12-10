import aiofiles
from discord.ext.prettyhelp import PrettyHelp
from discord.ext import commands
from stuff.defs import lockdownmodthing, data, client, rolecheck
import datetime, time, discord, asyncio, logging, os


debughook = data.debughook
loghook = data.loghook

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)
with open("output.log") as f:
	if len(f.read().splitlines()) > 7:
		logging.info(f"Shutting down...")
logging.info(f"Starting up...")

now = datetime.datetime.now()
description = ""
hexa = f"<t:{(time.mktime(now.timetuple()))}:R>".replace(".0", "")

bot = commands.Bot(intents=discord.Intents.all(), owner_ids={935659484695646238, 511012867407872000, 655303532273991691}, command_prefix=commands.when_mentioned_or("/"), help_command=PrettyHelp(color=client.blank, show_bot_perms=True, no_category="System"))

extensions = ["cogs.lockdown", "cogs.mass"]
for extension in extensions:
	bot.load_extension(extension)
bot.load_extension('jishaku')
owner = bot.create_group("bot", "Advanced bot commands")


@bot.listen('on_ready')
async def ready():
	print("Online")
	q = discord.Webhook.from_url(debughook, session=client.session2)
	await bot.change_presence(activity=discord.Game(name="with frogs"))
	logging.info(f"Logged in!")
	async with aiofiles.open("output.log") as f:
		await q.edit_message(message_id=1047667970555519036, content="", attachments=[], file=discord.File(fp=f.name, filename="log.py"))
		await q.send(username=bot.user.name, avatar_url=bot.user.avatar.url, content="Online")

admin = bot.create_group("admin", "Admin commands")
@admin.command(description="Makes the bot say something")
@rolecheck(1000205572173471744, 1008027971694633060)
async def say(
				ctx: discord.ApplicationContext,
				message: discord.Option(description="Message to send") = "** **",
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


flag = bot.create_group("flag")
@flag.command(description="Sets whether you want moderators to be arrested for doing more than 1 mod action per minute")
@commands.is_owner()
async def toggle(ctx: discord.ApplicationContext, uwu: discord.Option(name="toggle", description="Figure it out yourself", choices=["Enable", "Disable"])):
	if uwu == "Enable":
		tooooo = "OwO"
	else:
		tooooo = "UwU"
	async with aiofiles.open("toggle.txt", "w") as f:
		await f.write(tooooo)
		await ctx.respond("Done")


@owner.command(description="Shows basic bot information")
@commands.is_owner()
async def debug(ctx: discord.ApplicationContext):
	await ctx.respond(f"Bot last restarted {hexa}.\nOwners:\n<@" + ">\n<@".join(str(owner) for owner in bot.owner_ids) + f">\n{len(bot.cogs)}/3 cogs loaded.", file=await client.asyncFile(), allowed_mentions=discord.AllowedMentions.none())


@owner.command(description="Puts something in output.log")
@commands.is_owner()
async def log(ctx: discord.ApplicationContext, message: discord.Option(description="Log message to put in output.log")):
	logging.info(message)
	await asyncio.sleep(1)
	async with aiofiles.open("output.log") as f:
		await ctx.respond(file=discord.File(f.name, filename="log.py"), ephemeral=True)


@bot.listen('on_application_command_error')
async def errors(ctx: discord.ApplicationContext, error):
	if isinstance(error, commands.CommandOnCooldown):
		await ctx.respond(f"Command on cooldown, kinda sussy...", ephemeral=True)
		async with aiofiles.open("toggle.txt") as f:
			if (await f.read()) == "OwO":
				await lockdownmodthing(bot=bot, mod=ctx.author)
	elif isinstance(error, commands.NotOwner):
		await ctx.respond("Only <@" + "> and <@".join(str(id) for id in bot.owner_ids) + "> may use this command!", allowed_mentions=discord.AllowedMentions.none())
	elif isinstance(error, commands.MissingAnyRole):
		await ctx.respond(f"You require one of the following roles to use this command:\n<@&" + ">\n<@&".join(str(sus) for sus in error.missing_roles) + ">", allowed_mentions=discord.AllowedMentions.none())
	else:
		webhook = discord.Webhook.from_url(debughook, session=client.session2)
		await webhook.send(username=bot.user.name, avatar_url=bot.user.avatar.url,  content=f"{error}")


with open("token.txt") as token:
	bot.run(token.read())