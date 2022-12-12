import os
import shutil
import logging

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

standard_input = "help" 
if not len(open('output.log').read()) >= 1:
	logging.info(f"Started console")

command = input("Enter a command or help\n")
if command == "help":
	print("start - Starts the bot\ntoken [token] - Sets the bot token\nreset - Resets the entire bot")
	logging.info(f"Help command used")
	exec(open('main.py').read())

elif command == "start" or command == "run":
	if os.path.exists("token.txt"):
		logging.info(f"Starting up...")
		exec(open('bot.py').read())
	else:
		logging.info(f"Attempted startup but no token was set")
		print("Token is not set")
		exec(open('main.py').read())

elif command.startswith("token"):
	try:
		with open("token.txt", "w") as f1:
			f1.write(command.split()[1])
		with open("toggle.txt", "w") as f2:
			f2.write("UwU")
		logging.info(f"Token set")
		print('Set')
	except IndexError:
		os.remove('token.txt')
		logging.info("No token was provided to token command")
		print('No token was providied')
	finally:
		exec(open('main.py').read())

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
							exec(open('main.py').read())

else: 
	print("Unknown command")
	logging.info(f"Invalid command used")
	exec(open('main.py').read())