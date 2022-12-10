import os
import shutil
standard_input = "help" 

command = input("Enter a command or help\n")
if command == "help":
	print("start - Starts the bot\ntoken [token] - Sets the bot token\nreset - Resets the entire bot")
	exec(open('main.py').read())

elif command == "start":
	if os.path.exists("token.txt"):
		exec(open('bot.py').read())

elif command.startswith("token"):
	with open("token.txt", "w") as f1:
		f1.write(command.split()[1])
	with open("toggle.txt", "w") as f2:
		f2.write("UwU")
	exec(open('main.py').read())

elif command == "reset":
	os.remove("token.txt")
	os.remove("toggle.txt")
	os.remove("output.log")
	shutil.rmtree("stuff/__pycache__")
	shutil.rmtree("cogs/__pycache__")
	exec(open('main.py').read())

else: 
	print("Unknown command")
	exec(open('main.py').read())