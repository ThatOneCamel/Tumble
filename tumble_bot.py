import discord
from discord.ext import commands
import asyncio
import subprocess
import importlib
import tumble_files
import os
import tweepy
from datetime import datetime
USER_ID = 'optional_admin_user_id'
CHANNEL_ID = 'your_channel_id'

ACCOUNT_NAME="KuroEFX"
BOT_MESSAGE="rejoice lads, the best time of the week is finally upon us <:noBG:837408477126590464>"

#Creating an instance of the discord client for the bot
auth = tweepy.AppAuthHandler("secret","token")
api = tweepy.API(auth)

client = discord.Client()
client = commands.Bot(command_prefix='$')

startTime = datetime.now()


async def sendUpdate(channel):
	'''#count = 0
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
			
	'''
	while not client.is_closed():		
		try:
			if channel is not None:
				#Get Latest Tweet
				tweet = api.user_timeline(ACCOUNT_NAME, count = 1, tweet_mode = "extended", exclude_replies = True, include_rts = False)[0]
				tweet_link = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
				
				try:
					if tweet.id in tumble_files.readStoredTweets(tweet.user.screen_name):
						print("Found tweet in sentTweets. Will not send a message")
					elif BOT_MESSAGE != "":
						#Store the tweet then send the Discord message and tweet link
						tumble_files.storeTweet(tweet.user.screen_name, tweet.id)
						await channel.send(" {message} \n {tweet}".format(message = BOT_MESSAGE, tweet = tweet_link))
					else:
						#Otherwise just send the link.
						await channel.send(tweet_link)
				except Exception as e:
					print("Probably didn't have any tweets stored, continuing as usual")
					await channel.send(tweet_link)
			
			else:
				print('ERROR: Channel not found!')
		except tweepy.TweepError as e:
			print(e.response.text)
		print("Waiting...")
		await asyncio.sleep(3600)

@client.event
async def on_ready():
	#Bot is logged in
	await client.wait_until_ready()
	print('Logged in as {0.user}'.format(client))
	await client.change_presence(activity=discord.Game(name='The Waiting Game'))
	
	client.loop.create_task(sendUpdate(client.get_channel(CHANNEL_ID)))

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
		await user.send("```It has been: {} days which is: {} hours, {} minutes, and {} seconds since Tweety began running```".format(days, hours, minutes, seconds))
		
	elif message.content.startswith(client.command_prefix + 'help'):
		#Base message
		helpMsg = "```\nWelcome to Tweety!\nEverything should be handled automatically."
		
		if message.author.id == USER_ID:
			#Base Message + Admin Commands
			helpMsg += "\n\n\n[Admin Commands]:\n\t$kill - Stops the Tweety process\n\t$hello - Debug Command\n\t$time - Returns how long the Tumble process has been running\n```"
			
		await user.send(helpMsg)

	elif message.content.startswith(client.command_prefix + 'status'):
		if message.author.id == USER_ID:
			print("You are using the Twitter version of Tumble, TWEETY")
			print("Tumble ID: " + str(client.user.id))
			print("Author ID: " + str(message.author.id))
			print("DiscordPY Version: " + discord.__version__)
		else:
			await user.send("You're not authorized to run this command")
			
	elif message.content.startswith(client.command_prefix + 'reload'):
		if message.author.id == USER_ID:
			importlib.reload(tumble_files)
			tumble_files.getUserInfo(ID_FILENAME)
			tumble_files.getUserInfo(SUBS_FILENAME)
			tumble_files.getUserInfo(tumble_files.TWITTER_FILENAME)
			await user.send("tweety has been reloaded...")
		
	elif message.content.startswith(client.command_prefix + 'version'):
		await user.send("What's New?\n You're looking at it, Tweety!")
	
	elif message.content.startswith(client.command_prefix + 'safety'):
		tumble_files.getUserInfo(ID_FILENAME)
		tumble_files.getUserInfo(SUBS_FILENAME)
		tumble_files.getUserInfo(tumble_files.TWITTER_FILENAME)



