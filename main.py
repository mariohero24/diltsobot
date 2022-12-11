import os
import shutil
import logging

logging.basicConfig(filename="output.log", filemode="a", level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s",)

standard_input = "help" 

command = input("Enter a command or help\n")
if command == "help":
	print("start - Starts the bot\ntoken [token] - Sets the bot token\nreset - Resets the entire bot")
	exec(open('main.py').read())

elif command == "start" or command == "run":
	if os.path.exists("token.txt"):
		logging.info(f"Starting up...")
		exec(open('bot.py').read())
	else:
		print("Token is not set")
		exec(open('main.py').read())

elif command.startswith("token"):
	with open("token.txt", "w") as f1:
		f1.write(command.split()[1])
	with open("toggle.txt", "w") as f2:
		f2.write("UwU")
	exec(open('main.py').read())

elif command == "reset":
	os.remove("token.txt")
	os.remove("toggle.txt")
	shutil.rmtree("stuff/__pycache__")
	shutil.rmtree("cogs/__pycache__")
	exec(open('main.py').read())

else: 
	print("Unknown command")
	exec(open('main.py').read())