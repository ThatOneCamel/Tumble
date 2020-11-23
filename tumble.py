#Cameron Thomas
#May 2019
#ThomasCameronT@gmail.com
ID_FILENAME = "users.dat"
SUBS_FILENAME = "creators.dat"
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

tumble_files.getUserInfo(ID_FILENAME)
tumble_files.getUserInfo(SUBS_FILENAME)

print("Users:")
print(tumble_files.getSubbedSet())
print("Creators:")
print(tumble_files.getCreatorSet())

#Starting Bot
tumble_bot.client.loop.create_task(tumble_bot.sendUpdate())
tumble_bot.client.run(tokenHere)
