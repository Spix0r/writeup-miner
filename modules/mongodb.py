import pymongo
from .Logger import logger
from .Notify import notify

def existdb(myclient):
    try:
        logger("Checking for Database existence.", "INF")
        dbnames = myclient.list_database_names()
        if "writeupminer" in dbnames:
            logger("Database Found.", "OK")
            return True
        logger("Database Not Found.", "ERR")
    except Exception as e:
        logger("{}".format(e), "ERR")
        exit(1)

def updateDatabase(mydb, new_feeds, exist):
    try:
        logger("Updating Database.", "INF")
        mycol = mydb["writeups"]
        if exist:
            logger("Removing previous collection.", "INF")
            mycol.drop()
        else:
            logger("Creating new collection.", "INF")
        for feed in new_feeds:
            mycol.insert_one({"url":feed['url']})
        logger("Database Updated.", "OK")
    except Exception as e:
        logger("{}".format(e), "ERR")
        exit(1)

def push_to_database(mydb, new_feed):
    try:
        logger("Pushing new posts to database.", "INF")
        mycol = mydb["writeups"]
        mycol.insert_one({"url":new_feed['url']})
        logger("Pushed new posts to database.", "OK")
    except Exception as e:
        logger("{}".format(e), "error")
        exit(1)


def check_database(mydb, new_feeds, token, chatid):
    try:
        logger("Checking for new posts.", "INF")
        mycol = mydb["writeups"]
        old_feeds = mycol.find({})
        urls = []
        for old_feed in old_feeds:
            urls.append(old_feed['url'])

        for new_feed in new_feeds:
            if new_feed["url"] not in urls:
                logger("New Feed Found : "+new_feed["title"], "OK")
                push_to_database(mydb, new_feed)
                notify(token, chatid, new_feed)
    except Exception as e:
        logger("{}".format(e), "ERR")
        exit(1)