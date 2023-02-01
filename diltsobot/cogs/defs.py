import discord, datetime, asyncio
import aiofiles
from discord.ext.prettyhelp import PrettyHelp
from discord import utils
from traceback import format_exception
loop = asyncio.get_event_loop()
from randseal import Client, BLANK
from discord.ext import commands
from enum import Enum

class ids(Enum):
	botlogchannel_TextChannel = 1070170166849175552
	modlogs_TextChannel = 1070214131464032356
	admin_Role = 1069941851920007248
	staff_Role = 1070177785915658403
	immune_Role = 1070207680045658213
	mod_Role = 1070177368397852813
	trial_Role = 1070177532026044436
	botdev_Role = 1070176520166965278
	member_Role = 1070213193550528562
	ender_Role = 1070176347860779078
	diltso_Role = 1070177146456260710
	override_Role = 1070220701556035604
	outputlog_Message = 1070226498910429204

client = Client()

class Bot(commands.Bot):
	"""Bot class cause yes"""
	def __init__(self):
		super().__init__(intents=discord.Intents.all(), command_prefix=commands.when_mentioned_or(
			"/"), help_command=PrettyHelp(color=BLANK, show_bot_perms=True, no_category="System"))
		with open('toggle.txt', 'w') as f:
			f.write("UwU")
		self.load_extensions("diltsobot.cogs.lockdown", "diltsobot.cogs.mass", "diltsobot.cogs.core", "diltsobot.cogs.managment", "jishaku")
		self.channels = Channels(self)
		self.ids = ids

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
				e = await self.channels.botlogchannel()
				await e.send(file=discord.File('error.err'), username=self.user.name, avatar_url=self.user.avatar.url)


class view(discord.ui.View):
	def __init__(self, **kwargs):
		super().__init__(timeout=256, **kwargs)
	@discord.ui.button(label="Stop", emoji="🛑")
	async def button_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
		await interaction.response.defer(ephemeral=True)
		await interaction.delete_original_response()


async def lockdownmodthing(bot: Bot, mod: discord.Member):
	"""Custom function that arrests a user"""
	staffrole = discord.Object(ids.staff_Role)
	trialmodrole = discord.Object(ids.trial_Role)
	modrole = discord.Object(ids.mod_Role)
	devrole = discord.Object(ids.botdev_Role)
	adminrole = discord.Object(ids.admin_Role)
	roles = {staffrole, trialmodrole, modrole, devrole, adminrole}
	for role in roles:
		try:
			await mod.remove_roles(role, reason="Mod lockdown")
		except:
			pass
	else:
		duration = datetime.timedelta(days=1)
		await mod.timeout_for(duration, reason="Mod lockdown")
		chan = await bot.channels.modlogchannel()
		await chan.send(embed=discord.Embed(colour=BLANK, title=f"{mod} arrested."))


class Channels:
	def __init__(self, bot: Bot):
		self.bot = bot

	async def botlogchannel(self) -> discord.TextChannel:
		return await utils.get_or_fetch(self.bot, "channel", ids.botlogchannel_TextChannel)

	async def modlogchannel(self) -> discord.TextChannel:
		return await utils.get_or_fetch(self.bot, "channel", ids.modlogs_TextChannel)

def needs_any_role(*items: int):
	idsa = list(items)
	idsa.append(ids.override_Role)
	original = commands.has_any_role(*idsa).predicate
	async def extended_check(ctx: discord.ApplicationContext) -> bool:
		if ctx.guild == None:
			return False
		return await original(ctx)
	return commands.check(extended_check)

async def get_or_fetch_message(channel: discord.TextChannel, id: int) -> discord.Message:
	return await utils.get_or_fetch(channel, "message", id)