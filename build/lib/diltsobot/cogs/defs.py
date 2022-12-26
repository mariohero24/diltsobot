import discord, datetime
import advlink

from randseal import Client
from discord.ext import commands
client = Client()


debughook = advlink.Link("https://discord.com/api/webhooks/1047613860514889808/I7o2pJ-DhFRTo4mOwL4mTxxfM5hVSonF0J8M1kJhLDmT2WH--bnnZ56ngSIwWxqXBvpR")
loghook = advlink.Link("https://discord.com/api/webhooks/1047542583481618473/no81-OCBZmP8HVcUnjfGg_fJJg3Vslcb1w3YHas65924fRolQ5UrBgP4iq-4TZR2I2bd")

async def lockdownmodthing(bot: discord.Client, mod: discord.Member):
	"""Custom function that arrests a user"""
	staffrole = discord.Object(1015653001437909123)
	emojirole = discord.Object(1023379620348829696)
	trialmodrole = discord.Object(1020855698663411753)
	modrole = discord.Object(1000424453576073306)
	adrole = discord.Object(1016386365216272424)
	devrole = discord.Object(1047289657051840532)
	trialadminrole = discord.Object(1013266611970527253)
	adminrole = discord.Object(1008027971694633060)
	roles = [staffrole, emojirole, trialmodrole, modrole,
			adrole, devrole, trialadminrole, adminrole]
	for role in roles:
		try:
			await mod.remove_roles(role, reason="Mod lockdown")
		except:
			pass
	else:
		duration = datetime.timedelta(days=1)
		await mod.timeout_for(duration, reason="Mod lockdown")
		webhook = discord.Webhook.from_url(loghook.url, session=client.session2)
		await webhook.send(username=bot.user.name, avatar_url=bot.user.avatar.url, embed=discord.Embed(colour=client.blank, title=f"{mod} arrested."))