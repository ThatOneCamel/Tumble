#Cameron Thomas
#May 2019 | May 2021
#ThomasCameronT@gmail.com
import importlib
import tumble_files
import tumble_bot

#Tumble Code

#c_enabled = True
#Data initialization
#postSet = getPage(myCreator)
#print("Post Set:")
#print(postSet)
#store(myCreator, postSet)

tumble_files.getUserInfo(tumble_files.ID_FILENAME)
tumble_files.getUserInfo(tumble_files.SUBS_FILENAME)

print("Subbed Users:")
print(tumble_files.getSubbedSet())
print("Creators:")
print(tumble_files.getCreatorSet())

#Starting Bot
tumble_bot.client.run(tokenHere)