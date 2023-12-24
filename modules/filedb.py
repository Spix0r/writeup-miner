from .Logger import logger
from .Notify import notify
import os

## Check if Database Exists

def makeDatabaseDir(dirname):
    try:
        os.makedirs(dirname)
        logger("DB Directory Created Successfully", "OK")
    except FileExistsError:
        logger("DB Directory Already Exists!", "INF")
    except Exception as e:
        logger(str(e), "ERR")

## Push into Database

def pushDatabase(data, filename):
    with open(filename,'w') as f:
        for i in data:
            f.write(i+"\n")

## Load Datbase

def loadDatabase(filename):
    try:
        with open(filename, 'r') as file:
            dataList = file.readlines()
            dataList = [data.strip() for data in dataList]
    except FileNotFoundError:
        logger(f"Error ! {filename} not found!", "ERR")
        exit(1)

    logger("File : {} loaded successfully.".format(filename), "OK")
    return dataList

## Check for new feeds

def checkDatabase(newFeeds, filename, token, chatid):
    oldFeeds = loadDatabase(filename)
    feedsToUpdate = oldFeeds
    counter = 0
    logger("Searching for new Feeds ...", "INF")
    for feed in newFeeds:
        if feed["url"].strip() not in oldFeeds:
            counter += 1
            logger("New feed found {}".format(feed["url"].strip()), "OK")
            notify(token, chatid, feed)
            feedsToUpdate.append(feed["url"].strip())
    pushDatabase(feedsToUpdate, filename)
    logger("Job done! Total New feeds found : {}".format(counter), "OK")

