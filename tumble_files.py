import urllib.request
import re

ID_FILENAME = "users.dat"
SUBS_FILENAME = "creators.dat"
creators = set()
subbedUsers = set()

def annyeong():
	hello = ["안녕", "World"]
	return hello

def helloWorld():
	return "Hello"

def getCreatorSet():
	return creators
	
def getSubbedSet():
	return subbedUsers
	
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
		postIDs = re.findall("https:\/\/" + creator + ".tumblr.com\/post\/([0-9]+)", page)
		#If bot breaks, add \/ to the end of the regex above
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
	filename = "./creators/" + creator + "_posts.txt"
	try:
		mFile = open(filename, "r")
		for post in mFile:
			oldSet.append(int(post))
		oldSet.sort()
		return oldSet
	except Exception as e:
		print(e)
		store(creator, list(getPage(creator)))
		oldSet = readData(creator)
		#print("Returned old set. Old set =")
		print(oldSet)
		return oldSet
		
		
def store(creator, posts):
	filename = "./creators/" + creator + "_posts.txt"
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
		message += creator + " has [" + str(len(newest)) + "] new post(s), here's their latest post:\n"
		message += newest[-1]
		#for item in newest:
			#message += item + "\n"
		return message
	else:
		return message


def addCreator(name):
	if name not in creators:
		creators.add(name)
		writeFile(SUBS_FILENAME)
	return
	
def removeCreator(name):
	if name in creators:
		creators.remove(name)
		writeFile(SUBS_FILENAME)
		return True
	return False
	
#End html scraper

# -----------------------------------



def addUser(uid):
	
	if uid not in subbedUsers:
		subbedUsers.add(uid)
		writeFile(ID_FILENAME)
		print("Successfully added " + str(uid) + " to userIDs [" + ID_FILENAME +"]")
		return True
	#End If in statement
	
	return False


def removeUser(uid):
	if uid in subbedUsers:
		subbedUsers.remove(uid)
		writeFile(ID_FILENAME)
		return True
	return False


def writeFile(filename):
	userFile = open(filename, "w+")
	
	if filename == ID_FILENAME:
		for user in subbedUsers:
			userFile.write(str(user) + "\n")
			
	elif filename == SUBS_FILENAME:
		for author in creators:
			userFile.write(str(author) + "\n")
			
	userFile.close()
	return

def getUserInfo(filename):
	try:
		userFile = open(filename, "r")
		
		if filename == ID_FILENAME:
			for uid in userFile:
				subbedUsers.add(int(uid))
			print("Retrieved Subscribed User IDs")
			
		elif filename == SUBS_FILENAME:
			for author in userFile:
				creators.add(author.strip())
			print("Retrieved Creator Subscriptions")

		userFile.close()
		return
	except Exception as e:
		print(e)
		print("File " + filename + " does not exist")
		return
