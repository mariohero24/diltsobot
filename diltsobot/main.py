import os
import shutil
import logging
from .bot import Bot
from importlib import resources, metadata

def console(token: str | None=None):
	"""Console function for... yeah idc"""
	bot = Bot()

	logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

	if not len(open('output.log').read()) >= 1:
		logging.info(f"Started console")

	command = input("Enter a command or help\n")

	if command == "help":
		print("start/run - Starts the bot.\ntoken [token] - Sets the bot token. Set the token to 'token' to use the token parmameter.\nreset - Resets the bot files.")
		logging.info(f"Help command used")
		with resources.open_text('diltsobot', 'main.py') as fp:
			exec(fp.read())

	elif command == "start" or command == "run":
		if os.path.exists("token.txt"):
			logging.info(f"Starting up...")
			with open('token.txt') as f:
				bot.run(f.read())
		else:
			logging.info(f"Attempted startup but no token was set")
			print("Token is not set")
			with resources.open_text('diltsobot', 'main.py') as fp:
				exec(fp.read())

	elif command.startswith("token"):
		tok = command.split()[1]
		if tok == "token":
			toke = token
		else:
			toke = tok
		try:
			with open('token.txt', 'w') as f:
				f.write(toke)
			logging.info(f"Token set")
			print('Set')
			with resources.open_text('diltsobot', 'main.py') as fp:
				exec(fp.read())
		except:
			os.remove('token.txt')
			logging.info("Something went wrong in setting the token")
			print("Something went wrong in setting the token")
			with resources.open_text('diltsobot', 'main.py') as fp:
				exec(fp.read())

	elif command == "reset":
		try:
			os.remove("token.txt")
		finally:
			try:
				os.remove("toggle.txt")
			finally:
				try:
					shutil.rmtree("stuff/__pycache__")
				finally:
					try:
						shutil.rmtree("cogs/__pycache__")
					finally:
						try:
							with open('output.log', 'w'):
								pass
						finally:
							try:
								logging.info('Reset files')
							finally:
								with resources.open_text('diltsobot', 'main.py') as fp:
									exec(fp.read())

	else: 
		print("Unknown command")
		logging.info(f"Invalid command used")

__version__: int = int(metadata.version('diltsobot'))