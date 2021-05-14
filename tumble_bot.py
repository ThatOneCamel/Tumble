import discord
from discord.ext import commands
import asyncio
import subprocess
import importlib
import tumble_files
import os
from datetime import datetime
USER_ID = your_user_id
CREATOR_A = "greatcheesecakepersona"
CREATOR_B = "midgethetree"
CREATOR_C = "deedee-sims" #Special Case
CREATOR_TEST = "shadowefx"
ID_FILENAME = tumble_files.ID_FILENAME
SUBS_FILENAME = tumble_files.SUBS_FILENAME

#Creating an instance of the discord client for the bot
intents = discord.Intents.default()
intents.members = True

client = discord.Client()
client = commands.Bot(command_prefix='$', intents = intents)


startTime = datetime.now()


async def sendUpdate():
	#count = 0
	user = client.get_user(USER_ID)
	
	userset = set()
	for uid in tumble_files.getSubbedSet():
		userset.add(client.get_user(int(uid)))
		
	while not client.is_closed():
		for name in tumble_files.getCreatorSet():
			#print(name)
			message = tumble_files.checkForUpdates(name)
			if message and userset != set():
				for mUser in userset:
					await mUser.send(message)
			
		#message = checkForUpdates(CREATOR_A)
		#messageB = checkForUpdates(CREATOR_B)
		###if(c_enabled):
			#print("C = " + str(c_enabled))
			###messageC = checkForUpdates(CREATOR_C)

		"""if message:
			await user.send(message)
		if messageB:
			await user.send(messageB)
		if messageC and c_enabled:
			await user.send(messageC)"""
			
			
		print("Waiting...")
		await asyncio.sleep(3600)
		#count +=1

@client.event
async def on_ready():
	#Bot is logged in
	await client.wait_until_ready()
	print('Logged in as {0.user}'.format(client))
	await client.change_presence(activity=discord.Game(name='The Waiting Game'))
	client.loop.create_task(sendUpdate())

@client.event
async def on_message(message):

	#client.user being the bot itself in this case
	user = client.get_user(message.author.id)
	if message.author == client.user:
		return

	if message.content.startswith(client.command_prefix + 'hello'):
		#user = client.get_user(USER_ID)
		#myMod.printHello(user, message)
		await user.send(tumble_files.annyeong()[0])
		await message.channel.send(tumble_files.annyeong()[1])


	elif message.content.startswith(client.command_prefix + 'subscribe') or message.content.startswith(client.command_prefix + 'sub'):
		#myID = message.author.id
		#user = client.get_user(USER_ID)
		if tumble_files.addUser(message.author.id):
			await user.send("You have successfully been subscribed!")
		else:
			await user.send("You are already subscribed.")
		#client.loop.create_task(sendUpdate())
		
	elif message.content.startswith(client.command_prefix + 'who'):
		await user.send("You are subscribed to: " + ", ".join(tumble_files.getCreatorSet()))
		
		
	elif message.content.startswith(client.command_prefix + 'add'):
		if message.author.id not in tumble_files.getSubbedSet():
			await user.send("You must be subscribed to add a new creator.")
		else:
			mCreator = message.content.split(" ")[1]
			tumble_files.addCreator(mCreator)
			await user.send("Successfully added " + mCreator)
			
	
	elif message.content.startswith(client.command_prefix + 'remove'):
		if message.author.id not in tumble_files.getSubbedSet():
			await user.send("You must be subscribed to remove a creator.")
		else:
			mCreator = message.content.split(" ")[1]
			if tumble_files.removeCreator(mCreator):
				await user.send("Successfully removed " + mCreator)
			else:
				await user.send("There's no existing creator by [" + mCreator +"] in your subscription list. ")
		
		
	elif message.content.startswith(client.command_prefix + 'unsubscribe') or message.content.startswith(client.command_prefix + 'unsub'):
		if tumble_files.removeUser(message.author.id):
			await user.send("You have been unsubscribed from all notifications")
		else:
			await user.send("You were not subscribed.")
		
	elif message.content.startswith(client.command_prefix + 'kill') or message.content.startswith(client.command_prefix + 'seppuku'):
		if message.author.id == USER_ID:
			await user.send("Shutting down...")
			exit()
		else:
			await user.send("You're not authorized to run this command")
	
	
	elif message.content.startswith(client.command_prefix + 'time'):
		endTime = datetime.now()
		duration = endTime - startTime
		days, seconds = duration.days, duration.seconds
		hours = days * 24 + seconds // 3600
		minutes = (seconds % 3600) // 60
		seconds = seconds % 60
		
		await user.send("Start day was: " + startTime.strftime("%Y-%m-%d, %H:%M:%S"))
		await user.send("```It has been: {} days which is: {} hours, {} minutes, and {} seconds since Tumble began running```".format(days, hours, minutes, seconds))
		
	elif message.content.startswith(client.command_prefix + 'help'):
		#Base message
		helpMsg = "```\nWelcome to Tumble!\nHere are a list of useful commands:\n\n[General Commands]\n\t$subscribe - Adds you to our user subscription list\n\t$who - Prints out the creators you are subscribed to\n\t$add creatorName - Adds the specified creator to your subscription list\n\t$remove creatorName - Removes a creator from your subscription list\n\t$unsubscribe - Removes you from the subscription list\n\t$pull - Manually check blogs for updates"
		
		if message.author.id == USER_ID:
			#Base Message + Admin Commands
			helpMsg += "\n\n\n[Admin Commands]:\n\t$kill - Stops the Tumble process\n\t$hello - Debug Command\n\t$time - Returns how long the Tumble process has been running\n```"
			
		await user.send(helpMsg)
		
		
	elif message.content.startswith(client.command_prefix + 'pull'):
		print("Hard pull performed")
		foundUpdate = False
		for name in tumble_files.getCreatorSet():
			message = tumble_files.checkForUpdates(name)
			print(message)
			if message:
				await user.send(message)
				foundUpdate = True
		
		if not foundUpdate:
			await user.send("No updates found")
			
	elif message.content.startswith(client.command_prefix + 'status'):
		if message.author.id == USER_ID:
			print("Tumble ID: " + str(client.user.id))
			print("Author ID: " + str(message.author.id))
			print("DiscordPY Version: " + discord.__version__)
		else:
			await user.send("You're not authorized to run this command")
			
	elif message.content.startswith(client.command_prefix + 'reload'):
		importlib.reload(tumble_files)
		tumble_files.getUserInfo(ID_FILENAME)
		tumble_files.getUserInfo(SUBS_FILENAME)
		await user.send("tumble_files.py has been reloaded...")
		
	elif message.content.startswith(client.command_prefix + 'version'):
		await user.send("What's New?\n Can now edit tumble_files.py file without interrupting bot functions")
	
	elif message.content.startswith(client.command_prefix + 'safety'):
		tumble_files.getUserInfo(ID_FILENAME)
		tumble_files.getUserInfo(SUBS_FILENAME)


