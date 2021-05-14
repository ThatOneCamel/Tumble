#Cameron Thomas
#May 2019 | May 2021
#ThomasCameronT@gmail.com
import importlib
import tumble_files
import tumble_bot
import tweepy
#Tumble/Tweety Code

#c_enabled = True
#Data initialization
#postSet = getPage(myCreator)
#print("Post Set:")
#print(postSet)
#store(myCreator, postSet)

#tumble_files.getUserInfo(tumble_files.ID_FILENAME)
#tumble_files.getUserInfo(tumble_files.SUBS_FILENAME)

tumble_files.getUserInfo(tumble_files.TWITTER_FILENAME)
print("Current Twitter Account: " + tumble_bot.ACCOUNT_NAME)
#print(tumble_files.getCreatorSet())

#Starting Bot
tumble_bot.client.run('your_id_here')