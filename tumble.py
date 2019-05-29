#Cameron Thomas
#May 2019
#ThomasCameronT@gmail.com

import discord
from discord.ext import commands
import urllib.request
import re
import asyncio

USER_ID = 'user_id_here'
CREATOR_A = "greatcheesecakepersona"
CREATOR_B = "midgethetree"
CREATOR_C = "deedee-sims" #Special Case
CREATOR_TEST = "shadowefx"

myCreator = CREATOR_C

def getPage(creator):
	try:
		#Get html from webpage
		url = ("https://" + creator + ".tumblr.com")
		response = urllib.request.urlopen(url)
		print("Established connection")
		data = response.read()
		page = data.decode("utf8")
		response.close()
		
		#Scan page for regex
		print("Scanning " + creator + "'s page for posts")
		postIDs = re.findall("https:\/\/" + creator + ".tumblr.com\/post\/([0-9]+)\/", page)
		
		#Converting strings to integers
		postIDs = [int(x) for x in set(postIDs)]
		postIDs.sort()
		return postIDs #returns set of postIDs
		
	except Exception as e:
		print(e)
		print("Failed to retrieve info from creator's webpage")
		fail = set()
		return fail

#Reads saved post data on system
def readData(creator):
	oldSet = list()
	filename = creator + "_posts.txt"
	try:
		mFile = open(filename, "r")
		for post in mFile:
			oldSet.append(int(post))
		oldSet.sort()
		return oldSet
	except Exception as e:
		print(e)
		store(creator, getPage(creator))
		oldSet = readData(creator)
		#print("Returned old set. Old set =")
		print(oldSet)
		return oldSet
		
		
def store(creator, posts):
	filename = creator + "_posts.txt"
	posts.sort()
	try:
		#Case file exists
		mFile = open(filename, "r")
		old = readData(creator)
		#print("OLD")
		#print(old)
		if old != posts:
			raise Exception("New post(s) added")
		else:
			print("No new posts found")
			#print("Old vs posts")
			#print(old)
			#print(posts)
		mFile.close()
	except Exception as e:
		#File does not exist or new posts are found
		print(e)
		mFile = open(filename, "w+")
		for item in posts:
			mFile.write(str(item) + "\n")
		mFile.close()
		print("Successfully updated file [" + mFile.name +"]")
		
def getLatestPosts(creator):
	existingPosts = set(readData(creator))
	newPosts = set(getPage(creator))
	#print("Inside beginning of latest posts")
	#print(newPosts)
	#print(existingPosts)
	
	updatedPosts = newPosts - existingPosts
	updatedPosts = list(updatedPosts)
	updatedPosts.sort()
	#print("UPDATED POSTS")
	#print(updatedPosts)
	if len(updatedPosts) is 0:
		#print("End empty list of latest posts")
		return list()
	else:
		store(creator, list(newPosts))
		addresses = list()
		for postID in updatedPosts:
			addresses.append("https://" + creator + ".tumblr.com/post/" + str(postID))
		#print("End addresses of latest posts")
		#print(addresses)
		return addresses


def checkForUpdates(creator):
	newest = getLatestPosts(creator)
	message = str()
	if len(newest) > 0:
		message += creator + " has posted recently, here's their latest post:\n"
		message += newest[-1]
		#for item in newest:
			#message += item + "\n"
		return message
	else:
		return message
#End html scraper

# -----------------------------------

#Tumble Code

#Creating an instance of the discord client for the bot
client = discord.Client()
client = commands.Bot(command_prefix='$')

async def sendUpdate():
	await client.wait_until_ready()
	#count = 0
	user = client.get_user(USER_ID)
	while client.is_closed:
		message = checkForUpdates(CREATOR_A)
		messageB = checkForUpdates(CREATOR_B)
		messageC = checkForUpdates(CREATOR_C)

		if message:
			await user.send(message)
		if messageB:
			await user.send(messageB)
		if messageC:
			await user.send(messageC)
		print("Waiting...")
		await asyncio.sleep(3600)
		#count +=1

@client.event
async def on_ready():
	#Bot is logged in
	print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
	#client.user being the bot itself in this case
	if message.author == client.user:
		return

	if message.content.startswith(client.command_prefix + 'hello'):
		user = client.get_user(USER_ID)
		await user.send('안녕')
		await message.channel.send('Hello!')

#Starting Bot
client.loop.create_task(sendUpdate())
client.run('TOKEN')
